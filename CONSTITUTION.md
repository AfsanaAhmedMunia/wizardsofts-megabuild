# Wizardsofts Megabuild Constitution

**Version**: 1.0
**Last Updated**: December 27, 2025
**Status**: Official Standard

---

## 📜 Purpose

This constitution establishes the foundational rules, standards, and guidelines that **ALL agents, developers, and contributors** must follow when working on the Wizardsofts Megabuild monorepo.

**Compliance is Mandatory**: Any code, service, or documentation that does not adhere to this constitution will be rejected.

---

## 🏗️ Tech Stack Standards

### Frontend Applications

| Technology | Version | Use Case | Mandatory |
|------------|---------|----------|-----------|
| **Next.js** | 14+ | All web applications | ✅ Yes |
| **React** | 19+ | UI components | ✅ Yes |
| **TypeScript** | 5+ | Type safety | ✅ Yes |
| **Tailwind CSS** | 4+ | Styling | ✅ Yes |
| **ESLint** | 9+ | Code linting | ✅ Yes |
| **Prettier** | 3+ | Code formatting | ✅ Yes |

**Package Manager**: npm (with `--legacy-peer-deps` if needed)

**Build Output**: Standalone (for Docker deployment)

```javascript
// next.config.js
module.exports = {
  output: 'standalone',  // Required for Docker
}
```

---

### Backend Services (Spring Boot)

| Technology | Version | Use Case | Mandatory |
|------------|---------|----------|-----------|
| **Spring Boot** | 3.4+ | Java microservices | ✅ Yes |
| **Spring Cloud** | 2024.0+ | Service discovery, gateway | ✅ Yes |
| **Java** | 17+ | Programming language | ✅ Yes |
| **Maven** | 3.9+ | Build tool | ✅ Yes |
| **PostgreSQL Driver** | Latest | Database connectivity | ✅ Yes |

**Base Image**: `eclipse-temurin:17-jre-alpine`

---

### Backend Services (Python ML/FastAPI)

| Technology | Version | Use Case | Mandatory |
|------------|---------|----------|-----------|
| **Python** | 3.11+ | Programming language | ✅ Yes |
| **FastAPI** | Latest | REST APIs | ✅ Yes |
| **uv** | Latest | Package management | ✅ Yes |
| **Pydantic** | 2+ | Data validation | ✅ Yes |
| **SQLAlchemy** | 2+ | ORM | ✅ Yes |
| **Pandas** | Latest | Data analysis | ✅ Yes |

**Base Image**: `ghcr.io/astral-sh/uv:python3.11-bookworm` or `python:3.11-slim`

**Package Management**: Use `uv` for dependency management

---

### Infrastructure Services

| Service | Version | Purpose | Required |
|---------|---------|---------|----------|
| **Traefik** | 2.10+ | Reverse proxy, SSL | ✅ Yes |
| **PostgreSQL** | 15-alpine | Database | ✅ Yes |
| **Redis** | 7-alpine | Cache, queue | ✅ Yes |
| **Eureka** | 2024.0+ | Service discovery | ✅ Yes (for Java) |
| **Prometheus** | Latest | Metrics | ⚠️ Optional |
| **Grafana** | Latest | Dashboards | ⚠️ Optional |
| **Keycloak** | 23+ | Authentication | ⚠️ Optional |
| **GitLab** | Latest | CI/CD | ⚠️ Optional |

---

## 🔢 Port Allocation Standards

### Reserved Port Ranges

| Range | Purpose | Example Services |
|-------|---------|------------------|
| **3000-3099** | Frontend Applications | Web apps |
| **5000-5099** | Python FastAPI Services | ML/AI services |
| **8000-8099** | Miscellaneous HTTP Services | Custom APIs |
| **8080-8199** | Spring Boot Services | Gateway, APIs |
| **8200-8299** | Infrastructure HTTP | - |
| **5432-5433** | PostgreSQL | Database |
| **6379** | Redis | Cache/Queue |
| **9000-9099** | Monitoring/Metrics | Prometheus |
| **11434** | AI Services | Ollama |

