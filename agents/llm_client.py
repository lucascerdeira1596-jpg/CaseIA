import os
import time
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()

llm_nvidia = ChatNVIDIA(
    model="nvidia/nemotron-3-super-120b-a12b",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0,
    max_tokens=2048,
)

def invoke_llm(mensagens, max_tentativas=3):
    for tentativa in range(max_tentativas):
        try:
            return llm_nvidia.invoke(mensagens)
        except Exception as e:
            if "503" in str(e) and tentativa < max_tentativas - 1:
                espera = 2 ** tentativa
                print(f"[NVIDIA NIM sobrecarregado, tentativa {tentativa + 1}/{max_tentativas}, aguardando {espera}s...]")
                time.sleep(espera)
            else:
                raise
