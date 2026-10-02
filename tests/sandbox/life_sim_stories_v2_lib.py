"""Deterministic life-sim stories.json v2 builder (REQ11-12).

Emits flat fixture keys per REQ11-11 contract. No LLM. No StoryRecord dump.
No invent gpt_signals / taxonomy axis IDs. Scale locks match REQ11-01.
"""

from __future__ import annotations

import json
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

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

LANGS = ("et", "ru", "en")
DEFAULT_LOCATION = "Uus Veerenni, Tallinn"
DEFAULT_CANONICAL_TYPE = "complaint"

# Civic theme ids (label strings only — not taxonomy axis IDs).
DEFAULT_THEME_IDS: tuple[str, ...] = (
    "waste",
    "lighting",
    "pothole",
    "construction",
    "crossing",
    "noise",
    "parking",
    "playground",
    "greenery",
    "drainage",
)

# Composed-template banks: title / issue / request per lang × theme.
# Cardinality × place variants × story_seq → full uniqueness without LLM.
_THEME_I18N: dict[str, dict[str, dict[str, str]]] = {
    "waste": {
        "et": {
            "title": "Üleujutatud prügikastid",
            "issue": "prügikastid on üle ujutatud ja haisevad",
            "request": "Palun korraldada erakorraline jäätmevedu",
        },
        "ru": {
            "title": "Переполненные баки",
            "issue": "мусорные баки переполнены и сильно пахнут",
            "request": "Прошу организовать внеочередной вывоз отходов",
        },
        "en": {
            "title": "Overflowing waste bins",
            "issue": "waste bins overflow and smell strongly",
            "request": "Please arrange an extra waste collection",
        },
    },
    "lighting": {
        "et": {
            "title": "Tänavavalgustus ei tööta",
            "issue": "tänavavalgustus ei tööta õhtuti",
            "request": "Palun kontrollida ja parandada valgustust",
        },
        "ru": {
            "title": "Не работает освещение",
            "issue": "уличное освещение не работает вечером",
            "request": "Прошу проверить и починить освещение",
        },
        "en": {
            "title": "Street lighting outage",
            "issue": "street lighting fails in the evening",
            "request": "Please inspect and repair the lighting",
        },
    },
    "pothole": {
        "et": {
            "title": "Ohtlik auk teel",
            "issue": "teel on ohtlik auk, mis kahjustab autosid",
            "request": "Palun teha teeremont võimalikult kiiresti",
        },
        "ru": {
            "title": "Опасная яма",
            "issue": "на дороге опасная яма, повреждает машины",
            "request": "Прошу срочно отремонтировать покрытие",
        },
        "en": {
            "title": "Dangerous pothole",
            "issue": "a dangerous pothole damages vehicles",
            "request": "Please repair the road surface promptly",
        },
    },
    "construction": {
        "et": {
            "title": "Öine ehitusmüra",
            "issue": "öisel ajal on mürarikas ehitustöö",
            "request": "Palun piirata mürarikkad tööd päevasele ajale",
        },
        "ru": {
            "title": "Ночной шум стройки",
            "issue": "ночью идут шумные строительные работы",
            "request": "Прошу ограничить шумные работы дневным временем",
        },
        "en": {
            "title": "Night construction noise",
            "issue": "noisy construction continues at night",
            "request": "Please limit noisy works to daytime hours",
        },
    },
    "crossing": {
        "et": {
            "title": "Puudub ohutu ülekäik",
            "issue": "ristmikul puudub ohutu ülekäik jalakäijatele",
            "request": "Palun lisada ülekäigurada või liiklusmärgid",
        },
        "ru": {
            "title": "Нет безопасного перехода",
            "issue": "на перекрёстке нет безопасного перехода",
            "request": "Прошу добавить переход или знаки",
        },
        "en": {
            "title": "Missing safe crossing",
            "issue": "there is no safe pedestrian crossing",
            "request": "Please add a crosswalk or traffic signs",
        },
    },
    "noise": {
        "et": {
            "title": "Liigne müra õhtuti",
            "issue": "õhtuti on liigne müra, mis häirib und",
            "request": "Palun kontrollida müratasemeid ja reegleid",
        },
        "ru": {
            "title": "Лишний шум вечером",
            "issue": "вечером лишний шум мешает сну",
            "request": "Прошу проверить уровень шума и правила",
        },
        "en": {
            "title": "Excess evening noise",
            "issue": "excess noise in the evening disturbs sleep",
            "request": "Please check noise levels and rules",
        },
    },
    "parking": {
        "et": {
            "title": "Ebaseaduslik parkimine",
            "issue": "autod pargivad kõnniteel ja blokeerivad juurdepääsu",
            "request": "Palun suurendada järelevalvet parkimise üle",
        },
        "ru": {
            "title": "Незаконная парковка",
            "issue": "машины паркуются на тротуаре и блокируют проход",
            "request": "Прошу усилить контроль парковки",
        },
        "en": {
            "title": "Illegal sidewalk parking",
            "issue": "cars park on the sidewalk and block access",
            "request": "Please increase parking enforcement",
        },
    },
    "playground": {
        "et": {
            "title": "Mänguväljak vajab remonti",
            "issue": "mänguväljaku seadmed on katki või ohtlikud",
            "request": "Palun parandada või asendada mänguväljaku seadmed",
        },
        "ru": {
            "title": "Ремонт площадки",
            "issue": "оборудование детской площадки сломано или опасно",
            "request": "Прошу отремонтировать или заменить оборудование",
        },
        "en": {
            "title": "Playground needs repair",
            "issue": "playground equipment is broken or unsafe",
            "request": "Please repair or replace the playground gear",
        },
    },
    "greenery": {
        "et": {
            "title": "Hooldamata roheala",
            "issue": "roheala on hooldamata ja risune",
            "request": "Palun planeerida roheala hooldus",
        },
        "ru": {
            "title": "Неухоженная зелёная зона",
            "issue": "зелёная зона неухожена и захламлена",
            "request": "Прошу запланировать уход за зелёной зоной",
        },
        "en": {
            "title": "Neglected greenery",
            "issue": "the green area is neglected and littered",
            "request": "Please schedule greenery maintenance",
        },
    },
    "drainage": {
        "et": {
            "title": "Umbes juhtunud sademevesi",
            "issue": "sademevesi ei voola ära ja tekitab lomi",
            "request": "Palun puhastada sademevee äravool",
        },
        "ru": {
            "title": "Засор ливнёвки",
            "issue": "ливневая канализация не отводит воду, лужи",
            "request": "Прошу прочистить ливневой сток",
        },
        "en": {
            "title": "Blocked storm drain",
            "issue": "storm water does not drain and forms puddles",
            "request": "Please clear the storm drain",
        },
    },
}

