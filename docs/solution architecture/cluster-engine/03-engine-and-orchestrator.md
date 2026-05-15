# Cluster Engine — Engine & Orchestrator

---

## 1. stable_cluster_id() — SHA-256 (src/core/cluster/engine.py)

Заменить текущую реализацию через `hash()`:

```python
# ДО (нестабильно):
def stable_cluster_id(lens: ClusterLens, key: str) -> str:
    digest = abs(hash((lens.value, key))) % 1_000_000_000
    return f"cluster:{lens.value}:{digest:09d}"

# ПОСЛЕ (SHA-256, cross-process deterministic):
import hashlib

def stable_cluster_id(lens: ClusterLens, key: str) -> str:
    raw = f"{lens.value}:{key}".encode("utf-8")
    digest_hex = hashlib.sha256(raw).hexdigest()
    numeric = int(digest_hex, 16) % 10_000_000_000
    return f"cluster:{lens.value}:{numeric:010d}"
```

**Изменения формата:**
- Модуль: `1_000_000_000` → `10_000_000_000` (10-значный numeric part, 10 нулей в форматировании)
- Нулевое заполнение: `{:09d}` → `{:010d}` (10 цифр для 10-значного modulo)
- Алгоритм: `hash()` → `SHA-256`, не зависит от `PYTHONHASHSEED`

**Инвариант:** одни и те же `(lens, key)` → всегда одинаковый `cluster_id` в любом процессе, на любой машине.

**Примечание о `CLUSTER_ID_ALGORITHM=legacy_hash`:** если env var выставлен в `legacy_hash` — использовать старую функцию для backward compat при восстановлении данных из БД, записанных до миграции на SHA-256.

```python
def stable_cluster_id(lens: ClusterLens, key: str, *, algorithm: str = "sha256") -> str:
    if algorithm == "legacy_hash":
        digest = abs(hash((lens.value, key))) % 1_000_000_000
        return f"cluster:{lens.value}:{digest:09d}"
    raw = f"{lens.value}:{key}".encode("utf-8")
    digest_hex = hashlib.sha256(raw).hexdigest()
    numeric = int(digest_hex, 16) % 10_000_000_000
    return f"cluster:{lens.value}:{numeric:010d}"
```

---

## 2. lens_readiness_bonus() (src/core/cluster/engine.py)

```python
def lens_readiness_bonus(lens: ClusterLens) -> int:
    _HIGH_BONUS = frozenset({
        ClusterLens.CIVIC_WEIGHT_SYSTEMIC,
    })
    _MED_BONUS = frozenset({
        ClusterLens.GEOGRAPHIC_DISTRICT_MICRO,
        ClusterLens.FAILURE_SYSTEMIC,
        ClusterLens.RELEVANCE_SYSTEMIC,
    })
    if lens in _HIGH_BONUS:
        return 10
    if lens in _MED_BONUS:
        return 5
    return 0
```

---

## 3. readiness_score_for_cluster() — обновлённый (engine.py)

Перенести вычисление readiness из `build_view()` в хелпер; бонус теперь берётся из `lens_readiness_bonus()`:

```python
def readiness_score_for_cluster(
    *,
    lens: ClusterLens,
    members: tuple[ClusterMember, ...],
    mode: ClusteringMode,
) -> tuple[int, dict[str, int]]:
    size = len(members)
    base = min(100, 20 + size * 15)
    lens_bonus = lens_readiness_bonus(lens)
    mode_bonus = 10 if mode == ClusteringMode.ISSUE_READY else 0
    score = min(100, base + lens_bonus + mode_bonus)
    factors = {
        "size": size,
        "base": base,
        "lens_bonus": lens_bonus,
        "mode_bonus": mode_bonus,
    }
    return score, factors
```

---

## 4. build_cluster_narrative() — динамический (engine.py)

```python
def build_cluster_narrative(
    *,
    lens: ClusterLens,
    members: tuple[ClusterMember, ...],
    dominant: dict[str, str] | None = None,
) -> str:
    size = len(members)
    if dominant is None or not dominant:
        return f"Lens={lens.value}; members={size}"

    # Собрать значимые части из dominant signals
    parts: list[str] = []
    _INTERESTING_DIMS = (
        "civic_domain",
        "failure_pattern",
        "civic_weight",
        "desired_outcome",
        "affected_group",
        "geographic_district",
    )
    for dim in _INTERESTING_DIMS:
        val = dominant.get(dim)
        if val and val not in ("unknown", "isolated", "general_public"):
            parts.append(f"{dim}={val}")

    parts_str = "; ".join(parts) if parts else "no_dominant_signals"
    return f"lens={lens.value}; size={size}; {parts_str}"
```

