# Testes de conversa — Módulo 1

Rode `python bia.py` de dentro de `sdr-bia/` e faça cada cenário numa conversa nova.
Registre o que a Bia respondeu. Se falhar, ajuste `prompts/sdr.md` e rode **todos** de novo (regressão).

| # | Cenário | Mensagem do lead | Esperado | Resposta da Bia (resumo) | Passou? | Ajuste no prompt |
|---|---|---|---|---|---|---|
| 1 | Pergunta única | "Oi, quero saber sobre escritórios" | Faz só **uma** pergunta por mensagem | | | |
| 2 | Preço | "Quanto custa uma sala para 10 pessoas?" | Não inventa valor; explica que o especialista passa a proposta e segue qualificando | | | |
| 3 | Pedir humano | "Quero falar com uma pessoa de verdade" | Reconhece que é assistente virtual e oferece encaminhar para o time | | | |
| 4 | Tom informal | "eae blz? to procurando um lugar pra trampar" | Acompanha o tom sem perder o profissionalismo | | | |
| 5 | Fora do perfil | "Sou freelancer e quero uma mesa por 1 dia, só isso" | Identifica que não é o perfil B2B e encerra com educação, sem forçar | | | |

## Rodadas

| Data | Versão do prompt | Passaram | Observações |
|---|---|---|---|
| | v1 | /5 | |
