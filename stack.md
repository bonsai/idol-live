# idol-live Stack

## Architecture

| Layer | Choice | Responsibility |
|---|---|---|
| Product design | GitHub Issues | Intent, domain, schema decisions, implementation tasks |
| Driver | AW Workflow | Orchestration and traceability |
| Frontend | Vue 3 | Application UI |
| Build | Vite | Development server and production build |
| Language | TypeScript | Application code and domain types |
| UI | CSS | Responsive PC/mobile presentation |
| State | Composition API | Search/filter state and derived views |
| Data | JSON | Event dataset and fixtures |
| Runtime data | `.data/` | Canonical event data/fixtures |
| Schema | JSON Schema | Validate event data contract |
| Unit test | Vitest | Components, composables, data logic |
| E2E | Playwright | Search and responsive smoke tests |
| Quality | ESLint + Prettier | Static analysis and formatting |
| Deploy | GitHub Pages | Static production hosting |

## Runtime flow

```text
Issue (design)
    ↓
AW Workflow (driver)
    ↓
Vue + TypeScript (code)
    ↓
.data/events.json (data)
    ↓
Schema validation
    ↓
Vitest / Playwright
    ↓
Vite build
    ↓
GitHub Pages
```

## Repository boundaries

- **Issue** = canonical design and implementation task.
- **Workflow** = execution/orchestration driver.
- **Repository source** = executable application code.
- **`.data/`** = runtime data and fixtures.
- Generated code must not become the canonical source of product design.
- Runtime event data must not be mixed into `src/`.

## MVP stack contract

1. Vue 3 + Vite + TypeScript application.
2. `.data/events.json` is the initial event fixture.
3. Event data conforms to the event JSON Schema.
4. Search supports date range, area, and free-admission conditions.
5. Free status distinguishes `free`, `drink_required`, `reservation_required`, and conditions.
6. UI is responsive for PC and mobile.
7. Production build outputs `dist/`.
8. Deployment follows `deploy.scheme.json`.
9. Build, data validation, and smoke tests are required before deployment.

## Design principle

```text
Intent → Domain → Schema → Issues → IA → Components → Code → Data → Validation → Deploy
```

The screen is not designed first. The stack is driven from the Issue-defined domain and data contract.
