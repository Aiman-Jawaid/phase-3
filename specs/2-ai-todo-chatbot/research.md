# Research Document: AI Todo Chatbot Implementation

## Research Task 1: Cohere API Integration

### Decision: Cohere Client Wrapper Implementation
**Rationale**: The Cohere API needs to be adapted to work with OpenAI Agents SDK patterns. We'll create a wrapper that translates between Cohere's API format and the expected format for the agent system. This maintains model-agnostic agent logic while using Cohere as the LLM provider.

**Implementation Approach**:
- Use Cohere's Python SDK to create a client wrapper
- Implement a function that takes a conversation history and returns a response
- Format the response to be compatible with the agent orchestration system
- Handle tool calling functionality through Cohere's function calling capabilities

**Alternatives Considered**:
- Directly using OpenAI API with Cohere: Would violate the requirement to use Cohere API
- Building a custom agent system: Would be over-engineering compared to adapting existing patterns

## Research Task 2: Backend Project Structure

### Decision: AI Module Organization
**Rationale**: The existing backend structure should be extended with a dedicated AI module to avoid disrupting existing functionality. Based on typical FastAPI project structures, we'll create an ai/ directory within the backend.

**Implementation Approach**:
- Create backend/ai/ directory
- Within ai/, create subdirectories for: agents/, mcp_tools/, models/, and services/
- Place the main agent orchestration in ai/agents/
- Place MCP tools in ai/mcp_tools/
- Place new conversation/message models in ai/models/
- Place conversation management services in ai/services/

**Alternatives Considered**:
- Modifying existing API routes: Could disrupt existing functionality
- Creating a separate service: Violates the requirement to integrate into existing backend

## Research Task 3: Database Schema and Task Model

### Decision: Database Model Integration
**Rationale**: Need to examine the existing backend structure to understand the Task model and database connections. Based on the project description, we know it uses SQLModel with Neon PostgreSQL.

**Expected Structure**:
- The existing Task model likely has fields: id, user_id, title, description, completed, created_at, updated_at
- Database connection is managed through SQLModel's create_engine and session management
- Authentication adds user_id to requests which can be passed to tools

**Implementation Approach**:
- Locate the existing Task model in the backend codebase
- Understand the current database session management
- Create Conversation and Message models following the same patterns
- Implement MCP tools that connect to the same database session

## Research Task 4: Frontend Integration Approach

### Decision: Chat UI Integration
**Rationale**: The chat UI needs to be added to the existing dashboard without redesigning the main layout. A floating button or sidebar integration would work well with minimal disruption.

**Implementation Approach**:
- Add a floating chatbot icon button in the bottom-right corner of the dashboard
- Clicking the icon opens a chat panel that slides in from the right
- Panel contains message history and input field
- Panel can be minimized/closed without losing conversation context
- Conversation ID is stored in frontend state or sessionStorage

**Alternatives Considered**:
- Redesigning the entire dashboard: Violates the requirement not to redesign the main layout
- Modal approach: Less convenient for extended conversations
- Dedicated chat page: Would require navigation away from dashboard

## Additional Research: OpenAI Agents SDK with Cohere

### Decision: Agent Architecture Pattern
**Rationale**: While the requirement mentions "OpenAI Agents SDK architecture concepts", we need to implement the pattern without using the actual OpenAI SDK. Instead, we'll implement the core concepts (Agent, Runner, Tool invocation) with Cohere as the underlying LLM.

**Implementation Approach**:
- Create an Agent class that manages the conversation state
- Create a Runner that orchestrates the agent's interaction with tools
- Implement Tool classes for each MCP function (add_task, list_tasks, etc.)
- Use Cohere's language model to determine which tools to call based on user input

**Alternatives Considered**:
- Using LangChain or similar frameworks: Might add unnecessary complexity
- Custom-built simple parser: Might lack sophistication for natural language understanding

## Security and Authentication Research

### Decision: JWT Integration with MCP Tools
**Rationale**: The system must extract user identity from JWT tokens and ensure all operations are scoped to the authenticated user. This requires passing the user context to MCP tools.

**Implementation Approach**:
- Extract user_id from JWT token in the /api/chat endpoint
- Pass user_id as a parameter to all MCP tools
- Each MCP tool validates that operations are performed only on resources belonging to the authenticated user
- Implement proper error handling when users try to access resources they don't own

**Alternatives Considered**:
- Passing user context through headers to tools: Less secure and more complex
- Storing user context globally: Violates the stateless architecture requirement