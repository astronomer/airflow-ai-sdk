# Features

## Core Features

- **LLM tasks with `@task.llm`:** Define tasks that call language models (e.g. GPT-3.5-turbo) to process text.
- **Agent tasks with `@task.agent`:** Orchestrate multi-step AI reasoning by leveraging custom tools.
- **Automatic output parsing:** Use function type hints (including Pydantic models) to automatically parse and validate LLM outputs.
- **Branching with `@task.llm_branch`:** Change the control flow of a DAG based on the output of an LLM.
- **Model support:** Support for [all models in the Pydantic AI library](https://ai.pydantic.dev/models/) (OpenAI, Anthropic, Gemini, Ollama, Groq, Mistral, Cohere, Bedrock)
- **Embedding tasks with `@task.embed`:** Create vector embeddings from text using sentence-transformers models.

## Why Use Airflow for AI Workflows?

Airflow provides several advantages for orchestrating AI workflows:

- **Flexible scheduling:** run tasks on a fixed schedule, on-demand, or based on external events
- **Dynamic task mapping:** easily process multiple inputs in parallel with full error handling and observability
- **Branching and conditional logic:** change the control flow of a DAG based on the output of certain tasks
- **Error handling:** built-in support for retries, exponential backoff, and timeouts
- **Resource management:** limit the concurrency of tasks with Airflow Pools
- **Monitoring:** detailed logs and monitoring capabilities
- **Scalability:** designed for production workflows

## Task Decorators

### @task.llm

The `@task.llm` decorator enables calling language models from your Airflow tasks. It supports:

- Configurable models from various providers
- System and user prompts
- Structured output parsing with Pydantic models
- Type validation

### @task.agent

The `@task.agent` decorator adds agent capabilities to your Airflow tasks, enabling:

- Multi-step reasoning
- Tool usage for external operations
- Memory and context management
- Complex problem-solving workflows

### @task.llm_branch

The `@task.llm_branch` decorator adds LLM-based decision making to your DAG control flow:

- Routes execution based on LLM output
- Ensures output matches a downstream task ID
- Supports both single and multiple branch selection

### @task.embed

The `@task.embed` decorator creates vector embeddings from text:

- Uses sentence-transformers models
- Creates embeddings usable for semantic search, clustering, etc.
- Configurable model selection
- Optional normalization and other encoding parameters
