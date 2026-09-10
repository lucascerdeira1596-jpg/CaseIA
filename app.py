from datetime import datetime
from html import escape

import streamlit as st

from core.graph import montar_grafo
from infrastructure.llm_client import get_estatisticas_uso, resetar_estatisticas_uso

st.set_page_config(page_title="NVIDIA Startup AI Radar", page_icon="◉", layout="wide", initial_sidebar_state="collapsed")


@st.cache_resource
def carregar_grafo():
    return montar_grafo()


def icone(nome: str) -> str:
    return f'<span class="material-symbols-rounded" aria-hidden="true">{nome}</span>'


def aplicar_estilo():
    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400..700,0..1,-50..200');
          :root { --accent:#9cdb30; --ink:#f2f6f2; --muted:#aebbb2; --line:rgba(217,235,220,.14); --surface:rgba(22,35,27,.88); }
          .stApp { background:radial-gradient(circle at 92% -8%,rgba(118,185,0,.22),transparent 25%),radial-gradient(circle at 8% 108%,rgba(118,185,0,.12),transparent 28%),linear-gradient(135deg,#0c120f 0%,#132018 52%,#1b3022 100%); color:var(--ink); font-family:'Manrope',sans-serif; min-height:100vh; }
          .stApp:before { content:''; position:fixed; z-index:0; width:420px; height:420px; right:-155px; top:-140px; border:1px solid rgba(156,219,48,.28); border-radius:50%; box-shadow:0 0 0 58px rgba(156,219,48,.045),0 0 0 116px rgba(156,219,48,.025); pointer-events:none; }
          .block-container { position:relative; z-index:1; }
          #MainMenu, footer, header { visibility:hidden; }
          .block-container { max-width:1180px; padding:2.3rem 2rem 4rem; }
          .material-symbols-rounded { font-family:'Material Symbols Rounded'; font-weight:normal; font-style:normal; font-size:1.15rem; line-height:1; vertical-align:-.2em; }
          .radar-nav { display:flex; justify-content:space-between; align-items:center; margin-bottom:1.8rem; color:var(--muted); }.radar-brand { display:flex; align-items:center; gap:.72rem; color:#f5f8f5; }.radar-brand .material-symbols-rounded { color:var(--accent); font-size:1.8rem; font-variation-settings:'FILL' 1; }.brand-name { font-size:1.5rem; font-weight:800; letter-spacing:-.045em; line-height:1; }.radar-status { font-size:.72rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
          .search-card { background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:1.15rem 1.25rem .45rem; box-shadow:0 18px 42px rgba(0,0,0,.18); margin-bottom:1.3rem; backdrop-filter:blur(10px); }.search-card-title { display:flex; gap:.5rem; align-items:center; color:#f0f5f1; font-size:.88rem; font-weight:800; margin-bottom:.2rem; }.search-card-title .material-symbols-rounded { color:var(--accent); font-variation-settings:'FILL' 1; }.examples { color:var(--muted); font-size:.78rem; margin:.1rem 0 .5rem; }
          div[data-testid='stTextInput'] label { color:#dce7df; font-size:.82rem; font-weight:700; } div[data-testid='stTextInput'] input { background:#0e1711; color:#f1f6f1; border:1px solid rgba(211,233,215,.23); border-radius:10px; padding:.75rem .9rem; font-size:.94rem; } div[data-testid='stTextInput'] input:focus { border-color:var(--accent); box-shadow:0 0 0 3px rgba(156,219,48,.14); }
          div[data-testid='stFormSubmitButton'] > button, div[data-testid='stDownloadButton'] > button { border:1px solid #8bc72c; border-radius:10px; background:#476f08; color:#fff; font-family:'Manrope',sans-serif; font-weight:800; min-height:43px; box-shadow:0 5px 14px rgba(0,0,0,.22); } div[data-testid='stFormSubmitButton'] > button:hover, div[data-testid='stDownloadButton'] > button:hover { background:#5e920c; border-color:#a2df3b; color:#fff; }
          .section-kicker { display:flex; align-items:center; gap:.45rem; color:#aebbb2; font-family:'DM Mono',monospace; font-size:.72rem; letter-spacing:.08em; text-transform:uppercase; margin-top:1.8rem; }.section-kicker .material-symbols-rounded { color:var(--accent); } h2 { color:#f1f6f1; font-size:1.4rem !important; letter-spacing:-.035em; margin-top:.3rem !important; }
          div[data-testid='stMarkdownContainer'], div[data-testid='stMarkdownContainer'] p, div[data-testid='stMarkdownContainer'] li, div[data-testid='stExpanderDetails'] { color:#e2ebe4; }
          div[data-testid='stMetric'] { background:var(--surface); border:1px solid var(--line); border-radius:13px; padding:.85rem 1rem; } div[data-testid='stMetricLabel'] { color:#aebbb2; font-size:.75rem; font-weight:700; } div[data-testid='stMetricValue'] { color:#f2f7f3; font-size:1.55rem; font-weight:800; }
          .startup-meta { display:flex; align-items:center; gap:.55rem; color:#b7c4bb; font-size:.8rem; margin:.15rem 0 .9rem; }.badge { display:inline-flex; align-items:center; border-radius:99px; padding:.25rem .62rem; font-family:'DM Mono',monospace; font-size:.7rem; font-weight:500; }.badge-native { background:#294a10; color:#d6f5a4; }.badge-enabled { background:#193b59; color:#c3e4ff; }.badge-non-ai { background:#303936; color:#d5ddd7; }.confidence { font-weight:800; color:#d5ddd7; }.confidence-high { color:#a8e547; }.confidence-medium { color:#f1d568; }.confidence-low { color:#f69085; }
          div[data-testid='stExpander'] { border:1px solid var(--line); border-radius:14px; background:var(--surface); margin-bottom:.7rem; overflow:hidden; } div[data-testid='stExpander'] details summary { padding:.15rem .2rem; font-weight:800; color:#f1f6f1; } div[data-testid='stVerticalBlockBorderWrapper'] { border-color:var(--line); border-radius:16px; background:var(--surface); } div[data-testid='stAlert'] { border-radius:12px; }
          @media (max-width:700px) { .block-container { padding:1.15rem 1rem 3rem; }.radar-status { display:none; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def montar_texto_exportacao(pergunta, resultado, stats):
    startups = resultado.get("startups_candidatas", [])
    perfis = resultado.get("perfis_classificados", [])
    linhas = ["# NVIDIA Startup AI Radar — Relatório", "", f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}", f"**Pergunta:** {pergunta}", f"**Startups candidatas encontradas:** {len(startups)}"]
    total_chamadas = stats["nvidia"] + stats["groq"]
    if total_chamadas:
        linhas.append(f"**Motor de IA dos agentes:** {stats['nvidia']} chamadas via NVIDIA NIM (nemotron-3-super-120b-a12b), {stats['groq']} via Groq (fallback)")
    linhas.extend(["", "## Classificação e transparência por startup"])
    for perfil in perfis:
        linhas.extend(["", f"### {perfil['nome']} — {perfil.get('classificacao', '?')}", f"- **Confiança da classificação:** {perfil.get('confianca', 'N/A')}", f"- **Justificativa da classificação:** {perfil.get('justificativa', 'N/A')}", f"- **Uso de IA:** {perfil.get('uso_de_ia_descricao', 'N/A')}", f"- **Evidências válidas:** {perfil.get('qtd_evidencias_validas', 0)}", f"- **Rejeitadas por URL inválida:** {perfil.get('qtd_rejeitadas_por_url', 0)}", f"- **Rejeitadas — não sustentam a afirmação:** {perfil.get('qtd_rejeitadas_por_semantica', 0)}"])
        if perfil.get("possivelmente_alucinado"):
            linhas.append("- ⚠️ Pelo menos uma evidência citada pelo modelo foi descartada na validação.")
    return "\n".join(linhas + ["", "---", "", resultado["briefing_final"]])


def classe_classificacao(classificacao: str) -> str:
    return {"ai-native": "badge-native", "ai-enabled": "badge-enabled", "non-ai": "badge-non-ai"}.get(classificacao.lower(), "badge-non-ai")


def renderizar_startup(perfil):
    classificacao = perfil.get("classificacao", "Não classificada")
    confianca = perfil.get("confianca", "N/A")
    chave_confianca = {"alta": "high", "média": "medium", "baixa": "low"}.get(confianca.lower(), "")
    with st.expander(f"{perfil['nome']}  ·  {classificacao}"):
        st.markdown(f"<div class='startup-meta'><span class='badge {classe_classificacao(classificacao)}'>{escape(classificacao)}</span><span>Confiança: <span class='confidence confidence-{chave_confianca}'>{escape(confianca)}</span></span></div>", unsafe_allow_html=True)
        st.markdown(f"**Racional da classificação**  \n{perfil.get('justificativa', 'N/A')}")
        st.markdown(f"**Uso de IA identificado**  \n{perfil.get('uso_de_ia_descricao', 'N/A')}")
        st.markdown("<div class='section-kicker'>" + icone("verified") + " Auditoria de evidências</div>", unsafe_allow_html=True)
        validas, urls, semantica = st.columns(3)
        validas.metric("Evidências válidas", perfil.get("qtd_evidencias_validas", 0))
        urls.metric("URLs descartadas", perfil.get("qtd_rejeitadas_por_url", 0))
        semantica.metric("Trechos descartados", perfil.get("qtd_rejeitadas_por_semantica", 0))
        if perfil.get("possivelmente_alucinado"):
            st.warning("Há evidências descartadas na validação. Consulte as métricas de auditoria acima.")


aplicar_estilo()
app = carregar_grafo()
if "resultado" not in st.session_state:
    st.session_state.resultado = None
    st.session_state.stats = None
    st.session_state.pergunta_usada = None

st.markdown(f"<div class='radar-nav'><div class='radar-brand'>{icone('neurology')} <span class='brand-name'>NVIDIA Startup AI Radar</span></div><div class='radar-status'>Inteligência de ecossistema · Brasil</div></div>", unsafe_allow_html=True)
st.markdown("<div class='search-card'><div class='search-card-title'>" + icone("travel_explore") + " Inicie uma análise</div><div class='examples'>Exemplos: healthtechs com IA intensiva · startups jurídicas · atendimento por voz</div>", unsafe_allow_html=True)
with st.form("formulario_busca", border=False):
    pergunta = st.text_input("O que você está procurando?", placeholder="Ex.: Quero startups de saúde que usam IA de forma intensiva")
    buscar = st.form_submit_button("Executar análise", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if buscar:
    if not pergunta.strip():
        st.warning("Escreva uma pergunta para iniciar a análise.")
    else:
        resetar_estatisticas_uso()
        with st.spinner("Mapeando startups, validando evidências e preparando recomendações..."):
            st.session_state.resultado = app.invoke({"pergunta_usuario": pergunta})
        st.session_state.stats = get_estatisticas_uso()
        st.session_state.pergunta_usada = pergunta

resultado = st.session_state.resultado
if resultado is not None:
    stats = st.session_state.stats
    startups = resultado.get("startups_candidatas", [])
    perfis = resultado.get("perfis_classificados", [])
    total_chamadas = stats["nvidia"] + stats["groq"]
    st.markdown("<div class='section-kicker'>" + icone("insights") + " Resultado da análise</div>", unsafe_allow_html=True)
    col_startups, col_nvidia, col_groq = st.columns(3)
    col_startups.metric("Startups analisadas", len(startups))
    col_nvidia.metric("Chamadas NVIDIA NIM", stats["nvidia"])
    col_groq.metric("Fallback Groq", stats["groq"])
    if total_chamadas:
        st.info(f"Execução concluída com {stats['nvidia']} chamadas via NVIDIA NIM e {stats['groq']} via Groq como fallback de resiliência.")
    if not startups:
        st.warning("Nenhuma startup encontrada para essa consulta. Tente ampliar os termos de busca.")
    else:
        st.markdown("<div class='section-kicker'>" + icone("domain") + " Mapa de startups</div>", unsafe_allow_html=True)
        st.subheader(f"{len(startups)} startup(s) candidata(s)")
        for perfil in perfis:
            renderizar_startup(perfil)
        st.markdown("<div class='section-kicker'>" + icone("description") + " Briefing executivo</div>", unsafe_allow_html=True)
        st.subheader("Recomendações NVIDIA")
        with st.container(border=True):
            st.markdown(resultado["briefing_final"])
        texto_exportacao = montar_texto_exportacao(st.session_state.pergunta_usada, resultado, stats)
        st.download_button(label="Baixar relatório completo (.md)", data=texto_exportacao.encode("utf-8"), file_name=f"briefing_nvidia_radar_{datetime.now().strftime('%Y%m%d_%H%M')}.md", mime="text/markdown", use_container_width=True)
