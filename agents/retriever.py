import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )

def retriever(state):
    criterios = state["criterios_busca"]
    conn = get_connection()
    cursor = conn.cursor()

    condicoes = []
    valores = []

    if criterios.get("setor"):
        condicoes.append("setor ILIKE %s")
        valores.append(f"%{criterios['setor']}%")

    palavras_chave = criterios.get("palavras_chave", [])
    if palavras_chave:
        condicoes_texto = []
        for palavra in palavras_chave:
            condicoes_texto.append("descricao_curta ILIKE %s")
            valores.append(f"%{palavra}%")
        condicoes.append(f"({' OR '.join(condicoes_texto)})")

    where_clause = " OR ".join(condicoes) if condicoes else "TRUE"

    query = f"""
        SELECT id, nome, site, setor, estagio, localizacao, descricao_curta
        FROM startups
        WHERE {where_clause}
        LIMIT 10;
    """

    print("SQL:", query)
    print("Valores:", valores)
    cursor.execute(query, valores)
    colunas = [desc[0] for desc in cursor.description]
    resultados = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

    cursor.close()
    conn.close()

    return {"startups_candidatas": resultados}
