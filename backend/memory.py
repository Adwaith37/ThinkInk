import json
import os
from datetime import datetime

DATA_FOLDER = "data/users"

DEFAULT_EXAMPLES = [
    """# Large Language Models Are Changing How We Write — And How We Think

There's a quiet revolution happening inside every text box on the internet.

## Introduction

When OpenAI released GPT-3 in 2020, most people outside research circles barely noticed. Three years later, ChatGPT crossed 100 million users in two months — faster than any technology in history. Today, large language models (LLMs) are embedded in everything from email clients to legal software. But beneath the surface-level productivity gains lies a deeper shift: AI is beginning to change not just how we write, but how we think.

## What Makes LLMs Different

Previous software followed rules. LLMs learn patterns.

Trained on hundreds of billions of words scraped from the internet, books, and academic papers, models like GPT-4, Claude, and Gemini don't look up answers — they predict the most statistically likely continuation of any given prompt. The result is text that feels eerily human, because in a very real sense, it is: it's a distillation of human language at scale.

This is what makes LLMs genuinely new. They're not search engines. They're not databases. They're probabilistic mirrors of human expression.

## The Productivity Argument

The economic case for LLMs is straightforward:

- **Developers** using GitHub Copilot write code 55% faster, according to a 2023 GitHub study
- **Customer support teams** resolve tickets faster with AI-assisted responses
- **Content teams** produce first drafts in minutes instead of hours
- **Researchers** summarize 50-page papers in seconds

For knowledge workers, LLMs are becoming what spreadsheets were to accountants in the 1980s — not a replacement, but a force multiplier so significant that not using them becomes a competitive disadvantage.

## The Deeper Question: Are We Thinking Less?

Here's where it gets uncomfortable.

If AI drafts your emails, summarizes your meetings, and outlines your reports, what happens to the cognitive muscles those tasks used to exercise? Writing isn't just output — it's thinking made visible. The struggle to find the right word, to construct a coherent argument, to anticipate a reader's objection: these friction points are where ideas sharpen.

There's a real risk that over-reliance on AI assistance creates a generation of professionals who can prompt fluently but think shallowly.

The answer isn't to avoid these tools — that ship has sailed. The answer is intentionality: knowing when to use AI as a starting point and when to do the hard thinking yourself.

## What Comes Next

The next wave of LLM development is moving toward reasoning, not just pattern matching. Models like OpenAI's o1 are designed to "think before they answer" — working through problems step by step rather than predicting the next likely token.

Combined with multimodal capabilities (understanding images, audio, and video), and integration into every software layer we use, LLMs in 2025 look nothing like the novelty chatbots of 2022.

## Conclusion

Large language models are not a productivity tool. They are a fundamental shift in how humans interact with knowledge.

The organizations and individuals who thrive won't be those who resist this shift or those who surrender to it blindly. They'll be those who develop the wisdom to know which thoughts to outsource and which ones are worth the struggle of thinking through themselves.

The most important skill of the AI era might not be prompting. It might be knowing when not to.""",

    """# Why Cybersecurity Is the Defining Technology Challenge of Our Generation

Every 39 seconds, a cyberattack occurs somewhere in the world.

## Introduction

In May 2021, a ransomware group called DarkSide shut down the Colonial Pipeline — the artery responsible for nearly half of the US East Coast's fuel supply. Gas stations ran dry. Prices spiked. The company paid $4.4 million in Bitcoin within hours.

It was a watershed moment. Not because it was the biggest cyberattack in history — it wasn't — but because it made viscerally clear that digital vulnerabilities now have physical consequences. Cybersecurity is no longer an IT department problem. It is a civilizational one.

## The Scale of the Threat

The numbers are staggering:

- Global cybercrime costs are projected to reach **$10.5 trillion annually by 2025**, according to Cybersecurity Ventures
- The average cost of a single data breach reached **$4.45 million in 2023**, per IBM's annual report
- Ransomware attacks increased by **93% year-over-year** in 2021
- The cybersecurity workforce gap stands at **3.4 million unfilled positions** worldwide

What makes this especially alarming is that the attack surface is expanding faster than defenses can scale. Every smart device, every cloud migration, every remote worker is a potential entry point.

## Why Traditional Defenses Are Failing

The old model of cybersecurity was built like a castle: strong walls, a moat, a clear perimeter. Once you were inside the network, you were trusted.

That model is dead.

Modern organizations have no perimeter. Employees work from coffee shops. Data lives in dozens of cloud services. Partners have direct API access to core systems. The castle metaphor broke the moment the walls dissolved.

The successor architecture is Zero Trust: assume breach, verify every request, grant minimum necessary access. It's less a product than a philosophy — and implementing it requires rethinking decades of infrastructure decisions.

## The AI Arms Race

Artificial intelligence has arrived on both sides of the battlefield.

Defenders are using AI to detect anomalies at network speed, correlate threat intelligence across millions of signals, and automate response to routine attacks. Security operations centers that once required armies of analysts can now triage alerts with a fraction of the staff.

But attackers have access to the same tools.

AI-generated phishing emails now pass every readability test humans have traditionally used to spot fakes. Deepfake audio is being used in real-time voice scams impersonating executives. Automated vulnerability scanners probe targets 24 hours a day, looking for the single misconfigured server that opens the door.

The asymmetry is brutal: defenders must be right every time. Attackers only need to be right once.

## The Human Factor

Despite all the technology, the most exploited vulnerability remains the same as it was 30 years ago: people.

Ninety-five percent of cybersecurity breaches involve human error. A password reused across accounts. A link clicked in a moment of distraction. An IT administrator who approved an access request without verifying the identity of the requester.

Technical solutions matter. But culture matters more. Organizations that treat security as everyone's responsibility — not just the IT team's — are measurably more resilient than those that don't.

## Conclusion

Cybersecurity is not a problem that will be solved. It is a condition that must be managed — permanently, adaptively, and collectively.

The stakes have never been higher. The infrastructure that powers hospitals, financial systems, water treatment plants, and democratic elections now runs on software. Securing that software is not a technical challenge with a technical solution.

It is the defining governance challenge of the digital age. And we are, collectively, still in the early chapters of figuring out how to meet it."""

"""# The Quiet Revolution: How Quantum Computing Will Break — and Rebuild — the Internet

The encryption protecting your bank account was designed to take a classical computer longer than the age of the universe to crack. A quantum computer could do it in hours.

## Introduction

In 2019, Google announced that its quantum processor Sycamore had performed a calculation in 200 seconds that would take the world's fastest supercomputer 10,000 years. They called it quantum supremacy. IBM pushed back on the numbers. Physicists argued about the methodology.

But beneath the academic debate, one thing was clear: quantum computing had crossed from theoretical physics into engineering reality. And the implications for cybersecurity, drug discovery, financial modeling, and artificial intelligence are so profound that governments worldwide are treating quantum capability as a matter of national security.

## What Makes Quantum Different

Classical computers think in bits — binary switches that are either 0 or 1. Every calculation, every pixel, every encrypted message is ultimately a sequence of these two states.

Quantum computers use qubits. Thanks to a property called superposition, a qubit can be 0, 1, or both simultaneously. A second property called entanglement means qubits can be correlated across any distance, so that the state of one instantly influences another. A third property, interference, allows quantum algorithms to amplify correct answers and cancel wrong ones.

The result: a quantum computer with 300 qubits can represent more states simultaneously than there are atoms in the observable universe. For certain classes of problems, this isn't a marginal improvement over classical computing. It's a different category of machine entirely.

## The Problems Quantum Will Solve

Not every problem benefits from quantum computation. Sending emails, streaming video, running spreadsheets — classical computers handle these perfectly well.

But some problems have a structure that quantum computers are uniquely suited to attack:

- **Cryptography**: Shor's algorithm can factor large numbers exponentially faster than any classical approach, breaking the RSA encryption that secures most of the internet
- **Drug discovery**: Simulating molecular interactions at the quantum level to find new medicines — a task that overwhelms classical supercomputers
- **Optimization**: Finding the best route through millions of variables, relevant to logistics, finance, and supply chain management
- **Machine learning**: Accelerating the training of AI models by exploring solution spaces that classical computers can only sample

## The Encryption Crisis Nobody Is Talking About

Here is the uncomfortable reality: every piece of encrypted data transmitted today can be recorded and stored, waiting for quantum computers powerful enough to decrypt it.

Intelligence agencies call this "harvest now, decrypt later." Sensitive government communications. Medical records. Financial transactions. Corporate secrets. Anything encrypted with today's standards and transmitted over the internet is potentially already in someone's archive, waiting.

The National Institute of Standards and Technology finalized its first post-quantum cryptography standards in 2024. Migration will take years. For critical infrastructure, it needed to start yesterday.

## Where We Actually Are

Despite the headlines, practical quantum computing remains enormously difficult.

Qubits are extraordinarily fragile. They must be cooled to temperatures colder than outer space. The slightest vibration, electromagnetic interference, or thermal fluctuation causes decoherence — the quantum state collapses, and the calculation fails. Current systems have error rates that make them unsuitable for most practical applications without significant error correction overhead.

IBM, Google, IonQ, and a wave of startups are racing to build fault-tolerant quantum computers. Most experts believe cryptographically relevant quantum computers are still 10 to 15 years away. But in technology, timelines have a way of compressing unexpectedly.

## Conclusion

Quantum computing is not a technology that will arrive with a press release and a product launch. It will arrive the way all paradigm shifts do — gradually, then suddenly.

The organizations preparing now — migrating to quantum-resistant encryption, investing in quantum literacy, experimenting with early quantum hardware — will not just survive the transition. They will define what comes after it.

The internet as we know it was built on assumptions about what computers can do. Quantum computing changes those assumptions at the foundation level. Everything built on top will need to be rethought.""",

    """# The Autonomous Vehicle Promise: Why Self-Driving Cars Are Harder Than We Thought

In 2015, Elon Musk predicted fully self-driving cars by 2017. It is now nearly a decade later.

## Introduction

The pitch was intoxicating: eliminate the 1.35 million people killed in road accidents every year. Free commuters from the cognitive burden of driving. Unlock trillions in economic productivity as vehicles become mobile offices. Reshape cities built around parking lots and traffic patterns designed for human reflexes.

The technology was supposed to be close. The best engineers in the world — backed by tens of billions of dollars from Google, Tesla, Uber, GM, and dozens of startups — were working on it. The problem turned out to be one of the hardest in the history of engineering.

## Why Humans Are Surprisingly Good at Driving

To understand why autonomous vehicles are difficult, it helps to appreciate how remarkable human driving actually is.

Every time you merge onto a highway, you are simultaneously processing visual information from multiple angles, predicting the behavior of a dozen other drivers, interpreting ambiguous signals — the car that's been in the merge lane for too long, the truck that's drifting slightly — and making split-second decisions based on incomplete information.

You do this while occasionally glancing at your passenger, sipping coffee, and listening to a podcast. You've been doing it so long it feels automatic.

Replicating this in software requires solving perception, prediction, and planning simultaneously, in real time, across an effectively infinite range of scenarios — including ones that have never appeared in any training dataset.

## The Edge Case Problem

Autonomous vehicle engineers talk obsessively about edge cases — the rare, unpredictable situations that fall outside normal operating parameters.

A mattress falling off a truck on the highway. A child chasing a ball between parked cars. A construction worker using hand signals that contradict the traffic light. A partially obscured stop sign covered in graffiti.

For humans, these scenarios are handled through general intelligence — the ability to reason about novel situations using accumulated understanding of how the world works. Current AI systems, no matter how sophisticated, are fundamentally pattern matchers. They generalize imperfectly from training data to real-world scenarios.

The brutal mathematics: a system that handles 99.9% of situations perfectly will still fail in 1 in every 1,000 encounters. At scale, across millions of vehicles and billions of miles, that means thousands of failures every day.

## Where Progress Is Actually Happening

Despite the hype cycles and high-profile setbacks, real progress is being made — just more slowly and narrowly than predicted.

**Waymo** operates a fully driverless commercial robotaxi service in Phoenix, San Francisco, and Los Angeles. Customers summon rides through an app. There is no human in the vehicle. By any reasonable measure, this is remarkable.

**Tesla's Full Self-Driving** handles highway driving and navigating complex urban environments with increasing competence, though it requires driver supervision and generates controversy with every reported incident.

**Trucking** may see autonomous vehicles before consumer cars. The highway environment is more structured and predictable. Companies like Aurora and Kodiak are running autonomous trucks on fixed interstate routes between distribution centers.

The pattern emerging is not the universal autonomy predicted in 2015. It is geofenced, domain-specific, gradually expanding autonomy in controlled environments.

## The Regulation Gap

Technology is only half the problem.

Who is liable when an autonomous vehicle causes an accident? How do regulators certify a system too complex to fully audit? How do cities redesign infrastructure for vehicles that don't need parking near their destination?

These questions don't have clean technical answers. They require negotiation between engineers, lawyers, insurers, city planners, and elected officials — processes that move at a fundamentally different speed than software development.

## Conclusion

The autonomous vehicle future is coming. The evidence from Waymo's operational robotaxis, from the relentless improvement in perception systems, from the billions still flowing into the sector despite years of missed predictions — all of it points toward eventual arrival.

What the last decade has taught us is that "eventual" was always doing a lot of work in that sentence.

The engineers who predicted 2017 weren't wrong about the destination. They were wrong about the terrain. It turns out the last few percentage points of reliability — the difference between impressive demos and deployable technology — are separated from the first ninety-five percent by a chasm that only grinding, unglamorous engineering work can cross.

That work is happening. Quietly, methodically, expensively. One edge case at a time."""
]





