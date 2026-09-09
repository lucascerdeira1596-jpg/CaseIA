import os
import cohere
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def rerank(pergunta: str, documentos: list[str], top_n: int = 3):
    resposta = co.rerank(
        query=pergunta,
        documents=documentos,
        top_n=top_n,
        model="rerank-v3.5",
    )
    return resposta.results