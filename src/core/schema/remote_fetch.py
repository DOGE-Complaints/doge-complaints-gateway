"""Federation remote pack fetch (SSR-35 / REQ4 §5.3 consume).

Stub manifest format (minimal until federation registry SSOT):

    GET {SCHEMA_ROOT_URL}/{schema_id}/{schema_version}/manifest.json

    {
      "schema_id": "<must match active NODE_SCHEMA_ID>",
      "schema_version": "<must match NODE_SCHEMA_VERSION>",
      "files": {
        "pack.json": "https://…/pack.json",
        "payload.schema.json": "https://…/payload.schema.json"
      }
    }

``SCHEMA_ROOT_URL`` is an http(s) registry root — **never** a Volume/filesystem mount
(use ``SCHEMA_PACKS_ROOT`` for disk). Files land under packs root as nested
``<id>/<ver>/``. Fresh cache (``pack.json`` present) skips fetch unless
``SCHEMA_PACK_REFRESH`` is true. Failures raise ``ConfigError`` — no foreign
default pack (e.g. tallinn).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import httpx

from core.config.schema import ConfigError

_MANIFEST_NAME = "manifest.json"
_PACK_NAME = "pack.json"


def pack_cache_fresh(packs_root: Path, schema_id: str, schema_version: str) -> bool:
    """True when nested ``pack.json`` already exists (skip fetch unless refresh)."""
    return (packs_root / schema_id / schema_version / _PACK_NAME).is_file()


def manifest_url(schema_root_url: str, schema_id: str, schema_version: str) -> str:
    root = schema_root_url.rstrip("/")
    return f"{root}/{schema_id}/{schema_version}/{_MANIFEST_NAME}"


def _validate_manifest(
    raw: Any, *, schema_id: str, schema_version: str
) -> dict[str, str]:
    if not isinstance(raw, dict):
        raise ConfigError(
            "SCHEMA_ROOT_URL stub manifest must be a JSON object "
            f"(schema_id={schema_id!r}/{schema_version!r})."
        )
    mid = raw.get("schema_id")
    mver = raw.get("schema_version")
    if mid is not None and mid != schema_id:
        raise ConfigError(
            f"SCHEMA_ROOT_URL manifest schema_id={mid!r} does not match "
            f"NODE_SCHEMA_ID={schema_id!r}."
        )
    if mver is not None and mver != schema_version:
        raise ConfigError(
            f"SCHEMA_ROOT_URL manifest schema_version={mver!r} does not match "
            f"NODE_SCHEMA_VERSION={schema_version!r}."
        )
    files = raw.get("files")
    if not isinstance(files, dict) or not files:
        raise ConfigError(
            "SCHEMA_ROOT_URL stub manifest missing non-empty 'files' map "
            f"(schema_id={schema_id!r}/{schema_version!r})."
        )
    if _PACK_NAME not in files:
        raise ConfigError(
            "SCHEMA_ROOT_URL stub manifest must list files['pack.json'] "
            f"(schema_id={schema_id!r}/{schema_version!r})."
        )
    out: dict[str, str] = {}
    for name, url in files.items():
        if not isinstance(name, str) or not name or "/" in name or "\\" in name:
            raise ConfigError(
                f"SCHEMA_ROOT_URL manifest has invalid file name {name!r} "
                "(basename only; no path separators)."
            )
        if name in {".", ".."}:
            raise ConfigError(
                f"SCHEMA_ROOT_URL manifest has invalid file name {name!r}."
            )
        if not isinstance(url, str) or not url.strip():
            raise ConfigError(
                f"SCHEMA_ROOT_URL manifest file {name!r} needs a non-empty URL."
            )
        trimmed = url.strip()
        lower = trimmed.lower()
        if not (lower.startswith("http://") or lower.startswith("https://")):
            raise ConfigError(
                f"SCHEMA_ROOT_URL manifest file {name!r} URL must be http(s), "
                f"got {url!r}."
            )
        out[name] = trimmed
    return out


def ensure_remote_pack(
    *,
    schema_root_url: str,
    schema_id: str,
    schema_version: str,
    packs_root: Path,
    refresh: bool = False,
    client: httpx.Client | None = None,
) -> bool:
    """Fetch stub manifest + files into nested cache when miss or refresh.

    Returns True if a fetch ran, False if skipped (fresh cache, refresh=False).
    Raises ConfigError on any failure — caller must not fall back to another pack.
    """
    if pack_cache_fresh(packs_root, schema_id, schema_version) and not refresh:
        return False

    own_client = client is None
    http = client or httpx.Client(timeout=30.0)
    try:
        m_url = manifest_url(schema_root_url, schema_id, schema_version)
        try:
            response = http.get(m_url)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ConfigError(
                f"SCHEMA_ROOT_URL fetch failed for active "
                f"{schema_id!r}/{schema_version!r} at {m_url}: {exc}. "
                "No foreign default pack is applied."
            ) from exc

        try:
            payload: Any = response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            raise ConfigError(
                f"SCHEMA_ROOT_URL manifest at {m_url} is not valid JSON: {exc}. "
                "No foreign default pack is applied."
            ) from exc

        files = _validate_manifest(
            payload, schema_id=schema_id, schema_version=schema_version
        )
        dest = packs_root / schema_id / schema_version
        dest.mkdir(parents=True, exist_ok=True)

        for name, file_url in files.items():
            try:
                file_resp = http.get(file_url)
                file_resp.raise_for_status()
            except httpx.HTTPError as exc:
                raise ConfigError(
                    f"SCHEMA_ROOT_URL file fetch failed for {name!r} "
                    f"({file_url}): {exc}. No foreign default pack is applied."
                ) from exc
            (dest / name).write_bytes(file_resp.content)

        if not (dest / _PACK_NAME).is_file():
            raise ConfigError(
                f"SCHEMA_ROOT_URL fetch did not produce {_PACK_NAME} under "
                f"{dest}. No foreign default pack is applied."
            )
        return True
    finally:
        if own_client:
            http.close()


def maybe_fetch_active_pack(
    *,
    schema_root_url: str | None,
    schema_id: str,
    schema_version: str,
    refresh: bool,
    environ: Mapping[str, str] | None = None,
    client: httpx.Client | None = None,
) -> bool:
    """Boot helper: when URL set, ensure cache then let resolve_pack run."""
    if not schema_root_url:
        return False
    from core.schema.resolver import default_packs_root

    return ensure_remote_pack(
        schema_root_url=schema_root_url,
        schema_id=schema_id,
        schema_version=schema_version,
        packs_root=default_packs_root(environ=environ),
        refresh=refresh,
        client=client,
    )
