from app.schemas.validation import ValidationIssue


def only_digits(value: str) -> str:
    return "".join(filter(str.isdigit, value or ""))


def is_valid_cnpj(cnpj: str) -> bool:
    cnpj = only_digits(cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calc_digit(base: str, weights: list[int]) -> int:
        total = sum(int(d) * w for d, w in zip(base, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    d1 = calc_digit(cnpj[:12], [5,4,3,2,9,8,7,6,5,4,3,2])
    d2 = calc_digit(cnpj[:13], [6,5,4,3,2,9,8,7,6,5,4,3,2])

    return cnpj.endswith(f"{d1}{d2}")


def validate_cnpj_rules(data: dict) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    issuer = data.get("issuer_cnpj")
    recipient = data.get("recipient_cnpj")

    if issuer and not is_valid_cnpj(issuer):
        issues.append(
            ValidationIssue(
                code="INVALID_ISSUER_CNPJ",
                message="Issuer CNPJ is invalid.",
                severity="error",
                field="issuer_cnpj",
            )
        )

    if recipient and not is_valid_cnpj(recipient):
        issues.append(
            ValidationIssue(
                code="INVALID_RECIPIENT_CNPJ",
                message="Recipient CNPJ is invalid.",
                severity="error",
                field="recipient_cnpj",
            )
        )

    return issues