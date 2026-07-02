# Claude Code Starter Kit (free)

A few real, tested [Claude Code](https://docs.claude.com/en/docs/claude-code)
extensions to make your setup faster and safer — plus the mental model for
building your own. Everything here is format-correct and smoke-tested.

## What's inside

**Hooks** — deterministic guardrails & automation (they fire whether or not the
model "remembers"):
- `hooks/guard-bash.py` — a `PreToolUse` guard that blocks destructive shell
  commands (`rm -rf /`, force-push to `main`, fork bombs, `dd` to a disk,
  `curl | sh`, …) and tells the model what to do instead.
- `hooks/session-context.py` — a `SessionStart` hook that injects your branch,
  uncommitted changes, recent commits, and `NOTES.md` into context, so every
  session opens knowing where you left off.

**Slash command**
- `commands/commit.md` → `/commit` — groups changes by intent and writes commit
  messages that match your repo's existing style. Note the `` !`git status` ``
  lines: they run *when you invoke the command*, so Claude sees your diff with zero
  round-trips.

## The mental model (why these work)

Claude Code has four extension points, each for a different job:

- **Hooks** — *enforce.* Code that runs on an event (before/after a tool, at
  session start). The only mechanism that can **guarantee** something, because it
  isn't a prompt the model can forget. Guardrails and automation live here.
- **Slash commands** — *trigger a workflow* you invoke with `/name`.
- **Subagents** — *isolate a job* in its own context, often on a cheaper model
  (big cost win).
- **Skills** — *teach a procedure* the model auto-invokes when your description matches.

The hook contract: Claude pipes a JSON event to your script on **stdin**; for
gating hooks you print a JSON decision on **stdout**. Golden rule: **fail open** —
if your hook errors, exit 0 and let the action through, so a buggy guard never
bricks the agent. Both hooks here follow that.

## Install

1. Copy `hooks/*.py` to `~/.claude/hooks/` and `commands/commit.md` to
   `~/.claude/commands/`.
2. Add to your `~/.claude/settings.json`:

       {
         "hooks": {
           "PreToolUse": [
             { "matcher": "Bash", "hooks": [
               { "type": "command", "command": "python3 ~/.claude/hooks/guard-bash.py" } ] }
           ],
           "SessionStart": [
             { "hooks": [
               { "type": "command", "command": "python3 ~/.claude/hooks/session-context.py" } ] }
           ]
         }
       }

3. Start a new session — you should see your project context printed at the top.
   Requires Python 3 on PATH.

## Want the full kit?

This is the starter subset. The **Claude Code Pro Kit** adds:

- Two more hooks — `protect-paths.py` (block edits to secrets/lockfiles/CI/vendored
  code) and `auto-format.py` (format on every edit).
- Two more commands — `/review` (multi-agent review with parallel cheap lenses +
  skeptical confidence scoring) and `/scope` (a verified context map before you code).
- Three subagents — `test-writer`, `debugger`, `pr-describer` (cost-tiered across
  Sonnet/Haiku).
- The `onboard-claude` skill — auto-writes a project's `CLAUDE.md` from its real conventions.
- A complete, mergeable `settings.json`.
- **The full field guide** — the hook contract in depth, the cost-tiering strategy
  that makes expensive-model sessions cheap, and the cross-cutting patterns
  (scan-cheap-verify-skeptical, context injection, guard-with-code) that make it all pay off.

➡️ **Get the Pro Kit: [ko-fi.com/claudecodekit](https://ko-fi.com/claudecodekit)**

## License
MIT. Use it, adapt it, ship it.

---
*Built with the help of an AI coding agent and tested for correctness.*
