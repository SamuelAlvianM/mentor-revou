# mentor-revou

Cinematic portfolio for Samuel Alvian (software engineer at Penbisa, RevoU mentor), written for the
RevoU cohort so they can see what real projects look like. Visual reference: activetheory.net/work.
Palette: `#4E1F6E` `#3E3E75` `#45A9A9` `#98E8DE`.

```
frontend/   Next.js 16 (src/app, TypeScript, Tailwind v4): shader background, work index, case overlays
backend/    Flask + Flask-SQLAlchemy (SQLAlchemy is the ORM; Flask is only the web framework)
scripts/    capture-shots.ps1 + make_shots.py: re-shoot live sites and optimise them into frontend/public/shots
```

## Run

Backend (port 5000):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python seed.py     # creates instance/mentor_revou.db and fills it
.\.venv\Scripts\python app.py
```

Frontend (port 3000, forwards `/api/*` to Flask via `rewrites` in `next.config.ts`):

```powershell
cd frontend
npm install
npm run dev
```

`API_URL` (default `http://127.0.0.1:5000`) tells Next where Flask lives. Frontend source lives under `frontend/src/`; components and TypeScript files use lowercase-kebab-case names.

## API

| Method | Path | |
|---|---|---|
| GET | `/api/projects`, `/api/projects/<slug>` | projects with screenshots |
| GET | `/api/profile` | skills and path |
| POST | `/api/contact` | stores a `Message` row |

Models (`backend/models.py`): `Project` 1—N `Shot`, `Skill`, `Milestone`, `Message`.

## Edit the content

Projects, skills and the timeline live in `backend/seed.py`. Edit, then re-run `python seed.py`
(it drops and recreates the tables, including contact messages).

## Screenshots

Live sites are shot from their public pages. Management Asset and Reporting System were run locally
against throwaway demo databases (no real records). Parlor Hills POS has no preview and shows a
generated schematic. Nothing from the SAM-AMANDA-GALANG folder is used. To refresh the live-site shots:

```powershell
powershell -File scripts\capture-shots.ps1 -Out .\raw
backend\.venv\Scripts\python scripts\make_shots.py .\raw
```
