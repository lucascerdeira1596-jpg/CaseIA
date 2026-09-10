def briefing_agent(state):
    perfis = {p["startup_id"]: p for p in state["perfis_classificados"]}
    recomendacoes = state["recomendacoes"]

    secoes = []

    for rec in recomendacoes:
        perfil = perfis.get(rec["startup_id"], {})
        secao = f"## {rec['nome']} — {rec['classificacao']}\n\n"
        secao += f"**Uso de IA:** {perfil.get('uso_de_ia_descricao', 'N/A')}\n\n"

        if not rec["recomendacoes"]:
            secao += "_Nenhuma tecnologia NVIDIA suficientemente relevante encontrada para esta startup._\n\n"
        else:
            for tech in rec["recomendacoes"]:
                secao += f"### {tech['tecnologia']} (prioridade: {tech['nivel_prioridade']})\n"
                secao += f"- **Justificativa técnica:** {tech['justificativa_tecnica']}\n"
                secao += f"- **Justificativa de negócio:** {tech['justificativa_negocio']}\n"
                secao += f"- **Complexidade:** {tech['complexidade_implementacao']}\n"
                secao += f"- **Próxima ação:** {tech['proxima_acao_sugerida']}\n"
                secao += f"- **Evidências:** {', '.join(tech['evidencias_utilizadas'])}\n\n"

        secoes.append(secao)

    briefing_completo = "# Briefing — NVIDIA Startup AI Radar\n\n" + "\n---\n\n".join(secoes)

    return {"briefing_final": briefing_completo}
