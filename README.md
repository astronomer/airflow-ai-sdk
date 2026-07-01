# airflow-ai-sdk

## ⚠️ Discontinuation of project

> This project is no longer actively maintained by Astronomer. Development has been paused and we are
> not accepting new contributions, bug fixes or releases.
>
> **We recommend migrating to [`apache-airflow-providers-common-ai`](https://pypi.org/project/apache-airflow-providers-common-ai/)**, the official Apache Airflow provider for AI and LLM workflows, which is where new development now happens. See the [migration guide](https://www.astronomer.io/blog/migrating-from-airflow-ai-sdk-to-apache-airflow-s-common-ai-provider/) for step-by-step instructions.
>
> The code is still here for you to explore, fork and adapt under the terms of its license. Please note
> that it may not work with the latest dependencies or platforms, and it could contain security
> vulnerabilities. Astronomer can't offer guarantees or warranties for its use.
>
> If you're interested in adopting or stewarding this project, we'd be happy to chat, reach us at
> oss@astronomer.io. Thanks for being part of the open-source journey and helping keep great ideas
> alive!

---

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

> [!TIP]
> You can find further information and a full DAG example for each of these decorators in the [Airflow AI SDK Decorators & Code Snippets](https://www.astronomer.io/ebooks/quick-notes-airflow-ai-sdk-decorators-code-snippets/) quick notes!

## Example

```python
from typing import Literal
import pendulum
from airflow.decorators import dag, task
from airflow.models.dagrun import DagRun


@task.llm(
    model="gpt-4o-mini",
    output_type=Literal["positive", "negative", "neutral"],
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
