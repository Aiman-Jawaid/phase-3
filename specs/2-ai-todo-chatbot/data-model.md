# Data Model: AI Todo Chatbot (Phase III)

## Overview
This document defines the data models for the AI Todo Chatbot feature, including new models for conversation management and their relationships to existing models.

## Entity Definitions

### Conversation
**Description**: Represents a chat session between a user and the AI assistant, containing metadata about the conversation and linking to associated messages.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the conversation
- `user_id`: UUID/FK - Reference to the user who owns this conversation
- `created_at`: DateTime - Timestamp when the conversation was initiated
- `updated_at`: DateTime - Timestamp when the conversation was last updated

**Relationships**:
- One-to-Many with Message (one conversation has many messages)
- Many-to-One with User (many conversations belong to one user)

**Validation Rules**:
- `user_id` must reference an existing user
- `created_at` is set automatically on creation
- `updated_at` is updated automatically when messages are added

### Message
**Description**: Represents an individual message in a conversation, storing the content, sender (user or assistant), timestamp, and linking to the conversation and user.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the message
- `conversation_id`: UUID/FK - Reference to the conversation this message belongs to
- `user_id`: UUID/FK - Reference to the user who sent this message
- `role`: String(Enum: "user", "assistant") - Indicates whether the message was sent by user or assistant
- `content`: Text - The actual content of the message
- `created_at`: DateTime - Timestamp when the message was created

**Relationships**:
- Many-to-One with Conversation (many messages belong to one conversation)
- Many-to-One with User (many messages are associated with one user)

**Validation Rules**:
- `conversation_id` must reference an existing conversation
- `user_id` must reference an existing user
- `role` must be either "user" or "assistant"
- `content` must not be empty
- `created_at` is set automatically on creation

### Task (Existing)
**Description**: Represents a todo item owned by a user, containing title, description, completion status, and timestamps. This model is reused from Phase II.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the task
- `user_id`: UUID/FK - Reference to the user who owns this task
- `title`: String - The title of the task
- `description`: Text (Optional) - Detailed description of the task
- `completed`: Boolean - Whether the task is completed
- `created_at`: DateTime - Timestamp when the task was created
- `updated_at`: DateTime - Timestamp when the task was last updated

**Relationships**:
- Many-to-One with User (many tasks belong to one user)

**Validation Rules**:
- `user_id` must reference an existing user
- `title` must not be empty
- `completed` defaults to false

## State Transitions

### Task State Transitions
- **Pending → Completed**: When a user marks a task as done via chatbot or UI
- **Completed → Pending**: When a user reopens a completed task via chatbot or UI

### Message Role Transitions
- **Static**: Message roles are immutable once created (either "user" or "assistant")

## Indexes and Performance Considerations

### Required Indexes
1. `Conversation.user_id` - For efficient retrieval of conversations by user
2. `Message.conversation_id` - For efficient retrieval of messages by conversation
3. `Message.created_at` - For chronological ordering of messages
4. `Task.user_id` - For efficient retrieval of tasks by user
5. `Task.completed` - For filtering completed vs pending tasks

### Query Patterns
1. Retrieve all conversations for a specific user
2. Retrieve all messages in a specific conversation (chronological order)
3. Retrieve all tasks for a specific user (filtered by completion status)
4. Retrieve latest message in a conversation for context

## Data Integrity Constraints

### Foreign Key Constraints
- `Conversation.user_id` references `User.id`
- `Message.conversation_id` references `Conversation.id`
- `Message.user_id` references `User.id`
- `Task.user_id` references `User.id`

### Ownership Enforcement
- All MCP tools must verify that the authenticated user matches the `user_id` field
- Queries should always filter by the authenticated user's `user_id`
- No cross-user data access is allowed

## Schema Evolution Considerations

### Future Extensibility
- Conversation model could include `title` field for user-defined titles
- Message model could include `metadata` field for tool call information
- Task model could include `priority` or `due_date` fields in future phases

### Migration Strategy
- New tables (Conversation, Message) can be added without affecting existing Task table
- All new models should follow the same naming and constraint conventions as existing models
- Indexes should be added with consideration for performance impact during peak usage