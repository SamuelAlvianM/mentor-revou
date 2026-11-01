# Graph Report - mentor-revou  (2026-10-31)

## Corpus Check
- 55 files · ~305,344 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 325 nodes · 582 edges · 22 communities (14 shown, 5 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 19 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `467f2412`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- functions.tsx
- experience.tsx
- devDependencies
- lesson-page.tsx
- compilerOptions
- array-methods.tsx
- models.py
- memory.tsx
- logic.tsx
- mentor-revou Agent Guide
- app/layout.tsx
- mentor-revou
- deploy.sh
- frontend/README.md
- make_icons.py
- frontend/AGENTS.md
- eslint.config.mjs
- next.config.ts
- make_shots.py

## God Nodes (most connected - your core abstractions)
1. `Tape` - 29 edges
2. `compilerOptions` - 16 edges
3. `CodeTabs()` - 12 edges
4. `H2()` - 12 edges
5. `P()` - 12 edges
6. `C()` - 12 edges
7. `Callout()` - 12 edges
8. `Quiz()` - 12 edges
9. `DualCode` - 11 edges
10. `Player()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `create_app()` --uses--> `Milestone`  [INFERRED]
  backend/app.py → backend/models.py
- `create_app()` --uses--> `Project`  [INFERRED]
  backend/app.py → backend/models.py
- `create_app()` --uses--> `Skill`  [INFERRED]
  backend/app.py → backend/models.py
- `generateMetadata()` --calls--> `findLesson()`  [EXTRACTED]
  frontend/src/app/learning/[slug]/page.tsx → frontend/src/lib/learning.ts
- `Page()` --calls--> `findLesson()`  [EXTRACTED]
  frontend/src/app/learning/[slug]/page.tsx → frontend/src/lib/learning.ts

## Import Cycles
- None detected.

## Communities (22 total, 5 thin omitted)

### Community 0 - "functions.tsx"
Cohesion: 0.07
Nodes (44): CodeTabs(), Highlight(), KEYWORDS, Lang, LANG_LABEL, code, t, cart (+36 more)

### Community 1 - "experience.tsx"
Cohesion: 0.08
Nodes (27): dynamic, Home(), About(), delay(), LAYERS, CaseOverlay(), Contact(), State (+19 more)

### Community 2 - "devDependencies"
Cohesion: 0.06
Nodes (34): eslint, eslint-config-next, dependencies, next, react, react-dom, simple-icons, devDependencies (+26 more)

### Community 3 - "lesson-page.tsx"
Cohesion: 0.10
Nodes (17): metadata, delay(), LearningHome(), dynamicParams, generateMetadata(), Page(), Cursor(), LearningShell() (+9 more)

### Community 4 - "compilerOptions"
Cohesion: 0.07
Nodes (28): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+20 more)

### Community 5 - "array-methods.tsx"
Cohesion: 0.15
Nodes (15): access(), Film, FILMS, pop(), push(), s(), search(), shift() (+7 more)

### Community 6 - "models.py"
Cohesion: 0.19
Nodes (14): create_app(), Message, Milestone, _now(), Project, SQLAlchemy models. Relationships: Project 1-N Shot. This is the ORM layer.…, Contact form submissions., Shot (+6 more)

### Community 7 - "memory.tsx"
Cohesion: 0.22
Nodes (11): ArrVal, Box, BoxView(), clone(), isArr(), isObj(), ObjVal, Prim (+3 more)

### Community 9 - "mentor-revou Agent Guide"
Cohesion: 0.29
Nodes (6): Build, lint, and checks, Conventions, Dev environment, mentor-revou Agent Guide, Pitfalls, Repository layout

### Community 10 - "app/layout.tsx"
Cohesion: 0.33
Nodes (4): grotesk, metadata, plex, viewport

### Community 11 - "mentor-revou"
Cohesion: 0.33
Nodes (5): API, Edit the content, mentor-revou, Run, Screenshots

### Community 12 - "deploy.sh"
Cohesion: 0.70
Nodes (4): err(), log(), deploy.sh script, warn()

### Community 13 - "frontend/README.md"
Cohesion: 0.50
Nodes (3): Deploy on Vercel, Getting Started, Learn More

### Community 14 - "make_icons.py"
Cohesion: 0.50
Nodes (3): Image, Build the round header logo and favicons from the ORIGINAL (undistorted) SAM…, round_icon()

## Knowledge Gaps
- **112 isolated node(s):** `eslintConfig`, `nextConfig`, `name`, `version`, `private` (+107 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 173 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tape` connect `array-methods.tsx` to `functions.tsx`, `memory.tsx`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `Cursor()` connect `lesson-page.tsx` to `experience.tsx`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `ShaderBackground()` connect `lesson-page.tsx` to `experience.tsx`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **What connects `eslintConfig`, `nextConfig`, `name` to the rest of the system?**
  _112 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `functions.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.0715962441314554 - nodes in this community are weakly interconnected._
- **Should `experience.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.080338266384778 - nodes in this community are weakly interconnected._
- **Should `devDependencies` be split into smaller, more focused modules?**
  _Cohesion score 0.05714285714285714 - nodes in this community are weakly interconnected._