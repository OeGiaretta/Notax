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

    if not data.get("invoice_number"):
        issues.append(
            ValidationIssue(
                code="MISSING_INVOICE_NUMBER",
                message="Invoice number is missing.",
                severity="error",
                field="invoice_number",
            )
        )

    if not data.get("issuer_cnpj"):
        issues.append(
            ValidationIssue(
                code="MISSING_ISSUER_CNPJ",
                message="Issuer CNPJ is missing.",
                severity="error",
                field="issuer_cnpj",
            )
        )

    if not data.get("recipient_cnpj"):
        issues.append(
            ValidationIssue(
                code="MISSING_RECIPIENT_CNPJ",
                message="Recipient CNPJ is missing.",
                severity="error",
                field="recipient_cnpj",
            )
        )

    total_value = data.get("total_value")
    if not total_value:
        issues.append(
            ValidationIssue(
                code="MISSING_TOTAL_VALUE",
                message="Total value is missing.",
                severity="error",
                field="total_value",
            )
        )
    elif total_value in ["0", "0.00", 0, 0.0]:
        issues.append(
            ValidationIssue(
                code="ZERO_TOTAL_VALUE",
                message="Total value is zero.",
                severity="warning",
                field="total_value",
            )
        )

    items = data.get("items", [])

    if not items:
        issues.append(
            ValidationIssue(
                code="MISSING_ITEMS",
                message="No items found in invoice.",
                severity="error",
                field="items",
            )
        )

    for index, item in enumerate(items, start=1):
        prefix = f"items[{index - 1}]"

        if not item.get("code"):
            issues.append(
                ValidationIssue(
                    code="MISSING_ITEM_CODE",
                    message=f"Item {index} is missing product code.",
                    severity="warning",
                    field=f"{prefix}.code",
                )
            )

        if not item.get("name"):
            issues.append(
                ValidationIssue(
                    code="MISSING_ITEM_NAME",
                    message=f"Item {index} is missing product name.",
                    severity="warning",
                    field=f"{prefix}.name",
                )
            )

        if not item.get("ncm"):
            issues.append(
                ValidationIssue(
                    code="MISSING_NCM",
                    message=f"Item {index} is missing NCM.",
                    severity="error",
                    field=f"{prefix}.ncm",
                )
            )

        if not item.get("cfop"):
            issues.append(
                ValidationIssue(
                    code="MISSING_CFOP",
                    message=f"Item {index} is missing CFOP.",
                    severity="error",
                    field=f"{prefix}.cfop",
                )
            )

        if not item.get("value"):
            issues.append(
                ValidationIssue(
                    code="MISSING_ITEM_VALUE",
                    message=f"Item {index} is missing product value.",
                    severity="warning",
                    field=f"{prefix}.value",
                )
            )

    summary = build_summary(issues)
    score = calculate_score(issues)
    status = determine_status(issues)

    return ValidationResult(
        status=status,
        score=score,
        summary=summary,
        issues=issues,
    )