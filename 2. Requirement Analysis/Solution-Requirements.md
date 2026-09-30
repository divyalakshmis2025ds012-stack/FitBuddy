# Solution Requirements

## Functional requirements
| ID | Requirement |
|---|---|
| FR-1 | User can submit username, user ID, age, weight, goal and intensity from the home page |
| FR-2 | System generates a 7-day workout plan (warm-up, main workout, cooldown per day) |
| FR-3 | System generates a nutrition tip based on the user's goal |
| FR-4 | System stores the user and the original plan in the database |
| FR-5 | User can submit feedback and receive a revised plan |
| FR-6 | Admin can open `/view-all-users` to see all users and plans |
| FR-7 | JSON API routes are available and testable at `/docs` |

## Non-functional requirements
- Internet connection is needed for Gemini API calls
- Gemini API key is kept in `.env` (not in source code)
- Modular code so each feature can be changed independently

## Software requirements
Python, FastAPI, Uvicorn, Jinja2, SQLAlchemy, python-multipart, google-generativeai, python-dotenv, VS Code (or any IDE), web browser.
