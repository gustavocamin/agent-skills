---
name: thinking-tools
description: Enhance perspective, argument, and insight using your vault as the source. Use when the user invokes /ghost, /challenge, /stranger, /compound, or /week.
---

# Thinking Tools Skill

Commands that use your vault to think harder, argue better, and see yourself more clearly.
Each command treats the vault as primary evidence — no outside knowledge is injected unless
explicitly requested.

**Vault location:** all PARA folders live inside `second-brain/` relative to the
working directory. The root contains only directories — no loose `.md` files.
Each PARA folder may contain subdirectories, so always traverse recursively
(glob `**/*.md`) when reading a folder.

---

## /ghost [question]

**Answers a question as you, drawing from your notes, beliefs, and writing style.**

1. Accept an optional question. If none given, answer: "What do I actually think right now?"
2. Read:
   - `second-brain/02. Areas/` for stated values, recurring priorities, and ongoing responsibilities
   - `second-brain/02. Areas/Personal Development/` for beliefs, principles, and goals
   - `second-brain/01. Projects/` for current context and decisions in progress
   - Recent `second-brain/00. Inbox/` notes for unprocessed thoughts
   - Any journal or reflection notes in `second-brain/03. Resources/` or periodic notes
3. Extract:
   - Recurring positions and stances (what the user defends across multiple notes)
   - Characteristic framings (how they tend to structure problems)
   - Vocabulary and tone patterns
4. Answer the question in first person, as the user would answer it based on the evidence.
   Do not invent positions — only express what the vault supports.
5. At the end, add one line: "Source confidence: X/3" where X reflects how much explicit
   material exists (1 = inferred, 2 = partially supported, 3 = directly stated).

Output: prose, 200–350 words. No headers. First person throughout.

---

## /challenge

**Argues against your current thinking using evidence from the vault.**

1. Read all notes in `second-brain/01. Projects/`, `second-brain/02. Areas/`, and `second-brain/03. Resources/`
2. Extract the user's dominant positions: stated goals, beliefs, frameworks, and decisions
3. For each position, find:
   - Notes that contain contradicting evidence (even if unintentional)
   - Readwise highlights that challenge the position
   - Cases where a past self held a different view
   - Structural weaknesses in the reasoning (missing assumptions, circular logic)
4. Construct the strongest possible case against each dominant position using only
   vault-sourced material. Steel-man the opposition before critiquing.
5. Output 3–5 challenges, each structured as:
   - **Position you hold**: one sentence
   - **The counter**: argument with vault evidence
   - **What this demands of you**: one question you'd have to answer to defend your view

Do not soften challenges to be polite. The goal is productive discomfort.

---

## /stranger

**Portrait of you as seen by an outside reader of your vault.**

1. Read a broad cross-section of the vault:
   - All of `second-brain/02. Areas/` (who you say you are and what you care about)
   - A sample of `second-brain/03. Resources/` (what you read and study)
   - All of `second-brain/01. Projects/` (what you actually pursue)
   - `second-brain/04. Archiving/` for historical patterns
2. Adopt the perspective of an intelligent, neutral reader who knows nothing about the
   user except what the vault contains.
3. Observe:
   - What themes dominate the vault by sheer volume?
   - What is conspicuously absent given the stated interests?
   - What tensions are visible between different parts of the vault?
   - What does the vault suggest this person is afraid of, drawn to, or avoiding?
   - What would a stranger conclude about this person's identity, obsessions, and blindspots?
4. Write a portrait in third person. Be honest and specific — cite notes by name where
   relevant. Avoid flattery. Avoid harshness for its own sake.

Output: prose, 300–500 words. Third person. No bullet points.

---

## /compound [question]

**Answers the same question at three points in time; shows how context compounds.**

1. Accept a question as argument (e.g., `/compound O que é sucesso para mim?`)
2. Identify three time periods from the vault:
   - **Past**: oldest notes available (Archiving, early created dates)
   - **Middle**: notes from roughly the midpoint of the vault's timeline
   - **Now**: notes from the last 60 days
3. For each period, answer the question using only notes from that period as evidence.
   Extract direct quotes where possible.
4. After the three answers, write a synthesis:
   - What changed and what didn't
   - Which shifts were conscious (explicitly stated) vs. invisible (only visible in retrospect)
   - What the trajectory suggests about where things are heading
5. Output three labeled sections (Past / Middle / Now) + one synthesis paragraph.
   Each period: 100–150 words. Synthesis: 100–150 words.

Use `created` frontmatter dates to determine periods. If dates are sparse, use folder
location and note content as proxies.

---

## /week

**Weekly review across calendar, tasks, 7–14 days of notes, context files, and recent captures.**

1. Determine the review window: last 7 days (extend to 14 if notes are sparse).
2. Gather:
   - All daily/periodic notes created in the window (from `Periodic Notes` plugin output)
   - All notes modified in the window across the full vault
   - All items in `second-brain/00. Inbox/` (regardless of date)
   - All `second-brain/01. Projects/` notes — check `status` and last `modified` date
   - `second-brain/02. Areas/` for responsibilities that may have been neglected
3. Process in order:
   - **Inbox**: list items pending triage; suggest disposition for each (project / area / resource / discard)
   - **Projects**: for each active project, state last action taken and current next action; flag any with no activity in 7+ days
   - **Areas**: flag any area with no note activity in the window
   - **Captures**: highlight the most interesting idea or insight that arrived this week
   - **Patterns**: one observation about the week as a whole — what dominated, what was avoided
4. Close with one question to carry into the next week.

Output: structured, but not bureaucratic. Skip sections that have nothing to report.
Use plain prose for observations; use a short list only when items ≥ 3.
