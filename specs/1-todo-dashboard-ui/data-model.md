# Data Model: Todo Dashboard UI

## Task Entity
- **id**: Unique identifier for the task (string/number)
- **title**: The main text of the task (string)
- **description**: Optional detailed description of the task (string, nullable)
- **completed**: Boolean indicating completion status (boolean)
- **createdAt**: Timestamp when the task was created (Date/string)
- **updatedAt**: Timestamp when the task was last updated (Date/string)
- **userId**: Foreign key linking to the user who owns the task (string/number)

## User Entity
- **id**: Unique identifier for the user (string/number)
- **email**: User's email address (string)
- **name**: User's display name (string)
- **createdAt**: Timestamp when the user account was created (Date/string)

## Validation Rules
- Task title must not be empty
- Task userId must reference an existing user
- createdAt and updatedAt timestamps are automatically managed by the system

## Relationships
- A User has many Tasks (one-to-many relationship)
- Each Task belongs to a single User

## State Transitions
- Task can transition from incomplete (completed: false) to complete (completed: true)
- Task can transition from complete (completed: true) back to incomplete (completed: false)
- Task can be deleted by the owning user