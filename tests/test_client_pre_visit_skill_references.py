from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_DIR = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "客户访前一页纸"
)
SKILL_PATH = SKILL_DIR / "SKILL.md"

REFERENCE_FILES = {
    "data-discipline.md": "cisp://skill/client-pre-visit-one-pager/data-discipline",
    "web-evidence-policy.md": "cisp://skill/client-pre-visit-one-pager/web-evidence-policy",
    "tool-binding.md": "cisp://skill/client-pre-visit-one-pager/tool-binding",
    "evidence-model.md": "cisp://skill/client-pre-visit-one-pager/evidence-model",
    "derivation-and-generation-rules.md": "cisp://skill/client-pre-visit-one-pager/derivation-and-generation-rules",
    "report-template.md": "cisp://skill/client-pre-visit-one-pager/report-template",
    "pdf-style.md": "cisp://skill/client-pre-visit-one-pager/pdf-style",
}


class ClientPreVisitSkillReferenceTests(unittest.TestCase):
    def test_skill_is_a_thin_progressive_disclosure_entrypoint(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertLessEqual(len(skill_text.splitlines()), 500)
        self.assertIn("## 渐进式资源加载（强制）", skill_text)
        self.assertIn("## 核心执行顺序", skill_text)
        self.assertNotIn("```markdown", skill_text)
        self.assertNotIn("# 客户访前一页纸（贷款及综合金融营销版）", skill_text)

        for filename in REFERENCE_FILES:
            with self.subTest(filename=filename):
                self.assertIn(f"`references/{filename}`", skill_text)

    def test_all_direct_references_exist_and_declare_unique_future_uris(self) -> None:
        discovered_ids: set[str] = set()

        for filename, resource_id in REFERENCE_FILES.items():
            with self.subTest(filename=filename):
                path = SKILL_DIR / "references" / filename
                self.assertTrue(path.is_file())
                text = path.read_text(encoding="utf-8")
                self.assertIn(f"<!-- resource-id: {resource_id} -->", text)
                self.assertIn("<!-- resource-version: 0-dev -->", text)
                self.assertIn("## 内容索引", text)
                self.assertNotIn("references/", text)
                discovered_ids.add(resource_id)

        self.assertEqual(len(discovered_ids), len(REFERENCE_FILES))

    def test_report_template_keeps_the_fixed_seven_chapter_skeleton(self) -> None:
        template = (SKILL_DIR / "references" / "report-template.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("```markdown", template)
        self.assertIn("### 标题白名单", template)
        for section in (
            "{{D.section_numbers.core}}、核心观点",
            "{{D.section_numbers.summary}}、执行摘要",
            "{{D.section_numbers.profile}}、客户全景画像",
            "{{D.section_numbers.industry}}、产业画像与行业洞察",
            "{{D.section_numbers.marketing}}、定制化营销方案",
            "{{D.section_numbers.risk}}、风险预警与合规提示",
            "{{D.section_numbers.visit}}、拜访建议与话题清单",
        ):
            with self.subTest(section=section):
                self.assertIn(section, template)

        self.assertEqual(template.count("```markdown"), 1)
        self.assertGreaterEqual(len(re.findall(r"\{\{D\.", template)), 20)

    def test_reference_boundaries_keep_critical_rules(self) -> None:
        expected = {
            "data-discipline.md": "开放纳入模式（最高优先级）",
            "web-evidence-policy.md": "定向搜索外部公开资料",
            "tool-binding.md": "p0010058_query_business_basic_deep",
            "evidence-model.md": '"opportunity_register"',
            "derivation-and-generation-rules.md": "生成贷款营销核心观点",
            "report-template.md": "结构纪律",
            "pdf-style.md": "中文字体与加粗渲染（强制）",
        }
        for filename, sentinel in expected.items():
            with self.subTest(filename=filename):
                text = (SKILL_DIR / "references" / filename).read_text(
                    encoding="utf-8"
                )
                self.assertIn(sentinel, text)

    def test_pdf_tables_have_a_hard_minimum_column_width(self) -> None:
        pdf_style = (SKILL_DIR / "references" / "pdf-style.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("所有可见列的硬最小宽度为 **18 mm**", pdf_style)
        self.assertIn("table-layout: fixed; width: 165.9mm", pdf_style)
        self.assertIn("<colgroup><col ...></colgroup>", pdf_style)
        self.assertIn("colWidths=[...]", pdf_style)
        self.assertIn("不得逐字换行", pdf_style)

        allocation_line = next(
            line
            for line in pdf_style.splitlines()
            if line.startswith("执行摘要主要机会 18 / 28")
        )
        allocations = re.findall(
            r"(?:^|；|,|，)([^；，]+?) "
            r"(\d+(?:\.\d+)?(?: / \d+(?:\.\d+)?)+)",
            allocation_line,
        )
        self.assertGreaterEqual(len(allocations), 18)
        for table_name, widths_text in allocations:
            with self.subTest(table=table_name.strip()):
                widths = [float(value) for value in widths_text.split(" / ")]
                self.assertTrue(all(width >= 18 for width in widths))
                self.assertAlmostEqual(sum(widths), 165.9, places=6)


if __name__ == "__main__":
    unittest.main()
