# Research Summary: Secure Todo Management Backend

## Decision: JWT Token Handling from Better Auth
- **Rationale**: Need to understand exact JWT structure to properly decode user_id. Better Auth follows standard JWT practices where the subject claim (sub) contains the user identifier. This is the standard practice for user identification in JWT tokens.
- **Implementation**: Will verify JWT using BETTER_AUTH_SECRET and extract sub claim as user_id. Use python-jose library for secure token verification.
- **Alternatives considered**: Using different claims (email, id), but sub is standard for user identification and is what Better Auth uses by default.

## Decision: Database Migration Strategy
- **Rationale**: Need reliable way to ensure database schema matches model definitions. For a simple application like this, auto-creating tables on startup is sufficient while keeping complexity low.
- **Implementation**: Auto-create tables on startup for simplicity using SQLModel's create_engine with echo=True for debugging (can migrate to Alembic later if needed).
- **Alternatives considered**: Alembic migrations vs manual SQL vs auto-create. Alembic would be overkill for this simple schema, while auto-create is perfect for development and simple deployments.

## Decision: CORS Policy
- **Rationale**: Frontend needs to communicate with backend securely without exposing the API unnecessarily.
- **Implementation**: Allow localhost:3000 with credentials and authorization headers using FastAPI's CORSMiddleware.
- **Alternatives considered**: Wildcard (*) vs specific origin vs multiple origins. Specific origin is most secure for development.

## Decision: Error Handling Strategy
- **Rationale**: Consistent error responses needed for frontend handling to provide good user experience.
- **Implementation**: Standard error response format with status codes using FastAPI's HTTPException for proper HTTP responses.
- **Alternatives considered**: Different error formats and structures. FastAPI's built-in exception handling is the standard approach.

## Decision: Dependency Management
- **Rationale**: Need to select the right libraries that work well with FastAPI and SQLModel.
- **Implementation**:
  - FastAPI: Modern Python web framework with excellent Pydantic integration
  - SQLModel: Combines Pydantic and SQLAlchemy for type-safe database models
  - python-jose: Secure JWT handling library
  - uvicorn: ASGI server for running FastAPI
- **Alternatives considered**: Other ORMs like Tortoise ORM, but SQLModel integrates better with Pydantic schemas used by FastAPI.

## Decision: Authentication Middleware Pattern
- **Rationale**: Need a reusable way to protect endpoints and extract user context.
- **Implementation**: Create a dependency function that verifies JWT and returns user_id. This can be injected into any route that requires authentication.
- **Alternatives considered**: Decorators vs dependencies vs custom middleware class. FastAPI dependencies are the idiomatic approach.

## Decision: Project Structure
- **Rationale**: Organize code in a maintainable way that follows Python/FastAPI best practices.
- **Implementation**:
  - `main.py`: Application entry point
  - `db.py`: Database engine and session management
  - `models.py`: SQLModel database models
  - `schemas.py`: Pydantic request/response models
  - `auth.py`: JWT verification logic
  - `routes/tasks.py`: Task-related API endpoints
- **Alternatives considered**: Different structuring approaches, but this follows FastAPI's recommended patterns.

## Decision: Environment Configuration
- **Rationale**: Secure handling of sensitive configuration values like database URLs and auth secrets.
- **Implementation**: Use python-dotenv to load from .env file, with validation for required variables.
- **Alternatives considered**: Hardcoded values (insecure), environment variables only, or config files. python-dotenv provides the right balance of security and convenience.