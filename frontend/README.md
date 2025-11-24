# CareConnect Frontend

Vue 3 single-page application that consumes the FastAPI backend and surfaces all CRUD workflows for the caregivers platform. Refer to the project-level `README.md` for a complete overview.

## Quick start

```powershell
cd frontend
npm install
npm run dev
```

The app expects the API base URL from `VITE_API_BASE_URL`. Copy `.env.example` to `.env` if you need to point to a custom deployment.

### Additional scripts

- `npm run build` – production build
- `npm run lint` – ESLint + TypeScript checks
