docker_compose('examples/docker-compose.yaml')

sync_pyproj_toml = sync('./pyproject.toml', '/usr/local/airflow/airflow-ai-sdk/pyproject.toml')
sync_readme = sync('./README.md', '/usr/local/airflow/airflow_ai_sdk/README.md')
sync_src = sync('./airflow_ai_sdk', '/usr/local/airflow/airflow_ai_sdk/airflow_ai_sdk')

docker_build(
    'airflow-ai-sdk',
    context='.',
    dockerfile='examples/Dockerfile',
    ignore=['.venv', '**/logs/**'],
    live_update=[
        sync_pyproj_toml,
        sync_src,
        sync_readme,
        run(
            'cd /usr/local/airflow/airflow_ai_sdk && uv pip install -e .',
            trigger=['pyproject.toml']
        ),
    ]
)