#!/usr/bin/env python3
"""Generate previsit one-pager PDF reports for two companies using weasyprint."""

import json, os, html
from datetime import datetime
from weasyprint import HTML as WHTML

# ── Paths ──
TOOL_RESULTS_DIR = "/Users/ice/.workbuddy/projects/Users-ice-2work-code-1_mcp-cisp-mcp/185476b9-5c7d-44fa-a023-cb44cca66155/tool-results"
ZT_BD_FILE = os.path.join(TOOL_RESULTS_DIR, "mcp-connector-proxy-cisp-mcp_p0010058_query_business_basic_deep-1785138958213-1a269f.txt")
CMB_BD_FILE = os.path.join(TOOL_RESULTS_DIR, "mcp-connector-proxy-cisp-mcp_p0010058_query_business_basic_deep-1785139041702-5a5699.txt")
CMB_OP_FILE = os.path.join(TOOL_RESULTS_DIR, "mcp-connector-proxy-cisp-mcp_p0050007_p0050008_query_public_opinion_info-1785139212968-d833d1.txt")
OUTPUT_DIR = "/Users/ice/2work/code/1_mcp/cisp-mcp/output/pdf"

QUERY_TIME = "2026-07-27 15:50:21"

# ── CSS (per SKILL.md fixed layout) ──
CSS = """
@page {
    size: Letter;
    margin: 20mm 25mm;
    @bottom-center {
        content: "对公客户访前一页纸 · 第 " counter(page) " 页";
        font-size: 8pt;
        color: #808080;
        font-family: "Songti SC", "STSong", serif;
    }
}
body {
    font-family: "Songti SC", "STSong", "SimSun", serif;
    font-size: 10.5pt;
    line-height: 1.6;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}
h1 {
    font-family: "Heiti SC", "PingFang SC", "Hiragino Sans GB", sans-serif;
    font-size: 18pt;
    text-align: center;
    color: #000;
    margin: 0 0 6pt 0;
    font-weight: bold;
}
.meta-line {
    font-size: 9pt;
    text-align: center;
    color: #555;
    margin: 0 0 4pt 0;
}
.customer-name {
    font-size: 12pt;
    text-align: center;
    font-weight: bold;
    margin: 0 0 12pt 0;
    color: #000;
}
h2 {
    font-family: "Heiti SC", "PingFang SC", "Hiragino Sans GB", sans-serif;
    font-size: 14pt;
    color: #4F81BD;
    margin: 16pt 0 8pt 0;
    font-weight: bold;
    page-break-after: avoid;
}
h3 {
    font-family: "Heiti SC", "PingFang SC", "Hiragino Sans GB", sans-serif;
    font-size: 12pt;
    color: #4F81BD;
    margin: 12pt 0 6pt 0;
    font-weight: bold;
    page-break-after: avoid;
}
p { margin: 4pt 0; }
strong { color: #1a3a5a; }
table {
    width: 165.9mm;
    border-collapse: collapse;
    font-size: 9pt;
    margin: 4pt 0 8pt 0;
    table-layout: fixed;
}
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th, td {
    border: 0.5pt solid #000;
    padding: 3pt 4pt;
    vertical-align: middle;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
th {
    font-weight: bold;
    background-color: #E8EDF3;
    text-align: center;
}
.data-source {
    text-align: center;
    color: #808080;
    font-size: 8pt;
    margin: 4pt 0 12pt 0;
    border-top: 0.5pt solid #808080;
    padding-top: 3pt;
}
.usage-notes {
    margin-top: 16pt;
    font-size: 9pt;
    color: #555;
    border-top: 1pt solid #ccc;
    padding-top: 8pt;
}
.usage-notes p { margin: 3pt 0; }
"""

def esc(text):
    """HTML-escape text."""
    if text is None:
        return ""
    return html.escape(str(text))

