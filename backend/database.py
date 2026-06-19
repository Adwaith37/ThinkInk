from supabase import create_client
from dotenv import load_dotenv
import os
import hashlib
from backend.examples import get_default_examples_for_new_user

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


# ── User operations ──────────────────────────────

def load_user(user_id: str) -> dict:
    res = supabase.table("users").select("*").eq("user_id", user_id).execute()
    if res.data:
        user = res.data[0]
        chats_res = supabase.table("chats").select("*").eq("user_id", user_id).execute()
        chats = {}
        for chat in chats_res.data:
            chats[chat["chat_id"]] = {
                "topic": chat["topic"],
                "current_blog": chat["current_blog"],
                "history": chat["history"],
                "created_at": chat["created_at"]
            }
        return {
            "examples": user["examples"] or get_default_examples_for_new_user(),
            "preferences": user["preferences"] or {},
            "chats": chats,
            "current_chat_id": None
        }
    else:
        supabase.table("users").insert({
            "user_id": user_id,
            "examples": get_default_examples_for_new_user(),
            "preferences": {}
        }).execute()
        return {
            "examples": get_default_examples_for_new_user(),
            "preferences": {},
            "chats": {},
            "current_chat_id": None
        }
    


def hash_pin(pin: str) -> str:
    """Hash PIN before storing"""
    return hashlib.sha256(pin.encode()).hexdigest()

def create_user_with_pin(user_id: str, pin: str) -> bool:
    """Create new user with PIN"""
    hashed = hash_pin(pin)
    res = supabase.table("users").select("user_id").eq("user_id", user_id).execute()
    if res.data:
        return False  # User already exists
    supabase.table("users").insert({
        "user_id": user_id,
        "examples": get_default_examples_for_new_user(),
        "preferences": {},
        "current_chat_id": None,
        "pin": hashed
    }).execute()
    return True

def verify_pin(user_id: str, pin: str) -> bool:
    """Verify user PIN"""
    hashed = hash_pin(pin)
    res = supabase.table("users").select("pin").eq("user_id", user_id).execute()
    if not res.data:
        return False
    return res.data[0]["pin"] == hashed

def save_preferences(user_id: str, preferences: dict):
    supabase.table("users").update({
        "preferences": preferences
    }).eq("user_id", user_id).execute()

def get_preferences(user_id: str) -> dict:
    res = supabase.table("users").select("preferences").eq("user_id", user_id).execute()
    if res.data:
        return res.data[0]["preferences"] or {}
    return {}

def add_example(user_id: str, blog: str, category: str = "opinion",
                 style: str = "analytical", has_personal_voice: bool = False):
    from backend.rag import add_example_to_rag, delete_oldest_if_limit
    from datetime import datetime

    res = supabase.table("users").select("examples").eq("user_id", user_id).execute()
    examples = res.data[0]["examples"] if res.data else []

    example_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    delete_oldest_if_limit(user_id, max_examples=8)
    add_example_to_rag(user_id, blog, example_id, category, style, has_personal_voice)

    examples.append(blog)
    if len(examples) > 8:
        examples.pop(0)

    supabase.table("users").update({
        "examples": examples
    }).eq("user_id", user_id).execute()

# ── Chat operations ──────────────────────────────

def create_new_chat(user_id: str, topic: str) -> str:
    from datetime import datetime
    chat_id = datetime.now().strftime("%Y%m%d%H%M%S")

    # Ensure user exists
    load_user(user_id)

    supabase.table("chats").insert({
        "chat_id": chat_id,
        "user_id": user_id,
        "topic": topic,
        "current_blog": "",
        "history": [],
        "created_at": datetime.now().strftime("%d %b %Y, %H:%M")
    }).execute()

    # Track current chat in users table
    supabase.table("users").update({
        "current_chat_id": chat_id
    }).eq("user_id", user_id).execute()

    return chat_id

def set_current_chat(user_id: str, chat_id: str):
    supabase.table("users").update({
        "current_chat_id": chat_id
    }).eq("user_id", user_id).execute()

def get_current_blog(user_id: str) -> str:
    # Get current chat id
    res = supabase.table("users").select("current_chat_id").eq("user_id", user_id).execute()
    if not res.data or not res.data[0]["current_chat_id"]:
        return ""

    chat_id = res.data[0]["current_chat_id"]
    chat_res = supabase.table("chats").select("current_blog").eq("chat_id", chat_id).execute()
    if chat_res.data:
        return chat_res.data[0]["current_blog"] or ""
    return ""

def save_current_blog(user_id: str, blog: str):
    import json
    res = supabase.table("users").select("current_chat_id").eq("user_id", user_id).execute()
    if not res.data or not res.data[0]["current_chat_id"]:
        return

    chat_id = res.data[0]["current_chat_id"]

    # Get existing history
    chat_res = supabase.table("chats").select("history").eq("chat_id", chat_id).execute()
    history = chat_res.data[0]["history"] if chat_res.data else []
    history.append(blog)
    if len(history) > 5:
        history.pop(0)

    supabase.table("chats").update({
        "current_blog": blog,
        "history": history
    }).eq("chat_id", chat_id).execute()

def get_chat_blog(user_id: str, chat_id: str) -> str:
    res = supabase.table("chats").select("current_blog").eq("chat_id", chat_id).execute()
    if res.data:
        return res.data[0]["current_blog"] or ""
    return ""

def get_all_chats(user_id: str) -> list:
    res = supabase.table("chats").select("*").eq("user_id", user_id).order("chat_id", desc=True).execute()
    result = []
    for chat in res.data:
        result.append({
            "chat_id": chat["chat_id"],
            "topic": chat["topic"],
            "created_at": chat["created_at"],
            "current_blog": chat["current_blog"]
        })
    return result


def is_username_taken(user_id: str) -> bool:
    """Check if username already exists"""
    res = supabase.table("users").select("user_id").eq("user_id", user_id).execute()
    return bool(res.data)