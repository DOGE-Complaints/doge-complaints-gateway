# Acceptance verification — task-m2-16-02-t03-single-command-launch

## AC checklist
- [x] GAP-SIM-03 закрыт: one-command launch работает и документирован.

## Verification commands
```bash
cd doge-complaints-gateway && make -n simulate
```

## Verification performed
- Added `Makefile` with `simulate` target.
- Dry-run confirms launch command `python3 tests/simulation_runner.py`.
