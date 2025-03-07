# examples

This directory contains examples of how to use the Airflow AI SDK. To run Airflow locally, run (from the root of the repo):

```bash
export AIRFLOW_HOME=$(pwd)/examples AIRFLOW__CORE__LOAD_EXAMPLES=false && uv run airflow standalone
```

Each example can also be run with:

```bash
uv run examples/dags/example_dag.py
```
