from typing import TypedDict, Optional

class RadarState(TypedDict):
    pergunta_usuario: str
    criterios_busca: Optional[dict]
    startups_candidatas: Optional[list]
    perfis_estruturados: Optional[list]
    perfis_classificados: Optional[list]
    recomendacoes: Optional[list]
    briefing_final: Optional[str]