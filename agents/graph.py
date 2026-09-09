from langgraph.graph import StateGraph, END
from state import RadarState
from query_planner import query_planner
from retriever import retriever

def montar_grafo():
    grafo = StateGraph(RadarState)

    grafo.add_node("query_planner", query_planner)
    grafo.add_node("retriever", retriever)

    grafo.set_entry_point("query_planner")
    grafo.add_edge("query_planner", "retriever")
    grafo.add_edge("retriever", END)

    return grafo.compile()