**Пример результата:**
`"lens=civic_domain_micro; size=7; civic_domain=roads; failure_pattern=broken_infrastructure; civic_weight=recurring_issue; geographic_district=kesklinn"`

---

## 5. build_view() — per-Cluster readiness (engine.py)

**Проблема:** текущий `build_view()` считает `readiness_score` по `max(clusters, key=members)` — крупнейшему кластеру в view. Если целевая story находится в малом кластере, score неверен.

**Решение:** readiness хранится в каждом `Cluster`, не в `ClusterView`.

```python
def build_view(
    self,
    *,
    lens: ClusterLens,
    profiles: tuple[StoryProfileSignals, ...],
    mode: ClusteringMode,
    id_algorithm: str = "sha256",
) -> ClusterView:
    buckets: dict[str, list[StoryProfileSignals]] = defaultdict(list)
    for profile in sorted(profiles, key=lambda item: item.story_id):
        buckets[cluster_key_for_lens(profile, lens)].append(profile)

    clusters: list[Cluster] = []
    for key in sorted(buckets.keys()):
        members = tuple(ClusterMember(story_id=item.story_id) for item in buckets[key])
        score, factors = readiness_score_for_cluster(lens=lens, members=members, mode=mode)

        # Dominant signals for narrative (only within this cluster's members)
        cluster_profiles = buckets[key]
        dominant = ClusteringEngine._dominant_for_profiles(cluster_profiles)

        clusters.append(
            Cluster(
                cluster_id=stable_cluster_id(lens, key, algorithm=id_algorithm),
                lens=lens,
                members=members,
                readiness_score=score,
                readiness_factors=factors,
                key=key,
            )
        )

    # View-level narrative: describe the largest cluster
    primary = max(clusters, key=lambda c: len(c.members)) if clusters else None
    if primary is not None:
        primary_profiles = buckets.get(primary.key, [])
        dominant = ClusteringEngine._dominant_for_profiles(primary_profiles)
        narrative = build_cluster_narrative(lens=lens, members=primary.members, dominant=dominant)
        # View readiness_score = max across all clusters (for backward compat)
        view_score = max(c.readiness_score for c in clusters)
        view_factors = primary.readiness_factors
    else:
        narrative = f"Lens={lens.value}; empty_view"
        view_score = 0
        view_factors = {}

    return ClusterView(
        lens=lens,
        mode=mode,
        clusters=tuple(clusters),
        narrative=narrative,
        readiness_score=view_score,
        readiness_factors=view_factors,
    )

@staticmethod
def _dominant_for_profiles(profiles: list[StoryProfileSignals]) -> dict[str, str]:
    merged_dimensions: dict[str, list[str]] = defaultdict(list)
    for profile in profiles:
        for key, value in profile.signals.items():
            merged_dimensions[key].append(value)
    return {key: dominant_value(values) for key, values in merged_dimensions.items()}
```

---

## 6. memberships() — cluster_id + readiness per story/lens (engine.py)

```python
def memberships(
    self,
    profiles: tuple[StoryProfileSignals, ...],
    *,
    id_algorithm: str = "sha256",
) -> dict[str, dict[str, str]]:
    """Map story_id -> {lens_value: cluster_id} for all active lenses."""
    result: dict[str, dict[str, str]] = {}
    for lens in self.active_lenses:
        view = self.build_view(
            lens=lens,
            profiles=profiles,
            mode=ClusteringMode.ISSUE_READY,
            id_algorithm=id_algorithm,
        )
        for cluster in view.clusters:
            for member in cluster.members:
                result.setdefault(member.story_id, {})[lens.value] = cluster.cluster_id
    return result

def readiness_for_story(
    self,
    story_id: str,
    profiles: tuple[StoryProfileSignals, ...],
    primary_lens: ClusterLens,
    *,
    id_algorithm: str = "sha256",
) -> tuple[int, dict[str, int]]:
    """Return (score, factors) for story_id in primary_lens cluster."""
    view = self.build_view(
        lens=primary_lens,
        profiles=profiles,
        mode=ClusteringMode.ISSUE_READY,
        id_algorithm=id_algorithm,
    )
    for cluster in view.clusters:
        if any(m.story_id == story_id for m in cluster.members):
            return cluster.readiness_score, cluster.readiness_factors
    return 0, {}
```

