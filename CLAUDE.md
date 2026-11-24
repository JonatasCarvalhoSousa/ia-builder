# CLAUDE.md — IA-builder

Este repositório é o caderno de estudos do Jônatas (Jhow) para vagas de **AI Builder com foco em agentes de vendas**: um **SDR de IA** que conversa com leads, qualifica, agenda reuniões e passa o lead pronto para o vendedor. O case de referência é o mercado de **escritórios flexíveis B2B** (modelo de empresas como a Woba). Leia este arquivo inteiro antes de responder qualquer coisa.

## Quem eu sou

- Analista de QA. Antes disso, trabalhei vários anos como dev front-end React, então JavaScript e TypeScript são familiares. Python ainda é novo para mim.
- Uso **Mac** (zsh, Homebrew, Python 3.13 em `.venv` na raiz `IA-builder/`). Dê comandos e atalhos de macOS.
- Escreva em **português**. Termos técnicos podem ficar em inglês.

## Como quero ser ajudado

Meu objetivo é **aprender**, não só terminar os exercícios.

1. **Passo a passo concreto.** Diga em que pasta estou, qual arquivo criar, o conteúdo completo e o comando para rodar. Instruções vagas me travam.
2. **Explique antes ou junto do código.** O conceito e o porquê, depois o exemplo, com o que cada parte faz.
3. **Não entregue a solução inteira de um exercício** sem eu pedir. Dê dicas em níveis: pista, esqueleto e, se eu pedir, a solução.
4. Quando eu errar, explique a mensagem de erro e o que ela ensina antes de corrigir. Diga se o erro é do meu lado (4xx, código) ou do serviço (5xx).
5. **Compare com JavaScript/React** quando ajudar.
6. **Use meu lado de QA:** para cada parte do agente, sugira testes (pytest para o código, conversas de teste e evals para a IA).
7. Traga a **visão de vendas**: por que aquela pergunta ou regra faz sentido para um SDR e para o vendedor que recebe o lead.
8. No fim de cada sessão, proponha atualizar a seção "Onde estou" abaixo.

## Material de estudo

- **Guia principal (atual):** SDR de IA para espaços flexíveis (case Woba): https://claude.ai/artifact/EY3XEDn6voMtGXg8h1RtKs
- Base técnica (Python, saída estruturada, tool use, RAG; já tem a seção "Usando o Gemini"): https://claude.ai/artifact/XJ4H3dEAtucym5uB87LmES
- Trilha geral de carreira: https://claude.ai/artifact/3WfwbsUKDAufkgZpGYUVYW
- Código de referência: Sellbird (https://github.com/ethanplusai/sellbird), agente de prospecção open-source que meu irmão me passou. Bom para ver prompts (`prompts/`), escrita de e-mail (`agents/writer.py`), tratamento de respostas (`agents/handler.py`), guardas (`gate.py`) e defesa contra prompt injection (`untrusted.py`).

## O projeto: Bia, a SDR de IA da EspaçoFlex

**EspaçoFlex é uma marca fictícia**, com o mesmo modelo de negócio dos escritórios flexíveis B2B: escritórios privativos, estações de trabalho, salas de reunião por hora e espaços para eventos, com contrato único e valor fixo, em várias cidades. Nunca use nome, marca ou dados reais da Woba nem de outra empresa no código, nos prompts ou no README.

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
    ├── evals/            # conversas-modulo1.md, personas.json, rodar.py (Módulo 5)
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

- **Guia atual:** SDR de IA (case Woba)
- **Módulo atual:** 1, Conversa (começando)
- **Já feito antes:** ambiente montado, chave do Gemini funcionando, exercícios iniciais de Python (Pydantic, pytest) em `fase1/exercicios`
- **Próximo passo:** criar `sdr-bia/prompts/sdr.md` e `sdr-bia/bia.py`, rodar a Bia e fazer os 5 testes de conversa (pergunta única, preço, pedir humano, tom informal, lead fora do perfil)
- **Dúvidas em aberto:** —

### Checklist

Preparação
- [x] Ambiente, venv e chave do Gemini
- [x] Primeiros exercícios de Python e pytest
- [ ] Ler "O negócio" e "Como funciona o trabalho de um SDR" no guia
- [ ] Escrever à mão uma conversa ideal SDR x lead (vira exemplo few-shot)

Bia
- [ ] Módulo 1: chat da Bia + 5 testes de conversa + ajustes no prompt
- [ ] Módulo 2: ficha do lead, extrator, nota, próximo passo + testes pytest
- [ ] Módulo 3: espacos.json, FAQ, ferramentas, RAG e agendamento
- [ ] Módulo 4: resumo de handoff e mensagem para o vendedor
- [ ] Módulo 5: 12 personas, lead simulado, evals e persona maliciosa
- [ ] Etapa 6: FastAPI + widget React + painel de leads + Docker
- [ ] README com GIF, arquitetura, tabela de evals e decisões
- [ ] Vídeo de 1 a 2 minutos da demo para o LinkedIn
