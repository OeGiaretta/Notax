from app.core.rules.financial_rules import validate_financial_rules
from app.core.rules.item_rules import validate_item_rules
from app.core.rules.required_fields import validate_required_fields
from app.core.rules.cnpj_rules import validate_cnpj_rules
from app.core.rules.date_rules import validate_date_rules

from app.schemas.validation import (
    ValidationIssue,
    ValidationResult,
    ValidationSummary,
)

def calculate_score(issues: list[ValidationIssue]) -> int:
    score = 100

    for issue in issues:
        if issue.severity == "error":
            score -= 20
        elif issue.severity == "warning":
            score -= 10
        elif issue.severity == "info":
            score -= 2

    return max(score, 0)


def determine_status(issues: list[ValidationIssue]) -> str:
    severities = {issue.severity for issue in issues}

    if "error" in severities:
        return "error"

    if "warning" in severities:
        return "warning"

    return "ok"


def build_summary(issues: list[ValidationIssue]) -> ValidationSummary:
    errors = sum(1 for issue in issues if issue.severity == "error")
    warnings = sum(1 for issue in issues if issue.severity == "warning")
    info = sum(1 for issue in issues if issue.severity == "info")

    return ValidationSummary(
        total_issues=len(issues),
        errors=errors,
        warnings=warnings,
        info=info,
    )

def validate_invoice_data(data: dict) -> ValidationResult:
    issues: list[ValidationIssue] = []

    issues.extend(validate_required_fields(data))
    issues.extend(validate_financial_rules(data))
    issues.extend(validate_item_rules(data))
    issues.extend(validate_cnpj_rules(data))
    issues.extend(validate_date_rules(data))

    summary = build_summary(issues)
    score = calculate_score(issues)
    status = determine_status(issues)

    return ValidationResult(
        status=status,
        score=score,
        summary=summary,
        issues=issues,
    )