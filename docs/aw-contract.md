# AW Contract

AW is the driver of this repository.

## Input
Natural-language product intent, for example: "9/14〜9/20 東京の無銭・フリーアイドルライブを探す".

## AW responsibilities
- Normalize intent and constraints.
- Create/update design Issues.
- Derive domain ontology and data schema requirements.
- Break implementation into executable Issues.
- Drive Vue implementation in repository code.
- Validate `.data/` fixtures against the design.
- Run review and deployment checks.

## Storage rule
- Issues = design/specification/decisions/tasks.
- Workflow = AW driver/orchestration.
- Repository = executable code.
- `.data/` = event data and fixtures.

Do not duplicate the canonical design in source code or README when it belongs in an Issue.
