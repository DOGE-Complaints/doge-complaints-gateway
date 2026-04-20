# 11. Cross-cutting: Security, Config, Observability

## Security baseline (demo-safe)
- service-role never exposed to public route path;
- auth middleware chain at API boundary;
- strict input validation and output shaping;
- secret redaction in logs;
- no debug mode in runtime.

## Config governance
- centralized config module (env schema + defaults);
- explicit env contract for demo/pilot profiles;
- feature flags for pilot adapters (wallet, blockchain, tokenization).

## Observability
- structured logging with `trace_id`;
- health endpoints (`/health`, `/health/detailed`);
- metrics:
  - intake throughput
  - clustering latency
  - issue promotion success rate
  - projection contract violations

## Failure strategy
- fail-closed for unsafe operations;
- fail-soft for optional enrichments;
- retry with backoff for external adapters;
- dead-letter pattern reserved for pilot async jobs.