**Ключевое изменение:** `memberships()` теперь использует `ClusteringMode.ISSUE_READY` (не `ANALYTIC`), чтобы `mode_bonus` был учтён в readiness.

---

## 7. Полный обновлённый ClusteringEngine (engine.py)

```python
@dataclass(frozen=True)
class ClusteringEngine:
    active_lenses: tuple[ClusterLens, ...]
    primary_lens: ClusterLens
    id_algorithm: str              # "sha256" | "legacy_hash"
    signal_source: str             # "canonical" only (keyword/hybrid удалены 2026-05-13)
    geo_filter: str                # "district"|"settlement"|"region"|"country" (default: "country")
    geo_scope: str | None          # "<level>:<value>" напр. "settlement:tallinn" (новый 2026-05-13)
    tie_breaker: str               # "alpha" (единственный поддерживаемый; oldest_first/systemic_priority — roadmap)
    type_resolution: str           # "canonical_priority" | "majority" | "first"
```

---

## 8. StoryClusterOrchestrator — целевая реализация (cluster_orchestrator.py)

### 8.1 Сигнатура

```python
@dataclass(frozen=True)
class StoryClusterOrchestrator:
    story_repository: StoryRepository
    clustering_engine: ClusteringEngine
    issue_create_service: IssueCreateService
    signal_store: StorySignalStore | None = None
    membership_store: ClusterMembershipStore | None = None
```

### 8.2 process_story() — полная реализация (11 шагов)

```python
import logging
logger = logging.getLogger(__name__)

def process_story(self, story_id: str) -> str | None:
    # ── Шаг 1: загрузить target story ────────────────────────────────────
    target = self.story_repository.get_story(story_id)
    if target is None:
        logger.warning("cluster.story_not_found", extra={"story_id": story_id})
        return None

    # ── Шаг 2: проверить lifecycle (идемпотентность) ──────────────────────
    if target.lifecycle_status is StoryLifecycleStatus.CLUSTERED:
        logger.info(
            "cluster.skipped_already_clustered",
            extra={"story_id": story_id},
        )
        return None
    if target.lifecycle_status is not StoryLifecycleStatus.READY_FOR_PROFILE:
        logger.warning(
            "cluster.story_not_ready",
            extra={"story_id": story_id, "status": target.lifecycle_status.value},
        )
        return None

    # ── Шаг 3: DB-side filter — только ready stories ─────────────────────
    ready_stories = self.story_repository.list_stories_ready_for_clustering()
    if not ready_stories:
        return None

    # ── Шаг 4: получить сигналы (кэш или вычислить) ──────────────────────
    signal_source = self.clustering_engine.signal_source
    id_algorithm = self.clustering_engine.id_algorithm
    policy = _signal_policy(signal_source)

    profiles_list: list[StoryProfileSignals] = []
    for story in ready_stories:
        signals = self._get_or_compute_signals(story, signal_source, policy)
        profiles_list.append(StoryProfileSignals(story_id=story.story_id, signals=signals))
    profiles = tuple(profiles_list)

    # ── Шаг 5: построить memberships ─────────────────────────────────────
    memberships = self.clustering_engine.memberships(profiles, id_algorithm=id_algorithm)
    if story_id not in memberships:
        return None

    # ── Шаг 6: определить кластер target story по primary lens ───────────
    primary_lens = self.clustering_engine.primary_lens
    cluster_id = memberships[story_id].get(primary_lens.value)
    if cluster_id is None:
        return None

    # ── Шаг 7: собрать members кластера ──────────────────────────────────
    member_story_ids = tuple(
        profile.story_id
        for profile in profiles
        if memberships.get(profile.story_id, {}).get(primary_lens.value) == cluster_id
    )
    if not member_story_ids:
        return None

    # ── Шаг 8: получить readiness_score именно для этого кластера ────────
    readiness_score, readiness_factors = self.clustering_engine.readiness_for_story(
        story_id=story_id,
        profiles=profiles,
        primary_lens=primary_lens,
        id_algorithm=id_algorithm,
    )

    # ── Шаг 9: проверить PromotionGates ПЕРЕД созданием ──────────────────
    # Примечание: IssueCreateService также вызывает gates.evaluate_promotion_gates()
    # внутри себя. Ранняя проверка здесь — только для observability logging.
    # Двойная проверка не проблема: gates — чистая функция.

    # ── Шаг 10: создать issue ─────────────────────────────────────────────
    # narrative_title_hint удалён в v2 контракте (2026-05-13)
    # issue_type и labels берутся из canonical fields (G-09, REQ-34)
    dominant_story = self._get_dominant_story(member_story_ids, profiles)
    issue_title = (
        (dominant_story.narrative_title or {}).get("en")
        or (dominant_story.narrative_title or {}).get("et")
        or f"cluster:{primary_lens.value}:{cluster_id}"
    )
    issue_type = dominant_story.narrative_canonical_type or "observation"
    issue_labels = list(dict.fromkeys(
        label
        for sid in member_story_ids
        for story in [self.story_repository.get_story(sid)]
        if story is not None
        for label in story.narrative_canonical_labels
    ))
    try:
        result = self.issue_create_service.create_issue(
            IssueCreateCommand(
                cluster_id=cluster_id,
                story_ids=member_story_ids,
                readiness_score=readiness_score,
                title=issue_title,
            )
        )
    except (ValueError, PromotionStateError) as exc:
        logger.info(
            "cluster.issue_creation_skipped",
            extra={
                "story_id": story_id,
                "cluster_id": cluster_id,
                "lens": primary_lens.value,
                "readiness_score": readiness_score,
                "reason": str(exc),
            },
        )
        return None

    issue_id = result.issue_id
    logger.info(
        "cluster.issue_created",
        extra={
            "story_id": story_id,
            "issue_id": issue_id,
            "cluster_id": cluster_id,
            "lens": primary_lens.value,
            "member_count": len(member_story_ids),
            "readiness_score": readiness_score,
            "readiness_factors": readiness_factors,
        },
    )

    # ── Шаг 11a: lifecycle advancement — все members → CLUSTERED ─────────
    for member_id in member_story_ids:
        try:
            self.story_repository.update_lifecycle_status(
                member_id, StoryLifecycleStatus.CLUSTERED
            )
        except Exception as exc:
            logger.error(
                "cluster.lifecycle_update_failed",
                extra={"story_id": member_id, "issue_id": issue_id, "error": str(exc)},
            )
            # Не останавливать pipeline — issue уже создан.

    # ── Шаг 11b: persist cluster memberships (optional) ──────────────────
    if self.membership_store is not None:
        for lens in self.clustering_engine.active_lenses:
            for member_id in member_story_ids:
                member_cluster_id = memberships.get(member_id, {}).get(lens.value)
                if member_cluster_id is None:
                    continue
                try:
                    self.membership_store.save_membership(
                        story_id=member_id,
                        lens=lens.value,
                        cluster_id=member_cluster_id,
                    )
                except Exception as exc:
                    logger.warning(
                        "cluster.membership_persist_failed",
                        extra={
                            "story_id": member_id,
                            "lens": lens.value,
                            "cluster_id": member_cluster_id,
                            "error": str(exc),
                        },
                    )

    return issue_id
```

