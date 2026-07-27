#!/usr/bin/env python3
"""Generate a multi-page A4 PDF enterprise profile using fpdf2 with Chinese support."""

from fpdf import FPDF
import os

EFF_W = 170  # effective width in mm (A4 210 - 40 margins)

class EnterpriseProfilePDF(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
        self.font_regular = None
        self.font_bold = None
        for fp in font_paths:
            if os.path.exists(fp):
                self.add_font("CN", "", fp)
                self.add_font("CN", "B", fp)
                self.font_regular = "CN"
                self.font_bold = "CN"
                break
        if not self.font_regular:
            raise RuntimeError("No Chinese font found on this system")
        self.set_auto_page_break(True, 20)

    def header(self):
        if self.page_no() > 1:
            self.set_font(self.font_regular, "", 7)
            self.set_text_color(150, 150, 150)
            self.cell(EFF_W, 5, "CISP 企业画像 · 证通股份有限公司（续）", align="R")
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_regular, "", 7)
        self.set_text_color(150, 150, 150)
        self.cell(EFF_W, 10, f"第 {self.page_no()} 页", align="C")

    def title_block(self, text):
        self.set_font(self.font_bold, "", 18)
        self.set_text_color(30, 58, 95)
        self.cell(EFF_W, 12, text)
        self.ln(10)
        self.set_draw_color(37, 99, 235)
        self.set_line_width(0.6)
        self.line(self.l_margin, self.get_y(), self.l_margin + EFF_W, self.get_y())
        self.ln(6)

    def section_title(self, text):
        self.set_font(self.font_bold, "", 12)
        self.set_text_color(37, 99, 235)
        self.cell(EFF_W, 9, text)
        self.ln(7)
        self.set_draw_color(203, 213, 225)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.l_margin + EFF_W, self.get_y())
        self.ln(4)

    def bullet(self, label, value, size=9):
        """Render a bold label + regular value on one or more lines."""
        self.set_font(self.font_regular, "", size)
        self.set_text_color(34, 34, 34)

        # try to fit on one line first
        w_label = self.get_string_width(label)
        # If it fits, render on same line
        full_text = label + value
        if self.get_string_width(full_text) <= EFF_W:
            self.set_font(self.font_bold, "", size)
            self.set_text_color(30, 58, 95)
            self.cell(w_label, 5.5, label)
            self.set_font(self.font_regular, "", size)
            self.set_text_color(34, 34, 34)
            self.cell(EFF_W - w_label, 5.5, value)
            self.ln(6)
        else:
            # Bold label on its own line
            self.set_font(self.font_bold, "", size)
            self.set_text_color(30, 58, 95)
            self.cell(EFF_W, 5.5, label)
            self.ln(6)
            # Value on next line(s)
            self.set_font(self.font_regular, "", size)
            self.set_text_color(34, 34, 34)
            self.multi_cell(EFF_W, 5.5, value)
            self.ln(1)

    def body_text(self, text, size=9):
        self.set_font(self.font_regular, "", size)
        self.set_text_color(34, 34, 34)
        self.multi_cell(EFF_W, 5.5, text)
        self.ln(1)

    def simple_table(self, headers, rows, col_widths):
        # Ensure col_widths sum fits EFF_W
        total_w = sum(col_widths)
        if total_w > EFF_W:
            scale = EFF_W / total_w
            col_widths = [w * scale for w in col_widths]

        # header
        self.set_fill_color(37, 99, 235)
        self.set_text_color(255, 255, 255)
        self.set_font(self.font_regular, "", 9)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=0, fill=True, align="L")
        self.ln()

        # rows
        for ri, row in enumerate(rows):
            if ri % 2 == 0:
                self.set_fill_color(248, 250, 252)
            else:
                self.set_fill_color(255, 255, 255)
            self.set_text_color(34, 34, 34)
            self.set_font(self.font_regular, "", 8.5)

            # Calculate max height needed
            max_lines = 1
            for i, cell_text in enumerate(row):
                lines = self.multi_cell(col_widths[i], 6.5, str(cell_text), dry_run=True, output="LINES")
                max_lines = max(max_lines, len(lines))

            row_h = max_lines * 6.5

            # Check page break
            if self.get_y() + row_h > self.h - self.b_margin:
                self.add_page()
                y_before = self.get_y()
                # redo header
                self.set_fill_color(37, 99, 235)
                self.set_text_color(255, 255, 255)
                self.set_font(self.font_regular, "", 9)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], 7, h, border=0, fill=True, align="L")
                self.ln()
                self.set_fill_color(248, 250, 252)
                self.set_text_color(34, 34, 34)
                self.set_font(self.font_regular, "", 8.5)

            y_start = self.get_y()
            x_start = self.get_x()

            for i, cell_text in enumerate(row):
                # Draw fill background
                self.set_fill_color(248, 250, 252) if ri % 2 == 0 else self.set_fill_color(255, 255, 255)
                self.rect(x_start + sum(col_widths[:i]), y_start, col_widths[i], row_h, "F")

                self.set_xy(x_start + sum(col_widths[:i]), y_start)
                self.set_font(self.font_regular, "", 8.5)
                self.set_text_color(34, 34, 34)
                self.multi_cell(col_widths[i], 6.5, str(cell_text))

            self.set_xy(x_start, y_start + row_h)
        self.ln(3)

    def check_page_break(self, needed_mm=30):
        if self.get_y() > self.h - self.b_margin - needed_mm:
            self.add_page()


