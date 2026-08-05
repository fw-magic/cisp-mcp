<!-- resource-id: cisp://skill/client-pre-visit-one-pager/report-template -->
<!-- resource-version: 0-dev -->
<!-- source-skill-version: v4.1-open -->

# 最终报告固定骨架

本文件是‘客户访前一页纸’ Skill 的调试期本地资源，也是对应未来 MCP Resource 的唯一正文源。进入主 `SKILL.md` 指定阶段后完整读取本文件。

## 内容索引

- [结构纪律]
- [Markdown 固定骨架]
- [标题白名单]

## 报告输出格式（严格填空骨架 · 模型只填值、不造结构）

> **使用约定**：以下是贷款及综合金融营销版完整报告骨架。七个大章节固定显示，模型使用内部原值、外部来源、候选摘要和分层分析填充 FACT/OPP/LEAD/SERVICE/RISK/WATCH/QUESTION。
>
> **结构纪律**：
>
> 1. 禁止新增、改名、合并、拆分或调换章节；禁止创造骨架外的小标题。
> 2. 仅允许按骨架中已经写明的 `{{#if ...}}` 条件隐藏画像内部事实表或产业模块内的可选事实表；七个大章节不得隐藏或重编号。
> 3. 不输出任何未被替换的占位符、条件标签、工具名、字段路径或内部状态。
> 4. 表格某行所有事实字段均为空时删除该行；某条件板块无有效事实时隐藏整块。不得用模型常识、未通过准入的网页或示例值补齐。
> 5. “核心观点”以内部主体为底座并引用优先 OPP/RISK；“执行摘要”固定展示核心特征、主要机会、主要风险和拜访建议，且在此首次定义全文唯一的 OPP/RISK 编号。
> 6. “客户全景画像”独立展示企业基本信息、关键决策人、股权、资产和核心经营数据；不得与产业画像合并。
> 7. “产业画像与行业洞察”独立展示产业链位置、行业周期与资金占用、行业对标、政策融资环境和行业风险贷款启示；行业资料不足时保留章节并展示事实边界与核验问题，不生成空表。
> 8. “定制化营销方案”固定展示贷款需求线索、产品候选和推进路径。产品候选是营销假设，不是客户已确认需求或授信结论。
> 9. “风险预警与合规提示”固定显示；无风险命中时只展示资料边界与必要准入核验，不生成空表或低风险结论。“拜访建议与话题清单”固定显示并与营销机会编号闭环。
> 10. `D.company_overview_facts` 或 `D.company_overview_fallback` 验收失败时按确定性规则重新构建；`D.core_internal_baseline` 验收失败时只允许基于同一事实白名单重写一次，仍失败则使用回退文本；`D.core_viewpoint` 验收失败时只基于已经通过证据验收的核心观点分项重新生成，禁止重新搜索或补造事实；其他必填总结字段生成失败时才重写对应大模型派生字段。不得交付缺少核心观点、执行摘要或已显示小节信息解读的报告。
> 11. 骨架中的 `<p align="center">—————————————————数据来源————————————————</p>` 是来源分隔线语义标记。Markdown 回退保留该居中标记；PDF 或 DOCX 排版时必须转换为下方规定的全宽居中分隔组件，禁止作为普通左对齐正文段落或依赖空格定位。

