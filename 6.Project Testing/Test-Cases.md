# Test Cases

Fill the **Actual result / Status** columns after running each test.

| ID | Test | Steps | Expected result | Actual result / Status |
|---|---|---|---|---|
| TC-1 | Home page loads | Open `http://127.0.0.1:8000/` | Input form is shown | |
| TC-2 | Generate plan (form) | Fill all fields, submit | Result page shows a 7-day plan and a nutrition tip | |
| TC-3 | Missing form field | Submit with a field empty | Request rejected (validation error) | |
| TC-4 | Feedback revision | On result page, submit feedback | Updated plan is shown | |
| TC-5 | Feedback with no saved plan | `POST /update-plan/{id}` for an unknown ID | Response says original plan not found | |
| TC-6 | Admin dashboard | Open `/view-all-users` | Table of users and plans | |
| TC-7 | Swagger UI | Open `/docs` | All JSON routes listed and executable | |
| TC-8 | Nutrition tip API | `GET /nutrition-tip?goal=weight loss` | JSON with `goal` and `nutrition_tip` | |
| TC-9 | Missing API key / unavailable model | Run without a valid key or model name | Error text is returned instead of a crash | |
