# Quickstart Guide: AI Todo Chatbot Implementation

## Overview
This guide provides a quick overview of the AI Todo Chatbot implementation to help developers get started quickly.

## Architecture Summary

### Components
1. **AI Agent**: Core component that processes natural language and orchestrates tool usage
2. **MCP Tools**: Stateless functions that interact with the database (add_task, list_tasks, update_task, complete_task, delete_task)
3. **Conversation Manager**: Handles persistence and retrieval of conversation history
4. **Chat API Endpoint**: Secure endpoint that connects user requests to the agent

### Data Flow
1. User sends message to POST /api/chat
2. Endpoint validates JWT and extracts user_id
3. Conversation history is loaded from database
4. AI agent processes message and may call MCP tools
5. MCP tools perform database operations with user ownership validation
6. Agent generates response based on tool results
7. Response and conversation history are saved to database
8. Response is returned to user

## Environment Setup

### Required Environment Variables
```bash
COHERE_API_KEY=your_cohere_api_key_here
DATABASE_URL=your_database_connection_string
BETTER_AUTH_SECRET=your_auth_secret
```

### Project Structure
```
backend/
├── ai/                     # AI module
│   ├── agents/             # Agent orchestration
│   ├── mcp_tools/          # MCP tools implementation
│   ├── models/             # New conversation models
│   └── services/           # Conversation services
├── api/                    # Existing API routes
├── models/                 # Existing data models
└── main.py                 # FastAPI application entry point
```

## Key Implementation Files

### MCP Tools
Located in `backend/ai/mcp_tools/`
- `add_task.py` - Creates new tasks for authenticated user
- `list_tasks.py` - Retrieves tasks for authenticated user
- `update_task.py` - Updates existing tasks for authenticated user
- `complete_task.py` - Marks tasks as completed for authenticated user
- `delete_task.py` - Deletes tasks for authenticated user

### Agent Components
Located in `backend/ai/agents/`
- `chat_agent.py` - Main agent class that processes user input
- `cohere_client_wrapper.py` - Adapter for Cohere API integration
- `tool_registry.py` - Registry for MCP tools

### Models
Located in `backend/ai/models/`
- `conversation.py` - Conversation model definition
- `message.py` - Message model definition

### Services
Located in `backend/ai/services/`
- `conversation_service.py` - Manages conversation lifecycle
- `message_service.py` - Handles message persistence

## Development Workflow

### 1. Start with MCP Tools
Implement the MCP tools first as they are the foundation for database operations:
```python
# Example MCP tool structure
def add_task(user_id: str, title: str, description: str = None) -> dict:
    """Add a new task for the authenticated user."""
    # Validate user_id owns this task
    # Create task in database
    # Return structured result
```

### 2. Build the Agent
Create the agent that will orchestrate tool usage:
```python
# Example agent interaction
def process_message(conversation_id: str, user_id: str, message: str) -> str:
    """Process user message and return agent response."""
    # Load conversation history
    # Determine intent and select tools
    # Execute tools and get results
    # Generate response
```

### 3. Implement the API Endpoint
Connect everything through the secure API endpoint:
```python
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest, current_user: User = Depends(get_current_user)):
    # Process message through agent
    # Return response
```

## Testing Approach

### Unit Tests
- Test each MCP tool individually with different user contexts
- Test agent logic with mock tools
- Test conversation history reconstruction

### Integration Tests
- Test full chat flow from API to database
- Verify user isolation between different users
- Test authentication and authorization

### End-to-End Tests
- Test natural language commands end-to-end
- Verify conversation continuity after server restart
- Test error handling for invalid inputs

## Security Considerations

### User Isolation
- Every MCP tool must validate that the operation is for the authenticated user
- Never trust user_id from frontend input - always extract from JWT
- Implement proper error handling when users try to access others' data

### Input Validation
- Validate all inputs before passing to agent/tools
- Implement rate limiting to prevent abuse
- Sanitize all user inputs to prevent injection attacks

## Performance Considerations

### Database Queries
- Add proper indexes on user_id, conversation_id, and created_at fields
- Use efficient queries to load conversation history
- Consider pagination for very long conversations

### Cohere API Usage
- Implement proper error handling for API timeouts/unavailability
- Consider caching for frequently requested information
- Monitor API usage costs