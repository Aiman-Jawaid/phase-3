# Claude Agent Context for Todo Application

## Current Project Context

### Project Overview
- Full-Stack Todo Application with AI Chatbot (Phase III)
- Backend: FastAPI
- Frontend: Next.js
- Database: Neon Serverless PostgreSQL with SQLModel ORM
- Authentication: Better Auth (JWT)

### AI Chatbot Integration (Current Focus)
- LLM Provider: Cohere API
- Architecture: OpenAI Agents SDK patterns (Agent, Runner, Tool invocation)
- Tools Layer: MCP (Model Context Protocol)
- MCP Tools Implemented:
  - add_task
  - list_tasks
  - update_task
  - complete_task
  - delete_task

### Database Models
- Task (existing from Phase II)
- Conversation (new for chatbot)
- Message (new for chatbot)

### Key Requirements
- Stateless architecture (no server memory storage)
- Conversation history persisted in database
- User data isolation enforced
- JWT authentication required for all endpoints
- Cohere API as the only LLM provider

## Technical Guidelines

### Architecture Patterns
- MCP tools must be stateless and enforce user ownership
- Agent must never directly access database
- All state must be retrieved from database on each request
- Tools must return structured JSON only

### Security Considerations
- JWT tokens must be validated for all requests
- User ID must be derived from JWT, never from frontend input
- MCP tools must verify user ownership of tasks
- Input validation required at all boundaries

### Integration Points
- POST /api/chat endpoint for chat interactions
- Existing Task CRUD APIs remain unchanged
- Better Auth JWT validation integrated with new endpoints