"""Reset and fill the database. Run: python seed.py

Facts come from Samuel's CV and the project folders in C:\\sam\\work.
Projects without screenshots (internal systems) get no Shot rows;
the frontend draws a schematic panel for them.
"""
import json

from app import app
from models import Milestone, Project, Shot, Skill, db

PROJECTS = [
    {
        "slug": "penbisa",
        "title": "Penbisa",
        "tagline": "A studio that starts from wanting to be able.",
        "category": "Studio · Web",
        "role": "Software engineer",
        "year": "Now",
        "status": "Live",
        "url": "https://penbisa.id",
        "featured": True,
        "summary": (
            "Penbisa — short for Pengen Bisa, 'I want to be able to' — designs and builds digital "
            "products for clients. This is where I work every day. The site is a fully animated "
            "landing page with a hidden dashboard that the team uses to fill in its own content."
        ),
        "stack": ["Nuxt 4", "Nuxt UI", "Tailwind v4", "Drizzle ORM", "PostgreSQL", "anime.js", "driver.js"],
        "highlights": [
            "Thin pages, fat server: every backend route and every type lives in server/",
            "ISR public pages with no cookie reads, so they stay cache-safe",
            "Guided dashboard tours, one driver.js instance per step",
        ],
        "shots": [
            ("penbisa-home.webp", "Home — showreel hero"),
            ("penbisa-karya.webp", "Work — filterable portfolio"),
        ],
    },
    {
        "slug": "orbita",
        "title": "Orbita",
        "tagline": "All the business notes, tidy in one place.",
        "category": "SaaS · Operations",
        "role": "Software engineer",
        "year": "2026",
        "status": "Live",
        "url": "https://orbitacrm.my.id",
        "featured": True,
        "summary": (
            "A modular operations platform: Sales, Finished-goods Logistics, Raw Material Warehouse, "
            "Production and HR — five modules that talk to each other. Each client gets their own "
            "address and their own data. The landing page previews every module with a rotating "
            "browser mockup instead of a screenshot gallery."
        ),
        "stack": ["Nuxt 4", "Nuxt UI", "Drizzle ORM", "PostgreSQL", "Highcharts", "anime.js", "driver.js"],
        "highlights": [
            "Five modules, one platform: sales, logistics, raw material, production, HR",
            "Per-tenant database configuration and subdomain portals",
            "Trial, packages and subscription flow built in",
        ],
        "shots": [
            ("orbita-home.webp", "Home — module mockup"),
            ("orbita-parts.webp", "Five connected parts"),
            ("orbita-modul.webp", "Module explorer"),
            ("orbita-start.webp", "How to start"),
        ],
    },
    {
        "slug": "cosmos",
        "title": "COSMOS",
        "tagline": "Research that helps Indonesian SMEs compete.",
        "category": "Portal · CMS",
        "role": "Software engineer",
        "year": "2026",
        "status": "Live",
        "url": "https://cosmosriset.org",
        "featured": True,
        "summary": (
            "The public site and content dashboard of an Indonesian SME research center: "
            "publications, articles, news, data and products, in Indonesian and English. "
            "Editors write in a rich-text editor and the other language is drafted by an AI translator."
        ),
        "stack": ["Nuxt 4", "Drizzle ORM", "PostgreSQL", "TipTap", "nuxt-auth-utils", "i18n"],
        "highlights": [
            "153 API endpoints across 33 modules, 44 database tables",
            "Bilingual content stored in paired columns, ID ↔ EN translation on the server",
            "Three roles — user, author, master — enforced per endpoint",
        ],
        "shots": [
            ("cosmos-home.webp", "Home — stats and focus"),
            ("cosmos-products.webp", "Products"),
        ],
    },
    {
        "slug": "cheverse",
        "title": "CHE-VERSE",
        "tagline": "Chemistry as a galaxy you can play with.",
        "category": "Experiment · 3D",
        "role": "Solo — design and code",
        "year": "2026",
        "status": "Local build",
        "url": None,
        "featured": True,
        "summary": (
            "A semi-game for chemical engineering, born from my degree: a periodic table with "
            "animated Bohr models, a mass-balance calculator, and a reaction balancer with 2.5D "
            "animation, all inside a neon-purple starfield."
        ),
        "stack": ["Nuxt 4", "TresJS", "Three.js", "Tailwind v4"],
        "highlights": [
            "All 118 elements on an accurate grid, click for shells, density, melting point",
            "Editable electron shells: add or remove electrons by hand",
            "Mr → moles → particles converter and stoichiometry solver",
        ],
        "shots": [("cheverse.webp", "Module select")],
    },
    {
        "slug": "compassionate-companion",
        "title": "Compassionate Companion",
        "tagline": "A quiet site for a community of accompaniment.",
        "category": "Community · CMS",
        "role": "Software engineer",
        "year": "2026",
        "status": "Live",
        "url": "https://compassionate-companion.com",
        "featured": False,
        "summary": (
            "A bilingual site for a learning community rooted in Ignatian spirituality, with events, "
            "a journal and a separate admin area. Serif type, warm earth palette, slow motion."
        ),
        "stack": ["Nuxt 4", "Drizzle ORM", "PostgreSQL", "i18n"],
        "highlights": ["Single-process Nuxt app: frontend and API together", "Bilingual ID / EN with an admin area"],
        "shots": [("cc-home.webp", "Home")],
    },
    {
        "slug": "konsa",
        "title": "Konsa",
        "tagline": "A chat assistant that answers from your own knowledge.",
        "category": "AI · Product",
        "role": "Software engineer",
        "year": "2026",
        "status": "In production",
        "url": "https://konsa.cosmosriset.org",
        "featured": False,
        "summary": (
            "Landing page, admin panel and chat for an AI assistant backed by a retrieval layer. "
            "Route → service → Prisma, with tests for every behaviour change. Its cinematic clay "
            "visual style became a reusable design skill."
        ),
        "stack": ["Next.js 16", "React 19", "Prisma", "MongoDB", "Tailwind v4", "Vitest"],
        "highlights": ["Thin routes, logic in services, types in one place", "Sessions in the DB with httpOnly cookies"],
        "shots": [
            ("konsa-1.webp", "Landing — scroll story"),
            ("konsa-2.webp", "What Konsa can help with"),
        ],
    },
    {
        "slug": "sistem-reporting",
        "title": "Sistem Reporting",
        "tagline": "Every technician visit, reported and traceable.",
        "category": "Field service · PWA",
        "role": "Software engineer",
        "year": "2026",
        "status": "Internal",
        "url": None,
        "featured": False,
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
        "shots": [
            ("sr-home.webp", "Home — menu and permit reminder"),
            ("sr-unit.webp", "Forklift units"),
        ],
    },
    {
        "slug": "management-asset",
        "title": "Management Asset",
        "tagline": "Scan the tag, know where the thing is.",
        "category": "Internal tool · RFID",
        "role": "Software engineer",
        "year": "2026",
        "status": "Internal",
        "url": None,
        "featured": False,
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
        "shots": [
            ("ma-home.webp", "Event management menu"),
            ("ma-list.webp", "Asset register"),
            ("ma-loans.webp", "Loan requests"),
            ("ma-events.webp", "Events and activities"),
        ],
    },
    {
        "slug": "parlor-hills",
        "title": "Parlor Hills POS",
        "tagline": "One codebase, six counters, one playground.",
        "category": "POS · Kiosk",
        "role": "Software engineer",
        "year": "2026",
        "status": "Internal",
        "url": None,
        "featured": False,
        "summary": (
            "Point-of-sale front end for an indoor playground: ticket counter, member kiosk, "
            "kitchen and bar screens, ride instructors and finance — each with its own layout, "
            "picked by the signed-in role. Payments through Xendit, live updates over WebSocket."
        ),
        "stack": ["Nuxt 3", "Nuxt UI", "WebSocket", "Xendit", "pdfmake"],
        "highlights": ["Layout chosen by role in a global middleware", "Printing, QR/barcode and Excel export"],
        "shots": [],
    },
]

