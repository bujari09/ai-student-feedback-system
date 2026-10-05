# AI Student Feedback System

Cloud Computing project (Master in Computer Science): a system that collects anonymous student feedback, stores it in a cloud database, analyzes sentiment and main topics with Google Cloud NLP, and presents the results on a dashboard.

> Work in progress. The project is built in phases. This README will be expanded with installation, deployment, and testing details as the phases are completed.

## Architecture

```text
User → React Dashboard → Nginx (Compute Engine VM) → FastAPI Backend
                                                      ├── Firestore (Cloud Database)
                                                      └── Cloud Natural Language API / Vertex AI Gemini
                                                              ↓
                                                      Sentiment + Topic Analysis → Dashboard
```

## Technologies

| Layer | Technology |
|---|---|
| Infrastructure | Google Compute Engine (e2-micro, Ubuntu 24.04 LTS) |
| Backend | Python 3.12, FastAPI, Pydantic |
| Database | Google Cloud Firestore (Native mode) |
| NLP | Google Cloud Natural Language API, Vertex AI Gemini (fallback for unsupported languages) |
| Frontend | React + Vite |
| Web server | Nginx |

## Project status

| Phase | Status |
|---|---|
| 1. Google Cloud project, billing, APIs | ✅ Done |
| 2. VM configuration (Compute Engine) | ✅ Done |
| 3. Documentation structure (Google Drive) | ✅ Done |
| 4. Cloud Database (Firestore) | ✅ Done |
| 5. Backend FastAPI | ✅ Done |
| 6–7. NLP: sentiment and topic analysis | ⏳ In progress |
| 8–9. React dashboard and integration | ⏳ Planned |
| 10–12. Testing, deployment, final report | ⏳ Planned |

## API endpoints (current)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Service and database status |
| POST | `/api/feedback` | Submit anonymous feedback |
| GET | `/api/feedback` | List the latest feedback |

## Security

- No credentials in the repository. The app uses Google Application Default Credentials: the VM's service account in the cloud, `gcloud auth application-default login` locally.
- Configuration through `.env` (see `backend/.env.example`). `.env` is git-ignored.
- Least-privilege service account; only port 80 is public, and SSH goes through Identity-Aware Proxy.
- Students are identified only by an anonymous ID (e.g. `student_001`).

## Running the backend locally

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
gcloud auth application-default login
uvicorn app.main:app --reload --port 8000
```

Interactive API docs: http://127.0.0.1:8000/docs
