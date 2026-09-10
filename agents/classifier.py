import json
from infrastructure.llm_client import invoke_llm

PROMPT_SISTEMA = """Você é um especialista em classificar a maturidade de IA de startups, segundo estas definições:

- AI-native: a IA é o núcleo do produto. Sem a tecnologia de IA, o produto não existiria ou perderia sua proposta de valor central. A empresa constrói/treina/orquestra modelos como parte fundamental da oferta.
- AI-enabled: a empresa usa IA como uma camada adicional sobre um produto que já existia ou que funcionaria (com menos eficiência) sem ela. IA melhora a experiência, mas não é o motivo de existir do negócio.
- non-AI: a empresa não usa IA de forma relevante, ou o uso é superficial/cosmético, sem impacto real no produto.

Analise o perfil da startup fornecido e classifique. Responda APENAS com um JSON válido:
{
  "classificacao": "AI-native, AI-enabled ou non-AI",
  "justificativa": "1-2 frases explicando a decisão, referenciando o que foi encontrado nas evidências",
  "confianca": "alta, média ou baixa"
}
"""

def classifier(state):
    perfis = state["perfis_estruturados"]
    perfis_classificados = []

    for perfil in perfis:
        mensagem_usuario = json.dumps({
            "nome": perfil["nome"],
            "setor": perfil["setor"],
            "descricao_curta": perfil["descricao_curta"],
            "tecnologias_ia_mencionadas": perfil["tecnologias_ia_mencionadas"],
            "uso_de_ia_descricao": perfil["uso_de_ia_descricao"],
        }, ensure_ascii=False)

        resposta = invoke_llm([
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": mensagem_usuario},
        ])

        classificacao = json.loads(resposta.content)

        perfis_classificados.append({
            **perfil,
            **classificacao,
        })

    return {"perfis_classificados": perfis_classificados}
