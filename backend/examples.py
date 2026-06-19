"""
Categorized example library for few-shot prompting and RAG.

Each example carries metadata so retrieval can match on:
- category: the type of blog (travel, tech, professional, gaming, opinion, news)
- style: the dominant writing style (storytelling, analytical, listicle, opinion)
- has_personal_voice: whether the example demonstrates first-person personal narrative

New users get a spread of these as their starting example pool.
Categories are also used to scope RAG retrieval once a topic is classified.
"""

CATEGORIES = [
    "travel",
    "tech",
    "professional",
    "gaming",
    "opinion",
    "news"
]

EXAMPLES = [

    # ── TRAVEL ────────────────────────────────────────
    {
        "category": "travel",
        "style": "storytelling",
        "has_personal_voice": True,
        "content": """# I Spent 3 Days in Kyoto — Here's What Nobody Tells You About Japan's Ancient Capital

I almost missed the best part of Kyoto because every travel blog sent me to the wrong place.

## The Morning That Changed Everything

It was 5:47 AM on my second day. I'd woken up early on accident — jet lag finally working in my favor. While every tourist was still asleep dreaming of geishas and matcha, I wandered into Fushimi Inari alone.

No crowds. No selfie sticks. Just 10,000 vermillion torii gates disappearing into the mountain mist.

That's when I understood why people return to Japan obsessively. It's not the famous spots. It's the version of those spots that exists before the world wakes up.

## What the Instagram Posts Don't Show

**Fushimi Inari takes 3 hours minimum** if you want to reach the summit. Every blog says "it's worth it." None of them mention the vending machines selling cold Pocari Sweat halfway up, which at that point feel like divine intervention.

The crowds arrive at 9 AM like clockwork. By then I was back at my guesthouse eating tamagoyaki and feeling unreasonably smug.

## The Neighborhoods Nobody Recommends

Arashiyama gets all the attention. Fushimi gets the Instagram traffic.

But **Nishiki Market at 7 AM** — before the tour groups — is the real Kyoto. Vendors setting up. Fishmongers arguing. An elderly woman offering me a skewer of grilled mochi because I looked confused about what it was.

That interaction cost me nothing and is the clearest memory I have from the entire trip.

## The Practical Things I Wish I'd Known

- **IC Card** (Suica or ICOCA) is non-negotiable. Cash-only taxis will drain your budget fast
- **Konbini breakfast** (7-Eleven Japan) is genuinely good — onigiri, tamago sando, hot coffee for under $4
- **Book Arashiyama bamboo grove for sunrise** or accept that your photos will include 200 strangers
- The **ryokan experience** is worth the splurge for one night minimum

## Conclusion

Kyoto rewards the unhurried. Slow down. Wake up early. Get lost in a neighborhood that's not in your guidebook.

## Frequently Asked Questions

**How many days do you need in Kyoto?**
Minimum 3 days, ideally 5. The city reveals itself slowly.

**What's the best time of year to visit?**
Cherry blossom season (late March to early April) is stunning but crushingly crowded. Mid-November for autumn foliage offers similar beauty with thinner crowds.

**Is Kyoto expensive?**
It depends entirely on your choices. Street food and konbini meals keep costs low. Ryokans and kaiseki dinners push budgets high quickly."""
    },
    {
        "category": "travel",
        "style": "listicle",
        "has_personal_voice": False,
        "content": """# 7 Underrated European Cities That Deserve Your Next Trip (Not Paris, Not Rome)

In 2024, over 600,000 tourists visited the Louvre **on a single day** during peak season. Meanwhile, equally stunning cities sit nearly empty.

## Why Overtourism Is Changing How People Travel

Venice now charges entry fees just to manage crowd volume. Barcelona residents have protested mass tourism in the streets. The era of chasing the same five European capitals is ending — not because those cities stopped being beautiful, but because the experience of visiting them has degraded under their own popularity.

Here are seven cities that deliver the same architectural grandeur, food culture, and history without the crowds.

## 1. Porto, Portugal

Lisbon's quieter sibling has the same tiled buildings and river views, with **a third of the tourist density**. Port wine cellars line the riverbank, and a single Francesinha sandwich costs less than a coffee in central Paris.

## 2. Ljubljana, Slovenia

A car-free city center, a dragon-guarded bridge, and a castle overlooking the entire town. Slovenia's capital combines Vienna's elegance with Croatia's affordability.

## 3. Gdansk, Poland

Baltic amber, colorful merchant houses, and a UNESCO-protected old town rebuilt brick-by-brick after WWII. Most travelers skip it entirely for Krakow.

## 4. Ghent, Belgium

Brussels gets the EU headquarters. Bruges gets the tour buses. Ghent gets the actual medieval atmosphere, minus either crowd.

## 5. Valencia, Spain

Barcelona's beaches, Barcelona's food scene, **40% lower accommodation costs**, and the actual birthplace of paella.

## 6. Tbilisi, Georgia

Technically transcontinental, culturally unmatched. Sulfur bathhouses, a wine culture older than France's, and a old town carved into a hillside.

## 7. Plovdiv, Bulgaria

Europe's oldest continuously inhabited city, with a Roman amphitheater still in active use for concerts.

## Conclusion

The best European trip in 2025 isn't about seeing more famous landmarks — it's about avoiding the version of travel where you spend more time in lines than in the actual place.

## Frequently Asked Questions

**Are these cities safe for solo travelers?**
Yes, all seven rank above the EU average for traveler safety according to recent tourism board data.

**What's the best time to visit Eastern Europe?**
Late spring (May-June) or early autumn (September) avoid both winter cold and summer crowds.

**Is English widely spoken in these cities?**
In tourist areas and among younger residents, yes. Basic local phrases are still appreciated."""
    },

    # ── TECH ──────────────────────────────────────────
    {
        "category": "tech",
        "style": "analytical",
        "has_personal_voice": False,
        "content": """# Large Language Models Are Changing How We Write — And How We Think

There's a quiet revolution happening inside every text box on the internet.

## Introduction

When OpenAI released GPT-3 in 2020, most people outside research circles barely noticed. Three years later, ChatGPT crossed 100 million users in two months — faster than any technology in history. Today, large language models (LLMs) are embedded in everything from email clients to legal software.

## What Makes LLMs Different

Previous software followed rules. LLMs learn patterns. Trained on hundreds of billions of words, models like GPT-4, Claude, and Gemini predict the most statistically likely continuation of any given prompt.

## The Productivity Argument

- **Developers** using GitHub Copilot write code 55% faster
- **Customer support teams** resolve tickets faster with AI-assisted responses
- **Content teams** produce first drafts in minutes instead of hours

## The Deeper Question: Are We Thinking Less?

If AI drafts your emails and outlines your reports, what happens to the cognitive muscles those tasks used to exercise? Writing isn't just output — it's thinking made visible.

## Conclusion

Large language models are not a productivity tool. They are a fundamental shift in how humans interact with knowledge. The most important skill of the AI era might not be prompting. It might be knowing when not to.

## Frequently Asked Questions

**Will LLMs replace human writers?**
Unlikely entirely — but they will replace writers who don't adapt to using them as a tool rather than a crutch.

**What's the biggest risk of relying on LLMs for writing?**
Cognitive offloading — losing the thinking process that writing was originally forcing you to do.

**How fast is this technology improving?**
Capability benchmarks have roughly doubled year over year since 2020, though gains are starting to plateau on some tasks."""
    },
    {
        "category": "tech",
        "style": "opinion",
        "has_personal_voice": False,
        "content": """# Why Cybersecurity Is the Defining Technology Challenge of Our Generation

Every 39 seconds, a cyberattack occurs somewhere in the world.

## Introduction

In May 2021, a ransomware group called DarkSide shut down the Colonial Pipeline. Gas stations ran dry. The company paid $4.4 million in Bitcoin within hours. It made viscerally clear that digital vulnerabilities now have physical consequences.

## The Scale of the Threat

- Global cybercrime costs projected at **$10.5 trillion annually by 2025**
- Average cost of a single data breach: **$4.45 million in 2023**
- **3.4 million unfilled** cybersecurity positions worldwide

## Why Traditional Defenses Are Failing

The old model was built like a castle: strong walls, clear perimeter. That model is dead. Modern organizations have no perimeter — employees work remotely, data lives in dozens of cloud services.

The successor architecture is Zero Trust: assume breach, verify every request, grant minimum necessary access.

## Conclusion

Cybersecurity is not a problem that will be solved. It is a condition that must be managed — permanently, adaptively, and collectively.

## Frequently Asked Questions

**What is Zero Trust architecture?**
A security model that assumes no user or device is automatically trusted, requiring continuous verification regardless of network location.

**Why are there so many unfilled cybersecurity jobs?**
Demand has outpaced training pipelines — the field grew faster than universities and bootcamps could supply qualified candidates.

**Is ransomware still a major threat in 2025?**
Yes, attacks increased significantly year over year, with critical infrastructure increasingly targeted."""
    },

    # ── PROFESSIONAL ──────────────────────────────────
    {
        "category": "professional",
        "style": "storytelling",
        "has_personal_voice": True,
        "content": """# I Got Laid Off Twice in Two Years — Here's What Actually Helped Me Land My Next Role

The second layoff hurt less than the first, but only because I'd already learned the lesson the hard way.

## The First Time

I found out on a Tuesday, in a 12-minute video call with HR and my manager's camera conspicuously off. Twenty minutes later my laptop access was revoked. I'd been planning a project roadmap that morning.

I spent the next six weeks doing what most people do — refreshing job boards, sending the same resume to forty companies, and quietly panicking about my mortgage.

## What I Got Wrong

I treated job searching like applying to college: send applications everywhere, hope volume works in my favor. It didn't. I got maybe three callbacks out of around 150 applications.

The job I eventually landed came from a referral, not a cold application. That's not a coincidence — it's the pattern almost everyone in my network described once I actually asked them.

## The Second Time

Eighteen months later, a reorg hit my new company. This time I knew what to do immediately.

**I didn't apply blindly. I reached out to twelve people directly** — former colleagues, people I'd worked with on cross-team projects, even a recruiter who'd reached out to me a year earlier for a role I'd turned down.

Within three weeks I had two real conversations in motion. Within five weeks I had an offer.

## What Actually Worked

- **Direct outreach beats applications** — a message to someone who already knows your work outperforms a cold resume every time
- **Your network is built before you need it**, not during the crisis — the people who helped me were ones I'd stayed in touch with for no transactional reason
- **Specificity in outreach matters** — "I'm looking for senior PM roles in fintech, here's exactly why I'd be a fit for your team" gets responses; "let me know if you hear of anything" doesn't
- **The emotional toll is real and worth acknowledging** — pretending layoffs don't affect your confidence doesn't make the job search faster, it just makes you worse at it

## Conclusion

Layoffs are increasingly a normal part of careers, not a personal failure. The skill that actually protects you isn't a perfect resume — it's relationships you've maintained before you needed anything from them.

## Frequently Asked Questions

**How long does the average layoff job search take?**
Recent data suggests 3-6 months on average, though this varies significantly by industry, seniority, and network strength.

**Is networking really more effective than applying online?**
Multiple studies and most recruiters confirm referrals have dramatically higher conversion rates than cold applications.

**How do you network when you don't have one yet?**
Start before you need it — engage genuinely with former colleagues and industry contacts with no immediate ask attached."""
    },
    {
        "category": "professional",
        "style": "analytical",
        "has_personal_voice": False,
        "content": """# Why Most Corporate Reorgs Fail Within 18 Months

Roughly 70% of organizational restructuring efforts fail to achieve their stated goals, according to multiple longitudinal studies on corporate change management.

## The Pattern Behind the Failure

Reorgs are typically announced with confident language — "improved agility," "better cross-functional collaboration," "closer alignment with strategic priorities." Eighteen months later, many of these same organizations quietly reorganize again.

## What Actually Goes Wrong

**Reporting lines change faster than workflows do.** Teams get reshuffled on an org chart while the actual processes they use to get work done remain unchanged, creating friction between new structure and old habits.

**Communication lags behind decision-making.** Leadership typically finalizes structure changes weeks before communicating them clearly to affected employees, creating a vacuum filled by rumor and anxiety.

**Metrics rarely change to match new goals.** If a reorg's stated purpose is "faster decision-making," but performance reviews still measure the same metrics as before, employees have no incentive to actually behave differently.

## The Companies That Get It Right

Organizations that successfully execute restructuring typically share three traits: they redesign incentive structures alongside reporting structures, they over-communicate rather than under-communicate, and they measure success against the original stated goal rather than declaring victory once the org chart is updated.

## Conclusion

A reorg is not a structural change — it's a behavioral change wearing a structural disguise. Companies that forget this distinction tend to repeat the exercise every 18 months indefinitely.

## Frequently Asked Questions

**Why do companies reorganize so frequently?**
Often because the previous reorg didn't address root causes, only symptoms, leading leadership to attempt structural fixes repeatedly.

**What's the most common mistake in reorg communication?**
Announcing the "what" without adequately explaining the "why," which leaves employees filling gaps with their own assumptions.

**Do reorgs actually improve performance?**
Evidence is mixed — well-executed ones can, but most studies find limited measurable performance improvement from structure changes alone."""
    },

    # ── GAMING ────────────────────────────────────────
    {
        "category": "gaming",
        "style": "storytelling",
        "has_personal_voice": True,
        "content": """# 200 Hours Into Elden Ring, I Finally Understand Why Everyone Calls It a Masterpiece

I died to the same boss eleven times before I realized the game wasn't being unfair — I was.

## My Rocky Start

I almost refunded this game in the first three hours. I wandered into Caelid by accident, got obliterated by enemies clearly meant for a much later stage of the game, and nearly concluded that FromSoftware's reputation for difficulty was just punishing design dressed up as art.

That assumption was wrong, and realizing why it was wrong is the entire appeal of this game.

## The Moment It Clicked

Around hour 40, stuck on Margit, I finally did what the game had been quietly telling me to do the entire time: I left. I explored somewhere else. I came back twenty hours later with better gear, a stronger build, and an actual strategy instead of brute-forcing the same attack pattern repeatedly.

I beat him in two tries.

**That's when I understood Elden Ring isn't hard in the way people describe it. It's honest.** The difficulty isn't artificial — it's a direct, unforgiving signal that you're approaching a problem wrong, and the solution is almost always "go explore, get stronger, come back smarter."

## What Makes the Open World Actually Work

Most open-world games pad their map with repetitive side content. Elden Ring's world rewards genuine curiosity — a random cave might contain a build-defining weapon, or a legacy dungeon disguised as an unremarkable ruin.

**I found one of the game's best weapons by accident**, falling through a hole I wasn't supposed to notice, in an area I'd walked past four separate times.

## The Boss Design Philosophy

Malenia remains, even after 200 hours, the hardest boss fight I've experienced in any game. I died to her over 60 times. The moment I finally won felt disproportionately significant compared to literally any other achievement I've had in gaming.

That's not an accident. FromSoftware designs difficulty as an emotional mechanic, not just a mechanical one.

## Conclusion

Elden Ring isn't for everyone, and it shouldn't pretend to be. But the people who call it a masterpiece aren't exaggerating — they're describing exactly what it feels like to finally beat something that seemed designed to be unbeatable.

## Frequently Asked Questions

**Is Elden Ring too hard for casual players?**
It's challenging by design, but the open structure means you can explore and grow stronger rather than being forced through difficulty walls immediately.

**How long does it take to finish Elden Ring?**
A focused main-story playthrough takes around 50-60 hours; full exploration easily exceeds 100-150 hours.

**Do you need to play previous Souls games first?**
No — Elden Ring is self-contained and doesn't require prior FromSoftware game knowledge."""
    },
    {
        "category": "gaming",
        "style": "listicle",
        "has_personal_voice": False,
        "content": """# 6 Indie Games From the Last Year That Outperformed Their AAA Competition

Indie game revenue crossed **$3 billion globally** in the last reported fiscal year, a number that would have seemed implausible a decade ago.

## Why Indie Games Are Outpacing Expectations

Smaller teams with smaller budgets are increasingly producing more critically acclaimed, more innovative experiences than studios with hundreds of millions in development funding. The reasons are structural: indie teams can take creative risks publishers consider too unpredictable to fund at AAA budget scale.

## 1. Hades II

Supergiant Games followed up one of the most acclaimed roguelikes in years with a sequel that improved nearly every system rather than simply repeating the formula.

## 2. Animal Well

A single solo developer spent **seven years** building a metroidvania with puzzle design so intricate that the community is still discovering secrets months after release.

## 3. Balatro

A poker-deckbuilding hybrid that became one of the most addictive releases of the year, built by essentially one person, with a production budget a fraction of a single AAA marketing campaign.

## 4. Pacific Drive

A survival-driving game with a genuinely original premise — your car as both shelter and character — from a first-time studio.

## 5. Thank Goodness You're Here

A short, hand-animated comedy game that proved narrative experimentation doesn't need a massive budget to land emotionally.

## 6. UFO 50

Fifty interconnected retro-style games in a single package, a structurally ambitious project that took its small team **over eight years** to complete.

## Conclusion

The gap between indie and AAA isn't budget anymore — it's risk tolerance. Smaller teams can gamble on weird, original ideas that bigger studios increasingly can't justify to shareholders.

## Frequently Asked Questions

**Are indie games cheaper than AAA games?**
Generally yes, though pricing has crept upward as indie production values have improved.

**Why are solo developers able to compete with large studios?**
Modern engines like Unity and Godot have dramatically lowered the technical barrier to building polished games.

**Is the indie game market oversaturated?**
Discovery is genuinely difficult given volume, but quality titles still consistently break through via word of mouth and platforms like Steam's discovery algorithms."""
    },

    # ── OPINION ───────────────────────────────────────
    {
        "category": "opinion",
        "style": "opinion",
        "has_personal_voice": False,
        "content": """# The Quiet Revolution: How Quantum Computing Will Break — and Rebuild — the Internet

The encryption protecting your bank account was designed to take a classical computer longer than the age of the universe to crack. A quantum computer could do it in hours.

## Introduction

In 2019, Google announced that its quantum processor Sycamore performed a calculation in 200 seconds that would take the fastest supercomputer 10,000 years. Quantum computing had crossed from theoretical physics into engineering reality.

## What Makes Quantum Different

Classical computers think in bits — 0 or 1. Quantum computers use qubits which can be 0, 1, or both simultaneously through superposition.

## The Encryption Crisis

Every piece of encrypted data transmitted today can be recorded and stored, waiting for quantum computers powerful enough to decrypt it. Intelligence agencies call this "harvest now, decrypt later."

The National Institute of Standards and Technology finalized its first post-quantum cryptography standards in 2024. Migration will take years. For critical infrastructure, it needed to start yesterday.

## Conclusion

The organizations preparing now — migrating to quantum-resistant encryption, investing in quantum literacy — will not just survive the transition. They will define what comes after it.

## Frequently Asked Questions

**How close are we to practical quantum computers?**
Most experts estimate cryptographically relevant quantum computers are still 10-15 years away, though timelines have historically compressed faster than predicted.

**What is post-quantum cryptography?**
Encryption methods designed to remain secure even against attacks from sufficiently powerful quantum computers.

**Should individuals worry about quantum computing now?**
Not urgently, but organizations handling sensitive long-term data should begin migration planning immediately."""
    },
    {
        "category": "opinion",
        "style": "analytical",
        "has_personal_voice": False,
        "content": """# The Autonomous Vehicle Promise: Why Self-Driving Cars Are Harder Than We Thought

In 2015, Elon Musk predicted fully self-driving cars by 2017. It is now nearly a decade later.

## Introduction

The pitch was intoxicating: eliminate 1.35 million road deaths per year, free commuters from driving, reshape cities. The technology was supposed to be close. It turned out to be one of the hardest problems in the history of engineering.

## The Edge Case Problem

Autonomous vehicle engineers talk obsessively about edge cases — rare, unpredictable situations outside normal parameters. A mattress falling off a truck. A child chasing a ball between parked cars.

For humans, these are handled through general intelligence. Current AI systems are fundamentally pattern matchers. A system that handles 99.9% of situations perfectly still fails 1 in every 1,000 encounters.

## Where Progress Is Actually Happening

**Waymo** operates a fully driverless commercial robotaxi service in Phoenix, San Francisco, and Los Angeles — no human in the vehicle. **Trucking** may see autonomy before consumer cars, given more structured highway environments.

## Conclusion

The autonomous vehicle future is coming. What the last decade taught us is that the last few percentage points of reliability are separated from the first ninety-five percent by a chasm that only grinding, unglamorous engineering work can cross.

## Frequently Asked Questions

**Are self-driving cars safe today?**
Within their geofenced operating areas, services like Waymo report strong safety records, though broader unrestricted autonomy remains unsolved.

**Why is trucking expected to achieve autonomy before passenger cars?**
Highway driving is more structured and predictable than complex urban environments with pedestrians and irregular traffic patterns.

**What's the biggest unsolved problem in autonomous driving?**
Handling rare, unpredictable edge cases that don't appear sufficiently in training data."""
    },

    # ── NEWS ──────────────────────────────────────────
    {
        "category": "news",
        "style": "listicle",
        "has_personal_voice": False,
        "content": """# The 2026 World Cup Will Be the Most Chaotic Tournament FIFA Has Ever Run — Here's Why

For the first time in history, three nations will simultaneously host football's biggest event, and with 48 teams entering the tournament, the format itself may become the story.

## A Tournament Restructured From the Ground Up

The expansion from 32 to 48 teams represents the largest structural change in World Cup history. More qualifying spots means more nations get tournament experience, but it also means **the group stage now includes teams with significantly larger talent gaps** than previous tournaments.

## The Logistics Problem Nobody's Solved Yet

Hosting across the United States, Mexico, and Canada means players and fans will face genuinely different climates, altitudes, and time zones within a single tournament — something no previous World Cup has had to manage at this scale.

## Why the Format Change Is Controversial

Critics argue the expanded format dilutes quality — more teams means more lopsided group-stage matches. Supporters argue it democratizes access, giving smaller football nations qualification pathways that previously didn't exist.

## What to Actually Watch For

- **Travel fatigue** across three countries could meaningfully affect performance for teams drawn into geographically spread groups
- **Smaller nations** making genuine tournament runs for the first time, given expanded qualification slots
- **Broadcast and ticket demand** expected to set tournament revenue records given North America's market size

## Conclusion

Whether the 48-team format succeeds or becomes a cautionary tale for future expansion will likely depend less on the football itself and more on how well three countries coordinate an event of this scale.

## Frequently Asked Questions

**When does the 2026 World Cup begin?**
The tournament is scheduled for June 2026 across the United States, Mexico, and Canada.

**Why did FIFA expand to 48 teams?**
To increase global participation and qualification opportunities for smaller football nations, alongside commercial growth motivations.

**Is hosting across three countries unprecedented?**
Yes, this marks the first World Cup with three host nations in tournament history."""
    },
    {
        "category": "news",
        "style": "analytical",
        "has_personal_voice": False,
        "content": """# Why the Global Microchip Shortage Never Fully Ended — It Just Changed Shape

In 2021, car manufacturers idled factories over missing semiconductors. In 2025, the shortage looks different, but it hasn't disappeared.

## The Original Crisis

COVID-era demand spikes for electronics collided with semiconductor fabrication facilities running at fixed capacity, creating shortages across industries from automotive to gaming consoles. Estimated losses for automakers alone exceeded **$210 billion** during the worst of the disruption.

## What's Actually Different Now

Commodity chip shortages have largely resolved. **Advanced chip shortages have not.** The bottleneck has shifted from general semiconductor supply to the most cutting-edge fabrication nodes — the chips required for AI training, which are dominated by a small number of facilities globally.

## The Geopolitical Layer

A significant share of advanced chip manufacturing capacity is concentrated in Taiwan, creating a dependency that governments increasingly treat as a national security concern rather than a purely commercial supply chain issue.

## What Companies Are Actually Doing

Major economies have committed substantial subsidy packages to onshore chip manufacturing, though new fabrication facilities typically take **several years minimum** to become operational, meaning near-term supply dynamics remain largely unchanged regardless of these investments.

## Conclusion

The chip shortage as a single crisis is over. The chip shortage as a structural vulnerability in modern technology supply chains is very much ongoing, just less visible to consumers than empty car lots were in 2021.

## Frequently Asked Questions

**Is the chip shortage over in 2025?**
For commodity chips, largely yes. For advanced AI-relevant chips, supply remains constrained relative to demand.

**Why does chip manufacturing concentration matter geopolitically?**
Heavy reliance on a small number of facilities in a single region creates strategic vulnerability if access were disrupted.

**How long does it take to build a new chip fabrication facility?**
Typically several years from groundbreaking to full production capacity, even with significant funding."""
    },
]


def get_examples_by_category(category: str) -> list:
    """Return all example content strings matching a category."""
    return [ex["content"] for ex in EXAMPLES if ex["category"] == category]


def get_default_examples_for_new_user() -> list:
    """
    Spread of examples across categories for a brand new user's
    starting example pool, before they've accepted any blogs of their own.
    """
    return [ex["content"] for ex in EXAMPLES]


def get_examples_with_personal_voice(category: str = None) -> list:
    """Return examples tagged as having personal/first-person voice,
    optionally filtered to a specific category."""
    filtered = [ex for ex in EXAMPLES if ex["has_personal_voice"]]
    if category:
        filtered = [ex for ex in filtered if ex["category"] == category]
    return [ex["content"] for ex in filtered]