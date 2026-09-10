"""Popula o PostgreSQL com as startups e documentos versionados no projeto."""

import json
from pathlib import Path

from infrastructure.postgres_repository import get_connection

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def popular_startups(conn, startups):
    ids_por_nome = {}
    with conn.cursor() as cursor:
        for startup in startups:
            cursor.execute(
                """
                INSERT INTO startups (nome, site, setor, estagio, localizacao, descricao_curta, ano_fundacao, tamanho_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    startup["nome"], startup["site"], startup["setor"], startup["estagio"],
                    startup["localizacao"], startup["descricao_curta"], startup["ano_fundacao"],
                    startup["tamanho_time"],
                ),
            )
            ids_por_nome[startup["nome"]] = cursor.fetchone()[0]
    conn.commit()
    return ids_por_nome


def popular_documentos(conn, documentos, ids_por_nome):
    pulados = 0
    with conn.cursor() as cursor:
        for documento in documentos:
            startup_id = ids_por_nome.get(documento["startup_nome"])
            if startup_id is None:
                print(f"⚠️ Startup não encontrada: {documento['startup_nome']} — documento pulado")
                pulados += 1
                continue
            cursor.execute(
                """
                INSERT INTO documentos (startup_id, tipo, titulo, conteudo_texto, url_fonte, data_publicacao)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (
                    startup_id, documento["tipo"], documento["titulo"], documento["conteudo_texto"],
                    documento["url_fonte"], documento["data_publicacao"],
                ),
            )
    conn.commit()
    print(f"Documentos inseridos: {len(documentos) - pulados} | pulados: {pulados}")


def main():
    with (PROJECT_ROOT / "data" / "startups_config.json").open(encoding="utf-8") as arquivo:
        startups = json.load(arquivo)["startups"]
    with (PROJECT_ROOT / "data" / "documentos_seed.json").open(encoding="utf-8") as arquivo:
        documentos = json.load(arquivo)["documentos"]

    with get_connection() as connection:
        ids_por_nome = popular_startups(connection, startups)
        print(f"Startups inseridas: {len(ids_por_nome)}")
        popular_documentos(connection, documentos, ids_por_nome)


if __name__ == "__main__":
    main()
