FROM quay.io/astronomer/astro-runtime:12.7.1-base

USER root

RUN pip install -U uv

COPY ./examples/requirements.txt ${AIRFLOW_HOME}/requirements.txt
COPY ./pyproject.toml ${AIRFLOW_HOME}/airflow_ai_sdk/pyproject.toml
COPY ./README.md ${AIRFLOW_HOME}/airflow_ai_sdk/README.md
COPY ./uv.lock ${AIRFLOW_HOME}/airflow_ai_sdk/uv.lock
COPY ./airflow_ai_sdk ${AIRFLOW_HOME}/airflow_ai_sdk/airflow_ai_sdk

# install the package in editable mode
RUN uv pip install --system -e "${AIRFLOW_HOME}/airflow_ai_sdk[openai,duckduckgo]"

# install the requirements
RUN uv pip install --system -r "${AIRFLOW_HOME}/requirements.txt"

# make sure astro user owns the package
RUN chown -R astro:astro ${AIRFLOW_HOME}/airflow_ai_sdk

USER astro