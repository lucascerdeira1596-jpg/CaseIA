import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from rag.bm25_search import bm25_search
from rag.embeddings import embed_query
from rag.rerank import rerank

load_dotenv()

client = QdrantClient(
    host=os.getenv("QDRANT_HOST"),
    port=int(os.getenv("QDRANT_PORT")),
)

def _fusao_por_rank_reciproco(ids_vetoriais, ids_lexicais, k=60):
    scores = {}
    for rank, chunk_id in enumerate(ids_vetoriais):
        scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (k + rank + 1)
    for rank, chunk_id in enumerate(ids_lexicais):
        scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)

def buscar_tecnologias_nvidia(texto_perfil: str, top_k_vetorial: int = 15, top_k_fusao: int = 10, top_n_final: int = 5):
    vetor = embed_query(texto_perfil)

    resposta = client.query_points(
        collection_name="nvidia_knowledge",
        query=vetor,
        limit=top_k_vetorial,
    )
    candidatos_vetoriais = resposta.points
    candidatos_lexicais = bm25_search(texto_perfil, top_k=top_k_vetorial)

    chunks_por_id = {c.payload["chunk_index"]: c.payload for c in candidatos_vetoriais}
    for c in candidatos_lexicais:
        chunks_por_id.setdefault(c["chunk_index"], c)

    ids_vetoriais = [c.payload["chunk_index"] for c in candidatos_vetoriais]
    ids_lexicais = [c["chunk_index"] for c in candidatos_lexicais]

    fusao = _fusao_por_rank_reciproco(ids_vetoriais, ids_lexicais)[:top_k_fusao]
    candidatos_fundidos = [chunks_por_id[chunk_id] for chunk_id, _ in fusao]

    textos_para_rerank = [
        f"{c['titulo']}\n\n{c['conteudo_texto']}\n\nQuando recomendar: {c['recomendar_para']}"
        for c in candidatos_fundidos
    ]

    resultados_rerank = rerank(texto_perfil, textos_para_rerank, top_n=top_n_final)

    return [
        {
            "tecnologia": candidatos_fundidos[r.index]["tecnologia"],
            "titulo": candidatos_fundidos[r.index]["titulo"],
            "conteudo_texto": candidatos_fundidos[r.index]["conteudo_texto"],
            "url_fonte": candidatos_fundidos[r.index]["url_fonte"],
            "recomendar_para": candidatos_fundidos[r.index]["recomendar_para"],
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