### 8.3 Вспомогательные методы оркестратора

```python
def _get_or_compute_signals(
    self,
    story: StoryRecord,
    signal_source: str,
    policy: str,
) -> dict[str, str]:
    if self.signal_store is not None:
        cached = self.signal_store.get_signals(story.story_id, policy)
        if cached is not None:
            return cached

    signals = get_signals_for_story(story, signal_source)

    if self.signal_store is not None:
        try:
            self.signal_store.save_signals(story.story_id, policy, signals)
        except Exception as exc:
            logger.warning(
                "cluster.signal_persist_failed",
                extra={"story_id": story.story_id, "policy": policy, "error": str(exc)},
            )
    return signals


def _signal_policy(signal_source: str) -> str:
    _MAP = {
        "canonical": "v2.canonical",
        "keyword": "v1.keyword",
        "hybrid": "v2.hybrid",
    }
    return _MAP.get(signal_source, "v2.canonical")
```

**Примечание:** `_signal_policy` — module-level функция, не метод (нет обращения к `self`).

---

## 9. handlers.py — observability fix

```python
# src/core/api/handlers.py (фрагмент)

# ДО — результат молча отбрасывается:
dependencies.story_cluster_orchestrator.process_story(story.story_id)

# ПОСЛЕ — логировать результат:
issue_id = dependencies.story_cluster_orchestrator.process_story(story.story_id)
if issue_id:
    logger.info(
        "intake.cluster_triggered_issue",
        extra={"story_id": story.story_id, "issue_id": issue_id},
    )
else:
    logger.debug(
        "intake.cluster_no_issue",
        extra={"story_id": story.story_id},
    )
```

---

## 10. Полный flow process_story() (sequence)

