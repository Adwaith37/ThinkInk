from groq import Groq
import json


def evaluate_blog(blog: str, topic: str, search_context: str,
                  api_key: str, model: str = "openai/gpt-oss-120b",
                  has_personal_experience: bool = False,
                  blog_category: str = "general",
                  preferences_text: str = "") -> dict:
    """Evaluate blog quality across 8 dimensions, accounting for blog type and user preferences."""

    client = Groq(api_key=api_key)

    if has_personal_experience:
        stats_guidance = """- Factual Integrity (0-10): PENALIZE heavily if the blog contains statistics, survey results, or percentages NOT in the research context. A personal experience blog with NO statistics is fine and should score 8-9 if the narrative is authentic. INVENTED statistics score 2-3 regardless of how specific they sound. Fabricated scenes the author never described score 1-3."""
        faq_guidance = "- Do NOT penalize absence of FAQ. Personal blogs should end with personal reflection. PENALIZE if a generic planning/FAQ section exists when the author's input was purely experiential."
        primary_dimension = "personal_voice"
        primary_guidance = """- Personal Voice (0-10): Does the blog sound like a real person's genuine memory? High scores (8-10): specific named places/activities the author mentioned, author's actual opinions preserved in their spirit not softened into generic praise, narrative anchored in the author's framing. Low scores (1-4): reads like a generic destination guide written in first person, invented activities or scenes the author never described, personal details replaced with generic travel-writing synonyms."""
    else:
        stats_guidance = """- Factual Integrity (0-10): Score on accuracy against research context. PENALIZE invented statistics not present in research context. Reward specific, accurate, verifiable claims."""
        faq_guidance = "- REWARD presence of FAQ section, clear H2/H3 structure, scannable format."
        primary_dimension = "seo"
        primary_guidance = """- SEO (0-10): keyword usage in title and first paragraph, heading structure (H1/H2/H3 hierarchy), meta-friendly introduction, scannable format with bullets and bold."""

    preferences_guidance = f"""
USER STYLE PREFERENCES (check whether the blog honored these):
{preferences_text}
Score Preference Alignment on how closely the blog matched these stored preferences.
If no preferences provided, score 7 as neutral.""" if preferences_text else """
USER STYLE PREFERENCES: None stored yet. Score Preference Alignment at 7 (neutral)."""

    eval_prompt = f"""You are an expert blog evaluator. Evaluate strictly and objectively.

BLOG TYPE: {"Personal experience / first-person narrative" if has_personal_experience else "General topic blog"}
CATEGORY: {blog_category}
TOPIC: {topic}

RESEARCH CONTEXT (only facts explicitly here are considered real):
{search_context[:600] if search_context else "No research context provided. Any statistics in the blog are unverified."}
{preferences_guidance}

BLOG TO EVALUATE:
{blog[:1800]}

Evaluate across ALL 8 dimensions. Return ONLY a valid JSON object:

{{
    "primary_dimension": {{
        "name": "{primary_dimension}",
        "score": <0-10>,
        "issues": ["specific issue 1", "specific issue 2"],
        "suggestion": "one specific actionable improvement"
    }},
    "readability": {{
        "score": <0-10>,
        "issues": ["specific issue 1", "specific issue 2"],
        "suggestion": "one specific actionable improvement"
    }},
    "factual_integrity": {{
        "score": <0-10>,
        "issues": ["list any invented statistics or fabricated scenes, or empty list if none"],
        "suggestion": "one specific actionable improvement"
    }},
    "tone": {{
        "score": <0-10>,
        "issues": ["specific issue 1", "specific issue 2"],
        "suggestion": "one specific actionable improvement"
    }},
    "originality": {{
        "score": <0-10>,
        "issues": ["specific issue 1", "specific issue 2"],
        "suggestion": "one specific actionable improvement"
    }},
    "structure": {{
        "score": <0-10>,
        "issues": ["specific issue 1", "specific issue 2"],
        "suggestion": "one specific actionable improvement"
    }},
    "engagement": {{
        "score": <0-10>,
        "issues": ["specific issue 1", "specific issue 2"],
        "suggestion": "one specific actionable improvement"
    }},
    "preference_alignment": {{
        "score": <0-10>,
        "issues": ["specific issue 1", "specific issue 2"],
        "suggestion": "one specific actionable improvement"
    }},
    "overall_score": <weighted average — see weights below>,
    "top_issues": ["single most critical issue", "second most critical issue"],
    "dimension_to_fix": "the single dimension with the lowest score",
    "revision_instruction": "one specific targeted instruction addressing only the lowest-scoring dimension"
}}

SCORING GUIDANCE:
{primary_guidance}
- Readability (0-10): sentence length variety, paragraph breaks max 3-4 sentences, flow, no repeated phrases or duplicate sections, complete sentences throughout
{stats_guidance}
- Tone (0-10): engaging, human, confident, not robotic or generic, matches the blog type, free of banned AI phrases like "captivate audiences" / "truly unforgettable" / "unique blend" / "seamless" / "game-changing"
- Originality (0-10): unique angle or genuine personal insight present, not a Wikipedia summary, takes a clear stance, goes beyond the obvious
- Structure & Organization (0-10): strong hook in introduction, logical section ordering where each section flows naturally from the previous, smooth transitions between sections, single strong conclusion (not two or more), proper heading hierarchy (H1 title then H2 sections then H3 subsections), no ideas jumping around randomly
- Engagement Value (0-10): hooks the reader in the first two sentences, uses concrete examples or stories to illustrate points, maintains reader interest across the whole piece, provides genuinely useful or surprising insight, does not simply list facts without context or narrative purpose
- Preference Alignment (0-10): how well the blog matched the user's stored style preferences above — tone formality, length, storytelling depth, formatting choices

WEIGHTS FOR OVERALL SCORE:
{"personal_voice" if has_personal_experience else "seo"}: 0.20
readability: 0.12
factual_integrity: 0.15
tone: 0.12
originality: 0.12
structure: 0.13
engagement: 0.11
preference_alignment: 0.05

CRITICAL SCORING RULES:
- A blog with fabricated statistics scores maximum 5/10 on factual_integrity regardless of other qualities
- A personal experience blog that invents scenes the author never described scores maximum 4/10 on personal_voice
- Repeated sections or a duplicated conclusion scores maximum 5/10 on structure
- Generic AI phrases lower tone score by 1-2 points each
- A blog that simply lists information without narrative purpose scores maximum 5/10 on engagement
- The revision_instruction must name ONE specific thing to fix — not a general "improve quality"

Return ONLY the JSON object, no preamble, no explanation, no markdown fences."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": eval_prompt}],
            max_tokens=1100
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        return result

    except Exception as e:
        print(f"Evaluator error: {e}")
        return {
            "primary_dimension": {"name": primary_dimension, "score": 7, "issues": [], "suggestion": ""},
            "readability": {"score": 7, "issues": [], "suggestion": ""},
            "factual_integrity": {"score": 7, "issues": [], "suggestion": ""},
            "tone": {"score": 7, "issues": [], "suggestion": ""},
            "originality": {"score": 7, "issues": [], "suggestion": ""},
            "structure": {"score": 7, "issues": [], "suggestion": ""},
            "engagement": {"score": 7, "issues": [], "suggestion": ""},
            "preference_alignment": {"score": 7, "issues": [], "suggestion": ""},
            "overall_score": 7.0,
            "top_issues": [],
            "dimension_to_fix": "",
            "revision_instruction": ""
        }


def revise_blog(blog: str, topic: str, revision_instruction: str,
                dimension_to_fix: str, search_context: str, api_key: str,
                model: str = "openai/gpt-oss-120b",
                has_personal_experience: bool = False,
                personal_experience: str = "") -> str:
    """Revise blog targeting one specific dimension based on evaluator feedback."""

    client = Groq(api_key=api_key)

    dimension_guidance = {
        "personal_voice": "Focus ONLY on making the blog sound like a genuine personal memory. Preserve specific place names, activities, and opinions the author mentioned. Remove any invented scenes or activities not described in the original experience. Do not soften the author's opinions into generic praise.",
        "seo": "Focus ONLY on improving heading structure, keyword presence in the title and first paragraph, and scannable formatting. Do not change the core content.",
        "readability": "Focus ONLY on sentence length variety, paragraph breaks (max 3-4 sentences each), and eliminating repeated phrases or near-duplicate sections.",
        "factual_integrity": "Focus ONLY on removing statistics, percentages, or survey results not present in the research context. Replace fabricated numbers with specific named examples or the author's own observations instead.",
        "tone": "Focus ONLY on replacing generic AI phrases with specific, confident, human language. Remove any of these if present: 'captivate audiences', 'truly unforgettable', 'unique blend', 'seamless', 'game-changing', 'in today's rapidly evolving landscape'.",
        "originality": "Focus ONLY on sharpening the central angle. Add one specific contrarian observation, surprising fact from the research context, or genuine prediction that goes beyond what is obvious about this topic.",
        "structure": "Focus ONLY on structural issues: ensure there is only one conclusion section, ensure sections flow logically from one to the next, add transition sentences between sections if abrupt, fix any heading hierarchy issues. Do not change the content itself.",
        "engagement": "Focus ONLY on making the piece more engaging: strengthen the opening hook if it is generic, add one concrete example or story to illustrate the main point, ensure at least one sentence per section gives the reader a reason to care about what they are reading.",
        "preference_alignment": "Focus ONLY on adjusting the blog to better match the user's stored style preferences as described in the revision instruction. This may mean adjusting length, formality, storytelling depth, or formatting."
    }

    specific_guidance = dimension_guidance.get(
        dimension_to_fix,
        "Improve the overall quality based on the feedback provided."
    )

    experience_reminder = f"""
