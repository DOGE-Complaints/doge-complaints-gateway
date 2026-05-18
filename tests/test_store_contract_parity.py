from __future__ import annotations

from core.infrastructure.repositories import (
    InMemoryClusterMembershipStore,
    InMemoryStoryEmbeddingStore,
    InMemoryStorySignalStore,
)


def test_story_embedding_store_writes_vector_tuple_not_sql_embedding() -> None:
    """REQ-39 H-01: in-memory store keeps embedding_vector tuple (GAP-08 write contract)."""
    store = InMemoryStoryEmbeddingStore()
    store.save_story_embedding(
        story_id="s1",
        model_name="test-model",
        embedding_vector=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8),
        source_checksum="abc123",
        embedding_policy_version="test.v1",
    )
    assert store._rows is not None
    row = store._rows[0]
    assert "embedding_vector" in row
    assert "embedding" not in row
    assert isinstance(row["embedding_vector"], tuple)


def test_story_signal_store_writes_dict_not_json_string() -> None:
    """REQ-39 H-02: signals stored as dict mapping, not pre-serialized JSON string."""
    store = InMemoryStorySignalStore()
    signals = {"type": "complaint", "urgency": "3"}
    store.save_signals(story_id="s1", policy="test-policy", signals=signals)
    result = store.get_signals(story_id="s1", policy="test-policy")
    assert result == signals
    assert isinstance(result, dict)


def test_cluster_membership_filters_by_lens() -> None:
    """REQ-39 H-03: get_cluster_members respects lens."""
    store = InMemoryClusterMembershipStore()
    store.save_membership(story_id="s1", lens="geo", cluster_id="c1")
    store.save_membership(story_id="s2", lens="topic", cluster_id="c1")
    members = store.get_cluster_members(cluster_id="c1", lens="geo")
    assert "s1" in members
    assert "s2" not in members
