# Examples

The airflow-ai-sdk comes with several example DAGs that demonstrate how to use the various decorators and features. All examples can be found in the [`examples/dags`](https://github.com/astronomer/airflow-ai-sdk/tree/main/examples/dags) directory of the repository.

## Available Examples

### 1. LLM Calls - GitHub Changelog

[View example code](https://github.com/astronomer/airflow-ai-sdk/blob/main/examples/dags/github_changelog.py)

Demonstrates using `@task.llm` to summarize GitHub commits with a language model.

**Features demonstrated:**
- Using `@task.llm` decorator with a specific model (gpt-4o-mini)
- Specifying a detailed system prompt for commit summarization
- Transforming task input to LLM input (joining commits into a string)
- Weekly scheduling for regular changelog generation

### 2. Structured Output - Product Feedback

[View example code](https://github.com/astronomer/airflow-ai-sdk/blob/main/examples/dags/product_feedback_summarization.py)

Shows how to use `@task.llm` with Pydantic models to parse structured data from product feedback.

**Features demonstrated:**
- Creating a custom Pydantic model for structured LLM output
- PII masking in preprocessing
- Using `result_type` parameter with a Pydantic model
- Task mapping with `expand()` to process multiple feedback items
- Conditional execution with `AirflowSkipException`

### 3. Agent Tasks - Deep Research

[View example code](https://github.com/astronomer/airflow-ai-sdk/blob/main/examples/dags/deep_research.py)

Illustrates how to use `@task.agent` with custom tools to perform deep research on topics.

**Features demonstrated:**
- Creating a custom agent with tools
- Using the `@task.agent` decorator
- Creating custom tools (web content fetching)
- Integrating with external APIs (DuckDuckGo search)
- Using runtime parameters for dynamic DAG execution

### 4. Branching Tasks - Support Ticket Routing

[View example code](https://github.com/astronomer/airflow-ai-sdk/blob/main/examples/dags/support_ticket_routing.py)

Demonstrates how to use `@task.llm_branch` to route support tickets based on priority.

**Features demonstrated:**
- Using `@task.llm_branch` for conditional workflow routing
- Setting up branch tasks based on LLM decisions
- Configuring `allow_multiple_branches` parameter
- Processing DAG run configuration parameters
- Detailed prompt engineering for classification tasks

### 5. Embedding Tasks - Text Embedding

[View example code](https://github.com/astronomer/airflow-ai-sdk/blob/main/examples/dags/text_embedding.py)

Shows how to use `@task.embed` to create vector embeddings from text.

**Features demonstrated:**
- Using `@task.embed` decorator
- Specifying embedding model parameters
- Generating vector embeddings from text
- Configuring encoding parameters (normalization)
- Task mapping to process multiple texts in parallel

## Running the Examples

The examples can be run in a local Airflow environment with the following steps:

1. Clone the [examples repository](https://github.com/astronomer/ai-sdk-examples):
   ```bash
   git clone https://github.com/astronomer/ai-sdk-examples.git
   ```

2. Navigate to the examples directory:
   ```bash
   cd ai-sdk-examples
   ```

3. Start the Airflow environment:
   ```bash
   astro dev start
   ```

For more information on the individual examples, refer to the code comments in each example file.
