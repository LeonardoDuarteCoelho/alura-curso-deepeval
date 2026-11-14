# Project: Continuous LLM Evaluation with GitHub Actions, DeepEval, and FastAPI

Welcome to the repository for Alura's [Continuous Integration for LLMs](https://cursos.alura.com.br/course/gitactions-mlflow-deepeval) course. This project explores automated evaluation and CI/CD practices for LLM applications.

## 🚀 About the Project

The project provides a FastAPI chatbot that answers questions using a legal reference text. The chatbot connects to a local LLM through LM Studio's OpenAI-compatible API. The DeepEval test suite evaluates metrics including `Faithfulness`, `AnswerRelevancy`, `Bias`, and `Toxicity`.

## ✨ Technologies

- **Python 3.11**: Project runtime
- **FastAPI**: Chatbot API framework
- **Uvicorn**: ASGI server
- **LM Studio** and **OpenAI SDK**: Local model serving and client integration
- **DeepEval**: LLM evaluation framework
- **Pytest**: Testing framework
- **SQLAlchemy**: SQLite conversation history persistence
- **Docker**: Application containerization
- **GitHub Actions**: CI/CD platform
- **python-dotenv**: Environment variable management

## 📁 Project Structure

```text
.
├── .env                          # Local environment variables (do not commit)
├── .gitignore
├── Dockerfile
├── pytest.ini
├── requirements.txt
├── README.md
├── data/
│   └── context.txt               # Chatbot reference content
├── app/
│   ├── main.py                   # FastAPI entry point
│   ├── chatbot.py                # Chatbot logic and model integration
│   ├── sanitization.py           # Response sanitization
│   ├── schema/
│   │   └── chat.py               # Request schema
│   └── database/
│       ├── crud.py               # Conversation history operations
│       ├── database.py           # SQLAlchemy configuration
│       └── models.py             # Database models
└── tests/
    ├── test_chatbot_flow.py      # DeepEval chatbot tests
    ├── custom_metrics.py         # Custom evaluation metrics
    ├── groq_custom_model.py      # Groq evaluator adapter
    ├── operouter_custom_model.py # OpenRouter evaluator adapter
    └── gemini_custom_model.py    # Gemini evaluator adapter
```

## ⚙️ Local Environment Setup

1. **Obtain the project** and open a terminal in its root directory.

2. **Create a virtual environment** with Python 3.11:
   ```powershell
   py -3.11 -m venv .venv
   ```

3. **Install dependencies:**
   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. **Start LM Studio:** Download and load a model, then start the server on the **Developer** tab. List the available model identifiers:
   ```powershell
   Invoke-RestMethod http://localhost:1234/v1/models
   ```

5. **Configure `.env`:** Create it in the project root, using an identifier returned by LM Studio:
   ```env
   LM_STUDIO_BASE_URL=http://localhost:1234/v1
   LM_STUDIO_API_KEY=lm-studio
   LM_STUDIO_MODEL=gemma-4-e4b-it
   ```
   LM Studio does not require authentication by default, so `lm-studio` can be used as a placeholder. If authentication is enabled, use your LM Studio token instead. Do not commit `.env`.

## ▶️ Running the Project Locally

1. **Start the FastAPI application** from the project root:
   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```
   Open the interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs). For `POST /chat/`, provide a `session-id` header and a question. Omit `model` or set it to `null` to use `LM_STUDIO_MODEL`. An explicit model must be available in LM Studio. Conversation history is stored in `chat_history.db` by session ID.

2. **Alternatively, build and run the API with Docker Desktop:**
   ```powershell
   docker build -t chatbot-api .
   docker run --env-file .env -e LM_STUDIO_BASE_URL=http://host.docker.internal:1234/v1 -p 8000:8000 chatbot-api
   ```
   The container needs access to the LM Studio server on the host; `localhost` inside the container refers to the container itself.

3. **Run the DeepEval tests** after configuring their evaluators and starting the API:
   ```powershell
   .\.venv\Scripts\python.exe -m deepeval test run tests/test_chatbot_flow.py -vv
   ```
   The current test file instantiates Groq and Gemini evaluators and requires `GROQ_API_KEY` and `GOOGLE_API_KEY`. It also sends a Groq model name to the chatbot; change that value to an LM Studio model identifier. `CONFIDENT_API_KEY` is optional for uploading results. To run entirely locally, the evaluator also needs a local model adapter.

## 🤖 CI/CD with GitHub Actions

This checkout does not currently contain a GitHub Actions workflow. A workflow can build the Docker image, start the API, and run the DeepEval suite after its models and credentials are configured. GitHub-hosted runners cannot automatically access an LM Studio server on your computer; use a runner with access to a model server or another inference setup.

## 📚 References

- [LM Studio: local server](https://lmstudio.ai/docs/developer/core/server)
- [LM Studio: OpenAI compatibility](https://lmstudio.ai/docs/developer/openai-compat)
- [FastAPI](https://fastapi.tiangolo.com/)
- [DeepEval](https://deepeval.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
