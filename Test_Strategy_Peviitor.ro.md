# Test Strategy — peviitor.ro

> **Project**: peviitor.ro — open source job search engine for Romania
> **Author**: Boga Sebastian-Nicolae
> **Date**: June 2026
> **Version**: 15.0

### Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **Reviewed By** | | | |
| Project Manager | Diana Dragoi | ___________________________ | ___/___/2026 |
| QA Lead | Ana-Maria Talmacel | ___________________________ | ___/___/2026 |
| **Approved By** | | | |
| Product Owner | Boga Sebastian-Nicolae | ___________________________ | ___/___/2026 |

---

## 1. SCOPE

### 1.1 Purpose of the Document

This document defines the test strategy for the **peviitor.ro** platform — the open source job search engine for Romania. A core strategic principle is that the platform is built exclusively with **open source and free technologies**, and this commitment is not subject to change. Its purpose is to establish a unified testing approach covering all major platform components, from front-end to the indexing infrastructure, with the following scope objectives for each area:

**Apache SOLR**
- Upgrade to the latest stable version
- Maintain two dedicated cores: `job` and `company`
- Ensure the SOLR schema matches the Job and Company models defined in peviitor_core
- Guarantee data consistency — no orphaned fields, no missing mandatory fields from the job or company model
- Implement Basic Authentication as a security layer

**PHP API (api.peviitor.ro)**
- Maintain two versions: **v0** for development and testing, **v1** for production
- Keep the codebase simple, fast, and easy to maintain
- Ensure the code is easily deployable
- Ensure the code is testable
- Eliminate security vulnerabilities
- Secure all API endpoints

**UI (search-engine)**
- Keep the UI simple to write and maintain
- Ensure the UI conforms to the UX Design (Figma)
- Host the UI on GitHub Pages
- Ensure the UI remains accessible even if the BFF PHP API is down (graceful degradation)

**Search Functionality**
- Make the search interface easy to use
- Deliver relevant search results
- Provide useful filters for users (location, company, tags, work mode)

### 1.2 Objectives

- Ensure the quality of aggregated data (jobs, companies)
- Validate search engine functionality (SOLR)
- Confirm the correctness of the REST API (api.peviitor.ro)
- Verify the user experience in the web interface (search-engine)
- Identify defects early through manual and automated testing
- Ensure availability and performance on the existing infrastructure (Raspberry Pi 5, CloudFlare)

### 1.3 Components in Scope

| Component | Technology | Role |
|-----------|-----------|------|
| Frontend (search-engine) | React 18, Redux Toolkit, Vite, Tailwind CSS | User interface for searching and displaying jobs |
| API (api.peviitor.ro) | PHP (v0-v6) | REST API wrapper over SOLR, search and filter endpoints |
| Core (peviitor_core) | PHP, Shell, Docker | SOLR indexing, data validation, workflows (scraped → verified → published) |
| Apache SOLR | SOLR (Raspberry Pi 5) | Full-text search engine, jobs/companies schemas, Romanian diacritics support |
| Validator (admin.peviitor.ro) | JavaScript, Docker | Manual job validation |
| Scrapers | Python, JavaScript, Scrapy, JMeter | Automated job collection from 700+ companies |

> **Note**: Mobile application testing (androidAPP) is **not** covered in this document. A separate test strategy will be created for mobile testing.

### 1.4 Out of Scope

- Individual scraper testing (each scraper is handled separately by the scraping teams)

### 1.5 Quality Benefits Targeted

- **Performance**: Response times < 2s for searches, daily indexing
- **Reliability**: Correct data, no dead links, expired jobs automatically removed
- **Disaster Recovery**: SOLR index backup and restoration
- **Scalability**: Ability to aggregate 40,000+ jobs updated daily
- **Validity**: Compliance with the data schema (Job Model, Company Model)

### 1.6 GitHub Repositories

