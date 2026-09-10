import json
import re
from pathlib import Path
from rank_bm25 import BM25Okapi

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def _tokenizar(texto):
    return re.findall(r"\w+", texto.lower())

def _montar_texto_busca(chunk):
    return f"{chunk['titulo']}\n\n{chunk['conteudo_texto']}\n\nQuando recomendar: {chunk['recomendar_para']}"

with (PROJECT_ROOT / "data" / "nvidia_knowledge_base.json").open(encoding="utf-8") as f:
    _CHUNKS = json.load(f)["knowledge_base"]

_CORPUS_TOKENIZADO = [_tokenizar(_montar_texto_busca(c)) for c in _CHUNKS]
_BM25 = BM25Okapi(_CORPUS_TOKENIZADO)

def bm25_search(query: str, top_k: int = 15):
    scores = _BM25.get_scores(_tokenizar(query))
    indices_ordenados = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    return [
        {"chunk_index": i, "score_bm25": float(scores[i]), **_CHUNKS[i]}
        for i in indices_ordenados
        if scores[i] > 0
    ]
