# Content Doctrine — Microsoft AI / Azure / Copilot LinkedIn Feed

> This file is the north star. It overrides any older topic guidance in any skill file, command file, or script prompt.

---

## Brand Identity

**Author:** Abhinav Jain  
**Niche:** Microsoft AI ecosystem — Azure, Copilot, Power Platform, AI Foundry, RAG, AI Search  
**Positioning:** The trusted, practical voice for professionals navigating the Microsoft AI landscape.  
**Audience:** IT professionals, Azure practitioners, business decision-makers, Power Platform developers, developers and architects adopting Microsoft AI — people who work in or alongside Microsoft technology stacks.  
**Voice archetype:** The senior colleague who has already done the hard work, distilled it, and now makes it clear for everyone else.

---

## Topic Filter (every post must pass all 4)

| Gate | Question |
|------|----------|
| **Relevance** | Does this touch Microsoft AI, Azure, Copilot, Power Platform, or adjacent Microsoft technology? |
| **Stakes** | Does the reader's job, career, productivity, or project outcome improve because of this post? |
| **Accuracy** | Can every fact, stat, or claim be verified from a Microsoft official source, blog, or credible tech publication? |
| **Practicality** | Does this help someone do something, understand something, or decide something — today? |

---

## The 5 Daily Streams

| Stream | Format | Topic Lane |
|--------|--------|-----------|
| **News** | Short text (150–250 words) | Microsoft AI / Azure / Copilot / AI Foundry announcements this week |
| **Tips & Tricks** | Short text (100–200 words) | Practical how-tos: Power Platform, Azure, Copilot Studio, AI Search |
| **Carousel** | 7 slides + caption | Deep-dive: RAG architecture, Copilot Studio, Prompt Flow, AI Search, Azure OpenAI |
| **Infographic** | 1080×1080 PNG + caption text | Microsoft/Azure adoption data, product comparisons, feature matrices |
| **Motivation / Productivity** | Short text (150–250 words) | AI productivity hacks using Microsoft tools (Copilot, Power Automate, Teams) |

---

## AMPLIFY List (what to write more of)

- Azure OpenAI Service: real integration patterns, not marketing copy
- Microsoft Copilot across M365, Teams, Outlook, Word — practical daily use
- Power Platform: Power Automate, Power Apps, Copilot Studio workflows with concrete outcomes
- RAG (Retrieval-Augmented Generation) on Azure AI Search — architecture decisions
- AI Foundry: model deployment, evaluation, prompt engineering on the platform
- Productivity gains that are specific and measurable (minutes saved, steps reduced)
- "How I configured X in 5 steps" style tips that are instantly actionable
- Comparisons: Azure AI Search vs alternatives, GPT-4o vs GPT-4.1 for specific use cases
- Microsoft certification and skills that are in demand now

---

## DROP List (never write about)

- Generic AI hype ("AI will change everything") without Microsoft-specific context
- OpenAI/Anthropic/Google product launches that have no Microsoft angle
- Motivational content disconnected from a specific Microsoft tool or practice
- Startup tactics, indie-hacker advice, build-in-public content
- SaaS metrics, CAC, MRR, churn — general business operations not tied to AI tools
- Unverified claims, hallucinated statistics, or vague "studies show" without a source
- Tool-config step-by-step tutorials longer than a post allows (link to Docs instead)
- Clickbait alarmism ("AI will steal your job by next Tuesday")

---

## Writing Rules (apply to every post, every stream)

1. **First-person allowed** for tips and motivation streams — "Here is what I do in Power Automate..."
2. **Third-person observer voice** for news and infographic captions
3. **Specific numbers always win** — "saves 40 minutes/day" beats "saves a lot of time"
4. **Source everything** — reference the Microsoft Blog, Azure Updates, Microsoft Learn, or a named report
5. **No em-dashes** — use commas, semicolons, or periods instead
6. **Hook under 120 characters** — never start with "I" or "Did you know"
7. **Line break every 1–2 sentences** for readability
8. **End every post with a question or clear CTA** — never "what do you think?"
9. **No hashtag spam** — 1–3 relevant hashtags maximum, at the end
10. **Accuracy over speed** — if a fact is uncertain, remove it or verify it before publishing

---

## Banned Words (never use in any post)

game-changer, disruptive, hustle, grind, crush it, synergy, paradigm shift, thought leader, go viral, revolutionary, groundbreaking, unprecedented, cutting-edge, state-of-the-art, next-generation, empower, unlock, journey, ecosystem, world-class, comprehensive, curated, innovative, transformative, passionate, excited to share, delve, underscore, vibrant, tapestry, interplay, intricate, garner, pivotal, showcase, foster, align with, landscape, leverages, encompasses, facilitates, utilized, commenced, subsequent to, prior to, in order to, stands as, serves as, is a testament to, plays a vital role, game-changing, supercharge.

---

## Banned LinkedIn Patterns

- "No X. No Y. Just Z."
- "It's not just about X. It's about Y."
- "And here's the kicker"
- "X changed everything"
- "Enter:"
- "Not because of X. But because of Y."
- "Not just X, but also Y"
- "This isn't about X, it's about Y"
- Email sign-off language ("To your success", "Rooting for you")

---

## Deduplication

Before picking any topic for any stream:
1. Check `infographic-run-log.json` — last 14 topics are banned for infographic
2. Check `carousel-hook-log.json` — last hook style is banned for carousel
3. No two posts on the same day should cover the same product/feature angle

---

## Accuracy Standard

Every statistic, product claim, or feature description must cite its source in the post metadata (for the history log), even if the source is not shown in the post body. Never invent stats. If a specific number is not findable, write around it with observable facts instead.