---

### Assigned Ports (DO NOT CHANGE)

#### Frontend Applications (3000-3099)

| Port | Service | Profile | Description |
|------|---------|---------|-------------|
| **3000** | ws-wizardsofts-web | web-apps | Corporate website |
| **3001** | gibd-quant-web | gibd-quant | Quant-Flow frontend |
| **3002** | ws-daily-deen-web | web-apps | Daily Deen Guide |

#### Python ML Services (5000-5099)

| Port | Service | Profile | Description |
|------|---------|---------|-------------|
| **5001** | gibd-quant-signal | gibd-quant | Signal generation |
| **5002** | gibd-quant-nlq | gibd-quant | Natural language queries |
| **5003** | gibd-quant-calibration | gibd-quant | Stock calibration |
| **5004** | gibd-quant-agent | gibd-quant | LangGraph agents |

#### Spring Boot Services (8080-8199)

| Port | Service | Profile | Description |
|------|---------|---------|-------------|
| **8080** | ws-gateway | shared | API Gateway |
| **8182** | ws-trades | shared | Trades API |
| **8183** | ws-company | shared | Company Info API |
| **8184** | ws-news | shared | News API |

#### Service Discovery (8200-8299)

| Port | Service | Profile | Description |
|------|---------|---------|-------------|
| **8762** | ws-discovery | shared | Eureka (was 8761, changed due to conflict) |

#### Database & Cache

| Port | Service | Profile | Description |
|------|---------|---------|-------------|
| **5433** | postgres | shared | PostgreSQL (was 5432, changed due to host conflict) |
| **6379** | redis | shared | Redis |

---

### Port Conflict Resolution Rules

1. **Check Host Ports First**: Before assigning a port, verify it's not in use:
   ```bash
   lsof -i :<port>
   ```

2. **Use Alternative Ports**: If the default port is taken, use next available in range:
   - Postgres: 5432 → 5433 (done)
   - Eureka: 8761 → 8762 (done)

3. **Document Changes**: Update this constitution when ports change

4. **Container Ports Stay Same**: Only host ports change
   ```yaml
   ports:
     - "5433:5432"  # host:container
   ```

---

## 🐳 Docker Standards

### Dockerfile Requirements

**All services MUST have**:

1. **Multi-stage builds** (deps → builder → runner)
2. **Health checks** using `wget` (NOT `curl`)
3. **Non-root user** in final image
4. **Minimal base image** (alpine preferred)
5. **Proper .dockerignore**

**Example Health Check**:
```yaml
healthcheck:
  test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
  interval: 30s
  timeout: 10s
  retries: 5
```

**Why wget?**: Alpine images don't include curl by default. Using wget prevents "command not found" errors in health checks.

---

### Docker Compose Standards

**Profile Requirements**:

| Profile | Purpose | Services |
|---------|---------|----------|
| **shared** | Infrastructure + Shared APIs | postgres, redis, eureka, gateway, trades, company, news |
| **gibd-quant** | ML Services | All shared + signal, nlq, calibration, agent, celery, quant-web |
| **web-apps** | Corporate Websites | wizardsofts-web, daily-deen-web |
| **all** | Complete Deployment | Everything |

**Service Naming Convention**:
- Spring Boot: `ws-<service-name>` (e.g., ws-gateway, ws-trades)
- Python ML: `gibd-quant-<service-name>` (e.g., gibd-quant-signal)
- Web Apps: `ws-<domain>-web` (e.g., ws-wizardsofts-web)

**Container Naming**:
```yaml
services:
  ws-gateway:
    container_name: ws-gateway  # Must match service name
```

---

### Traefik Label Standards

