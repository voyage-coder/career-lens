# AI Resume Analyzer and Career Coach

React + Vite + TypeScript frontend; FastAPI + SQLAlchemy backend; PostgreSQL-ready database; Gemini API integration with local NLP heuristics.

## Run backend
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # on Windows; use cp on macOS/Linux
uvicorn app.main:app --reload

## Run frontend (new terminal)
cd frontend
npm install
npm run dev

Frontend http://localhost:5173 | API docs http://localhost:8000/docs

SQLite is the local default. Set DATABASE_URL to a PostgreSQL connection string for deployment. Add GEMINI_API_KEY to backend/.env to enable Gemini career coaching. ATS score is an explainable heuristic estimate, not an official ATS score. Email verification, password reset delivery, cloud file storage, admin UI, and production load testing remain follow-up work.
