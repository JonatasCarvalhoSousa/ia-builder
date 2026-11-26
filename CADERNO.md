# Caderno de estudos — AI Builder (SDR de IA)

O que vale lembrar, em poucas linhas. Atualizado a cada sessão.
Regra: se eu não consigo explicar com as minhas palavras, ainda não aprendi.

---

## 1. Negócio e vendas

### O funil do lead
`Lead → MQL → SQL → Reunião → Oportunidade/Proposta → Fechamento`

- **MQL**: tem o perfil (ICP), mas ninguém conversou ainda.
- **SQL**: o SDR conversou e confirmou **necessidade, prazo e decisor**.
- O SDR (humano ou IA) vai até a **reunião**. Proposta e fechamento são do executivo (AE/closer).

### Conceitos-chave
| Termo | Em uma frase |
|---|---|
| ICP | O tipo de empresa que mais se beneficia (aqui: times híbridos, várias cidades, escritório subutilizado) |
| Persona | Quem eu converso dentro da empresa (Facilities, RH, CFO, líder comercial) |
| SLA de resposta | Tempo até o primeiro contato. Onde a IA mais brilha: responde às 22h |
| Handoff | Passar o lead para o vendedor com resumo, sem ele ter que perguntar tudo de novo |
| BANT | Budget, Authority, Need, Timing |

### O que cada persona quer ouvir
- **CFO** → economia, sem CAPEX, valor fixo.
- **RH** → experiência do time, flexibilidade.
- **Facilities** → simplicidade operacional, um contrato só.

## 2. Princípios do agente

- **A IA conversa e entende; o código decide** (nota, regras, agendamento, limites).
- A Bia **qualifica e agenda**. Não fecha negócio, não fala de preço.
- Uma pergunta por mensagem, até 3 frases, conectar com o que o lead disse.
- Nunca finge ser humana; sempre oferece saída para uma pessoa.

## 3. Técnico (Python + Gemini)

- **Traceback:** ler de baixo para cima. A última linha diz o tipo do erro e a mensagem; as de cima mostram o caminho. Procure a primeira linha que aponta para um arquivo **meu** (ex.: `bia.py, line 26`).
- **Erros HTTP:** 4xx = problema meu (chave, nome do modelo, requisição). 5xx = problema do serviço (503 = sobrecarga, temporário). **429 RESOURCE_EXHAUSTED** = estourei a cota/limite por minuto do meu plano (é 4xx: o serviço está bem, eu é que passei do limite).
- **Diagnóstico antes de opinião (2026-11-26):** testei vários modelos com o mesmo "ok". Os `flash` grandes (3.5 a 3.8) davam 503, enquanto os `flash-lite` (3.5-lite, 3.1-lite) respondiam. Modelo mais procurado = mais 503. Ter uma lista de modelos reserva resolve.
- **Resiliência:** `types.HttpRetryOptions` (tentar de novo com espera crescente) + `try/except errors.APIError` (não derrubar o chat) + modelo reserva.
- **Memória do chat:** a API não lembra nada; o objeto `chat` guarda o histórico e reenvia tudo a cada `send_message`.

## 4. Erros que já cometi e o que aprendi

| Data | Erro | Causa | Lição |
|---|---|---|---|
| 2026-11-26 | `ServerError: 503 UNAVAILABLE` no primeiro "Olá" | Modelo sobrecarregado no Google (lado do serviço, 5xx). Meu código estava certo | Ler o traceback **de baixo para cima**. 5xx = esperar/retry/modelo reserva; 4xx = corrigir do meu lado. Agente em produção precisa de retry + try/except + mensagem de fallback, senão o chat morre na cara do lead |

## 5. Perguntas de revisão

Perguntas que respondi nas sessões, com a resposta corrigida. Releia antes de entrevistas.

| Data | Pergunta | Resposta certa (resumo) | Acertei? |
|---|---|---|---|
| | | | |
