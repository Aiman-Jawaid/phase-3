---
id: 1
title: "Todo Constitution Update"
stage: constitution
date_iso: "2026-01-09"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "user"
command: "sp.constitution"
labels:
  - "constitution"
  - "todo-app"
  - "hackathon"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml:
  - "none"
---

# Todo Constitution Update

## Outcome
Updated the project constitution to reflect the specific requirements for the Todo Full-Stack Web Application project. The new constitution includes principles for full-stack specification adherence, authentication-first security, test-first implementation, type-safe development, minimalist feature development, and API contract compliance.

## Evaluation
The constitution has been successfully updated with project-specific principles that align with the tech stack (Next.js, FastAPI, SQLModel, Better Auth) and requirements (Task CRUD, JWT authentication, user isolation). All placeholder tokens have been replaced with concrete values, and the document reflects the governance structure for the hackathon project.

## Prompt Text
```
Hackathon II - Todo Full-Stack Web Application

## Project Overview
You are the AI software architect and developer for a full-stack Todo application (Phase II). The project is structured as a monorepo using Spec-Kit + Claude Code. Your goal is to implement all features, backend, frontend, database models, and authentication exactly according to the specs.

## Tech Stack
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI, SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth with JWT
- Spec-Driven: Claude Code + Spec-Kit Plus

## Monorepo Structure
- /.spec-kit/config.yaml - Spec-Kit configuration
- /specs/overview.md - Project overview
- /specs/features/ - Feature specs (task-crud.md, authentication.md)
- /specs/api/ - API endpoint specs (rest-endpoints.md)
- /specs/database/ - Schema (schema.md)
- /specs/ui/ - UI component and page specs
- /frontend/CLAUDE.md - Frontend implementation patterns
- /backend/CLAUDE.md - Backend implementation patterns
- /CLAUDE.md - Root project instructions

## Feature Requirements
1. Task CRUD operations for logged-in users
2. JWT-secured API endpoints
3. User authentication (Sign-up, Sign-in) using Better Auth
4. Responsive frontend with Tailwind CSS
5. RESTful API endpoints
6. Task filtering and sorting
7. Only authenticated users can view/edit their tasks
8. Each endpoint must validate JWT tokens and enforce user ownership

## Workflow Instructions
1. Always read relevant spec before implementing:
   - @specs/features/task-crud.md
   - @specs/features/authentication.md
   - @specs/api/rest-endpoints.md
   - @specs/database/schema.md
   - @specs/ui/components.md
2. Update backend according to FastAPI + SQLModel + JWT conventions.
3. Update frontend using Next.js + Tailwind CSS + API client for requests.
4. Make sure JWT tokens are attached to all API calls.
5. Test features individually, then end-to-end.

## API Behavior
- All endpoints require Authorization: Bearer <JWT token>
- Requests without token → 401 Unauthorized
- Users can only see and modify their own tasks
- Endpoints: GET/POST/PUT/DELETE/PATCH as per spec
- Include filtering and sorting parameters where applicable

## Database Schema
- users (managed by Better Auth): id, email, name, created_at
- tasks: id, user_id, title, description, completed, created_at, updated_at
- indexes: tasks.user_id, tasks.completed

## Frontend Guidelines
- Use server components by default
- Client components for interactivity
- API client at /lib/api.ts for all backend calls
- Tailwind CSS for styling (no inline CSS)
- Reusable components in /components
- Pages in /app

## Backend Guidelines
- FastAPI app entry point: main.py
- Models in models.py
- Routes in routes/
- DB connection in db.py
- Handle errors with HTTPException
- Pydantic models for request/response validation

## Spec Reference
Always use @specs/[path].md for implementation guidance.
```

## Response Text
Updated the constitution file with project-specific principles for the Todo Full-Stack Web Application, including specification adherence, security-first approach, test-first development, type safety, minimalist development, and API compliance. The constitution now properly governs development activities for this hackathon project with appropriate governance and versioning.