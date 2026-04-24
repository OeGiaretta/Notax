from datetime import datetime, timezone
from app.schemas.validation import ValidationIssue
from dateutil.parser import parse as parse_date

def validate_date_rules(data: dict) -> list[ValidationIssue]:
    issues:list[ValidationIssue] = []
    issued_at= data.get("issued_at")

    if issued_at:
        try:
            dt = datetime.fromisoformat(issued_at)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            if dt > datetime.now(timezone.utc):
                issues.append(
                    ValidationIssue(
                        code="INVALID_ISSUER_DATE",
                        message="Invoice issue date is in the future.",
                        severity="warning",
                        field="issued_at",
                    )
                )
        except Exception:
            issues.append(
                ValidationIssue(
                    code="INVALID_DATE_FORMAT",
                    message="Invalid issued_at format.",
                    severity="error",
                    field="issued_at",
                )
            )
        return issues