# validation-logic

Business logic for the validation platform — owned by the **Data Quality Team**.

This repository contains validation rules, entity helpers, JSON schemas, and the
`business-config.yaml` file that controls which rules are active and how they are
routed. It is the single source of truth for all data quality checks run by the
platform.

## How it connects to the live system

`validation-lib` fetches this repository's contents directly via raw GitHub URLs.
**The `main` branch is production.** When a change is merged to `main`, all running
instances of the validation platform pick it up automatically within 30 minutes
(configurable). No separate deployment step is required.

There is no "production logic folder" elsewhere — this repository _is_ the production
logic.

## Repository structure

```
validation-logic/
├── rules/
│   └── loan/              # Validation rule files (rule_NNN_vN.py)
├── entity_helpers/        # Field mapping helpers (logical → physical)
├── schema_helpers/        # Schema loading utilities
├── models/                # JSON Schema files for each entity version
└── business-config.yaml   # Master config — controls what is live
```

## For the Data Quality Team

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow: how to add a rule,
raise a PR, get it reviewed, and see it go live.

## For platform engineers

The fetch URI is configured in `validation-lib/validation_lib/local-config.yaml`:

```yaml
business_config_uri: "https://raw.githubusercontent.com/<org>/validation-logic/main/business-config.yaml"
```

Changing this URI is how you point an environment at a different branch (e.g. `staging`).
