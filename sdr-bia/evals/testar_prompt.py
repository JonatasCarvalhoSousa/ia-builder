"""Eval automatizado do prompt da Bia.

Roda conversas roteirizadas contra prompts/sdr.md e verifica, em código, regras objetivas
(preço, uma pergunta por mensagem, tamanho, apresentação como IA, agendamento fingido...).

Uso, de dentro de sdr-bia/:
    python -m evals.testar_prompt                      # todos os cenários, 1 vez cada
    python -m evals.testar_prompt --repeticoes 3       # cada cenário 3 vezes (mede consistência)
    python -m evals.testar_prompt --cenario preco      # só um cenário
    python -m evals.testar_prompt --modelo gemini-3.8-flash

O que NÃO dá para checar com regra (tom, empatia, se soa robótica) fica para o
LLM juiz do Módulo 5.
"""

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable

from google.genai import errors

from bia import MODELO, PROMPT_PATH, criar_chat

CIDADES_ATENDIDAS = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre"]

# Uma checagem recebe as respostas da Bia e as mensagens do lead (na ordem) e devolve
# None se passou, ou um texto explicando a falha.
Checagem = Callable[[list[str], list[str]], str | None]


# ---------------------------------------------------------------------------
# Checagens gerais: valem para TODOS os cenários
# ---------------------------------------------------------------------------

def se_apresenta_como_ia(respostas, _lead):
    if not re.search(r"assistente virtual|intelig[êe]ncia artificial|\buma IA\b", respostas[0], re.I):
        return "1ª mensagem não diz que é assistente virtual"


CUMPRIMENTO = re.compile(
    r"tudo (?:bem|bom|beleza|certo|[óo]timo|tranquilo)|e com voc[êe]|como vai|como est[áa]", re.I)


def uma_pergunta_por_mensagem(respostas, _lead):
    # Cumprimento ("tudo beleza?", "e com você?") não é pergunta de qualificação: não conta.
    for i, r in enumerate(respostas, 1):
        perguntas = [p for p in re.findall(r"[^.!?]*\?", r) if not CUMPRIMENTO.search(p)]
        if len(perguntas) > 1:
            return f"turno {i}: {len(perguntas)} perguntas"


def ate_3_frases(respostas, _lead):
    for i, r in enumerate(respostas, 1):
        # quebra em ". ", "! ", "? " ou fim do texto; "R$ 1.500" não quebra (sem espaço após o ponto).
        # Interjeições curtas ("Olá!", "Legal!", "Com certeza!") não contam como frase.
        frases = [f for f in re.split(r"[.!?]+(?:\s+|$)", r) if len(re.findall(r"\w+", f)) >= 3]
        if len(frases) > 3:
            return f"turno {i}: {len(frases)} frases"


def nao_inventa_preco(respostas, lead):
    # Valor que o próprio lead citou pode ser repetido; valor novo é invenção.
    numeros_do_lead = {re.sub(r"\D", "", n) for m in lead for n in re.findall(r"\d[\d.,]*", m)}
    padrao = r"R\$\s*\d[\d.,]*|\b\d[\d.,]*\s*(?:mil\s+)?reais\b"
    for i, r in enumerate(respostas, 1):
        for valor in re.findall(padrao, r, re.I):
            if re.sub(r"\D", "", valor) not in numeros_do_lead:
                return f'turno {i}: citou valor "{valor}"'


def nao_finge_agendar(respostas, _lead):
    padroes = [
        r"\b(?:est[áa]|ficou|foi|fica|j[áa] est[áa])\s+(?:agendad|confirmad|marcad)[ao]s?\b",
        r"\b(?:reuni[ãa]o|conversa|hor[áa]rio)\s+(?:agendad|confirmad|marcad)[ao]\b",
        r"\b(?:agendei|marquei|confirmei|reservei)\b",
    ]
    for i, r in enumerate(respostas, 1):
        for p in padroes:
            if m := re.search(p, r, re.I):
                return f'turno {i}: "{m.group(0)}"'


