# Implementation Plan: Secure Todo Management Backend

**Feature**: Secure Todo Management Backend
**Branch**: `1-fastapi-backend`
**Created**: 2026-01-10
**Status**: Draft

## Technical Context

- **Backend Framework**: FastAPI (Python 3.9+)
- **ORM**: SQLModel for database interactions
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: JWT token verification (Better Auth)
- **Frontend Integration**: Next.js frontend via API calls
- **Environment**: Uses .env for configuration
- **API Style**: RESTful endpoints under `/api` prefix
- **Authentication Model**: Stateless JWT verification (tokens issued by frontend Better Auth)
- **Data Isolation**: Per-user task access enforcement
- **CORS Configuration**: Allow localhost:3000 for frontend integration

### Infrastructure Requirements
- **Runtime**: Python environment with uvicorn for ASGI server
- **Dependencies**: FastAPI, SQLModel, PyJWT, python-jose[cryptography], psycopg2-binary
- **Environment Variables**:
  - `BETTER_AUTH_SECRET`: JWT verification secret
  - `DATABASE_URL`: Neon PostgreSQL connection string

### Known Unknowns
- JWT token structure from Better Auth → RESOLVED: Uses standard JWT with 'sub' claim for user_id
- Exact CORS requirements beyond localhost:3000 → RESOLVED: Only localhost:3000 needed for frontend integration
- Database migration strategy → RESOLVED: Auto-create tables on startup for simplicity

## Constitution Check

### Full-Stack Specification Adherence
- [X] Backend API endpoints must match spec requirements
- [X] Database schema must match entity definitions
- [X] Authentication flows must follow JWT verification pattern

### Authentication-First Security
- [X] All endpoints require JWT token validation
- [X] User data isolation enforced on every query
- [X] No user_id accepted from request body (only from JWT)

### Test-First Implementation (NON-NEGOTIABLE)
- [X] Unit tests for JWT verification logic
- [X] Integration tests for all API endpoints
- [X] End-to-end tests for complete user flows

### Type-Safe Development
- [X] Pydantic models for all request/response schemas
- [X] Proper type hints in all Python functions
- [X] SQLModel models with proper typing

### Minimalist Feature Development
- [X] Minimal viable implementation for each endpoint
- [X] No over-engineering of authentication logic
- [X] Simple, focused API design

### API Contract Compliance
- [X] RESTful endpoint patterns
- [X] Proper HTTP status codes for all responses
- [X] Consistent request/response schemas

## Gates

### Gate 1: Environment & Dependencies
**Pass Condition**: Python environment ready with all required packages installed
**Verification**: `pip install fastapi sqlmodel uvicorn python-jose[cryptography] psycopg2-binary`

### Gate 2: Authentication Integration
**Pass Condition**: JWT tokens from Better Auth can be successfully verified
**Verification**: Token decoding and user_id extraction works with sample tokens

### Gate 3: Database Connectivity
**Pass Condition**: Successful connection to Neon PostgreSQL with table creation
**Verification**: Tasks table created and accessible with proper indexing

### Gate 4: API Endpoint Compliance
**Pass Condition**: All required endpoints implemented with proper authentication
**Verification**: All CRUD operations work with proper user isolation

### Gate 5: Frontend Integration
**Pass Condition**: Next.js frontend can successfully communicate with backend
**Verification**: API calls from frontend work with JWT token passing

## Phase 0: Research & Resolution

### research.md

#### Decision: JWT Token Handling from Better Auth
- **Rationale**: Need to understand exact JWT structure to properly decode user_id
- **Implementation**: Will verify JWT using BETTER_AUTH_SECRET and extract sub claim as user_id
- **Alternatives considered**: Using different claims (email, id), but sub is standard for user identification

#### Decision: Database Migration Strategy
- **Rationale**: Need reliable way to ensure database schema matches model definitions
- **Implementation**: Auto-create tables on startup for simplicity (can migrate to Alembic later)
- **Alternatives considered**: Alembic migrations vs manual SQL vs auto-create

#### Decision: CORS Policy
- **Rationale**: Frontend needs to communicate with backend securely
- **Implementation**: Allow localhost:3000 with credentials and authorization headers
- **Alternatives considered**: Wildcard vs specific origin vs multiple origins

