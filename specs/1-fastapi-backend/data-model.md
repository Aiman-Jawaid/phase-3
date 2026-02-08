# Data Model: Secure Todo Management Backend

## Entity: Task
- **Attributes**:
  - `id`: Integer (Primary Key, Auto-increment)
  - `user_id`: String (Indexed, Foreign Key reference)
  - `title`: String (Required, 1-200 characters)
  - `description`: Text (Optional)
  - `completed`: Boolean (Default: False)
  - `created_at`: DateTime (Auto-populated)
  - `updated_at`: DateTime (Auto-populated)

- **Relationships**:
  - Belongs to exactly one User (identified by user_id from JWT)

- **Validation Rules**:
  - Title must be 1-200 characters
  - Completed defaults to False
  - User can only access their own tasks

## Entity: User (Implicit)
- **Attributes**:
  - `user_id`: String (from JWT token payload)
  - Identified by `sub` claim in JWT

- **Access Control**:
  - User can only access tasks where user_id matches their JWT sub claim

## Database Schema
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

## Constraints
- `title` is required and must be 1-200 characters
- `completed` defaults to False
- `user_id` is indexed for performance
- `completed` is indexed for filtering
- All tasks are associated with a user_id from JWT