from __future__ import annotations

import pytest

from core.projection import (
    I18nText,
    IssueProjectionService,
    ProjectionContractError,
    ProjectionInput,
    SpaIssueStatus,
    SpaIssueType,
    SpaLabel,
    project_distinct_issue,
)


def _sample_input(*, summary: I18nText | None = None) -> ProjectionInput:
    return ProjectionInput(
        issue_id="issue-1",
        status=SpaIssueStatus.NEW.value,
        issue_type=SpaIssueType.IMPROVEMENT.value,
        labels=(SpaLabel.WASTE.value, SpaLabel.DISTRICT.value),
        title=I18nText(et="Pealkiri", ru="Заголовок", en="Title"),
        summary=summary,
        description=I18nText(et="Kirjeldus", ru="Описание", en="Description"),
    )


def test_project_distinct_issue_happy_path() -> None:
    out = project_distinct_issue(_sample_input())
    d = out.to_public_dict()
    assert d["id"] == "issue-1"
    assert d["status"] == "NEW"
    assert d["type"] == "IMPROVEMENT"
    assert d["labels"] == ["waste", "district"]
    assert set(d["title"].keys()) == {"et", "ru", "en"}
    assert d["summary"] == d["title"]


def test_summary_fallback_per_locale() -> None:
    partial = I18nText(et="", ru="Кратко", en="")
    out = project_distinct_issue(_sample_input(summary=partial))
    assert out.summary["et"] == "Pealkiri"
    assert out.summary["ru"] == "Кратко"
    assert out.summary["en"] == "Title"


def test_rejects_unknown_label() -> None:
    bad = ProjectionInput(
        issue_id="i",
        status=SpaIssueStatus.NEW.value,
        issue_type=SpaIssueType.IMPROVEMENT.value,
        labels=("unknown",),
        title=I18nText(et="a", ru="b", en="c"),
        summary=None,
        description=I18nText(et="d", ru="e", en="f"),
    )
    with pytest.raises(ProjectionContractError):
        project_distinct_issue(bad)


def test_rejects_placeholder_arweave() -> None:
    bad = ProjectionInput(
        issue_id="i",
        status=SpaIssueStatus.NEW.value,
        issue_type=SpaIssueType.IMPROVEMENT.value,
        labels=(SpaLabel.WASTE.value,),
        title=I18nText(et="a", ru="b", en="c"),
        summary=None,
        description=I18nText(et="d", ru="e", en="f"),
        arweave_txid="fake",
    )
    with pytest.raises(ProjectionContractError):
        project_distinct_issue(bad)


REQUIRED_SPA_KEYS = frozenset({"id", "status", "type", "labels", "title", "summary", "description"})


def test_spa_contract_required_keys() -> None:
    out = project_distinct_issue(_sample_input())
    d = out.to_public_dict()
    assert REQUIRED_SPA_KEYS.issubset(d.keys())


def test_issue_projection_service_delegates() -> None:
    svc = IssueProjectionService()
    out = svc.project(_sample_input())
    assert out.id == "issue-1"
