from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
from embeddings import embed_query

load_dotenv()

client = QdrantClient(
    host=os.getenv("QDRANT_HOST"),
    port=int(os.getenv("QDRANT_PORT")),
)

vetor = embed_query("Minha startup usa atendimento por voz e call center, o que a NVIDIA recomenda?")

resposta = client.query_points(
    collection_name="nvidia_knowledge",
    query=vetor,
    limit=25,  # mais que o total de chunks, pra ver o ranking inteiro
)

for r in resposta.points:
    print(f"[{r.score:.4f}] {r.payload['tecnologia']}")
    