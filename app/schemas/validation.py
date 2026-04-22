from pydantic import BaseModel
from typing import List

class ValidationIssue(BaseModel):
    code: str
    message: str
    severity: str

class ValidationResult(BaseModel):
    status: str
    issues: List[ValidationIssue]