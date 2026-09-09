import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    host=os.getenv("QDRANT_HOST"),
    port=int(os.getenv("QDRANT_PORT")),
)

client.create_collection(
    collection_name="nvidia_knowledge",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)

print("Collection 'nvidia_knowledge' criada com sucesso.")