_PLACE_SUFFIX: dict[str, tuple[str, ...]] = {
    "et": (
        "hoovi A",
        "hoovi B",
        "maja sissepääsu juures",
        "parkla servas",
        "kooli lähedal",
        "bussipeatuse juures",
        "ristmiku nurgas",
        "mänguväljaku kõrval",
    ),
    "ru": (
        "у двора A",
        "у двора B",
        "у подъезда",
        "у края парковки",
        "возле школы",
        "у остановки",
        "на углу перекрёстка",
        "рядом с площадкой",
    ),
    "en": (
        "at yard A",
        "at yard B",
        "by the entrance",
        "at the parking edge",
        "near the school",
        "by the bus stop",
        "at the intersection corner",
        "beside the playground",
    ),
}

_INSTITUTION_DEFAULT: dict[str, str] = {
    "et": "Tallinna Linnavalitsus",
    "ru": "Таллиннская городская управа",
    "en": "Tallinn City Government",
}

V2_REQUIRED_KEYS: tuple[str, ...] = (
    "fixture_story_id",
    "fixture_user_id",
    "created_at",
    "language",
    "title",
    "body",
    "title_i18n",
    "description_i18n",
    "summary_i18n",
    "session_language",
    "location_query",
    "canonical_type",
    "canonical_labels",
)


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
    if n <= 0:
        return []
    span = (end - start).total_seconds()
    if span <= 0:
        return [start] * n
    lam = max(steepness, 1e-9)
    out: list[datetime] = []
    for _ in range(n):
        u = rng.random()
        x = math.log1p(u * (math.expm1(lam))) / lam
        out.append(start + timedelta(seconds=span * x))
    out.sort()
    return out


def load_params(path: Path | None) -> dict[str, Any]:
    """Load optional pack params.json; empty/absent → {}."""
    if path is None or not path.is_file():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}
    return raw


def _theme_weights(params: dict[str, Any]) -> list[tuple[str, float]]:
    foci = params.get("story_foci")
    themes_raw: list[Any] = []
    if isinstance(foci, dict):
        themes_raw = list(foci.get("themes") or [])
    weights: list[tuple[str, float]] = []
    for item in themes_raw:
        if isinstance(item, str) and item.strip():
            weights.append((item.strip(), 1.0))
            continue
        if isinstance(item, dict):
            tid = str(item.get("id") or item.get("theme") or "").strip()
            if not tid:
                continue
            try:
                w = float(item.get("weight", 1.0))
            except (TypeError, ValueError):
                w = 1.0
            weights.append((tid, max(w, 0.0)))
    if not weights:
        return [(t, 1.0) for t in DEFAULT_THEME_IDS]
    # Unknown theme ids still usable as labels; fall back to waste bank text.
    return weights


