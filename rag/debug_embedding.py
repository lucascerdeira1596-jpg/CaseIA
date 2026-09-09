from embeddings import embed_query

vetor = embed_query("teste de diagnóstico")
print("Tipo do retorno:", type(vetor))
print("Tamanho do vetor:", len(vetor))
print("Primeiros 5 valores:", vetor[:5])