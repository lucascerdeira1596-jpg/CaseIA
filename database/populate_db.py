import os
import json
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

def popular_startups(conn, startups):
    ids_por_nome = {}
    cursor = conn.cursor()

    for s in startups:
        cursor.execute(
            """
            INSERT INTO startups (nome, site, setor, estagio, localizacao, descricao_curta, ano_fundacao, tamanho_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (s["nome"], s["site"], s["setor"], s["estagio"], s["localizacao"],
             s["descricao_curta"], s["ano_fundacao"], s["tamanho_time"])
        )
        novo_id = cursor.fetchone()[0]
        ids_por_nome[s["nome"]] = novo_id

    conn.commit()
    cursor.close()
    return ids_por_nome

def popular_documentos(conn, documentos, ids_por_nome):
    cursor = conn.cursor()
    pulados = 0

    for d in documentos:
        startup_id = ids_por_nome.get(d["startup_nome"])

        if startup_id is None:
            print(f"⚠️  Startup não encontrada: {d['startup_nome']} — documento pulado")
            pulados += 1
            continue

        cursor.execute(
            """
            INSERT INTO documentos (startup_id, tipo, titulo, conteudo_texto, url_fonte, data_publicacao)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (startup_id, d["tipo"], d["titulo"], d["conteudo_texto"],
             d["url_fonte"], d["data_publicacao"])
        )

    conn.commit()
    cursor.close()
    print(f"Documentos inseridos: {len(documentos) - pulados} | pulados: {pulados}")

def main():
    with open("data/startups_config.json", encoding="utf-8") as f:
        startups = json.load(f)["startups"]

    with open("data/documentos_seed.json", encoding="utf-8") as f:
        documentos = json.load(f)["documentos"]

    conn = get_connection()

    try:
        ids_por_nome = popular_startups(conn, startups)
        print(f"Startups inseridas: {len(ids_por_nome)}")

        popular_documentos(conn, documentos, ids_por_nome)
    finally:
        conn.close()


if __name__ == "__main__":
    main()