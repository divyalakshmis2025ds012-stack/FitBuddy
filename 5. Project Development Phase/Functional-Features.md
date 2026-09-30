# Functional Features

Source code is in the `Source Code` folder.

| Feature | Route | Implemented in |
|---|---|---|
| Home / input form | `GET /` | `routes.py`, `templates/index.html` |
| Generate 7-day plan + nutrition tip (form) | `POST /generate-workout` | `routes.py`, `gemini_generator.py`, `gemini_flash_generator.py` |
| Submit feedback, revised plan (form) | `POST /submit-feedback` | `routes.py`, `updated_plan.py` |
| Admin dashboard | `GET /view-all-users` | `routes.py`, `templates/all_users.html` |
| JSON: workout plan | `POST /generate-workout/gemini` | `routes.py` |
| JSON: nutrition tip | `GET /nutrition-tip?goal=...` | `routes.py` |
| JSON: generate and save plan | `POST /generate-plan` | `routes.py`, `database.py` |
| JSON: update plan | `POST /update-plan/{user_id}` | `routes.py`, `updated_plan.py` |

## Run
```bash
cd "Source Code"
python -m venv fitbuddy-env
source fitbuddy-env/bin/activate        # Windows: fitbuddy-env\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                    # add your GOOGLE_API_KEY
uvicorn app.main:app --reload
```
