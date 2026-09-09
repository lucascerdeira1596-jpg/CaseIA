from graph import montar_grafo

app = montar_grafo()

resultado = app.invoke({
    "pergunta_usuario": "Quero startups de saúde que usam IA de forma intensiva"
})

print("Critérios extraídos:", resultado["criterios_busca"])
print("\nStartups encontradas:")
for s in resultado["startups_candidatas"]:
    print(f"- {s['nome']} ({s['setor']})")
    