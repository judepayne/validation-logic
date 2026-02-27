# Contributing to validation-logic

This guide is for members of the **Data Quality Team** who write and maintain
validation rules. It covers the day-to-day workflow, how changes go live, and
what to do when something needs to be rolled back.

---

## Not sure where to start? Raise an issue

If you've spotted a problem with an existing rule, want to request a new one, or
have a question about the data model — but aren't ready to make a change yourself
— **raise a GitHub issue**. No coding or Git knowledge required.

[**→ Raise a Data Quality Issue**](../../issues/new/choose)

The form asks for a plain-English description of the problem or request, an
example if you have one, and the business context. The DQ team lead will triage
it and either action it directly or assign it to the right person.

---

## The golden rule: `main` is live

The `main` branch of this repository is directly connected to the production
validation platform. When your change is merged to `main`, the platform picks it
up automatically within 30 minutes — **no deployment step, no ticket to raise,
no one to notify.**

This means:
- Changes are reviewed and approved _before_ merge, not after
- You cannot push directly to `main` (branch protection prevents it)
- Every change to `main` has an audit trail: who proposed it, who approved it, and why

---

## What you can change

| File / folder | Who owns it | What changes here |
|---|---|---|
| `rules/loan/rule_NNN_vN.py` | DQ analysts | Add new rules or new versions of existing rules |
| `business-config.yaml` | DQ team lead | Activate/deactivate rules, change rule routing, add schema mappings |
| `models/*.json` | DQ team lead + platform engineer | New or updated JSON schemas |
| `entity_helpers/` | Platform engineer | Field mapping definitions (logical ↔ physical) |
| `schema_helpers/` | Platform engineer | Schema loading utilities |

**Rule files are immutable once published.** Never edit a rule file that has already
been merged to `main`. If a rule needs to change, create a new versioned file
(e.g. `rule_007_v2.py`) and update `business-config.yaml` to point to the new version.
This preserves the audit trail and makes rollback clean.

---

## Day-to-day workflow

### Step 1 — Create a branch

In VS Code (Source Control panel) or on GitHub:

```
Branch name convention:  feature/rule-007-exposure-limit
                         fix/rule-003-status-typo
                         config/activate-thorough-ruleset
```

Never work directly on `main`.

### Step 2 — Make your changes

For a new rule, you will typically change two files:

1. **Create the rule file** — e.g. `rules/loan/rule_007_v1.py`
2. **Update `business-config.yaml`** — add the new `rule_id` to the appropriate ruleset(s)

See the [Rules Guide](https://github.com/judepayne/validation-lib/blob/main/docs/RULES-GUIDE.md)
for the full rule file format and examples.

### Step 3 — Open a pull request

Push your branch and open a PR on GitHub. The PR template will prompt you to fill in:
- What the rule does
- What business requirement it addresses
- How you tested it

Be specific in the description — it becomes the permanent record of _why_ this change
was made.

### Step 4 — Automated checks run

GitHub Actions runs automatically within a minute of opening the PR:

- **Python syntax check** — catches typos and import errors in rule files
- **Ruff lint** — enforces code style
- **Config validation** — checks `business-config.yaml` is valid YAML with the
  required structure

If any check fails, the PR cannot be merged. Fix the issue and push again — the
checks re-run automatically.

### Step 5 — Peer review

A second DQ analyst reviews your changes. They check:
- Does the rule logic match the described business requirement?
- Are the field names correct (logical names, not physical paths)?
- Does the rule return the right status for valid and invalid data?
- Is `business-config.yaml` updated correctly?

Reviewers leave comments on the PR. You can push follow-up commits to address them.

### Step 6 — Team lead approval

The DQ team lead gives final approval. For changes to `business-config.yaml` or
`models/`, a platform engineer co-approves.

### Step 7 — Merge

Once all required approvals are in and all checks pass, merge the PR. The `main`
branch updates, and the change is live within 30 minutes.

For an immediate rollout (e.g. urgent fix), ask a platform engineer to clear the
cache on the relevant service. This is a one-command operation on their side.

---

## Going live — the full picture

```
Your branch
    │
    │  (automated checks: lint, syntax, config validation)
    │
    ▼
Pull Request ──► Peer review ──► Team lead approval
    │
    ▼
Merged to main  ←── this is the moment of deployment
    │
    │  (validation-lib fetches main automatically within 30 min)
    │
    ▼
Live on all running instances
```

You do not need to:
- Raise a deployment ticket
- Notify the platform team
- Copy files anywhere
- Restart any service

The platform fetches `business-config.yaml` and all rule files directly from `main`
via GitHub raw URLs. The repository _is_ the deployment.

---

## Rollback

If a merged change causes problems, roll it back via a revert PR:

1. On GitHub, open the PR that introduced the problem
2. Click **"Revert"** — GitHub creates a new PR that undoes the change
3. The revert PR goes through the same review process (but can be expedited)
4. On merge, the bad change is undone within 30 minutes

The original change is never deleted from the history — the revert is a new commit
that cancels it out. This preserves the full audit trail.

For an immediate rollback before the revert PR can be reviewed, ask a platform
engineer to point the service at the last known-good commit temporarily.

---

## Repository setup (for administrators)

The following settings must be configured on GitHub for the workflow to function
correctly. **This is a one-time setup task** for whoever administers the repository.

### Branch protection on `main`

In **Settings → Branches → Branch protection rules**, add a rule for `main`:

- [x] Require a pull request before merging
- [x] Require approvals — set to **2** (peer + team lead)
- [x] Dismiss stale pull request approvals when new commits are pushed
- [x] Require review from Code Owners
- [x] Require status checks to pass before merging
  - Add status check: `validate` (this is the GitHub Actions job name)
- [x] Require branches to be up to date before merging
- [x] Do not allow bypassing the above settings (apply to administrators too)

### CODEOWNERS

The `.github/CODEOWNERS` file (already in this repo) routes PR reviews automatically.
No analyst needs to remember who to add as a reviewer — GitHub does it.

### Required tooling for analysts

| Tool | Purpose | Required? |
|---|---|---|
| VS Code | Code editing, built-in Git UI | Recommended |
| GitHub Copilot (VS Code extension) | Python autocomplete for rule writing | Recommended |
| GitHub Pull Requests (VS Code extension) | Create and review PRs without leaving VS Code | Optional |
| Python 3.11+ | Local testing of rules before opening a PR | Optional but useful |

---

## Quick reference

| Task | How |
|---|---|
| Start a new rule | Create branch → write `rules/loan/rule_NNN_vN.py` → update `business-config.yaml` → open PR |
| Modify an existing rule | Create a new versioned file (`rule_NNN_v2.py`) — never edit the original |
| Activate a rule in a ruleset | Edit `business-config.yaml`, add `rule_id` under the correct schema key |
| Deactivate a rule | Edit `business-config.yaml`, remove or comment out the `rule_id` |
| Roll back a change | Open the original PR on GitHub → click Revert → merge the revert PR |
| Force an immediate refresh | Ask a platform engineer to clear the logic cache |
| Check what's currently live | Look at `business-config.yaml` on `main` |
| Understand a rule's field names | See `entity_helpers/loan_v1.json` for the logical → physical mapping |
