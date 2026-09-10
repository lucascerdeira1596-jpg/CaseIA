from langgraph.graph import StateGraph, END
from core.state import RadarState
from agents.query_planner import query_planner
from agents.retriever import retriever
from agents.extractor import extractor
from agents.classifier import classifier
from agents.evidence_validator import evidence_validator
from agents.rag_agent import rag_agent
from agents.recommendation import recommendation_agent
from agents.briefing_agent import briefing_agent

def montar_grafo():
    grafo = StateGraph(RadarState)

    grafo.add_node("query_planner", query_planner)
    grafo.add_node("retriever", retriever)
    grafo.add_node("extractor", extractor)
    grafo.add_node("classifier", classifier)
    grafo.add_node("evidence_validator", evidence_validator)
    grafo.add_node("rag_agent", rag_agent)
    grafo.add_node("recommendation_agent", recommendation_agent)
    grafo.add_node("briefing_agent", briefing_agent)

    grafo.set_entry_point("query_planner")
    grafo.add_edge("query_planner", "retriever")
    grafo.add_edge("retriever", "extractor")
    grafo.add_edge("extractor", "classifier")
    grafo.add_edge("classifier", "evidence_validator")
    grafo.add_edge("evidence_validator", "rag_agent")
    grafo.add_edge("rag_agent", "recommendation_agent")
    grafo.add_edge("recommendation_agent", "briefing_agent")
    grafo.add_edge("briefing_agent", END)

    return grafo.compile()
