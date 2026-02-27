## Summary
<!-- One sentence: what does this change do? -->

## Business requirement
<!-- What data quality requirement or business rule does this address? -->
<!-- Link to ticket if applicable: -->

## Type of change
- [ ] New rule
- [ ] New version of an existing rule (new file created, original untouched)
- [ ] `business-config.yaml` update only (activate/deactivate/re-route rules)
- [ ] New schema version
- [ ] Other (describe below)

## Rule details
<!-- Complete this table if adding or modifying a rule. -->

| Field | Value |
|---|---|
| Rule ID | `rule_NNN_vN` |
| Entity type | e.g. `loan` |
| Ruleset(s) affected | e.g. `quick`, `thorough` |
| Expected status — valid data | PASS / WARN |
| Expected status — invalid data | FAIL / NORUN |

## Testing
<!-- Describe how you verified this rule produces the correct result. -->
<!-- Paste example input and output if helpful. -->

- [ ] Tested against valid example data → correct status returned
- [ ] Tested against invalid example data → correct status returned
- [ ] `business-config.yaml` updated to include/route the rule

## Checklist
- [ ] Rule file is named correctly: `rule_NNN_vN.py`
- [ ] Rule class is named exactly `Rule` (capital R)
- [ ] Rule uses `self.entity.<logical_name>` — no raw dict access
- [ ] No existing published rule files were edited (versioned file created instead)
- [ ] PR description explains _why_ this change is needed, not just what it does
