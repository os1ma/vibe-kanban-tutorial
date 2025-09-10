# CLAUDE.md

## Project Overview
This is a TODO application project written in Python.

## Project Structure
```
.
├── CLAUDE.md (this file)
└── README.md
```

## Development Commands

### Installing Dependencies
```bash
uv sync
```

### Adding Dependencies
```bash
uv add <package-name>
```

### Adding Dev Dependencies
```bash
uv add --dev <package-name>
```

### Linting
```bash
uv run ruff check .
uv run ruff format .
```

### Type Checking
```bash
uv run mypy .
```

### Testing
```bash
uv run pytest
```

### Running the Application
```bash
uv run uvicorn app.main:app --reload
```

## Dependencies
- Python 3.11+
- uv (for dependency management)

## Notes
- This is a new TODO application project
- Implementation details to be added as development progresses