from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from datetime import datetime

load_dotenv()                      # lê o .env (procura na pasta atual e nas pastas acima)
client = genai.Client(
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=2,        # tenta até 4 vezes
            initial_delay=2,   # espera 2s, depois ~4s, ~8s... (exponential backoff)
            max_delay=20,
        )
    )
)
MODELO = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = Path("prompts/sdr.md").read_text(encoding="utf-8")

chat = client.chats.create(
    model=MODELO,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.6,           # 0 = sempre igual; 1+ = mais criativo
        max_output_tokens=300,     # teto de segurança para o tamanho da resposta
    ),
)

def salvar_conversa(chat) -> Path:
    pasta = Path("evals/conversas")
    pasta.mkdir(parents=True, exist_ok=True)          # cria a pasta se não existir
    arquivo = pasta / f"{datetime.now():%Y-%m-%d_%H%M%S}.md"

    linhas = []
    for msg in chat.get_history():                    # o histórico que o chat guarda
        quem = "Lead" if msg.role == "user" else "Bia"
        texto = "".join(p.text or "" for p in msg.parts)
        linhas.append(f"**{quem}:** {texto}\n")

    arquivo.write_text("\n".join(linhas), encoding="utf-8")
    return arquivo

print("Converse com a Bia (digite 'sair' para encerrar)\n")
while (mensagem := input("Você: ").strip()).lower() != "sair":
    if not mensagem:               # Enter vazio: ignora em vez de mandar "" para a API
        continue
    try:
        resposta = chat.send_message(mensagem)
    except errors.APIError as erro:
        print(f"Bia: Desculpa, tive uma instabilidade aqui. Pode mandar de novo? [{erro.code}]\n")
        continue
    print(f"Bia: {resposta.text}\n")

caminho = salvar_conversa(chat)
print(f"Conversa salva em {caminho}")