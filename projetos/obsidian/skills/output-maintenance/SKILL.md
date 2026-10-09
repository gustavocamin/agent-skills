---
name: output-maintenance
description: Create outputs and maintain the vault's health and potential. Use when the user invokes /backlinks, /graduate, /learned, /weekly-learnings, /make, /money, /leverage, or /xarticle.
---

# Output & Maintenance Skill

Commands for turning vault content into external outputs and keeping the vault
structurally sound. The vault is only as valuable as what it produces and how well
it's connected.

**Vault location:** all PARA folders live inside `second-brain/` relative to the
working directory. The root contains only directories — no loose `.md` files.
Each PARA folder may contain subdirectories, so always traverse recursively
(glob `**/*.md`) when reading a folder.

---

## /backlinks

**Finds missing links and wires new connections across the vault.**

1. Walk every `.md` file in `second-brain/` recursively, excluding `second-brain/Readwise/Full Document Contents/` and `second-brain/_resources/`
2. For each file, extract:
   - The note's title (stem) and key concepts from its body
   - Its existing outgoing `[[wikilinks]]`
3. Build a candidate link list:
   - For each note, find other notes whose title appears as plain text (unlinked mention)
     in the body prose — excluding code blocks, tables, and image embeds
   - Also flag notes that share 3+ significant content words with another note but have
     no link between them
4. Filter candidates:
   - Skip links that already exist
   - Skip self-links
   - Skip mentions shorter than 5 characters
   - Skip generic terms (articles, prepositions, common verbs)
5. For each candidate link:
   - Show: source note → target note → the sentence containing the unlinked mention
   - Suggest whether to link inline (replace the word in context) or add to a
     `## Veja também` footer section
6. Do not write changes automatically. Present the candidates and ask: "Aplicar todos,
   selecionar, ou revisar primeiro?"
7. If the user confirms, apply inline links first; use footer only for proximity-based
   suggestions with no prose anchor.

---

## /graduate

**Promotes ideas from daily notes and inbox captures into permanent notes.**

1. Read:
   - All notes in `second-brain/00. Inbox/`
   - All periodic/daily notes from the last 30 days
2. Identify candidates for graduation — content that meets at least two criteria:
   - Appears in more than one note (recurrence signal)
   - Has been elaborated beyond a single sentence
   - Is referenced or linked from another note
   - Feels like a principle, framework, or claim rather than a task or event
3. For each candidate:
   - Name the emerging note: propose a clear, specific title (not a date)
   - Summarize the core idea in 2–3 sentences using the source material
   - List the source notes it should be distilled from
   - Suggest the correct PARA layer: `second-brain/03. Resources/` for concepts and frameworks,
     `second-brain/02. Areas/` if it's a recurring responsibility, `second-brain/01. Projects/` if it's actionable
4. Present the list of candidates with their proposed titles and layer assignments.
   Ask: "Criar todos, selecionar, ou ajustar primeiro?"
5. When confirmed, create each permanent note with full frontmatter and backlinks to
   the source notes. Move processed inbox items to their correct layer or mark them
   for archiving.

---

## /learned [topic]

**Mines the vault and generates three drafts: short post, personal essay, universal essay.**

1. Accept a topic as argument. If none given, use `/ideas` logic to identify the most
   developed theme in the vault right now.
2. Mine the vault for all material on the topic:
   - Direct notes (title or body matches topic)
   - Readwise highlights tagged or related to the topic
   - Inbox captures mentioning the topic
   - Periodic notes where the topic surfaced
3. Distill the core insight: the one thing the vault actually knows about this topic
   that is specific, earned, and non-obvious.
4. Generate three drafts from the same insight:

   **Draft 1 — Short post (X/LinkedIn format)**
   - 150–250 words
   - Opens with the insight stated plainly, no windup
   - Supports with one concrete example from the vault
   - Closes with implication or question
   - No headers, no bullet lists

   **Draft 2 — Personal essay**
   - 400–600 words
   - Opens with a specific moment or note from the vault
   - Develops the idea through personal experience and reflection
   - Uses "I" throughout
   - Closes with what changed or what remains unresolved

   **Draft 3 — Universal essay**
   - 400–600 words
   - Opens with the general problem the insight addresses
   - Develops through logic and examples (can use vault examples but frames them
     as "someone I know" or "a common pattern")
   - Uses "you" or third person
   - Closes with a transferable principle

5. Label each draft clearly. Do not blend the formats.

---

## /weekly-learnings

**Compiles the week's insights from daily notes into a single summary.**

1. Read all periodic/daily notes created or modified in the last 7 days
2. Also read `second-brain/00. Inbox/` notes created this week
3. Extract:
   - Explicit insights (sentences starting with "Percebi", "Aprendi", "Descobri",
     "I realized", "I learned", or similar markers)
   - Repeated themes across multiple days (even without explicit markers)
   - Decisions made and the reasoning given
   - Questions that emerged but weren't answered
4. Deduplicate and cluster by theme
5. Output a structured summary:

