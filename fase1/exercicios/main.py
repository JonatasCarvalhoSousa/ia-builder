import json, os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

load_dotenv()                      # lê o .env
chave = os.environ["GEMINI_API_KEY"]

# 1. Tipos e funções com type hints
def resumir(texto: str, max_palavras: int = 50) -> str:
    palavras = texto.split()
    return " ".join(palavras[:max_palavras])

# 2. Modelos Pydantic: o "contrato" dos dados
class Produto(BaseModel):
    nome: str
    preco: float
    em_estoque: bool = True

# 3. JSON <-> objeto, com validação
bruto = '{"nome": "Queijo", "preco": "29.9"}'
produto = Produto.model_validate_json(bruto)   # converte "29.9" em 29.9
print(produto.model_dump())

# 4. Tratar erro em vez de quebrar
try:
    Produto.model_validate_json('{"nome": "Leite"}')
except ValidationError as erro:
    print("Faltou campo:", erro.errors()[0]["loc"])