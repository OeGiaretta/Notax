from app.schemas.validation import ValidationIssue, ValidationResult


def validate_invoice_data(data: dict) -> ValidationResult:
    issues = []

    if not data.get("invoice_number"):
        issues.append(
            ValidationIssue(
                code="MISSING_INVOICE_NUMBER",
                message="Número da nota ausente.",
                severity="error"
            )
        )

    if not data.get("issuer_cnpj"):
        issues.append(
            ValidationIssue(
                code="MISSING_ISSUER_CNPJ",
                message="CNPJ do emitente ausente.",
                severity="error"
            )
        )

    if not data.get("recipient_cnpj"):
        issues.append(
            ValidationIssue(
                code="MISSING_RECIPIENT_CNPJ",
                message="CNPJ do destinatário ausente.",
                severity="error"
            )
        )

    total_value = data.get("total_value")
    if not total_value or total_value in ["0", "0.00", 0, 0.0]:
        issues.append(
            ValidationIssue(
                code="INVALID_TOTAL_VALUE",
                message="Valor total ausente ou zerado.",
                severity="error"
            )
        )

    items = data.get("items", [])
    if not items:
        issues.append(
            ValidationIssue(
                code="MISSING_ITEMS",
                message="Nenhum item encontrado na nota.",
                severity="error"
            )
        )

    for index, item in enumerate(items, start=1):
        if not item.get("ncm"):
            issues.append(
                ValidationIssue(
                    code="MISSING_NCM",
                    message=f"Item {index} sem NCM.",
                    severity="error"
                )
            )

        if not item.get("cfop"):
            issues.append(
                ValidationIssue(
                    code="MISSING_CFOP",
                    message=f"Item {index} sem CFOP.",
                    severity="error"
                )
            )

    status = "ok" if not issues else "warning"

    return ValidationResult(status=status, issues=issues)