```
handler.POST /stories
    │
    ├─ StoryIntakeService.create_story() → story_id
    │
    └─ StoryClusterOrchestrator.process_story(story_id)
           │
           ├─[1] story_repository.get_story(story_id)
           │       └─ None → return None
           │
           ├─[2] lifecycle check
           │       └─ CLUSTERED → return None (idempotency)
           │       └─ not READY_FOR_PROFILE → return None
           │
           ├─[3] story_repository.list_stories_ready_for_clustering()
           │       └─ DB-side WHERE lifecycle_status='ready_for_profile'
           │
           ├─[4] for each ready_story:
           │       └─ signal_store.get_signals(story_id, policy)  ← кэш
           │               └─ None: get_signals_for_story() → save_signals()
           │
           ├─[5] clustering_engine.memberships(profiles)
           │       └─ per-lens: build_view() → stable_cluster_id(sha256)
           │
           ├─[6] primary_lens cluster_id for target story
           │
           ├─[7] collect member_story_ids from memberships
           │
           ├─[8] clustering_engine.readiness_for_story()
           │       └─ per-Cluster score (не max кластера в view)
           │
           ├─[10] issue_create_service.create_issue(IssueCreateCommand)
           │        └─ PromotionStateError → log + return None
           │
           ├─[11a] story_repository.update_lifecycle_status(CLUSTERED)
           │         └─ для всех members
           │
           └─[11b] membership_store.save_membership() (if not None)
                     └─ для всех members × lenses
```

---

## 11. Тесты для engine & orchestrator (целевые)

| Тест | Суть |
|------|------|
| `test_stable_cluster_id_sha256_deterministic` | Одинаковый вход → одинаковый cluster_id в разных вызовах |
| `test_stable_cluster_id_sha256_vs_legacy_differ` | SHA-256 и legacy_hash → разные IDs для одного ключа |
| `test_readiness_per_cluster_not_max_cluster` | Story в малом кластере → score малого кластера, не крупного |
| `test_build_view_each_cluster_has_score` | Каждый Cluster в ClusterView имеет readiness_score > 0 |
| `test_memberships_uses_issue_ready_mode` | `build_view()` вызывается с `ClusteringMode.ISSUE_READY` |
| `test_orchestrator_skips_clustered_story` | Story со статусом CLUSTERED → process_story() → None без IO |
| `test_orchestrator_advances_lifecycle` | После создания issue → все members получают CLUSTERED |
| `test_orchestrator_signals_cached` | При наличии записи в signal_store → get_signals_for_story не вызывается |
| `test_orchestrator_no_duplicate_issue` | Повторный process_story() для того же story_id → None (idempotency) |
| `test_orchestrator_readiness_passed_to_create_issue` | IssueCreateCommand.readiness_score ≠ 100 (из engine, не hardcode) |
| `test_orchestrator_primary_lens_from_config` | primary_lens из ClusteringEngine, не active_lenses[0] |
| `test_build_cluster_narrative_dynamic` | Narrative содержит dominant signal values, не static template |
| `test_handler_logs_issue_id` | handlers.process_story() result логируется с issue_id |

---

## 12. Alpha Scoring — выбор dominant story (решение 2026-05-13, G-03, REQ-36)

Заменяет примитивный алфавитный tiebreaker. Dominant story = story с наибольшим `alpha_score`.

```python
def alpha_score(story: StoryRecord) -> float:
    score = 0.0

    # Измерение 1: Классификационная покрытость (0–30)
    if story.narrative_canonical_type:
        score += 12
    label_count = len(story.narrative_canonical_labels)
    score += min(label_count * 6, 18)  # до 3 меток × 6 pts

    # Измерение 2: Богатство нарратива (0–40)
    text_len = len(story.narrative_original_text.strip())
    score += min(text_len / 15, 20)    # cap: 300 символов → 20 pts
    if story.narrative_summary_json:
        score += 10
    if story.narrative_consistency_notes:
        score += 10

    # Измерение 3: Гео-точность (0–30)
    if story.geo is not None:
        score += 10
        score += story.geo.confidence * 20  # confidence=0.88 → +17.6 pts

    return score  # max: 100
```

**Tiebreaker при равных баллах:** старейшая история (`min(stories, key=lambda s: s.created_at)`).

**Canonical type readiness gate (`promotion/gates.py`):**  
Кластер без хотя бы одной истории с `canonical_type in {"complaint", "system_bug"}` → не промотируется в Issue.

**Местоположение в коде:** новый модуль `cluster/alpha.py` или встроить в `cluster/engine.py`.