def _pick_weighted(rng: random.Random, items: list[tuple[str, float]]) -> str:
    total = sum(w for _, w in items) or 1.0
    r = rng.random() * total
    acc = 0.0
    for tid, w in items:
        acc += w
        if r <= acc:
            return tid
    return items[-1][0]


def _neighbourhood_tags(params: dict[str, Any]) -> list[str]:
    uc = params.get("user_context")
    tags: list[Any] = []
    if isinstance(uc, dict):
        tags = list(uc.get("neighbourhood_tags") or [])
    out = [str(t).strip() for t in tags if str(t).strip()]
    return out


def _location_query(params: dict[str, Any]) -> str:
    tags = _neighbourhood_tags(params)
    if tags:
        return ", ".join(tags)
    return DEFAULT_LOCATION


def _place_base(params: dict[str, Any], lang: str) -> str:
    tags = _neighbourhood_tags(params)
    if tags:
        return tags[0]
    defaults = {
        "et": "Uus Veerenni",
        "ru": "Уус-Веэрэнни",
        "en": "Uus Veerenni",
    }
    return defaults.get(lang, DEFAULT_LOCATION)


def _direction_hint(params: dict[str, Any]) -> str:
    raw = str(params.get("node_social_direction") or "").strip()
    if not raw:
        return ""
    # Keep short — guiding interview text, not LLM expansion.
    one = " ".join(raw.split())
    return one[:80]


def _theme_bank(theme_id: str, lang: str) -> dict[str, str]:
    bank = _THEME_I18N.get(theme_id) or _THEME_I18N["waste"]
    return bank.get(lang) or bank["en"]


def compose_story_texts(
    *,
    lang: str,
    theme_id: str,
    story_seq: int,
    params: dict[str, Any],
) -> dict[str, Any]:
    """Compose unique multilingual title/body maps (deterministic, no LLM)."""
    hint = _direction_hint(params)
    hint_bit = f" ({hint})" if hint else ""
    suffix_idx = (story_seq - 1) % 8

    title_i18n: dict[str, str] = {}
    description_i18n: dict[str, str] = {}
    summary_i18n: dict[str, str] = {}
    for L in LANGS:
        bank = _theme_bank(theme_id, L)
        suffixes = _PLACE_SUFFIX.get(L) or _PLACE_SUFFIX["en"]
        place_L = f"{_place_base(params, L)} {suffixes[suffix_idx]}"
        title_i18n[L] = f"{bank['title']} — {place_L}"
        description_i18n[L] = (
            f"{place_L}{hint_bit}: {bank['issue']}. {bank['request']}. "
            f"[life-sim#{story_seq:05d}]"
        )
        summary_i18n[L] = f"{bank['title']}: {bank['issue']} [#{story_seq:05d}]"

    title = title_i18n[lang][:120]
    body = description_i18n[lang]

    labels = [theme_id]
    tags = _neighbourhood_tags(params)
    if tags:
        labels.append(tags[0].lower().replace(" ", "-"))

    return {
        "title": title,
        "body": body,
        "title_i18n": title_i18n,
        "description_i18n": description_i18n,
        "summary_i18n": summary_i18n,
        "canonical_labels": labels,
        "institution_i18n": dict(_INSTITUTION_DEFAULT),
    }


