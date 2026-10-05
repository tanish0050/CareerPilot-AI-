from pathlib import Path
import re, io
from fastapi import FastAPI,Form,File,UploadFile,HTTPException
from fastapi.responses import FileResponse
from pypdf import PdfReader
app=FastAPI(title="CareerPilot AI")
BASE=Path(__file__).parent
ROLES=[
 {"title":"Data Scientist","description":"Build predictive models and solve data problems.","skills":["python","sql","machine learning","statistics","pandas","scikit-learn","tensorflow","data analysis"],"learning_path":["Model evaluation","Feature engineering","ML projects"]},
 {"title":"Backend Developer","description":"Design APIs, services, databases and reliable backends.","skills":["python","sql","fastapi","django","api","docker","git","java"],"learning_path":["REST APIs","Databases","Docker deployment"]},
 {"title":"Full Stack Developer","description":"Build complete web applications.","skills":["javascript","react","html","css","node.js","python","sql","api","git"],"learning_path":["Architecture","Authentication","Deployment"]},
 {"title":"Data Analyst","description":"Turn data into reports and decisions.","skills":["sql","excel","python","tableau","power bi","statistics","pandas"],"learning_path":["Advanced SQL","Dashboards","Portfolio project"]},
 {"title":"AI/ML Engineer","description":"Build and evaluate practical machine-learning and AI systems.","skills":["python","machine learning","pytorch","tensorflow","scikit-learn","llm","generative ai","data analysis","sql"],"learning_path":["Model evaluation","Retrieval and AI systems","Deployment and monitoring"]},
 {"title":"Database Engineer","description":"Design reliable data models, tune queries, and operate database systems.","skills":["sql","postgresql","mysql","mongodb","redis","database design","query optimization","data modeling","etl"],"learning_path":["Relational modeling","Query plans and indexing","Migrations and data quality"]}]
SKILLS=sorted({x for r in ROLES for x in r['skills']},key=len,reverse=True)
PROJECT_IDEAS = {
 "Data Scientist": "Use a public dataset to build an end-to-end prediction project: clean data, compare a baseline with one model, explain the metric, and publish a notebook, README, and demo.",
 "Backend Developer": "Build and deploy a REST API with authentication, SQL storage, validation, automated tests, Docker, and clear OpenAPI docs.",
 "Full Stack Developer": "Ship a full-stack app that solves one real problem, with a React UI, API, database, login, tests, and a live demo.",
 "Data Analyst": "Create a business case study from a public dataset: SQL analysis, a Tableau/Power BI dashboard, and a one-page recommendation with evidence.",
 "AI/ML Engineer": "Build a citation-first AI assistant for public policy documents: answer with exact source passages, abstain when evidence is weak, and publish a small evaluation set with citation-accuracy results.",
 "Database Engineer": "Build a data-quality and schema-drift monitor that versions public datasets, detects breaking changes and query regressions, and generates a tested migration plan with rollback notes."
}
def growth_plan(text, role):
    checks = {
        "projects": r"\b(projects?|portfolio|github|capstone|deployed|built|developed)\b",
        "internships": r"\b(intern(ship)?|trainee|apprentice)\b",
        "hackathons": r"\b(hackathons?|hackfest|devpost)\b",
        "community": r"\b(open[- ]source|volunteer|student club|tech club|community|meetup|extracurricular|leadership)\b"
    }
    present = {name: bool(re.search(pattern, text, re.I)) for name, pattern in checks.items()}
    guides = [
        {"category":"Portfolio project", "signal":"projects", "action":PROJECT_IDEAS[role], "resource_label":"Find a project home", "resource_url":"https://github.com/"},
        {"category":"Hackathons", "signal":"hackathons", "action":"Join a college or online hackathon in the next 30 days. Build a small working demo with a 2–4 person team, present it, and link the result only after you participate.", "resource_label":"Explore hackathons", "resource_url":"https://devpost.com/hackathons"},
        {"category":"Internships", "signal":"internships", "action":"Apply each week to a few relevant paid internships, apprenticeships, or entry-level roles. Tailor your resume, include your project demo, and track follow-ups.", "resource_label":"Search internships", "resource_url":"https://www.linkedin.com/jobs/"},
        {"category":"Extracurricular & community", "signal":"community", "action":"Join a campus tech club or relevant developer community; contribute a small open-source fix or volunteer on a real project, then document your exact contribution.", "resource_label":"Find beginner issues", "resource_url":"https://github.com/topics/good-first-issue"}
    ]
    for guide in guides:
        guide["in_resume"] = present[guide["signal"]]
    if present["projects"]:
        guides[0]["action"] = "Polish your strongest project with a clear problem statement, your exact contribution, tests, a README, and a working demo. Add a measurable result only if you can support it."
    if present["hackathons"]:
        guides[1]["action"] = "For each hackathon, document the event and year, your team role, what you built, and a repo or demo. Add awards only if you actually received them; try a domain-specific event next."
    if present["internships"]:
        guides[2]["action"] = "Make your internship entry specific: list the feature or task you owned, tools used, and a verifiable outcome. Keep confidential company details out of the public portfolio."
    if present["community"]:
        guides[3]["action"] = "Make your community work concrete: name the group, describe your actual contribution and its outcome, and link a public PR, event, or volunteer deliverable when appropriate."
    return guides

