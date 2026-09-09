import os
import cohere
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def embed_documents(textos: list[str]) -> list[list[float]]:
    response = co.embed(
        texts=textos,
        model="embed-multilingual-v3.0",
        input_type="search_document",
    )
    return response.embeddings

def embed_query(texto: str) -> list[float]:
    response = co.embed(
        texts=[texto],
        model="embed-multilingual-v3.0",
        input_type="search_query",
    )
    return response.embeddings[0]