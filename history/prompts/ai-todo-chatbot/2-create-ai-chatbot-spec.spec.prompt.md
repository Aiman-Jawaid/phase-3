---
id: 2
title: "Create AI Todo Chatbot specification"
stage: "spec"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "ai-todo-chatbot"
branch: "2-ai-todo-chatbot"
user: "user"
command: "/sp.specify"
labels: ["spec", "ai-chatbot", "todo", "features"]
links:
  spec: "specs/2-ai-todo-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/2-ai-todo-chatbot/spec.md"
  - "specs/2-ai-todo-chatbot/checklists/requirements.md"
tests_yaml: []
---

# Prompt History Record

## Prompt Text

```
You are writing a formal SPECIFICATION for Phase III of a Full-Stack Todo Application.

This specification must describe WHAT to build, not HOW to code it.

The system already includes:
- Phase I: Console Todo App
- Phase II: Full-Stack Web App (Next.js + FastAPI + Neon PostgreSQL)
- Existing Task CRUD APIs
- JWT Authentication via Better Auth

Phase III must extend the SAME project by adding an AI-powered Todo Chatbot.

────────────────────────────────────────
📌 FEATURE NAME
────────────────────────────────────────
AI Todo Chatbot (Phase III)

────────────────────────────────────────
🎯 PURPOSE
────────────────────────────────────────
Allow authenticated users to manage their todo tasks using natural language through an AI chatbot interface.

The chatbot must understand user intent and perform task operations such as adding, listing, updating, completing, and deleting tasks.

────────────────────────────────────────
🧠 AI FRAMEWORK REQUIREMENTS
────────────────────────────────────────
- Use OpenAI Agents SDK architecture:
  - Agent
  - Runner
  - Tool invocation
- Replace Gemini/OpenAI models with **Cohere LLM**
- Use Cohere API for all LLM completions
- Agent logic must remain model-agnostic
- The Agent must NEVER access the database directly
- All data operations must be performed via MCP tools

────────────────────────────────────────
🏗️ ARCHITECTURE OVERVIEW
────────────────────────────────────────
- Backend: FastAPI (existing backend)
- AI Logic: OpenAI Agents SDK (architecture only)
- LLM Provider: Cohere
- Tools Layer: MCP (Model Context Protocol)
- Database: Neon Serverless PostgreSQL
- ORM: SQLModel
- Auth: Better Auth (JWT)

The chatbot must be fully integrated into the existing backend.
No separate backend or microservice is allowed.

────────────────────────────────────────
🧩 MCP TOOLS (REQUIRED)
────────────────────────────────────────
The MCP server must expose the following stateless tools:

1. add_task
2. list_tasks
3. update_task
4. complete_task
5. delete_task

Rules:
- Tools must accept user_id internally from authenticated context
- Tools must enforce task ownership
- Tools must return structured JSON
- Tools must not store any state in memory

────────────────────────────────────────
🗄️ DATABASE REQUIREMENTS
────────────────────────────────────────
The chatbot must persist conversation history.

Required models:
- Conversation
  - id
  - user_id
  - created_at
  - updated_at

- Message
  - id
  - conversation_id
  - user_id
  - role (user | assistant)
  - content
  - created_at

Tasks must reuse the existing Task table from Phase II.

────────────────────────────────────────
🌐 CHAT API ENDPOINT
────────────────────────────────────────
Endpoint:
POST /api/chat

Request:
- conversation_id (optional)
- message (string, required)

Response:
- conversation_id
- response (assistant message)
- tool_calls (array of MCP tools used, if any)

The server must remain stateless.
Conversation state must be reconstructed from the database on every request.

────────────────────────────────────────
🧠 AGENT BEHAVIOR SPECIFICATION
────────────────────────────────────────
The AI Agent must:

- Detect intent from natural language
- Map intent to MCP tools
- Confirm actions politely
- Ask clarification questions when input is ambiguous
- Handle errors gracefully (task not found, invalid input)
- Never hallucinate task IDs
- Never act on tasks belonging to another user

Natural language examples:
- "Add a task to buy groceries" → add_task
- "Show my pending tasks" → list_tasks(status=pending)
- "Mark task 3 as done" → complete_task
- "Delete the meeting task" → list_tasks + delete_task
- "Change task 1 title to call mom" → update_task

────────────────────────────────────────
🎨 FRONTEND INTEGRATION (UI SPEC)
────────────────────────────────────────
- Add a chatbot icon/button in the existing dashboard UI
- The icon should be minimal and professional
- Clicking the icon opens a chat panel or modal
- Chat UI should resemble a clean SaaS assistant
- Messages should display user and assistant roles clearly
- Chat UI must work alongside existing task UI

No redesign of the main dashboard layout is allowed.

────────────────────────────────────────
🔐 AUTH & SECURITY RULES
────────────────────────────────────────
- Chat endpoint must require valid JWT
- User identity must be derived from JWT only
- user_id must NOT be accepted from frontend input
- All task access must be scoped to authenticated user

────────────────────────────────────────
🚫 OUT OF SCOPE
────────────────────────────────────────
- Voice input
- Multi-agent collaboration
- External integrations
- Background jobs
- Frontend redesign

────────────────────────────────────────
✅ ACCEPTANCE CRITERIA
────────────────────────────────────────
- Chatbot can manage todos using natural language
- Uses Cohere as LLM provider
- Uses Agents SDK + MCP architecture
- Conversation resumes after server restart
- Fully integrated into existing backend
- Ready for hackathon evaluation
```

## Response Text

Created a comprehensive specification for the AI Todo Chatbot feature (Phase III) that extends the existing full-stack todo application. The specification includes user scenarios, functional requirements, key entities, and success criteria focused on natural language task management using Cohere AI and MCP tools architecture.

## Outcome

Successfully created spec file at specs/2-ai-todo-chatbot/spec.md with all required sections including user scenarios, functional requirements, and success criteria. Also created a quality checklist at specs/2-ai-todo-chatbot/checklists/requirements.md to validate the specification completeness.