def project_recommendations(found, preferred_role=""):
    tracks = [
        {"track":"AI / ML", "title":"Citation-First Policy Copilot with a Truthfulness Benchmark", "concept":"Let users ask questions about public campus or city-service policies; every answer must cite the exact source passage or say it cannot verify the answer.", "twist":"Create a 60-question test set and report citation accuracy, retrieval quality, and unsupported-answer rate instead of presenting a chatbot demo alone.", "skills":["python","machine learning","pytorch","tensorflow","scikit-learn","llm","generative ai","data analysis","sql"], "stack":"Python, FastAPI, SQLite FTS5; add embeddings or a local LLM only after the baseline works."},
        {"track":"Backend", "title":"Duplicate-Proof Reservation API Under Load", "concept":"Build an API for reserving limited appointment slots where retries, race conditions, and service restarts must never create double bookings.", "twist":"Demonstrate idempotency keys, database transactions, an audit trail, and a load test with p95 latency and zero overbookings.", "skills":["python","fastapi","django","api","docker","sql","redis","git","java","node.js"], "stack":"FastAPI or Node.js, PostgreSQL, Docker, and optional Redis plus k6 for load testing."},
        {"track":"Database", "title":"Schema-Drift and Data-Quality Observatory", "concept":"Track changing versions of a public dataset and surface schema changes, duplicate keys, null spikes, and slow query regressions before a dashboard silently breaks.", "twist":"Keep a lineage/audit log and generate a proposed migration with validation checks and rollback instructions; compare query plans before and after indexes.", "skills":["sql","postgresql","mysql","mongodb","redis","database design","query optimization","data modeling","etl"], "stack":"PostgreSQL or DuckDB, SQL, Python, and a small FastAPI dashboard; start with SQLite if databases are new."}
    ]
    for track in tracks:
        matched = [skill for skill in track["skills"] if skill in found]
        track["matched_skills"] = matched
        track["fit_score"] = round(100 * len(matched) / len(track["skills"]))
        track["next_skills"] = [skill for skill in track["skills"] if skill not in matched][:4]
    preferred_track = {
        "AI/ML Engineer": "AI / ML", "Data Scientist": "AI / ML",
        "Backend Developer": "Backend", "Full Stack Developer": "Backend",
        "Database Engineer": "Database", "Data Analyst": "Database"
    }.get(preferred_role)
    tracks.sort(key=lambda track: (track["track"] != preferred_track, -track["fit_score"]))
    tracks[0]["focus_reason"] = "Selected career track" if preferred_track else "Strongest resume overlap"
    return tracks

def skills(t): return [x for x in SKILLS if re.search(rf'(?<![\w.+#]){re.escape(x)}(?![\w.+#])',t,re.I)]
def pdf(b):
 try:
  x=' '.join(p.extract_text() or '' for p in PdfReader(io.BytesIO(b)).pages).strip()
  if not x: raise ValueError()
  return x
 except: raise HTTPException(400,'PDF text extract nahi ho saka. Text-based PDF upload karein ya resume paste karein.')
