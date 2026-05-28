# 🏥 Sanatorium Selection Service

A web service that recommends sanatoriums best matching a user's preferences. Ranking is powered by a **Weighted Goal Programming** algorithm — a multi-criteria optimization method.

Course project, Saint Petersburg Electrotechnical University (ETU "LETI"), Department of Information Systems, 2026.

![Python](https://img.shields.io/badge/python-3.11-blue)
![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-orange)
![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue)
![Tests](https://img.shields.io/badge/tests-35%20passed-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-83%25-brightgreen)

---

## Features

- User registration and authentication
- Customizable preference profile: budget, region, treatment goal, medical profile, services, accommodation conditions
- Tag system (28 tags across 3 categories) describing both sanatoriums and user preferences
- Priority sliders — the user sets the importance of each criterion
- Weighted Goal Programming algorithm for ranking sanatoriums
- Sanatorium catalog with detailed views
- Side-by-side comparison of up to 3 sanatoriums
- Review system with ratings
- Password change

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask, SQLAlchemy 2.0 |
| Frontend | React (JavaScript) |
| Database | PostgreSQL |
| Containerization | Docker, docker-compose |
| Testing | pytest, testcontainers |
| Code quality | ruff, mypy, pre-commit |

---

## Architecture

The project follows **Domain-Driven Design** principles (based on Percival & Gregory's *Architecture Patterns with Python*):

```
courseSanat/
├── domain/                  # Domain layer
│   ├── model.py             # Entities: User, UserProfile, Sanatorium, Tag, Review
│   └── goal_programming.py  # Weighted Goal Programming algorithm
├── adapters/                # Infrastructure layer
│   ├── database.py          # DB connection, association tables
│   ├── orm.py               # ORM mapping (SQLAlchemy)
│   └── repository.py        # Repositories (Repository pattern)
├── service_layer/           # Service layer
│   ├── services.py          # Application/business logic
│   ├── handlers.py          # Event handlers
│   └── message_bus.py       # Event bus
├── entrypoints/             # Entry points
│   └── flask_app.py         # REST API (Flask)
├── frontend/                # React application
│   └── src/App.js           # Single component with navigation
├── tests/                   # Test suite
│   ├── unit/                # Unit tests (algorithm, domain models)
│   ├── integration/         # Integration tests (repositories + real DB)
│   ├── api/                 # API tests (Flask test client)
│   └── conftest.py          # Shared fixtures (testcontainers, sessions)
├── seed.py                  # Database seeding with sample data
├── Dockerfile               # Backend image
├── docker-compose.yml       # Service orchestration
├── pyproject.toml           # Tooling config (ruff, mypy, pytest)
├── .pre-commit-config.yaml  # Pre-commit hooks
└── requirements.txt         # Python dependencies
```

### Design Patterns

**Domain-Driven Design** — domain models are independent of the database and frameworks. Business logic is encapsulated in the domain.

**Repository Pattern** — repositories abstract data access. The domain works with plain Python objects; conversion to ORM happens inside the repositories. Repositories receive their database session via dependency injection, which keeps them decoupled and testable.

**Service Layer** — coordinates calls between the domain and repositories.

**Event-Driven Architecture** — domain objects raise events (UserRegistered, ProfileCreated, ReviewCreated), and an event bus routes them to their handlers.

**Data Mapper** — ORM classes are separated from domain models; mapping is performed in the repository layer.

---

## Weighted Goal Programming Algorithm

Goal Programming solves a multi-criteria optimization problem: the user has several goals at once (low price, preferred region, desired services), and the algorithm finds the option with the minimal total deviation from all goals.

### Formalization

For each sanatorium a **score** is computed — a weighted sum of normalized deviations from the user's goals. The lower the score, the better the sanatorium matches the request.

#### Step 1: Weight normalization

The user sets criterion priorities (from 1 to 10). Weights are normalized:

```
w_i = priority_i / (priority_budget + priority_region + priority_medical + priority_services + priority_conditions)
```

The sum of all w_i = 1.

#### Step 2: Deviation calculation

**Budget** (percentage normalization):
```
d_budget = max(0, sanatorium_budget - target_budget) / target_budget
```
If the sanatorium is cheaper than the target, the deviation is 0 (not a problem). If more expensive, the deviation is proportional to the excess.

**Region** (binary):
```
d_region = 0 if the region matches
d_region = 1 if the region does not match
```

**Tags by category** (proportion of mismatch):
```
d_medical    = 1 - |selected_medical    ∩ sanatorium_medical|    / |selected_medical|
d_services   = 1 - |selected_services   ∩ sanatorium_services|   / |selected_services|
d_conditions = 1 - |selected_conditions ∩ sanatorium_conditions| / |selected_conditions|
```
If the user selected no tags in a category, the deviation is 0.

#### Step 3: Final score

```
score = w_budget * d_budget + w_region * d_region + w_medical * d_medical + w_services * d_services + w_conditions * d_conditions
```

All deviations lie in the range [0, 1], which allows them to be summed without distortion. Sanatoriums are sorted by ascending score.

---

## Getting Started

### With Docker (recommended)

```bash
git clone https://github.com/jareks0iq/sanatorium_selection_service.git
cd sanatorium_selection_service
docker-compose up --build
```

Once running:
- Frontend: http://localhost:3000
- API: http://localhost:5000
- The database is seeded automatically.

### Without Docker

**Requirements:** Python 3.11+, Node.js 18+, PostgreSQL 15+

1. Create a `sanat` database in PostgreSQL.

2. Backend:
```bash
pip install -r requirements.txt
python seed.py
python entrypoints/flask_app.py
```

3. Frontend:
```bash
cd frontend
npm install
npm start
```

---

## Testing

The project has a comprehensive test suite of **35 tests** with **83% coverage**, organized into three levels:

- **Unit tests** — the Goal Programming algorithm and domain models, in full isolation (no database).
- **Integration tests** — repositories tested against a real PostgreSQL database spun up on the fly via **testcontainers**, with per-test isolation.
- **API tests** — endpoints tested end-to-end through the Flask test client.

Run the tests:
```bash
pytest
```

Run with a coverage report:
```bash
pytest --cov=domain --cov=adapters --cov=service_layer --cov=entrypoints --cov-report=term-missing
```

> Integration and API tests require Docker to be running (testcontainers starts a PostgreSQL container automatically).

---

## Code Quality

Code quality is enforced automatically:

- **ruff** — linting and formatting
- **mypy** — static type checking
- **pre-commit** — runs the above checks before every commit

Set up the pre-commit hooks once:
```bash
pre-commit install
```

Run all checks manually:
```bash
ruff check .
ruff format .
mypy domain adapters service_layer entrypoints
pre-commit run --all-files
```

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/tags | All tags |
| GET | /api/sanatoriums/ | All sanatoriums |
| GET | /api/sanatoriums/\<id\> | Sanatorium by ID |
| POST | /api/register | Registration |
| POST | /api/login | Login |
| POST | /api/profile | Create / update profile |
| PUT | /api/password | Change password |
| POST | /api/recommend | Get recommendations (Weighted GP) |
| GET | /api/reviews/\<sanatorium_id\> | Reviews for a sanatorium |
| POST | /api/reviews | Create a review |

---

## Database Schema

**users** — users (id, name, login, password)

**profiles** — profiles with preferences and criterion weights

**sanatoriums** — sanatoriums (name, budget, region, food, rating)

**tags** — tags in three categories: medical, services, conditions

**sanatorium_tags** — many-to-many relation between sanatoriums and tags

**profile_tags** — many-to-many relation between profiles and tags

**reviews** — reviews (user_id, sanatorium_id, text, rating, created_at)

---

## Author

Student at ETU "LETI", Department of Information Systems, group 4374, 2026
