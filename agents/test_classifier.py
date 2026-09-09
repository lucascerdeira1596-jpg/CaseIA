import json
from extractor import extractor
from classifier import classifier
from evidence_validator import evidence_validator
from rag_agent import rag_agent
from recommendation import recommendation_agent

estado = {
    "startups_candidatas": [
        {"id": 7, "nome": "Laura", "setor": "Healthtech", "descricao_curta": "IA cognitiva para monitoramento hospitalar em tempo real, com foco em detecção precoce de sepse e deterioração clínica."}
    ]
}

estado.update(extractor(estado))
estado.update(classifier(estado))
estado.update(evidence_validator(estado))
estado.update(rag_agent(estado))
estado.update(recommendation_agent(estado))

print("=== Perfil completo após todos os agentes ===")
print(json.dumps(estado["perfis_classificados"][0], indent=2, ensure_ascii=False))

print("\n=== Tecnologias NVIDIA candidatas (RAG) ===")
for t in estado["perfis_classificados"][0]["tecnologias_nvidia_candidatas"]:
    print(f"[{t['score_relevancia']:.4f}] {t['tecnologia']} — {t['titulo']}")

print("\n=== Recomendação final para Laura ===")
print(json.dumps(estado["recomendacoes"][0], indent=2, ensure_ascii=False))