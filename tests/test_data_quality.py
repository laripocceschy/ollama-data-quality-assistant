import pandas as pd
import pytest

from app.data_quality import analyze_data


def test_detects_data_quality_issues():
    df = pd.DataFrame(
        {
            "transaction_id": [1001, 1002, 1002],
            "customer_id": [501, None, 503],
            "amount": [150.0, 250.0, -50.0],
            "date": [
                "2026-10-01",
                "2026-10-02",
                "data_invalida",
            ],
        }
    )

    result = analyze_data(df)

    assert result.total_rows == 3
    assert result.total_columns == 4

    assert result.issues["missing_customer_id"].count == 1
    assert result.issues["missing_customer_id"].percentage == 33.33

    assert result.issues["duplicate_transaction_rows"].count == 2
    assert result.issues["duplicate_transaction_rows"].percentage == 66.67

    assert result.issues["negative_amount"].count == 1
    assert result.issues["negative_amount"].percentage == 33.33

    assert result.issues["invalid_date"].count == 1
    assert result.issues["invalid_date"].percentage == 33.33


def test_detects_missing_required_columns():
    df = pd.DataFrame(
        {
            "transaction_id": [1001],
            "customer_id": [501],
            "amount": [150.0],
        }
    )

    with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
        analyze_data(df)


def test_detects_clean_dataset():
    df = pd.DataFrame(
        {
            "transaction_id": [1001, 1002, 1003],
            "customer_id": [501, 502, 503],
            "amount": [150.0, 250.0, 300.0],
            "date": [
                "2026-10-01",
                "2026-10-02",
                "2026-10-03",
            ],
        }
    )

    result = analyze_data(df)

    assert result.total_rows == 3
    assert result.total_columns == 4

    for issue in result.issues.values():
        assert issue.count == 0
        assert issue.percentage == 0.0