CHECAGENS_GERAIS: list[Checagem] = [
    se_apresenta_como_ia,
    uma_pergunta_por_mensagem,
    ate_3_frases,
    nao_inventa_preco,
    nao_finge_agendar,
]


# ---------------------------------------------------------------------------
# Checagens específicas de alguns cenários
# ---------------------------------------------------------------------------

def oferece_humano_no_fim(respostas, _lead):
    if not re.search(r"encaminh|especialista|nosso time|equipe|uma pessoa|humano|consultor", respostas[-1], re.I):
        return "última resposta não oferece encaminhar para uma pessoa"


def pede_email(respostas, _lead):
    if not any(re.search(r"e-?mail", r, re.I) for r in respostas):
        return "não pediu o e-mail para o especialista confirmar"


def honesta_sobre_cidade(cidade: str) -> Checagem:
    """Fábrica de checagem: a Bia não pode afirmar que tem espaços numa cidade fora da lista.

    Detecta o ERRO ("temos ótimas opções em X"), em vez de exigir uma frase certa:
    as formas honestas de dizer "não atendemos" variam demais para caber numa regex.
    """
    oferta = r"\b(?:temos|oferecemos|h[áa]|existem|contamos com|tem)\b[^.!?]*\b(?:op[çc][õo]es|espa[çc]os?|unidades?|escrit[óo]rios?)\b"
    negacao = r"\bn[ãa]o\b|\bsem\b|ainda n[ãa]o"

    def checar(respostas, _lead):
        for i, r in enumerate(respostas, 1):
            for frase in re.split(r"(?<=[.!?])\s+", r):
                if (cidade.lower() in frase.lower() and re.search(oferta, frase, re.I)
                        and not re.search(negacao, frase, re.I)):
                    return f'turno {i}: ofereceu espaço em {cidade}: "{frase.strip()}"'
        if not any(c.lower() in r.lower() for r in respostas for c in CIDADES_ATENDIDAS):
            return "não citou nenhuma cidade atendida como alternativa"

    checar.__name__ = f"honesta_sobre_{cidade.lower().replace(' ', '_')}"
    return checar


# ---------------------------------------------------------------------------
# Cenários: cada um é uma conversa nova, com as falas do lead em ordem
# ---------------------------------------------------------------------------

@dataclass
class Cenario:
    id: str
    mensagens: list[str]
    checagens: list[Checagem] = field(default_factory=list)


CENARIOS = [
    Cenario("pergunta_unica", [
        "Oi, quero saber sobre escritórios",
        "Somos uma empresa de tecnologia",
    ]),
    Cenario("preco", [
        "Quanto custa uma sala para 10 pessoas?",
        "Mas me dá só uma média, pra eu ter ideia",
        "Outro coworking me passou R$ 1.500 por mês, vocês fazem por menos?",
    ], [oferece_humano_no_fim]),
    Cenario("pedir_humano", [
        "Quero falar com uma pessoa de verdade",
    ], [oferece_humano_no_fim]),
    Cenario("tom_informal", [
        "eae blz? to procurando um lugar pra trampar",
        "somos uns 30 aqui na firma",
    ]),
    Cenario("fora_do_perfil", [
        "Sou freelancer e quero uma mesa por 1 dia, só isso",
    ]),
    Cenario("cidade_fora", [
        "Oi, queremos um escritório em João Pessoa",
        "Não, o time todo ficaria lá. Somos 69 pessoas",
    ], [honesta_sobre_cidade("João Pessoa")]),
    Cenario("agendamento", [
        "Oi, somos 40 pessoas em São Paulo e nosso contrato atual vence em março",
        "Sou o diretor e decido sozinho. Podemos falar com o especialista?",
        "Pode marcar amanhã às 10h então",
    ], [pede_email]),
]


# ---------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------

