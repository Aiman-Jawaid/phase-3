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