@app.get('/')
def home(): return FileResponse(BASE/'index.html')
@app.get('/api/roles')
def roles(): return [{'title':r['title'],'description':r['description']} for r in ROLES]
@app.post('/api/analyze')
async def analyze(resume_text:str=Form(''),job_description:str=Form(''),target_role:str=Form(''),resume_file:UploadFile|None=File(None)):
 text=resume_text
 if resume_file and resume_file.filename:
  raw=await resume_file.read(8*1024*1024+1)
  if len(raw)>8*1024*1024: raise HTTPException(400,'PDF must be 8 MB or smaller.')
  text+=' '+pdf(raw)
 if not text.strip(): raise HTTPException(400,'Paste resume text or choose a PDF first.')
 found=skills(text)
 out=[]
 for r in ROLES:
  match=[x for x in r['skills'] if x in found]; miss=[x for x in r['skills'] if x not in match]; score=round(18+70*len(match)/len(r['skills']))
  out.append({'title':r['title'],'description':r['description'],'score':score,'matched_skills':match,'missing_skills':miss[:5],'learning_path':r['learning_path']})
 out.sort(key=lambda x:x['score'],reverse=True)
 if target_role:
  out.sort(key=lambda x:x['title']!=target_role)
 selected_role = target_role if target_role in PROJECT_IDEAS else out[0]['title']
 jd=skills(job_description); jm=[x for x in jd if x in found]
 return {'word_count':len(text.split()),'profile_score':min(100,round(len(found)/10*100)),'resume_skills':found,'recommendations':out[:3],'growth_plan':growth_plan(text, selected_role),'project_recommendations':project_recommendations(found,target_role),'job_match':None if not jd else {'score':round(100*len(jm)/len(jd)),'matched_skills':jm,'missing_skills':[x for x in jd if x not in jm]},'note':'Scores are guidance, not hiring probabilities.'}

@app.post("/api/ai-review")
def ai_review(resume_text: str = Form(""), job_description: str = Form("")):
    import os
    from openai import OpenAI
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(503, "AI is not configured yet. Add OPENAI_API_KEY in Render Environment Variables.")
    if len(resume_text.strip()) < 40:
        raise HTTPException(400, "Paste at least a short resume summary for an AI review.")
    prompt = f"""Review this resume for a job seeker. Be practical, concise and encouraging. Return Markdown with: 1) strengths, 2) missing/weak areas, 3) 3 improved resume bullets, 4) next 3 career actions. Never invent experience.\n\nRESUME:\n{resume_text[:12000]}\n\nJOB DESCRIPTION (optional):\n{job_description[:6000]}"""
    try:
        response = OpenAI().responses.create(model=os.getenv("OPENAI_MODEL", "gpt-5-mini"), instructions="You are an expert resume coach and ATS reviewer.", input=prompt)
        return {"review": response.output_text}
    except Exception as exc:
        raise HTTPException(502, "AI review could not be completed. Check Render API key and model settings.") from exc

