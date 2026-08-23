# Contributing to TaskForge

First off: thank you for considering a contribution to TaskForge. It means a lot.

TaskForge is a small, sharp tool: an in-repo `.agent` file format + a runner
that executes it on GitHub events. We keep scope tight so we can keep it fast,
auditable, and reviewable. Contributions that broaden the surface area (new
agent DSLs, built-in multi-agent orchestration, hosted SaaS plumbing) will be
politely declined until the MVP is solid. See [oss-mission.md](oss-mission.md).

## How to contribute

1. Fork + branch from `main`.
2. Keep PRs focused: one behavior change per PR.
3. `.agent` files are reviewed like code — if you add a new reference agent,
   include its trace artifact as a committed JSON example.
4. `cargo fmt` and `cargo test`. CI runs both on every PR.
5. Add or update docs alongside any schema change.

## Running locally

```bash
cargo build
./target/debug/taskforge run .taskforge/agents/code-reviewer.agent.yml \
    --on pr --trace trace.json
```

## Reporting issues

- Bugs: open a GitHub Issue with the `.agent` file + the trace JSON that
  triggered the bug.
- Design proposals: open an Issue with `proposal:` label. Big ideas should land
  in a discussion first so we don't waste your time on a rejected PR. See our
  philosophy in [oss-mission.md](oss-mission.md).

## Code of conduct

Please be excellent to each other. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

We follow the "no jerks" rule: kindness is a technical requirement.

## License

By contributing, you agree your patches are licensed under Apache 2.0.
