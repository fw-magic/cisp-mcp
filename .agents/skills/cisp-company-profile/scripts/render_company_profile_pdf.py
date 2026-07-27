#!/usr/bin/env python3
"""Render a CISP company-profile evidence model as a polished A4 PDF."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


SCHEMA_VERSION = "1.0"
FONT_NAME = "CISP-CJK"
PAGE_WIDTH, PAGE_HEIGHT = A4

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#1F6FEB")
LIGHT_BLUE = colors.HexColor("#EAF2FF")
PALE_BLUE = colors.HexColor("#F5F8FC")
SLATE = colors.HexColor("#52657A")
LIGHT_SLATE = colors.HexColor("#E5EAF0")
TEXT = colors.HexColor("#18212B")
MUTED = colors.HexColor("#657589")
WHITE = colors.white
AMBER = colors.HexColor("#B96B00")
PALE_AMBER = colors.HexColor("#FFF4DC")
RED = colors.HexColor("#B42318")
PALE_RED = colors.HexColor("#FDECEC")
GREEN = colors.HexColor("#287A4B")
PALE_GREEN = colors.HexColor("#EAF7EF")


def _font_candidates() -> list[Path]:
    configured = _text(os.getenv("CISP_PROFILE_FONT"))
    skill_asset = (
        Path(__file__).resolve().parents[1] / "assets" / "NotoSansCJKsc-Regular.otf"
    )
    candidates = [
        Path(configured) if configured else None,
        skill_asset,
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf"),
        Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    ]
    return [candidate for candidate in candidates if candidate is not None]


def _register_fonts() -> None:
    try:
        pdfmetrics.getFont(FONT_NAME)
        return
    except KeyError:
        pass

    errors: list[str] = []
    for candidate in _font_candidates():
        if not candidate.is_file():
            continue
        try:
            pdfmetrics.registerFont(TTFont(FONT_NAME, str(candidate)))
            return
        except Exception as exc:  # pragma: no cover - depends on host font parser
            errors.append(f"{candidate}: {exc}")

    detail = f" Tried: {'; '.join(errors)}" if errors else ""
    raise RuntimeError(
        "No embeddable Chinese font found. Set CISP_PROFILE_FONT to a TTF/OTF "
        f"font path or use Markdown fallback.{detail}"
    )


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "是" if value else "否"
    return str(value).strip()


def _clip(value: Any, limit: int) -> str:
    value_text = _text(value)
    if len(value_text) <= limit:
        return value_text
    return value_text[: max(1, limit - 1)].rstrip() + "…"


def _escape(value: Any) -> str:
    return html.escape(_text(value)).replace("\n", "<br/>")


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _nonempty_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _parse_ratio(value: Any) -> float | None:
    match = re.search(r"-?\d+(?:\.\d+)?", _text(value).replace(",", ""))
    if not match:
        return None
    try:
        parsed = float(match.group(0))
    except ValueError:
        return None
    if parsed < 0:
        return None
    return min(parsed, 100.0)


def validate_evidence(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("Evidence root must be a JSON object")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported schema_version: {data.get('schema_version')!r}; "
            f"expected {SCHEMA_VERSION!r}"
        )

    report = data.get("report")
    if not isinstance(report, dict):
        raise ValueError("report must be a JSON object")

    required = ("company_name", "credit_code", "query_time", "mode", "report_id")
    missing = [key for key in required if not _text(report.get(key))]
    if missing:
        raise ValueError(f"Missing required report fields: {', '.join(missing)}")

    for key in (
        "shareholders",
        "personnel",
        "network",
        "assets",
        "risks",
        "changes",
    ):
        if key in data and not isinstance(data[key], list):
            raise ValueError(f"{key} must be a JSON array")

    evidence = data.get("evidence")
    if evidence is not None and not isinstance(evidence, dict):
        raise ValueError("evidence must be a JSON object")

    return data


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ProfileTitle",
            parent=base["Title"],
            fontName=FONT_NAME,
            fontSize=22,
            leading=28,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=4 * mm,
        ),
        "company": ParagraphStyle(
            "CompanyName",
            parent=base["Heading2"],
            fontName=FONT_NAME,
            fontSize=13,
            leading=18,
            textColor=TEXT,
            alignment=TA_CENTER,
            spaceAfter=4 * mm,
        ),
        "section": ParagraphStyle(
            "SectionHeading",
            parent=base["Heading2"],
            fontName=FONT_NAME,
            fontSize=15,
            leading=20,
            textColor=BLUE,
            spaceBefore=1 * mm,
            spaceAfter=3 * mm,
        ),
        "subsection": ParagraphStyle(
            "SubsectionHeading",
            parent=base["Heading3"],
            fontName=FONT_NAME,
            fontSize=11,
            leading=15,
            textColor=NAVY,
            spaceBefore=2 * mm,
            spaceAfter=2 * mm,
        ),
        "body": ParagraphStyle(
            "ProfileBody",
            parent=base["BodyText"],
            fontName=FONT_NAME,
            fontSize=9,
            leading=14,
            textColor=TEXT,
            spaceAfter=1.5 * mm,
        ),
        "small": ParagraphStyle(
            "ProfileSmall",
            parent=base["BodyText"],
            fontName=FONT_NAME,
            fontSize=7.6,
            leading=11,
            textColor=TEXT,
        ),
        "tiny": ParagraphStyle(
            "ProfileTiny",
            parent=base["BodyText"],
            fontName=FONT_NAME,
            fontSize=6.8,
            leading=9,
            textColor=MUTED,
        ),
        "label": ParagraphStyle(
            "ProfileLabel",
            parent=base["BodyText"],
            fontName=FONT_NAME,
            fontSize=7.5,
            leading=10,
            textColor=MUTED,
        ),
        "card_value": ParagraphStyle(
            "CardValue",
            parent=base["BodyText"],
            fontName=FONT_NAME,
            fontSize=13,
            leading=16,
            textColor=NAVY,
            alignment=TA_CENTER,
        ),
        "card_label": ParagraphStyle(
            "CardLabel",
            parent=base["BodyText"],
            fontName=FONT_NAME,
            fontSize=7.2,
            leading=9,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "white_header": ParagraphStyle(
            "WhiteHeader",
            parent=base["BodyText"],
            fontName=FONT_NAME,
            fontSize=8,
            leading=11,
            textColor=WHITE,
            alignment=TA_LEFT,
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=base["BodyText"],
            fontName=FONT_NAME,
            fontSize=9,
            leading=14,
            textColor=TEXT,
            leftIndent=2 * mm,
            rightIndent=2 * mm,
        ),
    }


def _paragraph(value: Any, style: ParagraphStyle) -> Paragraph:
    return Paragraph(_escape(value), style)


def _section_heading(number: str, title: str, styles: dict[str, ParagraphStyle]) -> Table:
    heading = Table(
        [[_paragraph(f"{number}  {title}", styles["section"])]],
        colWidths=[174 * mm],
    )
    heading.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 0, LIGHT_BLUE),
                ("LINEBEFORE", (0, 0), (0, -1), 4, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 1.5 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5 * mm),
            ]
        )
    )
    return heading


def _data_table(
    headers: list[str],
    rows: list[list[Any]],
    widths: list[float],
    styles: dict[str, ParagraphStyle],
    *,
    repeat_rows: int = 1,
) -> Table:
    table_data: list[list[Any]] = [
        [_paragraph(header, styles["white_header"]) for header in headers]
    ]
    for row in rows:
        table_data.append([_paragraph(value, styles["small"]) for value in row])

    table = Table(table_data, colWidths=widths, repeatRows=repeat_rows, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_SLATE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE_BLUE]),
                ("LEFTPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
            ]
        )
    )
    return table


def _key_value_table(
    entries: list[tuple[str, str]],
    styles: dict[str, ParagraphStyle],
) -> Table | None:
    filtered = [(label, value) for label, value in entries if _text(value)]
    if not filtered:
        return None
    rows = [
        [_paragraph(label, styles["label"]), _paragraph(value, styles["body"])]
        for label, value in filtered
    ]
    table = Table(rows, colWidths=[34 * mm, 140 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_SLATE),
                ("BACKGROUND", (0, 0), (0, -1), PALE_BLUE),
                ("ROWBACKGROUNDS", (1, 0), (1, -1), [WHITE, colors.HexColor("#FBFCFE")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.2 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2 * mm),
            ]
        )
    )
    return table


def _status_palette(level: str) -> tuple[colors.Color, colors.Color]:
    normalized = level.lower()
    if normalized in {"critical", "high", "重点关注"}:
        return PALE_RED, RED
    if normalized in {"attention", "warning", "提示关注"}:
        return PALE_AMBER, AMBER
    if normalized in {"clear", "success"}:
        return PALE_GREEN, GREEN
    return PALE_BLUE, SLATE


def _asset_display(asset: dict[str, Any]) -> str:
    explicit = _text(asset.get("count_display"))
    if explicit:
        return explicit
    count = asset.get("count")
    if isinstance(count, int):
        return f"{count:,}"
    if _text(count):
        return _text(count)
    status = _text(asset.get("status")).lower()
    if status == "failed":
        return "查询未完成"
    if status == "empty":
        return "本次未返回"
    return "未披露"


class ShareholderBarChart(Flowable):
    def __init__(self, shareholders: list[dict[str, Any]], width: float = 174 * mm):
        self.rows = [
            (item, _parse_ratio(item.get("ratio")))
            for item in shareholders[:5]
            if _parse_ratio(item.get("ratio")) is not None
        ]
        self.width = width
        self.height = 9 * mm + len(self.rows) * 8 * mm

    def wrap(self, avail_width: float, avail_height: float) -> tuple[float, float]:
        return min(self.width, avail_width), self.height

    def draw(self) -> None:
        canvas = self.canv
        label_width = 55 * mm
        bar_width = max(20 * mm, self.width - label_width - 20 * mm)
        y = self.height - 7 * mm
        canvas.setFont(FONT_NAME, 7.5)
        for item, ratio in self.rows:
            name = _clip(item.get("name"), 18)
            ratio_label = _clip(item.get("ratio"), 16)
            canvas.setFillColor(TEXT)
            canvas.drawString(0, y, name)
            canvas.setFillColor(LIGHT_SLATE)
            canvas.roundRect(label_width, y - 1.2 * mm, bar_width, 3.2 * mm, 1.2 * mm, fill=1, stroke=0)
            fill_width = bar_width * min(ratio or 0, 100) / 100
            canvas.setFillColor(BLUE)
            canvas.roundRect(label_width, y - 1.2 * mm, fill_width, 3.2 * mm, 1.2 * mm, fill=1, stroke=0)
            canvas.setFillColor(SLATE)
            canvas.drawRightString(self.width, y, ratio_label)
            y -= 8 * mm


def _dashboard(
    data: dict[str, Any],
    styles: dict[str, ParagraphStyle],
) -> list[Flowable]:
    report = _nonempty_dict(data.get("report"))
    summary = _nonempty_dict(data.get("summary"))
    subject = _nonempty_dict(data.get("subject"))
    shareholders = _as_list(data.get("shareholders"))
    assets = [_nonempty_dict(item) for item in _as_list(data.get("assets"))]
    risks = [_nonempty_dict(item) for item in _as_list(data.get("risks"))]
    evidence = _nonempty_dict(data.get("evidence"))

    story: list[Flowable] = [
        _paragraph(report.get("title") or "企业一页纸画像", styles["title"]),
        _paragraph(report["company_name"], styles["company"]),
    ]

    meta_rows = [
        [
            _paragraph("统一社会信用代码", styles["label"]),
            _paragraph(report["credit_code"], styles["small"]),
            _paragraph("登记状态", styles["label"]),
            _paragraph(subject.get("registration_status"), styles["small"]),
        ],
        [
            _paragraph("查询时间", styles["label"]),
            _paragraph(report["query_time"], styles["small"]),
            _paragraph("画像模式", styles["label"]),
            _paragraph(report["mode"], styles["small"]),
        ],
        [
            _paragraph("报告编号", styles["label"]),
            _paragraph(report["report_id"], styles["tiny"]),
            "",
            "",
        ],
    ]
    meta = Table(meta_rows, colWidths=[28 * mm, 61 * mm, 24 * mm, 61 * mm])
    meta.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_SLATE),
                ("BACKGROUND", (0, 0), (0, -1), PALE_BLUE),
                ("BACKGROUND", (2, 0), (2, -1), PALE_BLUE),
                ("SPAN", (1, 2), (3, 2)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2.5 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
            ]
        )
    )
    story.extend([meta, Spacer(1, 4 * mm)])

    story.append(_section_heading("01", "执行摘要", styles))
    summary_text = (
        summary.get("one_sentence")
        or summary.get("business_position")
        or "本次查询已形成企业公开信息摘要。"
    )
    summary_box = Table(
        [[_paragraph(_clip(summary_text, 260), styles["callout"])]],
        colWidths=[174 * mm],
    )
    summary_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8DDFB")),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ]
        )
    )
    story.extend([summary_box, Spacer(1, 3 * mm)])

    visible_assets = assets[:8]
    if visible_assets:
        cards: list[list[Any]] = []
        for start in range(0, len(visible_assets), 4):
            row: list[Any] = []
            for asset in visible_assets[start : start + 4]:
                card = Table(
                    [
                        [_paragraph(_asset_display(asset), styles["card_value"])],
                        [_paragraph(asset.get("dimension"), styles["card_label"])],
                    ],
                    colWidths=[41.5 * mm],
                )
                card.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
                            ("BOX", (0, 0), (-1, -1), 0.4, LIGHT_SLATE),
                            ("TOPPADDING", (0, 0), (-1, 0), 2.2 * mm),
                            ("BOTTOMPADDING", (0, -1), (-1, -1), 1.8 * mm),
                        ]
                    )
                )
                row.append(card)
            while len(row) < 4:
                row.append("")
            cards.append(row)
        asset_grid = Table(cards, colWidths=[43.5 * mm] * 4)
        asset_grid.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 1 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1 * mm),
                ]
            )
        )
        story.extend([asset_grid, Spacer(1, 3 * mm)])

    if risks:
        risk_cells: list[Any] = []
        for risk in risks[:6]:
            background, foreground = _status_palette(_text(risk.get("level")))
            cell = Table(
                [
                    [_paragraph(_clip(risk.get("topic"), 12), styles["card_label"])],
                    [_paragraph(_clip(risk.get("result"), 34), styles["small"])],
                ],
                colWidths=[56 * mm],
            )
            cell.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), background),
                        ("TEXTCOLOR", (0, 0), (-1, -1), foreground),
                        ("BOX", (0, 0), (-1, -1), 0.45, foreground),
                        ("TOPPADDING", (0, 0), (-1, -1), 1.5 * mm),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5 * mm),
                    ]
                )
            )
            risk_cells.append(cell)
        risk_rows: list[list[Any]] = []
        for start in range(0, len(risk_cells), 3):
            row = risk_cells[start : start + 3]
            while len(row) < 3:
                row.append("")
            risk_rows.append(row)
        risk_grid = Table(risk_rows, colWidths=[58 * mm] * 3)
        risk_grid.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 1 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 1 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 1 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1 * mm),
                ]
            )
        )
        story.extend(
            [
                _paragraph("核心风险面（查询时点）", styles["subsection"]),
                risk_grid,
                Spacer(1, 2.5 * mm),
            ]
        )

    top_shareholders = [
        f"{_text(item.get('name'))}（{_text(item.get('ratio')) or '比例未披露'}）"
        for item in shareholders[:3]
        if _text(item.get("name"))
    ]
    attention = [
        _clip(item, 85)
        for item in _as_list(summary.get("attention"))[:3]
        if _text(item)
    ]
    compact_rows: list[tuple[str, str]] = []
    if top_shareholders:
        compact_rows.append(("主要股东", "；".join(top_shareholders)))
    if attention:
        compact_rows.append(("提示关注", "；".join(attention)))
    compact = _key_value_table(compact_rows, styles)
    if compact is not None:
        story.extend([compact, Spacer(1, 2.5 * mm)])

    success_count = len(_as_list(evidence.get("successful_dimensions")))
    empty_count = len(_as_list(evidence.get("empty_dimensions")))
    failed_count = len(_as_list(evidence.get("failed_dimensions")))
    completion = (
        f"查询完整度：成功 {success_count} 个维度｜空结果 {empty_count} 个维度｜"
        f"未完成 {failed_count} 个维度"
    )
    completion_box = Table(
        [[_paragraph(completion, styles["small"])]],
        colWidths=[174 * mm],
    )
    completion_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.35, LIGHT_SLATE),
                ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
            ]
        )
    )
    story.append(completion_box)
    return story


def _subject_section(
    data: dict[str, Any],
    styles: dict[str, ParagraphStyle],
) -> list[Flowable]:
    subject = _nonempty_dict(data.get("subject"))
    entries = [
        ("法定代表人", _text(subject.get("legal_representative"))),
        ("企业类型", _text(subject.get("company_type"))),
        ("成立日期", _text(subject.get("established_date"))),
        ("注册资本", _text(subject.get("registered_capital"))),
        ("实收资本", _text(subject.get("paid_in_capital"))),
        ("注册地址", _text(subject.get("registered_address"))),
        ("登记机关", _text(subject.get("registration_authority"))),
        ("所属行业", _text(subject.get("industry"))),
        ("经营期限", _text(subject.get("operating_period"))),
        ("曾用名", _text(subject.get("former_names"))),
    ]
    section: list[Flowable] = [_section_heading("02", "主体与经营", styles)]
    table = _key_value_table(entries, styles)
    if table is not None:
        section.extend([table, Spacer(1, 4 * mm)])
    scope = _text(subject.get("business_scope_summary"))
    if scope:
        section.extend(
            [
                _paragraph("经营范围摘要", styles["subsection"]),
                _paragraph(scope, styles["body"]),
            ]
        )
    return section


def _equity_section(
    data: dict[str, Any],
    styles: dict[str, ParagraphStyle],
) -> list[Flowable]:
    shareholders = [
        _nonempty_dict(item) for item in _as_list(data.get("shareholders"))[:5]
    ]
    personnel = [_nonempty_dict(item) for item in _as_list(data.get("personnel"))[:5]]
    network = [_nonempty_dict(item) for item in _as_list(data.get("network"))]
    if not shareholders and not personnel and not network:
        return []

    section: list[Flowable] = [_section_heading("03", "股权、治理与经营网络", styles)]
    if shareholders:
        section.extend(
            [
                _paragraph("主要股东", styles["subsection"]),
                _data_table(
                    ["股东", "类型", "出资比例", "认缴信息"],
                    [
                        [
                            item.get("name"),
                            item.get("type"),
                            item.get("ratio"),
                            item.get("subscription"),
                        ]
                        for item in shareholders
                    ],
                    [66 * mm, 35 * mm, 25 * mm, 48 * mm],
                    styles,
                ),
            ]
        )
        chart = ShareholderBarChart(shareholders)
        if chart.rows:
            section.extend(
                [
                    Spacer(1, 3 * mm),
                    _paragraph("前五名股东比例图", styles["subsection"]),
                    chart,
                ]
            )

    if personnel:
        section.extend(
            [
                _paragraph("主要人员", styles["subsection"]),
                _data_table(
                    ["姓名", "职务", "说明"],
                    [
                        [item.get("name"), item.get("position"), item.get("note")]
                        for item in personnel
                    ],
                    [45 * mm, 55 * mm, 74 * mm],
                    styles,
                ),
            ]
        )

    if network:
        section.extend(
            [
                _paragraph("经营网络", styles["subsection"]),
                _data_table(
                    ["维度", "数量/状态", "代表项"],
                    [
                        [
                            item.get("dimension"),
                            item.get("count_display") or item.get("status"),
                            "；".join(_text(value) for value in _as_list(item.get("examples"))),
                        ]
                        for item in network
                    ],
                    [38 * mm, 33 * mm, 103 * mm],
                    styles,
                ),
            ]
        )
    return section


def _assets_section(
    data: dict[str, Any],
    styles: dict[str, ParagraphStyle],
) -> list[Flowable]:
    assets = [_nonempty_dict(item) for item in _as_list(data.get("assets"))]
    if not assets:
        return []
    rows = []
    for item in assets:
        records = []
        for record in _as_list(item.get("records"))[:3]:
            record_dict = _nonempty_dict(record)
            title = _text(record_dict.get("title"))
            detail = _text(record_dict.get("detail"))
            if title and detail:
                records.append(f"{title}（{detail}）")
            elif title or detail:
                records.append(title or detail)
        rows.append(
            [
                item.get("dimension"),
                _asset_display(item),
                "；".join(records),
                item.get("note"),
            ]
        )
    return [
        _section_heading("04", "经营资产与资质", styles),
        _data_table(
            ["维度", "数量/状态", "代表性记录", "数据说明"],
            rows,
            [31 * mm, 30 * mm, 78 * mm, 35 * mm],
            styles,
        ),
    ]


def _relations_section(
    data: dict[str, Any],
    styles: dict[str, ParagraphStyle],
) -> list[Flowable]:
    relations = _nonempty_dict(data.get("relations"))
    opinions = _nonempty_dict(data.get("public_opinion"))
    if not relations and not opinions:
        return []

    rows: list[list[Any]] = []
    if relations:
        examples = "；".join(
            _text(value) for value in _as_list(relations.get("examples"))[:5]
        )
        rows.append(
            [
                "投资与任职关联",
                relations.get("summary"),
                examples,
            ]
        )
    if opinions:
        opinion_examples = []
        for item in _as_list(opinions.get("records"))[:3]:
            item_dict = _nonempty_dict(item)
            pieces = [
                _text(item_dict.get("title")),
                _text(item_dict.get("date")),
                _text(item_dict.get("source")),
            ]
            opinion_examples.append(" / ".join(piece for piece in pieces if piece))
        rows.append(
            [
                "公开舆情线索",
                opinions.get("summary"),
                "；".join(opinion_examples),
            ]
        )
    return [
        _section_heading("05", "关联与舆情", styles),
        _data_table(
            ["维度", "概览", "代表性线索"],
            rows,
            [36 * mm, 50 * mm, 88 * mm],
            styles,
        ),
        Spacer(1, 3 * mm),
        _paragraph(
            "关联和舆情仅用于线索发现，不代表实际控制关系，也不等同于经核验的司法或监管事实。",
            styles["tiny"],
        ),
    ]


def _risk_section(
    data: dict[str, Any],
    styles: dict[str, ParagraphStyle],
) -> list[Flowable]:
    risks = [_nonempty_dict(item) for item in _as_list(data.get("risks"))]
    changes = [_nonempty_dict(item) for item in _as_list(data.get("changes"))[:5]]
    if not risks and not changes:
        return []

    has_relations = bool(
        _nonempty_dict(data.get("relations"))
        or _nonempty_dict(data.get("public_opinion"))
    )
    section_number = "06" if has_relations else "05"
    section: list[Flowable] = [
        _section_heading(section_number, "风险事实与近期变更", styles)
    ]
    if risks:
        risk_rows = []
        for item in risks:
            facts = "；".join(_text(value) for value in _as_list(item.get("facts"))[:3])
            scope = _text(item.get("scope"))
            if scope:
                facts = f"[{scope}] {facts}" if facts else f"[{scope}]"
            risk_rows.append([item.get("topic"), item.get("result"), facts])
        section.append(
            _data_table(
                ["主题", "本次查询结果", "关键事实"],
                risk_rows,
                [36 * mm, 42 * mm, 96 * mm],
                styles,
            )
        )
    if changes:
        section.extend(
            [
                _paragraph("近期工商变更", styles["subsection"]),
                _data_table(
                    ["日期", "变更事项", "变更摘要"],
                    [
                        [item.get("date"), item.get("item"), item.get("summary")]
                        for item in changes
                    ],
                    [30 * mm, 48 * mm, 96 * mm],
                    styles,
                ),
            ]
        )
    return section


def _evidence_section(
    data: dict[str, Any],
    styles: dict[str, ParagraphStyle],
) -> list[Flowable]:
    report = _nonempty_dict(data.get("report"))
    evidence = _nonempty_dict(data.get("evidence"))
    successful = [_text(item) for item in _as_list(evidence.get("successful_dimensions"))]
    empty = [_text(item) for item in _as_list(evidence.get("empty_dimensions"))]
    failed = []
    for item in _as_list(evidence.get("failed_dimensions")):
        if isinstance(item, dict):
            dimension = _text(item.get("dimension"))
            reason = _text(item.get("reason"))
            failed.append(f"{dimension}：{reason}" if reason else dimension)
        else:
            failed.append(_text(item))
    limitations = [_text(item) for item in _as_list(evidence.get("limitations"))]

    entries = [
        ("报告编号", _text(report.get("report_id"))),
        ("查询时间", _text(report.get("query_time"))),
        ("数据来源", _text(report.get("data_source") or "CISP MCP")),
        ("成功维度", "、".join(item for item in successful if item)),
        (
            "空结果维度",
            "、".join(item for item in empty if item)
            + ("；仅表示本次查询未返回相关公开记录" if empty else ""),
        ),
        ("未完成维度", "；".join(item for item in failed if item)),
        ("数据边界", "；".join(item for item in limitations if item)),
    ]
    has_relations = bool(
        _nonempty_dict(data.get("relations"))
        or _nonempty_dict(data.get("public_opinion"))
    )
    section_number = "07" if has_relations else "06"
    section: list[Flowable] = [
        _section_heading(section_number, "数据来源与证据说明", styles)
    ]
    table = _key_value_table(entries, styles)
    if table is not None:
        section.extend([table, Spacer(1, 4 * mm)])
    section.extend(
        [
            _paragraph("免责声明", styles["subsection"]),
            _paragraph(
                "本画像基于查询时点的公开数据摘要，仅用于企业概览和线索发现，"
                "不构成法律、财务、投资、估值、授信或企业准入意见。"
                "接口未返回记录、字段为空或查询失败，均不能被解释为企业完全合规或不存在相关风险。",
                styles["body"],
            ),
        ]
    )
    return section


def _append_section(story: list[Flowable], section: list[Flowable]) -> None:
    if not section:
        return
    story.append(PageBreak())
    story.extend(section)


def render_report(data: dict[str, Any], output_path: str | Path) -> Path:
    validated = validate_evidence(data)
    _register_fonts()
    styles = _styles()
    report = _nonempty_dict(validated.get("report"))

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(destination),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=18 * mm,
        title=_text(report.get("company_name")),
        author="CISP MCP",
        subject=_text(report.get("title") or "企业一页纸画像"),
        creator="CISP company-profile skill",
    )

    def on_page(canvas: Any, document: Any) -> None:
        canvas.saveState()
        canvas.setTitle(_text(report.get("company_name")))
        canvas.setAuthor("CISP MCP")
        canvas.setSubject(_text(report.get("title") or "企业一页纸画像"))
        canvas.setCreator("CISP company-profile skill")

        canvas.setStrokeColor(BLUE)
        canvas.setLineWidth(0.7)
        canvas.line(18 * mm, PAGE_HEIGHT - 13 * mm, PAGE_WIDTH - 18 * mm, PAGE_HEIGHT - 13 * mm)
        canvas.setFont(FONT_NAME, 7.5)
        canvas.setFillColor(BLUE)
        canvas.drawString(18 * mm, PAGE_HEIGHT - 10 * mm, "CISP MCP · 企业画像")
        canvas.setFillColor(MUTED)
        canvas.drawRightString(
            PAGE_WIDTH - 18 * mm,
            PAGE_HEIGHT - 10 * mm,
            _clip(report.get("report_id"), 42),
        )

        canvas.setStrokeColor(LIGHT_SLATE)
        canvas.line(18 * mm, 12 * mm, PAGE_WIDTH - 18 * mm, 12 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont(FONT_NAME, 7)
        canvas.drawString(18 * mm, 8 * mm, _clip(report.get("company_name"), 36))
        canvas.drawRightString(PAGE_WIDTH - 18 * mm, 8 * mm, f"第 {document.page} 页")
        canvas.restoreState()

    story: list[Flowable] = []
    story.extend(_dashboard(validated, styles))
    _append_section(story, _subject_section(validated, styles))
    _append_section(story, _equity_section(validated, styles))
    _append_section(story, _assets_section(validated, styles))
    _append_section(story, _relations_section(validated, styles))
    _append_section(story, _risk_section(validated, styles))
    _append_section(story, _evidence_section(validated, styles))

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return destination


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Evidence JSON must contain an object at the root")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a CISP company-profile evidence JSON file as PDF."
    )
    parser.add_argument("--input", required=True, type=Path, help="Evidence JSON path")
    parser.add_argument("--output", required=True, type=Path, help="Destination PDF path")
    args = parser.parse_args()

    data = _load_json(args.input)
    destination = render_report(data, args.output)
    print(destination.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
