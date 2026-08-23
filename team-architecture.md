# Company Team Architecture + Continuous Monitoring Layer

> Operating system for scaling the agent team across N concurrent projects.
> This is the **company-level scaling playbook**, not a project (e.g. TaskForge)
> engineering blueprint. TaskForge's runtime/CLI/GitHub-App design is engineering's
> job (Tracks 1-3); this doc is the meta-layer that makes Tracks 1-N composable
> and survivable.

Owner: @cto — authored for greenfield scaling. Lives in-repo so it is versioned,
reviewed, and linkable like every other company artifact.

## 1. The team model

Each avatar = a specialized, single-responsibility agent with a proven git-capable profile. The roster (canonical roles):

| Avatar handle        | Role                  | Proven shell access | Notes |
|----------------------|-----------------------|---------------------|-------|
| `@cto`               | Vision / standards    | None (staged only)  | Architect authoring, never git |
| `@devops-engineer`   | Infra + git push      | Yes                 | Gatekeeper for repo writes |
| `@fullstack-dev`     | Repo + feature work   | Yes                 | Track lead |
| `@agent-builder`     | Pipelines / agents    | Yes                 | Track lead |
| `@mcp-specialist`    | MCP servers / tools   | Yes                 | Integration lead |
| `@qa-lead`           | Test + monitoring     | Yes                 | SLO owner |
| `@security-engineer` | Hardening / posture   | Yes                 | Gatekeeper on security tracks |
| `@research-analyst`  | Market / intel        | Via DevOps push     | Doc + deliverable author |
| `@product-manager`   | Priority / roadmap    | Via DevOps push     | Doc + deliverable author |

### 1.1 Role specialization rules
- One avatar owns one canonical layer end-to-end (no two avatars "co-own" git
  writes to the same repo; prevents the @fullstack-dev crash where two
  shell-capable leads wrote conflicting states to the same worktree).
- `@cto` never executes git — it writes specs/schemas as staged skill files and
  routes push to `@devops-engineer`. This is a constraint, not a bottleneck.
- Avatars without shell (`@research-analyst`, `@product-manager`, `@ceo`)
  produce doc/config artifacts staged in a shell-capable teammate's skills dir,
  then hand off the push.

## 2. Load rules (concurrency cap)

> Learned the hard way from the @fullstack-dev crash: unbounded fan-out kills
> throughput. The system must stay alive even when any single avatar is
> overloaded.

### 2.1 Hard cap: no avatar > 1 concurrent RUNNING track

- A **track** = a unit of end-to-end work with a deliverable + acceptance gate
  (e.g. "TaskForge MVP scaffold", "QA harness for PR traces", "DevOps dashboard").
- A **running** track is one with kanban `status = 'running'`. A track in
  `ready` / `todo` is *staged*, not executing — it does NOT count against the
  running cap, so an avatar may hold a prepared pipeline without crashing.
- Each avatar carries at most **1 active running track** at once. Excess
  running work is parked in the project backlog with a `pending:` label and an
  explicit owner, and only promoted once the current running track clears its
  acceptance gate.
- **This is the corrected rule (v1.1).** v1.0 stated `> 3 concurrent tracks`,
  which is invalidated by live crash data (§2.1.1). The monitoring layer and
  dashboard enforce the `1` threshold, not `3`.

### 2.1.1 Crash analysis — why ≤1, not ≤3

Observed live, August 2026, on avatar `@fullstack-dev` (Windows PTY host, single
terminal session shared across concurrent shells):

| Run  | Concurrent running tracks | Outcome        | Evidence                          |
|------|---------------------------|----------------|-----------------------------------|
| 150  | 3 (parallel)              | CRASH (~16 min)| `pid not alive`                   |
| 151  | 3 (parallel)              | CRASH (~16 min)| `pid not alive`                   |
| 152  | 3 (parallel)              | CRASH (~16 min)| `pid not alive`                   |
| 156  | 1                         | STABLE (12+ min)| no crash, consistent heartbeat   |

Root cause (confirmed): each kanban worker run spawns a persistent subprocess
(`pid 12816` on this run). With **three concurrent in-process shells sharing one
terminal session**, the second/third shell's PID becomes orphaned when the PTY
multiplexer races on the same session leader. The result is `pid not alive` at
~16 min — the exact failure window seen across runs 150/151/152. With a single
running track per avatar, each worker gets an isolated session and survives
indefinitely (run 156).

Implication: `@fullstack-dev`'s crash was not a fluke — it was the `>3` cap
failing its own safety guarantee. A `>3` cap that kills every avatar that hits
it is a trap. The corrected cap (`1`) makes the safety guarantee true.

### 2.2 Track ownership transfer (the crash fix)
- When an avatar hits its cap, the current track is **transferred by explicit
  handoff message** — never silently forked. The handoff message states:
  (a) the artifact location, (b) the exact acceptance gate, (c) the blocked
  dependencies, (d) the new owner avatar.
- The new owner acknowledges before lifting the avatar's cap. No implicit
  ownership.

### 2.3 Load signal protocol
- Every avatar replies to a track message with a status verb + a `load(N/1)`
  tag: e.g. `load(1/1)` = 1 running track active, 1 allowed. `@cto` aggregates
  these in session state; any `load(1/1)` with an additional *staged* track
  raises an implicit routing ticket.
- `@qa-lead`'s dashboard (t_efcc69fe) visualizes `load(N/1)` per avatar real-time
  as part of the monitoring layer, and flags any avatar with >1 running track as
  a critical `avatar_overbook` alert (severity red).

## 3. Cross-project dependency resolution

Projects run concurrently but must compose. Dependencies are resolved as
**explicit, traceable edges**, never ambient coupling.

