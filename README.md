# CareerPilot AI

**A resume-to-career planning tool** that turns a resume and optional job description into role matches, skill gaps, a learning roadmap, and portfolio project recommendations.

> CareerPilot AI is a planning aid. Its match/readiness scores are heuristic signals—not hiring probabilities or guarantees.

## What it does

- **Resume input:** paste resume text or upload a text-based PDF (up to 8 MB).
- **Role matching:** compare skills across Data Scientist, Backend Developer, Full Stack Developer, Data Analyst, AI/ML Engineer, and Database Engineer paths.
- **Job-description comparison:** see recognized matching and missing skills when a job description is provided.
- **Learning roadmap:** get role-focused stages, weekly time estimates, deliverables, and learning links; choose a weekly study-hours target.
- **Project blueprints:** receive resume-aware AI/ML, backend, and database project concepts with a differentiating twist, suggested stack, matching skills, and skills to learn next.
- **Career-building actions:** get ideas for portfolio work, hackathons, internships, and extracurricular/community contributions.
- **Interview practice:** load role-specific practice questions.
- **PDF report:** download a formatted CareerPilot AI report with profile signals, matches, roadmap, project ideas, and next steps.
- **Progress tracking:** roadmap checklist progress is saved in the browser's local storage.

## Tech stack

- Python and FastAPI
- Vanilla HTML, CSS, and JavaScript
- `pypdf` for text-based PDF extraction
- Render deployment configuration in `render.yaml`

## Run locally

Requires Python 3.10 or later.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open **http://127.0.0.1:8000** in your browser. Keep the server terminal running while you use the app.

## Deploy to Render

1. Push this repository to GitHub.
2. In Render, create a **Web Service** and connect the repository.
3. Render can use the included `render.yaml`. If entering settings manually, use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Deploy and open the service URL provided by Render.

The current career-analysis, roadmap, interview, and PDF-report features do not require an API key.

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Serve the CareerPilot web app |
| `GET` | `/api/roles` | List supported career roles |
| `POST` | `/api/analyze` | Analyze resume text/PDF and optional job description |
| `POST` | `/api/roadmap` | Generate a role roadmap from resume text and weekly hours |
| `POST` | `/api/mock-interview` | Return role-specific interview questions |

FastAPI's interactive API docs are available at **`/docs`** while the server is running.

## Privacy and limitations

- Resume PDFs are parsed in memory; the app does not save uploaded resume files to disk.
- Roadmap completion state is stored in the current browser using local storage; it is not synced between devices.
- Skill matching uses a curated keyword list. Different wording or unrecognized skills may not be detected.
- Scanned/image-only PDFs may not contain extractable text and may need OCR before upload.
- Project ideas are starting points, not a claim that no similar project exists. Make a project distinct through its users, data, evaluation, and implementation decisions.
- Do not include confidential employer or personal information in a public portfolio.

## License

No license has been added yet. Unless a license is added, standard copyright applies and reuse permissions are not automatically granted.