def build(
    *,
    seed: int = SEED,
    params: dict[str, Any] | None = None,
    pack_id: str | None = None,
) -> dict[str, Any]:
    """Build users + v2 stories + meta using REQ11-01 scale locks."""
    params = dict(params or {})
    rng = random.Random(seed)
    theme_weights = _theme_weights(params)
    location_query = _location_query(params)

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
            # Preserve REQ11-01 RNG stream: v0_1 consumed randrange(len(BLURBS[lang])).
            _ = rng.randrange(5)
            theme_rng = random.Random(seed * 1_000_003 + story_seq)
            theme_id = _pick_weighted(theme_rng, theme_weights)
            texts = compose_story_texts(
                lang=lang,
                theme_id=theme_id,
                story_seq=story_seq,
                params=params,
            )
            created = all_times[time_idx]
            time_idx += 1
            row: dict[str, Any] = {
                "fixture_story_id": f"life-sim-story-{story_seq:05d}",
                "fixture_user_id": user["fixture_user_id"],
                "language": lang,
                "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "title": texts["title"],
                "body": texts["body"],
                "title_i18n": texts["title_i18n"],
                "description_i18n": texts["description_i18n"],
                "summary_i18n": texts["summary_i18n"],
                "session_language": lang,
                "location_query": location_query,
                "canonical_type": DEFAULT_CANONICAL_TYPE,
                "canonical_labels": texts["canonical_labels"],
                "institution_i18n": texts["institution_i18n"],
            }
            stories.append(row)

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
    unique_bodies = len({str(s["body"]) for s in stories})

    meta: dict[str, Any] = {
        "schema_note": (
            "on-disk life-sim fixtures v2; flat Narrative-aligned keys; "
            "not a public API / StoryRecord dump"
        ),
        "fixture_contract": "REQ11-11-v2",
        "generator": "life_sim_stories_v2_lib",
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
        "diversity": {
            "unique_bodies": unique_bodies,
            "total_stories": total_stories,
            "pass_full_uniqueness": unique_bodies >= total_stories,
            "method": "composed_templates_plus_story_seq",
            "llm": False,
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
            "users": "users.json",
            "stories": "stories.json",
            "params": "params.json",
            "pack_id": pack_id,
        },
        "params_consumed": {
            "story_foci_themes": [t for t, _ in theme_weights],
            "neighbourhood_tags": _neighbourhood_tags(params),
            "node_social_direction_present": bool(
                str(params.get("node_social_direction") or "").strip()
            ),
            "location_query": location_query,
        },
        "relation_to_canvas": (
            "pack SSOT under life_sim_packs/<pack_id>/; flat *_v0_1 sandbox JSON "
            "is not SSOT for new packs; canvas remains runner stash→submit array"
        ),
    }
    return {"users": users, "stories": stories, "meta": meta, "params": params}


def default_params_snapshot(*, seed: int = SEED) -> dict[str, Any]:
    """Load-manual §4.3 shaped params for a reference v2 pack."""
    return {
        "profile_id": "local",
        "n_users": N_USERS,
        "stories_per_user": {
            "mean": GAUSS_MEAN,
            "sigma": GAUSS_SIGMA,
            "clamp": [CLAMP_LO, CLAMP_HI],
        },
        "lang_mix": {"et": 0.60, "ru": 0.30, "en": 0.10},
        "calendar": {
            "year": 2026,
            "breakpoint": "2026-09-30T00:00:00Z",
            "mass_pre": PRE_MASS,
            "mass_post": POST_MASS,
        },
        "seed": seed,
        "node_social_direction": (
            "Uus Veerenni yard civic complaints: waste, lighting, construction noise"
        ),
        "user_context": {
            "personas": [],
            "neighbourhood_tags": ["Uus Veerenni", "Tallinn"],
            "notes": "REQ11-12 v2 rich reference pack",
        },
        "story_foci": {
            "themes": [
                {"id": "construction", "weight": 0.25},
                {"id": "waste", "weight": 0.20},
                {"id": "lighting", "weight": 0.15},
                {"id": "noise", "weight": 0.15},
                {"id": "pothole", "weight": 0.10},
                {"id": "parking", "weight": 0.08},
                {"id": "crossing", "weight": 0.07},
            ]
        },
    }


def write_pack(
    pack_dir: Path,
    *,
    seed: int = SEED,
    params: dict[str, Any] | None = None,
    pack_id: str | None = None,
    write_params: bool = True,
) -> dict[str, Any]:
    """Write users/stories/meta/(params) under life_sim_packs/<pack_id>/."""
    pack_dir.mkdir(parents=True, exist_ok=True)
    resolved_id = pack_id or pack_dir.name
    params_path = pack_dir / "params.json"
    if params is None and params_path.is_file():
        params = load_params(params_path)
    if params is None:
        params = default_params_snapshot(seed=seed)
    payload = build(seed=seed, params=params, pack_id=resolved_id)
    (pack_dir / "users.json").write_text(
        json.dumps(payload["users"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (pack_dir / "stories.json").write_text(
        json.dumps(payload["stories"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (pack_dir / "meta.json").write_text(
        json.dumps(payload["meta"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if write_params:
        params_path.write_text(
            json.dumps(params, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    request_md = pack_dir / "request.md"
    if not request_md.is_file():
        utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        request_md.write_text(
            f"# life-sim pack request\n\n"
            f"- utc: `{utc}`\n"
            f"- pack_id: `{resolved_id}`\n"
            f"- generator: `life_sim_stories_v2_lib` (REQ11-12)\n"
            f"- intent: rich v2 stories for demo load (deterministic, no LLM)\n",
            encoding="utf-8",
        )
    return payload["meta"]
