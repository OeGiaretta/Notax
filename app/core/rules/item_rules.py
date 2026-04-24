from app.schemas.validation import ValidationIssue


def validate_item_rules(data: dict) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

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
        return issues

    for index, item in enumerate(items, start=1):
        prefix = f"items[{index - 1}]"

        ncm = item.get("ncm")
        cfop = item.get("cfop")

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

        if not ncm:
            issues.append(
                ValidationIssue(
                    code="MISSING_NCM",
                    message=f"Item {index} is missing NCM.",
                    severity="error",
                    field=f"{prefix}.ncm",
                )
            )
        elif not ncm.isdigit() or len(ncm) != 8:
            issues.append(
                ValidationIssue(
                    code="INVALID_NCM_FORMAT",
                    message=f"Item {index} has an invalid NCM format.",
                    severity="error",
                    field=f"{prefix}.ncm",
                )
            )

        if not cfop:
            issues.append(
                ValidationIssue(
                    code="MISSING_CFOP",
                    message=f"Item {index} is missing CFOP.",
                    severity="error",
                    field=f"{prefix}.cfop",
                )
            )
        elif not cfop.isdigit() or len(cfop) != 4:
            issues.append(
                ValidationIssue(
                    code="INVALID_CFOP_FORMAT",
                    message=f"Item {index} has an invalid CFOP format.",
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

    return issues