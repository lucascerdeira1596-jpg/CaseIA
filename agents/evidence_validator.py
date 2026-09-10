import json
from infrastructure.llm_client import invoke_llm
from infrastructure.postgres_repository import get_documentos

PROMPT_VALIDACAO = """Você é um auditor cético. Sua tarefa é verificar se um trecho de texto contém evidência REAL e GENUÍNA (mesmo que parcial) para uma afirmação feita sobre uma startup.

IMPORTANTE: a afirmação pode combinar informações de várias fontes diferentes. Você está avaliando apenas UM trecho por vez.
Responda "sustenta_afirmacao": true se o trecho confirma genuinamente PELO MENOS UMA PARTE relevante da afirmação, mesmo que não cubra tudo.
Responda false apenas se o trecho não tem relação real com a afirmação, ou contradiz o que foi dito.

Responda APENAS com um JSON válido:
{
  "sustenta_afirmacao": true ou false,
  "motivo": "1 frase curta explicando por quê"
}
"""

def validar_semanticamente(afirmacao, trecho):
    mensagem_usuario = json.dumps({
        "afirmacao_da_empresa": afirmacao,
        "trecho_citado_como_evidencia": trecho,
    }, ensure_ascii=False)

    resposta = invoke_llm([
        {"role": "system", "content": PROMPT_VALIDACAO},
        {"role": "user", "content": mensagem_usuario},
    ])
    resultado = json.loads(resposta.content)
    return resultado


def evidence_validator(state):
    perfis = state["perfis_classificados"]
    perfis_validados = []

    for perfil in perfis:
        docs_reais = get_documentos(perfil["startup_id"])
        urls_reais = {d["url_fonte"] for d in docs_reais}

        evidencias_com_url_valida = [
            e for e in perfil.get("evidencias", [])
            if e["url_fonte"] in urls_reais
        ]
        qtd_rejeitadas_por_url = len(perfil.get("evidencias", [])) - len(evidencias_com_url_valida)

        evidencias_finais = []
        qtd_rejeitadas_por_semantica = 0

        for evidencia in evidencias_com_url_valida:
            checagem = validar_semanticamente(
                afirmacao=perfil["uso_de_ia_descricao"],
                trecho=evidencia["trecho"],
            )
            if checagem["sustenta_afirmacao"]:
                evidencias_finais.append(evidencia)
            else:
                qtd_rejeitadas_por_semantica += 1

        perfil_validado = {
            **perfil,
            "evidencias": evidencias_finais,
            "qtd_evidencias_validas": len(evidencias_finais),
            "qtd_rejeitadas_por_url": qtd_rejeitadas_por_url,
            "qtd_rejeitadas_por_semantica": qtd_rejeitadas_por_semantica,
            "possivelmente_alucinado": (qtd_rejeitadas_por_url + qtd_rejeitadas_por_semantica) > 0,
        }

        perfis_validados.append(perfil_validado)

    return {"perfis_classificados": perfis_validados}
