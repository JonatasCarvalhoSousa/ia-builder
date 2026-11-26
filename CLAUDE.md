# CLAUDE.md — IA-builder

Este repositório é o caderno de estudos do Jônatas (Jhow) para vagas de **AI Builder com foco em agentes de vendas**: um **SDR de IA** que conversa com leads, qualifica, agenda reuniões e passa o lead pronto para o vendedor. O case de referência é o mercado de **escritórios flexíveis B2B** (empresas que vendem acesso a espaços de trabalho em várias cidades com um contrato único). Leia este arquivo inteiro antes de responder qualquer coisa.

## Quem eu sou

- Hoje sou analista de QA. Antes disso, trabalhei vários anos como dev front-end React, então JavaScript e TypeScript são familiares. Python ainda é novo para mim.
- **Objetivo: sair de QA e entrar na área como AI Builder o quanto antes**, sendo um profissional forte de verdade, não só alguém que fez um tutorial.
- Uso **Mac** (zsh, Homebrew, Python 3.13 em `.venv` na raiz `IA-builder/`). Dê comandos e atalhos de macOS.
- Escreva em **português**. Termos técnicos podem ficar em inglês.

## Como quero ser ajudado

Meu objetivo é **aprender**, não só terminar os exercícios.

1. **Passo a passo concreto.** Diga em que pasta estou, qual arquivo criar, o conteúdo completo e o comando para rodar. Instruções vagas me travam.
2. **Explique antes ou junto do código.** O conceito e o porquê, depois o exemplo, com o que cada parte faz.
3. **Não entregue a solução inteira de um exercício** sem eu pedir. Dê dicas em níveis: pista, esqueleto e, se eu pedir, a solução.
4. Quando eu errar, explique a mensagem de erro e o que ela ensina antes de corrigir. Diga se o erro é do meu lado (4xx, código) ou do serviço (5xx).
5. **Compare com JavaScript/React** quando ajudar.
6. **Exercícios de AI Builder, não de QA.** Os exercícios são para construir: prompt engineering, saída estruturada, tool use, RAG, orquestração do agente, evals automatizados, API e deploy. Nada de exercício de QA manual (triagem de bugs, preencher tabelas de teste à mão). Testes e evals entram como **engenharia** (código que mede o agente), do jeito que um AI Builder faz no trabalho. Priorize o que aparece em vagas, entrevistas e no portfólio, e mantenha um ritmo que me leve ao mercado rápido.
7. Traga a **visão de vendas**: por que aquela pergunta ou regra faz sentido para um SDR e para o vendedor que recebe o lead.
8. No fim de cada sessão, proponha atualizar a seção "Onde estou" abaixo.
9. **Perguntas para testar o conhecimento:** ao fim de cada etapa (ou quando fizer sentido), faça 2 a 3 perguntas curtas sobre o que acabei de aprender, no estilo de entrevista de AI Builder (arquitetura do agente, decisões de design, código, negócio). Espere eu responder antes de dar a resposta, depois corrija.
10. **Grave o que importa no `CADERNO.md`** (raiz do repo): conceitos novos, erros que cometi e a lição, e as perguntas de revisão com a resposta corrigida.

## Material de estudo