**All public-facing services MUST include**:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.<service-name>.rule=Host(`<domain>`)"
  - "traefik.http.routers.<service-name>.entrypoints=websecure"
  - "traefik.http.routers.<service-name>.tls.certresolver=letsencrypt"
  - "traefik.http.services.<service-name>.loadbalancer.server.port=<port>"
```

**Example**:
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.wizardsofts-web.rule=Host(`www.wizardsofts.com`)"
  - "traefik.http.routers.wizardsofts-web.entrypoints=websecure"
  - "traefik.http.routers.wizardsofts-web.tls.certresolver=letsencrypt"
  - "traefik.http.services.wizardsofts-web.loadbalancer.server.port=3000"
```

---

## 🧪 Testing Standards

### Unit Tests

**Coverage Requirements**:
- Minimum: 70% code coverage
- Critical paths: 90%+ coverage

**Naming Convention**:
```
tests/unit/test_<module_name>.py          # Python
tests/unit/<component>.test.tsx           # TypeScript/React
src/test/java/.../ComponentTest.java      # Java
```

**Python Testing**:
```bash
# Must use pytest
pytest tests/unit/ --cov=src --cov-report=xml
```

**TypeScript Testing**:
```bash
# Must use Jest
npm run test
```

**Java Testing**:
```bash
# Must use JUnit
mvn test
```

---

### Integration Tests

**Location**: `tests/integration/`

**Requirements**:
- Test service-to-service communication
- Test database interactions
- Test external API integrations

**Run Before Deployment**:
```bash
pytest tests/integration/
```

---

### E2E Tests

**Location**: `tests/e2e/`

**Tool**: Playwright (via MCP)

**Requirements**:
- Test complete user workflows
- Test across all frontends
- Mobile responsive checks
- Accessibility audits (axe-core)

**Coverage**:
- [ ] Wizardsofts.com: Homepage, navigation, contact form
- [ ] Daily Deen Guide: Prayer times, hadith content
- [ ] Quant-Flow: Signal generation, NLQ queries, company pages

---

### Performance Tests

**Location**: `tests/performance/`

**Tool**: pytest-benchmark

**Requirements**:
- API response times < 200ms (95th percentile)
- Signal generation < 1s per stock
- NLQ queries < 2s

**Run Benchmarks**:
```bash
pytest tests/performance/ --benchmark-only
```

---

## 📖 Documentation Standards

### Code Documentation

**Python (Docstrings)**:
```python
def generate_signal(ticker: str, date: date) -> Signal:
    """
    Generate trading signal for a stock.

    Args:
        ticker: Stock ticker symbol (e.g., 'GP')
        date: Analysis date

    Returns:
        Signal object with type (BUY/SELL/HOLD) and confidence

    Raises:
        ValueError: If ticker not found

    Example:
        >>> signal = generate_signal('GP', date.today())
        >>> print(signal.signal_type)
        'BUY'
    """
```

**TypeScript (JSDoc)**:
```typescript
/**
 * Fetch company data from API
 *
 * @param ticker - Stock ticker symbol
 * @returns Promise with company data
 * @throws Error if API request fails
 *
 * @example
 * const company = await fetchCompany('GP');
 */
async function fetchCompany(ticker: string): Promise<Company> {
  // ...
}
```

**Java (Javadoc)**:
```java
/**
 * Retrieves trade data for a ticker.
 *
 * @param ticker the stock ticker symbol
 * @param startDate the start date for trade data
 * @return list of trade records
 * @throws DataNotFoundException if no data found
 */
public List<Trade> getTrades(String ticker, LocalDate startDate) {
    // ...
}
```

---

### README Requirements

**Every service MUST have a README.md with**:

1. **Service Name & Description**
2. **Tech Stack**
3. **Port Assignment**
4. **Environment Variables**
5. **Local Development Setup**
6. **API Endpoints** (if applicable)
7. **Testing Instructions**
8. **Deployment Instructions**

