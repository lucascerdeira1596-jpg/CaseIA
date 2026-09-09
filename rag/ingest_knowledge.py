import json
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import os
from dotenv import load_dotenv
from embeddings import embed_documents

load_dotenv()

client = QdrantClient(
    host=os.getenv("QDRANT_HOST"),
    port=int(os.getenv("QDRANT_PORT")),
)

def montar_texto_busca(chunk):
    return f"{chunk['titulo']}\n\n{chunk['conteudo_texto']}\n\nQuando recomendar: {chunk['recomendar_para']}"


def main():
    with open("data/nvidia_knowledge_base.json", encoding="utf-8") as f:
        chunks = json.load(f)["knowledge_base"]

    textos = [montar_texto_busca(c) for c in chunks]
    vetores = embed_documents(textos)

    pontos = []

    from qdrant_client.models import Distance, VectorParams

    client.delete_collection("nvidia_knowledge")
    client.create_collection(
        collection_name="nvidia_knowledge",
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    )



    for chunk, vetor in zip(chunks, vetores):
        pontos.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vetor,
                payload={
                    "tecnologia": chunk["tecnologia"],
                    "titulo": chunk["titulo"],
                    "conteudo_texto": chunk["conteudo_texto"],
                    "url_fonte": chunk["url_fonte"],
                    "recomendar_para": chunk["recomendar_para"],
                },
            )
        )

    client.upsert(collection_name="nvidia_knowledge", points=pontos)
    print(f"{len(pontos)} chunks indexados no Qdrant.")

if __name__ == "__main__":
    main()

