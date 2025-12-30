# Agent Guidelines - Wizardsofts Megabuild

**Version**: 1.0
**Last Updated**: December 30, 2025
**Audience**: AI Agents, Claude Code, GitHub Copilot, Cursor AI

---

## Purpose

This document provides **mandatory guidelines** for all AI agents working on the Wizardsofts Megabuild monorepo. These rules supplement the main [CONSTITUTION.md](CONSTITUTION.md) and must be followed without exception.

---

## 🔐 Authentication & Authorization

### Keycloak SSO - MANDATORY

**CRITICAL RULE**: **Keycloak acts as the central identity provider for ALL administrative interfaces.**

#### Requirements

1. **All admin interfaces MUST use Keycloak for authentication**
   - Grafana → Native OIDC integration
   - Prometheus → Traefik Forward Auth via OAuth2 Proxy
   - Eureka → Traefik Forward Auth via OAuth2 Proxy
   - Traefik Dashboard → Traefik Forward Auth via OAuth2 Proxy
   - Any new admin service → Must integrate before deployment

2. **User Management**
   - Administrative user: `mashfiqur.rahman`
   - Realm: `wizardsofts-admin`
   - Role: `admin` (grants access to all services)

3. **Integration Methods**
   - **Option A** (Preferred): Native OIDC/OAuth2 support
     - Example: Grafana, Keycloak Admin Console
   - **Option B**: Traefik Forward Auth via OAuth2 Proxy
     - Example: Prometheus, Eureka, custom admin panels

4. **Security Requirements**
   - MFA enabled for admin accounts
   - Session timeout: 30 minutes idle
   - Session maximum: 10 hours
   - IP whitelisting: Private networks only (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)

#### Implementation Reference

For detailed implementation steps, see [KEYCLOAK_SSO_INTEGRATION_PLAN.md](KEYCLOAK_SSO_INTEGRATION_PLAN.md)

#### Enforcement

- **Before deploying any admin service**, verify Keycloak integration is complete
- **Before modifying any admin interface**, ensure SSO compatibility is maintained
- **When asked to implement authentication**, always default to Keycloak

---

## 🔒 Security Principles

### Port Binding Rules

1. **Public Access** (0.0.0.0 binding):
   - 22 (SSH)
   - 25 (SMTP)
   - 80 (HTTP/Traefik)
   - 443 (HTTPS/Traefik)
   - Mail ports (465, 587, 993, 995, 143, 110)

2. **Private Network Access** (0.0.0.0 + UFW rules):
   - 3002 (Grafana)
   - 8080 (Traefik Dashboard)
   - 8180 (Keycloak Admin)
   - 8762 (Eureka)
   - 9090 (Prometheus)
   - 4000 (Appwrite Console)

3. **Localhost Only** (127.0.0.1 binding):
   - 8081 (Gateway - internal)
   - 8182-8184 (Business services - internal)
   - 11435 (Ollama - internal)
   - 5433 (PostgreSQL - internal)
   - 6379 (Redis - internal)

### UFW Firewall Configuration & Port Binding

**CRITICAL RULE**: **ALL ports MUST be bound to localhost (127.0.0.1) unless explicitly approved for external access.**

**Port Binding Rules**:

1. **Localhost ONLY** (127.0.0.1 binding - DEFAULT):
   - PostgreSQL (5433)
   - Redis (6379)
   - API Gateway (8081)
   - Business services (8182-8184)
   - ML services (5001-5004)
   - Ollama (11435)
   - Web apps (3000-3001) - access via Traefik only

2. **Private Network** (0.0.0.0 + UFW firewall - REQUIRES APPROVAL):
   - Admin interfaces: Grafana, Prometheus, Eureka, Keycloak
   - Must have UFW rules restricting to private IPs

3. **Public Internet** (0.0.0.0 - REQUIRES STRONG JUSTIFICATION):
   - Only: HTTP/HTTPS (80/443), SSH (22), Mail ports
   - Everything else is denied by default

**UFW Configuration Template**:
```bash
# For admin interfaces that need private network access
ufw allow from 10.0.0.0/8 to any port <PORT> comment "<Service Name>"
ufw allow from 172.16.0.0/12 to any port <PORT>
ufw allow from 192.168.0.0/16 to any port <PORT>

# Example: Keycloak Admin
ufw allow from 10.0.0.0/8 to any port 8180 comment "Keycloak Admin"
ufw allow from 172.16.0.0/12 to any port 8180
ufw allow from 192.168.0.0/16 to any port 8180

# Always verify
ufw status numbered
```

**Docker Compose Examples**:
```yaml
# ❌ WRONG - Database exposed to internet
ports:
  - "5433:5432"

# ✅ CORRECT - Database bound to localhost
ports:
  - "127.0.0.1:5433:5432"
```

