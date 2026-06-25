# ThinkInk — Technical Architecture

This document covers the internal design of ThinkInk for engineers and technical readers.

For a high-level overview, see the [README](../README.md).

---

## System Overview

ThinkInk is a FastAPI backend serving a vanilla JS frontend. The core of the system is a multi-agent generation pipeline that runs on every blog request, orchestrated by `main.py`.

```
User Request (POST /generate)
        ↓
Input Validation
        ↓
API Key Resolution (user's key or shared key)
        ↓
Rate Limit Check (Supabase — skipped if user has own key)
        ↓
Category Classification (Groq, ~5 tokens)
        ↓
RAG Retrieval (Pinecone — filtered by category + personal voice)
        ↓
Preference Loading (Supabase)
        ↓
Web Search (Serper → SearXNG → Supabase cache)
        ↓
Prompt Assembly (conditional rules per blog type)
        ↓
Generator Agent (Groq Llama 3.3 70B, max_tokens=2200)
        ↓
Evaluator Agent (Groq — 8 dimensions, skipped for new users)
        ↓
Score < 7.5? → Reviser Agent (targets lowest dimension only)
        ↓
Stream to User (SSE, token by token)
        ↓
Save to Supabase
```

---

## Classifier Chain

ThinkInk uses four lightweight LLM classifiers, each returning a single word (max_tokens=5-10):

| Classifier | Input | Output | Used For |
|---|---|---|---|
| Follow-up detector | User instruction + previous blog | A or B | Skip search on refinements |
| Category classifier | Topic string | travel/tech/professional/gaming/opinion/news | RAG filtering, evaluator config |
| Style classifier | Accepted blog text | storytelling/analytical/listicle/opinion | Pinecone metadata tagging |
| Preference extractor | Accepted blog text | JSON object | User preference profile update |

All classifiers fall back to keyword matching if the Groq call fails.

---

## RAG Pipeline

### Embedding Model
`sentence-transformers/all-MiniLM-L6-v2` — runs locally, 384-dimensional vectors, cosine similarity.

### Storage
Each example is stored in Pinecone with the following metadata:

```json
{
  "blog": "first 2000 characters of blog text",
  "user_id": "user_xyz",
  "category": "travel",
  "style": "storytelling",
  "has_personal_voice": true
}
```

Each user has their own Pinecone namespace, so examples never cross between accounts.

### Retrieval Logic

```python
# Category filter applied first
filter_dict = {"category": {"$eq": category}} if category else {}

# Over-fetch if personal voice requested, then re-rank
n_results = top_k * 2 if prefer_personal_voice else top_k

results = index.query(
    vector=topic_embedding,
    top_k=n_results,
    filter=filter_dict,
    include_metadata=True
)

# Soft-prefer personal voice examples when user provided experience
if prefer_personal_voice:
    results.sort(key=lambda m: m.metadata.get("has_personal_voice"), reverse=True)
```

### Seed Examples
New users receive a curated set from `backend/examples.py` — 12 examples across all 6 categories and 4 styles, each tagged with full metadata. This prevents cold-start quality degradation.

---

## Prompt Architecture

The prompt in `backend/prompt.py` is conditionally assembled — not a fixed template.

### Conditional Rule Generation

```python
if has_experience:
    stats_rule = "Statistics are OPTIONAL — only include if present in research context"
    faq_rule = "FAQ is OMITTED by default — end with personal reflection instead"
else:
    stats_rule = "Include 3-5 specific statistics from research context"
    faq_rule = "End with a properly formatted FAQ section"
```

This solves a specific failure mode: unconditional rules create silent contradictions when multiple rules compete (e.g. "always include FAQ" vs "omit FAQ for personal blogs"). By generating one active version of each rule per request, no contradiction exists.

### Prompt Structure

```
[Role definition]
[Task — conditionally generated based on new/refinement/improve]
[Preferences section — if stored preferences exist]
[Personal experience section — if user provided input]
[Search context — if new topic and search returned results]
[Previous blog — trimmed to 1500 chars if exists]
[RAG examples — trimmed to 500 chars each]
[Conditional rules block — stats, FAQ, structure per blog type]
[General quality checklist — applies except where conditional rules override]
[Output rules]
```

### Token Budget Management

Three trimming points prevent 413 context overflow errors:

1. Previous blog trimmed to 1500 characters before injection
2. RAG examples trimmed to 500 characters each
3. Search context trimmed to 600 characters in evaluator/reviser calls

---

## Evaluator Design

### 8 Dimensions

| Dimension | Weight | Notes |
|---|---|---|
| SEO / Personal Voice | 0.20 | Switches based on has_personal_experience |
| Factual Integrity | 0.15 | Penalizes invented statistics harshly |
| Structure | 0.13 | Catches duplicate conclusions, section ordering |
| Readability | 0.12 | Sentence variety, paragraph length |
| Tone | 0.12 | Detects banned AI phrases |
| Originality | 0.12 | Unique angle, not Wikipedia summary |
| Engagement | 0.11 | Hook quality, examples, reader interest |
| Preference Alignment | 0.05 | Match to stored user preferences |

