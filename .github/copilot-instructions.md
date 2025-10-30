## Copilot instructions for Airflow_Practice

Purpose
- Provide concise, actionable guidance so an AI coding agent can be productive in this repository.

Repository snapshot
- Current repo root contains `README.md` only (title: "Airflow_Practice"). No existing AI agent docs were found.

What to look for first
- Check these paths (common in Airflow projects): `dags/`, `plugins/`, `tests/`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `airflow.cfg`, and `scripts/`.
- If you find DAG modules, prefer reading a DAG file top-to-bottom to learn naming conventions and connection IDs.

Big-picture guidance
- This appears to be an Airflow practice repo. Since only `README.md` is present, assume this repo may contain DAGs and related infra in the paths above. If DAGs exist, there will typically be:
  - DAG definitions under `dags/` (one DAG per file is common). Use the DAG `dag_id` and task ids as ground-truth for naming.
  - Dependencies listed in `requirements.txt` or a `constraints.txt`.

Developer workflows (if present)
- If you find a `docker-compose.yml`, prefer using it to start a local Airflow stack for integration checks.
- When no scripts are present, ask the repo owner how they normally run Airflow locally (Common commands: `airflow db init`, `airflow scheduler`, `airflow webserver`, or `docker-compose up` when a compose file exists).

Patterns and conventions to preserve
- Preserve inferred naming from existing DAG files. Do not rename `dag_id`s, connection IDs, variable keys, or S3/GCS bucket names you find—these are integration touchpoints.
- If you add tests, follow any existing tests' structure (filename/location and test runner). If no tests exist, propose a `tests/` layout but do not add it without confirmation.

Integration points
- Search for usage of external connection IDs (strings like `aws_default`, `google_cloud_default`, `my_conn_id`) and treat them as secrets/config: do not hardcode credentials.

When editing or adding files
- Small, focused commits. Use descriptive commit messages: e.g., `docs: add copilot instructions` or `dags: add example DAG for X`.
- If creating a DAG, include minimal unit tests for individual Python functions (not scheduler integration tests) and document how to run them.

If information is missing
- Stop and request these items from the maintainer: sample DAG(s), `requirements.txt`, `docker-compose.yml` (or Dockerfile), and any preferred local run commands.

Examples to cite (from repository)
- `README.md` exists but contains only the repo title. Use it as the starting point when asking the maintainer for missing files.

Questions to ask the maintainer
- How do you run Airflow locally? (native `airflow` commands, `docker-compose`, or a Kubernetes setup)
- Where do you store connection credentials and environment configuration?

Next steps for the agent
1. If new files are added (DAGs, requirements, compose), re-run this analysis and update these instructions with concrete commands and examples from those files.
2. Ask the repo owner for missing artifacts if any critical integration or run instructions are required to complete a task.

— End of instructions —