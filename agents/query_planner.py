import json
from infrastructure.llm_client import invoke_llm
from infrastructure.postgres_repository import get_setores_existentes


def query_planner(state):
    pergunta = state["pergunta_usuario"]
    setores_existentes = get_setores_existentes()

    prompt_sistema = f"""Você é um planejador de consultas para um sistema de análise de startups brasileiras de IA.
Sua tarefa é transformar a pergunta do usuário em critérios estruturados de busca.

Os setores que EXISTEM no banco de dados são exatamente estes: {setores_existentes}
Se a pergunta do usuário mencionar um tema que se encaixe em algum desses setores, use o valor EXATO da lista.
Se não houver correspondência clara, retorne "setor": null.

Responda APENAS com um JSON válido, sem nenhum texto antes ou depois, no formato:
{{
  "setor": "string EXATA da lista de setores, ou null",
  "categoria_ia": "AI-native, AI-enabled, non-AI, ou null",
  "palavras_chave": ["lista", "de", "termos", "relevantes"],
  "intencao": "breve descrição da intenção da busca"
}}
"""

    resposta = invoke_llm([
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": pergunta},
    ])
    criterios = json.loads(resposta.content)
    return {"criterios_busca": criterios}
