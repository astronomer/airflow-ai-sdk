# airflow-ai-sdk

A Python SDK for working with LLMs from [Apache Airflow](https://github.com/apache/airflow). It allows users to call LLMs and orchestrate agent calls directly within their Airflow pipelines using decorator-based tasks.

We find it's often helpful to rely on mature orchestration tooling like Airflow for instrumenting LLM workflows and agents in production, as these LLM workflows follow the same form factor as more traditional workflows like ETL pipelines, operational processes, and ML workflows.

## Quick Start

```bash
pip install airflow-ai-sdk[openai]
```

Installing with no optional dependencies will give you the slim version of the package. The available optional dependencies are listed in [pyproject.toml](https://github.com/astronomer/airflow-ai-sdk/blob/main/pyproject.toml#L17).

## Features

- **LLM tasks with `@task.llm`:** Define tasks that call language models to process text
- **Agent tasks with `@task.agent`:** Orchestrate multi-step AI reasoning with custom tools
- **Automatic output parsing:** Use type hints to automatically parse and validate LLM outputs
- **Branching with `@task.llm_branch`:** Change DAG control flow based on LLM output
- **Model support:** All models in the Pydantic AI library (OpenAI, Anthropic, Gemini, etc.)
- **Embedding tasks with `@task.embed`:** Create vector embeddings from text

## Example

```python
from typing import Literal
import pendulum
from airflow.decorators import dag, task
from airflow.models.dagrun import DagRun


@task.llm(
    model="gpt-4o-mini",
    result_type=Literal["positive", "negative", "neutral"],
    system_prompt="Classify the sentiment of the given text.",
)
def process_with_llm(dag_run: DagRun) -> str:
    input_text = dag_run.conf.get("input_text")

    # can do pre-processing here (e.g. PII redaction)
    return input_text


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1),
    catchup=False,
    params={"input_text": "I'm very happy with the product."},
)
def sentiment_classification():
    process_with_llm()


sentiment_classification()
```

## Examples Repository

To get started with a complete example environment, check out the [examples repository](https://github.com/astronomer/ai-sdk-examples), which offers a full local Airflow instance with the AI SDK installed and 5 example pipelines:

```bash
git clone https://github.com/astronomer/ai-sdk-examples.git
cd ai-sdk-examples
astro dev start
```

If you don't have the Astro CLI installed, run `brew install astro` or see other options [here](https://www.astronomer.io/docs/astro/cli/install-cli).

## Documentation

For detailed documentation, see the [docs directory](docs/):

- [Getting Started](docs/index.md)
- [Features](docs/features.md)
- [Usage Guide](docs/usage.md)
- [Examples](docs/examples/index.md)

## License

[LICENSE](LICENSE)
