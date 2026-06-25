from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.database import (load_user, add_example, save_current_blog,
                               get_current_blog, create_new_chat, get_all_chats,
                               set_current_chat, get_chat_blog,
                               get_preferences, save_preferences, supabase,
                               create_user_with_pin, verify_pin, is_username_taken)
from backend.rag import retrieve_relevant_examples, get_example_count
from backend.prompt import build_prompt
from backend.search import search_topic
from backend.evaluator import run_evaluation_pipeline
from backend.preferences import (extract_preferences, merge_preferences,
                                  format_preferences_for_prompt)
from backend.examples import CATEGORIES
from groq import Groq
from datetime import date
import json
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MAX_REQUESTS_PER_USER_PER_DAY = 10
STYLES = ["storytelling", "analytical", "listicle", "opinion"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")


# ── Auth ──────────────────────────────────────────

class AuthRequest(BaseModel):
    user_id: str
    pin: str

@app.post("/signup")
def signup(request: AuthRequest):
    """Create new account — fails if username already taken"""
    created = create_user_with_pin(request.user_id, request.pin)
    if not created:
        raise HTTPException(
            status_code=409,
            detail="Username already taken! Please choose a different one."
        )
    return {"status": "created", "message": "Account created successfully!"}

@app.post("/signin")
def signin(request: AuthRequest):
    """Login to an existing account"""
    if not is_username_taken(request.user_id):
        raise HTTPException(
            status_code=404,
            detail="Username not found. Please sign up first!"
        )
    if verify_pin(request.user_id, request.pin):
        return {"status": "success", "message": "Login successful!"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect PIN. Try again!")


# ── Rate Limiting (Supabase) ─────────────────────

def check_rate_limit(user_id: str) -> bool:
    today = str(date.today())
    res = supabase.table("rate_limits").select("*").eq("user_id", user_id).execute()

    if not res.data:
        supabase.table("rate_limits").insert({
            "user_id": user_id, "request_count": 1, "reset_date": today
        }).execute()
        return True

    record = res.data[0]
    if record["reset_date"] != today:
        supabase.table("rate_limits").update({
            "request_count": 1, "reset_date": today
        }).eq("user_id", user_id).execute()
        return True

    if record["request_count"] >= MAX_REQUESTS_PER_USER_PER_DAY:
        return False

    supabase.table("rate_limits").update({
        "request_count": record["request_count"] + 1
    }).eq("user_id", user_id).execute()
    return True


def get_remaining_requests(user_id: str) -> int:
    today = str(date.today())
    res = supabase.table("rate_limits").select("*").eq("user_id", user_id).execute()

    if not res.data:
        return MAX_REQUESTS_PER_USER_PER_DAY

    record = res.data[0]
    if record["reset_date"] != today:
        return MAX_REQUESTS_PER_USER_PER_DAY

    return max(0, MAX_REQUESTS_PER_USER_PER_DAY - record["request_count"])


# ── Classifiers ───────────────────────────────────

SKIP_SEARCH_KEYWORDS = [
    "make it", "make this", "make the",
    "shorter", "longer", "simpler", "bigger", "smaller",
    "formal", "informal", "casual", "professional", "friendly",
    "detailed", "more detailed", "less detailed",
    "add more", "add a", "add some", "add this", "add that",
    "remove", "delete", "cut", "rewrite", "improve",
    "change", "fix", "update", "edit", "tone", "rephrase",
    "summarize", "expand", "condense", "simplify",
    "more", "less", "better", "deeper", "broader",
    "include", "exclude", "replace", "large", "small",
    "brief", "lengthy", "concise", "short", "long",
    "extend", "shorten", "enhance", "refine",
    "more engaging", "more interesting", "more specific",
    "more human", "less robotic", "more natural",
    "the blog", "the article", "the post", "paragraph",
    "section", "introduction", "conclusion", "heading"
]


def is_followup_instruction(instruction: str, previous_blog: str, api_key: str) -> bool:
    if not previous_blog or not instruction:
        return False

    client = Groq(api_key=api_key)
    classify_prompt = f"""You are a classifier. Analyze the user input and decide if it is:
A) A follow-up instruction to refine/modify an existing blog
B) A completely new blog topic request

Previous blog exists: YES
User input: "{instruction}"

Examples of follow-up instructions (A):
- "make it shorter", "i want it bigger", "add more details"
- "too formal, make it casual", "the conclusion is weak"
- "add statistics", "more engaging please", "remove the last section"
- "sounds robotic", "large", "detailed", "not good enough"
- "more depth", "expand this", "i dont like the intro"

Examples of new topic requests (B):
- "write about climate change", "quantum computing"
- "best travel destinations in 2026", "how does blockchain work"
- Any proper noun, place name, organization name, or topic that is unrelated to editing

KEY RULE: If the input looks like a topic, subject, place, organization, person, or event 
rather than an editing instruction, classify it as B even if it is short.
Short inputs are NOT automatically follow-up instructions.

Respond with ONLY one word: A or B"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": classify_prompt}],
            max_tokens=5
        )
        result = response.choices[0].message.content.strip().upper()
        print(f" Classification: '{instruction}' → {result}")
        return result == "A"
    except Exception as e:
        print(f"Classifier error: {e}")
        return any(keyword in instruction.lower() for keyword in SKIP_SEARCH_KEYWORDS)


def classify_category(topic: str, api_key: str) -> str:
    client = Groq(api_key=api_key)
    classify_prompt = f"""Classify this blog topic into exactly ONE category.

Topic: "{topic}"

Categories:
- travel (trips, destinations, travel experiences)
- tech (technology, AI, software, science)
- professional (career, business, corporate, workplace)
- gaming (video games, reviews, gaming culture)
- opinion (thought-leadership, predictions, takes on a subject)
- news (current events, comparisons, listicles on trending topics)

Respond with ONLY the category word, nothing else."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": classify_prompt}],
            max_tokens=5
        )
        result = response.choices[0].message.content.strip().lower()
        if result in CATEGORIES:
            print(f" Category detected: {result}")
            return result
        return "opinion"
    except Exception as e:
        print(f"Category classifier error: {e}")
        return "opinion"


