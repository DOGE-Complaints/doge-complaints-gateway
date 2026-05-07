from __future__ import annotations

from core.projection import I18nText, ProjectionInput, DOGEIssueStatus, DOGEIssueType, DOGEIssueLabel, project_distinct_issue


def _input(*, summary: I18nText | None = None) -> ProjectionInput:
    return ProjectionInput(
        issue_id="i18n-issue-1",
        status=DOGEIssueStatus.NEW.value,
        issue_type=DOGEIssueType.IMPROVEMENT.value,
        labels=(DOGEIssueLabel.DISTRICT.value,),
        title=I18nText(et="Valgustuse mure", ru="Проблема освещения", en="Lighting issue"),
        summary=summary,
        description=I18nText(
            et="Valgustid ei tööta öösiti",
            ru="Фонари не работают по ночам",
            en="Lights are not working at night",
        ),
    )


def test_locale_fields_preserve_differences_for_title_and_description() -> None:
    projection = project_distinct_issue(_input()).to_public_dict()
    title = projection["title"]
    description = projection["description"]

    assert title["et"] != title["en"]
    assert title["ru"] != title["en"]
    assert description["et"] != description["en"]
    assert description["ru"] != description["en"]


def test_summary_fallback_keeps_locale_specific_values() -> None:
    projection = project_distinct_issue(
        _input(summary=I18nText(et="", ru="Краткое описание", en=""))
    ).to_public_dict()

    assert projection["summary"]["et"] == projection["title"]["et"]
    assert projection["summary"]["en"] == projection["title"]["en"]
    assert projection["summary"]["ru"] == "Краткое описание"
    assert projection["summary"]["ru"] != projection["title"]["ru"]
