from groq import Groq
import json

def extract_preferences(blog: str, api_key: str, model: str = "openai/gpt-oss-120b") -> dict:
    """Silently extract writing preferences from an accepted blog"""
    
    client = Groq(api_key=api_key)
    
    extract_prompt = f"""You are an expert content analyst. Analyze this blog and extract the author's writing preferences.

BLOG:
{blog}

Return ONLY a JSON object with these exact fields, nothing else:

{{
    "preferred_tone": "one of: formal, informal, casual, authoritative, conversational, technical, friendly",
    "blog_length": "one of: short (300-500 words), medium (600-900 words), long (1000+ words)",
    "cta_style": "one of: question to reader, call to action, summary statement, open ended, none",
    "formatting": {{
        "uses_headings": true or false,
        "uses_bullet_points": true or false,
        "uses_bold_text": true or false,
        "uses_statistics": true or false,
        "uses_examples": true or false
    }},
    "industries": ["list", "of", "detected", "industries"],
    "audience_type": "one of: general public, professionals, students, enthusiasts, executives, developers",
    "writing_style": "one of: storytelling, analytical, listicle, educational, opinion, news",
    "avg_paragraph_length": "one of: short, medium, long"
}}

Return ONLY the JSON, no explanation, no preamble."""

    try:
        response = client.chat.completions.create(
            model= model,
            messages=[{"role": "user", "content": extract_prompt}],
            max_tokens=500
        )
        
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        
        result = json.loads(raw)
        print(f"✅ Preferences extracted: {result}")
        return result
        
    except Exception as e:
        print(f"Preference extraction error: {e}")
        return {}


def merge_preferences(existing: dict, new: dict) -> dict:
    """
    Merge new preferences with existing ones.
    Most recent accepted blogs have more weight.
    """
    if not existing:
        return new
    if not new:
        return existing

    merged = existing.copy()

    # Update simple string fields with latest value
    for key in ["preferred_tone", "blog_length", "cta_style", 
                "audience_type", "writing_style", "avg_paragraph_length"]:
        if key in new:
            merged[key] = new[key]

    # Merge formatting — True wins (if user ever used it, keep it)
    if "formatting" in new and "formatting" in existing:
        merged["formatting"] = {
            k: existing["formatting"].get(k, False) or new["formatting"].get(k, False)
            for k in new["formatting"]
        }
    elif "formatting" in new:
        merged["formatting"] = new["formatting"]

    # Merge industries — keep unique list, max 5
    existing_industries = existing.get("industries", [])
    new_industries = new.get("industries", [])
    combined = list(set(existing_industries + new_industries))
    merged["industries"] = combined[:5]

    return merged


def format_preferences_for_prompt(preferences: dict) -> str:
    """Convert preferences dict into a clean prompt string"""
    if not preferences:
        return ""

    lines = ["--- User Preferences (follow these strictly) ---"]

    if preferences.get("preferred_tone"):
        lines.append(f"Tone: {preferences['preferred_tone']}")

    if preferences.get("blog_length"):
        lines.append(f"Length: {preferences['blog_length']}")

    if preferences.get("cta_style"):
        lines.append(f"Ending style: {preferences['cta_style']}")

    if preferences.get("audience_type"):
        lines.append(f"Target audience: {preferences['audience_type']}")

    if preferences.get("writing_style"):
        lines.append(f"Writing style: {preferences['writing_style']}")

    if preferences.get("industries"):
        lines.append(f"Industries/topics: {', '.join(preferences['industries'])}")

    formatting = preferences.get("formatting", {})
    format_notes = []
    if formatting.get("uses_headings"):
        format_notes.append("use H2/H3 headings")
    if formatting.get("uses_bullet_points"):
        format_notes.append("use bullet points")
    if formatting.get("uses_bold_text"):
        format_notes.append("use bold for key terms")
    if formatting.get("uses_statistics"):
        format_notes.append("include statistics where relevant")
    if formatting.get("uses_examples"):
        format_notes.append("include real examples")
    if format_notes:
        lines.append(f"Formatting: {', '.join(format_notes)}")

    if preferences.get("avg_paragraph_length"):
        lines.append(f"Paragraph length: {preferences['avg_paragraph_length']}")

    lines.append("--- End of Preferences ---")

    return "\n".join(lines)