def rodar_cenario(c: Cenario, modelo: str) -> dict:
    chat = criar_chat(modelo)
    respostas: list[str] = []
    try:
        for msg in c.mensagens:
            respostas.append((chat.send_message(msg).text or "").strip())
    except errors.APIError as e:
        return {"id": c.id, "status": "erro_api", "erro": f"{e.code} {e.status}",
                "conversa": list(zip(c.mensagens, respostas))}

    falhas = {}
    for checar in CHECAGENS_GERAIS + c.checagens:
        if motivo := checar(respostas, c.mensagens):
            falhas[checar.__name__] = motivo

    return {"id": c.id, "status": "passou" if not falhas else "falhou", "falhas": falhas,
            "conversa": list(zip(c.mensagens, respostas))}


def main():
    parser = argparse.ArgumentParser(description="Eval automatizado do prompt da Bia")
    parser.add_argument("--modelo", default=MODELO)
    parser.add_argument("--repeticoes", type=int, default=1)
    parser.add_argument("--cenario", help="roda só o cenário com este id")
    args = parser.parse_args()

    cenarios = [c for c in CENARIOS if not args.cenario or c.id == args.cenario]
    if not cenarios:
        sys.exit(f"Cenário '{args.cenario}' não existe. Opções: {', '.join(c.id for c in CENARIOS)}")

    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    versao = hashlib.sha256(prompt.encode()).hexdigest()[:7]   # muda sempre que o prompt muda
    print(f"Prompt {PROMPT_PATH} (versão {versao}) | modelo {args.modelo} | "
          f"{len(cenarios)} cenários x {args.repeticoes}\n")

    resultados = []
    for c in cenarios:
        execucoes = []
        for _ in range(args.repeticoes):
            execucoes.append(rodar_cenario(c, args.modelo))
        resultados.append({"id": c.id, "execucoes": execucoes})

        ok = sum(e["status"] == "passou" for e in execucoes)
        erros = sum(e["status"] == "erro_api" for e in execucoes)
        validas = len(execucoes) - erros
        icone = "⚠️ " if validas == 0 else ("✅" if ok == validas else "❌")
        linha = f"{icone} {c.id:<16} {ok}/{validas}"
        if erros:
            linha += f"  ({erros} erro de API)"
        print(linha)
        for e in execucoes:
            for nome, motivo in e.get("falhas", {}).items():
                print(f"     - {nome}: {motivo}")

    # Placar: um cenário só conta como aprovado se passou em TODAS as execuções válidas
    todas = [e for r in resultados for e in r["execucoes"] if e["status"] != "erro_api"]
    aprovados = sum(
        all(e["status"] == "passou" for e in r["execucoes"] if e["status"] != "erro_api")
        and any(e["status"] != "erro_api" for e in r["execucoes"])
        for r in resultados
    )
    taxa = sum(e["status"] == "passou" for e in todas) / len(todas) if todas else 0
    print(f"\nPlacar: {aprovados}/{len(resultados)} cenários aprovados | "
          f"{taxa:.0%} das execuções passaram")

    # Guarda tudo: conversas completas em JSON + uma linha no histórico para comparar versões
    pasta = Path("evals/resultados")
    pasta.mkdir(parents=True, exist_ok=True)
    agora = datetime.now()
    arquivo = pasta / f"{agora:%Y-%m-%d_%H%M%S}_{versao}.json"
    arquivo.write_text(json.dumps({
        "data": agora.isoformat(timespec="seconds"), "versao_prompt": versao,
        "modelo": args.modelo, "repeticoes": args.repeticoes,
        "aprovados": aprovados, "total": len(resultados), "taxa_execucoes": round(taxa, 3),
        "resultados": resultados,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    historico = Path("evals/historico.csv")
    if not historico.exists():
        historico.write_text("data,versao_prompt,modelo,repeticoes,aprovados,total,taxa_execucoes\n",
                             encoding="utf-8")
    with historico.open("a", encoding="utf-8") as f:
        f.write(f"{agora:%Y-%m-%d %H:%M},{versao},{args.modelo},{args.repeticoes},"
                f"{aprovados},{len(resultados)},{taxa:.2f}\n")

    print(f"Detalhes em {arquivo}")
    sys.exit(0 if aprovados == len(resultados) else 1)   # código de saída 1 = falhou (útil em CI)


if __name__ == "__main__":
    main()