**Template**:
```markdown
# Service Name

Brief description of what this service does.

## Tech Stack
- Framework: FastAPI 0.109.0
- Language: Python 3.11
- Database: PostgreSQL 15

## Port
- **Development**: 5001
- **Production**: 5001
- **Profile**: gibd-quant

## Environment Variables
```bash
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
```

## Local Development
```bash
cd apps/service-name
uv sync
uv run uvicorn src.main:app --reload --port 5001
```

## API Endpoints
- GET /health - Health check
- POST /api/v1/endpoint - Description

## Testing
```bash
pytest tests/
```
```

---

### Architecture Documentation

**Location**: `docs/`

**Required Documents**:
- `ARCHITECTURE.md` - System architecture overview
- `API_REFERENCE.md` - All API endpoints
- `DATABASE_SCHEMA.md` - Database schema
- `DEPLOYMENT.md` - Deployment guide
- `TROUBLESHOOTING.md` - Common issues

---

## 🔐 Security Standards

### API Security

**All APIs MUST**:
1. Validate input using Pydantic (Python) or Bean Validation (Java)
2. Sanitize user input to prevent injection
3. Use HTTPS in production (via Traefik)
4. Implement rate limiting
5. Log security events

**Never Commit**:
- API keys
- Passwords
- Private keys
- `.env` files with real credentials

**Use**:
- `.env.example` with placeholders
- Environment variables in docker-compose.yml: `${VAR_NAME}`

---

### Database Security

1. **Use connection pooling**
2. **Parameterized queries only** (no string concatenation)
3. **Least privilege principle** for DB users
4. **Encrypt sensitive data** at rest

---

## 🚀 Deployment Standards

### GitLab CI/CD Pipeline

**Stages**:
1. **detect** - Detect changed services
2. **test** - Run tests for changed services
3. **build** - Build Docker images
4. **deploy** - Deploy to production (manual trigger)

**Change Detection**:
- Only build/test changed services
- Rebuild all if `docker-compose.yml` or `.env` changes

**Health Checks**:
- All services must pass health checks before deployment considered successful

---

### Rollback Procedure

**Automated Rollback**:
```bash
# Via GitLab CI/CD
# Trigger rollback job (manual)
```

**Manual Rollback**:
```bash
ssh deploy@10.0.0.84
cd /opt/wizardsofts-megabuild
git reset --hard HEAD~1
docker compose --profile all down
docker compose --profile all build
docker compose --profile all up -d
```

---

## 📊 Monitoring Standards

### Health Checks

**All services MUST expose**:
- `/health` or `/actuator/health` endpoint
- Return 200 OK when healthy
- Return 503 Service Unavailable when unhealthy

**Response Format**:
```json
{
  "status": "UP",
  "checks": {
    "database": "UP",
    "redis": "UP"
  }
}
```

---

### Logging Standards

**Log Levels**:
- **ERROR**: Failures requiring immediate attention
- **WARN**: Potential issues
- **INFO**: Important state changes
- **DEBUG**: Detailed debugging information

**Format** (JSON):
```json
{
  "timestamp": "2025-12-27T12:00:00Z",
  "level": "INFO",
  "service": "gibd-quant-signal",
  "message": "Generated signal for GP",
  "context": {
    "ticker": "GP",
    "signal": "BUY",
    "confidence": 0.75
  }
}
```

**Never Log**:
- Passwords
- API keys
- Personal identifiable information (PII)
- Credit card numbers

---

### Metrics

**Required Metrics** (via Prometheus):
- Request count
- Request duration (histogram)
- Error rate
- Active connections
- Memory usage
- CPU usage

---

## 🔄 Git Workflow Standards

### Branch Naming

| Type | Format | Example |
|------|--------|---------|
| Feature | `feature/<description>` | feature/add-signal-api |
| Bug Fix | `fix/<description>` | fix/health-check-error |
| Hotfix | `hotfix/<description>` | hotfix/security-patch |
| Infrastructure | `infra/<description>` | infra/add-prometheus |
| Documentation | `docs/<description>` | docs/update-readme |

