# AI Todo Chatbot Feature Documentation

## Overview
The AI Todo Chatbot feature enables users to manage their todo tasks through natural language interactions with an AI assistant. The system integrates with the existing todo management backend and provides a conversational interface for task operations.

## Features

### 1. Natural Language Task Management
Users can interact with the chatbot using natural language to:
- Add tasks: "Add a task to buy groceries"
- List tasks: "Show my pending tasks"
- Update tasks: "Change task 1 to 'buy milk and bread'"
- Complete tasks: "Complete task 1"
- Delete tasks: "Delete task 1" (with confirmation)

### 2. Conversation Context and History
- Maintains conversation context across multiple interactions
- Persists conversation history in the database
- Allows users to refer to previous exchanges in ongoing conversations

### 3. Secure Task Isolation
- Enforces strict user data isolation
- Users can only access and modify their own tasks
- Proper authentication and authorization checks

## Technical Implementation

### Backend Architecture
- **Routes**: `/api/chat` endpoint handles chat interactions
- **AI Services**: Cohere integration for natural language processing
- **MCP Tools**: Modular tools for task operations (add, list, update, complete, delete)
- **Database**: SQLModel for data persistence with proper indexing

### Security Features
- JWT-based authentication
- Rate limiting (10 requests per minute per IP)
- User isolation for task access
- Input validation for message length and content

### Error Handling
- Comprehensive error handling for Cohere API unavailability
- Connection and timeout error management
- Authentication error handling
- User-friendly error messages

### Performance Monitoring
- Response time tracking and logging
- Proper indexing for optimized database queries
- Efficient conversation context retrieval

## Confirmation for Destructive Operations
The system implements a confirmation mechanism for destructive operations like task deletion:
1. When a user requests a destructive action, the system asks for confirmation
2. The operation is held pending until the user confirms
3. User can confirm with responses like "yes", "confirm", "ok", etc.
4. The operation proceeds only after explicit confirmation

## API Endpoints

### POST /api/chat
- **Authentication**: Required JWT token
- **Rate Limit**: 10 requests per minute per IP
- **Request Body**:
  ```json
  {
    "conversation_id": "optional-existing-conversation-id",
    "message": "user message in natural language"
  }
  ```
- **Response**:
  ```json
  {
    "conversation_id": "conversation-identifier",
    "response": "assistant response",
    "tool_calls": ["list-of-executed-tool-calls"]
  }
  ```

## Frontend Integration
- Chat panel component accessible from the dashboard
- Real-time messaging interface
- Conversation persistence across sessions
- Loading states and error handling

## Environment Variables
- `COHERE_API_KEY`: API key for Cohere integration
- Standard backend environment variables (auth secret, database URL)

## Testing
The feature has been tested for:
- Basic task operations via natural language
- Conversation continuity and context maintenance
- Cross-user data isolation
- Error handling scenarios
- Rate limiting functionality
- UI integration