PERSONAL EXPERIENCE PROVIDED BY AUTHOR:
{personal_experience[:500]}

REMINDER: Only expand on what the author actually described. Do NOT invent new scenes, activities, or events they did not mention.""" if has_personal_experience and personal_experience else ""

    revise_prompt = f"""You are an expert blog editor making a targeted, surgical revision.

TOPIC: {topic}
DIMENSION TO FIX: {dimension_to_fix}
SPECIFIC INSTRUCTION: {revision_instruction}
REVISION FOCUS: {specific_guidance}

RESEARCH CONTEXT (only statistics from here are real and usable):
{search_context[:600] if search_context else "No research context. Do not add any statistics."}
{experience_reminder}

ORIGINAL BLOG:
{blog[:1800]}

REVISION RULES:
- Make ONLY the changes needed to address the specific dimension above
- Do NOT change sections that are already working well
- Do NOT add statistics not in the research context above
- Do NOT invent scenes, events, or activities not in the original blog or personal experience
- Do NOT add preamble like "Here is the revised blog"
- Do NOT add closing remarks
- Start DIRECTLY with the blog title
- Maintain complete sentences throughout — never cut off mid-thought
- If the blog already scores well on this dimension, make minimal changes

Begin the revised blog now:"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": revise_prompt}],
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Reviser error: {e}")
        return blog


