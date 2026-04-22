# Demo Auth Page

Static demo page for mocked third-party authentication with fixed user identity.

## Delivery boundary

- Source files live in `demo/auth-page`.
- Runtime delivery (local/demo mode) is handled by API transport routes in `src/core/api/asgi_app.py`.
- Served URLs:
  - `/demo/auth-page`
  - `/demo/auth-page/styles.css`

## Files

- `index.html` — standalone demo auth flow screen.
- `styles.css` — visual style aligned with `spa-app` dark/gold baseline.

## Quick smoke run

Option A:

```bash
open /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/demo/auth-page/index.html
```

Option B:

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/demo/auth-page
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

Option C (recommended, same process as API runtime):

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m core.api.asgi_app
```

Then open `http://127.0.0.1:8000/demo/auth-page`.

## Smoke checklist

1. CTA button is visible and clickable.
2. Loading state appears with "Гав-гав..." message.
3. Success state appears after loading.
4. Demo user identity block is visible (`external_user_id` and `identity_issuer`).
5. Page is reachable from ASGI runtime path `/demo/auth-page`.
