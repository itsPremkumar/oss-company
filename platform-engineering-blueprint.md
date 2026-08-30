# Platform Engineering Blueprint — t_c09dce5b

> How we build the internal platform that every product and agent runs on.
> Owner: @cto. This is the infrastructure contract, not a project spec.

## 1. Platform vision

A self-service internal platform where:
- **Products** (TaskForge, Hermes-ASI, Beacon) deploy with one config file.
- **Agents** (the 34-avatar team) get isolated, capability-scoped runtimes.
- **Engineers** (human or AI) get a single pane of glass for observability.

The platform is the product. Everything else runs on it.

## 2. Platform layers

```
┌─────────────────────────────────────────────────────────┐
│                  Products & Agents                       │
│  (TaskForge │ Hermes-ASI │ Beacon │ 34-avatar team)     │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────┐
│               Platform Services Layer                    │
│  (identity │ secrets │ config │ scheduling │ routing)   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────┐
│              Infrastructure Abstraction                  │
│  (compute │ storage │ network │ observability)          │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────┐
│                   Physical Infrastructure                │
│  (laptop:7052 │ laptop:8568 │ cloud VMs │ GH runners)   │
└─────────────────────────────────────────────────────────┘
```

## 3. Platform services

### 3.1 Identity & access
- **AgentOS capability model** — unforgeable tokens, not passwords.
- **AgentMesh DIDs** — decentralized identity for P2P agents.
- **Human SSO** — GitHub OAuth (no separate login).

### 3.2 Secrets management
- **Local**: OS keychain (Windows Credential Manager, macOS Keychain).
- **Remote**: AgentOS encrypted persistent memory.
- **Rotation**: automated, with audit trail.

### 3.3 Configuration
- **Declarative YAML** — single source of truth per service.
- **JSON Schema validation** — fail fast on bad config.
- **Environment promotion** — dev → staging → prod via git branches.

### 3.4 Scheduling
- **AgentOS scheduler** — priority-preemptive, per-agent quotas.
- **Claimer subsystem** — routes tasks to avatars (with Law 1 exclusion).
- **Concurrency cap** — no avatar > 3 concurrent tracks (§2.1 load rule).

### 3.5 Routing & discovery
- **AgentMesh A2AP** — agent-to-agent message routing.
- **Capability-based service registry** — find agents by what they can do.
- **Gossip protocol** — epidemic broadcast for discovery.

## 4. Infrastructure abstraction

### 4.1 Compute
- **Primary**: bare containers (Docker/Podman) on laptop:7052 + laptop:8568.
- **Burst**: GitHub Actions runners for CI/CD.
- **Future**: cloud VMs (Fly, Railway, Render) when on-prem isn't enough.

### 4.2 Storage
- **Default**: SQLite (zero-config, single-file).
- **HA path**: PostgreSQL when write throughput demands it.
- **Blob**: AgentOS filesystem (hierarchical namespace + schema-validated docs).

### 4.3 Network
- **Local**: direct process-to-process (AgentOS message passing).
- **Remote**: A2AP over WebSockets or gRPC.
- **P2P**: AgentMesh gossip + consensus for decentralized coordination.

### 4.4 Observability
- **Traces**: OpenTelemetry, every loop iteration emits a trace.
- **Metrics**: Prometheus-compatible, scraped by the dashboard.
- **Logs**: structured JSON, shipped to the dashboard (t_efcc69fe).
- **Health checks**: per-plugin, per-agent, per-service.

## 5. Platform contracts (SLIs/SLOs)

| Service | SLI | SLO |
|---------|-----|-----|
| Scheduler | Task dispatch latency | < 5s p99 |
| Claimer | Task claim success rate | > 99% |
| Identity | Token validation latency | < 10ms p99 |
| Secrets | Secret retrieval success | > 99.9% |
| Config | Config validation latency | < 100ms p99 |
| Routing | Message delivery success | > 99.9% |
| Dashboard | Dashboard load time | < 2s p95 |

## 6. Platform governance

### 6.1 Law 1 — claimer exclusion
A claimer with 2+ consecutive failures is excluded for 15 minutes. No re-dispatch to a faulting host within cooldown.

### 6.2 Law 8 — delegation credential parity
Git/crypto operations must never delegate to a non-interactive subagent unless credential-env parity is guaranteed.

### 6.3 Dependency gating
A track may not start until every declared upstream artifact is committed and referenced by SHA/ref.

### 6.4 CEO escalation
Escalation fires when: repo unreachable > 24h, avatar overload > 24h, track silent > 72h, dependency integrity violation.

## 7. Platform roadmap

### Phase 1 — Foundation (done)
- AgentOS kernel + scheduler
- AgentMesh A2AP + identity
- Claimer subsystem + Law 1
- Dashboard v1 (t_efcc69fe)

### Phase 2 — Intelligence (current)
- Phase 9 ASI Master (4 pillars as plugins)
- Formal reasoning (Lean/Z3)
- Scientific discovery loop
- Computer-use GUI loop

### Phase 3 — Scale (next)
- Multi-region compute
- PostgreSQL HA path
- Advanced P2P consensus
- Plugin marketplace (decentralized registry)

### Phase 4 — Maturity
- Formal verification of platform services
- Self-healing infrastructure
- Automated capacity planning

## 8. Platform acceptance criteria

- All products deploy with one config file.
- All agents run in isolated, capability-scoped runtimes.
- All engineers (human or AI) have a single pane of glass.
- All SLIs meet SLOs for 30 consecutive days.
- All governance laws (1, 8, dependency gating, escalation) are enforced.

Author: @cto
