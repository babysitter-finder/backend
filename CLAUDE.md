# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Babysitter Finder backend - A Django REST Framework API for a babysitter service platform. Uses Docker for development and production environments.

### Tech Stack
- Python 3.12 (Docker: python:3.12-slim-bookworm)
- Django 5.1.4
- Django REST Framework 3.15.2
- Celery 5.4.0 with Redis 7.4
- PostgreSQL 16
- Geocoding: geopy with Nominatim (OpenStreetMap)

## Development Commands

### Docker-based development (recommended)
```bash
# Build containers
docker-compose -f local.yml build

# Run containers
docker-compose -f local.yml up

# Run migrations
docker-compose -f local.yml run --rm django python manage.py makemigrations
docker-compose -f local.yml run --rm django python manage.py migrate
```

### Running tests
```bash
docker-compose -f local.yml run --rm django pytest

# Run specific test file
docker-compose -f local.yml run --rm django pytest hisitter/users/tests/test_views.py

# Run with coverage
docker-compose -f local.yml run --rm django coverage run -m pytest
```

### Code quality
```bash
# Pre-commit hooks (black, isort, flake8)
docker-compose -f local.yml run --rm django pre-commit run --all-files

# Individual tools
docker-compose -f local.yml run --rm django black .
docker-compose -f local.yml run --rm django flake8
docker-compose -f local.yml run --rm django mypy hisitter
```

## Architecture

### Django Apps (in `hisitter/`)
- **users**: Custom User model with Client and Babysitter profiles, includes Availability model for babysitters
- **services**: Service bookings between clients and babysitters
- **reviews**: Review system for completed services

### Configuration
- Settings split into `config/settings/` (base, local, production, test)
- Uses `django-environ` for environment variables
- Celery configured with Redis broker and django-celery-beat for scheduled tasks

### API
- Django REST Framework with Token Authentication
- API documentation at `/swagger/` and `/redoc/`
- All apps expose endpoints via `hisitter/<app>/urls.py`

### Key Models
- `User` (custom): Base user extending AbstractUser
- `Client`: User profile for parents seeking babysitters
- `Babysitter`: User profile with availability scheduling
- `Service`: Booking record linking client and babysitter
- `Review`: Feedback for completed services

### Background Tasks
- Celery workers for async tasks (email sending via Mailgun)
- Celery beat for scheduled tasks
- Flower dashboard at port 5555 for monitoring

## Code Style

- Line length: 120 characters
- Formatting: Black, isort
- Linting: flake8, pylint-django
- Type checking: mypy with django-stubs