def classify_style(blog: str, api_key: str) -> str:
    client = Groq(api_key=api_key)
    classify_prompt = f"""Classify the dominant writing style of this blog into exactly ONE category.

Blog (first part):
{blog[:800]}

Styles:
- storytelling (narrative-driven, anecdote-led, first-person journey)
- analytical (explains how/why something works, structured breakdown)
- listicle (numbered or bulleted list format as the main structure)
- opinion (argues a stance, makes a prediction or judgment)

Respond with ONLY the style word, nothing else."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": classify_prompt}],
            max_tokens=5
        )
        result = response.choices[0].message.content.strip().lower()
        if result in STYLES:
            print(f" Style detected: {result}")
            return result
        return "analytical"
    except Exception as e:
        print(f"Style classifier error: {e}")
        return "analytical"


def should_search(topic: str, instruction: str, previous_blog: str, api_key: str) -> bool:
    if not previous_blog or len(previous_blog.strip()) < 50:
        if topic and topic.strip():
            return True
        return False
    if instruction and instruction.strip():
        followup = is_followup_instruction(instruction, previous_blog, api_key)
        return not followup
    return False


def validate_input(topic: str, instruction: str) -> str:
    combined = (topic + instruction).strip()
    if not combined:
        return "Please provide a topic or instruction"
    if len(combined) > 2000:
        return "Input too long. Please keep it under 2000 characters"
    return ""


# ── Models ───────────────────────────────────────

class BlogRequest(BaseModel):
    user_id: str
    topic: str = ""
    instruction: str = ""
    accept: bool = False
    chat_id: str = ""
    personal_experience: str = ""
    groq_api_key: str = ""

class ChatRequest(BaseModel):
    user_id: str
    topic: str

class SwitchChatRequest(BaseModel):
    user_id: str
    chat_id: str


# ── Routes ───────────────────────────────────────

@app.get("/")
def home():
    return {"message": "Blog agent is running"}

@app.get("/app")
def serve_frontend():
    return FileResponse("frontend/index.html")

@app.post("/new_chat")
def new_chat(request: ChatRequest):
    chat_id = create_new_chat(request.user_id, request.topic)
    return {"chat_id": chat_id}

@app.post("/switch_chat")
def switch_chat(request: SwitchChatRequest):
    set_current_chat(request.user_id, request.chat_id)
    blog = get_chat_blog(request.user_id, request.chat_id)
    return {"blog": blog}

@app.get("/chats/{user_id}")
def get_chats(user_id: str):
    chats = get_all_chats(user_id)
    return {"chats": chats}

@app.get("/remaining/{user_id}")
def remaining_requests(user_id: str):
    remaining = get_remaining_requests(user_id)
    return {"remaining": remaining, "limit": MAX_REQUESTS_PER_USER_PER_DAY}


@app.post("/generate")
def generate_blog(request: BlogRequest):

    error = validate_input(request.topic, request.instruction)
    if error:
        raise HTTPException(status_code=400, detail=error)

    using_own_key = bool(request.groq_api_key and request.groq_api_key.startswith("gsk_"))
    active_api_key = request.groq_api_key if using_own_key else GROQ_API_KEY

    if not using_own_key:
        if not check_rate_limit(request.user_id):
            raise HTTPException(
                status_code=429,
                detail=f"You've reached your daily limit of {MAX_REQUESTS_PER_USER_PER_DAY} blogs. "
                       f"Come back tomorrow or add your free Groq key for unlimited access! "
            )
    else:
        print(f" Using user's own Groq key — no rate limit")

    user_data = load_user(request.user_id)
    previous_blog = get_current_blog(request.user_id)

    category = None
    if not previous_blog or len(previous_blog.strip()) < 50:
        category = classify_category(request.topic, active_api_key)

    rag_examples = retrieve_relevant_examples(
        user_id=request.user_id,
        topic=request.topic,
        category=category,
        prefer_personal_voice=bool(request.personal_experience),
        top_k=3
    )
    if not rag_examples:
        rag_examples = user_data.get("examples", [])

    # Trim examples to prevent prompt bloat
    if rag_examples:
        rag_examples = [ex[:500] for ex in rag_examples]

    preferences = get_preferences(request.user_id)
    preferences_text = format_preferences_for_prompt(preferences)
    if preferences_text:
        print(f" Using preferences: {preferences.get('preferred_tone', 'default')}")

    search_context = ""
    if should_search(request.topic, request.instruction, previous_blog, active_api_key):
        print(f" Searching web for: {request.topic}")
        search_context = search_topic(request.topic)
    else:
        print(f"Skipping search — refinement mode")

    prompt = build_prompt(
        topic=request.topic,
        examples=rag_examples,
        instruction=request.instruction,
        previous_blog=previous_blog,
        search_context=search_context,
        preferences_text=preferences_text,
        personal_experience=request.personal_experience
    )

    client = Groq(api_key=active_api_key)

    example_count = get_example_count(request.user_id)
    should_evaluate = example_count > 0

    def stream_blog():
        try:
            print(" Generating initial blog...")
            initial_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000
            )
            initial_blog = initial_response.choices[0].message.content.strip()

            if should_evaluate and (not previous_blog or not request.instruction):
                print(" Running evaluation pipeline...")
                final_blog, scores = run_evaluation_pipeline(
                blog=initial_blog,
                topic=request.topic,
                search_context=search_context,
                api_key=active_api_key,
                max_revisions=2,
                has_personal_experience=bool(request.personal_experience),
                personal_experience=request.personal_experience,
                blog_category=category or "general",
                preferences_text=preferences_text  
                )
                primary = scores.get("primary_dimension", {})
                readability = scores.get("readability", {}).get("score", 0)
                factual = scores.get("factual_integrity", {}).get("score", 0)
                structure = scores.get("structure", {}).get("score", 0)
                engagement = scores.get("engagement", {}).get("score", 0)
                overall = scores.get("overall_score", 0)
                primary_name = primary.get("name", "quality").upper()
                primary_score = primary.get("score", 0)
                score_badge = (f"\n\n---\n✨ **AI Evaluated** · {primary_name} {primary_score}/10 · "
                                f"Readability {readability}/10 · Structure {structure}/10 · "
                                f"Engagement {engagement}/10 · Factual {factual}/10 · "
                                f"Overall {overall}/10")
            else:
                final_blog = initial_blog
                score_badge = ""
                if not should_evaluate:
                    print(" Skipping evaluation — new user, saving tokens")

            for char in final_blog:
                yield f"data: {json.dumps({'token': char})}\n\n"

            if score_badge:
                for char in score_badge:
                    yield f"data: {json.dumps({'token': char})}\n\n"

            remaining = get_remaining_requests(request.user_id)
            remaining_msg = f"\n\n* {remaining} generations remaining today*"
            for char in remaining_msg:
                yield f"data: {json.dumps({'token': char})}\n\n"

            save_current_blog(request.user_id, final_blog)
            if request.accept:
                add_example(request.user_id, final_blog,
                            category=category or "opinion",
                            style="analytical",
                            has_personal_voice=bool(request.personal_experience))

            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            print(f"Pipeline error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(stream_blog(), media_type="text/event-stream")


@app.post("/accept")
def accept_blog(request: BlogRequest):
    blog = get_current_blog(request.user_id)
    if blog:
        using_own_key = bool(request.groq_api_key and request.groq_api_key.startswith("gsk_"))
        active_api_key = request.groq_api_key if using_own_key else GROQ_API_KEY

        category = classify_category(request.topic or blog[:200], active_api_key)
        style = classify_style(blog, active_api_key)
        has_voice = bool(request.personal_experience)

        add_example(request.user_id, blog, category=category,
                    style=style, has_personal_voice=has_voice)

        print(" Extracting preferences from accepted blog...")
        new_prefs = extract_preferences(blog, active_api_key)
        if new_prefs:
            existing_prefs = get_preferences(request.user_id)
            merged = merge_preferences(existing_prefs, new_prefs)
            save_preferences(request.user_id, merged)
            print(f" Preferences updated: {merged.get('preferred_tone', 'unknown')} tone")

    return {"status": "saved"}