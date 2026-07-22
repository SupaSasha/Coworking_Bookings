# Coworking Bookings

A backend service for booking workplaces in coworking spaces — desks, meeting rooms, private offices — with hourly time-slot scheduling.

Built with FastAPI, async SQLAlchemy, and Celery, following a layered architecture (`api → services → repositories → models`).

## Features

- **Hourly booking** — reserve a workplace for a specific `datetime_from` / `datetime_to` window, not just a full day.
- **Multiple workplace types per coworking** — each coworking location has its own set of workplaces (open desks, meeting rooms, private offices), each with its own price and available quantity.
- **Facilities** — amenities (Wi-Fi, coffee, printer, etc.) attached to workplaces through a many-to-many relationship.
- **JWT authentication** — access tokens issued on login/register, current-user lookup via `/auth/me`.
- **Password hashing via `pwdlib` (Argon2)** — modern password hashing, not legacy `bcrypt`/`passlib`.
- **Response caching** — Redis-backed caching via `fastapi-cache2` on read endpoints.
- **Background tasks** — Celery worker + beat, backed by Redis.
- **Versioned schema** — Alembic migrations.
- **Integration test suite** — `pytest` + `pytest-asyncio`, with a dedicated `test` service in Docker Compose.

## Tech stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL (via `asyncpg`) |
| Migrations | Alembic |
| Cache / broker | Redis |
| Background tasks | Celery (worker + beat) |
| Auth | JWT (`PyJWT`) + `pwdlib[argon2]` |
| Dependency management | Poetry |
| Testing | pytest, pytest-asyncio |
| Containerization | Docker Compose |

## Architecture

```
api/            HTTP endpoints (FastAPI routers)
   ↓
services/       Business logic, domain exceptions
   ↓
repositories/   Database access (SQLAlchemy CRUD)
   ↓
models/         ORM models (tables)
   ↓
database.py     Engine, session factory
   ↓
config.py       Settings (.env)
```

Each layer only depends on the layer directly below it.

## Data model

| Entity | Table | Description |
|---|---|---|
| `CoworkingsOrm` | `coworkings` | A physical location/branch (`title`, `location`) |
| `WorkplacesOrm` | `workplaces` | A bookable unit within a coworking (`title`, `description`, `price`, `quantity`) |
| `FacilitiesOrm` | `facilities` | An amenity, linked to workplaces many-to-many via `workplaces_facilities` |
| `UserOrm` | `users` | Registered account (email + hashed password) |
| `BookingsOrm` | `bookings` | A reservation: `workplace_id`, `user_id`, `datetime_from`, `datetime_to`, `price` |

## Getting started

### Prerequisites
- Python 3.12.13 (pinned in `pyproject.toml`)
- [Poetry](https://python-poetry.org/) 2.x
- Docker & Docker Compose
- PostgreSQL and Redis

### Setup

```bash
git clone https://github.com/SupaSasha/Coworking_Bookings
cd Coworking_Bookings

cp .env-example .env   # fill in DB / Redis / JWT settings

poetry install
```

### Run with Docker Compose

```bash
docker compose up -d --build
```

Starts the API (`booking_back`), Celery worker, Celery beat, and Redis, all attached to the external `myNetwork` Docker network (create it beforehand with `docker network create myNetwork` if it doesn't exist yet). PostgreSQL itself is expected to be reachable via `host.docker.internal` — see `extra_hosts` in `docker-compose.yml`.

### Run locally

```bash
poetry run alembic upgrade head
poetry run uvicorn src.main:app --reload
```

API docs available at `http://localhost:7777/docs`.

## API overview

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Create a new user |
| `POST` | `/auth/login` | Authenticate, set JWT cookie |
| `GET` | `/auth/me` | Get the current authenticated user |
| `POST` | `/auth/logout` | Clear the auth cookie |
| `GET` | `/coworkings` | List coworking locations |
| `POST` | `/coworkings` | Create a coworking location |
| `GET` / `PUT` / `PATCH` / `DELETE` | `/coworkings/{coworking_id}` | Manage a single coworking location |
| `GET` | `/coworkings/{coworking_id}/workplaces` | List workplaces at a location |
| `POST` | `/coworkings/{coworking_id}/workplaces` | Create a workplace |
| `PUT` / `PATCH` / `DELETE` | `/coworkings/{coworking_id}/workplaces/{workplace_id}` | Manage a single workplace |
| `GET` | `/facilities` | List available facilities |
| `POST` | `/facilities` | Create a facility |
| `POST` | `/bookings` | Create a booking |
| `GET` | `/bookings` | List all bookings |
| `GET` | `/bookings/me` | List the current user's bookings |

Full interactive documentation is available via Swagger UI at `/docs`.

## Testing

```bash
poetry run pytest
```

or, via Docker Compose:

```bash
docker compose run --rm test
```

## License
MIT