def get_user_file(user_id):
    return os.path.join(DATA_FOLDER, f"{user_id}.json")

def load_user(user_id):
    file_path = get_user_file(user_id)
    if not os.path.exists(file_path):
        return {
            "examples": DEFAULT_EXAMPLES,
            "chats": {},
            "current_chat_id": None,
            "preferences": {}  # ← New
        }
    with open(file_path, "r") as f:
        return json.load(f)

def save_user(user_id, data):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    file_path = get_user_file(user_id)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def create_new_chat(user_id, topic):
    data = load_user(user_id)
    chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
    data["chats"][chat_id] = {
        "topic": topic,
        "current_blog": "",
        "history": [],
        "created_at": datetime.now().strftime("%d %b %Y, %H:%M")
    }
    data["current_chat_id"] = chat_id
    save_user(user_id, data)
    return chat_id

def get_current_chat_id(user_id):
    data = load_user(user_id)
    return data.get("current_chat_id", None)

def set_current_chat(user_id, chat_id):
    data = load_user(user_id)
    data["current_chat_id"] = chat_id
    save_user(user_id, data)

def save_current_blog(user_id, blog):
    data = load_user(user_id)
    chat_id = data.get("current_chat_id")
    if not chat_id or chat_id not in data["chats"]:
        return
    chat = data["chats"][chat_id]
    chat["current_blog"] = blog
    history = chat.get("history", [])
    history.append(blog)
    if len(history) > 5:
        history.pop(0)
    chat["history"] = history
    save_user(user_id, data)

