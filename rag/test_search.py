import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from embeddings import embed_query
from rerank import rerank

load_dotenv()

client = QdrantClient(
    host=os.getenv("QDRANT_HOST"),
    port=int(os.getenv("QDRANT_PORT")),
)


def buscar(pergunta: str, top_k_vetorial: int = 15, top_n_final: int = 3):
    vetor_pergunta = embed_query(pergunta)

    resposta = client.query_points(
        collection_name="nvidia_knowledge",
        query=vetor_pergunta,
        limit=top_k_vetorial,
    )

    candidatos = resposta.points

    textos_candidatos = [c.payload["conteudo_texto"] for c in candidatos]

    resultados_rerank = rerank(pergunta, textos_candidatos, top_n=top_n_final)

    print(f"\nPergunta: {pergunta}\n")
    for r in resultados_rerank:
        chunk_original = candidatos[r.index].payload
        print(f"[rerank_score={r.relevance_score:.4f}] {chunk_original['tecnologia']} — {chunk_original['titulo']}")
        print(f"  {chunk_original['conteudo_texto'][:150]}...")
        print()

if __name__ == "__main__":
    buscar("Minha startup usa atendimento por voz e call center, o que a NVIDIA recomenda?")