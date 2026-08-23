# TaskForge

**GitHub-native agentic development.** Declare an agent as a single `.agent.yml`
file in your repo, and it runs automatically on pull requests — auditable,
observable, and version-controlled like any other source file.

> Think "GitHub Actions for LLM agents" — but the agent definition lives in your
> repo, ships in your diff, and gets code-reviewed like everything else.

## Why?

Today, agentic dev tools are:

- **SaaS-first** — you push your code + diff to someone else's server.
- **Separate products** — a whole new login, dashboard, and bill.
- **Black-box traces** — the review, lint, or fix output lives in a UI you can't
  link to, reference, or merge.

TaskForge flips that. Your agent *is* a file in your repo. It runs in the same
environment GitHub Actions already runs in. Its trace comes back as a PR comment
and an artifact you can `@link` in other issues.

## Quick start

```bash
# 1. Install (once)
curl -sfL https://taskforge.dev/install | sh

# 2. Add an agent to your repo
cat > .taskforge/agents/code-reviewer.agent.yml <<'EOF'
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
      You are a senior reviewer. Flag security issues and missing tests.
    on_event: |
      PR title: {{.PR.Title}}
      Diff: {{.PR.Diff}}
  tools:
    - name: github
    - name: shell
  outputs:
    - type: pr_comment
EOF

# 3. Run it locally against a diff
taskforge run code-reviewer --on pr --trace trace.json

# 4. (Or) add the GitHub App, and it auto-runs on every PR.
```

See the [full spec](oss-mission.md) and [CONTRIBUTING](CONTRIBUTING.md).

## The flagship spec

We picked TaskForge as our one open-source flagship. Read the mission and full
spec in [oss-mission.md](./oss-mission.md).

## Project layout

```
.
├── oss-mission.md            # company OSS mission + flagship spec
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── spec/                     # .agent YAML schema (JSON Schema)
│   └── agent.schema.json
└── (rust core lands here)
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
