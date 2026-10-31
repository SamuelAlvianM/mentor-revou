"""Reset and fill the database. Run: python seed.py

Facts come from Samuel's CV and the project folders in C:\\sam\\work.
Projects without screenshots (internal systems) get no Shot rows;
the frontend draws a schematic panel for them.
"""
import json

from app import app
from projects_data import PROJECTS
from models import Milestone, Project, Shot, Skill, db

SKILLS = {
    "Languages": ["TypeScript", "Python", "JavaScript", "PHP", "Rust"],
    "Frameworks": ["Next.js", "Nuxt", "React", "NestJS", "Laravel", "Flask", "Node.js", "Tailwind CSS"],
    "Data": ["PostgreSQL", "MySQL", "SQLite", "Prisma", "Drizzle ORM", "SQLAlchemy"],
    "Dev tools": ["DBeaver", "Postman", "Bruno", "Swagger", "9router"],
    "Ship": ["Docker", "Railway", "Netlify", "Vercel", "PM2", "Git"],
}

MILESTONES = [
    ("Now", "Software Engineer · DevOps", "Penbisa",
     "Web app developer building websites, apps and internal systems for clients and for our own studio. "
     "DevOps: system security and deployment for servers. AI engineer: building a personal AI system "
     "as a private assistant."),
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
                url=p["url"], featured=p["featured"], position=i, logo=p["logo"],
                stack_json=json.dumps(p["stack"]), highlights_json=json.dumps(p["highlights"]),
                features_json=json.dumps(p["features"]), build_json=json.dumps(p["build"]),
                facts_json=json.dumps(p["facts"]), links_json=json.dumps(p["links"]),
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
