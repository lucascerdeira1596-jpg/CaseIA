import json

with open("data/startups_config.json", encoding="utf-8") as f:
    startups = json.load(f)["startups"]

for s in startups:
    if len(s["estagio"]) > 50:
        print(f"❌ estagio muito longo ({len(s['estagio'])} chars): {s['nome']} -> {s['estagio']}")
    if len(s["localizacao"]) > 100:
        print(f"❌ localizacao muito longa: {s['nome']}")
    if len(s["tamanho_time"]) > 50:
        print(f"❌ tamanho_time muito longo: {s['nome']}")