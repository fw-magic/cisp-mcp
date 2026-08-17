---
name: report-pdf-style
description: 为新建中文专业报告 Skill 提供可复制的 Letter PDF 样式与渲染参考，包括真实 Regular/Bold 中文字体预检、ReportLab 样式 token、固定列宽表格、自然分页、PDF 元数据与文本检查、逐页 PNG 渲染、失败清理和 Markdown 回退。用于设计或创建新的报告类 Skill；落地后应把所需契约和工具复制到新 Skill 内部，不作为既有报告的运行时公共依赖。
---

# 报告 PDF 通用样式

把本 Skill 作为创建新报告 Skill 时的样式参考和起始模板。不得在此定义任何报告的章节、字段、业务编号、判断规则或免责声明。

新报告接入时，复制并内置实际需要的渲染契约与工具，再在报告自己的目录中补充业务配置。已落地报告不得在运行时跨目录导入本 Skill 的脚本或读取本 Skill 的 reference；这样单个报告 Skill 可独立分发、验证和演进。

## 强制工作流

1. 先由报告 Skill 完成内容生成、证据核验和 Markdown 语义验收；PDF 阶段只排版，不归纳、删节、补造或改写内容。
2. 创建新报告时完整读取 [通用渲染契约](references/render-contract.md)，把适用规则复制到新报告自己的 PDF reference，并把工具脚本复制到新报告自己的 `scripts/`；后续只读取和运行该报告的本地资源。
3. 使用 `scripts/report_pdf_toolkit.py` 的字体发现与预检；Regular 与 Bold 任一缺失、重名或缺少报告字符时停止 PDF 流程。
4. 调用方必须为每张表提供绝对 mm 列宽；使用工具脚本提供的样式和表格构造函数，禁止内容驱动自动列宽。
5. 只使用一种可控生成路径。完成 PDF 后运行结构检查，渲染全部页面为 PNG，并逐页检查。
6. 任一步失败时删除本次不完整 PDF、字体测试文件和预览目录，返回与 PDF 同内容源的完整 Markdown；不得返回摘要或残缺文件。
7. 验收通过后删除临时文件，只保留最终交付物和明确需要保留的测试资产。

## 工具

`scripts/report_pdf_toolkit.py` 是稳定工具层，不是万能 Markdown 渲染器。它提供：

- `discover_font_spec()`、`register_chinese_fonts()`：发现、核验并注册真实中文 Regular/Bold/标题字形；
- `make_styles()`、`make_table()`：生成通用段落样式与固定宽度、重复表头的表格；
- `draw_page_chrome()`：在首页和后续页绘制固定品牌页眉、审计标识、站点页脚与连续页码；
- `verify_pdf()`、`render_pdf()`：检查 Letter 页面、字体资源、文本、占位符、逐页页眉页脚、连续页码和表头填充并逐页渲染；
- `guarded_validate_or_fallback()`：验收失败时清理不完整产物并返回完整 Markdown。

评估模板或为新报告做首次迁移时可直接运行本目录脚本，例如：

```bash
uv run python .agents/skills/report-pdf-style/scripts/report_pdf_toolkit.py font-preflight --output tmp/pdfs/font-preflight.pdf
uv run python .agents/skills/report-pdf-style/scripts/report_pdf_toolkit.py verify --pdf output/pdf/report.pdf --render-dir tmp/pdfs/report-pages --every-page "水滴征信 MCP" --every-page "cisp.zenitera.com · 水滴征信 MCP" --page-numbers
```

新报告内置后必须自行定义标题、副标题、元信息、章节、表格列及绝对列宽、特殊段落、粗体白名单、文件名、语义验收和 Markdown 回退正文，并在其测试中证明不依赖本目录。
