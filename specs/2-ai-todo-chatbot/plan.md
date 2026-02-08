# Implementation Plan: AI Todo Chatbot (Phase III)

**Feature**: AI Todo Chatbot (Phase III)
**Created**: 2026-01-20
**Status**: Draft
**Previous Artifact**: specs/2-ai-todo-chatbot/spec.md

## Technical Context

### System Overview
The AI Todo Chatbot will extend the existing full-stack todo application by integrating an AI-powered interface that allows users to manage tasks using natural language. The system will use Cohere as the LLM provider with OpenAI Agents SDK architecture patterns and MCP tools for database operations.

### Technology Stack
- **Backend Framework**: FastAPI (existing)
- **LLM Provider**: Cohere API
- **AI Architecture**: OpenAI Agents SDK patterns
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (existing)
- **Authentication**: Better Auth (JWT)
- **Frontend Framework**: Next.js (existing)

### Known Constraints
- Must integrate into existing backend without disrupting Phase I & II functionality
- All conversation state must be persisted in database (stateless server)
- MCP tools must be the only pathway for database access by the agent
- Agent must not directly access database
- User data isolation must be maintained

### Dependencies
- Cohere Python SDK
- Existing Task CRUD APIs and models
- Better Auth JWT validation
- SQLModel ORM

### Unknowns/Decisions Needed
None - all unknowns have been resolved through research.

### Integration Points
- New POST /api/chat endpoint connecting to existing JWT auth
- MCP tools connecting to existing Task service/ORM
- Conversation and Message models integrating with existing database schema
- Frontend chat UI component integrating with existing Next.js dashboard

## Constitution Check

### Verification Against Core Principles

#### Full-Stack Specification Adherence
- ✅ Will follow specifications in /specs/ directory
- ✅ Backend APIs will conform to REST endpoint specs
- ✅ Database models will match schema definitions from spec
- ✅ Will include new AI chatbot features and MCP tool specifications

#### Authentication-First Security
- ✅ All chat endpoints will validate JWT tokens before processing requests
- ✅ User data isolation will be maintained: users can only access/modify own tasks
- ✅ Will utilize Better Auth with proper JWT handling
- ✅ Chatbot endpoints will require authentication

#### Test-First Implementation (NON-NEGOTIABLE)
- ✅ Will write tests before implementation code
- ✅ Will include unit tests for AI functions, integration tests for API endpoints
- ✅ Will include end-to-end tests for chatbot user flows
- ✅ Will follow Red-Green-Refactor cycle for all feature development

#### Type-Safe Development
- ✅ Will use strong typing with Python type hints for backend
- ✅ Will validate API contracts using Pydantic models
- ✅ Will avoid implicit any types in any new TypeScript code
- ✅ Will ensure proper typing for all API responses

#### Minimalist Feature Development
- ✅ Will implement with minimal viable approach satisfying requirements
- ✅ Will avoid over-engineering or speculative functionality
- ✅ Each feature will have clear business value and be testable
- ✅ Will follow YAGNI principles and prefer simple solutions

#### API Contract Compliance
- ✅ Will follow RESTful conventions for the new /api/chat endpoint
- ✅ Will properly implement the specified request/response schemas
- ✅ Will return proper HTTP status codes for all responses

#### AI-Powered Chatbot Integration
- ✅ Will integrate using Cohere API as LLM provider
- ✅ Will follow OpenAI Agents SDK architecture concepts (Agent, Runner, Tools)
- ✅ Agent will call MCP tools to interact with tasks, NOT directly access database
- ✅ Will handle natural language processing for task management

#### MCP Tool Governance
- ✅ Will implement MCP tools as stateless services within backend
- ✅ Tools will enforce user ownership and use existing Task tables
- ✅ Tools will return structured JSON only
- ✅ MCP tools will be the sole pathway for AI agent to interact with task data

#### Stateless Architecture Requirement
- ✅ FastAPI server will remain stateless with conversation history in database
- ✅ Each chat request will load conversation history from database
- ✅ No memory will be stored in RAM or global variables
- ✅ All state will live in database for scalability and restart resilience

## Gates

### Gate 1: Architecture Alignment
**Status**: PASS - Architecture aligns with all constitutional principles

### Gate 2: Security Compliance
**Status**: PASS - Security requirements met through JWT authentication and user isolation

### Gate 3: Integration Feasibility
**Status**: PASS - Integration with existing system architecture is feasible

### Gate 4: Technology Compatibility
**Status**: PASS - All planned technologies are compatible with existing stack

## Phase 0: Research & Resolution of Unknowns

### Research Task 1: Cohere API Integration
**Objective**: Understand how to integrate Cohere API with OpenAI Agents SDK patterns
- Research Cohere Python SDK documentation
- Investigate how to adapt Cohere responses to work with Agents SDK
- Determine how to maintain model-agnostic agent logic
**Status**: COMPLETED - See research.md for implementation approach

