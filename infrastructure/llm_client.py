import os
import time
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm_nvidia = ChatNVIDIA(
    model="nvidia/nemotron-3-super-120b-a12b",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0,
    max_tokens=4096,
    timeout=30,
)

llm_groq = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=4096,
)

def _eh_recuperavel(erro_str):
    return (
        "503" in erro_str
        or "429" in erro_str
        or "timeout" in erro_str
        or "timed out" in erro_str
        or "rate limit" in erro_str
        or "too many requests" in erro_str
    )

_estatisticas_uso = {"nvidia": 0, "groq": 0}

def get_estatisticas_uso():
    return dict(_estatisticas_uso)

def resetar_estatisticas_uso():
    _estatisticas_uso["nvidia"] = 0
    _estatisticas_uso["groq"] = 0

def invoke_llm(mensagens, max_tentativas_nvidia=2, max_tentativas_groq=3):
    for tentativa in range(max_tentativas_nvidia):
        try:
            resposta = llm_nvidia.invoke(mensagens)
            _estatisticas_uso["nvidia"] += 1
            return resposta
        except Exception as e:
            erro_str = str(e).lower()
            if _eh_recuperavel(erro_str) and tentativa < max_tentativas_nvidia - 1:
                time.sleep(2 ** tentativa)
            elif _eh_recuperavel(erro_str):
                print("[NVIDIA indisponível — usando Groq]")
                break
            else:
                raise

    for tentativa in range(max_tentativas_groq):
        try:
            resposta = llm_groq.invoke(mensagens)
            _estatisticas_uso["groq"] += 1
            return resposta
        except Exception as e:
            erro_str = str(e).lower()
            if _eh_recuperavel(erro_str) and tentativa < max_tentativas_groq - 1:
                print(f"[Groq limitado, tentativa {tentativa + 1}/{max_tentativas_groq}, aguardando...]")
                time.sleep(2 ** (tentativa + 2))
            else:
                raise