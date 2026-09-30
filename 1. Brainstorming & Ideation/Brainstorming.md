# Brainstorming & Ideation

## Idea
A web app where the user fills a short form (name, ID, age, weight, goal, intensity) and receives an AI-generated 7-day workout plan with a nutrition tip.

## Features considered
- Personalised 7-day workout plan (Gemini 1.5 Pro)
- One-line nutrition / recovery tip (Gemini 1.5 Flash - fast and low cost)
- Feedback-based plan revision
- Storage of users and plans in a database
- Admin page to view all users and plans
- JSON API with Swagger UI for direct testing

## Selected approach
FastAPI backend + Jinja2 HTML pages + SQLite (via SQLAlchemy) + Google Gemini API, split into small modules (routes, database, schemas, one file per AI task).
