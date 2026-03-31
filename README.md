# BlogAgentic

An AI-powered blog generation agent built with **LangGraph** and **FastAPI** that automates the creation of blog posts — including multilingual translation into Urdu and Punjabi.

---

## What It Does

BlogAgentic exposes a REST API endpoint that accepts a topic and generates a complete blog post (title + content) using a multi-step AI workflow. It supports two modes:

- **Topic Mode** — provide a topic, get a full SEO-friendly blog post
- **Language Mode** — provide a topic and a language (Urdu or Punjabi), get a translated blog post with culturally adapted content

---

## How It Works

The project uses **LangGraph** to orchestrate a stateful multi-node workflow:

**Topic Graph:**
```
START → title_creation → content_generation → END
```

**Language Graph:**
```
START → title_creation → content_generation → route → [urdu_translation / punjabi_translation] → END
```

Each node in the graph receives the current state, performs its task using the Groq LLM, and passes updated state to the next node.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM Provider | [Groq API](https://groq.com) — Qwen 3-32B model |
| Workflow Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM Framework | [LangChain](https://github.com/langchain-ai/langchain) |
| API Server | [FastAPI](https://fastapi.tiangolo.com) + Uvicorn |
| Monitoring | [LangSmith](https://smith.langchain.com) |

---

## Project Structure

```
BlogAgentic/
├── app.py                  # FastAPI app and /blogs endpoint
├── main.py                 # Entry point placeholder
├── requirements.txt        # Python dependencies
├── requtes.json            # Sample API request payloads
└── src/
    ├── graphs/
    │   └── graph_builder.py    # LangGraph workflow builder
    ├── states/
    │   └── blog_state.py       # State schema (TypedDict + Pydantic)
    ├── nodes/
    │   └── blog_node.py        # Node logic (title, content, translation, routing)
    └── llms/
        └── groqllm.py          # Groq LLM wrapper
```

---

## API Usage

**Endpoint:** `POST /blogs`

### Generate a blog on a topic
```json
{
  "topic": "Agentic AI"
}
```

### Generate a blog translated to Urdu
```json
{
  "topic": "Agentic AI",
  "language": "Urdu"
}
```

### Generate a blog translated to Punjabi
```json
{
  "topic": "Agentic AI",
  "language": "Punjabi"
}
```

### Response
```json
{
  "topic": "Agentic AI",
  "blog": {
    "title": "...",
    "content": "..."
  },
  "current_language": "urdu"
}
```

---

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables** — create a `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key
   LANGSMITH_API_KEY=your_langsmith_api_key
   ```

3. **Run the server**
   ```bash
   uvicorn app:app --reload
   ```

4. **Send a request**
   ```bash
   curl -X POST http://localhost:8000/blogs \
     -H "Content-Type: application/json" \
     -d '{"topic": "Agentic AI"}'
   ```

---

## Supported Languages

- English (default)
- Urdu
- Punjabi