def run_evaluation_pipeline(blog: str, topic: str, search_context: str,
                             api_key: str, model: str = "openai/gpt-oss-120b",
                             max_revisions: int = 2,
                             has_personal_experience: bool = False,
                             personal_experience: str = "",
                             blog_category: str = "general",
                             preferences_text: str = "") -> tuple:
    """
    Full evaluation pipeline:
    1. Evaluate blog with type-aware, preference-aware scoring across 8 dimensions
    2. If score < 7.5, revise targeting the single lowest-scoring dimension
    3. Repeat up to max_revisions times
    Returns: (final_blog, final_scores)
    """

    current_blog = blog
    final_scores = None

    for attempt in range(max_revisions + 1):
        print(f"🔍 Evaluation attempt {attempt + 1}/{max_revisions + 1}")

        scores = evaluate_blog(
            blog=current_blog,
            topic=topic,
            search_context=search_context,
            api_key=api_key,
            model=model,
            has_personal_experience=has_personal_experience,
            blog_category=blog_category,
            preferences_text=preferences_text
        )
        final_scores = scores
        overall = scores.get("overall_score", 8.0)

        print(f"📊 Overall score: {overall}/10")
        print(f"🎯 Weakest dimension: {scores.get('dimension_to_fix', 'unknown')}")

        if overall >= 7.5 or attempt == max_revisions:
            print(f"✅ Blog accepted with score {overall}/10")
            break

        print(f"✏️ Revising — fixing: {scores.get('dimension_to_fix', 'general quality')}...")

        current_blog = revise_blog(
            blog=current_blog,
            topic=topic,
            revision_instruction=scores.get("revision_instruction", "Improve overall quality"),
            dimension_to_fix=scores.get("dimension_to_fix", "tone"),
            search_context=search_context,
            api_key=api_key,
            model=model,
            has_personal_experience=has_personal_experience,
            personal_experience=personal_experience
        )

    return current_blog, final_scores