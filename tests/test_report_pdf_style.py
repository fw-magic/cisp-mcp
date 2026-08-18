from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
COMMON_SKILL = ROOT / ".agents" / "skills" / "report-pdf-style"
COMMON_CONTRACT = COMMON_SKILL / "references" / "render-contract.md"
CLIENT_PDF_CONFIG = (
    ROOT / ".agents" / "skills" / "客户访前一页纸" / "references" / "pdf-style.md"
)
EQUITY_PDF_CONFIG = (
    ROOT / ".agents" / "skills" / "股权结构分析" / "references" / "pdf-delivery.md"
)
COMMON_TOOLKIT_PATH = COMMON_SKILL / "scripts" / "report_pdf_toolkit.py"
CLIENT_TOOLKIT_PATH = ROOT / ".agents" / "skills" / "客户访前一页纸" / "scripts" / "report_pdf_toolkit.py"
EQUITY_TOOLKIT_PATH = ROOT / ".agents" / "skills" / "股权结构分析" / "scripts" / "report_pdf_toolkit.py"
FIXTURE_SCRIPT = (
    ROOT
    / "tests"
    / "fixtures"
    / "report_pdf_style"
    / "generate_layout_fixtures.py"
)


def load_toolkit(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ReportPdfStyleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.common_toolkit = load_toolkit(COMMON_TOOLKIT_PATH, "common_pdf_toolkit_test")
        cls.client_toolkit = load_toolkit(CLIENT_TOOLKIT_PATH, "client_pdf_toolkit_test")
        cls.equity_toolkit = load_toolkit(EQUITY_TOOLKIT_PATH, "equity_pdf_toolkit_test")

    def test_common_reference_and_embedded_contracts_share_visual_tokens(self) -> None:
        contract = COMMON_CONTRACT.read_text(encoding="utf-8")
        client = CLIENT_PDF_CONFIG.read_text(encoding="utf-8")
        equity = EQUITY_PDF_CONFIG.read_text(encoding="utf-8")

        for token in (
            "215.9 × 279.4 mm",
            "10.5 pt",
            "#4D6EEB",
            "#CED4EE",
            "黑色 0.5 pt",
            "STSongti-SC-Regular",
            "STSongti-SC-Bold",
            "KeepTogether",
            "水滴征信 MCP",
            "cisp.zenitera.com · 水滴征信 MCP",
        ):
            with self.subTest(token=token):
                self.assertIn(token, contract)
                self.assertIn(token, client)
                self.assertIn(token, equity)

    def test_existing_report_skills_have_no_runtime_dependency_on_common_skill(self) -> None:
        for skill_name in ("客户访前一页纸", "股权结构分析"):
            skill_dir = ROOT / ".agents" / "skills" / skill_name
            texts = [
                path.read_text(encoding="utf-8")
                for path in skill_dir.rglob("*")
                if path.is_file() and path.suffix in {".md", ".py", ".yaml"}
            ]
            with self.subTest(skill=skill_name):
                self.assertNotIn("report-pdf-style", "\n".join(texts))
                self.assertTrue((skill_dir / "scripts" / "report_pdf_toolkit.py").is_file())

    def test_common_layer_contains_no_report_business_rules(self) -> None:
        common_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (COMMON_SKILL / "SKILL.md", COMMON_CONTRACT)
        )
        for forbidden in (
            "FACT-xx",
            "OPP-xx",
            "RISK-xx",
            "核心观点四个标签",
            "银行营销",
            "贷款机会",
            "实际控制人",
            "最终受益人",
            "控制权脆弱性",
            "一致行动人",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, common_text)

    def test_report_adapters_keep_their_business_boundaries(self) -> None:
        client = CLIENT_PDF_CONFIG.read_text(encoding="utf-8")
        equity = EQUITY_PDF_CONFIG.read_text(encoding="utf-8")
        for expected in ("FACT/OPP/RISK", "机会台账深化", "报告使用说明", "拜访建议与话题清单"):
            self.assertIn(expected, client)
        self.assertIn("不得引入 FACT/OPP/RISK", equity)
        self.assertNotIn("## 报告使用说明", equity)
        self.assertNotIn("## 七、拜访建议与话题清单", equity)
        for expected in (
            "八项报告头部",
            "实际控制人",
            "最终受益人",
            "控制权脆弱性",
            "一致行动边界",
        ):
            self.assertIn(expected, equity)
            self.assertNotIn(expected, client)

    def test_equity_columns_are_absolute_and_sum_to_content_width(self) -> None:
        equity = EQUITY_PDF_CONFIG.read_text(encoding="utf-8")
        allocations = re.findall(
            r"^- ([^：\n]+)："
            r"(\d+(?:\.\d+)?(?: / \d+(?:\.\d+)?)+)。$",
            equity,
            flags=re.MULTILINE,
        )
        self.assertEqual(len(allocations), 14)
        for table_name, widths_text in allocations:
            with self.subTest(table=table_name):
                widths = [float(value) for value in widths_text.split(" / ")]
                self.assertAlmostEqual(sum(widths), 165.9, places=1)

    def test_toolkit_tokens_and_distinct_fonts_match_contract(self) -> None:
        for toolkit in (self.common_toolkit, self.client_toolkit, self.equity_toolkit):
            with self.subTest(toolkit=toolkit.__name__):
                self.assertEqual(toolkit.CONTENT_WIDTH_MM, 165.9)
                self.assertEqual(toolkit.SECTION_BLUE.hexval().lower(), "0x4d6eeb")
                self.assertEqual(toolkit.SECTION_ACCENT_BLUE.hexval().lower(), "0x4d6eeb")
                self.assertEqual(toolkit.TABLE_HEADER_BLUE.hexval().lower(), "0xced4ee")
                self.assertEqual(toolkit.PAGE_CHROME_BLUE.hexval().lower(), "0x4d6eeb")
                self.assertEqual(toolkit.PAGE_CHROME_LINE_BLUE.hexval().lower(), "0x4d6eeb")
                self.assertEqual(toolkit.PAGE_CHROME_TEXT.hexval().lower(), "0x3f4e63")
                self.assertEqual(toolkit.PAGE_CHROME_RULE.hexval().lower(), "0xd9e2f0")
                self.assertEqual(toolkit.HEADER_RULE_FROM_TOP_MM, 12.0)
                self.assertEqual(toolkit.FOOTER_RULE_FROM_BOTTOM_MM, 12.0)
                metadata = toolkit.validate_font_spec(
                    toolkit.discover_font_spec(),
                    "中文常规字体粗体测试",
                )
                self.assertEqual(metadata["regular"], "STSongti-SC-Regular")
                self.assertEqual(metadata["bold"], "STSongti-SC-Bold")
                self.assertNotEqual(metadata["regular"], metadata["bold"])
                toolkit.register_chinese_fonts(required_text="表头正文")
                table = toolkit.make_table(
                    ["表头"], [["正文"]], [165.9], toolkit.make_styles()
                )
                self.assertEqual(type(table).__name__, "Table")

    def test_equity_cjk_cells_wrap_and_actions_are_separate_lines(self) -> None:
        toolkit = self.equity_toolkit
        toolkit.register_chinese_fonts(required_text="建议行动中文路径")
        styles = toolkit.make_styles()
        self.assertEqual(styles["table"].wordWrap, "CJK")
        self.assertEqual(styles["table_header"].wordWrap, "CJK")
        table = toolkit.make_table(
            ["中间层主体", "实控人对该主体出资 / 控制比例"],
            [["宁波通商控股集团有限公司", "宁波市国资委通过多层路径形成治理关系，比例未披露"]],
            [131.1, 34.8],
            styles,
            compact_columns={1},
        )
        self.assertEqual(table._cellvalues[1][1].style.wordWrap, "CJK")
        actions = toolkit.make_action_list(["第一项", "第二项", "第三项"], styles)
        self.assertEqual(len(actions), 4)
        self.assertIn("建议行动", actions[0].getPlainText())
        self.assertEqual(
            [item.getPlainText() for item in actions[1:]],
            ["1. 第一项", "2. 第二项", "3. 第三项"],
        )

    def assert_visible_page_chrome(self, toolkit, rendered_page: Path, dpi: int) -> None:
        image = Image.open(rendered_page).convert("RGB")

        def ink_on_row(y: int) -> int:
            return sum(
                1
                for x in range(image.width)
                if any(channel < 240 for channel in image.getpixel((x, y)))
            )

        header_rule_y = round(toolkit.HEADER_RULE_FROM_TOP_MM / 25.4 * dpi)
        footer_rule_y = image.height - round(
            toolkit.FOOTER_RULE_FROM_BOTTOM_MM / 25.4 * dpi
        )
        self.assertGreater(
            max(ink_on_row(y) for y in range(header_rule_y - 2, header_rule_y + 3)),
            image.width // 2,
        )
        self.assertGreater(
            max(ink_on_row(y) for y in range(footer_rule_y - 2, footer_rule_y + 3)),
            image.width // 2,
        )
        self.assertTrue(
            all(
                ink_on_row(y) < 5
                for y in range(header_rule_y + 3, round(19 / 25.4 * dpi))
            ),
            f"正文或表格侵入页眉留白区：{rendered_page}",
        )
        self.assertGreater(
            sum(ink_on_row(y) for y in range(round(7 / 25.4 * dpi), header_rule_y)),
            30,
        )
        self.assertGreater(
            sum(
                ink_on_row(y)
                for y in range(image.height - round(12 / 25.4 * dpi), image.height - round(5 / 25.4 * dpi))
            ),
            30,
        )

    def test_generated_layout_fixtures_and_markdown_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            subprocess.run(
                [sys.executable, str(FIXTURE_SCRIPT), "--output-dir", str(output_dir)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            cases = (
                (
                    self.client_toolkit,
                    output_dir / "客户访前一页纸-排版测试.pdf",
                    output_dir / "客户访前一页纸-排版测试-回退.md",
                    [
                        "对公客户访前一页纸",
                        "一、核心观点",
                        "二、执行摘要",
                        "三、客户全景画像",
                        "四、产业画像与行业洞察",
                        "五、定制化营销方案",
                        "六、风险预警与合规提示",
                        "七、拜访建议与话题清单",
                        "报告使用说明",
                    ],
                    "机会编号",
                    7,
                ),
                (
                    self.equity_toolkit,
                    output_dir / "股权结构穿透分析-排版测试.pdf",
                    output_dir / "股权结构穿透分析-排版测试-回退.md",
                    [
                        "股权结构穿透分析",
                        "执行摘要",
                        "一、数据来源与互证方法",
                        "二、穿透起点：核心运营主体基本信息",
                        "三、当前股权结构",
                        "四、实际控制人与受益所有人穿透",
                        "五、历史股权变迁",
                        "六、一致行动人与关联关系识别",
                        "七、控制权脆弱性评估",
                        "八、潜在关联交易风险清单",
                        "数据来源与免责声明",
                    ],
                    "股东名称",
                    8,
                ),
            )
            for toolkit, pdf_path, markdown_path, expected, header, min_pages in cases:
                with self.subTest(pdf=pdf_path.name):
                    report = toolkit.verify_pdf(
                        pdf_path,
                        expected_text=expected,
                        expected_every_page_text=[
                            toolkit.HEADER_LEFT_TEXT,
                            toolkit.HEADER_RIGHT_TEXT,
                            toolkit.FOOTER_LEFT_TEXT,
                        ],
                        require_page_numbers=True,
                        repeated_header=header,
                        min_repeated_pages=2,
                    )
                    self.assertGreaterEqual(report["pages"], min_pages)
                    self.assertTrue(report["page_chrome_verified"])
                    self.assertTrue(
                        any("STSongti-SC-Regular" in item for item in report["fonts"])
                    )
                    self.assertTrue(
                        any("STSongti-SC-Bold" in item for item in report["fonts"])
                    )
                    rendered = toolkit.render_pdf(
                        pdf_path,
                        output_dir / f"{pdf_path.stem}-pages",
                        dpi=72,
                    )
                    self.assertEqual(len(rendered), report["pages"])
                    if pdf_path.name == "股权结构穿透分析-排版测试.pdf":
                        markdown = markdown_path.read_text(encoding="utf-8")
                        conclusion = re.search(
                            r"> \*\*一句话结论：\*\* ([^\n]+)\n\n\|",
                            markdown,
                        )
                        self.assertIsNotNone(conclusion)
                        assert conclusion is not None
                        conclusion_text = conclusion.group(1)
                        self.assertEqual(conclusion_text.count("；"), 6)
                        for raw_value in ("7.123456%", "34.567891%", "51.234567%"):
                            self.assertIn(raw_value, conclusion_text)
                        for unsupported in ("100%一致", "符合 IPO 申报条件", "具备 IPO 申报资格"):
                            self.assertNotIn(unsupported, conclusion_text)

                        machine_phrases = (
                            "产品识别",
                            "产品返回",
                            "产品结论",
                            "本次返回",
                            "本次未返回",
                            "本次未完成",
                            "当前不可用",
                            "0命中",
                            "0 命中",
                            "聚合值",
                            "数据断点",
                            "路径互证",
                            "接口原值",
                            "模型判定",
                            "系统判定",
                        )
                        for machine_phrase in machine_phrases:
                            self.assertNotIn(machine_phrase, markdown)

                        pdf_text = "".join(
                            page.extract_text() or ""
                            for page in PdfReader(str(pdf_path)).pages
                        )
                        normalized_pdf_text = re.sub(r"\s+", "", pdf_text)
                        for raw_value in ("7.123456%", "34.567891%", "51.234567%"):
                            self.assertIn(raw_value, normalized_pdf_text)
                        self.assertNotIn("具备IPO申报资格", normalized_pdf_text)
                        for machine_phrase in machine_phrases:
                            self.assertNotIn(
                                re.sub(r"\s+", "", machine_phrase),
                                normalized_pdf_text,
                            )
                    for rendered_page in rendered:
                        self.assert_visible_page_chrome(toolkit, rendered_page, dpi=72)
                    markdown = markdown_path.read_text(encoding="utf-8")
                    for text in expected:
                        self.assertIn(text, markdown)

    def test_headers_use_bold_and_data_uses_regular_font_resources(self) -> None:
        fixture_pdf = ROOT / "output" / "pdf" / "tests" / "客户访前一页纸-排版测试.pdf"
        self.assertTrue(fixture_pdf.is_file(), "Run the layout fixture generator first")
        runs: list[tuple[str, str]] = []
        for page in PdfReader(str(fixture_pdf)).pages:
            def visitor(text, _cm, _tm, font, _size):
                if text.strip() and font:
                    runs.append((text.strip(), str(font.get("/BaseFont"))))

            page.extract_text(visitor_text=visitor)
        header_fonts = [font for text, font in runs if text == "机会编号"]
        regular_fonts = [font for text, font in runs if text == "贷款机会"]
        bold_id_fonts = [font for text, font in runs if text == "OPP-01"]
        self.assertTrue(header_fonts and all("STSongti-SC-Bold" in font for font in header_fonts))
        self.assertTrue(regular_fonts and all("STSongti-SC-Regular" in font for font in regular_fonts))
        self.assertTrue(bold_id_fonts and all("STSongti-SC-Bold" in font for font in bold_id_fonts))

    def test_failed_pdf_is_deleted_and_full_markdown_is_returned(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            partial_pdf = root / "partial.pdf"
            partial_pdf.write_bytes(b"not-a-pdf" * 300)
            fallback = root / "fallback.md"
            complete_markdown = (
                "# 股权结构穿透分析\n\n## 测试企业\n\n"
                "## 执行摘要\n\n## 一、数据来源与互证方法\n\n"
                "## 八、潜在关联交易风险清单\n\n## 数据来源与免责声明\n"
            )
            fallback.write_text(complete_markdown, encoding="utf-8")
            render_dir = root / "pages"
            render_dir.mkdir()
            (render_dir / "stale.png").write_bytes(b"stale")

            ok, payload = self.client_toolkit.guarded_validate_or_fallback(
                partial_pdf,
                fallback,
                render_dir,
            )

            self.assertFalse(ok)
            self.assertFalse(partial_pdf.exists())
            self.assertFalse(render_dir.exists())
            self.assertIn(complete_markdown, payload)
            self.assertIn("已回退 Markdown", payload)


if __name__ == "__main__":
    unittest.main()