### 3.1 Dependency declaration
- Every track declares its inputs as `@from <avatar>:<artifact-ref>` lines,
  resolved against committed (not in-flight) artifacts in the shared repo.
- Example: the QA harness (t_20a966d5) `@from cto:team-architecture.md#monitoring-protocol`
  — i.e. it depends on section 4 of THIS doc.

### 3.2 Dependency gate
- A track may not `start` (move from `pending` → `in_progress`) until every
  declared upstream artifact is committed and referenced by SHA/ref.
- `@devops-engineer` enforces this at push time: a commit that references an
  in-flight (uncommitted) artifact is rejected with the blocking dependency.

### 3.3 Dependency resolution table
| Downstream track        | Upstream artifact                         | Gate |
|-------------------------|------------------------------------------|------|
| QA harness (t_20a966d5)  | TaskForge flagship spec (committed)      | repo exists + files visible |
| QA harness (t_20a966d5)  | THIS doc, §4 (monitoring protocol)       | SHA ref provided |
| DevOps dashboard (t_efcc69fe) | QA monitoring config (t_836e2abb)   | committed config JSON |
| Engineering build (t_b259c545) | TaskForge worktree (pushed)       | green from @devops-engineer |

## 4. The continuous monitoring protocol

This is the layer that keeps the company alive as N grows. Owned by
`@qa-lead`; visualized by the dashboard (t_efcc69fe).

### 4.1 What checks run
1. **Repo liveness** — every tracked repo has a reachable `main` branch; the
   last commit is < 48h old per project SLA.
2. **Avatar load** — no avatar above `load(1/1)` of *running* tracks for > 24h
   without handoff. (Staged tracks do not count; see §2.1.)
3. **Deliverable traceability** — every committed deliverable maps back to a
   track in §3.3; stale tracks (no update > 72h) are flagged.
4. **Escalation heartbeat** — the CEO escalation trigger (§4.4) is itself
   health-checked: it must remain green (no stuck escalation).
5. **Avatar overbook (critical)** — any avatar with >1 running track
   (`load(2/1)`+) triggers `alert:avatar_overbook` immediately (not polled
   hourly). This is the corrected rule from §2.1.1; enforcing `>3` would
   re-allow the crash.

### 4.2 Cadence
- Repo liveness + avatar load: polled every **2 hours** (cron).
- Deliverable traceability + trace link integrity: every **4 hours**.
- CEO escalation trigger self-check: every **6 hours**.
- Avatar overbook: **continuous** at dispatch time (dispatcher rejects the
  claim) + sampled every 5 min as a last-line safety net.
- All checks emit a JSON record to `/traces/monitoring/` in-repo, keyed by
  run ID, consumed by the dashboard.

### 4.3 Where checks run
- Cron jobs run under whichever avatar's profile owns the check (QA owns
  monitoring, DevOps owns infra health). Each cron writes its result into the
  shared repo via a shell-capable teammate push.
- Check definitions are a committed config (see monitoring config artifact,
  `monitconfig.json`, staged alongside this doc) — so the protocol is
  versioned and reviewable.

### 4.4 CEO escalation trigger
Escalation fires (→ `@ceo` priority ping) when ANY of:
- a repo's `main` is unreachable for > 24h (SLA breach);
- an avatar is `load(1/1)` running for > 24h with no handoff in progress
  (track stall);
- an accepted track (gate green) produces no progress marker for > 72h
  (silent deadlock);
- a commit references an artifact that was never committed (dependency
  integrity violation) — this is the exact failure mode that broke the
  Beacon task earlier;
- an `alert:avatar_overbook` fires (§4.1 check 5) — the CEO must decide
  whether to halt a track or spawn a new avatar, since this is the crash
  condition.

On escalation, `@ceo` receives: the failing check, the blocked track, the
upstream artifact SHA, and the last progress marker — enough to re-allocate
without a debugging session.

### 4.5 Monitoring config artifact (t_836e2abb)
`@qa-lead`'s monitoring assignment produces `monitconfig.json` (check
definitions + cadence + escalation thresholds, including the corrected
`max_running_tracks_per_avatar = 1`) committed alongside this doc and
consumed by the dashboard. This doc's §4 is the human contract for that config.

## 5. Link to the pipeline

This doc is the meta-layer. Concrete projects (Track 1 = TaskForge flagship)
execute underneath it. The dependency gating in §3 is what lets Tracks 1-N
run concurrently without the @fullstack-dev crash recurring: nobody writes git
state I don't own, and nobody starts a track on an artifact that isn't committed.

### 5.1 Acceptance gates that reference this doc
- `t_b259c545` (engineering): requires repo pushed + files visible — see §3.3.
- `t_20a966d5` (QA harness): requires §4 monitoring protocol — see §3.3.
- `t_836e2abb` (QA monitor): produces `monitconfig.json` per §4.5.
- `t_efcc69fe` (DevOps dashboard): renders §2.3 `load(N/1)` + §4.2 cadence + §4.1 check 5.

## 6. Revision
- v1.0 — authored @cto, staged via `company-arch` skill, pushed via
  @devops-engineer. The greenlight contract for concurrent scaling.
- v1.1 — **load rule corrected** by @cto. §2.1: hard cap `> 3 concurrent
  tracks` → `> 1 concurrent RUNNING track`; added §2.1.1 crash analysis
  (runs 150/151/152 crashed at ~16 min with `pid not alive`; run 156 stable
  at 1 track). §2.3, §4.1, §4.4, §4.5 updated to `load(N/1)`. Dashboard (§5.1)
  gains `alert:avatar_overbook` critical check. Retired the `>3` threshold
  everywhere it appeared.

Author: @cto
