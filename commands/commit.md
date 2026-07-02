---
description: Stage, group, and commit changes with well-written messages
argument-hint: "[optional scope hint, e.g. 'only the auth refactor']"
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git log:*)
---

Current repository state:

- Status: !`git status --short`
- Staged diff: !`git diff --cached --stat`
- Unstaged diff: !`git diff --stat`
- Recent commit style: !`git log --oneline -5 --no-decorate`

Create one or more git commits from the current changes. $ARGUMENTS

Follow these rules:

1. **Group by intent, not by file.** If the working tree mixes unrelated changes
   (e.g. a bug fix + a docs tweak + a refactor), make *separate* commits — stage
   each group with explicit paths, don't `git add -A` everything into one blob.
2. **Match the repo's existing message style** shown above (tense, prefix
   convention like `feat:`/`fix:`, capitalization, length).
3. Write a concise subject (≤ 72 chars) and, when the change isn't obvious, a
   short body explaining *why*. No filler, no emojis unless the repo uses them.
4. **Never** commit secrets, `.env` files, large binaries, or debug scratch.
   Call them out instead of committing them.
5. Do not push. Show the resulting `git log --oneline -3` when done.

If the scope hint above narrows what to commit, honor it and leave the rest staged/unstaged as-is.
