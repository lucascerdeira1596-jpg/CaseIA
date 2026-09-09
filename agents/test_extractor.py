import json
from extractor import extractor

estado_teste = {
    "startups_candidatas": [
        {
            "id": 7,
            "nome": "Laura",
            "setor": "Healthtech",
            "descricao_curta": "IA cognitiva para monitoramento hospitalar em tempo real, com foco em detecção precoce de sepse e deterioração clínica."
        }
    ]
}

resultado = extractor(estado_teste)

print(json.dumps(resultado["perfis_estruturados"][0], indent=2, ensure_ascii=False))