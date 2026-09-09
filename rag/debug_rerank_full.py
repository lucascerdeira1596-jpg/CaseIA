from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
from embeddings import embed_query
from rerank import rerank

load_dotenv()

client = QdrantClient(
    host=os.getenv("QDRANT_HOST"),
    port=int(os.getenv("QDRANT_PORT")),
)

pergunta = "Minha startup usa atendimento por voz e call center, o que a NVIDIA recomenda?"
vetor = embed_query(pergunta)

resposta = client.query_points(
    collection_name="nvidia_knowledge",
    query=vetor,
    limit=15,
)
candidatos = resposta.points

print("=== Candidatos enviados ao rerank (ordem original) ===")
for i, c in enumerate(candidatos):
    print(f"{i}: {c.payload['tecnologia']}")

textos = [
    f"{c.payload['titulo']}\n\n{c.payload['conteudo_texto']}\n\nQuando recomendar: {c.payload['recomendar_para']}"
    for c in candidatos
]

print("\n=== Resultado do rerank (TODOS, sem cortar top_n) ===")
resultados = rerank(pergunta, textos, top_n=len(textos))
for r in resultados:
    print(f"index={r.index} | score={r.relevance_score:.4f} | {candidatos[r.index].payload['tecnologia']}")