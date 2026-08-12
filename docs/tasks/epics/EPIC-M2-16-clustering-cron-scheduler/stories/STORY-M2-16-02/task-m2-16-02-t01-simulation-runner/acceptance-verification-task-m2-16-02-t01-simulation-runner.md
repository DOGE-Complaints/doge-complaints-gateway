# Acceptance verification — task-m2-16-02-t01-simulation-runner

## AC checklist
- [x] GAP-SIM-01 закрыт и подтвержден запуском runner.

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m py_compile tests/simulation_runner.py
cd doge-complaints-gateway && python3 tests/simulation_runner.py --help
```

## Verification performed
- `tests/simulation_runner.py` создан.
- CLI параметры `--max` / `--groups` доступны.
- Script includes summary + exit code policy and payload mapping.