### Revision Targeting

The evaluator returns a `dimension_to_fix` field (the single lowest-scoring dimension) and a `revision_instruction` (one specific change). The reviser receives both, plus a pre-written focus statement per dimension:

```python
dimension_guidance = {
    "structure": "Focus ONLY on structural issues: ensure there is only one conclusion section...",
    "factual_integrity": "Focus ONLY on removing statistics not present in research context...",
    "engagement": "Focus ONLY on strengthening the opening hook and adding one concrete example...",
    ...
}
```

This prevents the reviser from making random changes and ensures each revision pass is surgical rather than a full rewrite.

---

## Search Architecture

```
search_topic(topic)
      ↓
get_cached_search(topic)  ← Supabase lookup by MD5 hash of topic
      ↓ cache miss
is_time_sensitive?
  Yes → daily TTL cache
  No  → 7-day TTL cache
      ↓
search_with_serper(topic)  ← Google via Serper API
      ↓ fails or no results
search_with_searxng(topic) ← Public SearXNG instances (3 tried in order)
      ↓
save_search_cache(topic, result)
```

Cache keys are MD5 hashes of the normalized topic string. Time-sensitive detection uses keyword matching (today, latest, 2026, breaking, etc.).

---

## Database Schema

### users
```sql
user_id TEXT PRIMARY KEY
preferences JSONB DEFAULT '{}'      -- extracted preference profile
examples JSONB DEFAULT '[]'         -- backup of accepted blogs (max 8)
current_chat_id TEXT                -- active chat session
pin TEXT                            -- SHA-256 hashed
created_at TIMESTAMP
```

### chats
```sql
chat_id TEXT PRIMARY KEY
user_id TEXT REFERENCES users
topic TEXT
current_blog TEXT                   -- latest generated blog
history JSONB DEFAULT '[]'          -- last 5 blog versions
created_at TEXT
```

### rate_limits
```sql
user_id TEXT PRIMARY KEY
request_count INTEGER DEFAULT 0
reset_date DATE DEFAULT CURRENT_DATE  -- resets at midnight
```

### search_cache
```sql
topic_hash TEXT PRIMARY KEY         -- MD5 of normalized topic
topic TEXT                          -- original topic string
result TEXT                         -- search context string
cache_date DATE                     -- used for TTL comparison
```

---

## Authentication

ThinkInk uses username + PIN authentication:

1. Username is normalized to `user_{lowercase_name}` for consistent ID generation
2. PIN is hashed with SHA-256 before storage — never stored in plaintext
3. Separate `/signup` and `/signin` endpoints prevent username collision
4. Per-user Pinecone namespaces ensure complete data isolation between accounts
5. Optional user-supplied Groq API key stored in browser localStorage only — never persisted server-side

---

## Rate Limiting

Rate limits are stored in Supabase rather than application memory, so they survive server restarts (critical on free-tier hosting with frequent cold starts):

```python
def check_rate_limit(user_id: str) -> bool:
    today = str(date.today())
    record = supabase.table("rate_limits").select("*").eq("user_id", user_id).execute()

    if record["reset_date"] != today:
        # New day — reset counter
        update count to 1
        return True

    if count >= MAX_REQUESTS_PER_USER_PER_DAY:
        return False

    increment count
    return True
```

Users who supply their own Groq API key bypass rate limiting entirely.

---

## Streaming

Blog content is streamed to the frontend using Server-Sent Events (SSE):

```python
def stream_blog():
    for char in final_blog:
        yield f"data: {json.dumps({'token': char})}\n\n"
    yield f"data: {json.dumps({'done': True})}\n\n"

return StreamingResponse(stream_blog(), media_type="text/event-stream")
```

The frontend reads the stream using the Fetch API's `ReadableStream`:

```javascript
const reader = res.body.getReader()
while (true) {
    const { done, value } = await reader.read()
    if (done) break
    // parse SSE tokens and append to message bubble
}
```

Markdown is rendered in real time using `marked.js` as tokens arrive.

---

## Key Design Decisions

**Why Groq instead of OpenAI?**
Speed and free tier generosity. Llama 3.3 70B on Groq's custom hardware produces responses fast enough for streaming to feel responsive.

**Why Pinecone instead of ChromaDB?**
ChromaDB is local — it resets on every cloud deploy. Pinecone is hosted and persists across deployments.

**Why Supabase instead of local JSON files?**
Same reason — local files don't survive cloud server restarts. Supabase gives hosted PostgreSQL with a generous free tier.

**Why sentence-transformers locally instead of an embedding API?**
Eliminates a fourth paid API dependency. all-MiniLM-L6-v2 is small enough to run on a free-tier server without meaningful latency.

**Why not use a framework like LangChain?**
Direct Groq API calls give full control over token usage, retry logic, and streaming behavior. Framework abstractions add overhead and make debugging harder when prompt engineering requires tight iteration.
