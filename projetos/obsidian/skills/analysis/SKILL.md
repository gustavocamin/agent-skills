---
name: analysis
description: Analyze your Obsidian vault to surface patterns, connections, contradictions, and emerging ideas. Use when the user invokes /snapshot, /map, /trace, /connect, /contradict, /drift, /bloom, /emerge, or /ideas.
---

# Analysis Skill

Commands for deep vault analysis. Each command reads the vault structure and note
contents to produce insights the user cannot easily see themselves.

**Vault location:** all PARA folders live inside `second-brain/` relative to the
working directory. The root contains only directories — no loose `.md` files.
Each PARA folder may contain subdirectories (e.g. `second-brain/01. Projects/Trip OS/`),
so always traverse recursively (glob `**/*.md`) when reading a folder.

---

## /snapshot

**Full picture of who you are, what you're working on, and what you care about now.**

1. Read all files in `second-brain/01. Projects/` recursively (active work + next actions)
2. Read all files in `second-brain/02. Areas/` recursively (ongoing responsibilities)
3. Read recent notes in `second-brain/00. Inbox/` recursively (what's on the radar)
4. Read `second-brain/02. Areas/Personal Development/` recursively for values and goals
5. Synthesize into three sections:
   - **Who**: identity, values, professional context (from CV, career notes, goals)
   - **Now**: active projects, current priorities, next actions
   - **Cares about**: recurring themes, open questions, unresolved tensions

Output: prose summary, max 400 words. No lists unless three or more items.

---

## /map

**Full vault topology scan: clusters, orphans, dead ends, link density, intellectual landscape.**

1. Walk every `.md` file in `second-brain/` recursively, excluding `second-brain/Readwise/` and `second-brain/_resources/`
2. Build a link graph: for each file, record outgoing `[[wikilinks]]`
3. Compute:
   - **Clusters**: groups of ≥3 files that heavily link to each other
   - **Orphans**: files with zero incoming and zero outgoing links
   - **Dead ends**: files linked to by others but that link nowhere themselves
   - **Hubs**: files with the highest incoming link count
   - **Link density per folder**: ratio of links to files
4. Output a structured report:
   - Top 5 hubs (most linked-to notes)
   - Cluster map by folder/theme
   - Orphan list with folder location
   - Dead ends list
   - 3–5 observations about the intellectual landscape

---

## /trace [topic]

**Tracks how an idea evolved across the vault; builds a synonym vocabulary and traces the full arc.**

1. Accept a topic as argument (e.g., `/trace liderança`)
2. Build a synonym/related-term vocabulary: search the vault for the term and collect
   nearby words, alternate spellings, and related concepts used in context
3. Search all notes in `second-brain/` recursively (including Readwise) for any occurrence of the topic or synonyms
4. Sort matches chronologically by `created` frontmatter date
5. Output:
   - Synonym vocabulary discovered
   - Timeline of appearances: date → note → key sentence
   - Observations on how framing, tone, or depth shifted over time
   - Notes where the idea appears most developed

---

## /emerge

**Finds implicit or unstated ideas suggested by patterns across notes.**

1. Read all notes in `second-brain/02. Areas/` and `second-brain/03. Resources/` recursively
2. Look for:
   - Topics mentioned in 3+ unrelated notes that have no dedicated note of their own
   - Recurring questions or tensions that are never resolved
   - Concepts always referenced but never defined
   - Themes that appear across multiple PARA layers simultaneously
3. Output each emergent idea as:
   - **Idea**: one sentence naming the implicit concept
   - **Evidence**: 2–3 notes where it appears
   - **Gap**: what note or synthesis is missing

---

## /connect [A] [B]

**Finds non-obvious bridges and shared themes between two domains or notes.**

1. Accept two arguments (topics, note names, or folder names)
2. Retrieve all notes related to A and all notes related to B
3. Identify:
   - Shared vocabulary used in both domains
   - Notes that reference both
   - Structural parallels (similar patterns, frameworks, or tensions)
   - A third concept that mediates between the two
4. Output:
   - 3–5 bridges ranked by non-obviousness
   - For each bridge: the connecting concept + one quote from each side
   - One synthesis sentence the user has not written yet

---

## /contradict

**Finds incompatible beliefs, claims, or intentions across different notes.**

1. Read all notes in `second-brain/02. Areas/`, `second-brain/03. Resources/`, and `second-brain/01. Projects/` recursively
2. Extract declarative claims and stated beliefs (sentences with "is", "should",
   "always", "never", "I believe", "the key is", etc.)
3. Group claims by theme
4. Within each group, identify pairs that are logically incompatible or in tension
5. Output each contradiction as:
   - **Claim A**: quote + source note
   - **Claim B**: quote + source note
   - **Tension**: one sentence naming the contradiction
   - **Possible resolution**: one question to help the user decide

---

## /drift

**Compares stated intentions vs. actual behavior; surfaces avoidance patterns.**

1. Read `second-brain/01. Projects/` and `second-brain/02. Areas/` recursively for stated goals, intentions, and next actions
2. Read `second-brain/00. Inbox/` and `second-brain/04. Archiving/` recursively for what actually got done or abandoned
3. Look for:
   - Projects with goals but no recent progress notes
   - Areas with aspirations but no linked resources or actions
   - Topics that appear in intentions but never in actual work
   - Inbox items that keep getting deferred
4. Output:
   - **Gaps**: stated intention → evidence of no follow-through
   - **Avoidance patterns**: themes consistently deferred or underdeveloped
   - **Honest summary**: 2–3 sentences on the delta between intention and action

---

## /bloom [question]

**Maps all notes relevant to a question with relevance scores and connections.**

1. Accept a question as argument (e.g., `/bloom O que me impede de avançar na carreira?`)
2. Read all vault notes in `second-brain/` recursively, excluding `second-brain/_resources/` and `second-brain/Readwise/Full Document Contents/`
3. Score each note 0–3 for relevance to the question:
   - 0: unrelated
   - 1: tangentially related (shares a word or theme)
   - 2: directly relevant (addresses part of the question)
   - 3: central (would be a node in an answer)
4. For notes scoring ≥ 2, identify connections between them
5. Output:
   - Core notes (score 3) with key excerpt
   - Supporting notes (score 2) with one-line summary
   - Connections: pairs of notes that speak to each other around this question
   - One synthesis paragraph answering the question from the vault's perspective
   - Gaps: what the vault doesn't yet address about this question

---

## /ideas

**Deep 30-day scan with cross-domain pattern and graph analysis to generate novel ideas.**

1. Read all notes with `created` or `modified` within the last 30 days
2. Also read the top 10 hub notes (highest incoming link count) for stable context
3. Identify:
   - Recurring unresolved problems
   - Concepts from different domains that use parallel structures
   - Questions asked but never answered
   - Half-formed thoughts in Inbox notes
4. Generate ideas as combinations, inversions, or extensions of existing material:
   - **Combination**: merge two separate concepts into one new idea
   - **Inversion**: what if the opposite of a stated belief were true?
   - **Extension**: take an idea further than the notes currently go
   - **Application**: apply a framework from one domain to a problem in another
5. Output 5–7 ideas, each with:
   - **Idea**: one clear sentence
   - **Origin**: which notes it emerges from
   - **Why it's non-obvious**: what the vault currently misses that enables this
   - **First step**: one concrete action to develop it further
