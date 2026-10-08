import json

import ollama

from app.models import QualityMetrics


MODEL = "qwen2.5:3b"


def generate_report(metrics: QualityMetrics) -> str:
    """Gera um relatório textual usando o Ollama."""

    prompt = f"""
Você é um assistente especializado em qualidade de dados.

Analise as métricas abaixo e produza um relatório profissional
de qualidade de dados em português.

REGRAS OBRIGATÓRIAS:

1. Não faça cálculos matemáticos.
2. Utilize exatamente os números fornecidos nas métricas.
3. Não invente problemas, métricas ou informações.
4. Não classifique problemas como críticos, altos, médios ou baixos,
   pois nenhuma severidade foi fornecida pelo sistema.
5. Não considere automaticamente uma anomalia como um erro.
6. Valores negativos em "amount" devem ser tratados como uma
   anomalia que precisa de investigação.
7. Não presuma o significado de negócio de nenhum campo.
8. Não recomende excluir ou alterar registros sem evidências
   que justifiquem essa ação.
9. Diferencie claramente:
   - fato observado;
   - impacto potencial;
   - hipótese;
   - recomendação.
10. Nunca afirme uma causa como confirmada sem evidências.
11. Se as métricas não permitirem determinar a causa,
    deixe isso explícito.

Para cada problema encontrado, explique:
- o que foi observado;
- o impacto potencial;
- o que deveria ser investigado.

Métricas calculadas pelo sistema:

{json.dumps(
    metrics.model_dump(),
    ensure_ascii=False,
    indent=2,
)}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.message.content