from retriever import retriever

estado_teste = {
    "criterios_busca": {
        "setor": "Healthtech",
        "categoria_ia": "AI-native",
        "palavras_chave": ["saúde", "IA", "monitoramento"],
        "intencao": "Buscar startups de saúde AI-native"
    }
}

resultado = retriever(estado_teste)
for startup in resultado["startups_candidatas"]:
    print(f"- {startup['nome']} ({startup['setor']})")

print(f"\nTotal encontrado: {len(resultado['startups_candidatas'])}")
