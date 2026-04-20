# API Error Envelope Reference — STORY-M2-01-04

## Success envelope

```json
{
  "data": {
    "status": "ok"
  },
  "trace_id": "trace-123"
}
```

## Error envelope

```json
{
  "error": {
    "code": "INFRASTRUCTURE_ERROR",
    "type": "infrastructure",
    "message": "transport unavailable",
    "details": {}
  },
  "trace_id": "trace-123"
}
```

## Mapping reference
- `ConfigError` -> `VALIDATION_ERROR` / `validation`
- `ValueError` -> `DOMAIN_ERROR` / `domain`
- `ConnectionError` / `TimeoutError` / `OSError` -> `INFRASTRUCTURE_ERROR` / `infrastructure`
- other exceptions -> `INTERNAL_ERROR` / `internal`
