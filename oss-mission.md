# Company Open Source Mission & Flagship Spec

## The one flagship: TaskForge

After weighing the three ideas, we are committing all engineering weight behind
**TaskForge** — GitHub-native agentic development where agent behavior lives as
declarative `.agent` files directly in the repository, auto-runs on PRs, and
leaves auditable traces in the PR comments.

## Why TaskForge wins the "uniquely winnable" filter

- **No incumbent owns the model layer.** LangChain is workflow plumbing; Taskify,
  Agent.ai, etc. are SaaS products with no in-repo, version-controlled agent
  primitive. There is no GitHub-native `.agent` file format today. We get to
  define the standard.
- **Distribution is free.** It lives *inside* repos on GitHub — the exact place
  developers already are. No separate login, no separate dashboard. Every
  contributor to a repo is exposed to it automatically. This is how a grass-roots
  OSS project becomes a de-facto standard.
- **Defensible moat as community, not code.** The core runtime is small. The
  value is the public registry of `.agent` definitions + a convention for
  trace/observation. Hard for a SaaS-first competitor to replicate without
  rebuilding developer trust once we own the in-repo primitive.
- **Immediate productization path.** OSS runtime is the lead. Paid tiers become
  hosted runner fleet, private `.agent` stores, and enterprise policy control.
  Classic OSS-with-a-commercial-axon.

## What we are NOT building (and why we rejected the others)

- **AgentOS.** Correct analysis: multi-agent swarms need a wire standard. But
  "write a lightweight runtime that works with any LLM" is a
  solutions-looking-for-a-problem without a distribution beachhead. LLM
  abstraction layers are table stakes, not differentiation. Becomes a
  maintenance tail with weak discovery. Rejected for *now* — we will consume
  (not build) the swarm layer; TaskForge agents can call any LLM provider via
  the model field in the `.agent` file.
- **SkillSync.** A decentralized skill registry is elegant but requires network
  effects *before* product value materializes. Chicken-and-egg on the registry
  graph. Better as a future module *inside* TaskForge (an `.agent` skill can
  reference a registry skill), not as its own flagship.

## TaskForge — the spec (crisp)

### 1. What it is
A GitHub App + lightweight CLI that turns repo-stored `.agent` definitions into
runnable, observable agents. Agents are versioned, reviewed, and auditable like
code.

### 2. The `.agent` file format
YAML, stored at `.taskforge/agents/<name>.agent.yml` (or root-level
`<name>.agent.yml`). Example:

```yaml
# .taskforge/agents/code-reviewer.agent.yml
apiVersion: taskforge.dev/v1
kind: Agent
metadata:
  name: code-reviewer
spec:
  description: "Reviews PRs for security + test coverage"
  model: "anthropic/claude-3.5-sonnet"
  triggers:
    - event: pull_request
      actions: [opened, synchronize]
  prompts:
    system: |
      You are a senior reviewer. Flag security issues, missing tests, ...
    on_event: |
      PR title: {{.PR.Title}}
      Diff: {{.PR.Diff}}
  tools:
    - name: github
      config: {}
    - name: shell
      config: { image: "node:20", timeout: "300s" }
  outputs:
    - type: pr_comment
    - type: artifact
      name: review-report
```

### 3. Execution model
- A self-hosted-friendly runner (`taskforge run <agent> --on <event>`) executes
  agents in isolated containers, streams logs live to a trace.
- GitHub App listens for `pull_request` / `issue_comment` events, resolves the
  matching `.agent` file from the repo, launches a run, and writes results back
  as PR comments + a structured trace artifact.
- Runs are idempotent + cancellable. Each run = a `/trace/<run-id>.json` record
  stored as a PR artifact and optionally pushed to a trace UI.

### 4. Non-goals (keeps scope ruthless)
- No general multi-agent orchestration engine. One agent = one `.agent` file
  execution per event. (AgentOS territory stays a future layer.)
- No hosted SaaS by default — run locally or via the GitHub Action. Commercial
  offering = the managed runner pool, not the runtime itself.
- No language lock-in. Runtime is Rust core + language-agnostic agent I/O so any
  LLM provider can be dropped in.

### 5. First MVP slice (3 months)
1. `.agent` schema + YAML parser.
2. `taskforge run` CLI that runs an agent against a local dir, prints trace.
3. GitHub App that triggers an agent on PR open, posts a comment.
4. Trace artifact + `--follow` live logs.
5. Reference agents: `code-reviewer`, `lint-fixer`.

## Stack justification
- **Rust (core runtime)** — fast startup, single static binary, trivial to ship
  as a GitHub Action runner; memory-safe for shell isolation. Boring-for-prod
  wins.
- **YAML for `.agent` schema** — developers already read/write YAML; no new DSL
  to learn. Schema validated with a JSON Schema.
- **GitHub Actions / App model** — we avoid standing our own SaaS infra;
  leverage GitHub's existing auth + runner model. Distribution is a GH App
  install + one `.taskforge/` folder in the repo.
- **JSON trace format** — language-neutral; any observability tool can ingest.
- **Future commercial axon** — managed isolated runners + private agent
  registries, hosted by us. The runtime stays OSS.

## License
Apache 2.0 — encourages adoption, allows paid hosting layer without the
copyleft friction that scares enterprise adopters.

## Success =
- 100 repos adopting a `.agent` file within 6 months of launch.
- A PR review trace being posted in a real OSS project as a merged PR comment.
- A public trace directory that demonstrates the standard.

Owner: @cto — ship the spec, scaffold the repo, hand off to engineering.
