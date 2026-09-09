import os
import json
import psycopg2
from dotenv import load_dotenv
from llm_client import invoke_llm  

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )

def get_documentos(startup_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT tipo, titulo, conteudo_texto, url_fonte FROM documentos WHERE startup_id = %s;",
        (startup_id,)
    )
    colunas = [desc[0] for desc in cursor.description]
    docs = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
    cursor.close()
    conn.close()
    return docs

PROMPT_SISTEMA = """Você é um analista que extrai sinais de uso de IA a partir de textos sobre startups.
Analise os documentos fornecidos e extraia um perfil estruturado.

Responda APENAS com um JSON válido, no formato:
{
  "tecnologias_ia_mencionadas": ["lista de tecnologias/técnicas de IA citadas nos textos"],
  "uso_de_ia_descricao": "resumo em 1-2 frases de como a empresa usa IA, baseado SOMENTE no texto fornecido",
  "evidencias": [
    {"trecho": "trecho curto do texto que sustenta a afirmação", "url_fonte": "url exata do documento de onde veio"}
  ]
}

Se os documentos não mencionarem uso de IA de forma relevante, retorne tecnologias_ia_mencionadas como lista vazia.
NUNCA invente uma url_fonte que não esteja nos documentos fornecidos.
"""

def extractor(state):
    candidatas = state["startups_candidatas"]
    perfis = []

    for startup in candidatas:
        docs = get_documentos(startup["id"])

        texto_documentos = "\n\n".join(
            f"[Documento tipo={d['tipo']}, url={d['url_fonte']}]\n{d['conteudo_texto']}"
            for d in docs
        )

        mensagem_usuario = f"Startup: {startup['nome']}\nDescrição: {startup['descricao_curta']}\n\nDocumentos:\n{texto_documentos}"

        resposta = invoke_llm([
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": mensagem_usuario},
        ])

        #print("--- RESPOSTA BRUTA DO MODELO ---")
        #print(repr(resposta.content))
        #print("--- FIM ---")

        perfil_extraido = json.loads(resposta.content)

        perfis.append({
            "startup_id": startup["id"],
            "nome": startup["nome"],
            "setor": startup["setor"],
            "descricao_curta": startup["descricao_curta"],
            **perfil_extraido,
        })

    return {"perfis_estruturados": perfis}