### Research Task 2: Backend Project Structure
**Objective**: Map the existing backend structure to determine where to place new AI module
- Locate existing FastAPI application structure
- Identify where to place AI module without disrupting existing functionality
- Understand current dependency management and imports
**Status**: COMPLETED - See research.md for module organization approach

### Research Task 3: Database Schema and Task Model
**Objective**: Examine existing database schema and Task model structure
- Locate existing Task model definition
- Understand current database connection setup
- Identify relationships and constraints in existing schema
**Status**: COMPLETED - See research.md and data-model.md for details

### Research Task 4: Frontend Integration Approach
**Objective**: Determine how to integrate chat UI with existing dashboard
- Locate current dashboard UI structure
- Identify optimal placement for chatbot icon/button
- Plan chat panel/modal integration approach
**Status**: COMPLETED - See research.md for UI integration approach

## Phase 1: Design & Architecture

### Design Step 1: Data Model Definition
- Define Conversation and Message models based on requirements
- Establish relationships between new and existing models
- Define validation rules and constraints
**Status**: COMPLETED - See data-model.md for detailed specifications

### Design Step 2: API Contract Definition
- Define the POST /api/chat endpoint contract
- Specify request/response schemas
- Define error handling patterns
**Status**: COMPLETED - See contracts/chat-api.yaml for OpenAPI specification

### Design Step 3: MCP Tool Specifications
- Define detailed specifications for add_task, list_tasks, update_task, complete_task, delete_task
- Specify input/output contracts for each tool
- Define error handling and validation for each tool
**Status**: COMPLETED - See research.md for implementation approach

### Design Step 4: Agent Configuration
- Define agent system prompt and configuration
- Specify tool registration and orchestration
- Define behavior patterns for intent detection and clarification
**Status**: COMPLETED - See research.md for architecture approach

## Phase 2: Implementation Order

### Implementation Step 1: Backend Foundation
1. Create dedicated AI module directory structure
2. Set up Cohere client configuration with environment variables
3. Implement MCP tool base infrastructure
4. Ensure module can be imported without affecting existing APIs

### Implementation Step 2: MCP Tool Implementation
1. Implement add_task MCP tool with user ownership enforcement
2. Implement list_tasks MCP tool with user ownership enforcement
3. Implement update_task MCP tool with user ownership enforcement
4. Implement complete_task MCP tool with user ownership enforcement
5. Implement delete_task MCP tool with user ownership enforcement

### Implementation Step 3: Database Models
1. Implement Conversation SQLAlchemy/SQLModel model
2. Implement Message SQLAlchemy/SQLModel model
3. Ensure proper relationships and constraints
4. Add necessary indexes for performance

### Implementation Step 4: Agent Orchestration
1. Define AI Agent with task management responsibilities
2. Register MCP tools with the agent
3. Configure agent for intent inference and tool selection
4. Implement validation for multi-step tool usage

### Implementation Step 5: Conversation Memory
1. Implement conversation context reconstruction from database
2. Implement message persistence for user and assistant messages
3. Ensure stateless operation across requests

### Implementation Step 6: Chat API Endpoint
1. Create secure POST /api/chat endpoint with JWT validation
2. Extract user identity from token
3. Integrate agent invocation with conversation context
4. Implement response formatting and persistence

### Implementation Step 7: Frontend Chat UI
1. Add chatbot icon/button to existing dashboard
2. Implement chat panel or modal UI component
3. Create message display components for user/assistant roles
4. Connect UI to /api/chat endpoint with proper error handling

### Implementation Step 8: Security & Validation
1. Implement comprehensive input validation
2. Add edge case handling for various error scenarios
3. Perform security testing for user isolation
4. Validate all authentication flows

### Implementation Step 9: Testing & Verification
1. Test all natural language task operations
2. Verify task CRUD via chatbot matches manual UI actions
3. Test server restart scenario and conversation continuity
4. Perform regression testing for Phase I & II features

## Success Criteria for Implementation

### Technical Success
- [ ] All MCP tools function correctly with proper user ownership
- [ ] Agent correctly interprets natural language and selects appropriate tools
- [ ] Conversation state persists correctly through database storage
- [ ] API endpoint properly authenticates and authorizes requests
- [ ] Frontend UI integrates seamlessly with existing dashboard

### Business Success
- [ ] Users can manage tasks using natural language as specified
- [ ] System maintains performance requirements (response times)
- [ ] User data isolation is maintained without exceptions
- [ ] No disruption to existing Phase I & II functionality
- [ ] System works correctly after server restarts

## Risk Assessment

### High-Risk Areas
1. **Cohere Integration**: May require significant adaptation to work with Agents SDK patterns
2. **Security**: Complex authentication flow could introduce vulnerabilities
3. **Performance**: Large conversation histories could impact response times

### Mitigation Strategies
1. **Thorough Testing**: Implement comprehensive testing for all integration points
2. **Security Reviews**: Conduct focused security reviews of authentication and authorization
3. **Performance Monitoring**: Implement monitoring for response times and database queries