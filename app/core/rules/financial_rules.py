from decimal import Decimal, InvalidOperation

from app.schemas.validation import ValidationIssue


def parse_decimal(value: str | int | float | None) -> Decimal | None:
    if value is None:
        return None

    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def validate_financial_rules(data: dict) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    total_value = parse_decimal(data.get("total_value"))

    if total_value is None:
        issues.append(
            ValidationIssue(
                code="INVALID_TOTAL_VALUE",
                message="Total value is missing or invalid.",
                severity="error",
                field="total_value",
            )
        )
        return issues

    if total_value == Decimal("0.00"):
        issues.append(
            ValidationIssue(
                code="ZERO_TOTAL_VALUE",
                message="Total value is zero.",
                severity="warning",
                field="total_value",
            )
        )

    items = data.get("items", [])
    item_values: list[Decimal] = []

    for item in items:
        item_value = parse_decimal(item.get("value"))

        if item_value is not None:
            item_values.append(item_value)

    if item_values:
        items_total = sum(item_values, Decimal("0.00"))

        if items_total != total_value:
            issues.append(
                ValidationIssue(
                    code="TOTAL_VALUE_MISMATCH",
                    message="Invoice total value does not match the sum of item values.",
                    severity="error",
                    field="total_value",
                )
            )

    return issues