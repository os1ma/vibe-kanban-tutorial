# TODO Application

A modern TODO application built with Python and FastAPI.

## Features

- Create, read, update, and delete TODO items
- RESTful API design
- Type-safe with Python type hints
- Fast and efficient with FastAPI

## Requirements

- Python 3.11+
- uv (for dependency management)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Install dependencies using uv:
```bash
uv sync
```

## Usage

### Running the Application

Start the development server:
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## Development

### Running Tests
```bash
uv run pytest
```

### Linting and Formatting
```bash
uv run ruff check .
uv run ruff format .
```

### Type Checking
```bash
uv run mypy .
```

## Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── models/          # Data models
│   ├── routers/         # API route handlers
│   └── services/        # Business logic
├── tests/               # Test files
├── pyproject.toml       # Project configuration and dependencies
├── CLAUDE.md           # Development instructions
└── README.md           # This file
```

## License

[License information to be added]