def get_current_blog(user_id):
    data = load_user(user_id)
    chat_id = data.get("current_chat_id")
    if not chat_id or chat_id not in data["chats"]:
        return ""
    return data["chats"][chat_id].get("current_blog", "")

def get_all_chats(user_id):
    data = load_user(user_id)
    chats = data.get("chats", {})
    result = []
    for chat_id, chat in chats.items():
        result.append({
            "chat_id": chat_id,
            "topic": chat.get("topic", "Untitled"),
            "created_at": chat.get("created_at", ""),
            "current_blog": chat.get("current_blog", "")
        })
    result.sort(key=lambda x: x["chat_id"], reverse=True)
    return result

def get_chat_blog(user_id, chat_id):
    data = load_user(user_id)
    chats = data.get("chats", {})
    if chat_id in chats:
        return chats[chat_id].get("current_blog", "")
    return ""

def get_preferences(user_id) -> dict:
    """Get stored preferences for user"""
    data = load_user(user_id)
    return data.get("preferences", {})

def save_preferences(user_id, preferences: dict):
    """Save updated preferences for user"""
    data = load_user(user_id)
    data["preferences"] = preferences
    save_user(user_id, data)



def add_example(user_id, blog):
    """Add example to both JSON and ChromaDB"""
    from backend.rag import add_example_to_rag, delete_oldest_if_limit  # ← imports RAG

    data = load_user(user_id)

    # Generate unique ID using timestamp
    example_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

    # ← RAG: Add to ChromaDB for semantic search
    delete_oldest_if_limit(user_id, max_examples=8)
    add_example_to_rag(user_id, blog, example_id)

    # ← Also keep in JSON as fallback for new users
    data["examples"].append(blog)
    if len(data["examples"]) > 8:
        data["examples"].pop(0)

    save_user(user_id, data)
