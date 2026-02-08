---
id: 1
title: "Backend Specification for Todo Application"
stage: "spec"
date_iso: "2026-01-10"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "fastapi-backend"
branch: "1-fastapi-backend"
user: "tanze"
command: "/sp.specify"
labels: ["specification", "backend", "todo-app", "jwt-auth"]
links:
  spec: "specs/1-fastapi-backend/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/1-fastapi-backend/spec.md
  - specs/1-fastapi-backend/checklists/requirements.md
  - history/prompts/general/1-backend-specification.general.prompt.md
tests_yaml: |
  - "Specification completeness check"
  - "Quality checklist validation"
---

# Prompt History Record: Backend Specification for Todo Application

## PROMPT_TEXT

Backend (FastAPI) for Todo Full-Stack Application

────────────────────────
🎯 BACKEND OBJECTIVE
────────────────────────

Build a secure, production-ready FastAPI backend for a multi-user Todo application.
The backend must integrate seamlessly with a Next.js frontend using JWT authentication
issued by Better Auth. All task data must be persisted in Neon Serverless PostgreSQL and
strictly isolated per authenticated user.

────────────────────────
🧱 TECH STACK
────────────────────────

- Framework: FastAPI (Python)
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT verification)
- API Style: REST
- Environment configuration via `.env`

────────────────────────
🔐 AUTHENTICATION & SECURITY
────────────────────────

Authentication model:
- Better Auth runs on the frontend (Next.js)
- Backend does NOT handle signup/login UI
- Backend ONLY verifies JWT tokens

JWT Rules:
- All API routes require Authorization header:
  Authorization: Bearer <JWT_TOKEN>
- JWT must be verified using shared secret
- Secret comes from environment variable:
  BETTER_AUTH_SECRET
- Reject requests with:
  - Missing token → 401 Unauthorized
  - Invalid/expired token → 401 Unauthorized

User Identification:
- Decode JWT payload
- Extract:
  - user_id (primary identifier)
  - email (optional)
- Backend must NEVER trust user_id from request body
- user_id must come ONLY from decoded JWT

────────────────────────
🗄 DATABASE CONFIGURATION
────────────────────────

Database:
- Neon Serverless PostgreSQL
- Connection string from environment variable:
  Neon_db_url

Use SQLModel:
- Engine created once
- Session dependency injected into routes
- Auto-create tables on startup if not exist

────────────────────────
📊 DATABASE SCHEMA
────────────────────────

Table: tasks

Fields:
- id: integer (primary key, auto-increment)
- user_id: string (indexed)
- title: string (required, 1–200 chars)
- description: text (optional)
- completed: boolean (default false)
- created_at: timestamp
- updated_at: timestamp

Indexes:
- user_id
- completed

Each task MUST belong to exactly one user.

────────────────────────
📡 API ENDPOINTS
────────────────────────

Base path: /api

All endpoints:
- Require valid JWT
- Automatically scope data to authenticated user

1. GET /api/tasks
- Return all tasks for logged-in user
- Optional query params:
  - status: all | pending | completed
- Response: array of task objects

2. POST /api/tasks
- Create new task
- Body:
  - title (required)
  - description (optional)
- user_id taken from JWT
- Response: created task object

3. GET /api/tasks/{id}
- Fetch single task
- Only if task belongs to user
- Else → 404 Not Found

4. PUT /api/tasks/{id}
- Update task title/description/completed
- Ownership enforced
- Response: updated task

5. PATCH /api/tasks/{id}/complete
- Toggle completed status
- Ownership enforced

6. DELETE /api/tasks/{id}
- Delete task
- Ownership enforced
- Response: success message

────────────────────────
🧠 BUSINESS RULES
────────────────────────

- Users can only see their own tasks
- Tasks cannot be accessed across users
- Backend must enforce ownership on every query
- No endpoint should accept user_id from frontend
- JWT expiry must be respected

────────────────────────
🗂 PROJECT STRUCTURE
────────────────────────

backend/
├── main.py              # App entry point
├── db.py                # DB engine & session
├── models.py            # SQLModel models
├── auth.py              # JWT verification logic
├── routes/
│   └── tasks.py         # Task CRUD routes
├── schemas.py           # Pydantic request/response models
└── requirements.txt

────────────────────────
⚙ ENVIRONMENT VARIABLES
────────────────────────

Required:
- BETTER_AUTH_SECRET
- Neon_db_url

Optional:
- BETTER_AUTH_URL (for reference/debug)

────────────────────────
🔗 FRONTEND INTEGRATION
────────────────────────

Frontend expectations:
- Frontend sends JWT in Authorization header
- Backend responds with JSON
- CORS enabled for:
  http://localhost:3000

Frontend flow:
- Login → JWT issued by Better Auth
- JWT attached to all API calls
- Backend validates JWT and filters data
- UI updates using returned JSON

────────────────────────
❌ DO NOT
────────────────────────

- Do NOT implement login/signup UI
- Do NOT store passwords
- Do NOT trust user_id from frontend
- Do NOT return tasks of other users

────────────────────────
✅ SUCCESS CRITERIA
────────────────────────

- Backend runs without errors
- All endpoints protected by JWT
- Tasks persist in Neon database
- Each user only sees their own data
- Frontend can fully integrate:
  - Fetch tasks
  - Add task
  - Update task
  - Delete task
  - Toggle completion

## RESPONSE_TEXT

Successfully created a comprehensive feature specification for a secure todo management backend. The specification includes:

1. User scenarios with prioritized user stories covering core functionality:
   - Viewing personal tasks (P1)
   - Creating new tasks (P1)
   - Updating and completing tasks (P2)
   - Deleting tasks (P2)

2. Comprehensive functional requirements (FR-001 to FR-015) covering:
   - JWT authentication and user identification
   - Task CRUD operations with proper access control
   - Data persistence and security requirements
   - API communication protocols

3. Defined key entities (Task and User) with their attributes and relationships

4. Measurable success criteria (SC-001 to SC-007) focusing on:
   - System reliability and availability
   - Authentication effectiveness
   - Data integrity and isolation
   - Frontend integration capabilities

The specification has been refined to remove implementation-specific details, making it technology-agnostic while preserving the essential business requirements. A quality checklist was created and validated, confirming the specification meets all requirements for proceeding to the planning phase.