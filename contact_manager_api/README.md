# Contact Manager API (FastAPI + SQLModel + JWT)

Full CRUD for contacts, per-user access control via JWT auth, IP logging middleware, and CORS.

## Quickstart

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

# Optionally set env vars
# (defaults are fine for local use)
# set / export SECRET_KEY="change-me"
# set / export ACCESS_TOKEN_EXPIRE_MINUTES=60

uvicorn app.main:app --reload
