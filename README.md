# CareConnect – Online Caregivers Platform

CareConnect is a full-stack web application built with **FastAPI** and **Vue 3** that connects families with trustworthy caregivers. The project demonstrates database design, RESTful APIs, and CRUD flows across the core entities the course brief describes.

## Features

- Caregiver registration with profile management, hourly rates, and biography.
- Family member onboarding capturing caregiving needs, house rules, and contact details.
- Searchable caregiver directory with filters by caregiving type, city, and hourly rate.
- Job board for detailed caregiving announcements, including preferred schedules and requirements.
- Application workflow where caregivers apply to job posts and families review or triage submissions.
- Appointment scheduling with confirmation/decline handling and visibility for both parties.
- Internal messaging between caregivers and families once a match looks promising.

## Project Structure

```
backend/             FastAPI project (SQLite, SQLAlchemy ORM)
frontend/            Vue 3 + Vite SPA consuming the API
```

## Prerequisites

- Python 3.10+
- Node.js 18+

---

## Backend (FastAPI)

```powershell
# From the project root
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# launch the API (hot reload)
uvicorn app.main:app --reload
```

The API runs on `http://127.0.0.1:8000` by default. All tables are created automatically in `caregivers.db` the first time the server starts.

### Key Endpoints

| Resource       | Endpoint                  | Notes                                  |
| -------------- | ------------------------- | -------------------------------------- |
| Caregivers     | `/caregivers`             | CRUD, filter by type/city/rate         |
| Families       | `/families`               | CRUD                                   |
| Job posts      | `/job-posts`              | CRUD, filter by type/city              |
| Applications   | `/applications`          | CRUD, scope by job or caregiver        |
| Appointments   | `/appointments`          | CRUD, status updates (pending → final) |
| Messages       | `/messages`              | Conversation threads                    |

All payloads/response shapes are defined in `app/schemas.py`.

---

## Frontend (Vue 3 + Vite)

```powershell
# From the project root
cd frontend
npm install

# Create a local .env file (optional)
Copy-Item .env.example .env -ErrorAction SilentlyContinue
# or create a new file containing:
# VITE_API_BASE_URL=http://127.0.0.1:8000

npm run dev
```

The SPA is available on `http://127.0.0.1:5173` and expects the API base URL from `VITE_API_BASE_URL`. If the file is missing, it defaults to `http://127.0.0.1:8000`.

### Main Screens

- **Home** – quick search with highlights for caregivers and job posts.
- **Caregivers** – register/edit/delete caregiver profiles.
- **Families** – manage family profiles and caregiving requirements.
- **Job Board** – publish detailed caregiving opportunities and manage applications.
- **Appointments** – schedule and confirm caregiving sessions.
- **Messages** – exchange direct messages between families and caregivers.

Each screen exercises the corresponding CRUD operations exposed by the API.

---

## Deployment Notes

- FastAPI can be deployed to platforms such as [PythonAnywhere](https://www.pythonanywhere.com/), Azure App Service, Render, or any container-friendly PaaS.
- The Vite frontend builds into static assets (`npm run build`) deployable to Netlify, Vercel, GitHub Pages, or any static host. Point it at the deployed API via `VITE_API_BASE_URL`.

## Testing Checklist

- Create caregivers and families, then verify search filters.
- Post job announcements, submit applications, and accept/decline them.
- Create appointments and confirm/decline workflow.
- Send messages between the selected family and caregiver; ensure conversation history loads correctly.

Feel free to extend the seed data, add authentication, or integrate map-based city selection to further enhance the platform.
