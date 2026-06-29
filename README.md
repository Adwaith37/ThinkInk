# 🧠 ThinkInk

> An agentic AI blog generation platform that researches topics, retrieves personalized writing examples, evaluates its own output, and learns your writing style over time.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-green)
![Groq](https://img.shields.io/badge/LLM-Llama%203.3%2070B-orange)
![Pinecone](https://img.shields.io/badge/Vector%20DB-Pinecone-purple)
![Supabase](https://img.shields.io/badge/Database-Supabase-darkgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Screenshot



---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Demo](#demo)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Engineering Challenges](#engineering-challenges)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Overview

Most AI blog generators produce generic content because they treat every request independently — one prompt in, one blog out.

ThinkInk takes a different approach. It uses a **multi-stage agentic pipeline** where several AI components each handle a specific job: researching, generating, evaluating, and revising. The system also learns from user feedback over time, so each blog it produces becomes more aligned with the user's personal style.

---

## How It Works

No technical knowledge needed to understand this:

1. **You type a topic** — ThinkInk searches the web for current, accurate information about it
2. **It finds your style** — retrieves writing examples that match your category and voice from your personal library
3. **An AI writes a draft** — using the research and your style examples as context
4. **A second AI evaluates it** — scoring the draft across 8 quality dimensions
5. **A third AI fixes the weakest part** — targeting only what needs improvement, not rewriting everything
6. **The result streams to your screen** — word by word, like ChatGPT
7. **You refine it** — ask it to make it shorter, remove a section, change the tone — in plain language
8. **You accept it** — ThinkInk saves it as a style example and learns your preferences for next time

---

## Key Features

### 🤖 Multi-Agent Workflow

Three specialized AI agents work in sequence:

- **Generator Agent** — writes the initial blog using research and style examples
- **Evaluator Agent** — scores the blog across 8 dimensions and identifies the weakest one
- **Reviser Agent** — rewrites only the lowest-scoring dimension, not the whole piece

### 🔍 Category-Aware RAG (Retrieval-Augmented Generation)

RAG means the system retrieves relevant examples before generating — like giving a writer reference material before they start.

ThinkInk improves on basic RAG by tagging every example with:
- **Category** (travel, tech, professional, gaming, opinion, news)
- **Writing style** (storytelling, analytical, listicle, opinion)
- **Personal voice flag** (true/false)

This means a travel blog retrieves travel examples, not tech ones — and a personal experience piece retrieves first-person narrative examples specifically.

### 🌐 Real-Time Web Search with Smart Caching

Before generating any blog, ThinkInk searches the web for current information:

- **Serper** (Google-powered) as primary search
- **SearXNG** as an unlimited free fallback
- **Supabase cache** stores results — daily TTL for news topics, 7-day TTL for evergreen content
- Cache grows with usage, reducing API costs over time automatically

### 📊 8-Dimension Quality Evaluation

Every new blog is scored on:

| Dimension | What It Checks |
|---|---|
| SEO / Personal Voice | Keyword structure for general blogs; authentic first-person voice for personal pieces |
| Readability | Sentence variety, paragraph length, flow |
| Factual Integrity | No invented statistics or fabricated scenes |
| Tone | Human, confident, not robotic |
| Originality | Clear angle or stance, not a Wikipedia summary |
| Structure | Logical section ordering, single conclusion, smooth transitions |
| Engagement | Hook quality, concrete examples, reader interest |
| Preference Alignment | Match to the user's stored style preferences |

### 🧠 Automatic Preference Learning

When a user accepts a blog, three classifiers run automatically:
- **Category classifier** — what type of blog was this?
- **Style classifier** — what writing style does it use?
- **Preference extractor** — what tone, length, formatting, audience does this reflect?

These update a stored profile used to personalize every future generation.

### ✍️ Personal Experience Integration

Users can add their own memories or experiences before generating. The system treats that personal narrative as the structural spine of the article — not as an add-on. Generic FAQ and planning-guide content is automatically deprioritized when personal experience is present.

### 🔒 Production-Ready Architecture

- Per-user rate limiting stored in Supabase (survives server restarts)
- Bring-your-own Groq API key option (bypasses rate limit)
- SHA-256 hashed PINs
- Input validation and sanitization
- Token-efficient prompt trimming to prevent context overflow
- Search result caching to minimize API costs

---

## Technology Stack

| Layer | Technology | Why |
|---|---|---|
| Backend | FastAPI | Async support, streaming responses, clean API design |
| LLM | Groq (Llama 3.3 70B) | Fast inference, generous free tier |
| Vector Database | Pinecone | Scalable semantic search with metadata filtering |
| Database | Supabase (PostgreSQL) | Hosted Postgres for users, chats, rate limits, cache |
| Embeddings | sentence-transformers | Local embeddings, no extra API cost |
| Web Search | Serper + SearXNG | Google-quality results with an unlimited fallback |
| Frontend | Vanilla JS + HTML/CSS | No framework overhead, full control |
| Auth | Username + SHA-256 PIN | Simple, secure, per-user data isolation |

---

## Demo

**Live Application:**  https://thinkink-idr6.onrender.com/app

To try it:
1. Sign up with a username and a 4-digit PIN
2. Type any blog topic and hit Send
3. Refine the output with plain-language instructions ("make it shorter", "remove the FAQ")
4. Click Accept when happy — ThinkInk saves your style for next time
5. Bring your own free [Groq API key](https://console.groq.com) for unlimited generations

> Free accounts get **10 generations per day**. Resets at midnight.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Free accounts on: [Groq](https://console.groq.com), [Pinecone](https://pinecone.io), [Supabase](https://supabase.com), [Serper](https://serper.dev)

### Installation

```bash
# Clone the repo
git clone https://github.com/Adwaith37/ThinkInk.git
cd ThinkInk
```

```bash
# Create and activate virtual environment

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

```bash
# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_key
SERPER_API_KEY=your_serper_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=blog-agent
```

### Supabase Setup

Run this in your Supabase SQL editor:

```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    preferences JSONB DEFAULT '{}',
    examples JSONB DEFAULT '[]',
    current_chat_id TEXT DEFAULT NULL,
    pin TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE chats (
    chat_id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(user_id),
    topic TEXT,
    current_blog TEXT DEFAULT '',
    history JSONB DEFAULT '[]',
    created_at TEXT
);

CREATE TABLE rate_limits (
    user_id TEXT PRIMARY KEY,
    request_count INTEGER DEFAULT 0,
    reset_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE search_cache (
    topic_hash TEXT PRIMARY KEY,
    topic TEXT,
    result TEXT,
    cache_date DATE DEFAULT CURRENT_DATE
);

ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE chats DISABLE ROW LEVEL SECURITY;
ALTER TABLE rate_limits DISABLE ROW LEVEL SECURITY;
ALTER TABLE search_cache DISABLE ROW LEVEL SECURITY;
```

### Run Locally

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/app`

---

## Project Structure

```text
ThinkInk/
├── main.py                 # FastAPI app, all routes, classifier functions, pipeline orchestration
├── backend/
│   ├── prompt.py           # Prompt engineering with conditional rules per blog type
│   ├── evaluator.py        # 8-dimension evaluator + dimension-targeted reviser
│   ├── rag.py              # Pinecone operations — upsert, query, delete
│   ├── database.py         # All Supabase operations
│   ├── search.py           # Serper + SearXNG + smart cache logic
│   ├── preferences.py      # Preference extraction and prompt formatting
│   └── examples.py         # Categorized seed example library with metadata
├── frontend/
│   ├── index.html          # App UI — login, chat, sidebar
│   ├── style.css           # All styling
│   └── style.js            # Auth, streaming, experience panel, rate limit UI
├── docs/
│   ├── ARCHITECTURE.md     # Detailed technical architecture
│   └── screenshots/        # App screenshots
│       └── app.png         # Add after deployment
├── .env                    # API keys — never committed
├── .gitignore
└── requirements.txt
```

---

## Engineering Challenges

Real problems solved during development:

- **Prompt contradictions** — unconditional rules in prompts silently conflict; solved by generating conditional rule variants per blog type rather than one flat ruleset
- **RAG category sparsity** — with few examples per category, semantic search has nothing meaningful to select between; solved with metadata-filtered retrieval and a curated seed library
- **Evaluator-reviser communication** — passing a generic "improve quality" instruction to the reviser produced random changes; solved by passing the specific `dimension_to_fix` field so each revision pass is targeted
- **Token budget management** — long previous blogs and large example sets caused 413 errors; solved through prompt trimming at the RAG and previous-blog injection points
- **Fabricated statistics** — the LLM invents plausible-sounding numbers when forced by unconditional "include statistics" rules; solved by making statistics optional and conditional on research context availability
- **Personal voice dilution** — personal experience input was being paraphrased into generic travel-writing synonyms; solved by explicit priority ordering in the prompt and an anti-genericization instruction

---

## Future Improvements

- [ ] User analytics dashboard (acceptance rate, revision rate, category breakdown)
- [ ] Google OAuth login
- [ ] PDF and Word export for generated blogs
- [ ] Mobile-responsive UI
- [ ] Advanced retrieval reranking
- [ ] Preference-learning improvements based on usage patterns

---

## Detailed Documentation

For a full technical breakdown see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

Topics covered:
- Full pipeline architecture with data flow
- RAG design decisions
- Evaluator scoring weights and dimension design
- Preference learning implementation
- Prompt engineering decisions and tradeoffs

---

## Author

**Adwaith N** — [github.com/Adwaith37](https://github.com/Adwaith37)
