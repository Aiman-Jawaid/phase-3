# Todo API Backend

Secure Todo Management Backend with JWT Authentication built using FastAPI and SQLModel.

## Features

- JWT-based authentication and authorization
- User-isolated task management
- Full CRUD operations for tasks
- Filtering by task status (pending, completed)
- Data validation and error handling
- Secure API endpoints

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (via SQLModel)
- **Authentication**: JWT tokens with python-jose
- **ORM**: SQLModel (combines Pydantic and SQLAlchemy)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables by copying `.env.example` to `.env` and setting the appropriate values

## Environment Variables

- `BETTER_AUTH_SECRET`: Secret key for verifying JWT tokens from Better Auth
- `DATABASE_URL`: PostgreSQL connection string for Neon database
- `ENVIRONMENT`: Set to "development", "staging", or "production"

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

API documentation is available at `http://localhost:8000/docs`.

## API Endpoints

### Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

### Tasks

- `GET /api/tasks` - Get all tasks for the authenticated user
  - Query parameters: `status` (all, pending, completed)
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status
- `DELETE /api/tasks/{id}` - Delete a task

## Security

- All API endpoints require JWT authentication
- Users can only access their own tasks
- Input validation is performed on all endpoints
- Proper error handling without sensitive information disclosure

## Development

To run tests:
```bash
pytest tests/
```

For database migrations (in production), consider using Alembic after initial development.