# Acceptance verification — T06 (GAP-33-01)

| AC | Код / тест | Статус |
|----|------------|--------|
| `columns_v2` в Supabase db_checks | `dependencies.py` L69 | pass |
| `db_ready` учитывает v2 columns | `all(db_checks.values())` | pass |
| `/ready` shape с `columns_v2` | `test_supabase_ready_endpoint_shape.py` | pass |

Команды:
```bash
cd doge-complaints-gateway && python3 -m pytest tests/integration/supabase/test_supabase_ready_endpoint_shape.py -q
```