```markdown
# 客户访前一页纸（贷款及综合金融营销版）

报告编号：{{META.report_id}}  ｜  生成时间：{{META.generated_at}}  ｜  密级：机密

客户名称：{{B.basicList[0].orgName}}{{#if D.brand_name}}（品牌：{{D.brand_name}}）{{/if}}

## {{D.section_numbers.core}}、核心观点

{{D.core_viewpoint}}

<p align="center">—————————————————数据来源————————————————</p>

内部：水滴征信 MCP｜数据日期：{{META.generated_at}}
{{#if D.source_attributions.core.external_source_ids}}外部：{{joinUniqueSourceSiteNames WEB.sources|ids=D.source_attributions.core.external_source_ids|separator="、"|quote="《》"}}{{/if}}

## {{D.section_numbers.summary}}、执行摘要

### 核心特征

{{D.executive_core_features}}

### 主要机会

{{#if D.opportunity_register}}
| 机会编号 | 主要机会 | 企业专属触发事实 | 可能贷款用途 | 时点 | 证据强度 |
| --- | --- | --- | --- | --- | --- |
{{#each D.opportunity_register}}| **{{opportunity_id}}** | {{opportunity_title}} | {{trigger_fact}}；边界：{{boundary}} | {{likely_use_of_funds}} | {{timing}} | {{evidence_strength}} |{{/each}}
{{else}}
现有资料尚未形成可核验的企业专属贷款机会，本次拜访以融资需求、用途、金额期限、还款来源和增信条件诊断为主，不创建模拟 OPP。
{{/if}}

{{#if D.lead_register}}
| 线索编号 | 需求发现线索 | 可能金融需求 | 尚缺环节 | 证据强度 |
| --- | --- | --- | --- | --- |
{{#each D.lead_register}}| **{{lead_id}}** | {{lead_title}}：{{signal}} | {{possible_financial_need}} | {{missing_links}} | {{evidence_strength}} |{{/each}}
{{/if}}

{{#if D.service_register}}
| 服务编号 | 综合金融机会 | 类型 | 触发信号 | 核验方向 |
| --- | --- | --- | --- | --- |
{{#each D.service_register}}| **{{service_id}}** | {{service_title}} | {{service_type}} | {{trigger_signal}}；{{fit_logic}} | {{verification}} |{{/each}}
{{/if}}

### 主要风险

{{#if D.major_risk_register}}
| 风险编号 | 主要风险 | 已核实事实与边界 | 影响机会 | 对贷款营销的可能影响 |
| --- | --- | --- | --- | --- |
{{#each D.major_risk_register}}| **{{risk_id}}** | {{risk_title}} | {{fact_boundary}} | {{#if affected_opportunity_ids}}{{join affected_opportunity_ids|separator="、"}}{{else}}企业级{{/if}} | {{loan_impact}} |{{/each}}
{{else}}
现有资料未形成可列示的主要风险事实；这不等同于不存在风险，仍需取得基础准入资料并核验当前状态。
{{/if}}

{{#if D.watch_register}}
| 观察编号 | 风险观察 | 信号与边界 | 潜在影响 | 证据强度与核验方向 |
| --- | --- | --- | --- | --- |
{{#each D.watch_register}}| **{{watch_id}}** | {{watch_title}} | {{signal_boundary}} | {{possible_impact}} | {{evidence_strength}}；{{verification}} |{{/each}}
{{/if}}

### 拜访建议

{{D.executive_visit_strategy}}

<p align="center">—————————————————数据来源————————————————</p>

{{#if D.source_attributions.summary.internal_dimensions}}内部：水滴征信 MCP｜数据日期：{{META.generated_at}}{{/if}}
{{#if D.source_attributions.summary.external_source_ids}}外部：{{joinUniqueSourceSiteNames WEB.sources|ids=D.source_attributions.summary.external_source_ids|separator="、"|quote="《》"}}{{/if}}

## {{D.section_numbers.profile}}、客户全景画像

### （一）企业基本信息

| 项目 | 内容 |
| --- | --- |
| **企业全称** | {{B.basicList[0].orgName}} |
{{#if B.basicList[0].creditCode}}| **统一社会信用代码** | {{B.basicList[0].creditCode}} |{{/if}}
{{#if B.basicList[0].estDate}}| **成立时间** | {{B.basicList[0].estDate}} |{{/if}}
{{#if B.basicList[0].regAddr}}| **注册地址** | {{B.basicList[0].regAddr}} |{{/if}}
{{#if D.operating_address}}| **实际经营地址** | {{D.operating_address}} |{{/if}}
{{#if D.registered_capital_display}}| **注册资本** | {{D.registered_capital_display}} |{{/if}}
{{#if D.paid_in_capital_display}}| **实缴资本** | {{D.paid_in_capital_display}} |{{/if}}
{{#if B.basicList[0].orgType}}| **企业性质** | {{B.basicList[0].orgType}} |{{/if}}
{{#if D.employee_scale}}| **员工规模** | {{D.employee_scale}} |{{/if}}
{{#if B.basicList[0].industry}}| **所属行业** | {{B.basicList[0].industry}} |{{/if}}
{{#if D.qualifications}}| **企业资质** | {{D.qualifications}} |{{/if}}

**信息解读：** {{D.basic_interpretation}}

<p align="center">—————————————————数据来源————————————————</p>

内部：水滴征信 MCP｜数据日期：{{META.generated_at}}

{{#if D.person_rows}}
### （二）关键决策人信息

| 姓名 | 来源 | 职务/关系 | 背景与证据状态 |
| --- | --- | --- | --- |
{{#each D.person_rows}}| {{name}} | {{person_origin}} | {{position}} | {{background}}；身份置信度：{{identity_confidence}}{{#if conflicts}}；冲突：{{join conflicts|separator="；"}}{{/if}} |{{/each}}

**信息解读：** {{D.people_interpretation}}

<p align="center">—————————————————数据来源————————————————</p>

内部：水滴征信 MCP｜数据日期：{{META.generated_at}}
{{#if D.source_attributions.people.external_source_ids}}外部：{{joinUniqueSourceSiteNames WEB.sources|ids=D.source_attributions.people.external_source_ids|separator="、"|quote="《》"}}{{/if}}
{{/if}}

{{#if D.has_equity_or_network}}
### （三）股权结构与关联关系

{{#if D.has_shareholder_notes}}
| 股东 | 持股情况 | 说明 |
| --- | --- | --- |
{{#each D.shareholder_rows}}| {{name}} | {{holding_display}} | {{#if note}}{{note}}{{else}}—{{/if}} |{{/each}}
{{else}}
| 股东 | 持股情况 |
| --- | --- |
{{#each D.shareholder_rows}}| {{name}} | {{holding_display}} |{{/each}}
{{/if}}

**信息解读：** {{D.equity_interpretation}}

<p align="center">—————————————————数据来源————————————————</p>

内部：水滴征信 MCP｜数据日期：{{META.generated_at}}
{{#if D.source_attributions.equity.external_source_ids}}外部：{{joinUniqueSourceSiteNames WEB.sources|ids=D.source_attributions.equity.external_source_ids|separator="、"|quote="《》"}}{{/if}}
{{/if}}

{{#if D.has_assets}}
### （四）企业资产状况

{{#if D.tangible_asset_rows}}**有形资产：**

| 资产类型 | 可核验事实 | 权利与口径边界 |
| --- | --- | --- |
{{#each D.tangible_asset_rows}}| **{{asset_type}}** | {{fact}} | {{boundary}} |{{/each}}
{{/if}}

{{#if D.has_intangible_assets}}**无形资产：**

数量采用公开记录总量；代表记录为本报告展示的样本，不代表最新、全部有效或权利状态已经核验。

| 类型 | 数量 | 代表记录 |
| --- | --- | --- |
{{#if IP.patentsListMeta.totalCount}}| **专利** | {{IP.patentsListMeta.totalCount}} | {{D.patent_representatives}} |{{/if}}
{{#if SW.swListMeta.totalCount}}| **软件著作权** | {{SW.swListMeta.totalCount}} | {{D.software_representatives}} |{{/if}}
{{#if WC.resultListMeta.totalCount}}| **作品著作权** | {{WC.resultListMeta.totalCount}} | {{D.work_representatives}} |{{/if}}
{{#if TM.brandListMeta.totalCount}}| **商标** | {{TM.brandListMeta.totalCount}} | {{D.trademark_representatives}} |{{/if}}
{{#if ICP.icpListMeta.totalCount}}| **ICP 备案** | {{ICP.icpListMeta.totalCount}} | {{D.icp_representatives}} |{{/if}}
{{#if LIC.detailListMeta.totalCount}}| **工商许可** | {{LIC.detailListMeta.totalCount}} | {{D.license_representatives}} |{{/if}}
{{#if D.honor_count}}| **荣誉资质** | 代表记录 {{D.honor_count}} 项 | {{D.honor_representatives}} |{{/if}}
{{/if}}

**信息解读：** {{D.assets_interpretation}}

<p align="center">—————————————————数据来源————————————————</p>

{{#if D.source_attributions.assets.internal_dimensions}}内部：水滴征信 MCP｜数据日期：{{META.generated_at}}{{/if}}
{{#if D.source_attributions.assets.external_source_ids}}外部：{{joinUniqueSourceSiteNames WEB.sources|ids=D.source_attributions.assets.external_source_ids|separator="、"|quote="《》"}}{{/if}}
{{/if}}

{{#if D.has_core_operations}}
### （五）核心经营数据

信息说明：{{D.operations_boundary}}

{{#if D.has_core_operation_rows}}
| 指标 | 本次数据 | 数据口径 |
| --- | --- | --- |
{{#each D.core_operation_rows}}| **{{metric}}** | {{value}} | {{period_basis}} |{{/each}}

**信息解读：** {{D.operations_interpretation}}

<p align="center">—————————————————数据来源————————————————</p>

内部：水滴征信 MCP｜数据日期：{{META.generated_at}}
{{/if}}
{{/if}}

## {{D.section_numbers.industry}}、产业画像与行业洞察

### （一）产业链位置与经营模式

{{D.industry_positioning}}

{{#if D.industry_external_context}}行业背景：{{D.industry_external_context}}{{/if}}

**贷款视角解读：** {{D.industry_business_model_interpretation}}

### （二）行业周期与资金占用

{{#if D.has_industry_cycle}}
| 行业信号 | 已核实事实 | 时间与范围 | 可能的现金流传导 | 企业核验事项 |
| --- | --- | --- | --- | --- |
{{#each D.industry_cycle_rows}}| **{{signal}}** | {{verified_fact}} | {{period_scope}} | {{cashflow_transmission}} | {{enterprise_verification}} |{{/each}}

**贷款视角解读：** {{D.industry_cycle_interpretation}}
{{else}}
现有资料不足以形成可核验的行业周期与资金占用事实，本次应向企业核实采购周期、备货与库存、销售账期、回款节奏及资本开支计划。
{{/if}}

### （三）行业对标与经营参照

{{#if D.has_industry_benchmark}}
| 对标维度 | 企业行业位置 | 行业参考 | 时间与范围 | 贷款结构启示 |
| --- | --- | --- | --- | --- |
{{#each D.industry_benchmark_rows}}| **{{topic}}** | {{company_position}} | {{industry_reference}} | {{period_scope}} | {{lending_implication}} |{{/each}}

**贷款视角解读：** {{D.industry_benchmark_interpretation}}
{{else}}
现有资料未形成同范围、同期间、同口径的行业参照，不以异口径竞争对手数据推断企业经营地位；应取得企业实际产销、库存、应收和现金流资料后再作贷款结构判断。
{{/if}}

### （四）政策与融资环境

{{#if D.has_industry_policy}}
| 政策或融资环境 | 适用范围 | 与融资的关系 | 企业核验事项 |
| --- | --- | --- | --- |
{{#each D.industry_policy_rows}}| **{{policy_or_environment}}** | {{applicable_scope}} | {{financing_relevance}} | {{enterprise_verification}} |{{/each}}

**贷款视角解读：** {{D.industry_policy_interpretation}}
{{else}}
现有资料未形成可确认适用于该企业的现行行业融资政策；一般性产业支持不等于企业满足贷款准入条件。
{{/if}}

### （五）行业风险与贷款启示

{{#if D.has_industry_risk}}
| 行业风险信号 | 已核实事实 | 可能的现金流传导 | 企业核验事项 | 贷款结构启示 |
| --- | --- | --- | --- | --- |
{{#each D.industry_risk_rows}}| **{{signal}}** | {{verified_fact}} | {{cashflow_transmission}} | {{enterprise_verification}} | {{lending_implication}} |{{/each}}

**贷款视角解读：** {{D.industry_risk_interpretation}}
{{else}}
现有行业资料未形成可展示的风险事实，不据此作低风险判断；应结合企业销量、毛利、库存、应收、经营现金流和现有融资核验风险传导。
{{/if}}

资料边界：{{D.industry_information_boundary}}

<p align="center">—————————————————数据来源————————————————</p>

{{#if D.source_attributions.industry.internal_dimensions}}内部：水滴征信 MCP｜数据日期：{{META.generated_at}}{{/if}}
{{#if D.source_attributions.industry.external_source_ids}}外部：{{joinUniqueSourceSiteNames WEB.sources|ids=D.source_attributions.industry.external_source_ids|separator="、"|quote="《》"}}{{/if}}

## {{D.section_numbers.marketing}}、定制化营销方案

### （一）融资需求线索

{{#if D.financing_need_rows}}
| 机会 | 贷款需求场景 | 触发事实 | 可能资金用途 | 时点 | 证据强度 | 现场核验重点 |
| --- | --- | --- | --- | --- | --- | --- |
{{#each D.financing_need_rows}}| **{{opportunity_id}}** | {{need_scenario}} | {{trigger_fact}} | {{likely_use_of_funds}} | {{timing}} | {{evidence_strength}} | {{verification_focus}} |{{/each}}
{{else}}
现有资料尚未形成可核验的企业专属融资触发，本次拜访先完成融资用途、金额、期限、还款来源和增信条件诊断。
{{/if}}

{{#if D.lead_register}}
| 线索 | 信号 | 可能金融需求 | 缺失环节 | 证据强度 | 现场核验重点 |
| --- | --- | --- | --- | --- | --- |
{{#each D.lead_register}}| **{{lead_id}}** | {{lead_title}}：{{signal}} | {{possible_financial_need}} | {{missing_links}} | {{evidence_strength}} | 围绕缺失环节逐项确认 |{{/each}}
{{/if}}

{{#if D.service_register}}
| 综合金融机会 | 类型 | 触发信号 | 匹配逻辑 | 核验重点 |
| --- | --- | --- | --- | --- |
{{#each D.service_register}}| **{{service_id}}｜{{service_title}}** | {{service_type}} | {{trigger_signal}} | {{fit_logic}} | {{verification}} |{{/each}}
{{/if}}

### （二）贷款产品候选

{{#if D.loan_product_candidates}}
| 优先级与产品族 | 匹配逻辑 | 可能还款来源 | 可核验增信资源 | 准入缺口与开场话术 |
| --- | --- | --- | --- | --- |
{{#each D.loan_product_candidates}}| **{{priority}}｜{{product_family}}（{{opportunity_id}}）** | {{fit_logic}} | {{possible_repayment_source}} | {{possible_credit_enhancement}} | {{qualification_gaps}}；建议开场：{{opening_pitch}} |{{/each}}
{{else}}
现有资料不足以形成具体贷款产品候选，本次先完成融资需求诊断。
{{/if}}

{{#if D.service_product_candidates}}
| 优先级与综合金融产品 | 匹配逻辑 | 合作缺口与开场话术 |
| --- | --- | --- |
{{#each D.service_product_candidates}}| **{{priority}}｜{{product_family}}（{{service_id}}）** | {{fit_logic}} | {{qualification_gaps}}；建议开场：{{opening_pitch}} |{{/each}}
{{/if}}

信息边界：{{D.marketing_boundary}}

### （三）推进路径

| 阶段 | 关联主线 | 目标 | 关键动作 | 进入下一阶段的条件 |
| --- | --- | --- | --- | --- |
{{#each D.marketing_sequence}}| **{{stage}}** | {{#if related_opportunity_ids}}{{join related_opportunity_ids|separator="、"}}{{else}}融资需求诊断{{/if}}{{#if related_risk_ids}}；{{join related_risk_ids|separator="、"}}{{/if}} | {{objective}} | {{actions}} | {{exit_criteria}} |{{/each}}

<p align="center">—————————————————数据来源————————————————</p>

{{#if D.source_attributions.marketing.internal_dimensions}}内部：水滴征信 MCP｜数据日期：{{META.generated_at}}{{/if}}
{{#if D.source_attributions.marketing.external_source_ids}}外部：{{joinUniqueSourceSiteNames WEB.sources|ids=D.source_attributions.marketing.external_source_ids|separator="、"|quote="《》"}}{{/if}}

## {{D.section_numbers.risk}}、风险预警与合规提示

{{#if D.has_risks}}
| 风险编号 | 影响机会 | 关注事项 | 已核实事实与边界 | 对贷款营销的可能影响 | 现场核验与缓释方向 |
| --- | --- | --- | --- | --- | --- |
{{#each D.risks}}| **{{risk_id}}** | {{#if affected_opportunity_ids}}{{join affected_opportunity_ids|separator="、"}}{{else}}企业级{{/if}} | {{topic}} | {{detail}} | {{sales_implication}} | {{verification}} |{{/each}}
{{else}}
已核实风险事实：现有资料未形成可进入风险表的明确命中；这不等同于不存在相关事项，仍需按本章资料范围完成准入核验。
{{/if}}

{{#if D.watch_register}}
| 观察编号 | 观察事项 | 信号、主体与边界 | 潜在影响 | 证据强度 | 核验方向 |
| --- | --- | --- | --- | --- | --- |
{{#each D.watch_register}}| **{{watch_id}}** | {{watch_title}} | {{signal_boundary}} | {{possible_impact}} | {{evidence_strength}} | {{verification}} |{{/each}}
{{/if}}

**信息解读：** {{D.risk_interpretation}}

{{#if D.risk_compliance_context}}合规提示：{{D.risk_compliance_context}}{{/if}}

{{#if D.risk_zero_dimensions}}信息说明：近两年公开统计中以下事项记录数为 0：{{D.risk_zero_dimensions}}；仅代表该公开统计范围，不等同于不存在相关事项。{{/if}}

{{#if D.risk_information_boundary}}资料范围：{{D.risk_information_boundary}}{{/if}}

<p align="center">—————————————————数据来源————————————————</p>

{{#if D.source_attributions.risk.internal_dimensions}}内部：水滴征信 MCP｜数据日期：{{META.generated_at}}{{/if}}
{{#if D.source_attributions.risk.external_source_ids}}外部：{{joinUniqueSourceSiteNames WEB.sources|ids=D.source_attributions.risk.external_source_ids|separator="、"|quote="《》"}}{{/if}}

## {{D.section_numbers.visit}}、拜访建议与话题清单

### （一）本次拜访目标

{{#each D.visit_objectives}}- {{objective}}（关联：{{join related_opportunity_ids|separator="、"}}{{#if related_risk_ids}}；{{join related_risk_ids|separator="、"}}{{/if}}）{{/each}}

### （二）推荐话题

| 关联机会 | 话题 | 企业事实开场 | 转入贷款需求的衔接方式 |
| --- | --- | --- | --- |
{{#each D.recommended_topics}}| **{{#if related_opportunity_ids}}{{join related_opportunity_ids|separator="、"}}{{else}}融资需求诊断{{/if}}** | {{topic}} | {{opening_basis}} | {{transition}} |{{/each}}

### （三）关键问题

| 顺序 | 关联主线 | 建议对象 | 主题与依据 | 问法 | 对候选方案的影响 |
| --- | --- | --- | --- | --- | --- |
{{#each D.visit_questions}}| {{sequence}} | {{#if related_opportunity_ids}}{{join related_opportunity_ids|separator="、"}}{{else}}融资需求诊断{{/if}}{{#if related_risk_ids}}；{{join related_risk_ids|separator="、"}}{{/if}} | {{audience}} | **{{topic}}**：{{basis}} | {{question}} | {{answer_impact}} |{{/each}}

### （四）建议取得的资料

| 资料 | 核验目的 | 关联机会 | 关联风险 |
| --- | --- | --- | --- |
{{#each D.document_checklist}}| **{{document}}** | {{purpose}} | {{join related_opportunity_ids|separator="、"}} | {{join related_risk_ids|separator="、"}} |{{/each}}

### （五）禁忌提示

{{#each D.taboo_notes}}- {{this}}{{/each}}

<p align="center">—————————————————数据来源————————————————</p>

{{#if D.source_attributions.visit.internal_dimensions}}内部：水滴征信 MCP｜数据日期：{{META.generated_at}}{{/if}}
{{#if D.source_attributions.visit.external_source_ids}}外部：{{joinUniqueSourceSiteNames WEB.sources|ids=D.source_attributions.visit.external_source_ids|separator="、"|quote="《》"}}{{/if}}

## 报告使用说明

- 报告目的：本报告用于对公客户经理贷款营销访前准备；融资需求、产品方向、还款来源与增信资源均为待核验假设，不作为授信审批依据。
- 信息真实性：报告依据生成时点的公开信息形成；资料缺失或尚待补充不等同于不存在相关事实，建议在拜访中核实关键信息。
- 数据时效性：报告生成后如发生重大变化，建议重新生成报告。
- 保密义务：本报告涉及企业信息，接收方应按所在机构制度妥善保管，未经授权不得对外泄露。
```

### 标题白名单

最终报告只能出现骨架中实际存在的标题，标题名称必须逐字使用，禁止同义替换：`核心观点`、`执行摘要`、`核心特征`、`主要机会`、`主要风险`、`拜访建议`、`客户全景画像`、`（一）企业基本信息`、`（二）关键决策人信息`、`（三）股权结构与关联关系`、`（四）企业资产状况`、`（五）核心经营数据`、`产业画像与行业洞察`、`（一）产业链位置与经营模式`、`（二）行业周期与资金占用`、`（三）行业对标与经营参照`、`（四）政策与融资环境`、`（五）行业风险与贷款启示`、`定制化营销方案`、`（一）融资需求线索`、`（二）贷款产品候选`、`（三）推进路径`、`风险预警与合规提示`、`拜访建议与话题清单`、`（一）本次拜访目标`、`（二）推荐话题`、`（三）关键问题`、`（四）建议取得的资料`、`（五）禁忌提示`、`报告使用说明`。

