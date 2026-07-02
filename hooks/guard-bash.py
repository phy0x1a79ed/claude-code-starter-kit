#!/usr/bin/env python3
"""
PreToolUse guard for Bash — blocks destructive commands before they run.

Wire it up in settings.json:

  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [ { "type": "command",
                     "command": "python3 ~/.claude/hooks/guard-bash.py" } ] }
    ]
  }

How it works: Claude Code pipes the tool call to this script as JSON on stdin.
We inspect the command string and, if it matches a destructive pattern, emit a
`deny` decision as JSON on stdout. Anything else exits 0 silently and the command
proceeds. The `permissionDecisionReason` is shown to the model, so it is written
to tell Claude what to do *instead* — not just "no".
"""
import json
import re
import sys

# (pattern, reason) — reason is surfaced to the model, so make it actionable.
RULES = [
    (r"\brm\s+-rf?\s+(/|~|\$HOME)(\s|$)",
     "Refusing `rm -rf` on / or $HOME. Delete a specific subpath instead."),
    (r"\brm\s+-rf?\s+\*",
     "Refusing `rm -rf *` — too broad. Name the exact files to remove."),
    (r"\bgit\s+push\b.*\s--force(?!-with-lease)\b.*\b(main|master)\b",
     "Refusing force-push to main/master. Use --force-with-lease on a feature branch."),
    (r"\bgit\s+reset\s+--hard\b.*\borigin/",
     "`git reset --hard origin/...` discards local work. Stash or branch first, then confirm."),
    (r"\btmux\s+kill-server\b",
     "`tmux kill-server` kills every session for the user. Use `tmux kill-session -t <name>`."),
    (r":\(\)\s*\{\s*:\|:&\s*\}\s*;",
     "Fork-bomb pattern detected. Blocked."),
    (r"\bchmod\s+-R\s+0*777\s+/",
     "Refusing recursive chmod 777 on a root path — security risk."),
    (r"\bdd\b.*\bof=/dev/(sd|nvme|disk)",
     "Refusing raw `dd` to a block device — this can wipe a disk."),
    (r"\bmkfs\.",
     "Refusing to format a filesystem (mkfs)."),
    (r">\s*/dev/(sd|nvme)",
     "Refusing to write directly to a block device."),
    (r"\bcurl\b.*\|\s*(sudo\s+)?(ba)?sh\b",
     "Piping a remote script straight into a shell is risky. Download, read it, then run."),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # never block on a parse error — fail open, not closed
    cmd = (payload.get("tool_input") or {}).get("command", "")
    if not cmd:
        return 0
    for pattern, reason in RULES:
        if re.search(pattern, cmd):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }))
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
