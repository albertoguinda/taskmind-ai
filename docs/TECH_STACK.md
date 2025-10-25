# TaskMind AI - Technology Stack

## Backend Core

| Technology            | Version | Purpose        | Why?                                    |
| --------------------- | ------- | -------------- | --------------------------------------- |
| Python                | 3.11    | Language       | Latest stable, performance improvements |
| Django                | 4.2 LTS | Framework      | Long-term support, mature ecosystem     |
| Django REST Framework | 3.14    | API            | Industry standard for REST APIs         |
| PostgreSQL            | 15      | Database       | JSONB support, reliability              |
| Redis                 | 7.2     | Cache/Sessions | In-memory speed, pub/sub support        |

## AI/ML Stack

| Technology            | Version | Purpose    | Why?                      |
| --------------------- | ------- | ---------- | ------------------------- |
| Transformers          | 4.35    | NLP Models | Hugging Face ecosystem    |
| PyTorch               | 2.1     | ML Backend | Required for transformers |
| sentence-transformers | 2.2     | Embeddings | Semantic similarity       |

**Selected Models:**

- **Classification:** `facebook/bart-large-mnli` (zero-shot classification)
- **Embeddings:** `all-MiniLM-L6-v2` (sentence similarity)
- **Sentiment:** `distilbert-base-uncased-finetuned-sst-2-english`

**Why not OpenAI/Anthropic?**

- Cost: $0 vs $0.001-0.03 per request
- Privacy: Data stays local
- Latency: No network calls
- Interview: Shows deeper technical skills

## Async Processing

| Technology | Version | Purpose        | Why?                         |
| ---------- | ------- | -------------- | ---------------------------- |
| Celery     | 5.3     | Task Queue     | Django integration, mature   |
| RabbitMQ   | 3.12    | Message Broker | Reliable, clustering support |

**Alternative considered:** Redis as broker (rejected: less reliable for critical tasks)

## DevOps & Infrastructure

| Technology     | Version         | Purpose          | Why?                          |
| -------------- | --------------- | ---------------- | ----------------------------- |
| Docker         | 24.0            | Containerization | Environment consistency       |
| Docker Compose | 2.23            | Orchestration    | Easy local development        |
| Gunicorn       | 21.2            | WSGI Server      | Production-ready              |
| Nginx          | 1.25 (optional) | Reverse Proxy    | Static files, SSL termination |

## Development Tools

| Technology    | Version | Purpose        | Why?                 |
| ------------- | ------- | -------------- | -------------------- |
| pytest        | 7.4     | Testing        | Superior to unittest |
| pytest-django | 4.7     | Django testing | DRF integration      |
| pytest-cov    | 4.1     | Coverage       | Code quality metrics |
| black         | 23.11   | Formatting     | PEP 8 compliance     |
| flake8        | 6.1     | Linting        | Style enforcement    |
| mypy          | 1.7     | Type Checking  | Static analysis      |
| pre-commit    | 3.5     | Git Hooks      | Quality gates        |

## CI/CD

| Technology     | Purpose          | Why?                              |
| -------------- | ---------------- | --------------------------------- |
| GitHub Actions | CI/CD            | Free for public repos, easy setup |
| Codecov        | Coverage Reports | Visual feedback                   |

## Monitoring & Observability (Nice-to-have)

| Technology           | Purpose        | Why?                               |
| -------------------- | -------------- | ---------------------------------- |
| Sentry               | Error Tracking | Free tier, easy Django integration |
| Django Debug Toolbar | Development    | Performance insights               |

## Package Management

````toml
pyproject.toml (modern approach)
[project]
name = "taskmind-ai"
version = "0.1.0"
requires-python = ">=3.11"[tool.poetry]  # or pip-tools

## Architecture Patterns
- **Clean Architecture** (hexagonal ports & adapters)
- **Repository Pattern** (data access abstraction)
- **Dependency Injection** (constructor injection)
- **CQRS Light** (separate read/write operations)
- **Domain-Driven Design** (light version)

## File Structure Conventiontaskmind/
├── apps/                    # Django apps (bounded contexts)
│   ├── tasks/              # Task management domain
│   └── ai_engine/          # AI analysis domain
├── config/                  # Django settings
├── shared/                  # Shared kernel (cross-domain)
├── tests/                   # Test suites
└── docs/                    # Documentation

## Database Schema (Simplified)
```sql-- Task table (PostgreSQL)
CREATE TABLE tasks (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
title VARCHAR(200) NOT NULL,
description TEXT,
priority VARCHAR(20) DEFAULT 'MEDIUM',
urgency_score FLOAT,  -- AI-generated 0-1
status VARCHAR(20) DEFAULT 'TODO',
ai_keywords JSONB,    -- ["backend", "urgent", "bug"]
metadata JSONB,       -- Flexible field
created_at TIMESTAMP DEFAULT NOW(),
updated_at TIMESTAMP DEFAULT NOW()
);CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_urgency_score ON tasks(urgency_score DESC);
CREATE INDEX idx_tasks_ai_keywords ON tasks USING GIN(ai_keywords);

## API Design Principles
- RESTful conventions
- HATEOAS links (optional)
- Pagination: limit/offset + cursor
- Filtering: Django Filter Backend
- Versioning: URL-based (`/api/v1/`)
- Authentication: JWT (future)

## Performance Considerations
- **Database:** Connection pooling (pgBouncer future)
- **Caching:** Redis for hot data (task lists)
- **AI:** Model loaded once at startup (singleton)
- **Async:** Celery for >1s operations
- **Serialization:** orjson for speed (optional)

## Security (Production-Ready)
- Environment variables (never commit secrets)
- CORS configured properly
- SQL injection: ORM prevents
- XSS: DRF serializers escape
- CSRF: Django middleware
- Rate limiting: django-ratelimit

## What We're NOT Using (and why)
| Technology | Why Not? |
|------------|----------|
| MongoDB | PostgreSQL JSONB covers our needs |
| GraphQL | REST is simpler for this scope |
| FastAPI | Django ecosystem + ORM wins here |
| Microservices | Overkill for demo, adds complexity |
| Kubernetes | Docker Compose sufficient |
| Terraform | Local deployment only |
````
