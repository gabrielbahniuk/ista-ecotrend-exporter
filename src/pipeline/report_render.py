from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.pipeline.report_data import report_summary_recent
from src.pipeline.schemas import EnrichedRecord, ReportIndexContext, YearReportContext, YearSection


def _jinja_env(repo_root: Path) -> Environment:
    templates_dir = repo_root / "templates"
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_index_markdown(repo_root: Path, context: ReportIndexContext) -> str:
    return _jinja_env(repo_root).get_template("report_index.md.j2").render(**context)


def render_year_report_markdown(repo_root: Path, context: YearReportContext) -> str:
    return _jinja_env(repo_root).get_template("report_year.md.j2").render(**context)


def build_index_context(
    enriched: list[EnrichedRecord], years: list[int], generated_at: str
) -> ReportIndexContext:
    return {
        "generated_at": generated_at,
        "years": years,
        "summary_recent": report_summary_recent(enriched),
    }


def build_year_file_context(section: YearSection, generated_at: str) -> YearReportContext:
    return {
        "generated_at": generated_at,
        "year": int(section["year"]),
        "section": section,
    }