```
## Aprendizados da semana — [date range]

**Insights principais**
- [insight] → [source note]

**Temas recorrentes**
- [theme]: [brief description of how it surfaced]

**Decisões tomadas**
- [decision] — [reasoning in one sentence]

**Perguntas em aberto**
- [question]
```

6. Suggest which insights are strong enough to graduate into permanent notes (flag
   with `→ candidato a nota permanente`).

---

## /make

**Finds mature ideas, scores readiness, and suggests formats.**

1. Read all notes in `second-brain/03. Resources/` and `second-brain/02. Areas/` — look for density signals:
   - Notes with 3+ outgoing links
   - Notes that are linked to by 3+ other notes
   - Notes with substantial body content (> 300 words)
   - Topics that appear across multiple PARA layers
2. Score each candidate idea on three axes (1–3 each):
   - **Depth**: how developed is the thinking? (1 = rough, 3 = argued and supported)
   - **Originality**: how specific to the user's experience or perspective? (1 = generic, 3 = singular)
   - **Timeliness**: how alive is this idea right now in the vault? (1 = dormant, 3 = active)
3. For each idea scoring ≥ 6 total:
   - Propose 2–3 output formats that suit it:
     - Essay / article
     - Framework or model (diagram, matrix, checklist)
     - Thread or post series
     - Talk or presentation
     - Product, tool, or service
     - Course or workshop
   - For each format, write one sentence on why it fits this specific idea
4. Output ranked list (highest score first) with format suggestions.
   Flag the single highest-potential idea as the recommended starting point.

---

## /money

**Surfaces monetization opportunities, diagnoses revenue blockers, recommends actions.**

1. Read:
   - `second-brain/02. Areas/Career/` and `second-brain/02. Areas/Business/` for professional context
   - `second-brain/01. Projects/` for active work and deliverables
   - Any notes mentioning income, clients, consulting, products, or services
   - `/leverage` output if recently run (or run it as a sub-step)
2. Map the current revenue picture:
   - Existing income sources (explicit or inferable from notes)
   - Skills and knowledge available to monetize (from `/leverage`)
   - Ideas for products, services, or content that appear in the vault but haven't
     been acted on
3. Diagnose blockers:
   - What ideas exist but have no project attached?
   - What skills are well-documented but not offered?
   - What content is nearly ready to publish but stalled?
   - What relationships or audiences exist that could be activated?
4. Recommend 3–5 actions ranked by: effort required × speed to revenue × alignment
   with vault priorities. Format each as:
   - **Opportunity**: one sentence
   - **Evidence from vault**: which notes support this
   - **Blocker**: what's preventing it
   - **Next action**: one concrete step

Do not invent business ideas from scratch. Only surface what the vault already contains.

---

## /leverage

**Finds 3–7 skills and knowledge areas with outsized potential payoff.**

1. Read:
   - `second-brain/02. Areas/Career/` for professional skills and experience
   - `second-brain/03. Resources/` for studied topics and accumulated knowledge
   - `second-brain/01. Projects/` for applied skills (what the user actually does, not just studies)
   - Any CV, bio, or self-description notes
2. Build a skills inventory from vault evidence:
   - Explicit skills (named in notes)
   - Implicit skills (demonstrated through project work, decisions, frameworks used)
   - Knowledge domains with depth (topics with 3+ notes, Readwise highlights, or
     referenced in multiple projects)
3. Score each skill/area on:
   - **Rarity**: how uncommon is this combination? (1 = common, 3 = rare or unusual pairing)
   - **Demand**: does the vault suggest others need this? (1 = unclear, 3 = explicitly in demand)
   - **Development**: how developed is it? (1 = surface, 3 = deep and practiced)
4. Identify the 3–7 highest-scoring areas. For each:
   - Name the skill or knowledge area precisely
   - Describe the specific edge: what makes the user's version of this non-generic
   - Suggest one leverage move: how to apply, amplify, or combine it for outsized return
5. Close with: "The rarest combination in this vault: [X + Y]" — the intersection that
   is hardest for others to replicate.

---

## /xarticle

**Suggests next writing topics based on graph density, current energy, and synthesis potential.**

1. Run three scans in parallel:

   **Graph density scan**
   - Find topics with the highest link density (notes that are heavily linked to and from)
   - These are intellectually mature areas where synthesis is already possible

   **Energy scan**
   - Find topics modified or created in the last 30 days
   - Find topics appearing in Inbox or daily notes recently
   - These are alive right now

   **Synthesis gap scan**
   - Find topics with many related notes but no single note that ties them together
   - These are ready to be written: the material exists, the synthesis doesn't

2. Identify the intersection: topics that score in at least two of the three scans
3. For each candidate topic (aim for 5–7):
   - **Topic**: specific, writable title (not a category — a claim or question)
   - **Why now**: which scan(s) it appeared in
   - **Angle**: the specific argument or perspective this vault enables on the topic
   - **Format fit**: recommended format (short post / essay / thread / long-form)
   - **Estimated readiness**: how much writing vs. synthesizing is left (% ready)
4. Rank by: (energy × synthesis gap) — favor topics that are both alive and underwritten.
   Flag the single best starting point.
