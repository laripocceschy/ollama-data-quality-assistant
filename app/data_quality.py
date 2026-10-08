import pandas as pd

from app.models import QualityMetrics


def analyze_data(df: pd.DataFrame) -> QualityMetrics:
    """Analisa regras básicas de qualidade de dados."""

    required_columns = {
        "transaction_id",
        "customer_id",
        "amount",
        "date",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Colunas obrigatórias ausentes: "
            f"{sorted(missing_columns)}"
        )

    total_rows = len(df)

    null_counts = (
        df[list(required_columns)]
        .isna()
        .sum()
        .to_dict()
    )

    duplicate_count = int(
        df["transaction_id"].duplicated(keep=False).sum()
    )

    negative_amount_count = int(
        (df["amount"] < 0).sum()
    )

    parsed_dates = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    invalid_date_count = int(
        parsed_dates.isna().sum()
    )

    def percentage(count: int) -> float:
        if total_rows == 0:
            return 0.0

        return round((count / total_rows) * 100, 2)

    return QualityMetrics(
        total_rows=total_rows,
        total_columns=len(df.columns),
        issues={
            "missing_customer_id": {
                "count": int(null_counts["customer_id"]),
                "percentage": percentage(
                    int(null_counts["customer_id"])
                ),
            },
            "duplicate_transaction_rows": {
                "count": duplicate_count,
                "percentage": percentage(duplicate_count),
            },
            "negative_amount": {
                "count": negative_amount_count,
                "percentage": percentage(
                    negative_amount_count
                ),
            },
            "invalid_date": {
                "count": invalid_date_count,
                "percentage": percentage(
                    invalid_date_count
                ),
            },
        },
    )