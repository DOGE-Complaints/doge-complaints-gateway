# Acceptance verification — task-m2-16-02-t02-env-test-template

## AC checklist
- [x] GAP-SIM-02 закрыт и шаблон .env.test.example валиден по required vars.

## Verification commands
```bash
cd doge-complaints-gateway && rg -n "GATEWAY_URL|GATEWAY_API_TOKEN|SIMULATION_CANVAS_PATH|SIMULATION_GROUPS|SIMULATION_MAX_STORIES" .env.test.example
```

## Verification performed
- Added `.env.test.example` with required variables and usage comments.
- Added `.env.test` ignore rule to `.gitignore`.
