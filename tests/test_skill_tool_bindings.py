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
    "p0010010_query_business_profile": {"ent_info"},
    "p0980006_query_advanced_company_filter": {
        "eid",
        "page_no",
        "page_size",
    },
    "p0010059_query_business_basic_brief": {
        "ent_name",
        "credit_code",
        "types",
    },
    "p0980033_query_listing_financing_bidding_ipr": {"ent_info"},
    "p0980008_query_tax_rating": {"eid"},
    "p0980023_query_two_year_risk_summary": {"eid"},
    "p0130036_query_land_info": {
        "ent_info",
        "land_type",
        "page_no",
        "page_size",
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


def extract_report_template(skill_text: str) -> str:
    return skill_text.split("```markdown", 1)[1].split("```", 1)[0]


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
            "p0010010_query_business_profile",
            "p0980033_query_listing_financing_bidding_ipr",
            "p0130036_query_land_info",
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
            "p0010059_query_business_basic_brief",
            "p0980006_query_advanced_company_filter",
            "p0980008_query_tax_rating",
            "p0980023_query_two_year_risk_summary",
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

    def test_company_overview_replaces_model_generated_core_view(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertNotIn("core_view", skill_text)
        self.assertNotIn("简述：", skill_text)
        self.assertIn("{{D.company_overview}}", skill_text)
        self.assertIn('"company_overview": "按固定字段和固定顺序确定性拼接', skill_text)
        self.assertIn("`D.company_overview` 不由大模型生成", skill_text)
        self.assertIn("确保最终至少输出“{企业名称}。”", skill_text)

    def test_company_overview_documents_fixed_segment_order(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        headings = [
            "#### 4.1 基本信息片段",
            "#### 4.2 上市、退市或融资片段",
            "#### 4.3 招投标和知识产权片段",
            "#### 4.4 纳税片段",
            "#### 4.5 近两年风险片段",
        ]

        positions = [skill_text.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("财务片段固定不构建", skill_text)

    def test_company_overview_documents_risk_fields_in_order(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        risk_section = skill_text.split("#### 4.5 近两年风险片段", 1)[1]
        risk_section = risk_section.split("### 5. 生成大模型派生文案", 1)[0]
        fields = [
            "collect15",
            "collect1",
            "collect2",
            "collect3",
            "collect4",
            "collect5",
            "collect7",
            "collect10",
            "collect8",
            "collect9",
            "collect11",
            "collect12",
            "collect13",
        ]

        positions = [risk_section.index(f"`{field}`") for field in fields]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("`collect6`", risk_section)
        self.assertNotIn("`collect14`", risk_section)
        self.assertIn("非数字、产品空结果或调用失败时跳过", risk_section)

    def test_company_overview_uses_natural_lossless_display_rules(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        overview_section = skill_text.split("#### 4.1 基本信息片段", 1)[1]
        overview_section = overview_section.split(
            "### 5. 生成大模型派生文案",
            1,
        )[0]

        self.assertIn("企业名称和左括号之间不得出现逗号", overview_section)
        self.assertIn("企业规模为{entScaleName}", overview_section)
        self.assertIn("所属行业为{行业}", overview_section)
        self.assertIn("`groupName` 不进入核心观点", overview_section)
        self.assertNotIn("是一家隶属于{groupName}", overview_section)
        self.assertNotIn("企业属于{行业}", overview_section)
        self.assertIn("纯数字整数部分增加千分位", skill_text)
        self.assertIn("严格匹配 `YYYY-MM-DD`", skill_text)
        self.assertIn("必须保留全部有效数字和小数位", skill_text)

    def test_company_overview_separates_positive_and_zero_risks(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        risk_section = skill_text.split("#### 4.5 近两年风险片段", 1)[1]
        risk_section = risk_section.split("### 5. 生成大模型派生文案", 1)[0]

        self.assertIn("生成“{风险名称}{原值}条”", risk_section)
        self.assertIn("只登记到 `D.risk_zero_dimensions`", risk_section)
        self.assertIn("公开资料未披露案件或事项明细", risk_section)
        self.assertIn("近两年公开统计显示", risk_section)
        self.assertNotIn("生成“存在{原值}条{风险名称}”", risk_section)
        self.assertNotIn("生成“无{风险名称}”", risk_section)

    def test_legal_representative_fallback_is_documented(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "`B.personList` 为空但 `B.basicList[0].legRepName` 非空时",
            skill_text,
        )
        self.assertIn(
            "工商登记载明法定代表人为{name}；公开资料未披露其履历、决策权限和具体分工",
            skill_text,
        )
        self.assertIn("`position` 已包含“法定代表人”时", skill_text)

    def test_compact_report_tables_and_business_coverage_summary(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "## {{D.section_numbers.needs}}、需求识别与拜访核验",
            skill_text,
        )
        self.assertIn("### （一）需求线索核验", skill_text)
        self.assertIn("| 核验主题 | 已知依据与现场问题 |", skill_text)
        self.assertIn("| 类型 | 数量 | 代表记录 |", skill_text)
        self.assertIn("| 指标 | 本次数据 | 数据口径 |", skill_text)
        self.assertIn("| 风险维度 | 关键事实 | 范围与待核实事项 |", skill_text)
        self.assertIn("资料范围：{{D.coverage_summary}}", skill_text)
        self.assertIn(
            "`D.coverage_summary` 只用工商登记、股权、土地资产、知识产权",
            skill_text,
        )
        self.assertNotIn("六、需求识别与产品推荐", skill_text)
        self.assertNotIn("| 需求类型 | 识别依据 | 紧迫度 |", skill_text)
        self.assertNotIn("| 类型 | 数量 | 核心内容 | 取得方式 |", skill_text)
        self.assertNotIn("| 指标 | 数据 | 行业参考 | 评价 |", skill_text)
        self.assertNotIn("| 风险维度 | 本次结果 | 关键事实 | 范围 |", skill_text)
        self.assertNotIn("认缴出资额（接口原值）", skill_text)
        self.assertNotIn("本次不评级", skill_text)

    def test_report_template_uses_business_language(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        report_template = extract_report_template(skill_text)
        forbidden_terms = [
            "返回",
            "未取得",
            "取得",
            "查询成功",
            "查询失败",
            "首批返回",
            "本次查询",
            "接口",
            "字段",
            "空结果",
            "统计口径",
            "查询时间",
        ]

        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, report_template)

        self.assertIn("数据日期：{{META.generated_at}}", report_template)
        self.assertIn("资料范围：{{D.coverage_summary}}", report_template)
        self.assertIn("公开资料未披露", skill_text)
        self.assertIn("商业事件中的“取得订单”改写为“获得订单”", skill_text)

    def test_analysis_uses_information_interpretation_and_evidence_bounds(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        report_template = extract_report_template(skill_text)
        core_section = report_template.split(
            "## {{D.section_numbers.core}}、核心观点",
            1,
        )[1]
        core_section = core_section.split(
            "## {{D.section_numbers.summary}}、执行摘要",
            1,
        )[0]

        self.assertNotIn("信息解读：", core_section)
        self.assertNotIn("AI辅助分析", skill_text)
        self.assertEqual(report_template.count("**信息解读：**"), 7)
        self.assertIn("**信息解读：** {{D.basic_interpretation}}", report_template)
        self.assertIn("**信息解读：** {{D.people_interpretation}}", report_template)
        self.assertIn("**信息解读：** {{D.equity_interpretation}}", report_template)
        self.assertIn("**信息解读：** {{D.assets_interpretation}}", report_template)
        self.assertIn("**信息解读：** {{D.operations_interpretation}}", report_template)
        self.assertIn("**信息解读：** {{D.risk_interpretation}}", report_template)
        self.assertIn(
            "**信息解读：** 以下核验主题根据报告所列事实和信息缺口整理",
            report_template,
        )
        self.assertIn(
            "事实综合 → 可能的业务含义 → 拜访核验方向",
            skill_text,
        )
        self.assertIn("可能表明", skill_text)
        self.assertIn("所有总结分析必须同时包含事实依据", skill_text)
        self.assertIn("不得复制思迈特样稿中的强判断、估算值或模拟数据", skill_text)

    def test_skill_uses_natural_pagination_without_keep_together_guards(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("允许这些内容随页面剩余空间自然续页", skill_text)
        self.assertIn("较长单元格可跨页拆分", skill_text)
        self.assertIn("不使用 `KeepTogether`", skill_text)
        self.assertIn("不因避免断句、孤立标题或来源文字而主动移动整块内容", skill_text)
        self.assertIn("当前页空白超过可用正文区约三分之一", skill_text)
        self.assertNotIn("表头和 2 条数据", skill_text)
        self.assertNotIn("4 行以内的信息解读整段不得跨页", skill_text)
        self.assertNotIn("作为连续版式组", skill_text)
        self.assertNotIn("不得以断句残片", skill_text)

    def test_body_weight_and_bold_business_labels(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        report_template = extract_report_template(skill_text)

        self.assertIn("黑色正文必须使用宋体或等价中文宋体的常规字重", skill_text)
        self.assertIn("字体名含 `Black`、`Bold`、`Semibold`", skill_text)
        self.assertIn(
            "仅主标题、客户名称、蓝色章节标题、表头行、执行摘要的",
            skill_text,
        )
        self.assertIn("除明确允许加粗的标题、标签和表格标签项外", skill_text)
        self.assertIn("**核心价值判断：**", report_template)
        self.assertIn("**主要机会：**", report_template)
        self.assertIn("**主要风险：**", report_template)
        self.assertIn("**拜访建议：**", report_template)
        self.assertIn("**信息解读：**", report_template)
        self.assertIn("| **企业全称** |", report_template)
        self.assertIn("| **专利** |", report_template)
        self.assertIn("| **员工规模** |", report_template)
        self.assertIn("| **{{topic}}** |", report_template)
        self.assertIn("| {{name}} | {{ratio_display}} |", report_template)
        self.assertIn("- {{name}}：", report_template)
        self.assertNotIn("**{{B.basicList[0].orgName}}**", report_template)
        self.assertNotIn("**{{name}}**", report_template)
        self.assertNotIn("**报告目的：**", report_template)
        self.assertIn("| 项目 | 内容 |", report_template)

    def test_spacing_uses_styles_without_blank_pdf_paragraphs(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("所有 `##` 一级标题段前 12 pt、段后 6 pt", skill_text)
        self.assertIn("标题位于页首时不额外增加段前空白", skill_text)
        self.assertIn("普通正文段落段后 4 pt", skill_text)
        self.assertIn("PDF 使用段后样式控制间距，不插入空白段落", skill_text)
        self.assertIn("Markdown 回退在自然段之间保留一个空行", skill_text)

    def test_top_level_sections_are_dynamically_and_contiguously_numbered(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        report_template = extract_report_template(skill_text)

        self.assertIn('"section_numbers": {', skill_text)
        self.assertIn(
            "当前骨架固定得到核心观点“一”、执行摘要“二”、客户全景画像“三”、需求识别与拜访核验“四”；风险章节显示时为“五”",
            skill_text,
        )
        self.assertIn(
            "## {{D.section_numbers.core}}、核心观点",
            report_template,
        )
        self.assertIn(
            "## {{D.section_numbers.summary}}、执行摘要",
            report_template,
        )
        self.assertIn(
            "## {{D.section_numbers.profile}}、客户全景画像",
            report_template,
        )
        self.assertIn(
            "## {{D.section_numbers.needs}}、需求识别与拜访核验",
            report_template,
        )
        self.assertIn(
            "## {{D.section_numbers.risk}}、风险预警与合规提示",
            report_template,
        )
        self.assertNotIn("## 六、需求识别与拜访核验", skill_text)
        self.assertNotIn("## 七、风险预警与合规提示", skill_text)
        self.assertIn("不得跳号、重号", skill_text)
        self.assertIn("小节“（一）～（五）”不参与重编号", skill_text)

    def test_p0980033_prefers_verified_ent_id(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "`P0980033` 的 `ent_info` 优先传已核验的 `entId`",
            skill_text,
        )
        self.assertIn(
            "无法取得 `entId` 时回退规范企业全称",
            skill_text,
        )

    def test_land_asset_queries_are_category_scoped_and_paginated(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        binding_rows = parse_tool_binding_rows(skill_text)
        land_binding = binding_rows["p0130036_query_land_info"]

        self.assertIn('land_type="tdgy"', land_binding)
        self.assertIn('"tdcr"', land_binding)
        self.assertIn('"tddy"', land_binding)
        self.assertIn('page_no="1"', land_binding)
        self.assertIn('page_size="10"', land_binding)
        self.assertIn("默认不查询 `dkgs`", land_binding)

        self.assertIn("`detailListMeta.tdgyPageNum`", skill_text)
        self.assertIn("`detailListMeta.tdcrPageNum`", skill_text)
        self.assertIn("`detailListMeta.tddyPageNum`", skill_text)
        self.assertIn("不得使用聚合的 `totalPage`", skill_text)
        self.assertIn("土地供应、土地出让、土地抵押分别进入 `META`", skill_text)

    def test_land_alias_and_required_fields_are_documented(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("| `LAND` | `p0130036_query_land_info.data`", skill_text)
        self.assertIn('"LAND": {', skill_text)
        self.assertIn('"tdgy": {"status": "success|empty|failed"', skill_text)
        self.assertIn('"tdcr": {"status": "success|empty|failed"', skill_text)
        self.assertIn('"tddy": {"status": "success|empty|failed"', skill_text)

        required_fields = [
            "`B.basicList[0].industryClas`, `industry`, `operateScope`, `regAddr`",
            "`supplyArea`, `transactionPrice`, `contractDate`, `yearLimit`",
            "`landArea`, `transactionPrice`, `pubDate`, `yearLimit`, `landNo`",
            "`mortgageAcreage`, `mortgagePrice`, `mortgagorName`, `mortgageName`",
        ]
        for fields in required_fields:
            with self.subTest(fields=fields):
                self.assertIn(fields, skill_text)

    def test_tangible_asset_generation_is_deterministic_and_bounded(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        rules = skill_text.split("#### 有形资产生成规则", 1)[1]
        rules = rules.split("### 4. 构建确定性企业简述", 1)[0]

        ordered_segments = [
            "经营及地址背景",
            "土地供应",
            "土地出让",
            "土地抵押",
            "信息边界",
        ]
        order_text = " → ".join(ordered_segments)
        self.assertIn(order_text, rules)
        self.assertIn("JSON 内容完全一致的重复对象", rules)
        self.assertIn("不得跨土地供应、土地出让和土地抵押类别合并或去重", rules)
        self.assertIn("`supplyArea` 从大到小", rules)
        self.assertIn("`landArea` 从大到小", rules)
        self.assertIn("优先按有效 `pubDate`，再按 `boardStartDate`", rules)
        self.assertIn("`D.tangible_assets` 或任一无形资产事实非空", rules)
        self.assertIn(
            "`D.company_overview`、`D.tangible_assets` 和事实表格不属于模型派生分析",
            skill_text,
        )

    def test_land_totals_require_complete_consistent_decimal_inputs(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        rules = skill_text.split("#### 有形资产生成规则", 1)[1]
        rules = rules.split("### 4. 构建确定性企业简述", 1)[0]

        self.assertIn("类别分页已从第 1 页完整获取到类别页数", rules)
        self.assertIn("合并去重后的记录数与对应", rules)
        self.assertIn("字段单位完全一致", rules)
        self.assertIn("任意精度十进制加法", rules)
        self.assertIn("禁止二进制浮点、舍入、换算或补零", rules)
        self.assertIn("不得跨类别合计", rules)
        self.assertIn("不得使用 `dkgsResults[]` 参与任何合计", rules)
        self.assertIn("任一条件不满足时省略该合计", rules)

    def test_tangible_assets_avoid_ownership_and_zero_risk_inferences(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        rules = skill_text.split("#### 有形资产生成规则", 1)[1]
        rules = rules.split("### 4. 构建确定性企业简述", 1)[0]

        self.assertIn("不得称为当前产权、当前持有土地或自有土地", rules)
        self.assertIn("不能单独证明企业拥有土地、房屋、厂房或设备", rules)
        self.assertIn("公开资料中暂无可供展示的相关记录", rules)
        self.assertIn("房屋产权、厂房及设备账面净值、租赁安排等仍需结合", rules)
        for forbidden_claim in [
            "“无抵押”",
            "“无查封”",
            "“轻资产”",
            "“自有房产”",
            "“自有厂房”",
            "“办公场所租赁”",
        ]:
            with self.subTest(claim=forbidden_claim):
                self.assertIn(forbidden_claim, rules)

        self.assertIn(
            '"tangible_assets": ["实际使用的 B.basicList[0] 与 LAND 字段',
            skill_text,
        )
        self.assertIn(
            "`D.coverage_summary` 只用工商登记、股权、土地资产、知识产权",
            skill_text,
        )

    def test_skill_targets_current_twenty_five_tool_server(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("当前 25 工具版本", skill_text)
        self.assertIn("**SKILL 版本**：v1.9", skill_text)


if __name__ == "__main__":
    unittest.main()
