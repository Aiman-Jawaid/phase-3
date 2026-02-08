<!-- SYNC IMPACT REPORT -->
<!-- Version change: 1.0.0 → 1.1.0 -->
<!-- Modified principles: Full-Stack Specification Adherence, API Contract Compliance -->
<!-- Added sections: AI-Powered Chatbot Integration, MCP Tool Governance, Stateless Architecture Requirement -->
<!-- Templates requiring updates: ✅ Updated /specs/features/chatbot.md, ✅ Updated /specs/mcp-tools.md -->
<!-- Follow-up TODOs: None -->

# Todo Full-Stack Web Application Constitution

## Core Principles

### Full-Stack Specification Adherence
All implementations must strictly follow the specifications defined in the /specs/ directory. Frontend components must align with UI specs, backend APIs must conform to REST endpoint specs, and database models must match schema definitions. No implementation should deviate from the documented specs without explicit updates to the corresponding spec files. This includes the new AI chatbot features and MCP tool specifications.

### Authentication-First Security
Security is paramount - every API endpoint must validate JWT tokens before processing requests. User data isolation is non-negotiable: users can only access and modify their own tasks. All authentication flows must utilize Better Auth with proper JWT handling. No endpoint should be accessible without proper authentication unless explicitly defined as public. This applies to the new chatbot endpoints as well.

### Test-First Implementation (NON-NEGOTIABLE)
TDD is mandatory: Tests must be written before implementation code. Unit tests for individual functions, integration tests for API endpoints, and end-to-end tests for critical user flows must be implemented. All tests must pass before merging. The Red-Green-Refactor cycle is strictly enforced for all feature development. This includes testing for the AI chatbot functionality and MCP tools.

### Type-Safe Development
All code must be strongly typed using TypeScript for frontend and proper type hints in Python for backend. API contracts must be validated using Pydantic models. No implicit any types in TypeScript, and all API responses must have proper typing. Type checking must pass before code can be merged.

### Minimalist Feature Development
Features should be implemented with the minimal viable approach that satisfies requirements. Avoid over-engineering or adding speculative functionality. Each feature must have clear business value and be testable. Follow YAGNI (You Aren't Gonna Need It) principles and prefer simple solutions over complex abstractions.

### API Contract Compliance
All backend endpoints must follow RESTful conventions and properly implement CRUD operations for tasks. Request/response schemas must match the defined API specifications. Proper HTTP status codes must be returned for all responses. Filtering, sorting, and pagination must be implemented where specified. This extends to the new /api/chat endpoint and MCP tool endpoints.

### AI-Powered Chatbot Integration
The AI chatbot must be integrated into the existing backend using Cohere API as the LLM provider. The chatbot must follow OpenAI Agents SDK architecture concepts (Agent, Runner, Tools, Tool Invocation) while routing actual LLM calls through Cohere. The Agent must call MCP tools to interact with tasks and must NOT directly access the database. The system must handle natural language processing for task management (add, list, update, complete, delete) while maintaining contextual awareness of the authenticated user.

### MCP Tool Governance
MCP (Model Context Protocol) tools must be implemented as stateless services within the backend. These tools (add_task, list_tasks, update_task, complete_task, delete_task) must enforce user ownership, only use existing Task tables, and return structured JSON. MCP tools must be the sole pathway for the AI agent to interact with task data, ensuring proper security boundaries.

### Stateless Architecture Requirement
The FastAPI server must remain stateless with all conversation history persisted in the database. Every chat request must load conversation history from the database, append the new user message, run the AI Agent, store the assistant response, and return the response to the frontend. No memory should be stored in RAM or global variables - all state must live in the database to ensure scalability and server restart resilience.

## Security Requirements
All data transmission must use HTTPS. JWT tokens must be properly secured and have appropriate expiration times. SQL injection prevention through parameterized queries is mandatory. Input validation must be implemented at all API boundaries. Sensitive data should never be exposed in client-side code or logs. Special attention must be paid to protecting the COHERE_API_KEY and ensuring that the chatbot only accesses tasks belonging to the authenticated user.

## Development Workflow
All development must follow the spec-driven approach: read relevant specs before implementing (@specs/features/task-crud.md, @specs/features/authentication.md, @specs/features/chatbot.md, etc.). Use Next.js App Router patterns for frontend, FastAPI conventions for backend, and SQLModel for database interactions. All API calls must be made through the centralized API client at /lib/api.ts. Code reviews must verify compliance with all constitution principles. New development must also follow the MCP tool specifications and AI integration guidelines.

## Governance
This constitution governs all development activities for the Todo Full-Stack Web Application. All team members must comply with these principles. Amendments require explicit documentation and team approval. Code reviews must verify compliance with all principles before merging. Each pull request must demonstrate adherence to these guidelines. The constitution version must be updated according to semantic versioning: MAJOR for backward incompatible changes, MINOR for new principles or features, PATCH for clarifications.

**Version**: 1.1.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-20