**Before Creating Any Service**:
- Ask: "Does this service need external access?"
- Default answer: NO → bind to 127.0.0.1
- If YES: Justify and add UFW rules

---

## 🚀 Deployment Standards

### CI/CD Pipeline - STRICTLY ENFORCED

**CRITICAL RULE**: **SSH-based Docker deployments are ABSOLUTELY FORBIDDEN. ALL deployments MUST use GitLab CI/CD.**

**NEVER DO** (Violations will be rejected):
- ❌ **NEVER** use SSH to access production servers for docker operations
- ❌ **NEVER** run `docker-compose up/down/restart/build` on production via SSH
- ❌ **NEVER** manually deploy services via SSH (except for fixing CI/CD itself)
- ❌ **NEVER** bypass CI/CD for "quick fixes" or "urgent deploys"
- ❌ **NEVER** deploy without running automated tests
- ❌ **NEVER** suggest SSH deployment to users
- ❌ **NEVER** write scripts that deploy via SSH

**ALWAYS DO** (Required workflow):
- ✅ **ALWAYS** commit and push changes to GitLab repository
- ✅ **ALWAYS** let CI/CD pipeline automatically build and test
- ✅ **ALWAYS** trigger deployments from GitLab UI (manual trigger button)
- ✅ **ALWAYS** monitor pipeline execution in GitLab
- ✅ **ALWAYS** verify health checks pass after deployment
- ✅ **ALWAYS** use GitLab rollback job if issues occur
- ✅ **ALWAYS** inform users about CI/CD deployment process

**Correct Deployment Flow**:
1. Make code changes locally
2. Commit and push to GitLab: `git push origin master`
3. Navigate to GitLab: http://10.0.0.80/wizardsofts/wizardsofts-megabuild
4. Go to CI/CD → Pipelines
5. Wait for automatic build and test stages
6. Click "Run Pipeline" → Select "deploy" job → Trigger manually
7. Monitor logs and verify deployment success

**Only Exception**: SSH is permitted ONLY for:
- Emergency rollback when CI/CD is completely down
- Debugging CI/CD pipeline failures
- Server-level infrastructure maintenance (UFW, networking)
- Fixing the CI/CD system itself

### Deployment Checklist

Before marking any deployment task as complete:
- [ ] All tests passing
- [ ] Health checks returning 200 OK
- [ ] Services accessible via DNS
- [ ] Admin interfaces protected by Keycloak SSO
- [ ] **HTTPS/SSL verification**: Certificate valid and secure connection working
- [ ] Logs show no errors
- [ ] Metrics being collected (if Prometheus enabled)

#### HTTPS/SSL Verification Steps

**CRITICAL**: After every web application deployment, MUST verify HTTPS is working correctly:

```bash
# 1. Check certificate validity
openssl s_client -connect www.wizardsofts.com:443 -servername www.wizardsofts.com 2>/dev/null | openssl x509 -noout -dates

# 2. Verify HTTPS connection (should NOT show "not secure")
curl -I https://www.wizardsofts.com 2>&1 | grep -E "HTTP|SSL"

# 3. Check certificate issuer (should be Let's Encrypt or valid CA)
openssl s_client -connect www.wizardsofts.com:443 -servername www.wizardsofts.com 2>/dev/null | openssl x509 -noout -issuer

# 4. Test all deployed routes
curl -I https://www.wizardsofts.com/bondwala
curl -I https://www.gibd.wizardsofts.com
curl -I https://www.padmafoods.com
```

**Common Issues**:
- **Self-signed certificate**: Traefik Let's Encrypt not configured or domain not resolving
- **Certificate expired**: Let's Encrypt renewal failed
- **Mixed content warnings**: Some assets loading over HTTP instead of HTTPS
- **Wrong domain in certificate**: SNI configuration issue in Traefik

**Fix Process**:
1. Check Traefik configuration for Let's Encrypt settings
2. Verify domain DNS resolves to correct IP address
3. Check Traefik logs: `docker logs traefik 2>&1 | grep -i "acme\|certificate"`
4. Ensure ports 80 and 443 are accessible for ACME challenge
5. Force certificate renewal if needed: Delete Traefik acme.json and restart

---

## 📚 Documentation Requirements

### When Creating New Services

1. **Update CONSTITUTION.md**:
   - Add port assignment
   - Document profile membership
   - Add to service inventory

2. **Create Service README.md**:
   - Service description
   - Tech stack
   - Port assignments
   - Environment variables
   - API endpoints
   - Testing instructions

3. **Update Architecture Docs**:
   - Add service to architecture diagram
   - Document dependencies
   - Update deployment guide

