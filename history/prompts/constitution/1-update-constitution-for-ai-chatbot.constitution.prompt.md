---
id: 1
title: "Update constitution for AI chatbot integration"
stage: "constitution"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "ai-chatbot", "integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Prompt History Record

## Prompt Text

```
You are an expert full-stack AI systems architect.

Your task is to extend an existing Full-Stack Todo Web Application by integrating an AI-powered Todo Chatbot (Phase III) into the same backend codebase.

This project already has:
- A FastAPI backend
- SQLModel ORM
- Neon Serverless PostgreSQL database
- JWT-based authentication via Better Auth
- Existing Task CRUD APIs
- A Next.js frontend

You MUST integrate the AI chatbot INTO this existing backend.
DO NOT create a separate backend.
DO NOT redesign existing task APIs.
DO NOT break Phase I or Phase II functionality.

────────────────────────────────────────
🎯 OBJECTIVE
────────────────────────────────────────

Integrate an AI Todo Chatbot that allows authenticated users to manage their todos using natural language.

The chatbot must be able to:
- Add tasks
- List tasks (all / pending / completed)
- Update tasks
- Complete tasks
- Delete tasks
- Understand the currently logged-in user
- Explain which user is logged in (email / user_id)
- Confirm actions in a friendly way
- Handle errors gracefully

The chatbot must persist conversation history in the database but keep the server stateless.

────────────────────────────────────────
🧠 AI & MODEL REQUIREMENTS
────────────────────────────────────────

- Use **Cohere API** as the LLM provider
- Use **OpenAI Agents SDK architecture concepts**
  (Agent, Runner, Tools, Tool Invocation)
- Even though the SDK is OpenAI-based, the actual LLM calls must be routed through Cohere using its API key
- Agents logic must remain model-agnostic
- All reasoning must happen inside the Agent
- The Agent MUST call MCP tools to interact with tasks
- The Agent MUST NOT directly access the database

Environment Variables:
- COHERE_API_KEY
- DATABASE_URL
- BETTER_AUTH_SECRET

────────────────────────────────────────
🏗️ ARCHITECTURE RULES
────────────────────────────────────────

- Use a **stateless FastAPI server**
- Every chat request must:
  1. Receive a user message
  2. Load conversation history from the database
  3. Append the new user message
  4. Run the AI Agent
  5. Let the Agent invoke MCP tools
  6. Store the assistant response
  7. Return the response to the frontend

The server must NOT store memory in RAM.
All state must live in the database.

────────────────────────────────────────
🧩 MCP (MODEL CONTEXT PROTOCOL) TOOLS
────────────────────────────────────────

Implement an MCP Server inside the same backend exposing the following tools:

- add_task
- list_tasks
- update_task
- complete_task
- delete_task

Rules:
- MCP tools must be stateless
- MCP tools must enforce user ownership
- MCP tools must ONLY use existing Task tables
- MCP tools must return structured JSON

────────────────────────────────────────
🗄️ DATABASE MODELS (REQUIRED)
────────────────────────────────────────

Use SQLModel and Neon PostgreSQL.

Models:
1. Task
   - id
   - user_id
   - title
   - description
   - completed
   - created_at
   - updated_at

2. Conversation
   - id
   - user_id
   - created_at
   - updated_at

3. Message
   - id
   - conversation_id
   - user_id
   - role ("user" | "assistant")
   - content
   - created_at

────────────────────────────────────────
🔐 AUTHENTICATION & SECURITY
────────────────────────────────────────

- All chat endpoints must require a valid JWT
- User identity must be extracted from the JWT
- user_id must NEVER be trusted from frontend input
- The chatbot must only access tasks belonging to the authenticated user
- Return 401 for unauthenticated requests

────────────────────────────────────────
🌐 API ENDPOINT
────────────────────────────────────────

Implement the following endpoint:

POST /api/chat

Request:
- conversation_id (optional)
- message (string, required)

Response:
- conversation_id
- response (assistant message)
- tool_calls (if any)

────────────────────────────────────────
🧠 AGENT BEHAVIOR RULES
────────────────────────────────────────

- When user says "add", "remember", "create" → use add_task
- When user says "show", "list", "what's pending" → use list_tasks
- When user says "done", "complete", "finished" → use complete_task
- When user says "delete", "remove" → use delete_task
- When user says "change", "update", "rename" → use update_task
- If task is ambiguous, ask a clarification question
- Always confirm actions politely
- Never hallucinate task IDs
- If task not found, explain gracefully

────────────────────────────────────────
🧪 QUALITY & HACKATHON STANDARDS
────────────────────────────────────────

- Code must be clean and modular
- Follow existing backend folder structure
- Do NOT introduce unnecessary abstractions
- Favor clarity over cleverness
- The system must survive server restarts
- The chatbot must resume conversations correctly
- Output must be production-quality

────────────────────────────────────────
🚫 STRICTLY DO NOT
────────────────────────────────────────

- Do NOT create a new backend
- Do NOT remove existing endpoints
- Do NOT store memory in global variables
- Do NOT hardcode secrets
- Do NOT bypass MCP tools
- Do NOT redesign frontend UI

────────────────────────────────────────
✅ SUCCESS CRITERIA
────────────────────────────────────────

- AI chatbot fully integrated into existing backend
- Uses Cohere as LLM
- Uses Agents + MCP architecture
- Can manage todos via natural language
- Stateless, scalable, and secure
- Ready for hackathon judging
```

## Response Text

Updated the project constitution to include new principles for AI chatbot integration, MCP tool governance, and stateless architecture requirements. The constitution now includes guidelines for Cohere API usage, MCP tools implementation, and proper separation of concerns between the AI agent and database access.

## Outcome

The constitution has been successfully updated from version 1.0.0 to 1.1.0 to incorporate the new AI chatbot integration requirements while maintaining all existing principles and adding new ones specific to the AI functionality.