"""Project content shown on the site. Edit here, then run `python seed.py`.

Facts come from the project folders and their docs; numbers are only the ones those docs state.
"""


def _shots(prefix, items):
    return [(f"{prefix}-{i}.webp", cap) for i, cap in enumerate(items, 1)]


PROJECTS = [
    {
        "slug": "penbisa", "title": "Penbisa", "logo": "/logos/penbisa.png",
        "tagline": "A studio that starts from wanting to be able.",
        "category": "Studio · Web", "role": "Software engineer", "year": "Now", "status": "Live",
        "url": "https://penbisa.id", "featured": True,
        "summary": (
            "Penbisa, short for Pengen Bisa ('I want to be able to'), designs and builds digital products "
            "for clients. This is where I work every day. The public site is a fully animated landing page "
            "with a hidden dashboard that the team uses to fill in its own content."
        ),
        "stack": ["Nuxt 4", "Nuxt UI", "Tailwind v4", "Drizzle ORM", "PostgreSQL", "anime.js", "driver.js"],
        "highlights": [
            "Thin pages, fat server: every backend route and every type lives in server/",
            "ISR public pages with no cookie reads, so they stay cache-safe",
            "Guided dashboard tours, one driver.js instance per step",
        ],
        "features": [
            ["Animated landing", "A showreel-style hero, parallax built from vectors, and a motion vocabulary reused across every page."],
            ["Portfolio with filters", "Work grouped by category (web, apps, UI/UX, brand, games) with search and counts per filter."],
            ["Services and about pages", "Service breakdowns, a story timeline and a team page, all editable without touching code."],
            ["Hidden content dashboard", "The login lives in the footer. Inside, the team edits pages, works and settings, with guided tours for new editors."],
        ],
        "build": [
            ["Rendering per page", "Public pages use ISR and never read the session cookie, otherwise they would not be safe to cache for every visitor."],
            ["Sessions in the database", "Sign-in uses a server-side session behind an httpOnly cookie instead of JWT, so a session can be revoked."],
            ["Motion budget", "anime.js is loaded lazily and imported by subpath (about 41 KB gzip saved), and everything respects prefers-reduced-motion."],
            ["Layout by user agent", "Mobile versus desktop layout is chosen on the server to avoid hydration mismatches."],
        ],
        "facts": [["On the site", "6 published works"], ["Running", "4 years"], ["Reply time", "24 hours"]],
        "links": [["Live site", "https://penbisa.id"], ["Work page", "https://penbisa.id/karya"]],
        "shots": _shots("penbisa", ["Home — showreel hero", "Home — numbers and clients", "Home — services", "Services page", "About — our story"]),
    },
    {
        "slug": "orbita", "title": "Orbita", "logo": "/logos/orbita.png",
        "tagline": "All the business notes, tidy in one place.",
        "category": "SaaS · Operations", "role": "Software engineer", "year": "2026", "status": "Live",
        "url": "https://orbitacrm.my.id", "featured": True,
        "summary": (
            "A modular operations platform: Sales, Finished-goods Logistics, Raw Material Warehouse, "
            "Production and HR, five modules that talk to each other. Each client gets their own "
            "address and their own data. The landing page previews every module with a rotating "
            "browser mockup instead of a screenshot gallery."
        ),
        "stack": ["Nuxt 4", "Nuxt UI", "Drizzle ORM", "PostgreSQL", "Highcharts", "anime.js", "driver.js"],
        "highlights": [
            "Five modules, one platform: sales, logistics, raw material, production, HR",
            "Per-client address (subdomain portals) and role-based access",
            "Trial, packages and subscription flow built in",
        ],
        "features": [
            ["Sales Management", "Clients, products, transactions and product reports in a sidebar dashboard."],
            ["Logistic and Raw Material Warehouse", "Finished-goods stock, recap reports, raw-material monitor, requests and suppliers."],
            ["Production", "Recipes, mixing stock and a request history that asks the raw-material warehouse for ingredients."],
            ["Human Resource", "Accounts, roles and settings, including who may open which module."],
            ["Client dashboard", "Subscriptions, master data, a setup checklist and a guided tour for first-time users."],
        ],
        "build": [
            ["One central database", "Modules share one PostgreSQL. HR talks to the platform API; Sales connects with a least-privilege role and row-level security."],
            ["Deploy by build output", "Each Nuxt app is built locally and only its .output is shipped, then PM2 restarts it. No install on the server."],
            ["Honest product mockups", "The hero mockup mimics the real screens of each module so visitors see that these are different apps, not one screen with swapped text."],
        ],
        "facts": [["Modules", "5 + the main platform"], ["Apps per deploy", "6 PM2 apps"], ["Pricing tiers", "4 (Free to Pro)"]],
        "links": [["Live site", "https://orbitacrm.my.id"], ["Modules", "https://orbitacrm.my.id/modul"], ["Pricing", "https://orbitacrm.my.id/harga"]],
        "shots": _shots("orbita", ["Home — module mockup", "Five connected parts", "How the work flows", "Module explorer", "Pricing", "How to start"]),
    },
    {
        "slug": "cosmos", "title": "COSMOS", "logo": "/logos/cosmos.png",
        "tagline": "Research that helps Indonesian SMEs compete.",
        "category": "Portal · CMS", "role": "Software engineer", "year": "2026", "status": "Live",
        "url": "https://cosmosriset.org", "featured": True,
        "summary": (
            "The public site and content dashboard of an Indonesian SME research center: publications, "
            "articles, news, data and products, in Indonesian and English. Editors write in a rich-text "
            "editor and the other language is drafted by an AI translator."
        ),
        "stack": ["Nuxt 4", "Drizzle ORM", "PostgreSQL", "TipTap", "nuxt-auth-utils", "i18n"],
        "highlights": [
            "153 API endpoints across 33 modules, 44 database tables",
            "Bilingual content stored in paired columns, ID to EN translation on the server",
            "Three roles (user, author, master) enforced per endpoint",
        ],
        "features": [
            ["Research and publications", "Reports, policy papers and articles with covers, categories and full-text pages."],
            ["News and data", "A news feed plus datasets about local brands and intellectual property."],
            ["Products and Codelet", "Digital products and small interactive tools (calculators, trackers) for SMEs."],
            ["Editor dashboard", "A rich-text editor, media picker, notifications and per-section editing of the front page."],
        ],
        "build": [
            ["Three ways to fill the front page", "Inline key-value editing, a page builder and a config fallback, so the home page never renders empty."],
            ["Bilingual by design", "Every piece of content has an ID and an EN field; a Gemini call on the server drafts the missing language."],
            ["Self-hosted", "PM2 on a Mac mini, deployed over SSH with a script."],
        ],
        "facts": [["API endpoints", "153"], ["Database tables", "44"], ["Pages / components", "36 / 165"], ["Server code", "about 12,700 lines"]],
        "links": [["Live site", "https://cosmosriset.org"]],
        "shots": _shots("cosmos", ["Home — stats and focus", "Research, news and products", "Latest news and products", "Articles and Codelet tools"]),
    },
    {
        "slug": "hompimplay", "title": "Hompimplay", "logo": "/logos/hompimplay.png",
        "tagline": "One codebase, six counters, one water playground.",
        "category": "POS · Kiosk", "role": "Software engineer, POS", "year": "2026", "status": "Live",
        "url": "https://dashboard.hompimplay.id", "featured": False,
        "summary": (
            "I maintain the point-of-sale system of Hompimplay, a family water playground in Bandung: "
            "ticket counters, rides, food and beverage, member kiosk and finance. Each role sees its own "
            "layout. The public site shown in the screenshots is the park's landing page; my work is the "
            "dashboard behind it."
        ),
        "stack": ["Nuxt 3", "Nuxt UI", "WebSocket", "Xendit", "pdfmake", "Laravel API"],
        "highlights": [
            "Layout chosen by role in a global middleware",
            "Live payment updates over WebSocket",
            "Printing, QR/barcode and Excel export",
        ],
        "features": [
            ["Ticket counter (loket)", "Sell tickets and packages, reprint QR, see history filtered by payment method."],
            ["Rides (wahana)", "Ride products, instructors and wristband stock."],
            ["Food and beverage", "Kitchen and bar screens, orders, menus and stock for the restaurant side."],
            ["Member kiosk", "Self-service kiosk for members: top-up, ride tickets and an idle screen."],
            ["Finance and tenants", "Finance dashboards plus tenant managers and tenant cashiers."],
        ],
        "build": [
            ["One front end, many surfaces", "Counter, kiosk, kitchen, bar, instructor, tenant and finance each get their own layout, picked from the signed-in role."],
            ["Server as a thin proxy", "Nuxt server routes forward calls to the Laravel API with the user's token from the session."],
            ["Hardware-aware", "Receipts on Epson, QR labels on Zebra, with print layouts designed for each."],
        ],
        "facts": [["Layouts", "10 role layouts"], ["Dashboard areas", "15+"], ["Payments", "Xendit + WhatsApp notices"]],
        "links": [["POS dashboard", "https://dashboard.hompimplay.id"], ["Park landing page", "https://hompimplay.id"]],
        "shots": _shots("hompimplay", ["Park landing page", "Tickets and reservations", "Rides and activities", "Zones of the park"]),
    },
    {
        "slug": "konsa", "title": "Konsa", "logo": "/logos/konsa.png",
        "tagline": "A chat assistant that answers from your own knowledge.",
        "category": "AI · Product", "role": "Software engineer", "year": "2026", "status": "In production",
        "url": "https://konsa.cosmosriset.org", "featured": False,
        "summary": (
            "Landing page, admin panel and chat for an AI assistant backed by a retrieval layer over the "
            "team's own documents. Route, then service, then Prisma, with tests for every behaviour change. "
            "Its cinematic visual style became a reusable design skill."
        ),
        "stack": ["Next.js 16", "React 19", "Prisma", "MongoDB", "Tailwind v4", "Vitest"],
        "highlights": ["Thin routes, logic in services, types in one place", "Sessions in the DB with httpOnly cookies"],
        "features": [
            ["Chat grounded in your library", "Answers come from the team's documents, with access that follows each person."],
            ["Documents on demand", "Presentations, reports and spreadsheets generated from the conversation."],
            ["Works where the team works", "Web, team channels, Telegram and WhatsApp."],
            ["Scroll-story landing", "A cinematic landing page that explains the product one idea at a time."],
        ],
        "build": [
            ["Layers", "Thin route handlers call services, services call Prisma; types and props live in dedicated files."],
            ["Tested releases", "Vitest covers services and routes; a release script builds, checks a staging port, swaps a symlink and reloads PM2."],
            ["Size", "36 service files, 59 lib files, 16 hooks and 31 type files in the web app."],
        ],
        "facts": [["Framework", "Next.js 16 + React 19"], ["Database", "MongoDB via Prisma"], ["Tests", "Vitest"]],
        "links": [["Live site", "https://konsa.cosmosriset.org"]],
        "shots": _shots("konsa", ["Landing — scroll story", "What Konsa can help with", "Works in every channel"]),
    },
    {
        "slug": "sistem-reporting", "title": "Reporting System", "logo": "/logos/sistem-reporting.png",
        "tagline": "Every technician visit, reported and traceable.",
        "category": "Field service · PWA", "role": "Software engineer", "year": "2026", "status": "Internal",
        "url": None, "featured": False,
        "summary": (
            "Visit reporting for forklift service technicians: schedules, tickets, spare-part usage, "
            "unit history and operating-permit reminders. Self-hosted, photos on disk, installable as a "
            "phone app. Screens here run on demo accounts and demo units."
        ),
        "stack": ["Nuxt 4", "Nuxt UI 4", "Drizzle ORM", "PostgreSQL", "PWA", "Highcharts", "Leaflet"],
        "highlights": [
            "Schema and migrations owned by Drizzle; migrations run on every build",
            "Media stored on disk rather than in the database",
            "Role-based menus for admin, warehouse and technicians",
        ],
        "features": [
            ["Visit schedule", "Plan technician visits and follow them from assignment to report."],
            ["Reports and spare parts", "Daily reports with photos, spare-part usage and stock levels."],
            ["Customers and units", "Customer list and a history per forklift unit."],
            ["SILO reminders", "Highlights units whose operating-permit data is missing or about to expire."],
        ],
        "build": [
            ["Installable", "A PWA with push notifications so technicians can use it from the field."],
            ["Self-hosted on purpose", "Photos live on disk, so a read-only serverless filesystem would lose them."],
            ["Migrations on build", "Drizzle migrations run as part of the build, so the schema always ships with the code."],
        ],
        "facts": [["Roles", "admin, warehouse, technician"], ["Maps", "Leaflet"], ["Charts", "Highcharts"]],
        "links": [],
        "shots": _shots("sr", ["Home — menu and permit reminder", "Forklift units"]),
    },
    {
        "slug": "management-asset", "title": "Management Asset", "logo": "/logos/aktifit.png",
        "tagline": "Scan the tag, know where the thing is.",
        "category": "Internal tool · RFID", "role": "Software engineer", "year": "2026", "status": "Internal",
        "url": None, "featured": False,
        "summary": (
            "Asset registry, loans and event tracking with RFID scanning, built as a single-page "
            "Nuxt app with its own small connector service for the reader. Every write leaves an "
            "audit line in plain language."
        ),
        "stack": ["Nuxt 4", "Prisma 7", "SQLite", "Node connector"],
        "highlights": [
            "Repository layer per entity, uniform response shape",
            "Audit log written on every change",
            "Screens shown here run on demo data, not the real records",
        ],
        "features": [
            ["Asset register", "Code, form, position, purchase and current value, status and photo, with a live total."],
            ["Loan requests", "Requester, giver, bearer and dates, with per-item condition on the way out and back."],
            ["Events and activities", "Schedule, participants and staff, linked to the loans each event needs."],
            ["Scan and history", "Scan assets in a room with an RFID reader and review who did what."],
        ],
        "build": [
            ["Single-page app", "ssr is off; auth state comes from a user key and is checked in global route middleware."],
            ["Repositories and validation", "Each entity has a repository and a validation class; every handler answers in one response shape."],
            ["Reader connector", "A separate Node service next to the app talks to the RFID reader."],
        ],
        "facts": [["PM2 apps", "2 (app + connector)"], ["Database", "SQLite"], ["Modes", "SPA"]],
        "links": [],
        "shots": _shots("ma", ["Event management menu", "Asset register", "Loan requests", "Events and activities"]),
    },
    {
        "slug": "cheverse", "title": "CHEVERSE", "logo": "/logos/cheverse.svg",
        "tagline": "Chemistry as a galaxy you can play with.",
        "category": "Experiment · 3D", "role": "Solo — design and code", "year": "2026", "status": "Local build",
        "url": None, "featured": False,
        "summary": (
            "A semi-game for chemical engineering, born from my degree: a periodic table with "
            "animated Bohr models, a mass-balance calculator, and a reaction balancer with 2.5D "
            "animation, all inside a neon-purple starfield."
        ),
        "stack": ["Nuxt 4", "TresJS", "Three.js", "Tailwind v4"],
        "highlights": [
            "All 118 elements on an accurate grid, click for shells, density, melting point",
            "Editable electron shells: add or remove electrons by hand",
            "Mr to moles to particles converter and stoichiometry solver",
        ],
        "features": [
            ["Periodic table", "118 elements, category filters and a detail panel with an animated Bohr model."],
            ["Mass balance", "Inputs into a reactor, conversion slider and a breakdown of the outgoing streams."],
            ["Chemical reaction", "Balance an equation, find the limiting reagent and watch a 2.5D animation of it."],
        ],
        "build": [
            ["One dataset", "Ar leads to Mr leads to stoichiometry, so the three modules share the same element data."],
            ["Adaptive atoms", "Shell rings scale with the number of shells so large elements do not overlap."],
        ],
        "facts": [["Elements", "118"], ["Modules", "3"], ["Scene", "TresJS starfield"]],
        "links": [],
        "shots": _shots("cheverse", ["Module select", "Periodic table", "Element detail", "Mass balance", "Reaction balancer"]),
    },
    {
        "slug": "compassionate-companion", "title": "Compassionate Companion", "logo": "/logos/cc-website.svg",
        "tagline": "A quiet site for a community of accompaniment.",
        "category": "Community · CMS", "role": "Software engineer", "year": "2026", "status": "Live",
        "url": "https://compassionate-companion.com", "featured": False,
        "summary": (
            "A bilingual site for a learning community rooted in Ignatian spirituality, with programs, "
            "events, a journal and a separate admin area. Serif type, warm earth palette, slow motion."
        ),
        "stack": ["Nuxt 4", "Drizzle ORM", "PostgreSQL", "i18n"],
        "highlights": ["Single-process Nuxt app: frontend and API together", "Bilingual ID / EN with an admin area"],
        "features": [
            ["Programs and events", "Cards for retreats and workshops with dates, places and registration links."],
            ["Journal", "Reflections published by the community."],
            ["Admin area", "Members sign in; admins manage events and content."],
        ],
        "build": [
            ["One process", "Frontend and API run in a single Nuxt app."],
            ["Quiet design", "Serif headings, a warm palette and restrained motion to match the tone of the community."],
        ],
        "facts": [["Languages", "ID / EN"], ["Sections", "About, Events, Journal"]],
        "links": [["Live site", "https://compassionate-companion.com"]],
        "shots": _shots("cc", ["Home", "Programs and gatherings", "Spiritual journey"]),
    },
    {
        "slug": "alvians-kitchen", "title": "Alvian's Kitchen", "logo": "/logos/alvians-kitchen.png",
        "tagline": "Recipes, ingredient costs and sales for a family food shop.",
        "category": "Internal · Solo project", "role": "Solo — design and code", "year": "2026", "status": "Internal",
        "url": None, "featured": False,
        "summary": (
            "A solo internal tool for a small cake and food shop: recipes with their ingredients, the cost "
            "of raw materials, the cost of goods sold (HPP) per recipe, plus sales and customers. "
            "It is private, so only the logo is shown here."
        ),
        "stack": ["Nuxt", "Drizzle ORM", "PostgreSQL"],
        "highlights": ["Cost of goods calculated from recipe ingredients", "Users with forced first-login password change"],
        "features": [
            ["Recipes", "Each recipe lists its ingredients and quantities."],
            ["Raw materials", "Ingredient prices that feed the cost of every recipe."],
            ["HPP", "Cost of goods per recipe, recalculated when ingredient prices change."],
            ["Sales and customers", "Record sales and keep a customer list."],
        ],
        "build": [
            ["Small and private", "Admin-managed users; a new account must change its password on first login."],
        ],
        "facts": [["Type", "Solo internal project"]],
        "links": [],
        "shots": [],
    },
]
