#!/usr/bin/env python3
"""Convert the enterprise profile Markdown to a multi-page A4 PDF."""

import markdown
from weasyprint import HTML
import sys

def md_to_pdf(md_path: str, pdf_path: str):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "codehilite"],
    )

    css = """
    @page {
        size: A4;
        margin: 2cm 2.2cm;
        @bottom-center {
            content: "CISP 企业画像 · 证通股份有限公司 · 第 " counter(page) " 页";
            font-size: 9px;
            color: #888;
            font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
        }
    }

    body {
        font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
        font-size: 11pt;
        line-height: 1.75;
        color: #222;
    }

    h1 {
        font-size: 20pt;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 8px;
        margin-top: 0;
        color: #1e3a5f;
    }

    h2 {
        font-size: 14pt;
        margin-top: 24px;
        color: #2563eb;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 4px;
    }

    h3 {
        font-size: 12pt;
        margin-top: 18px;
        color: #333;
    }

    blockquote {
        background: #f1f5f9;
        border-left: 4px solid #2563eb;
        margin: 12px 0;
        padding: 8px 16px;
        color: #475569;
        font-size: 10pt;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 16px 0;
        font-size: 10pt;
    }

    th {
        background: #2563eb;
        color: white;
        font-weight: 600;
        padding: 6px 10px;
        text-align: left;
    }

    td {
        padding: 5px 10px;
        border-bottom: 1px solid #e2e8f0;
    }

    tr:nth-child(even) td {
        background: #f8fafc;
    }

    strong {
        color: #1e3a5f;
    }

    p {
        margin: 4px 0 8px 0;
    }

    ul, ol {
        margin: 4px 0 8px 0;
        padding-left: 20px;
    }

    li {
        margin: 2px 0;
    }

    code {
        background: #f1f5f9;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 9.5pt;
    }
    """

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    HTML(string=full_html).write_pdf(pdf_path)
    print(f"PDF generated: {pdf_path}")


if __name__ == "__main__":
    md_file = sys.argv[1] if len(sys.argv) > 1 else "output/cisp-cp-91310000324360627T-20260727.md"
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else md_file.replace(".md", ".pdf")
    md_to_pdf(md_file, pdf_file)
