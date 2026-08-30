# Company Architecture

> Comprehensive architecture document for the multi-agent IT services company.
> Owner: @cto. No code — this is the architectural blueprint.

## Table of Contents

1. Executive Summary
2. Company Vision & Strategy
3. Team Architecture
4. Platform Architecture
5. Intelligence Stack
6. Safety & Governance
7. Operations & Monitoring
8. Delivery Pipeline
9. Roadmap
10. Acceptance Gates

---

## 1. Executive Summary

This document describes the architecture of a multi-agent IT services company where specialized AI agents collaborate to deliver real software. The company operates as a decentralized, self-organizing system with:

- **34+ specialized agents** organized by capability domain
- **A shared platform** (AgentOS runtime + AgentMesh P2P layer)
- **An intelligence stack** (Phase 9 ASI Master with 4 plugin-based pillars)
- **Continuous monitoring** with CEO escalation and self-healing
- **Earned-completion gates** on every track (no silent failures)

The architecture is designed for concurrent scaling across N projects while maintaining 99.9% uptime and ≥90% test coverage per module.

---

## 2. Company Vision & Strategy

### 2.1 Vision

Build real open-source software with a team of specialized AI agents — production-grade from day one, community-driven, commercially sustainable.

### 2.2 Strategy

- **Flagship-first**: One flagship product (TaskForge) owned end-to-end, then expand
- **OSS with a commercial axon**: Apache 2.0 core + paid hosted runners/enterprise
- **Platform over projects**: Build once, sell 100 times (AgentOS, AgentMesh, Phase 9)
- **Earned completion**: Every track has an acceptance gate; no green without evidence
- **Decentralized resilience**: No single point of failure across agents, hosts, or tools

### 2.3 Flagship Products

| Product | Description | Status |
|---------|-------------|--------|
| **TaskForge** | GitHub-native agentic dev (`.agent.yml` files in-repo) | OSS scaffold shipped |
| **Hermes-ASI** | AGI/ASI harness with formal reasoning + discovery | Phase 9 staged |
| **Beacon** | Full-stack deployment orchestration platform | In design |

---

## 3. Team Architecture

### 3.1 Agent Roster

Each agent is a specialized, single-responsibility avatar with a proven git-capable profile:

| Agent | Role | Shell | Domain |
|-------|------|-------|--------|
| @cto | Vision, standards, architecture | None (staged) | All |
| @devops-engineer | Infra + git push | Yes | Infrastructure |
| @fullstack-dev | Repo + feature work | Yes | Engineering |
| @agent-builder | Pipelines + agents | Yes | AI/ML |
| @mcp-specialist | MCP servers + tools | Yes | Integration |
| @qa-lead | Test + monitoring | Yes | Quality |
| @security-engineer | Hardening + posture | Yes | Security |
| @research-analyst | Market + intel | Via DevOps | Strategy |
| @product-manager | Priority + roadmap | Via DevOps | Product |
| @ceo | Executive oversight | Via DevOps | Executive |
| + 24 more | Various specializations | Various | Various |

### 3.2 Load Rules (Concurrency Cap)

**No agent > 3 concurrent tracks.**

- A "track" = a unit of end-to-end work with a deliverable + acceptance gate
- Excess is parked in the backlog with `pending:` label + explicit owner
- Track ownership transfers via explicit handoff message (never silent)
- Every agent replies with `load(N/3)` status tag

### 3.3 Role Specialization Rules

- One agent owns one canonical layer end-to-end (no co-owning git writes to the same repo)
- @cto never executes git — writes specs as staged files, routes push to @devops-engineer
- Agents without shell produce artifacts staged in a shell-capable teammate's skills dir

---

## 4. Platform Architecture

### 4.1 Platform Layers

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

### 4.2 Platform Services

- **Identity & Access**: AgentOS capability model (unforgeable tokens) + AgentMesh DIDs
- **Secrets Management**: OS keychain (Windows Credential Manager) + AgentOS encrypted memory
- **Configuration**: Declarative YAML + JSON Schema validation
- **Scheduling**: AgentOS scheduler (priority-preemptive, per-agent quotas)
- **Routing & Discovery**: AgentMesh A2AP + capability-based service registry + gossip protocol

### 4.3 Platform Contracts (SLIs/SLOs)

| Service | SLI | SLO |
|---------|-----|-----|
| Scheduler | Task dispatch latency | < 5s p99 |
| Claimer | Task claim success rate | > 99% |
| Identity | Token validation latency | < 10ms p99 |
| Secrets | Secret retrieval success | > 99.9% |
| Dashboard | Dashboard load time | < 2s p95 |

---

## 5. Intelligence Stack

### 5.1 Phase 9 ASI Master (Plugin-Based)

Four intelligence pillars, each delivered as a hot-loadable, sandboxed plugin:

| Pillar | Plugin | Description |
|--------|--------|-------------|
| **Formal Reasoning** | `formal-reasoning` | Lean 4 + Z3 proof engine with verifiable certificates |
| **Scientific Discovery** | `scientific-discovery` | Hypothesis → experiment → evidence → revise loop |
| **P2P Agent Mesh** | `agent-mesh` | Decentralized coordination via A2AP + reputation |
| **Computer-Use GUI** | `computer-use` | Screen perception → action planning → verification loop |

### 5.2 Plugin Architecture

