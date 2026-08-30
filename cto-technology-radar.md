# CTO Technology Radar — t_edadc257

> What the company builds on, what we're exploring, and what we reject.
> Owner: @cto. Updated: 2025.

## Structure

- **ADOPT** — proven, default choice for production
- **TRIAL** — actively evaluating in real projects
- **HOLD** — interesting but not yet fit for production
- **REJECT** — anti-pattern for our scale; use costs more than it saves

---

## ADOPT (default for production)

| Tech | Why | Where |
|------|-----|-------|
| **Rust** | Single static binary, memory-safe, boring-for-prod | Compute core, runners, anything that runs in CI |
| **Go** | Fast compile, great concurrency, simple ops story | Control plane, CLIs, API servers |
| **TypeScript** | Type-safe, huge ecosystem, runs everywhere | Dashboard, SDKs, edge/browser/node |
| **Python** | Lingua franca for ML/AI glue, fast iteration | Data pipelines, SDK, scientific tooling |
| **YAML** | Devs already read/write it; no new DSL to learn | All declarative configs (`.agent.yml`, `beacon.yml`) |
| **JSON Schema** | Validate YAML declaratively, generate types | All config schemas |
| **SQLite** | Zero-config, single-file, fast enough for most | State store, local-first apps |
| **OpenTelemetry** | Vendor-neutral telemetry, traces + metrics + logs | All services |
| **GitHub Actions** | Where code already lives, no new infra | CI/CD, runners, PR automation |
| **Apache 2.0 / MIT** | Encourages adoption, no copyleft friction | All OSS releases |

## TRIAL (actively evaluating)

| Tech | What we're learning | Where |
|------|---------------------|-------|
| **Lean 4** | Formal verification, proof-carrying code | Phase 9 ASI Master — formal reasoning plugin |
| **Z3 SMT solver** | Automated theorem proving, counterexample search | Phase 9 ASI Master — proof backend |
| **AgentOS kernel** | Capability-based, message-passing agent runtime | Phase 9 ASI Master — runtime substrate |
| **AgentMesh A2AP** | Decentralized P2P agent coordination | Phase 9 ASI Master — distributed mesh |
| **Plugin architectures** | Hot-loadable, sandboxed capability plugins | Phase 9 ASI Master — all four pillars |
| **CQRS + Event Sourcing** | Separate read/write models, audit trail | State-heavy services (beacon dashboard) |
| **PostgreSQL (HA path)** | When SQLite isn't enough for write throughput | High-availability deployments |

## HOLD (interesting, not yet production-fit)

| Tech | Why on hold | What would change our mind |
|------|-------------|---------------------------|
| **Kubernetes** | Overkill for < 10 services, massive ops burden | If we exceed 20+ microservices or need multi-region |
| **WebAssembly (Wasm)** | Great isolation story, but tooling still rough | If plugin sandboxing becomes a hard requirement and native doesn't cut it |
| **eBPF** | Powerful observability, steep learning curve | If we need kernel-level tracing without sidecars |
| **Elixir/BEAM** | Great for soft-real-time, but small hiring pool | If we need massive concurrency for a specific real-time feature |
| **Differential privacy** | Important for user data, but complex to implement correctly | If we handle sensitive user data and need formal privacy guarantees |

## REJECT (anti-pattern at our scale)

| Tech | Why we reject it | What we use instead |
|------|------------------|---------------------|
| **LangChain / CrewAI** | Bloat, abstraction-heavy, vendor lock-in | Direct API calls + our own thin orchestration |
| **Vendor-specific LLM APIs** | Lock-in, price risk, portability | Abstraction layer (`.agent.yml` model field) — swap providers freely |
| **Serverless for long-running work** | Cold starts, timeout limits, unpredictable cost | Bare containers or small VMs with our own scheduler |
| **Custom DSLs** | Learning cost, tooling burden, fragmentation | YAML + JSON Schema — boring, familiar |
| **Microservices for < 5 services** | Distribution overhead > any benefit | Modular monolith, extract when pain is real |
| **Self-managed Kubernetes** | Undifferentiated heavy lifting | PaaS (Railway, Fly, Render) or managed K8s if forced |
| **Blockchain for non-crypto** | Hype, no real decentralization need, terrible DX | PostgreSQL + audit log |
| **Rewriting working code for "elegance"** | Breaks production, burns trust | If it compiles and has tests, it ships |

## Principles (the "why" behind the radar)

1. **Boring tech for production, shiny for R&D** — we ship on what we know; we experiment on the edges.
2. **Clarity beats completeness** — a crisp spec with 5 adopted technologies beats a bloated list of 50.
3. **No undifferentiated heavy lifting** — if it's not our core IP, buy it or use OSS; don't build it.
4. **Move fast, don't break production** — earned-completion gates are mandatory (no silent failures).
5. **Portability is non-negotiable** — every layer must be swappable (LLM provider, database, runtime).

Author: @cto