def generate():
    pdf = EnterpriseProfilePDF()
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.add_page()

    # ---- Title ----
    pdf.title_block("证通股份有限公司｜企业一页纸画像")

    # ---- Meta line ----
    pdf.set_font(pdf.font_regular, "", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(EFF_W, 5, "统一社会信用代码：91310000324360627T  查询日期：2026-07-27  模式：标准版")
    pdf.ln(5)
    pdf.cell(EFF_W, 5, "报告编号：CISP-CP-91310000324360627T-20260727-104538  数据源：CISP MCP")
    pdf.ln(8)

    # ---- 1. 执行摘要 ----
    pdf.section_title("1. 执行摘要")
    pdf.bullet("• 主体状态：", "在营（开业），截至 2026-04-08 最近核准登记")
    pdf.bullet("• 业务定位：", "软件开发、金融信息服务、证券行业联网互通平台建设、互联网数据服务等")
    pdf.bullet("• 规模与年限：", "成立于 2015-01-08，存续逾 11 年；注册资本 251,875 万元人民币")
    pdf.bullet("• 核心资产：", "商标 144 项、专利 53 项、软著 100 项、作品著作权 1 项、许可 17 项、荣誉资质 10 项、ICP 备案 18 项")
    pdf.bullet("• 关注事项：", "本次查询未返回行政处罚、经营异常、失信被执行等负面记录；存在 9 笔历史股权出质（2015-2016 年），均为成立初期事项")
    pdf.ln(3)

    # ---- 2. 主体与经营 ----
    pdf.section_title("2. 主体与经营")
    pdf.simple_table(
        ["项目", "信息"],
        [
            ["法定代表人", "范宇"],
            ["企业类型", "其他股份有限公司（非上市）"],
            ["成立日期", "2015-01-08"],
            ["注册资本", "251,875 万元人民币"],
            ["注册地址", "上海市浦东新区金葵路118号3-7层"],
            ["登记机关", "上海市市场监督管理局"],
            ["所属行业", "软件和信息技术服务业-应用软件开发（6513）"],
            ["经营期限", "2015-01-08 至 长期"],
            ["联系电话", "021-20538888"],
            ["电子邮箱", "public@zenitera.com"],
        ],
        [30, 140],
    )

    pdf.body_text(
        "经营范围摘要：许可项目含第一类、第二类增值电信业务。一般项目覆盖软件开发、软件外包、互联网安全、信息系统集成、工业互联网数据服务、大数据处理、物联网技术、金融信息服务、证券行业联网互通平台建设、计算机软硬件批发零售、投资与资产管理、电子商务等。",
        size=8.5,
    )

    # ---- 3. 股权与治理 ----
    pdf.section_title("3. 股权与治理")
    pdf.body_text("股东概览：含合伙企业、企业法人和自然人股东，持股比例分散，无单一股东绝对控股。代表项：", size=9)
    pdf.ln(1)
    pdf.simple_table(
        ["股东", "类型", "出资比例", "认缴金额"],
        [
            ["华林证券股份有限公司", "企业法人", "3.324901%", "11,500 万元"],
            ["上海勍瑞投资管理合伙企业", "企业法人", "1.933502%", "6,687.5 万元"],
            ["上海勍懋投资管理合伙企业", "企业法人", "1.310589%", "4,533 万元"],
            ["上海勍熙投资管理合伙企业", "企业法人", "1.182219%", "4,089 万元"],
            ["上海勍臻投资管理合伙企业", "企业法人", "1.160246%", "4,013 万元"],
        ],
        [58, 22, 22, 28],
    )

    pdf.body_text(
        "主要人员：张思宁（董事长）、范宇（总经理/董事）、张海（董事）、于新利（董事）、秦湘（董事）等，另有 16 人。",
        size=9,
    )
    pdf.body_text(
        "经营网络：分支机构 6 家（上海第一、第二分公司，北京、武汉、深圳、海南分公司）；官网 www.zenitera.com。",
        size=9,
    )

    # ---- 4. 经营资产与资质 ----
    pdf.section_title("4. 经营资产与资质")
    pdf.simple_table(
        ["维度", "数量", "代表性记录"],
        [
            ["商标", "144 项", "「会客听」（第38/36/9类）、「ZENIDATA」（第42/36类）"],
            ["专利", "53 项", "「会议文档同步控制方法」「自适应安全矩阵调用方法」"],
            ["软件著作权", "100 项", "证通消息中间件 ZTMQ V8.1、应用服务器 ZTWeb V8.0"],
            ["作品著作权", "1 项", "「会客听」logo（国作登字-2024-F-00084992）"],
            ["行政许可", "17 项", "建筑工程施工许可、企业境外投资证书"],
            ["荣誉资质", "10 项", "高新技术企业（2022国家级）、专精特新中小企业（2025省级）"],
            ["ICP 备案", "18 项", "沪ICP备15010564号，覆盖 zenitera.com 等域名"],
        ],
        [28, 20, 122],
    )

    # ---- 5. 风险事实 ----
    pdf.section_title("5. 风险事实")
    pdf.simple_table(
        ["主题", "查询结果", "关键事实"],
        [
            ["经营状态", "在营（开业）", "未返回吊销、注销或清算等异常状态"],
            ["执行与失信", "未命中", "未返回失信被执行人或被执行人记录"],
            ["经营异常/���重违法", "未命中", "未返回经营异常或严重违法记录"],
            ["行政处罚", "未命中", "未返回行政处罚记录"],
            ["股权与担保事项", "股权出质 9 笔", "2015-2016 年历史出质，质权人：上银瑞金资本管理有限公司"],
        ],
        [35, 35, 100],
    )

    # ---- 6. 数据说明 ----
    pdf.section_title("6. 数据说明")
    pdf.body_text(
        "成功维度：工商深度、商标、专利、软件著作权、作品著作权、许可、荣誉资质、ICP 备案（共 8 个维度）。",
        size=9,
    )
    pdf.body_text("空结果维度：无（全部维度均返回有效数据）。", size=9)
    pdf.body_text("未完成维度：无。", size=9)
    pdf.ln(2)
    pdf.body_text(
        "本画像���于查询时点的公开数据摘要，不构成法律、财务、投资或准入意见。各维度数据以接口返回的分页信息为准（首页 page_size=5），totalCount 代表该维度总量。",
        size=8,
    )

    # Save
    out_path = "/Users/ice/2work/code/1_mcp/cisp-mcp/output/cisp-cp-91310000324360627T-20260727.pdf"
    pdf.output(out_path)
    print(f"PDF generated: {out_path}")
    return out_path


if __name__ == "__main__":
    generate()
