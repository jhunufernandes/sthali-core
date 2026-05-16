# sthali-core

Core foundational package for the Sthali FastAPI ecosystem. Provides YAML-based configuration loading and validation via Pydantic.

## Project Structure

```
src/sthali_core/
└── config.py       # ConfigSchema (Pydantic base) + Config (YAML loader)
tests/
└── test_config.py  # Full unit test coverage (unittest style)
```

## Key Concepts

- **`ConfigSchema`** — Pydantic `BaseModel` subclass used as the base for all config schemas across the Sthali ecosystem. Extra fields are silently ignored by Pydantic.
- **`Config`** — YAML file loader. Reads the file, stores raw data in `yaml_config`, then calls `validate()`. Subclasses override `config_schema` (a `ClassVar`) to enforce stricter schemas.
- **`Config.load()`** — Class method that reads `CONFIG_FILE_PATH` env var (default: `config.yaml`) and returns a `Config` instance.

## Dependency Chain

`sthali-core` is the root. Nothing in core depends on other sthali packages.

## Python Version

Requires Python >= 3.14. Uses modern type hint syntax (`Self`, `ClassVar`).

## Testing

Uses stdlib `unittest` (not pytest). Run with:

```bash
cd /home/jhunu/sth/sthali-core
/home/jhunu/sth/.venv/bin/python -m unittest discover tests/
# or with coverage:
/home/jhunu/sth/.venv/bin/python -m coverage run -m unittest discover tests/ && python -m coverage report
```

## Linting

Ruff with `ALL` rules, Google docstring convention. Line length 119. Run:

```bash
/home/jhunu/sth/.venv/bin/ruff check src/ tests/
```

## Key Rules for AI

- Do not add new dependencies; this package intentionally depends only on `fastapi` (which pulls `pydantic`).
- Keep `ConfigSchema` as a plain Pydantic BaseModel with no required fields — subclasses add their own required fields.
- `Config.config_schema` is a `ClassVar[type[ConfigSchema]]`; subclasses set it to their own schema class.
- Tests use `unittest.TestCase`, not pytest. Maintain that style.
