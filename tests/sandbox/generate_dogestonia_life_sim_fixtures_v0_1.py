#!/usr/bin/env python3
"""Generate life-sim users+stories JSON for GW-REQ11-01 (scale / langs / 2026 curve).

Operator lock (INDEX / STORY-GW-REQ11-01):
  200 users; Gaussian mean 8.5, σ 2.0, clamp [1, 20];
  langs 60% et / 30% ru / 10% en;
  calendar 2026; breakpoint 2026-09-30; mass ~25% pre / ~75% post.

Fixture schema is on-disk only — no invent public API field names for intake.
"""

from __future__ import annotations

import json
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
USERS_OUT = ROOT / "dogestonia_life_sim_users_v0_1.json"
STORIES_OUT = ROOT / "dogestonia_life_sim_stories_v0_1.json"
META_OUT = ROOT / "dogestonia_life_sim_fixtures_v0_1_meta.json"

SEED = 20260929
N_USERS = 200
GAUSS_MEAN = 8.5
GAUSS_SIGMA = 2.0
CLAMP_LO = 1
CLAMP_HI = 20
LANG_WEIGHTS: tuple[tuple[str, float], ...] = (("et", 0.60), ("ru", 0.30), ("en", 0.10))
BREAKPOINT = datetime(2026, 9, 30, 0, 0, 0, tzinfo=timezone.utc)
YEAR_START = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
YEAR_END = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
PRE_MASS = 0.25
POST_MASS = 0.75

# Short civic blurbs per language (fixture text only; not an API contract).
BLURBS: dict[str, tuple[str, ...]] = {
    "et": (
        "Tänaval on ohtlik auk, mis vajab remonti.",
        "Prügikastid üleujutatud ja haisevad.",
        "Tänavavalgustus ei tööta õhtuti.",
        "Ristmikul puudub ohutu ülekäik.",
        "Mürarikas ehitus öisel ajal.",
    ),
    "ru": (
        "На улице опасная яма, нужен ремонт.",
        "Мусорные баки переполнены и пахнут.",
        "Уличное освещение не работает вечером.",
        "На перекрёстке нет безопасного перехода.",
        "Шумные работы ночью.",
    ),
    "en": (
        "Dangerous pothole on the street needs repair.",
        "Waste bins overflow and smell.",
        "Street lighting fails in the evening.",
        "No safe crossing at the intersection.",
        "Noisy construction at night.",
    ),
}


def _clamp_stories_per_user(rng: random.Random) -> int:
    raw = rng.gauss(GAUSS_MEAN, GAUSS_SIGMA)
    return max(CLAMP_LO, min(CLAMP_HI, int(round(raw))))


def _pick_lang(rng: random.Random) -> str:
    r = rng.random()
    acc = 0.0
    for lang, w in LANG_WEIGHTS:
        acc += w
        if r <= acc:
            return lang
    return LANG_WEIGHTS[-1][0]


def _sample_exponential_times(
    rng: random.Random,
    n: int,
    start: datetime,
    end: datetime,
    *,
    steepness: float,
) -> list[datetime]:
    """Sample n timestamps in [start, end] with exponential intensity toward end."""
    if n <= 0:
        return []
    span = (end - start).total_seconds()
    if span <= 0:
        return [start] * n
    # Inverse-CDF of truncated Exp with rate λ; higher steepness → more mass near end.
    lam = max(steepness, 1e-9)
    out: list[datetime] = []
    for _ in range(n):
        u = rng.random()
        # Map u∈(0,1) via (e^{λx}-1)/(e^{λ}-1) inverted → x in [0,1]
        x = math.log1p(u * (math.expm1(lam))) / lam
        out.append(start + timedelta(seconds=span * x))
    out.sort()
    return out


def build(*, seed: int = SEED) -> dict[str, Any]:
    rng = random.Random(seed)
    users: list[dict[str, Any]] = []
    for i in range(1, N_USERS + 1):
        users.append(
            {
                "fixture_user_id": f"life-sim-user-{i:04d}",
                "display_name": f"LifeSim Resident {i:04d}",
                "preferred_language": _pick_lang(rng),
            }
        )

    per_user_counts = [_clamp_stories_per_user(rng) for _ in users]
    total_stories = sum(per_user_counts)
    n_pre = int(round(total_stories * PRE_MASS))
    n_post = total_stories - n_pre

    pre_times = _sample_exponential_times(
        rng, n_pre, YEAR_START, BREAKPOINT, steepness=2.0
    )
    post_times = _sample_exponential_times(
        rng, n_post, BREAKPOINT, YEAR_END, steepness=4.0
    )
    all_times = pre_times + post_times
    rng.shuffle(all_times)

    stories: list[dict[str, Any]] = []
    time_idx = 0
    story_seq = 0
    for user, n_stories in zip(users, per_user_counts, strict=True):
        for _ in range(n_stories):
            story_seq += 1
            lang = _pick_lang(rng)
            blurbs = BLURBS[lang]
            body = blurbs[rng.randrange(len(blurbs))]
            created = all_times[time_idx]
            time_idx += 1
            stories.append(
                {
                    "fixture_story_id": f"life-sim-story-{story_seq:05d}",
                    "fixture_user_id": user["fixture_user_id"],
                    "language": lang,
                    "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "title": body[:72],
                    "body": body,
                }
            )

    lang_counts = {k: 0 for k, _ in LANG_WEIGHTS}
    for s in stories:
        lang_counts[str(s["language"])] += 1
    pre_count = sum(
        1
        for s in stories
        if datetime.strptime(str(s["created_at"]), "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
        < BREAKPOINT
    )
    post_count = total_stories - pre_count

    meta: dict[str, Any] = {
        "schema_note": "on-disk life-sim fixtures; not a public API contract",
        "seed": seed,
        "operator_lock": {
            "n_users": N_USERS,
            "gaussian_mean": GAUSS_MEAN,
            "gaussian_sigma": GAUSS_SIGMA,
            "clamp": [CLAMP_LO, CLAMP_HI],
            "langs": dict(LANG_WEIGHTS),
            "breakpoint": BREAKPOINT.strftime("%Y-%m-%d"),
            "mass_pre_post": [PRE_MASS, POST_MASS],
        },
        "counts": {
            "users": len(users),
            "stories": total_stories,
            "stories_per_user_min": min(per_user_counts),
            "stories_per_user_max": max(per_user_counts),
            "stories_per_user_mean": round(total_stories / len(users), 4),
            "lang_counts": lang_counts,
            "lang_fractions": {
                k: round(v / total_stories, 4) for k, v in lang_counts.items()
            },
            "pre_breakpoint": pre_count,
            "post_breakpoint": post_count,
            "pre_fraction": round(pre_count / total_stories, 4),
            "post_fraction": round(post_count / total_stories, 4),
        },
        "paths": {
            "users": USERS_OUT.name,
            "stories": STORIES_OUT.name,
        },
        "relation_to_canvas": (
            "supersedes canvas v0_1/v0_2 for life-sim multi-user scale; "
            "canvas remains runner stash→submit scenario array"
        ),
    }
    return {"users": users, "stories": stories, "meta": meta}


def write(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or build()
    USERS_OUT.write_text(
        json.dumps(data["users"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    STORIES_OUT.write_text(
        json.dumps(data["stories"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    META_OUT.write_text(
        json.dumps(data["meta"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return data["meta"]


def main() -> None:
    meta = write()
    print(json.dumps(meta["counts"], indent=2))
    print(f"wrote {USERS_OUT}")
    print(f"wrote {STORIES_OUT}")
    print(f"wrote {META_OUT}")


if __name__ == "__main__":
    main()