#### Decision: Error Handling Strategy
- **Rationale**: Consistent error responses needed for frontend handling
- **Implementation**: Standard error response format with status codes
- **Alternatives considered**: Different error formats and structures

## Phase 1: Design & Contracts

### data-model.md

#### Entity: Task
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

#### Entity: User (Implicit)
- **Attributes**:
  - `user_id`: String (from JWT token payload)
  - Identified by `sub` claim in JWT

- **Access Control**:
  - User can only access tasks where user_id matches their JWT sub claim

### API Contracts

#### Authentication Contract
- **Header**: `Authorization: Bearer <JWT_TOKEN>`
- **Verification**: Validate JWT signature using BETTER_AUTH_SECRET
- **User Extraction**: Extract `sub` claim from JWT payload as user_id

#### Endpoint: GET /api/tasks
- **Method**: GET
- **Headers**: Authorization required
- **Query Parameters**:
  - `status`: all | pending | completed (optional)
- **Response**: Array of Task objects
- **Success**: 200 OK
- **Errors**: 401 Unauthorized

#### Endpoint: POST /api/tasks
- **Method**: POST
- **Headers**: Authorization required
- **Body**:
  - `title`: string (required, 1-200 chars)
  - `description`: string (optional)
- **Response**: Created Task object
- **Success**: 201 Created
- **Errors**: 400 Bad Request, 401 Unauthorized

#### Endpoint: GET /api/tasks/{id}
- **Method**: GET
- **Headers**: Authorization required
- **Path Parameter**: `id` (task identifier)
- **Response**: Single Task object
- **Success**: 200 OK
- **Errors**: 401 Unauthorized, 404 Not Found

#### Endpoint: PUT /api/tasks/{id}
- **Method**: PUT
- **Headers**: Authorization required
- **Path Parameter**: `id` (task identifier)
- **Body**:
  - `title`: string (required, 1-200 chars)
  - `description`: string (optional)
  - `completed`: boolean (optional)
- **Response**: Updated Task object
- **Success**: 200 OK
- **Errors**: 400 Bad Request, 401 Unauthorized, 404 Not Found

#### Endpoint: PATCH /api/tasks/{id}/complete
- **Method**: PATCH
- **Headers**: Authorization required
- **Path Parameter**: `id` (task identifier)
- **Body**:
  - `completed`: boolean (required)
- **Response**: Updated Task object
- **Success**: 200 OK
- **Errors**: 400 Bad Request, 401 Unauthorized, 404 Not Found

#### Endpoint: DELETE /api/tasks/{id}
- **Method**: DELETE
- **Headers**: Authorization required
- **Path Parameter**: `id` (task identifier)
- **Response**: Success message
- **Success**: 200 OK
- **Errors**: 401 Unauthorized, 404 Not Found

### quickstart.md

# Quick Start: FastAPI Backend

## Prerequisites
- Python 3.9+
- pip package manager

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi sqlmodel uvicorn python-jose[cryptography] psycopg2-binary python-dotenv
   ```

4. **Configure environment variables**
   Create `.env` file with:
   ```
   BETTER_AUTH_SECRET=your_better_auth_secret
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

5. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

6. **Verify setup**
   - Navigate to `http://localhost:8000/docs` for API documentation
   - Backend should connect to database successfully

## Running Tests
```bash
pytest tests/
```

## Environment Variables
- `BETTER_AUTH_SECRET`: Secret key for verifying JWT tokens from Better Auth
- `DATABASE_URL`: PostgreSQL connection string for Neon database
- `ENVIRONMENT`: Set to "development", "staging", or "production"

## API Access
- Base URL: `http://localhost:8000/api`
- Authentication: Include `Authorization: Bearer <token>` header with all requests
- Frontend integration: Configure API client to append JWT from Better Auth

## Troubleshooting
- If getting database connection errors, verify DATABASE_URL format
- If JWT verification fails, ensure BETTER_AUTH_SECRET matches Better Auth configuration
- Check CORS errors if integrating with frontend from different port

## Next Steps
1. Implement JWT verification logic
2. Set up database models and connections
3. Create API endpoints with proper authentication
4. Integrate with frontend application