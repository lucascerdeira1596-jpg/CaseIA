import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "rag"))

from qdrant_client import QdrantClient
from dotenv import load_dotenv
from embeddings import embed_query
from rerank import rerank

load_dotenv()

client = QdrantClient(
    host=os.getenv("QDRANT_HOST"),
    port=int(os.getenv("QDRANT_PORT")),
)

def buscar_tecnologias_nvidia(texto_perfil: str, top_k_vetorial: int = 15, top_n_final: int = 5):
    vetor = embed_query(texto_perfil)

    resposta = client.query_points(
        collection_name="nvidia_knowledge",
        query=vetor,
        limit=top_k_vetorial,
    )
    candidatos = resposta.points

    textos_para_rerank = [
        f"{c.payload['titulo']}\n\n{c.payload['conteudo_texto']}\n\nQuando recomendar: {c.payload['recomendar_para']}"
        for c in candidatos
    ]

    resultados_rerank = rerank(texto_perfil, textos_para_rerank, top_n=top_n_final)

    return [
        {
            "tecnologia": candidatos[r.index].payload["tecnologia"],
            "titulo": candidatos[r.index].payload["titulo"],
            "conteudo_texto": candidatos[r.index].payload["conteudo_texto"],
            "url_fonte": candidatos[r.index].payload["url_fonte"],
            "score_relevancia": r.relevance_score,
        }
        for r in resultados_rerank
    ]


def rag_agent(state):
    perfis = state["perfis_classificados"]
    perfis_com_contexto = []

    for perfil in perfis:
        texto_perfil = (
            f"Startup do setor {perfil['setor']}, classificada como {perfil['classificacao']}. "
            f"Uso de IA: {perfil['uso_de_ia_descricao']} "
            f"Tecnologias mencionadas: {', '.join(perfil['tecnologias_ia_mencionadas'])}."
        )

        tecnologias_relevantes = buscar_tecnologias_nvidia(texto_perfil)

        perfis_com_contexto.append({
            **perfil,
            "tecnologias_nvidia_candidatas": tecnologias_relevantes,
        })

    return {"perfis_classificados": perfis_com_contexto}
