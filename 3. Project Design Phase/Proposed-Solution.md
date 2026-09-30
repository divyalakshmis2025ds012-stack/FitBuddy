# Proposed Solution

FitBuddy takes the user's goal and intensity, builds a prompt, and asks Gemini to act as a fitness trainer and return a structured 7-day plan. A second, lighter Gemini model returns a nutrition tip. Both results are shown on a result page. The plan is stored in SQLite; if the user sends feedback, the stored plan and the feedback are sent to Gemini again to produce a revised plan.

## Why two models
- **Gemini 1.5 Pro** - follows the structured Day 1-7 format reliably (plan and revision)
- **Gemini 1.5 Flash** - cheap and fast for a one-line tip

## Data model
- `users`: id, name, age, weight, goal, intensity, schedule (default 7)
- `plans`: id, user_id (FK to users), original_plan, updated_plan
