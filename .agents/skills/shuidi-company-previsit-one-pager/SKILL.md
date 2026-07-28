---
name: shuidi-company-previsit-one-pager
description: 使用客户 Agent 中连接标识为 cisp-mcp 的水滴 MCP 工商深度、知识产权、ICP备案、行政许可、荣誉资质和企业舆情工具，为指定中国企业生成严格基于接口事实的“对公客户访前一页纸”，默认交付 Letter 尺寸 PDF，无法生成 PDF 时回退完整 Markdown。适用于对公客户经理访前准备、企业拜访简报、客户全景画像、拜访问题清单、合作前背景了解，以及用户提出“公司访前一页纸”“客户访前报告”“拜访前帮我了解这家公司”“生成访前 PDF”等请求。
---

> 水滴 MCP 公司访前一页纸。
>
> 面向对公客户经理的访前准备工具。输入企业名称或统一社会信用代码，自动锚定主体，整合工商登记、主要人员、股权、知识产权、许可资质、近期公开动态和风险事实，生成与标准成品一致的紧凑 Letter 版式报告。
>
> 核心能力：
> - 主体工商核验与经营范围事实摘要
> - 主要人员、股东和经营网络速览
> - 专利、商标、软件著作权、作品著作权、ICP、许可和荣誉资质盘点
> - 近 90 天公开舆情中的机会线索与风险线索
> - 把 MCP 未覆盖的经营、财务和合作信息转成拜访核验问题
> - 默认生成 PDF；文档环境不可用时完整回退 Markdown
>
> 使用方式：`/shuidi-company-previsit-one-pager 企业名称或信用代码 [--format pdf|md]`

- **命令**：`/shuidi-company-previsit-one-pager`
- **数据源**：水滴 MCP
- **MCP Server 连接标识**：`cisp-mcp`
- **默认格式**：`pdf`
- **报告定位**：访前准备，不构成授信、法律、财务、投资或准入结论

---

## MCP 服务依赖

1. 仅使用客户 Agent 中配置名称或连接标识为 `cisp-mcp` 的 MCP Server。连接方式、认证方式和连接参数由客户 Agent 的 MCP 配置提供，不属于本 Skill 的职责。
2. 执行前检查 `cisp-mcp` 是否已连接，并检查下方绑定的工具名及输入参数 schema。不得只凭“水滴 MCP”“CISP MCP”等展示名称，或工具语义相似，改用其他 MCP Server。
3. 客户 Agent 可能把连接标识规范化为工具命名空间，例如将 `cisp-mcp` 显示为 `cisp_mcp`。只有当工具元数据明确归属于原始连接标识 `cisp-mcp` 时，才可把该命名空间下的同名工具视为本 Skill 的目标工具。
4. `p0010058_query_business_basic_deep` 是必需工具。`cisp-mcp` 未连接、该工具不存在或其参数 schema 与本 Skill 不兼容时，立即停止，不生成报告，并提示用户检查或连接 `cisp-mcp`；禁止改用互联网、其他 MCP 或同义工具补位。
5. 其余绑定工具为扩展维度工具。单个扩展工具不存在、不可用或调用失败时，将对应维度记为 `failed`，继续处理其他维度，不得跨 Server 寻找替代工具。
6. 始终通过 Agent 已注册的 `cisp-mcp` 工具调用服务。

## 数据纪律

1. 只使用本次水滴 MCP 返回的数据。禁止用互联网搜索、模型记忆、第三方数据库或样例企业内容补齐。
2. 先锚定唯一企业主体，再查询扩展维度。工商深度失败、无结果或主体不一致时停止生成。
3. 金额、比例、日期、数量和币种逐字保留接口原始值。禁止四舍五入、补零、换算、加总、相减、相乘或倒算。
4. 不根据股东、任职或投资关系推导实际控制人、最终受益人、一致行动关系、融资轮次或资本市场状态。
5. 分页接口以 `*ListMeta.totalCount` 表示总量；第一页记录只称“本次首批返回记录”，不得称为“最新”或“全部”。
6. 空数组只表示“本次查询未返回相关公开记录”；调用失败表示“该维度查询未完成”。两者不得互换。
7. 舆情只称“公开舆情线索”，不得升级为已经核验的司法、监管或经营事实。
8. 报告正文不得出现工具代码、产品码、JSON 路径、schema、调用失败堆栈、额度或积分信息。
9. 不输出身份证号、手机号、API Key、原始响应或非必要个人敏感信息。
10. 不生成营收、利润、市场份额、客户数量、融资金额、授信、存款、代发、贷款建议或银行产品推荐，除非接口直接返回对应事实；本 skill 当前固定不展示这些板块。