| Component | Repository | URL |
|-----------|-----------|-----|
| Frontend | search-engine | [github.com/peviitor-ro/search-engine](https://github.com/peviitor-ro/search-engine) |
| API | api.peviitor.ro | [github.com/peviitor-ro/api.peviitor.ro](https://github.com/peviitor-ro/api.peviitor.ro) |
| Core (indexing, schemas, workflows) | peviitor_core | [github.com/peviitor-ro/peviitor_core](https://github.com/peviitor-ro/peviitor_core) |
| Validator | admin.peviitor.ro | [github.com/peviitor-ro/admin.peviitor.ro](https://github.com/peviitor-ro/admin.peviitor.ro) |
| Mobile app (separate strategy) | androidAPP | [github.com/peviitor-ro/androidAPP](https://github.com/peviitor-ro/androidAPP) |
| Scrapers frontend | frontend | [github.com/peviitor-ro/frontend](https://github.com/peviitor-ro/frontend) |
| Scrapers scraping | scraping | [github.com/peviitor-ro/scraping](https://github.com/peviitor-ro/scraping) |
| Local dev environment | local_environment | [github.com/peviitor-ro/local_environment](https://github.com/peviitor-ro/local_environment) |
| Landing page | landing-page | [github.com/peviitor-ro/landing-page](https://github.com/peviitor-ro/landing-page) |
| Documentation | documentation | [github.com/peviitor-ro/documentation](https://github.com/peviitor-ro/documentation) |
| DevOps / hosting | devops | [github.com/peviitor-ro/devops](https://github.com/peviitor-ro/devops) |

> **Note**: This strategy covers the components in **scope** from 1.3. Repositories listed here for scrapers, mobile app, landing page, documentation, and devops are kept for reference but their individual testing is outside this document's scope.

### 2.1 Frontend Testing (search-engine)

| Area | Approach |
|------|----------|
| **Functional Testing** | Verify search flow: input query → API call → display results; filter by location, company, tags, work mode; pagination; empty states; error states |
| **UI / Visual Testing** | Layout consistency, responsive design (mobile/tablet/desktop), Tailwind CSS classes, component rendering with React |
| **Regression Testing** | Run on each release (~weekly), verify critical paths (search, filter, company page, job detail) |
| **Cross-browser Testing** | Chrome, Firefox, Edge, Safari — latest 2 versions |
| **Tools** | Manual exploratory, Chrome DevTools, React DevTools, Sentry for error monitoring |

### 2.2 API Testing (api.peviitor.ro)

| Area | Approach |
|------|----------|
| **Endpoint Validation** | Verify all REST endpoints (v0-v6): search, firme, stats; correct HTTP methods, headers, status codes |
| **Query Parameters** | Test `q`, `location`, `company`, `tags`, `workmode`, `page`, `limit` — valid, invalid, empty, boundary |
| **Error Handling** | 400 Bad Request, 404 Not Found, 500 Server Error — proper error messages and HTTP codes |
| **SOLR Proxy Behavior** | Verify API correctly proxies requests to SOLR; handle SOLR timeout/offline gracefully |
| **Tools** | Postman, Bruno, REST Client, automated scripts (PHPUnit where applicable) |

### 2.3 SOLR Indexing Testing

| Area | Approach |
|------|----------|
| **Schema Compliance** | Validate Job Model fields (url, title, company, location, tags, workmode, salary, etc.) against SOLR schema |
| **Diacritics Search** | Romanian diacritics: search "București" → matches "Bucuresti" and vice versa |
| **Full-text Search** | Verify relevance scoring, partial matches, phrase matching |
| **Facet Search** | Verify faceted counts by location, company, workmode, tags |
| **CRUD Operations** | Index, update, delete documents; verify atomic updates, expiration cleanup (daily @ 02:00) |
| **URL Validation Pipeline** | Verify daily @ 06:00: HEAD requests, 404 deletion, expired content detection |
| **Tools** | SOLR Admin UI, curl, PHP scripts from peviitor_core |

### 2.4 Data Validation Testing

| Area | Approach |
|------|----------|
| **Job Status Flow** | Verify `scraped` → `tested` / `verified` → `published` transitions |
| **Field Validation** | Required fields (url, title), formats (url, date ISO8601, salary format), max length (title ≤ 200 chars) |
| **Company Matching** | `company` field must match Company.name (case insensitive, diacritics accepted) |
| **Expiration Logic** | `expirationdate` = vdate + 30 days max; expired jobs deleted automatically |
| **Duplicate Detection** | `url` must be unique; reject duplicate entries |
| **Tools** | Manual via admin.peviitor.ro, automated scripts in peviitor_core/tests |

### 2.5 Cross-Component Integration

| Area | Approach |
|------|----------|
| **Frontend ↔ API** | Verify search results match API responses, filters translate to correct query params, pagination works end-to-end |
| **API ↔ SOLR** | Verify API correctly queries SOLR, returns results in expected JSON format |
| **Scrapers ↔ SOLR** | Verify scraped data reaches SOLR with correct fields and status |
| **Validator ↔ Core** | Verify admin.peviitor.ro status changes propagate to SOLR index |
| **Tools** | End-to-end manual tests, Postman collections, integration test scripts |

### 2.6 Non-Functional Requirements (NFRs)

#### 2.6.1 Performance Testing

- **Search Response Time**: P95 < 2s for standard queries, P99 < 5s for complex faceted queries
- **Indexing Throughput**: 40,000+ jobs indexed/updated daily within batch window
- **Concurrent Users**: Support 50+ simultaneous users on Raspberry Pi 5 infrastructure
- **API Latency**: P95 < 500ms for API-only endpoints (excluding network)
- **Tools**: Lighthouse, Chrome DevTools Performance tab, k6 (planned), SOLR query timing
- **Frequency**: Quarterly and before major releases

#### 2.6.2 Security Testing

- **OWASP Top 10**: Verify application against the [OWASP Top 10](https://owasp.org/www-project-top-ten/) web application security risks (broken access control, XSS, SQL injection, etc.)
- **SOLR Authentication**: Verify basic auth is enabled on solr.peviitor.ro (see `008_enable_solr_basic_auth_pi.sh`)
- **API Input Sanitization**: Verify SQL injection / XSS attempts are rejected
- **CORS Headers**: Verify proper CORS configuration on API
- **Sentry Error Monitoring**: No sensitive data leaked in error logs
- **GitHub Secret Scanning**: Automatically detects accidental commits of credentials, API keys, tokens, and other secrets across all repositories in the peviitor-ro organization. Alerts are sent to repository admins.
- **GitHub Code Scanning (CWE)**: Uses CodeQL to analyze code for security vulnerabilities mapped to Common Weakness Enumeration (CWE). Runs on every push and pull request. Results appear in the Security tab of each repository.
- **Dependabot**: Automated dependency monitoring that checks all libraries and packages for known vulnerabilities. Creates pull requests to update vulnerable dependencies to the latest patched version. Configured via `dependabot.yml` in each repository.
- **Tools**: Manual testing, OWASP ZAP (planned), browser DevTools, GitHub Security tab, Dependabot alerts
- **Frequency**: Bi-annually and after infrastructure changes; automated scanning runs on every push/PR via GitHub

#### 2.6.3 Accessibility Testing

- **WCAG Compliance**: Target [WCAG 2.2 Level AA](https://www.w3.org/TR/WCAG22/) — the current W3C Recommendation (October 2023) and the most widely adopted legal standard globally
- **Keyboard Navigation**: All functionality accessible via keyboard (Tab, Enter, Escape, arrow keys)
- **Screen Reader**: Proper ARIA labels, semantic HTML, alt text on images
- **Color Contrast**: Minimum 4.5:1 contrast ratio for normal text
- **Tools**: axe DevTools, Lighthouse Accessibility audit, WAVE, manual keyboard testing
- **Frequency**: Per release and during UI changes

#### 2.6.4 Usability Testing

- **Search Flow**: Intuitive search, clear filters, easy job detail access
- **Mobile Experience**: Touch-friendly, readable on small screens, fast mobile load
- **Onboarding**: First-time user understands how to search and filter within 30s
- **Error Messages**: Clear, helpful error messages (e.g., "No jobs found" with suggestions)
- **Tools**: Manual exploratory testing, Figma design review, user feedback from community
- **Frequency**: Per release and after UX/UI changes

#### 2.6.5 Additional NFRs

| NFR | Approach |
|-----|----------|
| **Reliability / Availability** | Platform uptime target: 99.5% (excluding planned maintenance); monitor via Sentry + CloudFlare analytics |
| **Data Accuracy** | Maximum 1% stale/incorrect jobs in index; URL validation runs daily |
| **Disaster Recovery** | SOLR index backup strategy; restore procedure documented in peviitor_core |
| **Browser Compatibility** | Latest 2 versions of Chrome, Firefox, Edge, Safari |
| **Mobile Responsiveness** | All pages functional on viewports ≥ 320px width |
| **SEO** | Verify meta tags, semantic HTML, proper heading hierarchy (h1-h6) |

### 2.7 Requirements — Where Testers Find Them

Testers use the following sources to understand what to test and what the expected behavior should be:

| Source | Location | What It Contains |
|--------|----------|------------------|
| **GitHub Issues** | [github.com/peviitor-ro](https://github.com/peviitor-ro) per repo (search-engine, api, peviitor_core) | Feature requests, bug reports, acceptance criteria, discussions |
| **GitHub Releases** | [github.com/peviitor-ro/search-engine/releases](https://github.com/peviitor-ro/search-engine/releases) | Release notes with changelog, new features, fixed bugs |
| **Figma Designs** | [Figma - Pe Viitor](https://www.figma.com/file/SS81SUL5ZnytusulXYwuUG/Pe-Viitor) | UI mockups, design system, component specs, user flows |
| **Swagger UI** | [test.peviitor.ro/swagger-ui](https://test.peviitor.ro/swagger-ui) | API contract: endpoints, request/response schemas, status codes |
| **peviitor_core README** | [github.com/peviitor-ro/peviitor_core](https://github.com/peviitor-ro/peviitor_core) | Job Model Schema, Company Model Schema, field rules, status flow |
| **Documentation** | [sad.peviitor.ro](https://sad.peviitor.ro) — Software Architecture Design | Architecture diagrams, component interactions, technology stack |
| **Discord** | [discord.gg/KPMkdUfQNu](https://discord.gg/KPMkdUfQNu) | Real-time discussions, clarifications, decisions, meeting notes |
| **Onboarding Portal** | [onboarding.peviitor.ro](https://onboarding.peviitor.ro) | General project overview, contributor guide, how-to guides |

> **Rule**: When a requirement is unclear or missing, the tester **must** ask for clarification in Discord or via a GitHub Issue before writing test cases. Never guess the expected behavior.

---

## 3. TEST TEAM

### 3.1 Team Structure

| Role | Number of Testers | Responsibilities |
|------|------------------|-----------------|
| **Manual QA Tester** | 5 | Functional testing, regression testing, exploratory testing, bug reporting, test case creation, cross-browser testing, data validation via admin.peviitor.ro |
| **Automation QA Tester** | 2 | Automated E2E tests (Playwright), API test automation (Postman collections), CI/CD integration, test script maintenance, regression automation |
| **Performance Tester** | 1 | Load testing (k6), SOLR query performance monitoring, API latency measurement, Lighthouse audits, capacity planning |
| **Security Tester** | 1 | OWASP Top 10 validation, penetration testing (OWASP ZAP), vulnerability assessment, security code review, Dependabot alert triage, secret scanning monitoring |

### 3.2 Responsibilities per Role

#### Manual QA Testers (5)
- Execute test cases for each release
- Perform exploratory testing on new features
- Log and track bugs in GitHub Issues
- Verify fixed bugs and close them
- Maintain test case repository
- Run regression checklists before production deploy
- Validate data quality via admin.peviitor.ro

#### Automation QA Testers (2)
- Develop and maintain automated test suites (Playwright, API)
- Integrate tests into GitHub Actions CI/CD pipeline
- Review manual test cases for automation potential
- Maintain test data and fixtures
- Report automation coverage metrics

#### Performance Tester (1)
- Conduct load tests on search and API endpoints
- Monitor SOLR query performance and indexing times
- Track Lighthouse scores per release
- Set up performance dashboards
- Identify bottlenecks and recommend optimizations

#### Security Tester (1)
- Perform security assessments against OWASP Top 10
- Configure and monitor GitHub Secret Scanning, Code Scanning (CodeQL), and Dependabot
- Conduct manual security reviews of API endpoints
- Verify CORS, authentication, and input sanitization
- Generate security test reports

### 3.3 Training & Onboarding

New testers will be onboarded via the [peviitor.ro onboarding portal](https://onboarding.peviitor.ro/) and receive access to the tools listed in Chapter 5 (TOOLS & ACCESS). Each tester will be assigned a mentor from the existing team for the first 2 weeks.

---

## 4. TEST LEVELS / TESTING TYPES

### 3.1 Unit Testing

| Layer | Scope | Responsibility |
|-------|-------|---------------|
| PHP (api / peviitor_core) | Utility functions, data transformations, SOLR query builders | Development team |
| JavaScript (search-engine) | Redux slices, selectors, utility functions | Frontend team |
| **Tools** | PHPUnit, Jest, Vitest | |
| **Frequency** | On each PR / commit | |

### 3.2 Integration Testing

| Integration | Scope |
|-------------|-------|
| API ↔ SOLR | Verify API queries return correct SOLR results |
| Frontend ↔ API | Verify network layer, response parsing, error states |
| Scrapers → Core | Verify scraped data is correctly parsed and indexed |
| **Tools** | PHPUnit (integration), Postman collections, manual |
| **Frequency** | Weekly, before release |

### 3.3 System Testing (End-to-End)

- **Full search flow**: user lands on peviitor.ro → searches by keyword → filters by location/workmode → views job details → clicks apply link
- **Admin validation flow**: admin.peviitor.ro → review scraped jobs → validate/reject → verify status change in SOLR
- **Cross-browser**: Chrome, Firefox, Edge, Safari
- **Mobile**: responsive layout on 320px–1920px viewports
- **Tools**: Manual exploratory, Playwright (planned)
- **Frequency**: Per release

### 3.4 Regression Testing

- **Critical path regression**: search, filter, pagination, job detail, company listing
- **Scope**: Every release verifies all existing functionality is unaffected
- **Tools**: Manual checklists, Postman collections, automated smoke suite (planned)
- **Frequency**: Per release (~weekly)

### 3.5 Acceptance Testing

- **Internal acceptance**: QA team validates against acceptance criteria from requirements
- **Community feedback**: Bug reports from Discord, GitHub Issues triaged and verified
- **Sign-off**: QA lead confirms all critical and major issues are resolved before production deploy
- **Frequency**: Per release

---

## 5. ENVIRONMENTS

### 5.1 LOCAL ENVIRONMENT

| Aspect | Detail |
|--------|--------|
| **Frontend URL** | `http://localhost:3000` |
| **API URL** | `http://localhost/api` (via local_environment Docker setup) |
| **SOLR** | Local SOLR instance via Docker (separate cores: jobs, companies) |
| **Purpose** | Feature development, unit testing, isolated debugging |
| **Who Has Access** | Developers |
| **Setup** | See [local_environment](https://github.com/peviitor-ro/local_environment) repo |
| **Data** | Minimal seed data; scraper output can be indexed manually for testing |

### 5.2 TEST ENVIRONMENT

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend** | [https://test.peviitor.ro](https://test.peviitor.ro) | Integration testing, UAT, regression before release |
| **API (Swagger UI)** | [https://test.peviitor.ro/swagger-ui](https://test.peviitor.ro/swagger-ui) | Interactive API documentation with request/response schemas for v0–v6 endpoints |
| **SOLR** | [https://testsolr.peviitor.ro](https://testsolr.peviitor.ro) | SOLR querying, schema validation, indexing tests, diacritics search verification |

**Details:**
- **Who Has Access**: QA team, developers
- **Data**: A subset of production data (~5,000 jobs) refreshed periodically
- **SOLR Cores**: `jobs`, `companies` — separate from production cores
- **API Versions**: v0–v6 all available for testing
- **CI/CD**: GitHub Actions auto-deploys on PR merge
- **Monitoring**: Sentry.io integrated; errors triaged by severity

#### 5.2.1 Build Definition

A **BUILD** is a deployable version of one or more components that has passed CI/CD and is ready for testing on the TEST environment.

| Component | What Constitutes a Build | Version Source |
|-----------|-------------------------|----------------|
| **Frontend (search-engine)** | A merged PR to `main` branch that passes GitHub Actions (lint + build) | Git tag / release (e.g. `v62`) |
| **API (api.peviitor.ro)** | A merged PR to `master` branch that passes GitHub Actions | Commit hash + release tag (e.g. `v1.2`) |
| **Core / SOLR config (peviitor_core)** | A merged PR to `main` branch with SOLR schema or workflow changes | Commit hash |

**Build ID format**: `[component]-v[number]-[YYYYMMDD]` (e.g. `frontend-v62-20260601`)

A full **release build** includes all three components deployed together with a matching release tag.

#### 5.2.2 Deploy Process to TEST Environment

| Step | Who | Action |
|------|-----|--------|
| 1 | **Developer** | Merges PR to `main`/`master` branch |
| 2 | **GitHub Actions** | Auto-triggers CI/CD pipeline: lint → test → build → deploy to test.peviitor.ro |
| 3 | **GitHub Actions** | Notifies in Discord `#deploy` channel when deploy completes |
| 4 | **QA Tester** | Receives notification and begins smoke testing |
| 5 | **QA Tester** | Verifies the build is stable (smoke tests pass) |
| 6 | **QA Tester** | Proceeds with full regression / feature testing |

**Deploy triggers:**
- **Automatic**: Every merge to `main`/`master` triggers a deploy to TEST
- **Manual**: A developer or QA lead can trigger a manual re-deploy via GitHub Actions workflow_dispatch

**Rollback**: If the deployed build is broken, the previous build is re-deployed via GitHub Actions using the last known good commit.

### 5.3 PRODUCTION ENVIRONMENT

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend** | [https://peviitor.ro](https://peviitor.ro) | Live platform — public facing |
| **SOLR** | [https://solr.peviitor.ro](https://solr.peviitor.ro) | Production SOLR querying, schema management, monitoring |

**Details:**
- **Who Has Access**: All users (frontend); QA lead & DevOps (SOLR admin with basic auth)
- **Data**: Full dataset — 40,000+ jobs updated daily via scrapers
- **Infrastructure**: Raspberry Pi 5, CloudFlare CDN, ClausWeb hosting
- **Deploy**: Manual deploy with QA lead sign-off; GitHub Actions build only
- **Monitoring**: Sentry.io, CloudFlare analytics

---

## 6. TOOLS & ACCESS

The table below centralizes all testing tools referenced in this document, along with access instructions for new testers.

| Tool | Used For | URL / Access / Install | Who Creates User | Who Ensures Availability |
|------|----------|----------------------|-----------------|-------------------------|
| **Chrome DevTools** | Frontend debugging, performance, network, console | Built into Chrome — `F12` / `Ctrl+Shift+I` | — (built-in) | — |
| **React DevTools** | React component inspection | Chrome extension: [chromewebstore.google.com](https://chromewebstore.google.com/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi) | — (built-in) | — |
| **Sentry.io** | Error monitoring (frontend + API) | [sentry.io](https://sentry.io) — account required | | |
| **Postman** | API endpoint testing, collections | [postman.com/downloads](https://www.postman.com/downloads/) | — (free tier) | — |
| **Bruno** | API endpoint testing (open source alternative) | [usebruno.com/downloads](https://www.usebruno.com/downloads) | — (open source) | — |
| **REST Client** | Quick API testing in editor | VS Code extension: [marketplace.visualstudio.com](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) | — (built-in) | — |
| **SOLR Admin UI** | SOLR querying, schema management, indexing tests | Prod: [solr.peviitor.ro](https://solr.peviitor.ro) / Test: [testsolr.peviitor.ro](https://testsolr.peviitor.ro) | | |
| **Swagger UI** | Interactive API documentation | [test.peviitor.ro/swagger-ui](https://test.peviitor.ro/swagger-ui) | — (public) | — |
| **curl** | Command-line SOLR/API testing | Built into Windows/macOS/Linux | — (built-in) | — |
| **PHPUnit** | PHP unit & integration tests | [docs.phpunit.de](https://docs.phpunit.de/) — install via Composer | Developer | Developer |
| **Jest** | JavaScript unit tests (search-engine) | [jestjs.io](https://jestjs.io/) — `npm install jest` | Developer | Developer |
| **Vitest** | JavaScript unit tests (search-engine alternative) | [vitest.dev](https://vitest.dev/) — `npm install vitest` | Developer | Developer |
| **Lighthouse** | Performance & accessibility audits | Built into Chrome DevTools — or CLI: `npm install -g lighthouse` | — (built-in) | — |
| **k6** | Performance / load testing (planned) | [grafana.com/docs/k6](https://grafana.com/docs/k6/) — installer per OS | | |
| **OWASP ZAP** | Security testing (planned) | [zaproxy.org/download](https://www.zaproxy.org/download/) | | |
| **axe DevTools** | Accessibility audit (WCAG) | Chrome extension: [chromewebstore.google.com](https://chromewebstore.google.com/detail/axe-devtools-web-accessib/lhdoppojpmngadmnindnejefpokejbdd) | — (built-in) | — |
| **WAVE** | Accessibility evaluation | Chrome extension: [chromewebstore.google.com](https://chromewebstore.google.com/detail/wave-evaluation-tool/jbbplnpkjmmeebjpijfedlgcdilocofh) | — (built-in) | — |
| **Playwright** | Automated E2E testing (planned) | [playwright.dev](https://playwright.dev/) — `npm init playwright` | Developer | Developer |
| **GitHub Actions** | CI/CD, automated test runs | [github.com/peviitor-ro](https://github.com/peviitor-ro) — included in repos | | |
| **GitHub Issues** | Bug tracking, test case management | [github.com/peviitor-ro](https://github.com/peviitor-ro) — included in repos | | |
| **GitHub Secret Scanning** | Detect accidentally committed credentials, API keys, tokens | [github.com/peviitor-ro](https://github.com/peviitor-ro) — Security tab → Secret scanning | — (auto-enabled for public repos) | GitHub |
| **GitHub Code Scanning (CodeQL)** | Analyze code for security vulnerabilities (CWE) on every push/PR | [github.com/peviitor-ro](https://github.com/peviitor-ro) — Security tab → Code scanning | — (auto-enabled) | GitHub |
| **Dependabot** | Automated dependency vulnerability checks & update PRs | [github.com/peviitor-ro](https://github.com/peviitor-ro) — Security tab → Dependabot alerts | — (auto-enabled) | GitHub |
| **admin.peviitor.ro** | Manual job validation | [admin.peviitor.ro](https://admin.peviitor.ro) | | |
| **Figma** | UI design review, usability validation | [figma.com](https://www.figma.com) — [Pe Viitor design](https://www.figma.com/file/SS81SUL5ZnytusulXYwuUG/Pe-Viitor) | | |
| **CloudFlare** | CDN, DNS, performance analytics | [dash.cloudflare.com](https://dash.cloudflare.com) | | |
| **Discord** | Team communication, bug discussion | [discord.gg/KPMkdUfQNu](https://discord.gg/KPMkdUfQNu) | — (public invite) | — |

> **Note**: Cells marked with "—" indicate tools that are free, built-in, or publicly accessible. Empty cells need to be filled in by the project lead with the responsible person's name.

---

## 7. DELIVERABLES

### Test Artifacts

| Artifact | Description | Owner |
|----------|-------------|-------|
| **Test Strategy** (this document) | Overall test approach and methodology | QA lead |
| **Test Cases** | Detailed step-by-step test cases for each component | QA team |
| **Test Checklists** | Quick regression checklists for releases | QA team |
| **Bug Reports** | Issues logged in GitHub Issues with severity, steps to reproduce, screenshots | QA team |
| **Test Summary Report** | Summary of test execution per release: passed/failed/blocked metrics | QA lead |

### Reporting Cadence

| Report | Frequency | Audience |
|--------|-----------|----------|
| Bug triage summary | Weekly | QA team, developers |
| Test execution report | Per release | QA lead, project lead |
| Release readiness status | Before each production deploy | All teams |

---

## 8. ENTRY CRITERIA

Before testing begins on a new release or feature, the following conditions must be met:

- [ ] Code has been merged to the target branch (main/master)
- [ ] Build passes successfully on CI/CD (GitHub Actions)
- [ ] Frontend builds without errors (`npm run build`)
- [ ] API returns healthy status (smoke test passes)
- [ ] SOLR cores are accessible and contain test data
- [ ] Test environment is deployed with the latest build
- [ ] Test cases / checklists are updated for new features
- [ ] Known critical bugs from previous release are fixed or documented as known issues

---

## 9. EXIT CRITERIA

A release is considered ready for production when all of the following are met:

- [ ] All S1 (Blocker), S2 (Critical), and S3 (Major) severity bugs are fixed and verified
- [ ] Regression test suite (critical path) passes: 100% pass rate
- [ ] New features are tested and accepted by QA
- [ ] Accessibility checks pass (no critical WCAG violations)
- [ ] Performance benchmarks are within acceptable thresholds (P95 < 2s search)
- [ ] Test summary report is reviewed and approved by QA lead
- [ ] Production deploy receives sign-off from QA lead and project lead

---

## 10. BUG LIFECYCLE

### 10.1 Bug Reporting Process

All bugs are tracked in **GitHub Issues** under the relevant repository (search-engine, api, peviitor_core). Each bug report must include:

- **Title**: Clear, descriptive summary of the issue
- **Environment**: test.peviitor.ro / peviitor.ro / local
- **Steps to Reproduce**: Numbered steps to recreate the bug
- **Actual Result**: What actually happens
- **Expected Result**: What should happen
- **Screenshots / Video**: Visual evidence (if applicable)
- **Browser / Device**: Chrome, Firefox, Edge, Safari + version
- **Severity**: See 10.3

### 10.2 Bug States

```
[New] → [Assigned] → [In Progress] → [Fixed] → [Verified] → [Closed]
                  ↘ [Rejected] → [Closed]
[Verified] → [Reopened] → [Assigned]
```

| State | Description |
|-------|-------------|
| **New** | Bug reported, not yet reviewed |
| **Assigned** | Assigned to a developer for fixing |
| **In Progress** | Developer is actively working on the fix |
| **Fixed** | Fix is deployed to test environment |
| **Verified** | QA has tested and confirmed the fix |
| **Closed** | Bug is resolved and accepted |
| **Rejected** | Not a bug / duplicates / cannot reproduce |
| **Reopened** | Bug reappears after verification |

### 10.4 Severity

Severity describes the **technical impact** of the bug (how bad the problem is). Priority is set separately by the Product Owner based on business urgency and is not tracked in this document.

#### Severity Levels

| Level | Label | Description | Example |
|-------|-------|-------------|---------|
| **S1 - Blocker** | `severity/blocker` | The application or a critical component is completely unusable. No workaround exists. Testing cannot proceed until resolved. | Search returns HTTP 500; SOLR core unavailable; page fails to load |
| **S2 - Critical** | `severity/critical` | A major feature is broken, data is incorrect or lost, or the user experience is severely degraded. No reasonable workaround exists. | Search returns zero results for valid queries; job details page crashes; incorrect salary data displayed |
| **S3 - Major** | `severity/major` | A feature does not work as expected but a partial workaround exists. Functionality is impaired but not completely blocked. | Filters return incorrect results on edge cases; pagination skips pages; search timeout on complex queries |
| **S4 - Minor** | `severity/minor` | A feature works correctly but has a minor issue that does not affect functionality. A workaround is easily available. | UI misalignment on tablet; typo in a label; missing tooltip |
| **S5 - Trivial** | `severity/trivial` | Cosmetic or low-impact issue. Does not affect functionality or user experience in a meaningful way. | Slightly off color shade; missing alt text on decorative image; extra whitespace |

---

## 11. RISK AND MITIGATION

| Risk | Description | Probability | Impact | Mitigation |
|------|-------------|-------------|--------|------------|
| **Single point of failure — Raspberry Pi 5** | Production server runs on a single Raspberry Pi 5. Hardware failure would take down peviitor.ro entirely. | Low | Critical | Daily SOLR backups; documented restore procedure; standby recovery plan via ClausWeb hosting |
| **Data quality from scrapers** | Scrapers may return incomplete or incorrect data (missing fields, wrong salary, dead URLs). | Medium | High | Daily URL validation pipeline (HEAD requests, 404 deletion); admin.peviitor.ro manual validation; status flow (scraped → tested → verified → published) |
| **Scraper breakage** | Target websites change their HTML structure, CSS selectors, or add anti-bot measures (CAPTCHA, IP blocking). | Medium | Major | Community-driven maintenance; multiple scraper technologies (Python, JS, JMeter); quick fallback to "tested" status |
| **SOLR index corruption** | SOLR index may become corrupted due to power failure, disk full, or software bug. | Low | Critical | Automated daily cron jobs for index optimization; backup scripts in peviitor_core; separate test SOLR for validation before production indexing |
| **Volunteer availability** | The project relies on volunteers. Key people may become unavailable, causing delays. | Medium | Medium | Cross-training across team members; documentation in GitHub; onboarding process for new volunteers |
| **API rate limiting / blocking** | Job portals may block peviitor scrapers or the API may be rate-limited by SOLR or CloudFlare. | Low | Major | Respect robots.txt; configurable scrape intervals; monitoring via Sentry and CloudFlare |
| **GitHub Actions free tier limits** | Free tier has monthly usage limits. Heavy CI/CD usage may exhaust the quota. | Low | Minor | Optimize workflows; cache dependencies; remove redundant triggers |
| **CloudFlare CDN outage** | CloudFlare is used as CDN and DNS provider. An outage would affect availability. | Very Low | Major | DNS failover not configured; accept as acceptable risk given CloudFlare's 99.99% SLA |
| **Security breach (SOLR / API)** | Unauthorized access to SOLR admin or API could leak or corrupt data. | Low | Critical | SOLR basic auth enabled; CORS restrictions; GitHub Secret Scanning; regular dependency updates via Dependabot |

---

## 12. ANNEX

### 12.1 Bug Report Template

```
**Title**: [Short descriptive summary]

**Environment**: test.peviitor.ro | peviitor.ro | local

**Steps to Reproduce**:
1. Go to https://test.peviitor.ro
2. Search for "software engineer"
3. Click "Load More" 3 times
4. Observe results

**Actual Result**: Only 10 results shown after clicking "Load More" 3 times; console shows 404 error.

**Expected Result**: 30 results should be displayed (10 per page × 3 pages).

**Severity**: S2 - Critical

**Browser**: Chrome 125
**OS**: Windows 11

**Screenshots**: [link or attachment]

**Additional Context**: Network tab shows GET /api/v6/search?page=3 returns 404
```

### 12.2 Test Case Example

```
Test Case ID: TC-SEARCH-001
Title: Verify basic keyword search returns relevant results
Feature: Search Engine
Environment: test.peviitor.ro
Preconditions: Browser open at https://test.peviitor.ro

Test Steps:
1. Click on the search input field
2. Type "software engineer" and press Enter
3. Wait for results to load
4. Observe the list of displayed job results

Expected Result:
- Results are displayed within 2 seconds
- Each result contains: job title, company name, location
- Results contain the keyword "software" or "engineer" or both
- Pagination controls are visible (if more than 10 results)
- No error messages are shown
```

### 12.3 Test Execution Report Template

```
TEST EXECUTION REPORT

Release: [vXX]
Date: [DD/MM/2026]
Tester: [Name]
Environment: test.peviitor.ro

1. EXECUTION SUMMARY
   Total Test Cases:      XX
   Passed:                XX (XX%)
   Failed:                XX (XX%)
   Blocked:               XX (XX%)
   Not Executed:          XX (XX%)

2. BUG SUMMARY
   S1 - Blocker:          XX
   S2 - Critical:         XX
   S3 - Major:            XX
   S4 - Minor:            XX
   S5 - Trivial:          XX
   Total Bugs Found:      XX

3. TEST COVERAGE
   Frontend:              XX/XX (XX%)
   API:                   XX/XX (XX%)
   SOLR Indexing:         XX/XX (XX%)
   Data Validation:       XX/XX (XX%)
   Cross-Component:       XX/XX (XX%)

4. KEY FINDINGS
   - [Critical issue found in ...]
   - [Major regression in ...]
   - [All accessibility checks passed]

5. RECOMMENDATION
   [Approve / Conditional Approve / Reject] for production deployment.

6. SIGN-OFF
   Tester: ___________________
   QA Lead: __________________
   Date: ___/___/2026
```
