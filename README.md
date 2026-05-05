# Promotions Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![CI Build](https://github.com/CSCI-GA-2820-SP26-001/promotions/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP26-001/promotions/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP26-001/promotions/branch/master/graph/badge.svg)](https://codecov.io/gh/CSCI-GA-2820-SP26-001/promotions)

## Overview

The Promotions service is a RESTful microservice built with Flask that manages promotional offers. It is deployed to OpenShift using a Tekton CD pipeline that automatically validates, builds, and deploys the service on every push to master.

## Contents

```text
service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes

features/                  - BDD test suite
├── environment.py         - Flask app context setup
├── promotions.feature     - Gherkin scenarios for all flows
└── steps/
    └── steps.py           - Step definitions

.tekton/                   - Tekton CD pipeline manifests
├── pipeline.yaml          - Full CD pipeline definition
├── workspace.yaml         - Shared PersistentVolumeClaim
├── tasks/
│   ├── clone.yaml         - Clones the repository
│   ├── lint.yaml          - Runs flake8 and pylint
│   ├── unittest.yaml      - Runs pytest with coverage
│   ├── build.yaml         - Builds and pushes container image
│   └── bdd.yaml           - Runs Behave BDD tests
└── triggers/
    ├── event-listener.yaml    - Listens for GitHub push events
    ├── trigger-binding.yaml   - Extracts values from the GitHub payload
    └── trigger-template.yaml  - Creates a PipelineRun on trigger

k8s/                       - Kubernetes/OpenShift manifests
├── deployment.yaml        - App deployment configuration
├── postgresql.yaml        - PostgreSQL deployment
├── service.yaml           - Kubernetes service
└── route.yaml             - OpenShift route
```

## Sprint 4 — CD Pipeline (Tekton + OpenShift)

### Pipeline Overview

The Sprint 4 CD pipeline is defined in `.tekton/pipeline.yaml` and runs the following tasks in order:

Each stage must pass before the next one begins. If any stage fails, the pipeline stops and the deployment does not proceed.

### Pipeline Tasks

| Task | File | Description |
|------|------|-------------|
| clone | `tasks/clone.yaml` | Clones the master branch into the shared workspace using `alpine/git` |
| lint | `tasks/lint.yaml` | Runs `flake8` and `pylint` against `service/` and `tests/` |
| unit-test | `tasks/unittest.yaml` | Runs `pytest` with a minimum 95% coverage requirement |
| build | `tasks/build.yaml` | Builds the container image using `buildah` and pushes to the OpenShift registry |
| bdd-tests | `tasks/bdd.yaml` | Runs `behave` BDD tests against the live OpenShift route using `BASE_URL` |

### Shared Workspace

All tasks share a `PersistentVolumeClaim` defined in `workspace.yaml` named `pipeline-workspace` (1Gi, ReadWriteOnce). This allows the cloned source code to be passed between tasks without re-cloning.

### Triggers

The pipeline is triggered automatically on every push to master via a GitHub webhook. The trigger setup consists of three resources:

- **EventListener** (`triggers/event-listener.yaml`) — exposes a route that receives GitHub push events
- **TriggerBinding** (`triggers/trigger-binding.yaml`) — extracts the repo URL and branch from the GitHub payload
- **TriggerTemplate** (`triggers/trigger-template.yaml`) — creates a new `PipelineRun` with the extracted values

### OpenShift Deployment Flow

1. PostgreSQL is deployed to OpenShift using `k8s/postgresql.yaml`
2. The Promotions service is deployed using `k8s/deployment.yaml`
3. A Kubernetes service is created via `k8s/service.yaml`
4. An OpenShift route is exposed via `k8s/route.yaml`
5. The pipeline verifies the deployment by running BDD tests against the live route URL

### OpenShift Route

The live route URL for the Promotions service is documented in the final submission checklist. The `/health` endpoint should return:

```json
{"status": "OK"}
```

## Running Tests Locally

**Unit tests:**
```bash
pytest --pspec --cov=service --cov-fail-under=95
```

**BDD tests:**
```bash
BASE_URL=http://localhost:8080 python -m behave
```

**Lint:**
```bash
flake8 service tests --count --max-complexity=10 --max-line-length=127 --statistics
pylint service tests --max-line-length=127
```

## License

Copyright (c) 2016, 2025 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.