4. **Keycloak Integration**:
   - Document OAuth client configuration
   - Update KEYCLOAK_SSO_INTEGRATION_PLAN.md
   - Add testing instructions

---

## 🧪 Testing Standards

### Before Committing Code

**Python**:
```bash
black src/
isort src/
flake8 src/
mypy src/
pytest tests/ --cov=src
```

**TypeScript**:
```bash
npm run lint
npm run format
npm run test
```

**Java**:
```bash
mvn checkstyle:check
mvn test
```

### Minimum Coverage

- Unit tests: 70%
- Critical paths: 90%
- Integration tests: Required for all API endpoints

---

## 🤖 AI Agent Behavior

### When Asked to Implement Features

1. **Always check the constitution first**
   - Read CONSTITUTION.md
   - Check existing patterns in codebase
   - Follow established conventions

2. **Ask clarifying questions**
   - If requirements are ambiguous
   - If multiple approaches are valid
   - If security implications exist

3. **Use AskUserQuestion tool**
   - Present options clearly
   - Explain trade-offs
   - Get explicit approval before major changes

### When Asked About Authentication

**Always default to Keycloak**:
- "How do I add authentication?" → Keycloak SSO
- "Can I use basic auth?" → No, use Keycloak SSO
- "What about API keys?" → For service-to-service only, admin = Keycloak
- "How do users log in?" → Through Keycloak

### When Encountering Conflicts

1. **Constitution takes precedence** over ad-hoc requests
2. **Security standards are non-negotiable**
3. **If user requests violate constitution**, politely explain the conflict and offer compliant alternatives

---

## 🛠️ Common Tasks & Patterns

### Adding a New Admin Service

1. Create service in `apps/<service-name>/`
2. Add health check endpoint
3. Configure Traefik labels (if public-facing)
4. **Integrate with Keycloak** (either native OIDC or OAuth2 Proxy)
5. Add to docker-compose with appropriate profile
6. Update CONSTITUTION.md port assignments
7. Test Keycloak SSO login
8. Add to CI/CD pipeline
9. Deploy via CI/CD (not manual SSH)

### Modifying Existing Services

1. Read existing configuration
2. Understand dependencies
3. Preserve Keycloak integration
4. Update tests
5. Update documentation
6. Deploy via CI/CD

---

## ⚠️ Red Flags - Stop and Ask

**STOP IMMEDIATELY** and ask the user if:
- You're about to commit secrets, API keys, or passwords
- You're being asked to deploy via SSH instead of CI/CD
- You're being asked to run docker-compose commands on production
- You're modifying production services directly via SSH
- You're implementing custom auth (instead of Keycloak)
- You're exposing admin interfaces without authentication
- You're binding services to 0.0.0.0 without localhost or UFW protection
- You're exposing databases (PostgreSQL/Redis) to 0.0.0.0
- You're skipping tests or bypassing CI/CD
- You're making breaking API changes without documentation

**REJECT IMMEDIATELY** (Don't even ask):
- Requests to SSH into production for docker deployments
- Requests to bypass CI/CD "just this once"
- Requests to bind PostgreSQL/Redis to 0.0.0.0
- Requests to commit .env files with real credentials
- Requests to disable security features for "convenience"

---

## 📖 Reference Documents

Required reading for all agents:
- [CONSTITUTION.md](CONSTITUTION.md) - Main project standards
- [KEYCLOAK_SSO_INTEGRATION_PLAN.md](KEYCLOAK_SSO_INTEGRATION_PLAN.md) - SSO implementation guide
- [PHASE_3_CICD_PROGRESS.md](PHASE_3_CICD_PROGRESS.md) - CI/CD setup status
- [IMPLEMENTATION_PROGRESS_REPORT.md](IMPLEMENTATION_PROGRESS_REPORT.md) - Security implementation

---

## 🎯 Summary: The Golden Rules

1. **NEVER use SSH for Docker deployments** - CI/CD only, zero exceptions
2. **NEVER bypass CI/CD pipeline** - No "quick fixes" or manual deploys
3. **ALWAYS bind to localhost** - Unless explicitly approved with UFW rules
4. **Keycloak for all admin auth** - No custom auth, no exceptions
5. **Constitution compliance** - Check CONSTITUTION.md before implementing
6. **Security first** - Never compromise security for convenience
7. **Document everything** - Update docs with every change
8. **Test before commit** - All tests must pass
9. **Ask when uncertain** - Better to clarify than break production

**Remember**: If you're unsure whether something violates these rules, it probably does. Ask first.

---

**Last Updated**: December 30, 2025
**Maintained By**: Wizardsofts Engineering Team
**For Questions**: Refer to CONSTITUTION.md or ask the user
