import json

import pandas as pd

from app.data_quality import analyze_data
from app.llm import generate_report


def main():
    df = pd.read_csv("data/sample_sales.csv")

    metrics = analyze_data(df)

    print("=== MÉTRICAS DE QUALIDADE ===")
    print(
        json.dumps(
            metrics.model_dump(),
            ensure_ascii=False,
            indent=2,
        )
    )

    print("\n=== RELATÓRIO GERADO PELO OLLAMA ===")

    report = generate_report(metrics)

    print(report)


if __name__ == "__main__":
    main()