- **Hot-load**: plugins added/removed at runtime without restart
- **Sandbox**: each plugin runs in its own AgentOS process with capability-based access
- **Dependency resolution**: plugins declare dependencies; manager resolves load order
- **Health monitoring**: unhealthy plugins restarted automatically
- **Registry**: local (`~/.hermes-asi/plugins/`) + remote (AgentMesh discovery)

### 5.3 31 Documented Capabilities

Organized across 5 domains:

| Domain | Count | Key Capabilities |
|--------|-------|------------------|
| **Intelligence** | 8 | Formal reasoning, discovery loop, GUI use, creative synthesis |
| **Infrastructure** | 7 | Scheduling, plugins, self-healing, claimer, load balancing |
| **Safety** | 6 | Guardrails, rate limits, anomaly detection, audit, human override |
| **Integration** | 5 | Hermes profiles, kanban, cron, MCP bridge, agent mesh |
| **Operations** | 5 | Tracing, SLO monitoring, dashboard, failover, coverage enforcement |

### 5.4 4 ASI Pathways

| Pathway | Description |
|---------|-------------|
| **Autonomous** | Self-directed goal pursuit |
| **Collaborative** | Human-in-the-loop |
| **Swarm** | Decentralized multi-agent coordination |
| **Formal** | Lean/Z3 verified reasoning |

---

## 6. Safety & Governance

### 6.1 Multi-Layer Safety Architecture

1. **Input guardrails**: validate task requests before execution
2. **Execution guardrails**: rate limiting, resource quotas, capability enforcement
3. **Output guardrails**: validate results before delivery
4. **Human override**: CRITICAL tasks require explicit human approval
5. **Audit trail**: append-only immutable log of all safety events

### 6.2 Governance Laws

| Law | Description | Status |
|-----|-------------|--------|
| **Law 1** — Claimer Exclusion | 2+ consecutive failures → 15min exclusion, no re-dispatch to faulting host | Staged |
| **Law 8** — Delegation Credential Parity | Git/crypto operations require credential-env parity in delegates | Staged |
| **Dependency Gating** | Track cannot start until upstream artifacts committed + SHA-referenced | Active |
| **CEO Escalation** | Auto-escalate on SLA breach, overload, silent deadlock, integrity violation | Active |

### 6.3 Safety Plugin Capabilities

- **Rate limiting**: per-minute (60), per-hour (500), concurrent (5)
- **Resource quotas**: CPU, memory, API calls, disk per agent
- **Anomaly detection**: Z-score based behavioral anomaly detection (threshold σ=3.0)
- **Custom rules**: pluggable safety rules per domain
- **Human override hooks**: registered callbacks per task type

---

## 7. Operations & Monitoring

### 7.1 Continuous Monitoring Protocol

| Check | Cadence | Escalation |
|-------|---------|------------|
| Repo liveness | Every 2 hours | CEO |
| Avatar load | Every 2 hours | CEO |
| Trace link integrity | Every 4 hours | CEO |
| Escalation self-check | Every 6 hours | CEO |

### 7.2 CEO Escalation Triggers

Escalation fires when ANY of:
- Repo `main` unreachable for > 24h (SLA breach)
- Avatar `load(3/3)` for > 24h without handoff (track stall)
- Accepted track produces no progress marker for > 72h (silent deadlock)
- Commit references artifact never committed (dependency integrity violation)

### 7.3 Observability Stack

- **Traces**: OpenTelemetry, every loop iteration emits a trace
- **Metrics**: Prometheus-compatible, scraped by dashboard
- **Logs**: structured JSON, shipped to dashboard
- **Health checks**: per-plugin, per-agent, per-service

---

## 8. Delivery Pipeline

### 8.1 Track Lifecycle

```
pending → in_progress → review → completed
              ↓
          cancelled
```

### 8.2 Earned-Completion Gates

Every track has an acceptance gate that must be satisfied before green-light:

| Gate | Requirement |
|------|-------------|
| **Repo exists** | GitHub URL accessible, files visible |
| **Tests pass** | ≥90% coverage per module, all tests green |
| **Spec committed** | Architecture spec committed to repo |
| **Safety review** | Multi-layer safety checks passed |
| **CEO sign-off** | No active escalation triggers |

### 8.3 Dependency Resolution

Every track declares inputs as `@from <avatar>:<artifact-ref>` lines, resolved against committed (not in-flight) artifacts. A track may not start until every declared upstream artifact is committed and referenced by SHA/ref.

---

## 9. Roadmap

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

---

## 10. Acceptance Gates

### 10.1 System-Level Acceptance

- [ ] All products deploy with one config file
- [ ] All agents run in isolated, capability-scoped runtimes
- [ ] All engineers (human or AI) have a single pane of glass
- [ ] All SLIs meet SLOs for 30 consecutive days
- [ ] All governance laws (1, 8, dependency gating, escalation) are enforced
- [ ] 99.9% uptime with self-healing
- [ ] ≥90% test coverage per module

### 10.2 Architecture Meta-Gates

- [ ] No single point of failure across agents, hosts, or tools
- [ ] No agent can access credentials it doesn't hold a capability for
- [ ] No green light without earned-completion evidence
- [ ] No commit without dependency integrity
- [ ] No silent failures — every failure has a trace

---

Author: @cto