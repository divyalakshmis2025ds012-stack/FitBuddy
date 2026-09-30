"""
routes.py
Core operational layer: bridges the HTML templates, the Gemini AI functions,
and the SQLite database.

Page routes (used by the HTML forms):
    GET  /                -> index.html (input form)
    POST /generate-workout-> generates plan + tip, saves them, renders result.html
    POST /submit-feedback -> revises plan based on feedback, renders result.html
    GET  /view-all-users  -> admin dashboard, renders all_users.html

JSON API routes (handy for testing in /docs):
    POST /generate-workout/gemini
    GET  /nutrition-tip
    POST /generate-plan
    POST /update-plan/{user_id}
"""

import os
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas import UserInput, FeedbackRequest, WorkoutRequest
from app.database import (
    save_user,
    save_plan,
    update_plan,
    get_original_plan,
    get_user,
    get_all_users_with_plans,
)
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "app", "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# ---------------------------------------------------------------------------
# 1. Home route
# ---------------------------------------------------------------------------

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------------------------------------------------------------------
# 2. Plan generator (form submission from index.html)
# ---------------------------------------------------------------------------

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    save_user(
        user_id=user_id, name=username, age=age, weight=weight,
        goal=goal, intensity=intensity,
    )

    plan = generate_workout_gemini({"goal": goal, "intensity": intensity})
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    save_plan(user_id, plan)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": plan,
            "nutrition_tip": nutrition_tip,
        },
    )


# ---------------------------------------------------------------------------
# 3. Feedback -> revised plan (form submission from result.html)
# ---------------------------------------------------------------------------

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...),
):
    user = get_user(user_id)
    original = get_original_plan(user_id)

    if not original:
        raise HTTPException(status_code=404, detail="Original plan not found for this user.")

    updated = update_workout_plan(original, feedback)
    update_plan(user_id, updated)

    nutrition_tip = generate_nutrition_tip_with_flash(user.goal if user else "general fitness")

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "username": user.name if user else "",
            "user_id": user_id,
            "age": user.age if user else "",
            "weight": user.weight if user else "",
            "goal": user.goal if user else "",
            "intensity": user.intensity if user else "",
            "workout_plan": updated,
            "nutrition_tip": nutrition_tip,
            "feedback_submitted": True,
        },
    )


# ---------------------------------------------------------------------------
# 4. Admin dashboard
# ---------------------------------------------------------------------------

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    user_data = get_all_users_with_plans()
    return templates.TemplateResponse(
        "all_users.html", {"request": request, "users": user_data}
    )


# ---------------------------------------------------------------------------
# JSON API routes (test these directly at /docs)
# ---------------------------------------------------------------------------

@router.post("/generate-workout/gemini")
async def generate_gemini_workout(request: WorkoutRequest):
    try:
        result = generate_workout_gemini(
            {"goal": request.goal, "intensity": request.intensity}
        )
        return {"model": "gemini-pro", "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nutrition-tip")
def get_flash_tip(goal: str):
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}


@router.post("/generate-plan")
def generate_plan(user_data: UserInput):
    try:
        save_user(
            user_id=user_data.user_id,
            name=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity,
        )
        plan = generate_workout_gemini(
            {"goal": user_data.goal, "intensity": user_data.intensity}
        )
        save_plan(user_data.user_id, plan)
        return {
            "message": "Workout plan generated and saved successfully!",
            "workout_plan": plan,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


@router.post("/update-plan/{user_id}", response_model=dict)
def update_user_plan(user_id: int, data: FeedbackRequest):
    original = get_original_plan(user_id)
    if not original:
        return {"error": "Original plan not found for this user."}
    updated = update_workout_plan(original, data.feedback)
    update_plan(user_id, updated)
    return {"updated_plan": updated}
