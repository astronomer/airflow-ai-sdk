# airflow-ai-sdk

## ⚠️ Discontinuation of project

> This project is no longer actively maintained by Astronomer. Development has been paused and we are
> not accepting new contributions, bug fixes or releases.
>
> **We recommend migrating to [`apache-airflow-providers-common-ai`](https://pypi.org/project/apache-airflow-providers-common-ai/)**, the official Apache Airflow provider for AI and LLM workflows. See the [migration guide](https://www.astronomer.io/blog/migrating-from-airflow-ai-sdk-to-apache-airflow-s-common-ai-provider/) for step-by-step instructions.
>
> If you're interested in adopting or stewarding this project, reach us at oss@astronomer.io.

---

This SDK allows you to work with LLMs from Apache Airflow, based on [Pydantic AI](https://ai.pydantic.dev). It enables calling LLMs and orchestrating agent calls directly within Airflow pipelines using decorator-based tasks.

## Quick Start

To install the package with optional dependencies:

```bash
pip install airflow-ai-sdk[openai,duckduckgo]
```

Note that installing the package with no optional dependencies will install the slim version, which does not include any LLM models or tools. The available optional packages are listed in the [pyproject.toml](https://github.com/astronomer/airflow-ai-sdk/blob/main/pyproject.toml#L17).

## Examples Repository

Check out the [examples repository](https://github.com/astronomer/ai-sdk-examples), which offers a full local Airflow instance with the AI SDK installed and 5 example pipelines:

```bash
git clone https://github.com/astronomer/ai-sdk-examples.git
cd ai-sdk-examples
astro dev start
```

If you don't have the Astro CLI installed, run `brew install astro` (or see other options [here](https://www.astronomer.io/docs/astro/cli/install-cli)).

## Design Principles

We follow the taskflow pattern of Airflow with four decorators:

- `@task.llm`: Define a task that calls an LLM. Under the hood, this creates a Pydantic AI `Agent` with no tools.
- `@task.agent`: Define a task that calls an agent. You can pass in a Pydantic AI `Agent` directly.
- `@task.llm_branch`: Define a task that branches the control flow of a DAG based on the output of an LLM. Enforces that the LLM output is one of the downstream task_ids.
- `@task.embed`: Define a task that embeds text using a sentence-transformers model.

The function supplied to each decorator is a translation function that converts the Airflow task's input into the LLM's input. If you don't want to do any translation, you can just return the input unchanged.

## Documentation

- [Features](features.md) - Overview of available features
- [Usage](usage.md) - Basic usage guide
- [Examples](examples/) - Detailed examples
- [API Reference](api-reference/) - API documentation

## Motivation

AI workflows are becoming increasingly common as organizations look for pragmatic ways to get value out of LLMs. Airflow is a powerful tool for managing the dependencies between tasks and for scheduling and monitoring them, and has been trusted by data teams for 10+ years.

This SDK is designed to make it easy to integrate LLM workflows into your Airflow pipelines, from simple LLM calls to complex agentic workflows.
