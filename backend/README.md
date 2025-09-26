# FastAPI Boilerplate

A production-ready FastAPI application boilerplate with clean architecture, dependency injection, and best practices.

## Features

- **Clean Architecture**: Separation of concerns with repositories, services, and API layers
- **Async Database**: SQLAlchemy with async support and session management
- **Authentication**: JWT-based authentication with password hashing
- **Dependency Injection**: FastAPI's dependency system for loose coupling
- **Configuration Management**: Environment-based configuration with validation
- **Database Migrations**: Alembic for database schema management
- **Containerization**: Docker and docker-compose setup
- **Logging**: Structured logging with configurable levels
- **Security**: CORS, trusted hosts, and security middleware
- **Type Safety**: Full type hints throughout the codebase

## Project Structure

```
app/
├── api/                    # API layer
│   ├── dependencies.py     # Dependency injection
│   └── v1/                 # API version 1
│       ├── endpoints/      # API endpoints
│       └── router.py       # Route configuration
├── core/                   # Core functionality
│   ├── config.py          # Configuration management
│   ├── database.py        # Database setup
│   ├── logging.py         # Logging configuration
│   └── security.py        # Security utilities
├── models/                 # Database models
├── repositories/           # Data access layer
│   ├── base.py            # Base repository pattern
│   └── user.py            # User repository
├── schemas/                # Pydantic schemas
├── services/               # Business logic layer
└── main.py                # Application entry point
```

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd fastapi-boilerplate
   cp .env.example .env
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Docker Setup

1. **Using docker-compose**:
   ```bash
   docker-compose up --build
   ```

2. **Using Docker only**:
   ```bash
   docker build -t fastapi-app .
   docker run -p 8000:8000 fastapi-app
   ```

## Database Migrations

1. **Initialize Alembic** (first time):
   ```bash
   alembic init alembic
   ```

2. **Create migration**:
   ```bash
   alembic revision --autogenerate -m "Create users table"
   ```

3. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get user by ID

## Configuration

Environment variables (see `.env.example`):

- `PROJECT_NAME` - Application name
- `DEBUG` - Debug mode
- `SECRET_KEY` - JWT secret key
- `DATABASE_URL` - Database connection string
- `CORS_ORIGINS` - Allowed CORS origins

## Architecture Patterns

### Repository Pattern
- Abstracts data access logic
- Provides consistent interface for data operations
- Supports testing with mock repositories

### Service Layer
- Contains business logic
- Orchestrates between repositories and API
- Handles validation and business rules

### Dependency Injection
- Loose coupling between components
- Easy testing and mocking
- Clean separation of concerns

## Security Features

- JWT token authentication
- Password hashing with bcrypt
- CORS middleware
- Trusted host middleware
- Input validation with Pydantic

## Development

1. **Code Style**: Follow PEP 8 and use type hints
2. **Testing**: Add tests for repositories, services, and endpoints
3. **Logging**: Use the provided logger mixin for consistent logging
4. **Error Handling**: Use FastAPI's HTTPException for API errors

## Production Deployment

1. **Environment Variables**: Set production values in `.env`
2. **Database**: Use PostgreSQL or MySQL for production
3. **Security**: Change default secret keys and passwords
4. **Monitoring**: Add health checks and monitoring
5. **Scaling**: Use multiple workers with Gunicorn

## License

MIT License
