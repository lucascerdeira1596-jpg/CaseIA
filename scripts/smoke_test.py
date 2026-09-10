"""Executa uma consulta ponta a ponta manualmente, sem interface web."""

from core.graph import montar_grafo


def main():
    resultado = montar_grafo().invoke({
        "pergunta_usuario": "Quero startups de saúde que usam IA de forma intensiva"
    })
    print(resultado["briefing_final"])


if __name__ == "__main__":
    main()
