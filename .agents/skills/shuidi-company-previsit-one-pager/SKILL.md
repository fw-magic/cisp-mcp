---
name: shuidi-company-previsit-one-pager
description: 使用水滴 MCP 的工商深度、知识产权、ICP备案、行政许可、荣誉资质和企业舆情工具，为指定中国企业生成严格基于接口事实的“对公客户访前一页纸”，默认交付 Letter 尺寸 PDF，无法生成 PDF 时回退完整 Markdown。适用于对公客户经理访前准备、企业拜访简报、客户全景画像、拜访问题清单、合作前背景了解，以及用户提出“公司访前一页纸”“客户访前报告”“拜访前帮我了解这家公司”“生成访前 PDF”等请求。
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

**命令**：`/shuidi-company-previsit-one-pager`  
**数据源**：水滴 MCP  
**默认格式**：`pdf`  
**报告定位**：访前准备，不构成授信、法律、财务、投资或准入结论

---

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

## 工具绑定

| 业务维度 | 水滴 MCP 工具 | 调用约定 |
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
- 缺失字段：删除所在行；整块无有效内容时删除整块并连续编号。

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
  "report": {
    "report_id": "CP-YYYYMMDD-HHMMSS",
    "generated_at": "YYYY-MM-DD HH:MM:SS",
    "classification": "机密",
    "company_name": "规范企业全称",
    "credit_code": "统一社会信用代码"
  },
  "core_view": "只含直接证据的一段核心观点",
  "summary": {
    "value_judgment": "登记、行业、资质和资产事实摘要",
    "opportunities": "仅基于正面舆情、有效荣誉或业务范围的访谈线索",
    "risks": "只陈述命中风险维度和数量",
    "visit_advice": "基于已有事实形成的访前沟通建议"
  },
  "basic": [{"label": "企业全称", "value": "原值"}],
  "people": [{"name": "姓名", "position": "职务", "note": "仅接口可证事实"}],
  "shareholders": [{"name": "股东名称", "ratio": "原始比例", "amount": "原始认缴信息"}],
  "assets": [{"type": "专利", "count": "原始总量", "representative": "首批代表记录", "status": "状态或口径"}],
  "news": [{"date": "发布时间", "emotion": "情感标签", "title": "标题", "source": "来源"}],
  "visit_questions": [{"topic": "核验主题", "basis": "MCP 已有事实或数据缺口", "question": "现场建议核实的问题"}],
  "risks": [{"topic": "风险维度", "result": "原始数量/状态", "detail": "关键事实", "scope": "目标企业自身或舆情线索"}],
  "evidence": {
    "successful": ["工商深度"],
    "empty": [],
    "failed": [],
    "query_time": "YYYY-MM-DD HH:MM:SS"
  }
}
```

整理规则：

- `basic` 只保留非空字段；注册资本按 `regCap + regCapCur` 原样组合。
- 股东最多展示 15 名。比例可解析时仅用于排序，展示仍使用原字符串；不可解析时保持接口顺序。
- 主要人员最多 8 名；不得补写教育、履历、创始人身份或实际控制关系。
- 各资产最多展示 3 个首批返回名称；总量使用分页元数据。
- 荣誉资质只能写“本次返回 N 项”，不得称全量。
- 舆情最多展示 5 条，保留标题、日期、来源和接口情感标签。
- 风险只写目标企业自身记录；关联主体记录必须单独标明范围。
- `visit_questions` 可询问主营收入结构、客户集中度、现金流、融资需求、研发投入和合作诉求，但不得预设答案或推荐具体银行产品。

## 报告骨架

按有效内容连续编号。以下板块无有效数据时删除整块。

```markdown
# 对公客户访前一页纸

报告编号：{report_id}  ｜  生成时间：{generated_at}  ｜  密级：机密

客户名称：{company_name}

## 一、核心观点

{core_view}

## 二、执行摘要

**核心价值判断：** {value_judgment}

**主要机会：** {opportunities}

**主要风险：** {risks}

**拜访建议：** {visit_advice}

## 三、客户全景画像

### （一）企业基本信息

{basic 两列表}

### （二）关键人员信息

{people 列表}

### （三）股权结构与经营网络

{shareholders 三列表；分支、投资和网站事实摘要}

### （四）无形资产与资质

{assets 四列表}

### （五）近期公开动态

{news 四列表}

## 四、拜访核验重点

{visit_questions 三列表}

## 五、风险预警与合规提示

{risks 四列表}

## 报告使用说明

- 本报告仅用于客户经理访前准备和沟通参考，不作为授信审批或其他专业决策依据。
- 本报告基于查询时点水滴 MCP 返回的公开数据；空结果、字段缺失和查询失败均不等同于不存在相关事实。
- 关键经营、财务和合作信息应在拜访中由客户经理进一步核实。
- 本报告涉及企业信息，接收方应按所在机构制度妥善保管。
```

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
| 关键人员 | 38 / 48 / 79.9 |
| 股东 | 84 / 32 / 49.9 |
| 无形资产与资质 | 31 / 24 / 70 / 40.9 |
| 近期公开动态 | 32 / 20 / 84 / 29.9 |
| 拜访核验重点 | 32 / 62 / 71.9 |
| 风险预警 | 34 / 29 / 76 / 26.9 |

### 生成与验收

1. 先按“报告骨架”完成内容，执行空字段、空行、空板块删除及连续编号，再开始排版。
2. 使用当前环境已有的文档、DOCX 或 PDF 创建能力生成 `output/pdf/{company_name}-公司访前一页纸.pdf`。如需 DOCX 中间文件，只把它作为本次临时产物。
3. 逐页渲染或预览最终 PDF，检查中文字体、页面尺寸、页边距、标题层级、表格换页、裁切、重叠和空白。
4. 验收通过后删除本次临时 JSON、DOCX、预览图片及一次性辅助文件，只保留最终 PDF。
5. 不把生成过程中临时编写的代码、命令或内部证据 JSON写入报告或聊天回复。
6. 当前环境无法创建或验收 PDF、中文字体不可用或转换失败时，不循环重试；删除不完整文件并回退完整 Markdown，说明“PDF 生成未完成：{原因}，已回退 Markdown”。

## Markdown 回退

用户指定 `--format md`，或 PDF 流程失败时，直接按“报告骨架”输出。Markdown 与 PDF 必须复用同一证据模型中的原值和条件删除结果。

聊天回复只包含：

- 企业规范全称；
- 查询日期；
- 生成格式；
- 最重要的 1 至 3 条数据边界；
- PDF 的绝对路径链接，或完整 Markdown 正文。

## 输出纪律

1. 使用中文，用户明确要求其他语言时除外。
2. 一级章节按实际保留内容连续编号；不得出现空标题、空表或整排“未披露”。
3. 事实与访谈建议分开。建议使用“建议核实”“可重点了解”，不写“应授信”“建议放款”“可合作”等结论。
4. 报告中统一写“水滴 MCP”，不得写 CISP、产品码、工具名或字段路径。
5. 不展示“产业画像与行业对标”“与我行合作现状”、授信/存款/代发明细和具体银行产品推荐。
6. “一页纸”是报告产品名称，不限制总页数；内容随有效数据自动增减。
7. 最终 PDF 必须经过逐页渲染验收；无法验收时不得交付 PDF，直接回退 Markdown。

---

**SKILL 版本**：v1.1  
**适配数据源**：水滴 MCP 当前 17 工具版本  
**页面规格**：Letter 215.9 × 279.4 mm  
**默认交付**：PDF，失败回退 Markdown
