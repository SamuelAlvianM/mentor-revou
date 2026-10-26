"""SQLAlchemy models. Relationships: Project 1-N Shot.

This is the ORM layer. Flask itself is only the web framework;
Flask-SQLAlchemy wires SQLAlchemy (the actual ORM) into it.
"""
import json
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    title = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    stack_json = db.Column(db.Text, nullable=False, default="[]")
    highlights_json = db.Column(db.Text, nullable=False, default="[]")
    url = db.Column(db.String(200))
    status = db.Column(db.String(40), nullable=False, default="Live")
    featured = db.Column(db.Boolean, nullable=False, default=False)
    position = db.Column(db.Integer, nullable=False, default=0)

    shots = db.relationship(
        "Shot",
        backref="project",
        order_by="Shot.position",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "title": self.title,
            "tagline": self.tagline,
            "summary": self.summary,
            "category": self.category,
            "role": self.role,
            "year": self.year,
            "stack": json.loads(self.stack_json),
            "highlights": json.loads(self.highlights_json),
            "url": self.url,
            "status": self.status,
            "featured": self.featured,
            "shots": [s.to_dict() for s in self.shots],
        }


class Shot(db.Model):
    __tablename__ = "shots"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    src = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(160), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self) -> dict:
        return {"src": self.src, "caption": self.caption}


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)


class Milestone(db.Model):
    __tablename__ = "milestones"

    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    place = db.Column(db.String(120), nullable=False)
    detail = db.Column(db.Text, nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)


class Message(db.Model):
    """Contact form submissions."""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=_now)
