from __future__ import annotations

import json

from core.infrastructure.db_supabase import _coerce_jsonb_text_id_sequence


def test_coerce_jsonb_postgrest_list() -> None:
    """GAP-09: PostgREST returns JSONB arrays as Python list."""
    assert _coerce_jsonb_text_id_sequence(["a", "b"]) == ("a", "b")


def test_coerce_json_string_legacy() -> None:
    assert _coerce_jsonb_text_id_sequence(json.dumps(["x", "y"])) == ("x", "y")


def test_coerce_none_empty() -> None:
    assert _coerce_jsonb_text_id_sequence(None) == ()


def test_coerce_tuple_like_sequence() -> None:
    assert _coerce_jsonb_text_id_sequence(("p", "q")) == ("p", "q")


def test_coerce_invalid_string_raises() -> None:
    try:
        _coerce_jsonb_text_id_sequence("not json")
    except json.JSONDecodeError:
        return
    raise AssertionError("expected json.JSONDecodeError")


def test_coerce_empty_list() -> None:
    assert _coerce_jsonb_text_id_sequence([]) == ()


def test_coerce_json_empty_array_string() -> None:
    assert _coerce_jsonb_text_id_sequence("[]") == ()


def test_coerce_list_of_ints_stringified() -> None:
    assert _coerce_jsonb_text_id_sequence([1, 2, 3]) == ("1", "2", "3")
