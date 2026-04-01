
This project is an automated regression suite for the public demo e-commerce site `automationexercise.com`. It combines **UI** (Playwright) and **API** (Playwright API client) validation to protect core “money path” flows such as **authentication, product browsing/search, cart/checkout, and order interactions**, while also verifying backend API integrity.

## Feature

### The Technical “What”
- **Playwright (UI)** + **Pytest (runner/assertions)** for end-to-end validation.
- **Playwright API client** for direct API contract checks and workflow consistency.
- **Fixtures + Page Objects** to keep tests readable and maintainable.
- **Flake resilience** using reruns and additional page-state normalization (e.g., consent overlay handling).
- **Rich reporting**: self-contained **HTML reports**, plus **Playwright traces and screenshots** on failure.

### The Business “So What?”
- **Hybrid API/UI validation** catches backend regressions earlier, reducing expensive UI-only debugging.
- **Release readiness** improves via automated quality gates on every PR/push.
- **Faster feedback loops**: tests run automatically in CI and produce artifacts immediately when something breaks.
- **Lower maintenance cost**: page interactions are centralized into page objects and common utilities.

## What Was Tested and Why

### Critical UI workflows (UI money path)
- Login/registration, logout, duplicate signup behavior
- Add/remove products in cart and checkout steps
- Contact form submission and newsletter subscription
- Product search and product detail visibility
- Category + brand browsing (filters) and navigation/header/footer correctness
- Order history + submitting product reviews

### API layer integrity (Shift-Left)
- Auth APIs: create account, verify login, update account, get user detail, delete account
- Product APIs: products list, product search, and brands list
- API workflow consistency checks (e.g., create -> verify -> detail -> delete)

## CI/CD Integration

### Automated Quality Gates
- Runs on `push` to `main`/`develop` and on `pull_request` via GitHub Actions.
- Executes the full suite (`pytest`) and fails the job when tests fail.

### Faster Releases
- The CI run produces:
  - HTML report artifacts under `reports/`
  - Playwright traces under `test-results/` (when available)
  - Screenshots for failed UI tests under `reports/screenshots/`

## Key Engineering Decisions

1. **Hybrid API-Driven UI Setup**
   - UI auth depends on creating a user via the API when possible (`created_account` + `ensure_logged_in_user` fixture).
   - Why it matters: it reduces UI setup time and isolates frontend issues from backend propagation timing.

2. **Smart Page Object Model (POM)**
   - Centralized navigation and assertions in `pages/` (e.g., `HomePage`, `ProductsPage`, `ProductPage`).
   - Why it matters: reduces “automation debt” when UI selectors change.

3. **Observability-First Debugging**
   - CI and local runs produce self-contained HTML.
   - UI failures capture screenshots automatically and Playwright tracing is enabled on failure.
   - Why it matters: debugging time is reduced because artifacts are attached to the failed run.

4. **Flakiness Controls**
   - Consistent overlay/consent handling to prevent pointer-event interception.
   - CI reruns (`pytest --reruns 3`) to absorb external-site transient behavior.

## Key Achievements and Highlights

**🚀 Project Highlights**
- **100+ automated checks** covering **auth, search/product browsing, cart/checkout, contact flow, and order-related UI actions**, plus **API CRUD/validation**.
- **CI/CD Ready:** tests run automatically on every `push`/`pull_request` via **GitHub Actions**, with artifacts (HTML report, Playwright traces/screenshots) produced when something fails.
- **Maintenance-First:** a fixture + Page Object Model approach centralizes UI interactions to reduce duplicated logic.
- **Higher Reliability:** flake mitigation via **reruns** and consistent handling of demo-site overlays/consent UI, backed by Playwright **tracing** and **screenshots** on failure.

## Tech Stack Used and Why
- **Python** — keeps the suite readable and extensible as test coverage grows.
- **Playwright** — reliable UI automation for complex selectors and auto-wait behavior to reduce flakiness.
- **Pytest** — flexible test runner with fixtures, markers (`ui`/`api`), and clean assertions.
- **Playwright API client** — fast API validation to catch backend contract issues before UI regressions.
- **GitHub Actions** — automated quality gate on every PR/push with downloadable failure artifacts.

## How to Run

### Local Setup
1. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
2. Install Playwright browser binaries (Chromium is used in CI):
   ```bash
   python -m playwright install --with-deps chromium
   ```

### Run Tests
- Run everything:
  ```bash
  pytest
  ```
- Run UI tests only:
  ```bash
  pytest -m ui
  ```
- Run API tests only:
  ```bash
  pytest -m api
  ```
- Run “smoke or ui” (as used in earlier CI iterations):
  ```bash
  pytest -m "smoke or ui"
  ```

