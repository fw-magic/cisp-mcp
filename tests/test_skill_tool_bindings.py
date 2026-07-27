from __future__ import annotations

import unittest
from pathlib import Path

from cisp_mcp import server


SKILL_PATH = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "shuidi-company-previsit-one-pager"
    / "SKILL.md"
)

EXPECTED_BINDINGS = {
    "p0010068_fuzzy_search_company_name": {"ent_name"},
    "p0010058_query_business_basic_deep": {
        "ent_name",
        "credit_code",
        "reg_no",
        "org_code",
    },
    "p0010073_query_trademark_info": {"ent_info"},
    "p0010078_query_patent_info": {"ent_info"},
    "p0010074_query_software_copyright_info": {"ent_info"},
    "p0010075_query_work_copyright_info": {"ent_info"},
    "p0010076_query_icp_filing_info": {"ent_info"},
    "p0010084_query_license_info": {"ent_info"},
    "p0110003_query_honor_qualification_info": {"ent_info"},
    "p0050007_p0050008_query_public_opinion_info": {"ent_name"},
}


def parse_tool_binding_rows(skill_text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in skill_text.splitlines():
        if not line.startswith("|") or "`" not in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 3:
            continue
        tool_cell = cells[1]
        if not (tool_cell.startswith("`") and tool_cell.endswith("`")):
            continue
        rows[tool_cell.strip("`")] = cells[2]
    return rows


class SkillToolBindingTests(unittest.IsolatedAsyncioTestCase):
    async def test_documented_parameters_match_mcp_tool_schemas(self) -> None:
        rows = parse_tool_binding_rows(SKILL_PATH.read_text(encoding="utf-8"))
        tools = {tool.name: tool for tool in await server.mcp.list_tools()}

        for tool_name, expected_parameters in EXPECTED_BINDINGS.items():
            with self.subTest(tool=tool_name):
                self.assertIn(tool_name, rows)
                self.assertIn(tool_name, tools)

                documented_row = rows[tool_name]
                schema_properties = tools[tool_name].inputSchema["properties"]
                for parameter in expected_parameters:
                    self.assertIn(parameter, documented_row)
                    self.assertIn(parameter, schema_properties)

    def test_ent_info_and_ent_name_are_not_cross_documented(self) -> None:
        rows = parse_tool_binding_rows(SKILL_PATH.read_text(encoding="utf-8"))

        ent_info_tools = {
            "p0010073_query_trademark_info",
            "p0010078_query_patent_info",
            "p0010074_query_software_copyright_info",
            "p0010075_query_work_copyright_info",
            "p0010076_query_icp_filing_info",
            "p0010084_query_license_info",
            "p0110003_query_honor_qualification_info",
        }
        for tool_name in ent_info_tools:
            with self.subTest(tool=tool_name):
                self.assertNotIn("ent_name", rows[tool_name])

        no_ent_info_tools = {
            "p0010068_fuzzy_search_company_name",
            "p0010058_query_business_basic_deep",
            "p0050007_p0050008_query_public_opinion_info",
        }
        for tool_name in no_ent_info_tools:
            with self.subTest(tool=tool_name):
                self.assertNotIn("ent_info", rows[tool_name])

        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertNotIn(
            "所有扩展查询工具不接受 `ent_name`",
            skill_text,
        )


if __name__ == "__main__":
    unittest.main()
