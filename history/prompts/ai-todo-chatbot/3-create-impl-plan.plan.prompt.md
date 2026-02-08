---
id: 3
title: "Create implementation plan for AI chatbot"
stage: "plan"
date_iso: "2026-01-20"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "ai-todo-chatbot"
branch: "2-ai-todo-chatbot"
user: "user"
command: "/sp.plan"
labels: ["plan", "ai-chatbot", "implementation", "architecture"]
links:
  spec: "specs/2-ai-todo-chatbot/spec.md"
  plan: "specs/2-ai-todo-chatbot/plan.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/2-ai-todo-chatbot/plan.md"
  - "specs/2-ai-todo-chatbot/research.md"
  - "specs/2-ai-todo-chatbot/data-model.md"
  - "specs/2-ai-todo-chatbot/contracts/chat-api.yaml"
  - "specs/2-ai-todo-chatbot/quickstart.md"
  - ".specify/memory/claude-context.md"
tests_yaml: []
---

# Prompt History Record

## Prompt Text

```
You are writing an IMPLEMENTATION PLAN based strictly on the previously approved sp.specify.

This plan must describe HOW the system will be built, step by step.
Do not repeat the specification text.
Do not write code.
Focus on order of work, components, and integration steps.

────────────────────────────────────────
🧭 OVERALL GOAL
────────────────────────────────────────
Integrate an AI-powered Todo Chatbot into the existing full-stack application using:
- FastAPI backend
- OpenAI Agents SDK architecture
- Cohere as the LLM provider
- MCP tools for task operations
- Existing authentication and database

The plan must ensure minimal disruption to Phase I & II functionality.

────────────────────────────────────────
🗂️ PHASE 1: BACKEND FOUNDATION
────────────────────────────────────────
1. Create a dedicated AI module inside the existing backend project.
2. Organize folders for:
   - agent definition
   - MCP tools
   - conversation memory handling
   - Cohere client configuration
3. Load Cohere API key securely from environment variables.
4. Ensure this module can be imported without affecting existing APIs.

────────────────────────────────────────
🧠 PHASE 2: COHERE LLM INTEGRATION
────────────────────────────────────────
1. Initialize a Cohere client wrapper compatible with Agents SDK.
2. Adapt the agent runner to use Cohere responses instead of Gemini/OpenAI.
3. Keep agent logic model-agnostic.
4. Validate that prompt → response flow works independently of tools.

────────────────────────────────────────
🧰 PHASE 3: MCP TOOL IMPLEMENTATION
────────────────────────────────────────
1. Implement MCP tools for:
   - add_task
   - list_tasks
   - update_task
   - complete_task
   - delete_task
2. Connect tools to existing Task service / ORM layer.
3. Enforce user ownership using authenticated user context.
4. Ensure tools return structured JSON only.
5. Prevent tools from storing state or memory.

────────────────────────────────────────
🧠 PHASE 4: AGENT ORCHESTRATION
────────────────────────────────────────
1. Define a single AI Agent responsible for task management.
2. Register MCP tools with the agent.
3. Configure the agent to:
   - infer user intent
   - select correct tool(s)
   - request clarification when needed
4. Ensure agent never fabricates task IDs.
5. Validate multi-step tool usage (e.g., list → delete).

────────────────────────────────────────
🗃️ PHASE 5: CONVERSATION MEMORY
────────────────────────────────────────
1. Design database models for:
   - conversations
   - messages
2. Store each user and assistant message persistently.
3. Reconstruct conversation context from database per request.
4. Keep backend stateless across requests.

────────────────────────────────────────
🌐 PHASE 6: CHAT API ENDPOINT
────────────────────────────────────────
1. Create POST /api/chat endpoint.
2. Secure endpoint using existing JWT authentication.
3. Extract user identity from token.
4. Accept user message and optional conversation_id.
5. Invoke agent runner with reconstructed context.
6. Save assistant response and tool calls.
7. Return structured chat response to frontend.

────────────────────────────────────────
🎨 PHASE 7: FRONTEND CHAT UI
────────────────────────────────────────
1. Add chatbot icon/button to existing dashboard.
2. Implement a chat panel or modal UI.
3. Display message bubbles for user and assistant.
4. Handle loading and error states.
5. Connect UI to /api/chat endpoint.
6. Preserve conversation_id in frontend state.

────────────────────────────────────────
🔐 PHASE 8: SECURITY & VALIDATION
────────────────────────────────────────
1. Ensure chat API rejects unauthenticated requests.
2. Confirm users can access only their own tasks.
3. Validate user inputs before sending to agent.
4. Handle edge cases:
   - empty messages
   - invalid task references
   - ambiguous instructions

────────────────────────────────────────
🧪 PHASE 9: TESTING & VERIFICATION
────────────────────────────────────────
1. Test all supported natural language actions.
2. Verify task CRUD via chatbot matches manual UI actions.
3. Restart server and confirm conversation continuity.
4. Ensure no regression in Phase I & II features.

────────────────────────────────────────
🚀 PHASE 10: FINAL REVIEW
────────────────────────────────────────
1. Review architecture against sp.specify.
2. Confirm Cohere is the only LLM used.
3. Verify Agents SDK pattern is clearly implemented.
4. Prepare project for demo and evaluation.

────────────────────────────────────────
📌 DELIVERABLES
────────────────────────────────────────
- AI chatbot fully integrated into existing app
- Cohere-powered agent with MCP tools
- Persistent conversation memory
- Frontend chat UI
- Clean, maintainable architecture
```

## Response Text

Created a comprehensive implementation plan for the AI Todo Chatbot (Phase III) feature. The plan includes technical context, constitution check, research document resolving unknowns, data model definitions, API contracts, and detailed implementation steps. All unknowns from the initial assessment have been researched and resolved, with supporting documentation created for the development team.

## Outcome

Successfully created the implementation plan document (specs/2-ai-todo-chatbot/plan.md) along with supporting artifacts: research.md, data-model.md, contracts/chat-api.yaml, quickstart.md, and claude-context.md. The plan is ready for the development team to begin implementation following the outlined phases and steps.