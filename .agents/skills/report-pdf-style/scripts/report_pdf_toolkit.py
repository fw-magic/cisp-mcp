#!/usr/bin/env python3
"""Shared Letter-size Chinese report PDF tokens, helpers, and validators."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Iterable, Sequence

from pypdf import PdfReader
from pypdf.generic import ContentStream
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle

PAGE_WIDTH_MM = 215.9
PAGE_HEIGHT_MM = 279.4
MARGIN_TOP_MM = 20.0
MARGIN_BOTTOM_MM = 20.0
MARGIN_LEFT_MM = 25.0
MARGIN_RIGHT_MM = 25.0
CONTENT_WIDTH_MM = 165.9

SECTION_BLUE = colors.HexColor("#4D6EEB")
SECTION_ACCENT_BLUE = colors.HexColor("#4D6EEB")
TABLE_HEADER_BLUE = colors.HexColor("#CED4EE")
GRID_BLACK = colors.black
PAGE_CHROME_BLUE = colors.HexColor("#4D6EEB")
PAGE_CHROME_LINE_BLUE = colors.HexColor("#4D6EEB")
PAGE_CHROME_TEXT = colors.HexColor("#3F4E63")
PAGE_CHROME_RULE = colors.HexColor("#D9E2F0")

HEADER_LEFT_TEXT = "水滴征信 MCP"
HEADER_RIGHT_TEXT = "审计留档"
FOOTER_LEFT_TEXT = "cisp.zenitera.com · 水滴征信 MCP"

HEADER_TEXT_FROM_TOP_MM = 9.0
HEADER_RULE_FROM_TOP_MM = 12.0
FOOTER_RULE_FROM_BOTTOM_MM = 12.0
FOOTER_TEXT_FROM_BOTTOM_MM = 7.5

BODY_SIZE = 10.5
BODY_LEADING = 15.0
TABLE_SIZE = 9.0
TABLE_LEADING = 12.0
META_SIZE = 9.0
META_LEADING = 12.0
TITLE_SIZE = 18.0
HEADING_1_SIZE = 14.0
HEADING_2_SIZE = 12.0

REGULAR_ALIAS = "ReportSongti"
BOLD_ALIAS = "ReportSongti-Bold"
HEADING_ALIAS = "ReportHeiti"


def draw_page_chrome(canvas: object, _document: object) -> None:
    """Draw the fixed report-family header, footer, and current page number."""
    page_width, page_height = LETTER
    left = MARGIN_LEFT_MM * mm
    right = page_width - MARGIN_RIGHT_MM * mm
    header_text_y = page_height - HEADER_TEXT_FROM_TOP_MM * mm
    header_rule_y = page_height - HEADER_RULE_FROM_TOP_MM * mm
    footer_rule_y = FOOTER_RULE_FROM_BOTTOM_MM * mm
    footer_text_y = FOOTER_TEXT_FROM_BOTTOM_MM * mm

    canvas.saveState()
    canvas.setLineWidth(0.5)
    canvas.setStrokeColor(PAGE_CHROME_LINE_BLUE)
    canvas.line(left, header_rule_y, right, header_rule_y)
    canvas.setFont(BOLD_ALIAS, 9.5)
    canvas.setFillColor(PAGE_CHROME_BLUE)
    canvas.drawString(left, header_text_y, HEADER_LEFT_TEXT)
    canvas.setFillColor(PAGE_CHROME_TEXT)
    canvas.drawRightString(right, header_text_y, HEADER_RIGHT_TEXT)

    canvas.setStrokeColor(PAGE_CHROME_RULE)
    canvas.line(left, footer_rule_y, right, footer_rule_y)
    canvas.setFont(REGULAR_ALIAS, 9)
    canvas.setFillColor(PAGE_CHROME_TEXT)
    canvas.drawString(left, footer_text_y, FOOTER_LEFT_TEXT)
    canvas.setFont(BOLD_ALIAS, 9)
    canvas.drawRightString(right, footer_text_y, f"第 {canvas.getPageNumber()} 页")
    canvas.restoreState()


class PdfContractError(RuntimeError):
    """Raised when a PDF violates the shared report contract."""


@dataclass(frozen=True)
class FontSpec:
    regular_path: Path
    regular_index: int
    bold_path: Path
    bold_index: int
    heading_path: Path
    heading_index: int


def _face_metadata(path: Path, index: int) -> tuple[str, TTFont]:
    font = TTFont("_ReportFontProbe", str(path), subfontIndex=index)
    raw_name = font.face.name
    name = raw_name.decode("utf-8", "replace") if isinstance(raw_name, bytes) else str(raw_name)
    return name, font


def discover_font_spec() -> FontSpec:
    songti = Path("/System/Library/Fonts/Supplemental/Songti.ttc")
    heiti = Path("/System/Library/Fonts/STHeiti Medium.ttc")
    if songti.is_file() and heiti.is_file():
        return FontSpec(songti, 6, songti, 1, heiti, 1)
    raise PdfContractError(
        "未发现受支持的中文 Regular/Bold/标题字体；请在报告适配器中显式提供 FontSpec"
    )


def validate_font_spec(
    font_spec: FontSpec,
    required_text: str = "正文测试粗体测试中文报告",
) -> dict[str, str]:
    regular_name, regular = _face_metadata(font_spec.regular_path, font_spec.regular_index)
    bold_name, bold = _face_metadata(font_spec.bold_path, font_spec.bold_index)
    heading_name, heading = _face_metadata(font_spec.heading_path, font_spec.heading_index)
    if regular_name == bold_name:
        raise PdfContractError("Regular 与 Bold 的 PostScript 名相同")
    missing: dict[str, list[str]] = {}
    for label, font in (("regular", regular), ("bold", bold), ("heading", heading)):
        absent = sorted(
            {
                char
                for char in required_text
                if not char.isspace() and ord(char) not in font.face.charToGlyph
            }
        )
        if absent:
            missing[label] = absent
    if missing:
        raise PdfContractError(f"中文字体缺字：{missing}")
    return {"regular": regular_name, "bold": bold_name, "heading": heading_name}


def register_chinese_fonts(
    font_spec: FontSpec | None = None,
    required_text: str = "正文测试粗体测试中文报告",
) -> dict[str, str]:
    font_spec = font_spec or discover_font_spec()
    metadata = validate_font_spec(font_spec, required_text)
    registered = set(pdfmetrics.getRegisteredFontNames())
    if REGULAR_ALIAS not in registered:
        pdfmetrics.registerFont(
            TTFont(
                REGULAR_ALIAS,
                str(font_spec.regular_path),
                subfontIndex=font_spec.regular_index,
            )
        )
    if BOLD_ALIAS not in registered:
        pdfmetrics.registerFont(
            TTFont(
                BOLD_ALIAS,
                str(font_spec.bold_path),
                subfontIndex=font_spec.bold_index,
            )
        )
    if HEADING_ALIAS not in registered:
        pdfmetrics.registerFont(
            TTFont(
                HEADING_ALIAS,
                str(font_spec.heading_path),
                subfontIndex=font_spec.heading_index,
            )
        )
    pdfmetrics.registerFontFamily(
        REGULAR_ALIAS,
        normal=REGULAR_ALIAS,
        bold=BOLD_ALIAS,
        italic=REGULAR_ALIAS,
        boldItalic=BOLD_ALIAS,
    )
    return metadata


def make_styles() -> dict[str, ParagraphStyle]:
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=styles["Normal"],
            fontName=HEADING_ALIAS,
            fontSize=TITLE_SIZE,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.black,
            spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "ReportH1",
            parent=styles["Normal"],
            fontName=HEADING_ALIAS,
            fontSize=HEADING_1_SIZE,
            leading=20,
            alignment=TA_LEFT,
            textColor=SECTION_BLUE,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=False,
        ),
        "h2": ParagraphStyle(
            "ReportH2",
            parent=styles["Normal"],
            fontName=HEADING_ALIAS,
            fontSize=HEADING_2_SIZE,
            leading=18,
            alignment=TA_LEFT,
            textColor=SECTION_BLUE,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=False,
        ),
        "body": ParagraphStyle(
            "ReportBody",
            parent=styles["Normal"],
            fontName=REGULAR_ALIAS,
            fontSize=BODY_SIZE,
            leading=BODY_LEADING,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=4,
            splitLongWords=True,
        ),
        "meta": ParagraphStyle(
            "ReportMeta",
            parent=styles["Normal"],
            fontName=REGULAR_ALIAS,
            fontSize=META_SIZE,
            leading=META_LEADING,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=0,
        ),
        "table": ParagraphStyle(
            "ReportTable",
            parent=styles["Normal"],
            fontName=REGULAR_ALIAS,
            fontSize=TABLE_SIZE,
            leading=TABLE_LEADING,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=0,
            splitLongWords=True,
        ),
        "table_header": ParagraphStyle(
            "ReportTableHeader",
            parent=styles["Normal"],
            fontName=BOLD_ALIAS,
            fontSize=TABLE_SIZE,
            leading=TABLE_LEADING,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=0,
            splitLongWords=True,
        ),
        "table_compact": ParagraphStyle(
            "ReportTableCompact",
            parent=styles["Normal"],
            fontName=REGULAR_ALIAS,
            fontSize=TABLE_SIZE,
            leading=TABLE_LEADING,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=0,
            splitLongWords=False,
            wordWrap="LTR",
        ),
        "table_bold": ParagraphStyle(
            "ReportTableBold",
            parent=styles["Normal"],
            fontName=BOLD_ALIAS,
            fontSize=TABLE_SIZE,
            leading=TABLE_LEADING,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=0,
            splitLongWords=True,
        ),
    }


def paragraph(text: object, style: ParagraphStyle, *, bold: bool = False) -> Paragraph:
    value = escape("" if text is None else str(text)).replace("\n", "<br/>")
    return Paragraph(f"<b>{value}</b>" if bold else value, style)


def make_table(
    headers: Sequence[object],
    rows: Sequence[Sequence[object]],
    col_widths_mm: Sequence[float],
    styles: dict[str, ParagraphStyle],
    *,
    compact_columns: Iterable[int] = (),
    bold_body_cells: Iterable[tuple[int, int]] = (),
    split_in_row: bool = False,
) -> Table:
    if len(headers) != len(col_widths_mm):
        raise PdfContractError("表头列数与列宽数量不一致")
    if abs(sum(col_widths_mm) - CONTENT_WIDTH_MM) > 0.05:
        raise PdfContractError(
            f"列宽合计必须为 {CONTENT_WIDTH_MM} mm，当前为 {sum(col_widths_mm):.3f} mm"
        )
    if any(len(row) != len(headers) for row in rows):
        raise PdfContractError("数据行列数与表头不一致")
    compact = set(compact_columns)
    bold_cells = set(bold_body_cells)
    data: list[list[Paragraph]] = [
        [paragraph(value, styles["table_header"]) for value in headers]
    ]
    for row_index, row in enumerate(rows):
        rendered: list[Paragraph] = []
        for col_index, value in enumerate(row):
            if (row_index, col_index) in bold_cells:
                cell_style = styles["table_bold"]
            elif col_index in compact:
                cell_style = styles["table_compact"]
            else:
                cell_style = styles["table"]
            rendered.append(paragraph(value, cell_style))
        data.append(rendered)
    # Standard Table splitting respects the frame height. LongTable's optimized
    # height scan can overrun the top margin for mixed long-cell fixtures.
    table = Table(
        data,
        colWidths=[width * mm for width in col_widths_mm],
        repeatRows=1,
        splitByRow=1,
        splitInRow=1 if split_in_row else 0,
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), BOLD_ALIAS),
                ("FONTNAME", (0, 1), (-1, -1), REGULAR_ALIAS),
                ("GRID", (0, 0), (-1, -1), 0.5, GRID_BLACK),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def _font_base_names(reader: PdfReader) -> set[str]:
    names: set[str] = set()
    for page in reader.pages:
        resources = page.get("/Resources")
        resources = resources.get_object() if resources else {}
        fonts = resources.get("/Font", {})
        fonts = fonts.get_object() if hasattr(fonts, "get_object") else fonts
        for font_ref in fonts.values():
            font = font_ref.get_object()
            base = font.get("/BaseFont")
            if base:
                names.add(str(base).lstrip("/"))
            descendant = font.get("/DescendantFonts")
            if descendant:
                for item in descendant:
                    descendant_font = item.get_object()
                    descendant_base = descendant_font.get("/BaseFont")
                    if descendant_base:
                        names.add(str(descendant_base).lstrip("/"))
    return names


def _page_fill_count(
    reader: PdfReader,
    page_index: int,
    rgb: tuple[float, float, float],
) -> int:
    page = reader.pages[page_index]
    stream = ContentStream(page.get_contents(), reader)
    count = 0
    for operands, operator in stream.operations:
        if operator == b"rg" and len(operands) == 3:
            values = tuple(float(value) for value in operands)
            if all(
                abs(actual - expected) <= 1 / 255 + 1e-6
                for actual, expected in zip(values, rgb)
            ):
                count += 1
    return count


def verify_pdf(
    pdf_path: Path,
    *,
    expected_text: Sequence[str] = (),
    expected_every_page_text: Sequence[str] = (),
    require_page_numbers: bool = False,
    repeated_header: str | None = None,
    min_repeated_pages: int = 2,
    regular_font_token: str = "STSongti-SC-Regular",
    bold_font_token: str = "STSongti-SC-Bold",
) -> dict[str, object]:
    if not pdf_path.is_file() or pdf_path.stat().st_size < 1000:
        raise PdfContractError(f"PDF 不存在或不完整：{pdf_path}")
    reader = PdfReader(str(pdf_path))
    if not reader.pages:
        raise PdfContractError("PDF 没有页面")
    page_sizes: list[list[float]] = []
    page_texts: list[str] = []
    for number, page in enumerate(reader.pages, start=1):
        width_mm = float(page.mediabox.width) / 72 * 25.4
        height_mm = float(page.mediabox.height) / 72 * 25.4
        page_sizes.append([round(width_mm, 2), round(height_mm, 2)])
        if abs(width_mm - PAGE_WIDTH_MM) > 0.2 or abs(height_mm - PAGE_HEIGHT_MM) > 0.2:
            raise PdfContractError(
                f"第 {number} 页不是 Letter：{width_mm:.2f} × {height_mm:.2f} mm"
            )
        page_texts.append(page.extract_text() or "")
    text = "\n".join(page_texts)
    if len(text.strip()) < 20:
        raise PdfContractError("PDF 文本不可提取或内容过少")
    missing = [item for item in expected_text if item not in text]
    if missing:
        raise PdfContractError(f"缺少必备文本：{missing}")
    page_chrome_failures: dict[int, list[str]] = {}
    for page_number, page_text in enumerate(page_texts, start=1):
        missing_on_page = [
            item for item in expected_every_page_text if item not in page_text
        ]
        if require_page_numbers and f"第 {page_number} 页" not in page_text:
            missing_on_page.append(f"第 {page_number} 页")
        if missing_on_page:
            page_chrome_failures[page_number] = missing_on_page
    if page_chrome_failures:
        raise PdfContractError(f"逐页页眉页脚或页码缺失：{page_chrome_failures}")
    placeholder_patterns = (
        r"\{\{[^{}]+\}\}",
        r"\[未替换[^\]]*\]",
        r"<placeholder>",
        r"\bTODO\b",
    )
    unresolved = [
        pattern
        for pattern in placeholder_patterns
        if re.search(pattern, text, flags=re.IGNORECASE)
    ]
    if unresolved:
        raise PdfContractError(f"检测到未替换占位符：{unresolved}")
    font_names = _font_base_names(reader)
    regular_matches = sorted(
        name for name in font_names if regular_font_token in name
    )
    bold_matches = sorted(name for name in font_names if bold_font_token in name)
    if not regular_matches or not bold_matches:
        raise PdfContractError(
            f"缺少真实中文 Regular/Bold 字体资源：{sorted(font_names)}"
        )
    if set(regular_matches) & set(bold_matches):
        raise PdfContractError("Regular 与 Bold 字体资源未分离")
    header_pages: list[int] = []
    target_rgb = (
        TABLE_HEADER_BLUE.red,
        TABLE_HEADER_BLUE.green,
        TABLE_HEADER_BLUE.blue,
    )
    if repeated_header:
        header_pages = [
            index
            for index, value in enumerate(page_texts)
            if repeated_header in value
        ]
        if len(header_pages) < min_repeated_pages:
            raise PdfContractError(
                f"表头“{repeated_header}”仅出现在 {len(header_pages)} 页"
            )
        pages_without_fill = [
            index + 1
            for index in header_pages
            if _page_fill_count(reader, index, target_rgb) < 1
        ]
        if pages_without_fill:
            raise PdfContractError(
                f"重复表头页面缺少 #CED4EE 实色填充：{pages_without_fill}"
            )
    return {
        "pdf": str(pdf_path.resolve()),
        "pages": len(reader.pages),
        "page_sizes_mm": page_sizes,
        "fonts": sorted(font_names),
        "text_characters": len(text),
        "repeated_header_pages": [index + 1 for index in header_pages],
        "page_chrome_verified": bool(expected_every_page_text or require_page_numbers),
    }


def render_pdf(pdf_path: Path, render_dir: Path, dpi: int = 120) -> list[Path]:
    command = shutil.which("pdftoppm")
    if not command:
        raise PdfContractError("未发现 pdftoppm，无法执行逐页视觉验收")
    render_dir.mkdir(parents=True, exist_ok=True)
    for stale_page in render_dir.glob("page-*.png"):
        stale_page.unlink()
    prefix = render_dir / "page"
    result = subprocess.run(
        [command, "-png", "-r", str(dpi), str(pdf_path), str(prefix)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise PdfContractError(f"PDF 渲染失败：{result.stderr.strip()}")
    pages = sorted(render_dir.glob("page-*.png"))
    if not pages:
        raise PdfContractError("PDF 渲染未生成页面图片")
    return pages


def guarded_validate_or_fallback(
    pdf_path: Path,
    markdown_path: Path,
    render_dir: Path,
    **verify_kwargs: object,
) -> tuple[bool, str | dict[str, object]]:
    markdown = markdown_path.read_text(encoding="utf-8")
    try:
        report = verify_pdf(pdf_path, **verify_kwargs)
        report["rendered_pages"] = [
            str(path.resolve()) for path in render_pdf(pdf_path, render_dir)
        ]
        return True, report
    except Exception as exc:
        if pdf_path.exists():
            pdf_path.unlink()
        shutil.rmtree(render_dir, ignore_errors=True)
        return False, f"PDF 生成未完成：{exc}，已回退 Markdown\n\n{markdown}"


def create_font_preflight(output: Path) -> dict[str, object]:
    from reportlab.pdfgen import canvas

    regular_sample = "正文测试：中文常规字形与可提取文本"
    bold_sample = "粗体测试：中文真实粗体字形与可提取文本"
    metadata = register_chinese_fonts(required_text=regular_sample + bold_sample)
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output), pagesize=LETTER)
    pdf.setFont(REGULAR_ALIAS, BODY_SIZE)
    pdf.drawString(25 * mm, 250 * mm, regular_sample)
    pdf.setFont(BOLD_ALIAS, BODY_SIZE)
    pdf.drawString(25 * mm, 240 * mm, bold_sample)
    pdf.save()
    report = verify_pdf(output, expected_text=["正文测试", "粗体测试"])
    report["font_preflight"] = metadata
    return report


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    preflight = subparsers.add_parser("font-preflight")
    preflight.add_argument("--output", type=Path, required=True)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--pdf", type=Path, required=True)
    verify.add_argument("--render-dir", type=Path)
    verify.add_argument("--expected", action="append", default=[])
    verify.add_argument("--every-page", action="append", default=[])
    verify.add_argument("--page-numbers", action="store_true")
    verify.add_argument("--repeat-header")
    verify.add_argument("--min-repeat-pages", type=int, default=2)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    try:
        if args.command == "font-preflight":
            report = create_font_preflight(args.output)
        else:
            report = verify_pdf(
                args.pdf,
                expected_text=args.expected,
                expected_every_page_text=args.every_page,
                require_page_numbers=args.page_numbers,
                repeated_header=args.repeat_header,
                min_repeated_pages=args.min_repeat_pages,
            )
            if args.render_dir:
                report["rendered_pages"] = [
                    str(path.resolve())
                    for path in render_pdf(args.pdf, args.render_dir)
                ]
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
