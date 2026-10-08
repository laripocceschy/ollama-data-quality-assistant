from pydantic import BaseModel


class QualityIssue(BaseModel):
    count: int
    percentage: float


class QualityMetrics(BaseModel):
    total_rows: int
    total_columns: int
    issues: dict[str, QualityIssue]