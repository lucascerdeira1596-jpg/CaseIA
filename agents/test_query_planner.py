from query_planner import query_planner

estado_teste = {
    "pergunta_usuario": "Quero startups de saúde que usam IA de forma intensiva"
}

resultado = query_planner(estado_teste)
print(resultado)