SKILLS = {
    "Languages": ["TypeScript", "Python", "JavaScript", "Rust"],
    "Frameworks": ["Next.js", "Nuxt", "React", "NestJS", "Flask", "Node.js", "Tailwind CSS"],
    "Data": ["PostgreSQL", "MySQL", "SQLite", "Prisma", "Drizzle ORM", "SQLAlchemy"],
    "Ship": ["Docker", "Railway", "Netlify", "PM2", "Git"],
}

MILESTONES = [
    ("Now", "Software Engineer", "Penbisa", "Building websites, apps and internal systems for clients and for our own studio."),
    ("Oct 2024 — May 2025", "Team Leader, Faculty", "RevoU · Full Stack Software Engineering",
     "Led 12 students through structured sessions, simulations and mentoring. 85% of those who started "
     "struggling and demotivated came back to meet and exceed the assignment criteria."),
    ("Aug 2024 — Jan 2025", "Project: POS Elola", "RevoU project", "A point-of-sale system."),
    ("Jun — Oct 2024", "Backend, WeRent & SaleMate", "Project",
     "RESTful API for a renting system on NestJS, PostgreSQL and AWS S3; 100% of it used by the web app."),
    ("Oct 2023 — May 2024", "Full Stack Software Engineering", "RevoU",
     "Certificates of Achievement and Excellence. Flask, Next.js, TypeScript, Prisma, PostgreSQL."),
    ("Oct 2022 — Jun 2023", "Quality Assurance", "Ataya Nata Walet",
     "Chemical engineer turned engineer: ISO 22000 food safety for 80 employees before I wrote code for a living."),
]


def run() -> None:
    with app.app_context():
        db.drop_all()
        db.create_all()
        for i, p in enumerate(PROJECTS):
            row = Project(
                slug=p["slug"], title=p["title"], tagline=p["tagline"], summary=p["summary"],
                category=p["category"], role=p["role"], year=p["year"], status=p["status"],
                url=p["url"], featured=p["featured"], position=i,
                stack_json=json.dumps(p["stack"]), highlights_json=json.dumps(p["highlights"]),
            )
            row.shots = [
                Shot(src=f"/shots/{src}", caption=cap, position=j) for j, (src, cap) in enumerate(p["shots"])
            ]
            db.session.add(row)
        n = 0
        for group, names in SKILLS.items():
            for name in names:
                db.session.add(Skill(group=group, name=name, position=n))
                n += 1
        for i, (period, title, place, detail) in enumerate(MILESTONES):
            db.session.add(Milestone(period=period, title=title, place=place, detail=detail, position=i))
        db.session.commit()
        print(f"seeded {len(PROJECTS)} projects, {n} skills, {len(MILESTONES)} milestones")


if __name__ == "__main__":
    run()
