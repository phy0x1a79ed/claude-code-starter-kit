#!/usr/bin/env python3
"""
SessionStart hook — injects live project context at the top of every session.

Wire it up in settings.json:

  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command",
                     "command": "python3 ~/.claude/hooks/session-context.py" } ] }
    ]
  }

Whatever this prints on stdout is added to Claude's context when a session
starts, so it always opens knowing the branch, what changed, recent history, and
any notes you left. This is the cheap-but-huge win most setups miss: no more
"what were we doing?" at the start of each session.
"""
import subprocess
import sys


def sh(cmd):
    try:
        out = subprocess.run(cmd, shell=True, capture_output=True,
                             text=True, timeout=10)
        return out.stdout.strip()
    except Exception:
        return ""


def section(title, body):
    return f"## {title}\n{body}\n" if body else ""


def main() -> int:
    if sh("git rev-parse --is-inside-work-tree 2>/dev/null") != "true":
        return 0

    branch = sh("git branch --show-current")
    status = sh("git status --short")
    log = sh("git log --oneline -8 --no-decorate")
    # A NOTES.md / TODO.md at repo root is a great place to leave yourself a note.
    notes = sh("head -40 NOTES.md 2>/dev/null || head -40 TODO.md 2>/dev/null")

    out = ["# Session context (auto-injected)\n"]
    out.append(section("Branch", f"`{branch}`"))
    out.append(section("Uncommitted changes",
                       f"```\n{status}\n```" if status else "_clean tree_"))
    out.append(section("Recent commits", f"```\n{log}\n```"))
    out.append(section("Notes to self", notes))
    print("\n".join(p for p in out if p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