## `cisp-mcp` 工具绑定

下表中的工具必须全部从连接标识为 `cisp-mcp` 的 MCP Server 解析。

| 业务维度 | `cisp-mcp` 工具 | 调用约定 |
| --- | --- | --- |
| 主体消歧 | `p0010068_fuzzy_search_company_name` | 参数 `ent_name`；仅简称、品牌名或可能重名时调用 |
| 工商深度 | `p0010058_query_business_basic_deep` | 必选；按输入类型四选一：企业名称用 `ent_name`，统一社会信用代码用 `credit_code`，注册号用 `reg_no`，组织机构代码用 `org_code` |
| 商标 | `p0010073_query_trademark_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 专利 | `p0010078_query_patent_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 软件著作权 | `p0010074_query_software_copyright_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 作品著作权 | `p0010075_query_work_copyright_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| ICP 备案 | `p0010076_query_icp_filing_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 工商许可 | `p0010084_query_license_info` | `ent_info=规范企业全称`，`license_type="gs"`，`page_no="1"`，`page_size="5"` |
| 荣誉资质 | `p0110003_query_honor_qualification_info` | `ent_info=规范企业全称`；使用本次返回列表，不宣称全量 |
| 近期舆情 | `p0050007_p0050008_query_public_opinion_info` | `ent_name=规范企业全称`；最近 90 个自然日，`page_size="10"`，`max_details=5` |

**参数名注意**：主体消歧使用 `ent_name`。工商深度按输入类型使用 `ent_name`、`credit_code`、`reg_no` 或 `org_code`。舆情使用 `ent_name`。商标、专利、软件著作权、作品著作权、ICP、许可和荣誉资质使用 `ent_info`。参数名不得跨工具混用。

不要调用通用网关 `query_cisp_product` 替代专用工具。不要默认调用二要素、三要素核验或单点关联工具。

## 字段别名

模板和内部证据整理使用以下短别名。别名只用于执行和模板，不写入客户报告。

| 别名 | 工具数据根路径 |
| --- | --- |
| `B` | `p0010058_query_business_basic_deep.data` |
| `TM` | `p0010073_query_trademark_info.data` |
| `IP` | `p0010078_query_patent_info.data` |
| `SW` | `p0010074_query_software_copyright_info.data` |
| `WC` | `p0010075_query_work_copyright_info.data` |
| `ICP` | `p0010076_query_icp_filing_info.data` |
| `LIC` | `p0010084_query_license_info.data` |
| `HON` | `p0110003_query_honor_qualification_info.data` |
| `OP` | `p0050007_p0050008_query_public_opinion_info` |
| `D` | 从上述原值忠实压缩形成的派生文案，不新增事实 |
| `META` | 查询时间、报告编号、格式等报告元数据 |

占位符语法：

- 直接字段：`{{B.basicList[0].orgName}}`
- 列表循环：`{{#each B.shareholderList|max=15}}...{{/each}}`
- 条件板块：`{{#if B.personList}}...{{/if}}`
- 列表计数：`{{count(B.dishonestList)}}`
- 派生文案：`{{D.core_view}}`
- 缺失字段：删除所在行；整块无有效内容时仅按骨架中的预定义条件隐藏，保留参考成品的原始章节编号，不连续重编号。

### 关键字段映射

| 展示项 | 字段 |
| --- | --- |
| 企业全称、信用代码、状态、法定代表人 | `B.basicList[0].orgName`, `creditCode`, `orgStatus`, `legRepName` |
| 成立、类型、资本、地址、行业、范围 | `estDate`, `orgType`, `regCap`, `regCapCur`, `paidInCap`, `regAddr`, `industry`, `operateScope` |
| 联系和年报 | `email`, `tel`, `ancheYear`, `B.basicInformationList` |
| 股东 | `B.shareholderList[].shareholderName`, `shareholderType`, `fundedRatio`, `subConAmt`, `subConCur`, `conDate` |
| 主要人员 | `B.personList[].perName`, `position`, `isFr`, `personAmount` |
| 分支、投资、网站 | `B.filiationList`, `B.entInvItemList`, `B.websiteOrOnlineList` |
| 风险 | `B.dishonestList`, `executedList`, `exceptionList`, `illegalList`, `caseInfoList`, `sharFrozList`, `sharePledgList` 及 mortgage、judicial aid、liquidation 列表 |
| 商标总量、代表项 | `TM.brandListMeta.totalCount`, `TM.brandList[].tmName` |
| 专利总量、代表项 | `IP.patentsListMeta.totalCount`, `IP.patentsList[].pttTitle`, `pttType`, `legalStatus` |
| 软著总量、代表项 | `SW.swListMeta.totalCount`, `SW.swList[].softName`, `softStatus` |
| 作品著作权 | `WC.resultListMeta.totalCount`, `WC.resultList[].workName`, `type` |
| ICP | `ICP.icpListMeta.totalCount`, `ICP.icpList[].webName`, `hostname`, `icpLicense` |
| 许可 | `LIC.detailListMeta.totalCount`, `LIC.detailList[].licName`, `licNo`, `licAuth`, `licStateName` |
| 荣誉资质 | `HON.itemNameList[].name`, `level`, `government`, `pubDate`, `status`, `revokeDate` |
| 舆情 | `OP.list_result.data.infoListMeta.totalCount`, 列表和详情中的 `title`, `pubTime`, `siteName`, `infoEmotion`, `content`, `url` |

## 执行工作流

### 1. 锚定主体

1. 输入是明确完整企业名、统一社会信用代码、注册号或组织机构代码时，直接调用工商深度。
2. 输入是简称、品牌名或存在多个合理主体时，先模糊查询；只有一个明显匹配时继续，否则列出不超过 5 个候选并等待用户确认。
3. 使用 `B.basicList[0].orgName` 作为全部扩展查询的企业名称锚点，使用 `creditCode` 作为主体一致性核对标识。
4. 工商深度返回主体与用户指定主体冲突时停止，不生成貌似完整的报告。

### 2. 查询扩展维度

主体确认后，并行调用商标、专利、软件著作权、作品著作权、ICP、工商许可、荣誉资质和近 90 天舆情。舆情日期使用执行日为 `end_date`，向前推 90 个自然日为 `start_date`，格式 `yyyy-MM-dd`，不设置情感过滤。

记录每个维度的状态：

- `success`：成功且有有效数据；
- `empty`：成功但返回空列表或无结果；
- `failed`：工具不可用、超时、权限不足或调用失败。

扩展维度失败时继续生成其他已取得内容；工商深度失败时终止。

### 3. 构建统一证据模型

先把 MCP 原值整理为以下 UTF-8 JSON，再从同一 JSON 生成 Markdown 和 PDF。禁止让两个格式分别归纳原始响应。

```json
{
  "META": {
    "report_id": "CP-YYYYMMDD-HHMMSS",
    "generated_at": "YYYY-MM-DD HH:MM:SS",
    "classification": "机密",
    "successful_dimensions": "以、连接",
    "empty_dimensions": "以、连接",
    "failed_dimensions": "以、连接"
  },
  "B": "工商深度工具 data 原值",
  "TM": "商标工具 data 原值",
  "IP": "专利工具 data 原值",
  "SW": "软件著作权工具 data 原值",
  "WC": "作品著作权工具 data 原值",
  "ICP": "ICP备案工具 data 原值",
  "LIC": "工商许可工具 data 原值",
  "HON": "荣誉资质工具 data 原值",
  "OP": "舆情工具完整返回原值",
  "D": {
    "core_view": "只含直接证据的一段核心观点",
    "has_summary": true,
    "value_judgment": "登记、行业、资质和资产事实摘要",
    "opportunities": "仅基于正面舆情、有效荣誉或业务范围的访谈线索",
    "risk_summary": "只陈述命中风险维度和数量",
    "visit_advice": "基于已有事实形成的访前沟通建议",
    "has_customer_profile": true,
    "has_basic": true,
    "has_equity_or_network": true,
    "has_assets": true,
    "has_intangible_assets": true,
    "has_core_operations": true,
    "has_industry_insight": false,
    "has_internal_bank_data": false,
    "has_visit_questions": true,
    "has_product_match": false,
    "has_marketing_plan": false,
    "visit_questions": [
      {"topic": "核验主题", "basis": "已取得事实或数据缺口", "question": "现场建议核实的问题"}
    ],
    "has_risks": true,
    "risks": [
      {"topic": "风险维度", "result": "原始数量或状态", "detail": "关键事实", "scope": "目标企业自身或公开舆情线索"}
    ]
  }
}
```

整理规则：

- `B` 至 `OP` 保存对应工具原值；`D` 只保存忠实压缩文案、条件布尔值和固定表格所需的派生展示项。
- `D.has_*` 只在对应板块至少存在一项有效事实时设为 `true`；不得为了保留版面而设为 `true`。
- 基本信息只保留非空字段；注册资本按 `regCap + regCapCur` 原样组合。
- 股东最多展示 15 名。比例可解析时仅用于排序，展示仍使用原字符串；不可解析时保持接口顺序。
- 主要人员最多 8 名；不得补写教育、履历、创始人身份或实际控制关系。
- 各资产最多展示 3 个首批返回名称；总量使用分页元数据。
- 荣誉资质只能写“本次返回 N 项”，不得称全量。
- 舆情最多展示 5 条，保留标题、日期、来源和接口情感标签。
- 风险只写目标企业自身记录；关联主体记录必须单独标明范围。
- `D.visit_questions` 可询问主营收入结构、客户集中度、现金流、融资需求、研发投入和合作诉求，但不得预设答案或推荐具体银行产品。
- `D.has_industry_insight`、`D.has_internal_bank_data`、`D.has_product_match` 与 `D.has_marketing_plan` 在当前水滴 MCP 唯一数据源模式下固定为 `false`；不得用公开搜索或模型知识将其改为 `true`。

## 报告输出格式（严格填空骨架 · 模型只填值、不造结构）

> **使用约定**：以下是“对公客户访前一页纸”的完整报告骨架。主标题、一级标题、二级标题、章节编号、表头、数据来源说明和报告使用说明均以参考成品 DOCX 为准。模型只把占位符替换为本次水滴 MCP 返回值或基于这些原值形成的忠实摘要，禁止自行新增结构。
>
> **结构纪律**：
>
> 1. 禁止新增、改名、合并、拆分或调换章节；禁止创造骨架外的小标题。
> 2. 仅允许按骨架中已经写明的 `{{#if ...}}` 条件隐藏整行、整表或整块。隐藏后保留原始编号，不得把后续章节重新编号。
> 3. 不输出任何未被替换的占位符、条件标签、工具名、字段路径或内部状态。
> 4. 表格某行所有事实字段均为空时删除该行；某条件板块无有效事实时隐藏整块。不得用模型常识、互联网或示例值补齐。
> 5. “信息解读”“核心观点”“执行摘要”和风险描述只能压缩已经取得的事实，不得推导实控人、融资、营收、市场地位、授信结论或产品适配。
> 6. “四、产业画像与行业洞察”“五、与我行合作现状”作为参考成品标题保留在骨架中；当前水滴 MCP 唯一数据源不支撑，条件固定为 `false`，最终报告必须隐藏。
> 7. “六、需求识别与产品推荐”只允许显示“（一）需求智能识别”，并把数据缺口写成待核实事项；“（二）产品精准匹配”和“（三）定制化营销方案”固定隐藏，不生成银行产品推荐。
> 8. “七、风险预警与合规提示”先展示工商深度返回的企业自身风险事实和负面舆情线索；五个固定风险小标题只在对应事实有直接证据时显示，风险等级统一写“本次不评级”。

```markdown
# 对公客户访前一页纸

报告编号：{{META.report_id}}  ｜  生成时间：{{META.generated_at}}  ｜  密级：机密

客户名称：{{B.basicList[0].orgName}}{{#if D.brand_name}}（品牌：{{D.brand_name}}）{{/if}}

{{#if D.core_view}}
## 一、核心观点

{{D.core_view}}
{{/if}}

{{#if D.has_summary}}
## 二、执行摘要

**核心价值判断：** {{D.value_judgment}}

{{#if D.opportunities}}**主要机会：** {{D.opportunities}}{{/if}}

{{#if D.risk_summary}}**主要风险：** {{D.risk_summary}}{{/if}}

**拜访建议：** {{D.visit_advice}}
{{/if}}

{{#if D.has_customer_profile}}
## 三、客户全景画像

{{#if D.has_basic}}
### （一）企业基本信息

| 企业全称 | {{B.basicList[0].orgName}} |
| --- | --- |
{{#if B.basicList[0].creditCode}}| 统一社会信用代码 | {{B.basicList[0].creditCode}} |{{/if}}
{{#if B.basicList[0].estDate}}| 成立时间 | {{B.basicList[0].estDate}} |{{/if}}
{{#if B.basicList[0].regAddr}}| 注册地址 | {{B.basicList[0].regAddr}} |{{/if}}
{{#if D.operating_address}}| 实际经营地址 | {{D.operating_address}} |{{/if}}
{{#if B.basicList[0].regCap}}| 注册资本 | {{B.basicList[0].regCap}} {{B.basicList[0].regCapCur}} |{{/if}}
{{#if B.basicList[0].paidInCap}}| 实缴资本 | {{B.basicList[0].paidInCap}} |{{/if}}
{{#if B.basicList[0].orgType}}| 企业性质 | {{B.basicList[0].orgType}} |{{/if}}
{{#if D.employee_scale}}| 员工规模 | {{D.employee_scale}} |{{/if}}
{{#if B.basicList[0].industry}}| 所属行业 | {{B.basicList[0].industry}} |{{/if}}
{{#if D.qualifications}}| 企业资质 | {{D.qualifications}} |{{/if}}

{{#if D.basic_interpretation}}信息解读：

{{D.basic_interpretation}}{{/if}}

—————————————————数据来源————————————————

水滴 MCP（工商登记、企业年报、荣誉资质）｜查询时间：{{META.generated_at}}
{{/if}}

{{#if B.personList}}
### （二）关键决策人信息

{{#each B.personList|max=8}}
- **{{perName}}：** {{position}}{{#if isFr}}；法定代表人标识：{{isFr}}{{/if}}
{{/each}}

{{#if D.people_interpretation}}信息解读：{{D.people_interpretation}}{{/if}}

—————————————————数据来源————————————————

水滴 MCP（工商登记主要人员信息）｜查询时间：{{META.generated_at}}
{{/if}}

{{#if D.has_equity_or_network}}
### （三）股权结构与关联关系

{{#if B.shareholderList}}
| 股东名称 | 持股比例 | 出资额（万元） |
| --- | --- | --- |
{{#each B.shareholderList|max=15}}| {{shareholderName}} | {{fundedRatio}} | {{subConAmt}}{{#if subConCur}} {{subConCur}}{{/if}} |{{/each}}
{{/if}}

{{#if D.network_summary}}关联关系：{{D.network_summary}}{{/if}}

{{#if D.equity_interpretation}}信息解读：{{D.equity_interpretation}}{{/if}}

—————————————————数据来源————————————————

水滴 MCP（工商股东、分支机构、对外投资和网站信息）｜查询时间：{{META.generated_at}}
{{/if}}

{{#if D.has_assets}}
### （四）企业资产状况

{{#if D.tangible_assets}}有形资产：

{{D.tangible_assets}}{{/if}}

{{#if D.has_intangible_assets}}无形资产：

| 类型 | 数量 | 核心内容 | 取得方式 |
| --- | --- | --- | --- |
{{#if IP.patentsListMeta.totalCount}}| 专利 | {{IP.patentsListMeta.totalCount}} | {{D.patent_representatives}} | 本次未核验 |{{/if}}
{{#if SW.swListMeta.totalCount}}| 软件著作权 | {{SW.swListMeta.totalCount}} | {{D.software_representatives}} | 本次未核验 |{{/if}}
{{#if WC.resultListMeta.totalCount}}| 作品著作权 | {{WC.resultListMeta.totalCount}} | {{D.work_representatives}} | 本次未核验 |{{/if}}
{{#if TM.brandListMeta.totalCount}}| 商标 | {{TM.brandListMeta.totalCount}} | {{D.trademark_representatives}} | 注册信息 |{{/if}}
{{#if ICP.icpListMeta.totalCount}}| ICP 备案 | {{ICP.icpListMeta.totalCount}} | {{D.icp_representatives}} | 备案信息 |{{/if}}
{{#if LIC.detailListMeta.totalCount}}| 工商许可 | {{LIC.detailListMeta.totalCount}} | {{D.license_representatives}} | 许可信息 |{{/if}}
{{#if D.honor_count}}| 荣誉资质 | 本次返回 {{D.honor_count}} 项 | {{D.honor_representatives}} | 公示信息 |{{/if}}
{{/if}}

{{#if D.assets_interpretation}}信息解读：{{D.assets_interpretation}}{{/if}}

—————————————————数据来源————————————————

水滴 MCP（知识产权、ICP备案、工商许可和荣誉资质）｜查询时间：{{META.generated_at}}
{{/if}}

{{#if D.has_core_operations}}
### （五）核心经营数据

| 指标 | 数据 | 行业参考 | 评价 |
| --- | --- | --- | --- |
{{#if D.employee_scale}}| 员工规模 | {{D.employee_scale}} | 本次未核验 | 本次不评价 |{{/if}}
{{#if D.branch_summary}}| 分支机构 | {{D.branch_summary}} | 本次未核验 | 本次不评价 |{{/if}}
{{#if D.website_summary}}| 网站与 ICP | {{D.website_summary}} | 本次未核验 | 本次不评价 |{{/if}}
{{#if D.recent_public_activity}}| 近期公开动态 | {{D.recent_public_activity}} | 本次未核验 | 本次不评价 |{{/if}}

{{#if D.operations_interpretation}}信息解读：{{D.operations_interpretation}}{{/if}}

—————————————————数据来源————————————————

水滴 MCP（企业年报、分支机构、网站备案和近 90 天公开舆情线索）｜查询时间：{{META.generated_at}}
{{/if}}
{{/if}}

{{#if D.has_industry_insight}}
## 四、产业画像与行业洞察

{{#if D.industry_chain}}
### （一）产业链定位

{{D.industry_chain}}
{{/if}}

{{#if D.industry_outlook}}
### （二）行业景气度

{{D.industry_outlook}}
{{/if}}

{{#if D.industry_benchmark}}
### （三）行业对标

{{D.industry_benchmark}}
{{/if}}

{{#if D.industry_risk}}
### （四）行业风险

{{D.industry_risk}}
{{/if}}
{{/if}}

{{#if D.has_internal_bank_data}}
## 五、与我行合作现状

{{#if D.cooperation_overview}}
### （一）合作概况

{{D.cooperation_overview}}
{{/if}}

{{#if D.credit_cooperation}}
### （二）信贷业务合作

{{D.credit_cooperation}}
{{/if}}

{{#if D.deposit_cooperation}}
### （三）存款业务合作

{{D.deposit_cooperation}}
{{/if}}

{{#if D.payroll_cooperation}}
### （四）代发业务合作

{{D.payroll_cooperation}}
{{/if}}
{{/if}}

{{#if D.has_visit_questions}}
## 六、需求识别与产品推荐

### （一）需求智能识别

| 需求类型 | 识别依据 | 紧迫度 |
| --- | --- | --- |
{{#each D.visit_questions}}| {{topic}}（待核实） | {{basis}}；建议现场核实：{{question}} | 本次不评级 |{{/each}}

{{#if D.has_product_match}}
### （二）产品精准匹配

{{D.product_match}}
{{/if}}

{{#if D.has_marketing_plan}}
### （三）定制化营销方案

{{D.marketing_plan}}
{{/if}}
{{/if}}

{{#if D.has_risks}}
## 七、风险预警与合规提示

| 风险维度 | 本次结果 | 关键事实 | 范围 |
| --- | --- | --- | --- |
{{#each D.risks}}| {{topic}} | {{result}} | {{detail}} | {{scope}} |{{/each}}

{{#if D.market_competition_risk}}
### （一）市场竞争风险

风险等级：本次不评级

{{D.market_competition_risk}}

应对建议：{{D.market_competition_question}}
{{/if}}

{{#if D.technology_iteration_risk}}
### （二）技术迭代风险

风险等级：本次不评级

{{D.technology_iteration_risk}}

应对建议：{{D.technology_iteration_question}}
{{/if}}

{{#if D.financial_transparency_risk}}
### （三）财务信息不透明风险

风险等级：本次不评级

{{D.financial_transparency_risk}}

应对建议：{{D.financial_transparency_question}}
{{/if}}

{{#if D.customer_concentration_risk}}
### （四）客户集中度风险

风险等级：本次不评级

{{D.customer_concentration_risk}}

应对建议：{{D.customer_concentration_question}}
{{/if}}

{{#if D.talent_competition_risk}}
### （五）人才竞争风险

风险等级：本次不评级

{{D.talent_competition_risk}}

应对建议：{{D.talent_competition_question}}
{{/if}}

—————————————————数据来源————————————————

水滴 MCP（工商风险事实与近 90 天公开舆情线索）｜查询时间：{{META.generated_at}}
{{/if}}

## 报告使用说明

- 报告目的：本报告仅为对公客户经理拜访前准备和沟通参考使用，不作为授信审批的最终依据。
- 信息真实性：报告仅基于查询时点水滴 MCP 返回的公开数据生成；空结果、字段缺失和查询失败均不等同于不存在相关事实，建议在拜访中核实关键信息。
- 数据时效性：报告生成后如发生重大变化，建议重新查询并生成报告。
- 保密义务：本报告涉及企业信息，接收方应按所在机构制度妥善保管，未经授权不得对外泄露。

数据边界：成功维度：{{META.successful_dimensions}}{{#if META.empty_dimensions}}；空结果维度：{{META.empty_dimensions}}{{/if}}{{#if META.failed_dimensions}}；未完成维度：{{META.failed_dimensions}}{{/if}}
```

### 标题白名单

最终报告只能出现上方骨架已有标题。以下标题名称必须逐字使用，禁止同义替换：

- `对公客户访前一页纸`
- `一、核心观点`
- `二、执行摘要`
- `三、客户全景画像`
- `（一）企业基本信息`
- `（二）关键决策人信息`
- `（三）股权结构与关联关系`
- `（四）企业资产状况`
- `（五）核心经营数据`
- `四、产业画像与行业洞察`
- `（一）产业链定位`
- `（二）行业景气度`
- `（三）行业对标`
- `（四）行业风险`
- `五、与我行合作现状`
- `（一）合作概况`
- `（二）信贷业务合作`
- `（三）存款业务合作`
- `（四）代发业务合作`
- `六、需求识别与产品推荐`
- `（一）需求智能识别`
- `（二）产品精准匹配`
- `（三）定制化营销方案`
- `七、风险预警与合规提示`
- `（一）市场竞争风险`
- `（二）技术迭代风险`
- `（三）财务信息不透明风险`
- `（四）客户集中度风险`
- `（五）人才竞争风险`
- `报告使用说明`

## 文档生成

默认 `--format pdf`。先依据统一证据模型形成完整 Markdown 内容，再由调用本 Skill 的模型直接使用当前环境可用的文档与 PDF 能力创建成品；不得依赖本 Skill 内嵌代码、固定脚本或外部模板。允许模型按当前环境选择 DOCX 中转、直接生成 PDF 或其他可靠路径，但不同格式必须复用同一证据模型和条件删除结果。

### 固定版式

- 页面：Letter，215.9 × 279.4 mm；上、下页边距 20 mm，左、右页边距 25 mm。
- 正文：宋体或可用的等价中文宋体，10.5 pt，单倍行距；表格正文 9 pt。
- 标题：黑体或等价中文黑体；主标题 18 pt 黑色居中，一级标题 14 pt、二级标题 12 pt，标题蓝色 `#4F81BD`。
- 元信息：报告编号、生成时间、密级使用 9 pt 居中；客户名称使用 12 pt 加粗居中。
- 数据来源：板块末尾加入灰色 `#808080` 居中分隔线及“水滴 MCP（数据维度）｜查询时间：{query_time}”。
- 表格：黑色 0.5 pt 网格线，单元格垂直居中，表头加粗并跨页重复；数据行不得跨页拆分。
- 标题与其后首段或首表保持同页；不得出现裁切、重叠、乱码、孤悬标题或异常大段空白。
- “一页纸”是产品名称，不强制压缩到一页。

表格列宽按可用正文宽度 165.9 mm 固定分配：

| 表格 | 列宽（mm） |
| --- | --- |
| 企业基本信息 | 35 / 130.9 |
| 股东 | 84 / 32 / 49.9 |
| 企业资产状况 | 31 / 24 / 70 / 40.9 |
| 核心经营数据 | 34 / 44 / 44 / 43.9 |
| 需求智能识别 | 40 / 90 / 35.9 |
| 风险预警 | 34 / 29 / 76 / 26.9 |

### 生成与验收

1. 先按“报告输出格式（严格填空骨架 · 模型只填值、不造结构）”替换占位符并执行预定义条件；不得自行调整章节编号或标题，再开始排版。
2. 使用当前环境已有的文档、DOCX 或 PDF 创建能力生成 `output/pdf/{company_name}-公司访前一页纸.pdf`。如需 DOCX 中间文件，只把它作为本次临时产物。
3. 逐页渲染或预览最终 PDF，检查中文字体、页面尺寸、页边距、标题层级、表格换页、裁切、重叠和空白。
4. 验收通过后删除本次临时 JSON、DOCX、预览图片及一次性辅助文件，只保留最终 PDF。
5. 不把生成过程中临时编写的代码、命令或内部证据 JSON写入报告或聊天回复。
6. 当前环境无法创建或验收 PDF、中文字体不可用或转换失败时，不循环重试；删除不完整文件并回退完整 Markdown，说明“PDF 生成未完成：{原因}，已回退 Markdown”。

## Markdown 回退

用户指定 `--format md`，或 PDF 流程失败时，直接按“报告输出格式（严格填空骨架 · 模型只填值、不造结构）”输出。Markdown 与 PDF 必须复用同一证据模型中的原值和条件结果。

聊天回复只包含：

- 企业规范全称；
- 查询日期；
- 生成格式；
- 最重要的 1 至 3 条数据边界；
- PDF 的绝对路径链接，或完整 Markdown 正文。

## 输出纪律

1. 使用中文，用户明确要求其他语言时除外。
2. 标题和编号逐字使用固定骨架。条件板块隐藏后不得连续重编号；不得出现空标题、空表或整排“未披露”。
3. 事实与访谈建议分开。建议使用“建议核实”“可重点了解”，不写“应授信”“建议放款”“可合作”等结论。
4. 报告中统一写“水滴 MCP”，不得写 CISP、产品码、工具名或字段路径。
5. 当前水滴 MCP 唯一数据源模式固定不展示“四、产业画像与行业洞察”“五、与我行合作现状”、授信/存款/代发明细和具体银行产品推荐。
6. “一页纸”是报告产品名称，不限制总页数；内容随有效数据自动增减。
7. 最终 PDF 必须经过逐页渲染验收；无法验收时不得交付 PDF，直接回退 Markdown。

---

**SKILL 版本**：v1.3
**适配数据源**：连接标识为 `cisp-mcp` 的水滴 MCP 当前 17 工具版本
**页面规格**：Letter 215.9 × 279.4 mm
**默认交付**：PDF，失败回退 Markdown
