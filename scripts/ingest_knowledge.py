"""Indexa a base versionada de tecnologias NVIDIA no Qdrant."""

import json
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from rag.embeddings import embed_documents

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
COLLECTION_NAME = "nvidia_knowledge"


def montar_texto_busca(chunk):
    return f"{chunk['titulo']}\n\n{chunk['conteudo_texto']}\n\nQuando recomendar: {chunk['recomendar_para']}"


def main():
    with (PROJECT_ROOT / "data" / "nvidia_knowledge_base.json").open(encoding="utf-8") as arquivo:
        chunks = json.load(arquivo)["knowledge_base"]

    client = QdrantClient(host=os.getenv("QDRANT_HOST"), port=int(os.getenv("QDRANT_PORT")))
    vetores = embed_documents([montar_texto_busca(chunk) for chunk in chunks])

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    )
    pontos = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vetor,
            payload={"chunk_index": indice, **chunk},
        )
        for indice, (chunk, vetor) in enumerate(zip(chunks, vetores))
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=pontos)
    print(f"{len(pontos)} chunks indexados no Qdrant.")


if __name__ == "__main__":
    main()