def load_bd(filepath):
    """Load business deep JSON and navigate to data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    d = data.get('data', data)
    if 'resultData' in d:
        d = d['resultData']
    if 'data' in d:
        d = d['data']
    return d

def parse_ratio(s):
    try:
        return float(str(s).replace('%', ''))
    except:
        return 0

def build_evidence_zt():
    """Build evidence model for 证通股份有限公司."""
    d = load_bd(ZT_BD_FILE)
    b = d['basicList'][0]

    # Basic info
    basic = [
        ("企业全称", b.get('orgName', '')),
        ("统一社会信用代码", b.get('creditCode', '')),
        ("法定代表人", b.get('legRepName', '')),
        ("登记状态", b.get('orgStatus', '')),
        ("成立日期", b.get('estDate', '')),
        ("企业类型", b.get('orgType', '')),
        ("注册资本", f"{b.get('regCap', '')} {b.get('regCapCur', '').replace('CNY:', '')}".strip()),
        ("注册地址", b.get('regAddr', '')),
        ("所属行业", b.get('industry', '')),
        ("联系电话", b.get('tel', '')),
        ("电子邮箱", b.get('email', '')),
        ("最新年报年度", b.get('ancheYear', '')),
    ]

    # Shareholders (top 15 by ratio)
    sl = d.get('shareholderList', [])
    sl_sorted = sorted(sl, key=lambda x: parse_ratio(x.get('fundedRatio', '0')), reverse=True)
    shareholders = []
    for s in sl_sorted[:15]:
        amt = f"{s.get('subConAmt', '')} {s.get('subConCur', '').replace('CNY:', '').strip()}".strip()
        shareholders.append({
            "name": s.get('shareholderName', ''),
            "ratio": s.get('fundedRatio', ''),
            "amount": amt,
            "type": s.get('shareholderType', ''),
        })

    # Persons (max 8)
    pl = d.get('personList', [])
    people = []
    for p in pl[:8]:
        note = "法定代表人" if p.get('isFr') == 1 or p.get('isFr') == '1' else ""
        people.append({
            "name": p.get('perName', ''),
            "position": p.get('position', ''),
            "note": note,
        })

    # Filiation
    fl = d.get('filiationList', [])
    filiation_names = [f.get('brName', '') for f in fl]

    # Websites
    wl = d.get('websiteOrOnlineList', [])
    websites = list(set(w.get('website', '') for w in wl if w.get('website')))

    # SharePledg
    spl = d.get('sharePledgList', [])

    # Extension dimensions (from previous MCP calls)
    assets = [
        {"type": "商标", "count": "144", "representative": "会客听（第38/36/9类）、ZENIDATA（第42/36类）", "status": "本次首批返回5条"},
        {"type": "专利", "count": "53", "representative": "会议文档同步控制方法、自适应安全矩阵调用方法", "status": "本次首批返回5条"},
        {"type": "软件著作权", "count": "100", "representative": "证通消息中间件ZTMQ V8.1、应用服务器ZTWeb V8.0", "status": "本次首批返回5条"},
        {"type": "作品著作权", "count": "1", "representative": "会客听logo（国作登字-2024-F-00084992）", "status": "本次返回1条"},
        {"type": "ICP备案", "count": "18", "representative": "沪ICP备15010564号，覆盖zenitera.com等域名", "status": "本次首批返回5条"},
        {"type": "行政许可", "count": "17", "representative": "建筑工程施工许可、企业境外投资证书", "status": "本次首批返回5条"},
        {"type": "荣誉资质", "count": "10", "representative": "高新技术企业（2022国家级）、专精特新中小企业（2025省级）", "status": "本次返回10项"},
    ]

    # News (empty for 证通)
    news = []

    # Risks
    risks = [
        {"topic": "股权出质", "result": f"{len(spl)}笔", "detail": "2015-2016年历史出质，质权人均为上银瑞金资本管理有限公司，出质人为公司股东（投资管理合伙企业）", "scope": "目标企业股东层面"},
        {"topic": "失信被执行", "result": "未命中", "detail": "本次查询未返回失信被执行人记录", "scope": "目标企业自身"},
        {"topic": "被执行人", "result": "未命中", "detail": "本次查询未返回被执行人记录", "scope": "目标企业自身"},
        {"topic": "经营异常", "result": "未命中", "detail": "本次查询未返回经营异常记录", "scope": "目标企业自身"},
        {"topic": "严重违法", "result": "未命中", "detail": "本次查询未返回严重违法记录", "scope": "目标企业自身"},
        {"topic": "行政处罚", "result": "未命中", "detail": "本次查询未返回行政处罚记录", "scope": "目标企业自身"},
    ]

    # Visit questions
    visit_questions = [
        {"topic": "主营收入结构", "basis": "经营范围覆盖软件开发、金融信息服务、证券行业联网互通等", "question": "建议核实各项业务收入占比和主要客户"},
        {"topic": "技术商业化进展", "basis": "软件著作权100项，代表产品包括ZTMQ消息中间件、ZTWeb应用服务器", "question": "建议了解核心产品的商业化落地情况和市场占有率"},
        {"topic": "股东治理结构", "basis": f"共{len(sl)}名股东，持股分散，最大股东华林证券持股3.324901%", "question": "建议了解实际经营控制方式和重大事项决策机制"},
        {"topic": "历史股权出质", "basis": f"{len(spl)}笔历史股权出质（2015-2016年），质权人为上银瑞金资本", "question": "建议核实上述出质是否已解除及当前股权状态"},
        {"topic": "资质续期计划", "basis": "高新技术企业（2022）、专精特新中小企业（2025）等资质", "question": "建议了解资质续期安排和后续申报计划"},
    ]

    # Evidence status
    evidence = {
        "successful": ["工商深度", "商标", "专利", "软件著作权", "作品著作权", "ICP备案", "行政许可", "荣誉资质"],
        "empty": ["近期舆情"],
        "failed": [],
        "query_time": QUERY_TIME,
    }

    return {
        "company_name": b.get('orgName', ''),
        "credit_code": b.get('creditCode', ''),
        "basic": basic,
        "people": people,
        "shareholders": shareholders,
        "shareholder_count": len(sl),
        "filiation": filiation_names,
        "websites": websites,
        "assets": assets,
        "news": news,
        "visit_questions": visit_questions,
        "risks": risks,
        "evidence": evidence,
        "core_view": (
            f"{b.get('orgName', '')}成立于{b.get('estDate', '')}，注册资本{b.get('regCap', '')}"
            f"万{b.get('regCapCur', '').replace('CNY:', '').strip()}，法定代表人{b.get('legRepName', '')}，"
            f"企业类型为{b.get('orgType', '')}，所属行业为软件开发，登记状态为{b.get('orgStatus', '')}。"
            f"公司持有商标144项、专利53项、软件著作权100项、作品著作权1项、ICP备案18项、"
            f"行政许可17项、荣誉资质10项。本次查询未返回失信被执行、被执行人、经营异常、"
            f"严重违法或行政处罚记录；存在9笔历史股权出质（2015-2016年），"
            f"质权人均为上银瑞金资本管理有限公司。"
        ),
        "summary": {
            "value_judgment": (
                "证通股份有限公司为非上市软件信息服务企业，存续逾11年，"
                "注册资本251,875.000000万人民币，持有较丰富的知识产权和资质组合，"
                "包括高新技术企业（2022国家级）和专精特新中小企业（2025省级）。"
            ),
            "opportunities": (
                "公司具备证券行业联网互通平台建设资质和金融信息服务能力，"
                "拥有「会客听」「ZENIDATA」等品牌商标，软件著作权覆盖消息中间件、"
                "应用服务器等核心技术组件，可重点了解其在金融科技领域的技术能力和合作诉求。"
            ),
            "risks": (
                "本次查询未返回失信被执行、被执行人、经营异常、严重违法或行政处罚记录。"
                "存在9笔历史股权出质记录（2015-2016年），质权人均为上银瑞金资本管理有限公司，"
                "属成立初期股东融资安排。"
            ),
            "visit_advice": (
                "建议现场核实公司主营收入结构、客户集中度和核心产品商业化进展；"
                "了解研发投入占比和技术团队规模；关注股东结构分散（82名股东，"
                "最大股东持股3.324901%）对公司治理的影响。"
            ),
        },
    }


def build_evidence_cmb():
    """Build evidence model for 招商银行股份有限公司."""
    d = load_bd(CMB_BD_FILE)
    b = d['basicList'][0]

    # Basic info
    basic = [
        ("企业全称", b.get('orgName', '')),
        ("统一社会信用代码", b.get('creditCode', '')),
        ("法定代表人", b.get('legRepName', '')),
        ("登记状态", b.get('orgStatus', '')),
        ("成立日期", b.get('estDate', '')),
        ("企业类型", b.get('orgType', '')),
        ("注册资本", f"{b.get('regCap', '')} {b.get('regCapCur', '').replace('CNY:', '')}".strip()),
        ("注册地址", b.get('regAddr', '')),
        ("所属行业", b.get('industry', '')),
        ("联系电话", b.get('tel', '')),
        ("电子邮箱", b.get('email', '')),
        ("最新年报年度", b.get('ancheYear', '')),
    ]

    # Shareholders (all 10, sorted by ratio)
    sl = d.get('shareholderList', [])
    sl_sorted = sorted(sl, key=lambda x: parse_ratio(x.get('fundedRatio', '0')), reverse=True)
    shareholders = []
    for s in sl_sorted[:15]:
        amt = f"{s.get('subConAmt', '')} {s.get('subConCur', '').replace('CNY:', '').strip()}".strip() if s.get('subConAmt') else "未披露"
        shareholders.append({
            "name": s.get('shareholderName', ''),
            "ratio": s.get('fundedRatio', ''),
            "amount": amt,
            "type": s.get('shareholderType', ''),
        })

    # Persons (max 8)
    pl = d.get('personList', [])
    people = []
    seen_names = set()
    for p in pl:
        name = p.get('perName', '')
        if name in seen_names:
            # Merge positions
            for pp in people:
                if pp['name'] == name:
                    pp['position'] = pp['position'] + "、" + p.get('position', '')
                    break
            continue
        seen_names.add(name)
        note = "法定代表人" if p.get('isFr') == 1 or p.get('isFr') == '1' else ""
        people.append({
            "name": name,
            "position": p.get('position', ''),
            "note": note,
        })
        if len(people) >= 8:
            break

    # Filiation
    fl = d.get('filiationList', [])
    filiation_count = len(fl)
    filiation_sample = [f.get('brName', '') for f in fl[:5]]

    # Websites
    wl = d.get('websiteOrOnlineList', [])
    websites = list(set(w.get('website', '') for w in wl if w.get('website')))

    # SharePledg
    spl = d.get('sharePledgList', [])

    # CaseInfo (administrative penalties)
    cl = d.get('caseInfoList', [])

    # Extension dimensions
    assets = [
        {"type": "商标", "count": "2,186", "representative": "一招大模型系列等", "status": "本次首批返回5条"},
        {"type": "专利", "count": "2,729", "representative": "音频指纹识别方法、装置、终端设备以及存储介质", "status": "本次首批返回5条"},
        {"type": "软件著作权", "count": "49", "representative": "招商银行核心业务系统等", "status": "本次首批返回5条"},
        {"type": "作品著作权", "count": "11", "representative": "招商银行品牌相关作品", "status": "本次首批返回5条"},
        {"type": "ICP备案", "count": "31", "representative": "粤B2-20040591，覆盖cmbchina.com等域名", "status": "本次首批返回5条"},
        {"type": "行政许可", "count": "2,425", "representative": "金融许可证、外汇业务许可证等", "status": "本次首批返回5条"},
        {"type": "荣誉资质", "count": "25", "representative": "财富世界500强、ESG最佳实践100强", "status": "本次返回25项"},
    ]

    # News (from opinion data)
    news = [
        {"date": "2026-07-25", "emotion": "正面", "title": "招商银行获得发明专利授权：\"音频指纹识别方法、装置、终端设备以及存储介质\"", "source": "证券之星"},
        {"date": "2026-07-24", "emotion": "中性", "title": "告别单一LPR时代，企业贷款迎来新锚DR！工行、招行、浦发吃螃蟹，每日定价有多香？", "source": "东方财富网"},
        {"date": "2026-07-24", "emotion": "中性", "title": "记者实探AI信用卡市场反响：行李箱仍比Token受欢迎", "source": "搜狐新闻 APP"},
        {"date": "2026-07-24", "emotion": "中性", "title": "多家上市银行设立市值管理小组，银行板块估值提升加速落地", "source": "金融界"},
        {"date": "2026-07-24", "emotion": "正面", "title": "银行评级上调叠加美元存款利率攀升，银行ETF易方达（516310）催化不断", "source": "金融界"},
    ]

    # Risks
    risks = [
        {"topic": "行政处罚", "result": f"{len(cl)}条", "detail": "处罚机关包括国家金融监督管理总局（2024年理财业务违规）、中国人民银行（2022年违反账户管理等）、中国银监会（2017、2018年内控管理违规）、深圳市国家外汇管理局（2020、2023年外汇业务违规）等", "scope": "目标企业自身"},
        {"topic": "失信被执行", "result": "未命中", "detail": "本次查询未返回失信被执行人记录", "scope": "目标企业自身"},
        {"topic": "被执行人", "result": "未命中", "detail": "本次查询未返回被执行人记录", "scope": "目标企业自身"},
        {"topic": "经营异常", "result": "未命中", "detail": "本次查询未返回经营异常记录", "scope": "目标企业自身"},
        {"topic": "严重违法", "result": "未命中", "detail": "本次查询未返回严重违法记录", "scope": "目标企业自身"},
    ]

    # Visit questions
    visit_questions = [
        {"topic": "合规整改进展", "basis": f"共{len(cl)}条行政处罚记录，最新为2025年金融监管总局", "question": "建议核实各项处罚的整改落实情况"},
        {"topic": "金融科技创新", "basis": "专利2,729项，近期获得音频指纹识别发明专利授权", "question": "建议了解AI和数字金融领域的技术路线和商业化计划"},
        {"topic": "DR定价机制", "basis": "近期舆情显示招行参与企业贷款DR定价创新", "question": "建议了解DR贷款业务试点规模和后续推广计划"},
        {"topic": "市值管理", "basis": "近期舆情显示多家银行设立市值管理小组", "question": "建议了解招行市值管理机制和估值提升举措"},
        {"topic": "AI信用卡业务", "basis": "近期舆情提及AI信用卡市场反响", "question": "建议了解AI信用卡产品设计和市场反馈"},
    ]

    # Evidence status
    evidence = {
        "successful": ["工商深度", "商标", "专利", "软件著作权", "作品著作权", "ICP备案", "行政许可", "荣誉资质", "近期舆情"],
        "empty": [],
        "failed": [],
        "query_time": QUERY_TIME,
    }

    return {
        "company_name": b.get('orgName', ''),
        "credit_code": b.get('creditCode', ''),
        "basic": basic,
        "people": people,
        "shareholders": shareholders,
        "shareholder_count": len(sl),
        "filiation": filiation_sample,
        "filiation_count": filiation_count,
        "websites": websites,
        "assets": assets,
        "news": news,
        "news_total": 647,
        "visit_questions": visit_questions,
        "risks": risks,
        "evidence": evidence,
        "core_view": (
            f"{b.get('orgName', '')}成立于{b.get('estDate', '')}，注册资本{b.get('regCap', '')}"
            f"万{b.get('regCapCur', '').replace('CNY:', '').strip()}，法定代表人{b.get('legRepName', '')}，"
            f"企业类型为{b.get('orgType', '')}，所属行业为商业银行服务，登记状态为{b.get('orgStatus', '')}。"
            f"公司持有商标2,186项、专利2,729项、软件著作权49项、作品著作权11项、"
            f"ICP备案31项、行政许可2,425项、荣誉资质25项。近90天公开舆情647条，"
            f"本次首批返回10条。存在12条行政处罚记录（2015-2025年），"
            f"涉及金融监管、外汇管理等领域。"
        ),
        "summary": {
            "value_judgment": (
                "招商银行为上市商业银行，存续39年，注册资本2,521,984.560100万人民币，"
                "是中国主要商业银行之一。知识产权储备丰富，专利2,729项、商标2,186项，"
                "荣誉资质包括财富世界500强等25项。"
            ),
            "opportunities": (
                "近期舆情显示公司在技术创新方面活跃，获得音频指纹识别方法发明专利授权；"
                "参与企业贷款DR定价机制创新；布局AI信用卡业务。"
                "可重点了解其在金融科技领域的创新战略和合作需求。"
            ),
            "risks": (
                "存在12条行政处罚记录（2015-2025年），处罚机关包括国家金融监督管理总局、"
                "中国人民银行、中国银监会、深圳市国家外汇管理局等，"
                "涉及理财业务违规、外汇业务违规、内控管理等问题。"
            ),
            "visit_advice": (
                "建议现场了解合规整改进展和内控提升措施；"
                "关注金融科技投入产出比和专利转化情况；"
                "了解市值管理小组的运作机制和估值提升策略。"
            ),
        },
    }


def generate_html(ev):
    """Generate full HTML from evidence model."""
    now = datetime.now()
    report_id = f"CP-{now.strftime('%Y%m%d-%H%M%S')}"
    generated_at = now.strftime('%Y-%m-%d %H:%M:%S')
    company = ev['company_name']
    credit_code = ev['credit_code']

    # Basic info table
    basic_rows = ""
    for label, value in ev['basic']:
        if value:
            basic_rows += f"<tr><td style='width:35mm'>{esc(label)}</td><td style='width:130.9mm'>{esc(value)}</td></tr>\n"

    # People table
    people_rows = ""
    for p in ev['people']:
        note = p.get('note', '')
        people_rows += (
            f"<tr><td style='width:38mm'>{esc(p['name'])}</td>"
            f"<td style='width:48mm'>{esc(p['position'])}</td>"
            f"<td style='width:79.9mm'>{esc(note)}</td></tr>\n"
        )

    # Shareholders table
    sh_rows = ""
    for s in ev['shareholders']:
        sh_rows += (
            f"<tr><td style='width:84mm'>{esc(s['name'])}</td>"
            f"<td style='width:32mm'>{esc(s['ratio'])}</td>"
            f"<td style='width:49.9mm'>{esc(s['amount'])}</td></tr>\n"
        )

    # Assets table
    asset_rows = ""
    for a in ev['assets']:
        asset_rows += (
            f"<tr><td style='width:31mm'>{esc(a['type'])}</td>"
            f"<td style='width:24mm'>{esc(a['count'])}</td>"
            f"<td style='width:70mm'>{esc(a['representative'])}</td>"
            f"<td style='width:40.9mm'>{esc(a['status'])}</td></tr>\n"
        )

    # News table
    news_rows = ""
    if ev['news']:
        for n in ev['news']:
            news_rows += (
                f"<tr><td style='width:32mm'>{esc(n['date'])}</td>"
                f"<td style='width:20mm'>{esc(n['emotion'])}</td>"
                f"<td style='width:84mm'>{esc(n['title'])}</td>"
                f"<td style='width:29.9mm'>{esc(n['source'])}</td></tr>\n"
            )
    else:
        news_rows = "<tr><td colspan='4' style='text-align:center'>本次查询未返回相关公开舆情记录</td></tr>"

    # Visit questions table
    vq_rows = ""
    for vq in ev['visit_questions']:
        vq_rows += (
            f"<tr><td style='width:32mm'>{esc(vq['topic'])}</td>"
            f"<td style='width:62mm'>{esc(vq['basis'])}</td>"
            f"<td style='width:71.9mm'>{esc(vq['question'])}</td></tr>\n"
        )

    # Risks table
    risk_rows = ""
    for r in ev['risks']:
        risk_rows += (
            f"<tr><td style='width:34mm'>{esc(r['topic'])}</td>"
            f"<td style='width:29mm'>{esc(r['result'])}</td>"
            f"<td style='width:76mm'>{esc(r['detail'])}</td>"
            f"<td style='width:26.9mm'>{esc(r['scope'])}</td></tr>\n"
        )

    # Filiation summary
    filiation_text = ""
    if 'filiation_count' in ev:
        filiation_text = f"分支机构{ev['filiation_count']}家"
        if ev['filiation']:
            filiation_text += f"（本次首批返回{len(ev['filiation'])}家：{esc('、'.join(ev['filiation']))}等）"
    else:
        filiation_text = f"分支机构{len(ev.get('filiation', []))}家"
        if ev.get('filiation'):
            filiation_text += f"（{esc('、'.join(ev['filiation']))}）"

    # Website summary
    website_text = "、".join(ev.get('websites', [])) if ev.get('websites') else "未披露"

    # News meta
    if 'news_total' in ev:
        news_meta = f"近90天公开舆情共{ev['news_total']}条，本次首批返回10条，以下展示5条代表性记录"
    elif ev['news']:
        news_meta = "以下为近期公开舆情代表性记录"
    else:
        news_meta = "本次查询未返回相关公开舆情记录"

    # Evidence status
    ev_status = ev['evidence']
    successful_str = "、".join(ev_status['successful']) if ev_status['successful'] else "无"
    empty_str = "、".join(ev_status['empty']) if ev_status['empty'] else "无"
    failed_str = "、".join(ev_status['failed']) if ev_status['failed'] else "无"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>{CSS}</style>
</head>
<body>

<h1>对公客户访前一页纸</h1>
<div class="meta-line">报告编号：{report_id} ｜ 生成时间：{generated_at} ｜ 密级：机密</div>
<div class="customer-name">客户名称：{esc(company)}</div>

<h2>一、核心观点</h2>
<p>{esc(ev['core_view'])}</p>

<h2>二、执行摘要</h2>
<p><strong>核心价值判断：</strong>{esc(ev['summary']['value_judgment'])}</p>
<p><strong>主要机会：</strong>{esc(ev['summary']['opportunities'])}</p>
<p><strong>主要风险：</strong>{esc(ev['summary']['risks'])}</p>
<p><strong>拜访建议：</strong>{esc(ev['summary']['visit_advice'])}</p>

<h2>三、客户全景画像</h2>

<h3>（一）企业基本信息</h3>
<table>
<thead><tr><th>项目</th><th>信息</th></tr></thead>
<tbody>
{basic_rows}
</tbody>
</table>
<div class="data-source">水滴 MCP（工商深度）｜查询时间：{QUERY_TIME}</div>

<h3>（二）关键人员信息</h3>
<table>
<thead><tr><th>姓名</th><th>职务</th><th>备注</th></tr></thead>
<tbody>
{people_rows}
</tbody>
</table>
<div class="data-source">水滴 MCP（工商深度）｜查询时间：{QUERY_TIME}</div>

<h3>（三）股权结构与经营网络</h3>
<table>
<thead><tr><th>股东名称</th><th>持股比例</th><th>认缴信息</th></tr></thead>
<tbody>
{sh_rows}
</tbody>
</table>
<p style="font-size:9pt;color:#555;">股东共{ev['shareholder_count']}名，上表按持股比例降序展示前{len(ev['shareholders'])}名。</p>
<p style="font-size:9pt;color:#555;">{filiation_text}。网站：{website_text}。</p>
<div class="data-source">水滴 MCP（工商深度）｜查询时间：{QUERY_TIME}</div>

<h3>（四）无形资产与资质</h3>
<table>
<thead><tr><th>类型</th><th>总量</th><th>首批代表记录</th><th>状态</th></tr></thead>
<tbody>
{asset_rows}
</tbody>
</table>
<p style="font-size:9pt;color:#555;">各维度总量来自分页元数据，本次仅展示首页返回记录，不代表全部。</p>
<div class="data-source">水滴 MCP（商标、专利、软件著作权、作品著作权、ICP备案、行政许可、荣誉资质）｜查询时间：{QUERY_TIME}</div>

<h3>（五）近期公开动态</h3>
<p style="font-size:9pt;color:#555;">{news_meta}。</p>
<table>
<thead><tr><th>日期</th><th>情感</th><th>标题</th><th>来源</th></tr></thead>
<tbody>
{news_rows}
</tbody>
</table>
<div class="data-source">水滴 MCP（近期舆情）｜查询时间：{QUERY_TIME}</div>

<h2>四、拜访核验重点</h2>
<table>
<thead><tr><th>核验主题</th><th>已有事实/数据缺口</th><th>现场建议核实的问题</th></tr></thead>
<tbody>
{vq_rows}
</tbody>
</table>
<div class="data-source">水滴 MCP（综合维度）｜查询时间：{QUERY_TIME}</div>

<h2>五、风险预警与合规提示</h2>
<table>
<thead><tr><th>风险维度</th><th>查询结果</th><th>关键事实</th><th>范围</th></tr></thead>
<tbody>
{risk_rows}
</tbody>
</table>
<div class="data-source">水滴 MCP（工商深度-风险维度）｜查询时间：{QUERY_TIME}</div>

<div class="usage-notes">
<h2 style="font-size:12pt;margin-top:0;">报告使用说明</h2>
<p>- 本报告仅用于客户经理访前准备和沟通参考，不作为授信审批或其他专业决策依据。</p>
<p>- 本报告基于查询时点水滴 MCP 返回的公开数据；空结果、字段缺失和查询失败均不等同于不存在相关事实。</p>
<p>- 关键经营、财务和合作信息应在拜访中由客户经理进一步核实。</p>
<p>- 本报告涉及企业信息，接收方应按所在机构制度妥善保管。</p>
<p style="color:#808080;font-size:8pt;">成功维度：{esc(successful_str)} ｜ 空结果维度：{esc(empty_str)} ｜ 未完成维度：{esc(failed_str)} ｜ 查询时间：{QUERY_TIME}</p>
</div>

</body>
</html>"""

    return html_content


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate 证通
    print("Building evidence model for 证通股份有限公司...")
    ev_zt = build_evidence_zt()
    print(f"  Company: {ev_zt['company_name']}")
    print(f"  Shareholders: {ev_zt['shareholder_count']}")
    print(f"  People: {len(ev_zt['people'])}")
    print(f"  Assets: {len(ev_zt['assets'])}")
    print(f"  News: {len(ev_zt['news'])}")
    print(f"  Risks: {len(ev_zt['risks'])}")

    html_zt = generate_html(ev_zt)
    pdf_path_zt = os.path.join(OUTPUT_DIR, "证通股份有限公司-公司访前一页纸.pdf")
    print(f"Generating PDF: {pdf_path_zt}")
    WHTML(string=html_zt).write_pdf(pdf_path_zt)
    print(f"  Done: {os.path.getsize(pdf_path_zt)} bytes")

    # Generate 招商银行
    print("\nBuilding evidence model for 招商银行股份有限公司...")
    ev_cmb = build_evidence_cmb()
    print(f"  Company: {ev_cmb['company_name']}")
    print(f"  Shareholders: {ev_cmb['shareholder_count']}")
    print(f"  People: {len(ev_cmb['people'])}")
    print(f"  Assets: {len(ev_cmb['assets'])}")
    print(f"  News: {len(ev_cmb['news'])}")
    print(f"  Risks: {len(ev_cmb['risks'])}")

    html_cmb = generate_html(ev_cmb)
    pdf_path_cmb = os.path.join(OUTPUT_DIR, "招商银行股份有限公司-公司访前一页纸.pdf")
    print(f"Generating PDF: {pdf_path_cmb}")
    WHTML(string=html_cmb).write_pdf(pdf_path_cmb)
    print(f"  Done: {os.path.getsize(pdf_path_cmb)} bytes")

    print("\n=== Both PDFs generated successfully ===")


if __name__ == "__main__":
    main()
