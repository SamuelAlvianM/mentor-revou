import os
import re
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from models import Message, Milestone, Project, Skill, db

BASE_DIR = Path(__file__).resolve().parent
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_app() -> Flask:
    load_dotenv(BASE_DIR / ".env")

    app = Flask(__name__)
    app.json.sort_keys = False  # keep skill groups in seed order (Languages, Frameworks, ...)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'mentor_revou.db'}"
    )
    (BASE_DIR / "instance").mkdir(exist_ok=True)

    origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    CORS(app, resources={r"/api/*": {"origins": origins}})

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", projects=Project.query.count())

    @app.get("/api/projects")
    def projects():
        rows = Project.query.order_by(Project.position).all()
        return jsonify([p.to_dict() for p in rows])

    @app.get("/api/projects/<slug>")
    def project(slug: str):
        row = Project.query.filter_by(slug=slug).first_or_404()
        return jsonify(row.to_dict())

    @app.get("/api/profile")
    def profile():
        skills: dict[str, list[str]] = {}
        for s in Skill.query.order_by(Skill.position).all():
            skills.setdefault(s.group, []).append(s.name)
        milestones = [
            {"period": m.period, "title": m.title, "place": m.place, "detail": m.detail}
            for m in Milestone.query.order_by(Milestone.position).all()
        ]
        return jsonify(skills=skills, milestones=milestones)

    @app.post("/api/contact")
    def contact():
        data = request.get_json(silent=True) or {}
        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip()
        body = str(data.get("body", "")).strip()
        if not name or not EMAIL_RE.match(email) or len(body) < 5:
            return jsonify(error="Please fill in name, a valid email and a message."), 400
        if len(name) > 120 or len(email) > 200 or len(body) > 4000:
            return jsonify(error="Message is too long."), 400
        db.session.add(Message(name=name, email=email, body=body))
        db.session.commit()
        return jsonify(ok=True), 201

    return app


app = create_app()

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG") == "1")
