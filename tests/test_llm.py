from types import SimpleNamespace
from unittest.mock import patch

from app.llm import generate_report
from app.models import QualityMetrics


def test_generate_report_uses_ollama():
    metrics = QualityMetrics(
        total_rows=10,
        total_columns=4,
        issues={
            "missing_customer_id": {
                "count": 2,
                "percentage": 20.0,
            },
            "duplicate_transaction_rows": {
                "count": 0,
                "percentage": 0.0,
            },
            "negative_amount": {
                "count": 1,
                "percentage": 10.0,
            },
            "invalid_date": {
                "count": 0,
                "percentage": 0.0,
            },
        },
    )

    fake_response = SimpleNamespace(
        message=SimpleNamespace(
            content="Relatório de teste."
        )
    )

    with patch(
        "app.llm.ollama.chat",
        return_value=fake_response,
    ) as mock_chat:
        result = generate_report(metrics)

    assert result == "Relatório de teste."

    mock_chat.assert_called_once()

    call_args = mock_chat.call_args

    assert call_args.kwargs["model"] == "qwen2.5:3b"