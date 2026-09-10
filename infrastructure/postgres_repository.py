"""Acesso centralizado aos dados relacionais do Radar."""

import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Abre uma conexão com o PostgreSQL configurado no arquivo .env."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )


def get_setores_existentes():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT setor FROM startups ORDER BY setor;")
        return [linha[0] for linha in cursor.fetchall()]


def get_documentos(startup_id: int):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT tipo, titulo, conteudo_texto, url_fonte "
            "FROM documentos WHERE startup_id = %s;",
            (startup_id,),
        )
        colunas = [descricao[0] for descricao in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