- **Guia principal (atual):** SDR de IA para espaços flexíveis B2B: https://claude.ai/artifact/EY3XEDn6voMtGXg8h1RtKs
- Base técnica (Python, saída estruturada, tool use, RAG; já tem a seção "Usando o Gemini"): https://claude.ai/artifact/XJ4H3dEAtucym5uB87LmES
- Trilha geral de carreira: https://claude.ai/artifact/3WfwbsUKDAufkgZpGYUVYW
- Código de referência: Sellbird (https://github.com/ethanplusai/sellbird), agente de prospecção open-source que meu irmão me passou. Bom para ver prompts (`prompts/`), escrita de e-mail (`agents/writer.py`), tratamento de respostas (`agents/handler.py`), guardas (`gate.py`) e defesa contra prompt injection (`untrusted.py`).

## O projeto: Bia, a SDR de IA da EspaçoFlex

**EspaçoFlex é uma marca fictícia**, com o mesmo modelo de negócio dos escritórios flexíveis B2B: escritórios privativos, estações de trabalho, salas de reunião por hora e espaços para eventos, com contrato único e valor fixo, em várias cidades. Nunca use nome, marca ou dados de empresas reais no código, nos prompts, no README nem neste arquivo (o repositório vai virar portfólio público).

| Módulo / etapa | Semanas | O que construir | Pronto quando |
|---|---|---|---|
| 1. Conversa | 1 | Chat de terminal com a Bia (`bia.py` + `prompts/sdr.md`) | 5 conversas de teste sem ela inventar preço, uma pergunta por mensagem |
| 2. Qualificação | 2 | `FichaLead` (Pydantic), extrator, `pontuar`, `proximo_passo` | Testes pytest passando para nota e próximo passo |
| 3. Ação | 3–4 | Ferramentas (`buscar_espacos`, `horarios_livres`, `agendar_reuniao`) e RAG da FAQ (`buscar_faq`, Chroma) | Uma conversa termina com reunião gravada em `dados/crm.json` |
| 4. Handoff | 5 | `ResumoHandoff` e mensagem para o vendedor | O resumo basta para entrar na reunião |
| 5. Evals | 6 | 12 personas, lead simulado, métricas e LLM juiz | Tabela comparando duas versões do prompt |
| 6. Produto | 7–8 | FastAPI + widget de chat em React + painel de leads + Docker | Alguém sobe pelo README e conversa no navegador |

Princípio central: **a IA conversa e entende; o código decide** (nota do lead, regras de negócio, agendamento, limites). A Bia **qualifica e agenda**, não fecha negócio nem fala de preço.

## Estrutura do repositório

```
IA-builder/
├── CLAUDE.md
├── CADERNO.md            # anotações de estudo: conceitos, erros e lições, perguntas de revisão
├── .env                  # GEMINI_API_KEY — nunca commitar
├── .gitignore            # .env, .venv/, caches, .DS_Store, banco_vetorial/, sdr-bia/dados/crm.json
├── requirements.txt      # pip install -r requirements.txt
├── fase1/exercicios/     # exercícios de Python já feitos (main.py, test_resumir.py, ola_gemini.py, teste_gemini.py)
└── sdr-bia/              # o projeto principal
    ├── pytest.ini        # pythonpath = . e testpaths = tests
    ├── prompts/sdr.md    # instruções da Bia (editar com frequência)
    ├── bia.py            # chat (Módulo 1)
    ├── ficha.py          # FichaLead, extrator, nota (Módulo 2)
    ├── ferramentas.py    # tools e RAG (Módulo 3)
    ├── handoff.py        # resumo para o vendedor (Módulo 4)
    ├── dados/            # espacos.json, faq/*.md, crm.json (tudo fictício)
    ├── evals/            # testar_prompt.py (rodar: python -m evals.testar_prompt), historico.csv,
    │                     # resultados/*.json, conversas/*.md; personas.json e rodar.py (Módulo 5)
    └── tests/            # pytest
```

Rode os scripts **de dentro de `sdr-bia/`**, porque os caminhos (`prompts/sdr.md`, `dados/...`) são relativos a essa pasta.

## Convenções técnicas

- **Provedor de IA: API do Gemini**, na minha conta pessoal com os créditos do Google AI Pro. Não uso conta da empresa.
- Bibliotecas: `google-genai`, `pydantic`, `python-dotenv`, `httpx`, `pytest`, `chromadb`.
- Chave no `.env` como `GEMINI_API_KEY`. Sempre `load_dotenv()` e `client = genai.Client()`. Nunca escreva a chave no código nem a peça no chat.
- Modelo padrão: `gemini-3.8-flash`. Se der `503 UNAVAILABLE`, use `gemini-3.6-flash` ou configure retry com `types.HttpRetryOptions`. Se o nome do modelo for recusado, consulte https://ai.google.dev/gemini-api/docs/quickstart.
- Conversa: `client.chats.create(model=..., config=types.GenerateContentConfig(system_instruction=..., temperature=...))` e `chat.send_message(...)`.
- Saída estruturada: `response_mime_type="application/json"` + `response_schema=ModeloPydantic`, ler `r.parsed` e validar sempre.
- Tool use: loop manual, com `automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)`, `r.function_calls` e `types.Part.from_function_response(...)`, com limite de passos.
- Regras de negócio e nota do lead em Python puro, testadas com pytest.
- **Só dados fictícios.** Nada de dados reais de clientes ou leads. Pensar em LGPD: coletar só o necessário, a Bia se apresenta como assistente virtual, respeitar opt-out.
- Um commit por exercício ou etapa concluída, com mensagem em português.

## Onde estou

> Atualize esta seção ao fim de cada sessão de estudo.

- **Guia atual:** SDR de IA para espaços flexíveis B2B
- **Módulo atual:** 2, Qualificação (começando)
- **Já feito:** ambiente e exercícios iniciais (`fase1/exercicios`). **Módulo 1 concluído (26/11/2026):** `bia.py` com `criar_chat()`, retry e salvamento de conversas; prompt v3; eval automatizado `evals/testar_prompt.py` (7 cenários, checagens em código, histórico por versão) com placar v2 4/7 → v3 **7/7** (3 repetições).
- **Modelo em uso:** `gemini-3.5-flash-lite`, porque os `flash` maiores estavam dando 503 com frequência. Testar o 3.8-flash de novo quando estabilizar (`--modelo`).
- **Próximo passo:** Módulo 2: `FichaLead` (Pydantic) + extrator com `response_schema`, depois `pontuar`, `faltando` e `proximo_passo` com testes pytest.
- **Pendências:** caso do freelancer (resolver com `proximo_passo` = `fora_do_perfil` no Módulo 2); tornar o repo público (configurar e-mail noreply do GitHub e limpar o histórico antes); README curto de status.
- **Dúvidas em aberto:** —

### Checklist

Preparação
- [x] Ambiente, venv e chave do Gemini
- [x] Primeiros exercícios de Python e pytest
- [ ] Ler "O negócio" e "Como funciona o trabalho de um SDR" no guia
- [ ] Escrever à mão uma conversa ideal SDR x lead (vira exemplo few-shot)

Bia
- [x] Módulo 1: chat da Bia + eval automatizado (7/7) + prompt v3
- [ ] Módulo 2: ficha do lead, extrator, nota, próximo passo + testes pytest
- [ ] Módulo 3: espacos.json, FAQ, ferramentas, RAG e agendamento
- [ ] Módulo 4: resumo de handoff e mensagem para o vendedor
- [ ] Módulo 5: 12 personas, lead simulado, evals e persona maliciosa
- [ ] Etapa 6: FastAPI + widget React + painel de leads + Docker
- [ ] README com GIF, arquitetura, tabela de evals e decisões
- [ ] Vídeo de 1 a 2 minutos da demo para o LinkedIn
