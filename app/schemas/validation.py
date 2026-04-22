from typing import List

from pydantic import BaseModel


class ValidationIssue(BaseModel):
    code: str
    message: str
    severity: str
    field: str | None = None


class ValidationSummary(BaseModel):
    total_issues: int
    errors: int
    warnings: int
    info: int


class ValidationResult(BaseModel):
    status: str
    score: int
    summary: ValidationSummary
    issues: List[ValidationIssue]