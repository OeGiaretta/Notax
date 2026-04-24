from app.schemas.validation import ValidationIssue


def validate_required_fields(data: dict) -> list[ValidationIssue]:
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

    return issues