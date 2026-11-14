# Avaliação contínua de LLMs com DeepEval e FastAPI

Projeto do curso [Integração contínua para LLMs](https://cursos.alura.com.br/course/gitactions-mlflow-deepeval). A API implementa um chatbot jurídico que responde com base no conteúdo de `data/context.txt` e mantém o histórico das conversas em SQLite. O chatbot usa um modelo local disponibilizado pelo LM Studio por meio da API compatível com OpenAI.

## Estrutura

- `app/main.py`: API FastAPI e endpoint `/chat/`.
- `app/chatbot.py`: instruções do chatbot e conexão com o modelo.
- `app/schema/` e `app/database/`: formato das requisições e persistência do histórico.
- `data/context.txt`: conteúdo de referência para as respostas.
- `tests/`: testes de avaliação DeepEval e adaptadores de modelos.
- `Dockerfile` e `requirements.txt`: imagem da aplicação e dependências Python.

## Configuração no Windows

1. Instale Python 3.11 e crie o ambiente virtual na raiz do projeto:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

2. No LM Studio, baixe e carregue um modelo e inicie o servidor na aba **Developer**. Confira os identificadores disponíveis:

   ```powershell
   Invoke-RestMethod http://localhost:1234/v1/models
   ```

3. Crie um arquivo `.env` na raiz, usando o identificador do modelo retornado pelo servidor:

   ```env
   LM_STUDIO_BASE_URL=http://localhost:1234/v1
   LM_STUDIO_API_KEY=lm-studio
   LM_STUDIO_MODEL=gemma-4-e4b-it
   ```

   O LM Studio não exige autenticação por padrão; `lm-studio` é um valor para o cliente OpenAI. Se você habilitar autenticação no servidor, use seu token em `LM_STUDIO_API_KEY`. Não versione o `.env`.

4. Inicie a API a partir da raiz do projeto:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```

   Acesse [http://localhost:8000/docs](http://localhost:8000/docs). No endpoint `POST /chat/`, informe um `session-id` e uma pergunta. Omita `model` ou informe `null` para usar `LM_STUDIO_MODEL`; se informar um modelo, ele deverá estar disponível no LM Studio. O histórico é associado ao `session-id` e armazenado em `chat_history.db`.

## Docker

O endereço `localhost` dentro do contêiner se refere ao próprio contêiner. No Docker Desktop, configure `LM_STUDIO_BASE_URL=http://host.docker.internal:1234/v1` no ambiente do contêiner e confira se o servidor LM Studio aceita conexões do contêiner.

```powershell
docker build -t chatbot-api .
docker run --env-file .env -e LM_STUDIO_BASE_URL=http://host.docker.internal:1234/v1 -p 8000:8000 chatbot-api
```

## Avaliação com DeepEval

Os testes em `tests/test_chatbot_flow.py` ainda usam modelos Groq e Gemini como avaliadores, instanciados durante a importação, e enviam um nome de modelo Groq ao chatbot. Para executá-los como estão, são necessárias `GROQ_API_KEY` e `GOOGLE_API_KEY`, além de adaptar o modelo enviado à API para um identificador disponível no LM Studio. `CONFIDENT_API_KEY` é opcional para envio de resultados ao Confident AI.

Para usar somente modelos locais, é necessário adaptar também o avaliador DeepEval e o modelo enviado pelo teste; a configuração do chatbot não altera automaticamente essas partes. Com a API em execução e os testes configurados, execute:

```powershell
.\.venv\Scripts\python.exe -m deepeval test run tests/test_chatbot_flow.py -vv
```

Um runner hospedado no GitHub não acessa automaticamente o LM Studio do computador local; a integração contínua precisa de um runner com acesso a um servidor de modelos ou de outra infraestrutura de inferência.

## Referências

- [LM Studio: servidor local](https://lmstudio.ai/docs/developer/core/server)
- [LM Studio: compatibilidade com OpenAI](https://lmstudio.ai/docs/developer/openai-compat)
- [FastAPI](https://fastapi.tiangolo.com/)
- [DeepEval](https://deepeval.com/)
