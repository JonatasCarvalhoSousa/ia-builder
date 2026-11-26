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
- **Lacuna no prompt vira invenção:** se o prompt não diz em quais cidades a empresa atua, o modelo inventa uma resposta plausível ("temos ótimas opções em João Pessoa"). Tudo o que a Bia precisa afirmar tem que vir do prompt ou de uma ferramenta.
- **Alucinação de ação:** sem ferramenta de agenda, a Bia disse "tudo anotado, agendado". O modelo *descreve* ações que não executou. A solução definitiva é ferramenta + código (Módulo 3); até lá, o prompt deixa claro o que ela não consegue fazer.
- **Onde corrigir cada problema:** prompt (estilo, regras, informações fixas), ferramenta (dados e ações reais), código (validação, regras de negócio). Saber escolher é o trabalho do AI Builder.

## 3. Técnico (Python + Gemini)

- **Traceback:** ler de baixo para cima. A última linha diz o tipo do erro e a mensagem; as de cima mostram o caminho. Procure a primeira linha que aponta para um arquivo **meu** (ex.: `bia.py, line 26`).
- **Erros HTTP:** 4xx = problema meu (chave, nome do modelo, requisição). 5xx = problema do serviço (503 = sobrecarga, temporário). **429 RESOURCE_EXHAUSTED** = estourei a cota/limite por minuto do meu plano (é 4xx: o serviço está bem, eu é que passei do limite).
- **Diagnóstico antes de opinião (2026-11-26):** testei vários modelos com o mesmo "ok". Os `flash` grandes (3.5 a 3.8) davam 503, enquanto os `flash-lite` (3.5-lite, 3.1-lite) respondiam. Modelo mais procurado = mais 503. Ter uma lista de modelos reserva resolve.
- **Resiliência:** `types.HttpRetryOptions` (tentar de novo com espera crescente) + `try/except errors.APIError` (não derrubar o chat) + modelo reserva.
- **Memória do chat:** a API não lembra nada; o objeto `chat` guarda o histórico e reenvia tudo a cada `send_message`.
- **`if __name__ == "__main__":`** roda o bloco só quando o arquivo é executado direto, não quando é importado. Assim o eval importa `criar_chat` do `bia.py` e testa **a mesma configuração** do chat (nunca uma cópia).
- **`python -m evals.testar_prompt`**: roda como módulo a partir da pasta atual, então `from bia import ...` funciona.

## 3.1 Evals (o que aprendi construindo o `evals/testar_prompt.py`)

- **Eval automatizado** = cenários roteirizados + checagens em código + placar salvo por versão do prompt (hash). Mudou o prompt, roda de novo e compara no `evals/historico.csv`.
- **Valide o avaliador.** A 1ª rodada deu 1/7, mas metade das falhas era bug do eval ("Olá!" contando como frase, regex que não conhecia "sem operação"). Antes de confiar no placar, leia as conversas das falhas.
- **Detecte o erro, não a frase certa.** Existem infinitas formas honestas de dizer "não atendemos lá"; já as formas de inventar ("temos opções em X") são poucas. A checagem fica mais robusta procurando o comportamento proibido.
- **Não determinismo:** a mesma Bia se apresentou numa rodada e não na outra, no mesmo cenário. Por isso existe `--repeticoes`: um cenário só está aprovado se passa todas as vezes.
- **Limite das regras em código:** regex não percebe que a Bia ofereceu mesa avulsa para um freelancer (fora do perfil B2B) nem que ela dispensou um lead de 69 pessoas. Isso precisa de **LLM juiz** com rubrica (Módulo 5).

## 4. Erros que já cometi e o que aprendi

| Data | Erro | Causa | Lição |
|---|---|---|---|
| 2026-11-26 | `ServerError: 503 UNAVAILABLE` no primeiro "Olá" | Modelo sobrecarregado no Google (lado do serviço, 5xx). Meu código estava certo | Ler o traceback **de baixo para cima**. 5xx = esperar/retry/modelo reserva; 4xx = corrigir do meu lado. Agente em produção precisa de retry + try/except + mensagem de fallback, senão o chat morre na cara do lead |

## 5. Perguntas de revisão

Perguntas que respondi nas sessões, com a resposta corrigida. Releia antes de entrevistas.

| Data | Pergunta | Resposta certa (resumo) | Acertei? |
|---|---|---|---|
| | | | |
