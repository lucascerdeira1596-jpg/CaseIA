import json
from infrastructure.llm_client import invoke_llm

PROMPT_SISTEMA = """Você é um analista que monta recomendações de tecnologia NVIDIA para startups, para uso do time de Startups & VCs da NVIDIA Brasil.

REGRAS IMPORTANTES:
- Só recomende tecnologias que estejam na lista de "tecnologias_candidatas" fornecida. NUNCA mencione uma tecnologia NVIDIA que não esteja nessa lista.
- Só cite evidências que estejam na lista de "evidencias" fornecida. NUNCA invente uma URL ou trecho novo.
- Se a lista de tecnologias candidatas não tiver nada realmente relevante para o perfil da startup, retorne uma lista de recomendações vazia — não force uma recomendação fraca só para preencher.

Responda APENAS com um JSON válido, no formato:
{
  "recomendacoes": [
    {
      "tecnologia": "nome exato de uma das tecnologias_candidatas",
      "justificativa_tecnica": "por que essa tecnologia resolve um gap técnico real da startup",
      "justificativa_negocio": "qual o ganho de negócio (custo, velocidade, novo mercado, etc.)",
      "nivel_prioridade": "alta, média ou baixa",
      "complexidade_implementacao": "alta, média ou baixa",
      "proxima_acao_sugerida": "ação concreta e específica para o time da NVIDIA dar o próximo passo com essa startup",
      "evidencias_utilizadas": ["url_fonte exata de uma ou mais evidências da lista fornecida"]
    }
  ]
}
"""

def recommendation_agent(state):
    perfis = state["perfis_classificados"]
    recomendacoes_por_startup = []

    for perfil in perfis:
        mensagem_usuario = json.dumps({
            "nome": perfil["nome"],
            "setor": perfil["setor"],
            "classificacao": perfil["classificacao"],
            "uso_de_ia_descricao": perfil["uso_de_ia_descricao"],
            "evidencias": [
                {"trecho": e["trecho"], "url_fonte": e["url_fonte"]}
                for e in perfil["evidencias"]
            ],
            "tecnologias_candidatas": [
                {
                    "tecnologia": t["tecnologia"],
                    "descricao": t["conteudo_texto"],
                    "quando_recomendar": t.get("recomendar_para", ""),
                }
                for t in perfil["tecnologias_nvidia_candidatas"]
            ],
        }, ensure_ascii=False)

        resposta = invoke_llm([
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": mensagem_usuario},
        ])

        resultado = json.loads(resposta.content)

        recomendacoes_por_startup.append({
            "startup_id": perfil["startup_id"],
            "nome": perfil["nome"],
            "classificacao": perfil["classificacao"],
            "recomendacoes": resultado["recomendacoes"],
        })

    return {"recomendacoes": recomendacoes_por_startup}
