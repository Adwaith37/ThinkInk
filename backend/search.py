import requests
import json
from dotenv import load_dotenv
from backend.database import supabase
import os
import hashlib
from datetime import date

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def get_topic_hash(topic: str) -> str:
    return hashlib.md5(topic.lower().strip().encode()).hexdigest()

def get_cached_search(topic: str) -> str:
    try:
        topic_hash = get_topic_hash(topic)
        today = str(date.today())

        # Check if topic is evergreen or time-sensitive
        time_sensitive_keywords = [
            "today", "latest", "news", "2025", "2026",
            "current", "now", "recent", "this week",
            "breaking", "update", "live"
        ]

        is_time_sensitive = any(
            keyword in topic.lower() 
            for keyword in time_sensitive_keywords
        )

        if is_time_sensitive:
            # Daily cache for news/current events
            res = supabase.table("search_cache").select("*").eq(
                "topic_hash", topic_hash).eq(
                "cache_date", today).execute()
        else:
            # 7 day cache for evergreen topics
            from datetime import timedelta
            week_ago = str(date.today() - timedelta(days=7))
            res = supabase.table("search_cache").select("*").eq(
                "topic_hash", topic_hash).gte(
                "cache_date", week_ago).execute()

        if res.data:
            print(f"✅ Cache hit for: {topic}")
            return res.data[0]["result"]
        return ""
    except Exception as e:
        print(f"Cache read error: {e}")
        return ""

def save_search_cache(topic: str, result: str):
    try:
        topic_hash = get_topic_hash(topic)
        today = str(date.today())
        supabase.table("search_cache").upsert({
            "topic_hash": topic_hash,
            "topic": topic[:200],
            "result": result,
            "cache_date": today
        }).execute()
        print(f"💾 Cached search for: {topic}")
    except Exception as e:
        print(f"Cache save error: {e}")

def search_with_serper(topic: str) -> str:
    """Primary search using Serper (Google results)"""
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "q": topic,
                "num": 5
            }
        )
        data = response.json()

        context = "Key Facts:\n"

        # Answer box if available
        if "answerBox" in data:
            answer = data["answerBox"].get("answer") or data["answerBox"].get("snippet", "")
            if answer:
                context += f"Quick Answer: {answer}\n\n"

        # Knowledge graph
        if "knowledgeGraph" in data:
            kg = data["knowledgeGraph"]
            if "description" in kg:
                context += f"Overview: {kg['description']}\n\n"

        # Organic results
        organic = data.get("organic", [])
        for i, result in enumerate(organic[:4], 1):
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            context += f"{i}. {title}: {snippet}\n\n"

        return context.strip()

    except Exception as e:
        print(f"Serper error: {e}")
        return ""

def search_with_searxng(topic: str) -> str:
    """Fallback search using public SearXNG instance"""
    # List of reliable public instances
    instances = [
        "https://searx.be",
        "https://search.sapti.me",
        "https://searx.tiekoetter.com"
    ]

    for instance in instances:
        try:
            response = requests.get(
                f"{instance}/search",
                params={
                    "q": topic,
                    "format": "json",
                    "language": "en"
                },
                timeout=5
            )
            data = response.json()
            results = data.get("results", [])

            if not results:
                continue

            context = "Key Facts:\n"
            for i, result in enumerate(results[:4], 1):
                title = result.get("title", "")
                content = result.get("content", "")[:300]
                context += f"{i}. {title}: {content}\n\n"

            print(f"✅ SearXNG fallback worked: {instance}")
            return context.strip()

        except Exception:
            continue

    return ""

def search_topic(topic: str) -> str:
    """Main search function with caching + fallback"""

    # Check cache first
    cached = get_cached_search(topic)
    if cached:
        return cached

    print(f"🔍 Searching: {topic}")

    # Try Serper first
    result = search_with_serper(topic)
    if result:
        save_search_cache(topic, result)
        return result

    # Fallback to SearXNG
    print(f"⚠️ Serper failed, trying SearXNG...")
    result = search_with_searxng(topic)
    if result:
        save_search_cache(topic, result)
        return result

    print(f"❌ All search methods failed for: {topic}")
    return ""