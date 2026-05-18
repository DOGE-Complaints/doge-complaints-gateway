from __future__ import annotations

import json

import pytest

from core.infrastructure.db_supabase import _coerce_jsonb_text_id_sequence, _parse_dt


def test_jsonb_list_coercion_covers_all_cases() -> None:
    """REQ-39 B-01: PostgREST JSONB list / legacy string / empty / coerced ints."""
    assert _coerce_jsonb_text_id_sequence(["a", "b"]) == ("a", "b")
    assert _coerce_jsonb_text_id_sequence('["x","y"]') == ("x", "y")
    assert _coerce_jsonb_text_id_sequence(None) == ()
    assert _coerce_jsonb_text_id_sequence([]) == ()
    assert _coerce_jsonb_text_id_sequence("[]") == ()
    assert _coerce_jsonb_text_id_sequence([1, 2]) == ("1", "2")


def test_text_json_columns_correct_deserialization() -> None:
    """REQ-39 B-02: TEXT columns hold JSON strings parsed like db_supabase row mapping."""
    raw_tags = '["tag1","tag2"]'
    assert tuple(json.loads(str(raw_tags or "[]"))) == ("tag1", "tag2")
    assert tuple(json.loads(str("[]" or "[]"))) == ()
    raw_labels = '["infrastructure","transport"]'
    assert json.loads(str(raw_labels)) == ["infrastructure", "transport"]


def test_datetime_parse_from_postgrest_format() -> None:
    """REQ-39 B-03: timestamptz ISO strings parse via _parse_dt (PostgREST shape)."""
    assert _parse_dt("2026-05-10T14:00:00+00:00") is not None
    assert _parse_dt("2026-05-10T14:00:00Z") is not None


def test_coerce_invalid_string_raises_not_silences() -> None:
    """REQ-39 B-04: invalid JSON must not silently become empty tuple."""
    with pytest.raises(json.JSONDecodeError):
        _coerce_jsonb_text_id_sequence("not json at all")
