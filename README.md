# FitBuddy – AI Fitness Plan Generator

FastAPI + Google Gemini (1.5 Pro & Flash) app that generates personalized 7-day
workout plans and nutrition tips, with feedback-based plan revision and an
admin dashboard.

## Folder structure

```
fitbuddy/
├── requirements.txt
├── .env.example
├── app/
│   ├── main.py                    # FastAPI entry point
│   ├── database.py                # SQLAlchemy models + DB helpers
│   ├── schemas.py                 # Pydantic request models
│   ├── gemini_generator.py        # Gemini 1.5 Pro – workout plan
│   ├── gemini_flash_generator.py  # Gemini Flash – nutrition tip
│   ├── updated_plan.py            # Gemini 1.5 Pro – feedback-based revision
│   ├── routes.py                  # All route handlers
│   ├── templates/
│   │   ├── index.html
│   │   ├── result.html
│   │   └── all_users.html
│   └── static/
│       └── images/
└── fitbuddy.db                    # auto-created on first run
```

## Setup (VS Code terminal)

```bash
# 1. Create and activate a virtual environment
python -m venv fitbuddy-env
fitbuddy-env\Scripts\activate        # Windows
source fitbuddy-env/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Gemini API key
cp .env.example .env
# then edit .env and paste your real key:
# GOOGLE_API_KEY=your_actual_key_here

# 4. Run the server
uvicorn app.main:app --reload
```

Get a free Gemini API key at https://aistudio.google.com/app/apikey

## Using it

- `http://127.0.0.1:8000/` – input form → generates your 7-day plan + tip
- `http://127.0.0.1:8000/view-all-users` – admin table of all users/plans
- `http://127.0.0.1:8000/docs` – interactive Swagger UI to test the JSON API routes directly

## Notes

- `gemini-1.5-pro` is used for the workout plan and feedback revisions
  (needs to follow structured formatting reliably).
- `gemini-1.5-flash` is used for the nutrition tip (cheap/fast, one-liner output).
- If either model name is deprecated on your API key's tier, swap it for
  whatever current Gemini model you have access to in `gemini_generator.py`,
  `gemini_flash_generator.py`, and `updated_plan.py`.