---

### Commit Messages

**Format**:
```
<type>: <subject>

<body>

🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Example**:
```
feat: Add natural language query endpoint

- Added NLQueryEngine with pattern-based parser
- Supports trend, threshold, and ranking queries
- Includes LLM fallback for complex queries

🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

### Pull Request Standards

**Required**:
1. Descriptive title
2. Summary of changes
3. Test plan
4. Screenshots (if UI changes)
5. All CI checks passing
6. No merge conflicts

**Template**:
```markdown
## Summary
Brief description of changes

## Changes
- Added feature X
- Fixed bug Y
- Updated documentation

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots
(if applicable)
```

---

## ⚠️ Breaking Changes Protocol

**When making breaking changes**:

1. **Document in CHANGELOG.md**
2. **Update migration guide**
3. **Notify team in advance**
4. **Provide backwards compatibility period** (if possible)
5. **Update all affected services**

**Example Breaking Change**:
```markdown
## BREAKING CHANGE (v2.0.0)

### Changed: Signal API Response Format

**Before**:
```json
{"signal": "BUY", "score": 0.75}
```

**After**:
```json
{
  "signal_type": "BUY",
  "total_score": 0.75,
  "confidence": 0.85
}
```

**Migration**: Update all API clients to use new field names.
```

---

## 🎯 Code Quality Standards

### Linting

**Python**:
```bash
# Must pass before commit
black src/
isort src/
flake8 src/
mypy src/
```

**TypeScript**:
```bash
# Must pass before commit
npm run lint
npm run format
```

**Java**:
```bash
# Must pass before compile
mvn checkstyle:check
```

---

### Code Review Checklist

**Before Approving PR**:
- [ ] Code follows constitution standards
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No hardcoded secrets
- [ ] Health checks work
- [ ] Docker build succeeds
- [ ] Ports don't conflict
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Logging appropriate level
- [ ] Error handling proper

---

## 🏆 Best Practices

### DRY (Don't Repeat Yourself)

- Extract common code into shared libraries
- Use configuration files for repeated patterns
- Create reusable components

### KISS (Keep It Simple, Stupid)

- Avoid over-engineering
- Prefer simple solutions
- Write readable code over clever code

### SOLID Principles

- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

---

## 📋 Checklist for New Services

When adding a new service:

- [ ] Choose appropriate port from reserved range
- [ ] Update this constitution with port assignment
- [ ] Create service in `apps/<service-name>/`
- [ ] Add Dockerfile with health check
- [ ] Add to appropriate docker-compose profile
- [ ] Add Traefik labels (if public-facing)
- [ ] Create README.md
- [ ] Add unit tests (70%+ coverage)
- [ ] Add integration tests
- [ ] Add to GitLab CI/CD pipeline
- [ ] Update architecture documentation
- [ ] Test locally
- [ ] Deploy to staging
- [ ] Deploy to production

---

## 🔄 Constitution Updates

**This constitution is a living document.**

**To propose changes**:
1. Create PR with updated CONSTITUTION.md
2. Explain rationale in PR description
3. Get team approval
4. Update version number
5. Notify all developers

**Version History**:
- v1.0 (2025-12-27): Initial constitution

---

## ⚖️ Enforcement

**Non-compliance consequences**:
1. PR rejected
2. CI/CD pipeline fails
3. Deployment blocked

**Zero tolerance for**:
- Committing secrets
- Skipping tests
- Ignoring security vulnerabilities
- Breaking production without rollback plan

---

## 📞 Questions?

For clarification on any constitutional standard:
1. Check existing services for examples
2. Consult architecture documentation
3. Ask in team chat
4. Create GitHub issue for constitution amendments

---

**Last Updated**: December 27, 2025
**Maintained By**: Wizardsofts Engineering Team
**Next Review**: Quarterly
