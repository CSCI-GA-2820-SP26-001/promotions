# Sprint 4 — Final Submission Checklist

## Story #52 — Final Submission Checklist and Route Documentation

### OpenShift Route URL

https://promotions-bs3581-dev.apps.rm1.0a51.p1.openshiftapps.com

### Checklist

| Item | Status | Notes |
|------|--------|-------|
| OpenShift route created | ✅ Complete | Route applied via `k8s/route.yaml` |
| `/health` endpoint returns `{"status": "OK"}` | ⏳ Pending | Blocked on PostgreSQL pod fix |
| Admin UI reachable from route | ⏳ Pending | Blocked on PostgreSQL pod fix |
| Tekton pipeline applied to cluster | ✅ Complete | Applied via `oc apply -f .tekton/` |
| Clone task | ✅ Complete | `tasks/clone.yaml` |
| Lint task | ✅ Complete | `tasks/lint.yaml` |
| Unit test task | ✅ Complete | `tasks/unittest.yaml` |
| Build task | ✅ Complete | `tasks/build.yaml` |
| BDD task | ✅ Complete | `tasks/bdd.yaml` |
| Container image built and pushed | ✅ Complete | Pushed to OpenShift registry |
| PostgreSQL deployed | ⏳ Pending | CrashLoopBackOff — PGDATA fix in progress |
| Promotions service deployed | ⏳ Pending | Waiting on PostgreSQL fix |
| BDD tests passing against live route | ⏳ Pending | Waiting on live deployment |
| README updated with pipeline docs | ✅ Complete | PR #69 open, pending merge |

### Verification Steps

Once the deployment is live, verify the following:

**Health Check:**
```bash
curl https://promotions-bs3581-dev.apps.rm1.0a51.p1.openshiftapps.com/health
# Expected: {"status": "OK"}
```

**BDD Tests:**
```bash
BASE_URL=https://promotions-bs3581-dev.apps.rm1.0a51.p1.openshiftapps.com python -m behave
# Expected: 13 scenarios passed
```

### Pipeline Evidence
- Pipeline applied to OpenShift cluster: `bs3581-dev`
- Server: `https://api.rm1.0a51.p1.openshiftapps.com:6443`
- Tekton tasks applied: clone, lint, unit-test, build, bdd-tests
- PVC created: `pipeline-workspace` (1Gi)
- EventListener created: `cd-listener`