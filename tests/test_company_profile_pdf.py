from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
RENDERER_PATH = (
    ROOT
    / ".agents"
    / "skills"
    / "cisp-company-profile"
    / "scripts"
    / "render_company_profile_pdf.py"
)
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "company_profile_catl.json"

SPEC = importlib.util.spec_from_file_location("company_profile_pdf_renderer", RENDERER_PATH)
assert SPEC is not None and SPEC.loader is not None
RENDERER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDERER)


class CompanyProfilePdfRendererTests(unittest.TestCase):
    def load_fixture(self) -> dict:
        return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_full_report_renders_valid_multipage_pdf(self) -> None:
        data = self.load_fixture()
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "catl-profile.pdf"
            rendered = RENDERER.render_report(data, output)

            self.assertEqual(rendered, output)
            self.assertTrue(output.exists())
            self.assertGreater(output.stat().st_size, 15_000)

            reader = PdfReader(str(output))
            self.assertGreaterEqual(len(reader.pages), 5)
            self.assertEqual(reader.metadata.title, "宁德时代新能源科技股份有限公司")
            self.assertEqual(reader.metadata.author, "CISP MCP")

            first_page = reader.pages[0].extract_text() or ""
            all_text = "\n".join(page.extract_text() or "" for page in reader.pages)
            for expected in (
                "宁德时代新能源科技股份有限公司",
                "91350900587527783P",
                "2026-07-27 10:08:43",
                "标准版",
                "CISP-CP-91350900587527783P-20260727-100843",
            ):
                self.assertIn(expected, first_page)

            self.assertIn("数据来源与证据说明", all_text)
            self.assertIn("本画像基于查询时点的公开数据摘要", all_text)
            self.assertNotIn("None", all_text)
            self.assertNotIn("{}", all_text)

    def test_sparse_partial_failure_and_long_text_render(self) -> None:
        long_scope = (
            "一般项目：技术服务、技术开发、技术咨询、技术交流、技术转让、"
            "技术推广；软件开发；数据处理服务；企业管理咨询。"
        ) * 18
        data = {
            "schema_version": "1.0",
            "report": {
                "title": "企业一页纸画像｜标准版",
                "company_name": "示例超长名称新能源技术研究开发与产业应用股份有限公司",
                "credit_code": "91350000EXAMPLE001",
                "query_time": "2026-07-27 12:00:00",
                "mode": "标准版",
                "report_id": "CISP-CP-91350000EXAMPLE001-20260727-120000",
                "data_source": "CISP MCP",
            },
            "summary": {
                "one_sentence": "主体已确认，部分扩展维度查询未完成。",
                "attention": ["专利维度查询超时，不能据此判断是否存在专利记录。"],
            },
            "subject": {
                "registration_status": "在营（开业）",
                "legal_representative": "示例人员",
                "business_scope_summary": long_scope,
            },
            "shareholders": [
                {
                    "name": "比例未披露的示例股东",
                    "type": "企业法人",
                    "ratio": "未披露",
                    "subscription": "",
                }
            ],
            "personnel": [],
            "network": [],
            "assets": [
                {
                    "dimension": "商标",
                    "status": "empty",
                    "count_display": "本次未返回",
                    "records": [],
                    "note": "成功但列表为空",
                },
                {
                    "dimension": "专利",
                    "status": "failed",
                    "records": [],
                    "note": "查询超时",
                },
            ],
            "risks": [
                {
                    "topic": "行政处罚",
                    "result": "本次未返回",
                    "facts": ["仅表示本次查询未返回相关公开记录"],
                    "level": "neutral",
                    "scope": "目标企业自身",
                }
            ],
            "changes": [],
            "evidence": {
                "successful_dimensions": ["工商深度"],
                "empty_dimensions": ["商标"],
                "failed_dimensions": [{"dimension": "专利", "reason": "查询超时"}],
                "limitations": ["字段缺失不等同于不存在相关记录"],
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "sparse-profile.pdf"
            RENDERER.render_report(data, output)
            reader = PdfReader(str(output))
            all_text = "\n".join(page.extract_text() or "" for page in reader.pages)

            self.assertGreaterEqual(len(reader.pages), 4)
            self.assertIn("查询超时", all_text)
            self.assertIn("成功但列表为空", all_text)
            self.assertIn("技术服务", all_text)
            self.assertNotIn("None", all_text)
            self.assertNotIn("{}", all_text)

    def test_schema_validation_rejects_missing_metadata(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing required report fields"):
            RENDERER.validate_evidence(
                {
                    "schema_version": "1.0",
                    "report": {
                        "company_name": "示例企业",
                    },
                }
            )

    def test_schema_validation_rejects_unknown_version(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported schema_version"):
            RENDERER.validate_evidence(
                {
                    "schema_version": "2.0",
                    "report": {},
                }
            )

    def test_ratio_parser_preserves_unparseable_values_for_table_only(self) -> None:
        self.assertEqual(RENDERER._parse_ratio("22.040000%"), 22.04)
        self.assertEqual(RENDERER._parse_ratio("100.5%"), 100.0)
        self.assertIsNone(RENDERER._parse_ratio("未披露"))
        self.assertIsNone(RENDERER._parse_ratio("-1%"))


if __name__ == "__main__":
    unittest.main()