ROADMAPS = {
 "Data Scientist": [("Python & data foundations", ["python","pandas","sql"], "Python tutorial + Pandas practice", "https://docs.python.org/3/tutorial/"), ("Statistics & EDA", ["statistics","data analysis"], "Analyze a public dataset", "https://www.kaggle.com/learn"), ("Machine learning", ["machine learning","scikit-learn"], "Build and evaluate a classifier", "https://scikit-learn.org/stable/getting_started.html"), ("Portfolio & interview", ["git"], "Publish two projects and practice explanations", "https://docs.github.com/")],
 "Backend Developer": [("Python & API basics", ["python","fastapi"], "Build a CRUD API", "https://fastapi.tiangolo.com/tutorial/"), ("Databases", ["sql"], "Design a small database", "https://www.postgresql.org/docs/"), ("Deployment", ["docker","git"], "Containerize and deploy your API", "https://docs.docker.com/get-started/")],
 "Full Stack Developer": [("Web foundations", ["html","css","javascript"], "Build a responsive portfolio", "https://developer.mozilla.org/en-US/docs/Learn_web_development"), ("Frontend app", ["react"], "Build a dashboard with an API", "https://react.dev/learn"), ("Backend & deploy", ["python","sql","git"], "Ship a full-stack capstone", "https://fastapi.tiangolo.com/")],
 "Data Analyst": [("SQL & spreadsheets", ["sql","excel"], "Answer five business questions with a clean dataset", "https://www.kaggle.com/learn/intro-to-sql"), ("Analysis & visualization", ["python","pandas","tableau","power bi"], "Build a dashboard and explain three insights", "https://www.kaggle.com/learn/data-visualization"), ("Portfolio & storytelling", ["statistics","data analysis"], "Publish an end-to-end case study with recommendations", "https://github.com/")],
 "AI/ML Engineer": [("AI foundations & evaluation", ["python","machine learning","scikit-learn"], "Build a baseline classifier and report precision, recall, and failure cases", "https://scikit-learn.org/stable/getting_started.html"), ("Retrieval and grounded answers", ["llm","generative ai","sql"], "Build the policy copilot with citations and a small labeled evaluation set", "https://platform.openai.com/docs/guides/retrieval"), ("Ship and monitor", ["fastapi","docker","git"], "Deploy the service and publish latency, citation accuracy, and abstention results", "https://fastapi.tiangolo.com/deployment/")],
 "Database Engineer": [("Relational data modeling", ["sql","database design","data modeling"], "Model a realistic booking or inventory database with constraints and seed data", "https://www.postgresql.org/docs/current/ddl.html"), ("Indexes and query plans", ["postgresql","query optimization"], "Compare EXPLAIN plans and benchmark queries before and after indexes", "https://www.postgresql.org/docs/current/using-explain.html"), ("Migrations and quality", ["etl","python","git"], "Build schema-drift checks, validation tests, migration history, and rollback notes", "https://docs.getdbt.com/docs/build/data-tests")]
}
@app.post("/api/roadmap")
def roadmap(resume_text: str = Form(""), target_role: str = Form(""), weekly_hours: int = Form(10)):
    found = skills(resume_text)
    role = target_role if target_role in ROADMAPS else "Data Scientist"
    weekly_hours = min(max(weekly_hours, 1), 40)
    weeks_per_stage = max(2, round(20 / max(weekly_hours, 3)))
    plan=[]
    for idx,(title,needed,task,url) in enumerate(ROADMAPS[role]):
        missing=[x for x in needed if x not in found]
        plan.append({"week_start":idx*weeks_per_stage+1,"week_end":(idx+1)*weeks_per_stage,"title":title,"focus":missing or needed,"task":task,"resource":{"label":"Start learning","url":url},"estimated_hours":weeks_per_stage*weekly_hours})
    readiness=min(95, 25+len(found)*7+sum(1 for x in ["projects","github","intern"] if x in resume_text.lower())*8)
    return {"role":role,"weekly_hours":weekly_hours,"total_weeks":len(plan)*weeks_per_stage,"job_readiness":readiness,"plan":plan,"projects":["Build one project with a clear README and demo", "Turn a real-world problem into a portfolio case study", "Practice explaining decisions in a 3-minute video"],"note":"Timeline is an estimate; consistent project work matters more than speed."}

INTERVIEW_BANK = {
 "Data Scientist": ["Explain the difference between overfitting and underfitting.", "How would you evaluate a classification model?", "Walk through one data project: data, approach, metric, outcome."],
 "Backend Developer": ["How would you design a secure REST API?", "Explain indexing and when it helps a SQL query.", "How would you debug a slow endpoint in production?"],
 "Full Stack Developer": ["How does a frontend communicate with a backend API?", "How do you manage state in a React application?", "Explain a project architecture you would choose and why."],
 "Data Analyst": ["How do you turn a business question into an analysis?", "What checks do you perform before trusting a dataset?", "How would you present a dashboard insight to a non-technical stakeholder?"],
 "AI/ML Engineer": ["How would you measure whether a retrieval-augmented answer is grounded in its sources?", "What should a system do when the model has low confidence or no supporting evidence?", "How would you monitor quality and latency after deploying an AI feature?"],
 "Database Engineer": ["How do you use an execution plan to decide whether an index will help?", "How would you roll out a schema change without breaking existing clients?", "How would you detect and recover from data-quality drift in a production pipeline?"]
}
@app.post("/api/mock-interview")
def mock_interview(target_role: str = Form("")):
    role = target_role if target_role in INTERVIEW_BANK else "Data Scientist"
    return {"role": role, "questions": INTERVIEW_BANK[role], "tip": "Use STAR for experience questions: Situation, Task, Action, Result. Record a 2-minute answer and improve it."}
