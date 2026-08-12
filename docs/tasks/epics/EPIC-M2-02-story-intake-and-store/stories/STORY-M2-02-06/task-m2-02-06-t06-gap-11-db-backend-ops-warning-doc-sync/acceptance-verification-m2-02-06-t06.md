# Верификация приёмки — TASK-M2-02-06-T06

| AC | Уровень | Формулировка | Код / тесты | Статус |
|----|---------|--------------|-------------|--------|
| §16 | P0 | Текст верификации = факт кода | analysis doc §16 | OK |
| Ops signal | P1 | WARNING при in_memory | `src/core/api/asgi_app.py` | OK |
| Регресс дефолта | P1 | Зафиксировано тестом | `tests/test_config_loading.py::test_db_backend_env_default_matches_schema` | OK |

Отдельный unit только на текст WARNING не требовался (см. README таска).
