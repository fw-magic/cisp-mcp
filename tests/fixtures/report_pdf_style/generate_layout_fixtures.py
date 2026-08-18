#!/usr/bin/env python3
"""Generate synthetic client-previsit and equity PDF layout fixtures."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from html import escape
from pathlib import Path
from typing import Sequence

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[3]
CLIENT_TOOLKIT_PATH = ROOT / ".agents" / "skills" / "客户访前一页纸" / "scripts" / "report_pdf_toolkit.py"
EQUITY_TOOLKIT_PATH = ROOT / ".agents" / "skills" / "股权结构分析" / "scripts" / "report_pdf_toolkit.py"


def load_toolkit(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载报告内置 PDF 工具：{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


pdfkit = load_toolkit(CLIENT_TOOLKIT_PATH, "client_previsit_pdf_toolkit")

LONG_COMPANY = "华东先进能源装备与数字化供应链科技股份有限公司"


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(cell).replace("\n", "<br>") for cell in row) + " |" for row in rows)
    return "\n".join(lines)


def document(path: Path) -> SimpleDocTemplate:
    path.parent.mkdir(parents=True, exist_ok=True)
    return SimpleDocTemplate(
        str(path),
        pagesize=LETTER,
        leftMargin=pdfkit.MARGIN_LEFT_MM * mm,
        rightMargin=pdfkit.MARGIN_RIGHT_MM * mm,
        topMargin=pdfkit.MARGIN_TOP_MM * mm,
        bottomMargin=pdfkit.MARGIN_BOTTOM_MM * mm,
        allowSplitting=True,
    )


def centered_styles(styles: dict[str, ParagraphStyle]) -> tuple[ParagraphStyle, ParagraphStyle]:
    subtitle = ParagraphStyle(
        "FixtureSubtitle",
        parent=styles["body"],
        fontName=pdfkit.BOLD_ALIAS,
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    centered_meta = ParagraphStyle(
        "FixtureCenteredMeta",
        parent=styles["meta"],
        alignment=TA_CENTER,
    )
    return subtitle, centered_meta


def labelled(label: str, value: str, style: ParagraphStyle) -> Paragraph:
    rendered_value = escape(value).replace("\n", "<br/>")
    return Paragraph(f"<b>{escape(label)}</b>{rendered_value}", style)


def quote_block(text: str, styles: dict[str, ParagraphStyle]) -> Table:
    block = Table(
        [[Paragraph(text, styles["body"])]],
        colWidths=[pdfkit.CONTENT_WIDTH_MM * mm],
        hAlign="LEFT",
    )
    block.setStyle(
        TableStyle(
            [
                ("LINEBEFORE", (0, 0), (0, 0), 2, pdfkit.SECTION_ACCENT_BLUE),
                ("LEFTPADDING", (0, 0), (0, 0), 8),
                ("RIGHTPADDING", (0, 0), (0, 0), 0),
                ("TOPPADDING", (0, 0), (0, 0), 0),
                ("BOTTOMPADDING", (0, 0), (0, 0), 0),
            ]
        )
    )
    return block


def build_client_fixture(pdf_path: Path, markdown_path: Path) -> None:
    styles = pdfkit.make_styles()
    subtitle, centered_meta = centered_styles(styles)
    story: list[object] = [
        Paragraph("对公客户访前一页纸", styles["title"]),
        Paragraph("报告编号：PREVISIT-LAYOUT-20260817 ｜ 生成时间：2026-08-17 10:00:00 ｜ 密级：机密", centered_meta),
        Paragraph(f"客户名称：{LONG_COMPANY}", subtitle),
    ]
    markdown: list[str] = [
        "# 对公客户访前一页纸",
        f"报告编号：PREVISIT-LAYOUT-20260817 ｜ 生成时间：2026-08-17 10:00:00 ｜ 密级：机密\n\n**客户名称：{LONG_COMPANY}**",
    ]

    story.append(Paragraph("一、核心观点", styles["h1"]))
    core = [
        ("1. 企业简介", "该企业聚焦先进能源装备、工业软件与供应链协同服务，形成覆盖研发、制造、交付和售后运维的综合经营基础。"),
        ("2. 重点发展方向", "正在推进高端产线扩建与核心供应商数字化协同，可能形成项目建设、设备更新和交易结算等综合金融需求。"),
        ("3. 风险提示", "扩产计划仍需结合订单、资本开支进度和回款周期核验，避免将公开规划直接视为确定融资需求。"),
        ("4. 拜访目标", "优先核验未来十二个月资本开支、订单回款和核心供应商结算安排，并确认贷款及现金管理合作切入点。"),
    ]
    indented = ParagraphStyle("ClientIndented", parent=styles["body"], firstLineIndent=21)
    for label, value in core:
        story.append(Paragraph(f"<b>{escape(label)}</b>", styles["body"]))
        story.append(Paragraph(escape(value), indented))
    markdown.append("## 一、核心观点\n\n" + "\n\n".join(f"**{label}**\n\n　　{value}" for label, value in core))

    story.append(Paragraph("二、执行摘要", styles["h1"]))
    summary = [
        ("核心特征：", "制造与数字化服务并行，经营链条长，项目制交付与持续运维收入并存。"),
        ("主要机会：", "1、扩产及设备更新可能形成中长期项目融资空间 OPP-01\n2、核心供应商结算协同可能形成供应链金融机会 OPP-02"),
        ("主要风险：", "1、资本开支时点和订单覆盖度尚待核验 RISK-01\n2、长账期项目可能带来阶段性资金占用 RISK-02"),
        ("拜访建议：", "先确认扩产项目的审批与付款计划，再核验订单、回款及增信资源，最后讨论产品组合。"),
    ]
    for label, value in summary:
        story.append(labelled(label, value, styles["body"]))
    markdown.append("## 二、执行摘要\n\n" + "\n\n".join(f"**{label}** {value}" for label, value in summary))

    story.append(Paragraph("三、客户全景画像", styles["h1"]))
    story.append(Paragraph("（一）企业基本信息", styles["h2"]))
    basic_rows = [
        ["企业全称", LONG_COMPANY],
        ["统一社会信用代码", "91310000LAYOUT0001"],
        ["法定代表人", "张明远"],
        ["企业类型", "其他股份有限公司（非上市）"],
        ["注册资本", "123456.789 万元人民币"],
        ["注册地址", "上海市浦东新区先进制造产业园创新大道 1888 号综合研发楼"],
    ]
    story.append(pdfkit.make_table(["项目", "信息"], basic_rows, [35, 130.9], styles, bold_body_cells={(index, 0) for index in range(len(basic_rows))}))
    markdown.append("## 三、客户全景画像\n\n### （一）企业基本信息\n\n" + markdown_table(["项目", "信息"], basic_rows))

    story.append(Paragraph("四、产业画像与行业洞察", styles["h1"]))
    industry_rows = [
        ["设备制造", "订单驱动", "较长", "扩产与设备更新", "关注订单覆盖与验收回款"],
        ["工业软件", "订阅与项目并行", "中等", "研发与交付投入", "关注续费率和项目毛利"],
    ]
    story.append(pdfkit.make_table(["板块", "收入特征", "回款周期", "资金需求", "贷款视角解读"], industry_rows, [27, 35, 29, 38, 36.9], styles))
    markdown.append("## 四、产业画像与行业洞察\n\n" + markdown_table(["板块", "收入特征", "回款周期", "资金需求", "贷款视角解读"], industry_rows))

    story.append(Paragraph("五、定制化营销方案", styles["h1"]))
    story.append(Paragraph("（一）机会台账深化", styles["h2"]))
    opportunity_rows = []
    for index in range(1, 43):
        opportunity_rows.append(
            [
                f"OPP-{index:02d}",
                "贷款机会" if index % 3 == 1 else ("融资线索" if index % 3 == 2 else "综合金融机会"),
                f"第 {index} 条经营动作涉及设备采购、工程付款或供应商协同，需要结合合同、付款节点和项目审批进一步核验。",
                "可能匹配项目贷款、流动资金贷款、票据、保函、现金管理或供应链金融产品族；仅为营销假设。",
                "高｜已核验" if index % 2 else "中｜线索",
            ]
        )
    story.append(pdfkit.make_table(["机会编号", "机会类型", "经营信号与场景", "金融需求与匹配逻辑", "证据标签"], opportunity_rows, [18, 28, 45, 44.9, 30], styles, compact_columns={0, 1, 4}, bold_body_cells={(index, 0) for index in range(len(opportunity_rows))}))
    markdown.append("## 五、定制化营销方案\n\n### （一）机会台账深化\n\n" + markdown_table(["机会编号", "机会类型", "经营信号与场景", "金融需求与匹配逻辑", "证据标签"], opportunity_rows))

    story.append(Paragraph("六、风险预警与合规提示", styles["h1"]))
    risk_rows = []
    for index in range(1, 13):
        risk_rows.append([f"RISK-{index:02d}", "风险观察", f"2026-08-{index:02d}", "中", "公开线索与内部数据仍需围绕订单真实性、回款安排和增信资源进行交叉核验。", "拜访核验"])
    story.append(pdfkit.make_table(["风险编号", "风险类型", "时点", "等级", "事实、边界与影响", "动作"], risk_rows, [18, 27, 40, 20, 35.9, 25], styles, compact_columns={0, 1, 2, 3}, bold_body_cells={(index, 0) for index in range(len(risk_rows))}))
    markdown.append("## 六、风险预警与合规提示\n\n" + markdown_table(["风险编号", "风险类型", "时点", "等级", "事实、边界与影响", "动作"], risk_rows))

    story.append(Paragraph("七、拜访建议与话题清单", styles["h1"]))
    visit_rows = [
        ["资本开支", "财务负责人", "扩产项目未来十二个月付款节奏如何，已取得哪些审批和订单覆盖？", "影响 OPP-01 的融资结构与提款安排"],
        ["供应链协同", "采购负责人", "核心供应商账期、票据使用和对账流程是否存在集中优化空间？", "影响 OPP-02 的供应链金融方案"],
    ]
    story.append(pdfkit.make_table(["话题", "对象", "建议问题", "答案影响"], visit_rows, [30, 50, 60.9, 25], styles))
    markdown.append("## 七、拜访建议与话题清单\n\n" + markdown_table(["话题", "对象", "建议问题", "答案影响"], visit_rows))

    story.append(Paragraph("数据来源", styles["h1"]))
    sources = [["内部", "水滴征信 MCP｜数据日期：2026-08-17"], ["外部", "企业官网与公开披露纯排版测试资料｜发布日期：2026-08-01"]]
    story.append(pdfkit.make_table(["类型", "来源"], sources, [30, 135.9], styles))
    markdown.append("## 数据来源\n\n" + markdown_table(["类型", "来源"], sources))

    story.append(Paragraph("报告使用说明", styles["h1"]))
    usage_style = ParagraphStyle(
        "ClientUsage",
        parent=styles["table"],
        textColor=colors.HexColor("#666666"),
        leftIndent=5.5,
        firstLineIndent=-5.5,
        spaceBefore=0,
        spaceAfter=0,
    )
    usage = [
        "报告目的：本报告仅用于客户经理访前准备和沟通参考，不作为授信审批依据。",
        "信息真实性：测试内容为纯排版夹具，不代表任何真实企业事实。",
        "数据时效性：正式报告须按查询时点重新核验全部资料。",
        "保密义务：接收方应按所在机构制度妥善保管报告。",
    ]
    story.extend(Paragraph("• " + escape(item), usage_style) for item in usage)
    markdown.append("## 报告使用说明\n\n" + "\n".join(f"- {item}" for item in usage))

    document(pdf_path).build(
        story,
        onFirstPage=pdfkit.draw_page_chrome,
        onLaterPages=pdfkit.draw_page_chrome,
    )
    markdown_path.write_text("\n\n".join(markdown) + "\n", encoding="utf-8")


def build_equity_fixture(pdf_path: Path, markdown_path: Path) -> None:
    styles = pdfkit.make_styles()
    subtitle, _ = centered_styles(styles)
    story: list[object] = [
        Paragraph("股权结构穿透分析", styles["title"]),
        Paragraph(LONG_COMPANY, ParagraphStyle("EquitySubtitle", parent=subtitle, fontSize=14, leading=18)),
    ]
    markdown: list[str] = ["# 股权结构穿透分析", f"## {LONG_COMPANY}"]
    meta = [
        ("目标企业：", LONG_COMPANY),
        ("统一社会信用代码：", "91310000LAYOUT0001"),
        ("法定代表人：", "张明远"),
        ("报告类型：", "股权结构穿透 · 控制权核查"),
        ("报告生成：", "2026-08-17 10:00:00"),
        ("审计留档编号：", "SKILL-EQ-91310000LAYOUT0001-20260817"),
        ("穿透方向：", "自下而上（境内运营主体 → 关键中间层 → 自然人 / 尚未完整穿透的境外层级）"),
        ("控制权稳定性：", "相对稳定 · 核心股东持股集中但协议安排仍待核验"),
    ]
    for label, value in meta:
        story.append(labelled(label, value, styles["meta"]))
        markdown.append(f"**{label}** {value}")

    story.append(Paragraph("执行摘要", styles["h1"]))
    conclusion_body = (
        "目标企业当前股权结构基本可识别，52 名直接股东资料完整，第一大股东与三家持股平台构成核心持股群体；"
        "现有股权与控制关系资料指向张明远为实际控制人和最终受益人（7.123456% 直接持股 + 34.567891% 总持股 + 51.234567% 表决权），相关结论已由工商股权与一条控制链条交叉印证；"
        "尚未取得同口径法定披露快照，未对股东名称、持股数及比例作跨时点一致性判断；"
        "2015-01-15 至 2021-07-15 可回溯 7 条合成工商变更，主要涉及注册资本和股东调整，不据此推断融资节奏；"
        "有限合伙、企业法人及自然人共同构成股东结构，员工及产业投资平台的协议安排仍需核验；"
        "股权出质、冻结与担保的最新情况尚待核验，不据此判断不存在相关记录；"
        "按本报告阈值控制权相对稳定，但协议控制、代持及尚未完整穿透的境外层级仍需法律尽调。"
    )
    story.append(quote_block(f"<b>一句话结论：</b>{conclusion_body}", styles))
    summary_rows = [["主体股权清晰度", "直接股东资料完整，机构平台较多", "88%"], ["实控人穿透路径", "控制结论已由一条独立链条交叉印证", "86%"], ["受益所有人锁定", "受益关系仍有一处境外层级待补充", "82%"], ["控制权稳定性", "相对稳定，协议安排待核验", "78%"], ["历史股权演化", "工商变更可回溯，缺少完整历史快照", "72%"], ["一致行动 / 关联交易", "仅形成疑似清单，不作法律认定", "65%"]]
    story.append(pdfkit.make_table(["关键判断", "结论", "置信度"], summary_rows, [46.5, 86.3, 33.1], styles, compact_columns={2}))
    actions = ["核验合伙协议", "复核表决权委托", "获取关联交易合同与流水"]
    story.extend(pdfkit.make_action_list(actions, styles))
    markdown.append("## 执行摘要\n\n> **一句话结论：** " + conclusion_body + "\n\n" + markdown_table(["关键判断", "结论", "置信度"], summary_rows) + "\n\n**建议行动：**\n\n" + "\n".join(f"{index}. {action}" for index, action in enumerate(actions, start=1)))

    story.append(Paragraph("一、数据来源与互证方法", styles["h1"]))
    source_rows = [["工商 / 当前股权", "水滴征信 MCP", "2026-08-17", "多方交叉核验"], ["实控人 / 受益所有人", "控制权与受益所有权资料", "2026-08-17", "与股权链条交叉印证"], ["历史股权变迁", "工商变更记录", "2026-08-17", "人员更替回溯"]]
    story.append(pdfkit.make_table(["数据维度", "数据来源", "采集时间", "互证方式"], source_rows, [36.5, 53.1, 33.2, 43.1], styles, compact_columns={2}))
    story.append(quote_block("股权穿透已至可识别自然人，仍有一处境外控制层级资料尚待补充；所有比例沿用原始口径。", styles))
    markdown.append("## 一、数据来源与互证方法\n\n" + markdown_table(["数据维度", "数据来源", "采集时间", "互证方式"], source_rows))

    story.append(Paragraph("二、穿透起点：核心运营主体基本信息", styles["h1"]))
    basic_rows = [["企业完整登记名", LONG_COMPANY], ["统一社会信用代码", "91310000LAYOUT0001"], ["企业类型", "其他股份有限公司（非上市）"], ["法定代表人", "张明远（董事兼总经理）"], ["注册资本", "123456.789 万元人民币"], ["实缴资本", "98765.4321 万元人民币，口径待复核"], ["总股本", "未披露"], ["成立日期", "2012-03-19"], ["登记机关", "上海市市场监督管理局"], ["登记状态", "存续"], ["注册地址", "上海市浦东新区先进制造产业园创新大道 1888 号综合研发楼"]]
    story.append(pdfkit.make_table(["项目", "内容"], basic_rows, [46.5, 119.4], styles, bold_body_cells={(index, 0) for index in range(len(basic_rows))}))
    markdown.append("## 二、穿透起点：核心运营主体基本信息\n\n" + markdown_table(["项目", "内容"], basic_rows))

    story.append(Paragraph("三、当前股权结构", styles["h1"]))
    story.append(Paragraph("3.1 股东全景（按持股比例降序 · 共 52 名）", styles["h2"]))
    shareholder_rows = []
    for index in range(1, 53):
        ratio = f"{max(0.100000, 31.123456 - index * 0.512345):.6f}%"
        shareholder_rows.append([str(index), f"华东先进制造产业投资合伙企业（有限合伙）第 {index:02d} 号专项平台", ratio, f"{50000 - index * 317}.1234", "有限合伙" if index % 3 else "企业法人", "待穿透；平台治理文件和最终出资人信息需结合合伙协议复核。"])
    story.append(pdfkit.make_table(["#", "股东名称", "持股比例", "认缴 / 持股数（万元）", "股东类型", "备注"], shareholder_rows, [10.0, 46.5, 23.2, 29.9, 24.9, 31.4], styles, compact_columns={0, 2, 3}))
    story.append(labelled("合计：", "共 52 名股东；测试夹具不执行比例合计。", styles["body"]))
    markdown.append("## 三、当前股权结构\n\n### 3.1 股东全景（按持股比例降序 · 共 52 名）\n\n" + markdown_table(["#", "股东名称", "持股比例", "认缴 / 持股数（万元）", "股东类型", "备注"], shareholder_rows))

    story.append(Paragraph("3.2 股东类型分布", styles["h2"]))
    type_rows = [["有限合伙", "35", "员工及产业投资平台"], ["企业法人", "12", "产业资本与集团公司"], ["自然人", "5", "已到穿透终点"]]
    story.append(pdfkit.make_table(["类型", "股东数", "说明"], type_rows, [39.8, 26.5, 99.6], styles, compact_columns={1}))
    story.append(Paragraph("3.3 集中度分析", styles["h2"]))
    concentration_rows = [["第一大股东持股", "30.611111%", "沿用原始口径"], ["前 3 大股东合计", "约 61.234567%", "定点计算"], ["前 5 大股东合计", "约 72.345678%", "定点计算"], ["前 10 大股东合计", "约 83.456789%", "定点计算"]]
    story.append(pdfkit.make_table(["指标", "数值", "说明"], concentration_rows, [49.8, 41.5, 74.6], styles, compact_columns={1}))
    markdown.append("### 3.2 股东类型分布\n\n" + markdown_table(["类型", "股东数", "说明"], type_rows) + "\n\n### 3.3 集中度分析\n\n" + markdown_table(["指标", "数值", "说明"], concentration_rows))

    story.append(Paragraph("四、实际控制人与受益所有人穿透", styles["h1"]))
    story.append(Paragraph("4.1 实控人 / 受益所有人锁定（比例沿用原始口径）", styles["h2"]))
    ubo_rows = [["1", "张明远", "实际控制人 / 最终受益人", "7.123456%", "34.567891%", "51.234567%", "2020-06-30"]]
    story.append(pdfkit.make_table(["序号", "姓名", "角色", "直接持股比例", "总持股比例", "表决权比例", "受益所有权形成日期"], ubo_rows, [11.6, 24.9, 29.9, 24.9, 24.9, 24.9, 24.8], styles, compact_columns={0, 3, 4, 5, 6}))
    story.append(quote_block("说明：现有股权与控制关系资料指向张明远为实际控制人和最终受益人；总持股比例与表决权比例沿用原始口径，仍有一处境外控制层级尚待补充。", styles))
    story.append(Paragraph("4.2 间接控制路径（仅列数据明确显示的中间层）", styles["h2"]))
    path_rows = [["华东能源产业控股有限公司", "30.611111%", "67.890123%", "控制关系资料与工商股权交叉印证"], ["华东先进制造员工持股平台", "12.345678%", "华东产业投资控股集团有限公司通过合伙协议形成治理线索，比例未披露", "仅为治理线索，不等同法律认定"]]
    story.append(pdfkit.make_table(["中间层主体", "该主体在目标企业持股", "实控人对该主体出资 / 控制比例", "控制依据"], path_rows, [51.4, 29.9, 34.8, 49.8], styles, compact_columns={1, 2}))
    story.append(Paragraph("4.3 一致行动人 / 配偶关联（如有披露）", styles["h2"]))
    relation_rows = [["现有资料尚未明确关联自然人", "核心管理层关系未披露", "员工持股平台共同投资关系待复核", "现有资料尚不足以确认一致行动关系，需取得协议或公开披露材料"]]
    story.append(pdfkit.make_table(["关联自然人", "与核心管理层关系", "持股平台关联", "依据"], relation_rows, [29.9, 36.5, 49.8, 49.7], styles))
    markdown.append("## 四、实际控制人与受益所有人穿透\n\n### 4.1 实控人 / 受益所有人锁定（比例沿用原始口径）\n\n" + markdown_table(["序号", "姓名", "角色", "直接持股比例", "总持股比例", "表决权比例", "受益所有权形成日期"], ubo_rows) + "\n\n### 4.2 间接控制路径（仅列数据明确显示的中间层）\n\n" + markdown_table(["中间层主体", "该主体在目标企业持股", "实控人对该主体出资 / 控制比例", "控制依据"], path_rows) + "\n\n### 4.3 一致行动人 / 配偶关联（如有披露）\n\n" + markdown_table(["关联自然人", "与核心管理层关系", "持股平台关联", "依据"], relation_rows))

    story.append(Paragraph("五、历史股权变迁", styles["h1"]))
    story.append(Paragraph("5.1 关键变更时间轴", styles["h2"]))
    history_rows = [[f"20{14 + index:02d}-0{index}-15", "注册资本 / 股东变更", f"变更前记录 {index} → 变更后记录 {index}", "仅列示工商登记中可核验的变更内容"] for index in range(1, 8)]
    story.append(pdfkit.make_table(["变更日期", "变更项", "变更前 → 变更后", "说明"], history_rows, [26.5, 29.9, 59.7, 49.8], styles, compact_columns={0}))
    story.append(Paragraph("5.2 历任法定代表人更替", styles["h2"]))
    legal_rows = [["2018-06-01", "李建国 → 张明远", "工商变更记录"], ["2023-05-18", "张明远 → 张明远", "职务调整，法定代表人未变化"]]
    story.append(pdfkit.make_table(["时间", "变更前 → 变更后", "说明"], legal_rows, [33.2, 69.7, 63.0], styles, compact_columns={0}))
    markdown.append("## 五、历史股权变迁\n\n### 5.1 关键变更时间轴\n\n" + markdown_table(["变更日期", "变更项", "变更前 → 变更后", "说明"], history_rows) + "\n\n### 5.2 历任法定代表人更替\n\n" + markdown_table(["时间", "变更前 → 变更后", "说明"], legal_rows))

    story.append(Paragraph("六、一致行动人与关联关系识别（疑似 · 供人工复核）", styles["h1"]))
    action_rows = [
        ["三家员工持股平台及其普通合伙人", "同一 GP 控制", "共同普通合伙人及交叉任职形成治理关联线索，多条路径最终到达同一控制主体", "核验合伙协议、董事提名与表决权安排"],
        ["产业投资平台 A 与 B 及关联管理人", "共同投资与共同任职", "共同投资两家被投企业且存在人员任职双重联系，不证明存在一致行动协议", "获取协议、董事会材料及定期报告披露"],
        ["区域产业基金与管理公司", "同一控制网络", "投资路径和任职路径均指向同一管理主体，但尚未取得一致行动协议", "访谈管理人并核验治理文件"],
        ["员工持股平台与核心管理层", "共同任职", "主要人员存在交叉任职，尚不足以证明各方在股东会采取一致行动", "核验董事会与股东会表决记录"],
        ["境内机构股东及关联投资平台", "共同投资", "多点关系网络显示共同投资事实，交易安排与表决机制尚待核验", "取得投资协议和定期报告披露"],
        ["历史股东与现任管理人员", "其他关联线索", "工商变更与人员任职记录存在时间交集，仅作为进一步人工复核线索", "核验历史档案与利益冲突申报"],
    ]
    story.append(pdfkit.make_table(["疑似一致行动主体", "证据类型", "证据明细", "复核建议"], action_rows, [41.5, 29.9, 61.4, 33.1], styles))
    story.append(quote_block("一致行动人基于启发式证据推断，不替代法律认定；仅输出疑似清单与证据链。", styles))
    markdown.append("## 六、一致行动人与关联关系识别（疑似 · 供人工复核）\n\n" + markdown_table(["疑似一致行动主体", "证据类型", "证据明细", "复核建议"], action_rows))

    story.append(Paragraph("七、控制权脆弱性评估", styles["h1"]))
    fragility_rows = [["单一最大股东持股", "30.611111%", "相对稳定区间"], ["Top3 股东持股合计", "约 61.234567%", "超过 60%"], ["实控人表决权（综合口径）", "51.234567%", "沿用原始控制权口径"], ["一致行动 / 协议安排", "尚待交叉核验", "需法律尽调"]]
    story.append(pdfkit.make_table(["指标", "本企业实测", "判定"], fragility_rows, [53.1, 49.8, 63.0], styles, compact_columns={1}))
    story.append(labelled("脆弱性结论：", "相对稳定（最大股东 30%–50% 且 Top3 超过 60%）——协议安排仍可能影响控制权。", styles["body"]))
    markdown.append("## 七、控制权脆弱性评估\n\n" + markdown_table(["指标", "本企业实测", "判定"], fragility_rows))

    story.append(Paragraph("八、潜在关联交易风险清单", styles["h1"]))
    risk_rows = [["关联方共同投资", "产业投资平台 A 与 B", "共同投资事实已取得，但未取得交易合同、定价和资金流水，不能认定违规关联交易。", "供尽调复核 · 不替客户决策"], ["高管交叉任职", "两家控股子公司", "董事与财务负责人存在交叉任职，需要核验授权、定价和利益冲突管理。", "供尽调复核 · 不替客户决策"]]
    story.append(pdfkit.make_table(["风险信号", "涉及主体", "描述", "提示"], risk_rows, [33.2, 38.2, 61.4, 33.1], styles))
    story.append(quote_block("仅基于已查得的股权 / 投资 / 关联企业数据列示，不替客户判定是否构成违规关联交易，由法务 / 审计复核。", styles))
    markdown.append("## 八、潜在关联交易风险清单\n\n" + markdown_table(["风险信号", "涉及主体", "描述", "提示"], risk_rows))

    story.append(Paragraph("数据来源与免责声明", styles["h1"]))
    story.append(labelled("数据来源：", "本报告使用纯排版测试数据，采集时间 2026-08-17 10:00:00。", styles["body"]))
    disclaimers = [
        "1. 本夹具包含 52 名合成股东和一处尚未完整穿透的境外层级，仅用于验证多页表格与穿透限制说明。",
        "2. 股权代持 / 协议控制 / 双重股权（AB 股）等特殊安排通常不在公开工商信息中，本报告无法完整识别，须配合客户访谈与合同尽调。",
        "3. 一致行动人识别基于启发式推断，不替代法律认定；正式披露或监管报批场景应由律师出具法律意见。",
        "4. 本报告仅供合规尽调与投资决策参考，不构成投资建议；不评估偿债能力，不建议授信额度，不替代专业判断。",
    ]
    story.append(Paragraph("<b>免责声明：</b>", styles["body"]))
    story.extend(Paragraph(escape(item), styles["body"]) for item in disclaimers)
    markdown.append("## 数据来源与免责声明\n\n**数据来源：** 本报告使用纯排版测试数据，采集时间 2026-08-17 10:00:00。\n\n**免责声明：**\n" + "\n".join(disclaimers))

    document(pdf_path).build(
        story,
        onFirstPage=pdfkit.draw_page_chrome,
        onLaterPages=pdfkit.draw_page_chrome,
    )
    markdown_path.write_text("\n\n".join(markdown) + "\n", encoding="utf-8")


def restrip(value: str) -> str:
    return value.replace("<b>", "").replace("</b>", "")


def main() -> int:
    global pdfkit
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "output" / "pdf" / "tests")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    client_pdf = args.output_dir / "客户访前一页纸-排版测试.pdf"
    client_md = args.output_dir / "客户访前一页纸-排版测试-回退.md"
    equity_pdf = args.output_dir / "股权结构穿透分析-排版测试.pdf"
    equity_md = args.output_dir / "股权结构穿透分析-排版测试-回退.md"
    pdfkit = load_toolkit(CLIENT_TOOLKIT_PATH, "client_previsit_pdf_toolkit_run")
    pdfkit.register_chinese_fonts(required_text="中文粗体常规字体客户访前报告免责声明")
    build_client_fixture(client_pdf, client_md)
    pdfkit = load_toolkit(EQUITY_TOOLKIT_PATH, "equity_pdf_toolkit_run")
    pdfkit.register_chinese_fonts(required_text="中文粗体常规字体股权结构报告免责声明")
    build_equity_fixture(equity_pdf, equity_md)
    print(client_pdf.resolve())
    print(equity_pdf.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
