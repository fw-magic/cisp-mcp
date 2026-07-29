---
name: shuidi-company-previsit-one-pager
description: 使用客户 Agent 中连接标识为 cisp-mcp 的水滴 MCP 工商深度、企业简述、土地资产、知识产权、ICP备案、行政许可、荣誉资质和企业舆情工具，为指定中国企业生成严格基于接口事实的“对公客户访前一页纸”，默认交付 Letter 尺寸 PDF，无法生成 PDF 时回退完整 Markdown。适用于对公客户经理访前准备、企业拜访简报、客户全景画像、拜访问题清单、合作前背景了解，以及用户提出“公司访前一页纸”“客户访前报告”“拜访前帮我了解这家公司”“生成访前 PDF”等请求。
---

> 水滴 MCP 公司访前一页纸。
>
> 面向对公客户经理的访前准备工具。输入企业名称或统一社会信用代码，自动锚定主体，整合工商登记、主要人员、股权、土地资产、知识产权、许可资质、近期公开动态和风险事实，生成与标准成品一致的紧凑 Letter 版式报告。
>
> 核心能力：
> - 主体工商核验与经营范围事实摘要
> - 主要人员、股东和经营网络速览
> - 土地供应、土地出让和土地抵押公开记录概述
> - 专利、商标、软件著作权、作品著作权、ICP、许可和荣誉资质盘点
> - 近 90 天公开舆情中的机会线索与风险线索
> - 把 MCP 未覆盖的经营、财务和合作信息转成拜访核验问题
> - 按企业画像产品的固定字段和顺序生成确定性企业简述，并生成审慎的信息解读
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
3. `B`、`ID`、`OV_*`、`LAND`、`TM` 至 `OP` 中的金额、比例、日期、数量和币种必须逐字保存。报告展示层允许做无损格式化，但禁止四舍五入、补零、截断有效小数、换算、加总、相减、相乘或倒算；仅“有形资产生成规则”允许对分页完整、记录数一致、字段均为有效数字且单位一致的同一土地类别做高精度十进制加总。
4. 不根据股东、任职或投资关系推导实际控制人、最终受益人、一致行动关系、融资轮次或资本市场状态。
5. 分页接口以 `*ListMeta.totalCount` 表示总量；第一页记录只称“本次首批返回记录”，不得称为“最新”或“全部”。
6. 空数组只表示“本次查询未返回相关公开记录”；调用失败表示“该维度查询未完成”。两者不得互换。
7. 舆情只称“公开舆情线索”，不得升级为已经核验的司法、监管或经营事实。
8. 报告正文不得出现工具代码、产品码、JSON 路径、schema、调用失败堆栈、额度或积分信息。
9. 不输出身份证号、手机号、API Key、原始响应或非必要个人敏感信息。
10. 不生成营收、利润、市场份额、客户数量、融资金额、授信、存款、代发、贷款建议或银行产品推荐，除非接口直接返回对应事实；本 skill 当前固定不展示这些板块。
11. 大模型可以归纳、压缩和组织本次 MCP 证据，但不得把数据缺口改写成事实，不得把公开舆情标题升级为目标企业已经实施的业务动作。
12. 未被接口直接支持时，禁止使用“行业领先”“头部企业”“绝对控股”“经营健康”“优质客户”“资本实力强”“建议授信”等判断性表述。
13. 每个大模型派生文案必须在内部证据映射 `EVIDENCE` 中列出至少一个来源字段或查询状态；`EVIDENCE` 仅用于生成与验收，不写入报告。
14. `D.company_overview` 必须按本 Skill 的确定性规则拼接，不得交给大模型自由改写；空字段、非数字风险字段、空结果和失败维度不得改写成“无”。
15. 内部执行可以使用产品、接口和查询术语；最终报告必须改写为业务语言，不得出现“返回”“未取得”“取得”“查询成功”“查询失败”“首批返回”“本次查询”“接口”“字段”“空结果”“统计口径”等数据调用表述。商业事件中的“取得订单”改写为“获得订单”。

## `cisp-mcp` 工具绑定

下表中的工具必须全部从连接标识为 `cisp-mcp` 的 MCP Server 解析。

| 业务维度 | `cisp-mcp` 工具 | 调用约定 |
| --- | --- | --- |
| 主体消歧 | `p0010068_fuzzy_search_company_name` | 参数 `ent_name`；仅简称、品牌名或可能重名时调用 |
| 工商深度 | `p0010058_query_business_basic_deep` | 必选；按输入类型四选一：企业名称用 `ent_name`，统一社会信用代码用 `credit_code`，注册号用 `reg_no`，组织机构代码用 `org_code` |
| 企业 ID 解析 | `p0010010_query_business_profile` | `ent_info=规范企业全称`；从 `orgName` 准确匹配且 `creditCode` 一致的 `basicList[]` 记录获取 `entId`，不得自行推算 |
| 简述基本信息 | `p0980006_query_advanced_company_filter` | 取得 `entId` 后调用：`eid=entId`，`page_no="1"`，`page_size="1"` |
| 简述工商补充 | `p0010059_query_business_basic_brief` | 优先 `credit_code=工商深度信用代码`，缺失时使用 `ent_name=规范企业全称`；严格二选一，`types=["basic"]` |
| 简述资本与经营线索 | `p0980033_query_listing_financing_bidding_ipr` | `ent_info` 优先传 `entId`，无法取得时回退规范企业全称 |
| 简述纳税评级 | `p0980008_query_tax_rating` | 仅在取得 `entId` 后调用：`eid=entId` |
| 简述近两年风险 | `p0980023_query_two_year_risk_summary` | 仅在取得 `entId` 后调用：`eid=entId` |
| 土地资产 | `p0130036_query_land_info` | `ent_info=规范企业全称`；分别以 `land_type="tdgy"`、`"tdcr"`、`"tddy"` 调用，`page_no="1"`、`page_size="10"`，再按各类别页数完成分页；默认不查询 `dkgs` |
| 商标 | `p0010073_query_trademark_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 专利 | `p0010078_query_patent_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 软件著作权 | `p0010074_query_software_copyright_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 作品著作权 | `p0010075_query_work_copyright_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| ICP 备案 | `p0010076_query_icp_filing_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 工商许可 | `p0010084_query_license_info` | `ent_info=规范企业全称`，`license_type="gs"`，`page_no="1"`，`page_size="5"` |
| 荣誉资质 | `p0110003_query_honor_qualification_info` | `ent_info=规范企业全称`；使用本次返回列表，不宣称全量 |
| 近期舆情 | `p0050007_p0050008_query_public_opinion_info` | `ent_name=规范企业全称`；最近 90 个自然日，`page_size="10"`，`max_details=5` |

**参数名注意**：主体消歧使用 `ent_name`。工商深度按输入类型使用 `ent_name`、`credit_code`、`reg_no` 或 `org_code`。企业 ID 解析使用 `ent_info`。简述工商补充严格使用 `credit_code` 或 `ent_name` 之一。简述基本信息、纳税和近两年风险使用 `eid`。简述资本与经营线索使用 `ent_info`，但值优先为已核验的 `entId`。舆情使用 `ent_name`。土地资产、商标、专利、软件著作权、作品著作权、ICP、许可和荣誉资质使用 `ent_info`。参数名不得跨工具混用。

不要调用通用网关 `query_cisp_product` 替代专用工具。不要默认调用二要素、三要素核验或单点关联工具。

## 字段别名

模板和内部证据整理使用以下短别名。别名只用于执行和模板，不写入客户报告。

| 别名 | 工具数据根路径 |
| --- | --- |
| `B` | `p0010058_query_business_basic_deep.data` |
| `ID` | `p0010010_query_business_profile.data` |
| `OV_BASIC` | `p0980006_query_advanced_company_filter.data` |
| `OV_BRIEF` | `p0010059_query_business_basic_brief.data` |
| `OV_MARKET` | `p0980033_query_listing_financing_bidding_ipr.data` |
| `OV_TAX` | `p0980008_query_tax_rating.data` |
| `OV_RISK` | `p0980023_query_two_year_risk_summary.data` |
| `LAND` | `p0130036_query_land_info.data` 按 `tdgy`、`tdcr`、`tddy` 分类保存的分页原值、合并记录和独立状态 |
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
- 确定性企业概述：`{{D.company_overview}}`
- 动态大章节编号：`{{D.section_numbers.core}}`、`{{D.section_numbers.summary}}`、`{{D.section_numbers.profile}}`、`{{D.section_numbers.needs}}`、`{{D.section_numbers.risk}}`
- 缺失字段：删除所在行；整块无有效内容时仅按骨架中的预定义条件隐藏。条件隐藏完成后按实际可见顺序连续重编号大章节，小节编号保持不变。

### 关键字段映射

| 展示项 | 字段 |
| --- | --- |
| 企业全称、信用代码、状态、法定代表人 | `B.basicList[0].orgName`, `creditCode`, `orgStatus`, `legRepName` |
| 企业内部 ID | `ID.basicList[].orgName`, `creditCode`, `entId` |
| 简述基本信息 | `OV_BASIC.entList[0].orgName`, `province`, `entScaleName`, `industry`, `regCap`, `regCapCur`；`OV_BRIEF.basicList[0].orgNameUsed`, `estDate`, `paidInCap` |
| 上市、退市、融资 | `OV_MARKET.data[0].listed[]`, `deListed[]` 的 `listdate`, `trademarket`, `securitycode`；`investmentFin[]` 的 `fundingstatus`, `latestroundname`, `investment` |
| 招投标、知识产权 | `OV_MARKET.data[0].callBid.countBid/overBid/ingBid`；`winBid.outBid/outBidAmount/zfOutBid/zfOutBidAmount`；`ipr.brand/patent/copyright` |
| 纳税评级 | `OV_TAX.list[].year`, `rating` |
| 近两年风险统计 | `OV_RISK.list[0].collect15/collect1/collect2/collect3/collect4/collect5/collect7/collect10/collect8/collect9/collect11/collect12/collect13` |
| 成立、类型、资本、地址、行业、范围 | `estDate`, `orgType`, `regCap`, `regCapCur`, `paidInCap`, `regAddr`, `industry`, `operateScope` |
| 土地资产背景 | `B.basicList[0].industryClas`, `industry`, `operateScope`, `regAddr` |
| 土地供应 | `LAND.tdgy.records[].district`, `projectName`, `landPosition`, `purposes`, `supplyArea`, `transactionPrice`, `contractDate`, `yearLimit` |
| 土地出让 | `LAND.tdcr.records[].district`, `projectName`, `landPosition`, `landUse`, `landArea`, `transactionPrice`, `pubDate`, `yearLimit`, `landNo` |
| 土地抵押 | `LAND.tddy.records[].administrativeArea`, `address`, `landNo`, `acreage`, `mortgageAcreage`, `mortgagePrice`, `mortgagorName`, `mortgageName`, `boardStartDate`, `boardEndDate`, `pubDate` |
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
5. 主体确认后调用 `p0010010_query_business_profile(ent_info=规范企业全称)`。只接受 `ID.basicList[]` 中 `orgName` 与规范企业全称完全一致、且双方信用代码均非空时 `creditCode` 也完全一致的记录；从该记录读取 `entId`。不得从信用代码、注册号或其他字段拼接、截取或推算 `entId`。
6. 企业 ID 解析失败、空结果或没有准确匹配时，将企业 ID、企业高级筛选、纳税评级和近两年风险维度记为 `failed`，但继续使用工商深度和不依赖 ID 的扩展维度生成报告。

### 2. 查询扩展维度

主体确认后，按以下依赖关系调用扩展维度：

1. `P0010059` 不依赖 `entId`：优先以 `B.basicList[0].creditCode` 调用；信用代码为空时才以规范企业全称调用；固定 `types=["basic"]`。
2. 成功取得 `entId` 后，并行调用 `P0980006`、`P0980008` 和 `P0980023`。`P0980006` 固定 `page_no="1"`、`page_size="1"`，并校验返回 `entList[0].eid` 与请求 `entId` 一致；不一致时该维度记为 `failed`。
3. `P0980033` 的 `ent_info` 优先传已核验的 `entId`；无法取得 `entId` 时回退规范企业全称。
4. 同时并行调用土地资产、商标、专利、软件著作权、作品著作权、ICP、工商许可、荣誉资质和近 90 天舆情。土地资产以规范企业全称分别调用 `land_type="tdgy"`、`"tdcr"`、`"tddy"`，三类第一页均固定 `page_no="1"`、`page_size="10"`；默认不调用 `dkgs`。舆情日期使用执行日为 `end_date`，向前推 90 个自然日为 `start_date`，格式 `yyyy-MM-dd`，不设置情感过滤。
5. 土地供应读取 `detailListMeta.tdgyPageNum`，土地出让读取 `detailListMeta.tdcrPageNum`，土地抵押读取 `detailListMeta.tddyPageNum`。类别页数为有效正整数且大于 1 时，以相同 `ent_info`、`land_type` 和 `page_size` 继续请求第 2 页至末页。不得使用聚合的 `totalPage` 代替类别页数，不得因其他类别还有页数而重复请求当前类别。
6. 土地三类结果和状态相互独立：任一类别失败只将该类别记为 `failed`；成功但对应结果列表为空记为 `empty`；成功且存在有效记录记为 `success`。土地供应、土地出让、土地抵押分别进入 `META`，不得用一个汇总状态覆盖另外两类。

记录每个维度的状态：

- `success`：成功且有有效数据；
- `empty`：成功但返回空列表或无结果；
- `failed`：工具不可用、超时、权限不足或调用失败。

`META.successful_dimensions` 只列 `success` 维度，`META.empty_dimensions` 只列 `empty` 维度，`META.failed_dimensions` 只列 `failed` 维度；同一维度不得重复出现在多个状态字段中。

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
  "ID": "企业工商照面工具 data 原值",
  "OV_BASIC": "企业高级筛选工具 data 原值",
  "OV_BRIEF": "工商简项工具 data 原值",
  "OV_MARKET": "上市投融资招投标知识产权工具 data 原值",
  "OV_TAX": "纳税评级工具 data 原值",
  "OV_RISK": "近两年风险统计工具 data 原值",
  "LAND": {
    "tdgy": {"status": "success|empty|failed", "pages": ["每页 data 原值"], "records": ["合并后的 tdgyResults 原值"]},
    "tdcr": {"status": "success|empty|failed", "pages": ["每页 data 原值"], "records": ["合并后的 tdcrResults 原值"]},
    "tddy": {"status": "success|empty|failed", "pages": ["每页 data 原值"], "records": ["合并后的 tddyResults 原值"]}
  },
  "TM": "商标工具 data 原值",
  "IP": "专利工具 data 原值",
  "SW": "软件著作权工具 data 原值",
  "WC": "作品著作权工具 data 原值",
  "ICP": "ICP备案工具 data 原值",
  "LIC": "工商许可工具 data 原值",
  "HON": "荣誉资质工具 data 原值",
  "OP": "舆情工具完整返回原值",
  "D": {
    "brand_name": null,
    "registered_capital_display": "注册资本和币种原值的可读组合",
    "paid_in_capital_display": null,
    "operating_address": null,
    "employee_scale": null,
    "qualifications": null,
    "source_dimensions": {"basic": "工商登记", "people": null, "equity": null, "assets": null, "operations": null, "risk": null},
    "coverage_summary": "以业务语言概括资料覆盖范围和待补充事项",
    "section_numbers": {"core": "一", "summary": "二", "profile": "三", "needs": "四", "risk": null},
    "company_overview": "按固定字段和固定顺序确定性拼接的企业概述",
    "value_judgment": "企业定位、可见能力信号和拜访价值的事实归纳",
    "opportunities": "目标企业自身公开事件、有效荣誉、许可或业务范围形成的访谈机会线索",
    "risk_summary": "命中风险维度、数量、范围和数据边界的摘要",
    "visit_advice": "基于已有事实形成的访前沟通主线和核验重点",
    "basic_interpretation": "基本登记事实与访前含义",
    "person_representatives": [],
    "people_interpretation": null,
    "has_equity_or_network": false,
    "shareholder_rows": [],
    "network_summary": null,
    "equity_interpretation": null,
    "has_assets": false,
    "tangible_assets": null,
    "land_supply_count": null,
    "land_supply_area_total": null,
    "land_supply_price_total": null,
    "land_supply_representative": null,
    "land_transfer_count": null,
    "land_transfer_area_total": null,
    "land_transfer_price_total": null,
    "land_transfer_representative": null,
    "land_mortgage_count": null,
    "land_mortgage_representative": null,
    "has_intangible_assets": false,
    "patent_representatives": null,
    "software_representatives": null,
    "work_representatives": null,
    "trademark_representatives": null,
    "icp_representatives": null,
    "license_representatives": null,
    "honor_count": null,
    "honor_representatives": null,
    "assets_interpretation": null,
    "has_core_operations": false,
    "operations_boundary": null,
    "branch_summary": null,
    "website_summary": null,
    "recent_public_activity": null,
    "operations_interpretation": null,
    "visit_questions": [],
    "has_risks": false,
    "risks": [],
    "risk_zero_dimensions": "以、连接的明确零值维度",
    "risk_interpretation": null
  },
  "EVIDENCE": {
    "company_overview": ["B.basicList[0].orgName", "实际进入简述的 OV_BASIC/OV_BRIEF/OV_MARKET/OV_TAX/OV_RISK 字段"],
    "coverage_summary": ["META 中各业务维度的 success/empty/failed 状态"],
    "tangible_assets": ["实际使用的 B.basicList[0] 与 LAND 字段；若有合计则逐项登记参与计算的原值"],
    "value_judgment": ["直接支持该归纳的字段"],
    "opportunities": ["直接支持该访谈线索的字段或目标企业自身舆情记录"],
    "risk_summary": ["直接支持该风险摘要的列表、数量和范围"],
    "visit_advice": ["支持该沟通主线的事实和数据缺口"],
    "其他 D 文案字段": ["对应事实字段或查询状态"]
  }
}
```

整理规则：

- `B`、`ID`、`OV_*`、`LAND`、`TM` 至 `OP` 保存对应工具原值；`D` 只保存确定性简述、忠实压缩文案、条件布尔值和固定表格所需的派生展示项。
- 工商深度成功后，`D.company_overview`、`D.value_judgment`、`D.opportunities`、`D.risk_summary`、`D.visit_advice`、`D.basic_interpretation` 和 `D.visit_questions` 为必填；不得因生成困难隐藏“一、核心观点”“二、执行摘要”或需求核验问题。
- 完成所有条件板块显隐判断后，按“核心观点 → 执行摘要 → 客户全景画像 → 产业画像与行业洞察（未来可选）→ 与我行合作现状（未来可选）→ 需求识别与拜访核验 → 风险预警与合规提示（可选）”过滤不可见板块，再从“一”开始连续填写 `D.section_numbers`。当前骨架固定得到核心观点“一”、执行摘要“二”、客户全景画像“三”、需求识别与拜访核验“四”；风险章节显示时为“五”。不得跳号、重号或根据历史编号保留空位；“报告使用说明”不编号，小节“（一）～（五）”不参与重编号。
- 其他 `D.has_*` 只在对应板块至少存在一项有效事实时设为 `true`；不得为了保留版面而设为 `true`。
- `D.source_dimensions.*` 只列实际为对应小节提供可见事实的维度，以“、”连接；不得列入 `empty`、`failed` 或未在该小节展示的数据维度。
- 基本信息只保留非空字段。展示层的无损格式化仅包括：纯数字整数部分增加千分位；严格匹配 `YYYY-MM-DD` 的日期显示为“YYYY年M月D日”；曾用名中的半角逗号、全角逗号或分号统一为“、”；已知币种代码显示其接口同时返回的中文名称。必须保留全部有效数字和小数位，不得改变精度；无法可靠识别时直接显示原值。
- `D.registered_capital_display` 使用无损格式化后的 `regCap` 与 `regCapCur` 组合为“金额单位（币种）”；接口明确 `regCap` 单位为万元时追加“万元”，不得重复单位。实缴资本同理。
- 股东最多展示 15 名，整理为 `D.shareholder_rows[] = {name, ratio_display, amount_display}`。比例可解析时仅用于排序；比例、认缴额和币种在展示层只允许上述无损格式化，不可解析时保持接口顺序和原值。
- 主要人员最多展示 8 名，整理为 `D.person_representatives[] = {name, position, is_legal_representative}`。只有 `isFr` 原值明确表示真时，才将布尔字段设为 `true`；`position` 已包含“法定代表人”时，展示层删除重复称谓。`B.personList` 为空但 `B.basicList[0].legRepName` 非空时，生成一条 `{name: legRepName, position: null, is_legal_representative: true}` 作为兜底，并在 `people_interpretation` 中写“工商登记载明法定代表人为{name}；公开资料未披露其履历、决策权限和具体分工，拜访中可确认本次议题的业务、财务及技术决策参与人”。不得补写教育、履历、创始人身份、决策权或实际控制关系。
- 土地资产按下方“有形资产生成规则”处理；其他各资产最多展示 3 个代表名称。总量使用分页元数据，最终报告统一称“代表记录”或“样本记录”。
- 荣誉资质只展示本报告采纳的代表记录数量，不得称全量，不得使用“返回”描述。
- 舆情最多展示 5 条，保留标题、日期、来源和接口情感标签。只有目标企业是事件主体，且标题或详情明确涉及其产品、项目、许可、荣誉、业务动作或风险事项时，才可进入 `D.opportunities`、`D.recent_public_activity` 或风险文案。
- 排除只把目标企业作为概念股、行情标的、行业举例或顺带提及的文章；排除无法确认主体、重复标题和纯市场价格波动内容。
- 风险只写目标企业自身记录；关联主体记录必须单独标明范围。只有明确大于零的统计、非空风险列表或合格的目标企业自身负面舆情才能进入 `D.risks[] = {topic, detail, scope}`；明确为零的近两年风险字段名称按固定顺序以“、”连接后写入 `D.risk_zero_dimensions`，不得进入风险表或写成“无风险”。
- `D.visit_questions[] = {topic, basis, question}`，可询问主营收入结构、客户集中度、现金流、融资需求、研发投入和合作诉求，但不得预设答案或推荐具体银行产品。
- `D.coverage_summary` 只用工商登记、股权、土地资产、知识产权、备案许可、荣誉资质、纳税评级、近期公开动态和近两年风险等业务名称概括资料范围；已覆盖内容写“报告已覆盖……”，无可展示内容写“公开资料中暂无可供展示的……”，调用失败写“相关资料尚待补充”。不得出现企业 ID 解析、工商简项、产品码、工具名、内部别名或查询状态。
- “四、产业画像与行业洞察”“五、与我行合作现状”“（二）产品精准匹配”和“（三）定制化营销方案”不进入当前水滴 MCP 唯一数据源骨架；不得用公开搜索或模型知识恢复这些板块。
- `D.has_risks=true` 时必须生成 `D.risk_interpretation`；只总结命中事实、范围和需核实事项，不评级、不推演未来损失。
- 每个非空 `D` 文案字段都必须在 `EVIDENCE` 中登记来源；来源仅为 `B`、`ID`、`OV_*`、`LAND`、`TM` 至 `OP` 的字段或该维度的 `success`、`empty`、`failed` 状态。

#### 有形资产生成规则

1. `B.basicList[0].industryClas`、`industry`、`operateScope` 和 `regAddr` 只用于说明企业经营及地址背景，不能单独证明企业拥有土地、房屋、厂房或设备；仅当 `LAND` 至少一类存在有效记录，或 `B` 中存在明确的抵押、司法协助等相关事实时，才生成 `D.tangible_assets`。`D.has_assets` 在 `D.tangible_assets` 或任一无形资产事实非空时设为 `true`。
2. `LAND` 各类别按页码顺序合并对应的 `tdgyResults[]`、`tdcrResults[]`、`tddyResults[]`。只删除同一类别内 JSON 内容完全一致的重复对象并保留首次出现项；不得跨土地供应、土地出让和土地抵押类别合并或去重。
3. 文案固定按“经营及地址背景 → 土地供应 → 土地出让 → 土地抵押 → 信息边界”组织。缺少有效事实的中间片段直接省略，不改变其余片段顺序。
4. 土地供应使用 `detailListMeta.tdgyCount` 作为公开记录数，概括 `district`、`purposes` 中有值且去重后的主要区域和用途；最多展示一条代表记录。代表记录按可解析的 `supplyArea` 从大到小选择，面积相同时按有效 `contractDate` 从新到旧选择；用于排序的解析值不得替换报告中的接口原值。
5. 土地出让使用 `detailListMeta.tdcrCount` 作为公开记录数，概括 `district`、`landUse` 中有值且去重后的主要区域和用途；最多展示一条代表记录。代表记录按可解析的 `landArea` 从大到小选择，面积相同时按有效 `pubDate` 从新到旧选择；用于排序的解析值不得替换报告中的接口原值。
6. 土地抵押使用 `detailListMeta.tddyCount` 作为公开记录数，最多展示一条代表记录。代表记录优先按有效 `pubDate`，再按 `boardStartDate` 从新到旧选择；可展示行政区、宗地地址或编号、抵押面积、抵押金额、抵押人、抵押权人和登记起止日期中的有效原值，不得把评估金额改写为抵押金额。
7. 同一类别只有在以下条件全部满足时才允许计算面积或成交价格合计：类别分页已从第 1 页完整获取到类别页数；合并去重后的记录数与对应 `tdgyCount`、`tdcrCount` 或 `tddyCount` 完全一致；参与合计的每条记录均有严格可解析的十进制数值；字段单位完全一致。任一条件不满足时省略该合计，只展示记录数和代表记录。
8. 土地供应只分别合计 `supplyArea` 和 `transactionPrice`，土地出让只分别合计 `landArea` 和 `transactionPrice`；土地抵押不计算面积或金额合计。使用任意精度十进制加法，禁止二进制浮点、舍入、换算或补零；结果使用精确十进制值并删除不必要的末尾零。不得跨类别合计，也不得使用 `dkgsResults[]` 参与任何合计。
9. 土地供应、土地出让只称“公开土地记录”“涉及土地供应/土地出让”，不得称为当前产权、当前持有土地或自有土地。企业所属行业、经营范围和注册地址不得推导为“轻资产”“重资产”“自有房产”“自有厂房”“办公场所租赁”或设备价值。
10. 土地抵押、工商抵押或司法记录明确为空时，只能以边界文案写“公开资料中暂无可供展示的相关记录”，不得写“无抵押”“无查封”或“资产权属清晰”；类别失败时不生成零值结论，只在资料范围中写“相关资料尚待补充”。
11. `D.tangible_assets` 末尾固定补充“房屋产权、厂房及设备账面净值、租赁安排等仍需结合财务报表或企业资料进一步核实。”不得把土地成交价格写成账面价值、评估价值或现值。
12. `EVIDENCE.tangible_assets` 逐项登记实际进入文案的 `B`、`LAND` 字段。存在合计时同时登记类别页数、类别记录数和每一项参与计算的原始数值；没有进入文案的字段不得作为证据。

### 4. 构建确定性企业简述

`D.company_overview` 不由大模型生成。先分别构建以下五个片段，删除空片段后按固定顺序直接连接：

```text
D.company_overview =
    基本信息片段
    + 上市/融资片段
    + 招投标/知识产权片段
    + 纳税片段
    + 近两年风险片段
```

如果所有简介扩展维度均失败或为空，基本信息片段仍必须使用 `B.basicList[0].orgName` 生成“{企业名称}。”，确保最终至少输出“{企业名称}。”。每个非空片段以句号结束，不重复添加句号。

#### 4.1 基本信息片段

1. 以 `B.basicList[0].orgName` 开头。
2. `OV_BRIEF.basicList[0]` 只接受企业名称或信用代码与主体锚点一致的记录。有 `orgNameUsed` 时紧接企业名称拼接“（曾用名：{无损格式化后的orgNameUsed}）”，企业名称和左括号之间不得出现逗号；有 `estDate` 时拼接“，成立于{无损格式化后的estDate}”。
3. `OV_BASIC.entList[0]` 只接受 `eid` 与已核验 `entId` 一致的记录。有 `province` 时拼接“，位于{province}”。
4. `entScaleName` 非空时拼接“，企业规模为{entScaleName}”。`groupName` 不进入核心观点，也不得据此生成“隶属于”“归属于”或其他强关系表述。
5. `industry` 非空时按半角连字符 `-` 切分：至少三层时只保留前三层并用 `-` 连接，不足三层时保留完整原值；拼接“，所属行业为{行业}”。
6. `regCap` 非空时拼接“，注册资本{无损格式化后的regCap}万元”；`regCapCur` 非空时按无损格式化规则追加币种。`paidInCap` 非空时拼接“，实缴资本{无损格式化后的paidInCap}万元”。字段已带单位时不得重复追加单位。
7. 片段末尾追加“。”。

#### 4.2 上市、退市或融资片段

1. 合并 `OV_MARKET.data[0].listed[]` 和 `deListed[]`。只要任一列表存在有效记录，就完全忽略 `investmentFin[]`。
2. 上市、退市记录按 `listdate` 原值升序排列。上市记录拼接“企业于{listdate}在{trademarket}上市”；退市记录拼接“企业于{listdate}从{trademarket}退市”；`securitycode` 非空时追加“，股票代码是：{securitycode}”。
3. 没有有效上市或退市记录时，才按接口顺序处理 `investmentFin[]`：
   - `fundingstatus="a"` 且 `latestroundname` 非空：写“企业目前已完成{latestroundname}融资”；`investment` 为明确正数时追加“，{latestroundname}融资金额为{investment}万元”。
   - `fundingstatus="b"` 且 `latestroundname` 非空：写“企业目前已进入{latestroundname}融资”。
   - `fundingstatus="c"`：写“企业目前已进入拟上市阶段”。
4. 多条有效记录使用逗号连接，片段末尾追加“。”；没有有效记录时省略整个片段。

#### 4.3 招投标和知识产权片段

1. `callBid.countBid` 为明确正整数时写“近2年企业共发布{countBid}个招标项目”；`overBid` 为明确正整数时追加“，其中{overBid}个完成招标”；`ingBid` 为明确正整数时追加“，{ingBid}个正在招标”。
2. `winBid.outBid` 为明确正整数时写“近2年共中标{outBid}个项目”；`outBidAmount` 非空时追加“，中标总金额为{outBidAmount}万元”；`zfOutBid` 为明确正整数时追加“，其中{zfOutBid}个政府项目”，且 `zfOutBidAmount` 非空时追加“，金额为{zfOutBidAmount}万元”。
3. `ipr.brand`、`ipr.patent`、`ipr.copyright` 中任一字段有明确值时，按商标、专利、著作权顺序写“知识产权方面有商标{brand}个，专利{patent}个，著作权{copyright}个”，缺失项跳过。
4. 招标、中标和知识产权分别成句；没有有效字段的句子省略。

#### 4.4 纳税片段

从 `OV_TAX.list[]` 中筛选 `year`、`rating` 均非空的记录，按 `year` 原值取最大年份；写“企业纳税情况，于{year}年被评为{rating}级。”。没有有效记录时省略整个片段。

#### 4.5 近两年风险片段

只读取 `OV_RISK.list[0]`，并按以下固定顺序处理：

| 字段 | 风险名称 |
| --- | --- |
| `collect15` | 重大税收违法 |
| `collect1` | 立案信息 |
| `collect2` | 裁判文书 |
| `collect3` | 法院公告 |
| `collect4` | 开庭公告 |
| `collect5` | 失信被执行人信息 |
| `collect7` | 被执行人信息 |
| `collect10` | 限高消费 |
| `collect8` | 行政处罚 |
| `collect9` | 经营异常 |
| `collect11` | 土地抵押 |
| `collect12` | 股权出质 |
| `collect13` | 动产抵押 |

- 字段为只包含数字的非负整数且大于零时，生成“{风险名称}{原值}条”。
- 字段明确为数字 `0` 时只登记到 `D.risk_zero_dimensions`，不进入核心观点。
- 空字符串、`null`、非数字、产品空结果或调用失败时跳过，不得生成零值或安全性结论。
- 至少存在一个大于零的风险描述时，以“近两年公开统计显示”开头，用“、”连接，末尾追加“；公开资料未披露案件或事项明细。”；没有大于零的描述时省略整个片段。

`EVIDENCE.company_overview` 逐项列出实际进入文本的字段。不得登记空结果、失败状态或未展示字段来为简述背书。财务片段固定不构建。

### 5. 生成大模型派生文案

先完成确定性字段整理，再让大模型一次性生成其余 `D` 文案，最后执行语义验收。不得直接把原始响应交给排版阶段临场概括。`D.company_overview`、`D.tangible_assets` 和事实表格不属于模型派生分析；执行摘要、各画像解读、需求核验说明和风险综合提示属于总结分析。除各分节统一使用“信息解读：”作为业务标签外，不添加模型来源标识。

生成要求：

1. `value_judgment`：60 至 120 个汉字。按“企业是什么、有哪些可见能力信号、为什么值得本次拜访进一步了解”的顺序，归纳登记、行业、许可、资质、知识产权和公开经营线索；不得退化为数量清单，同一句中连续列举的数量不超过 3 个，不使用市场地位、经营质量或授信判断。
2. `opportunities`：60 至 150 个汉字。写 1 至 3 条“访谈机会线索”；有目标企业自身事件时说明事件与待了解事项，没有合格事件时明确写“本次未形成可直接核验的近期机会事件”，再从业务范围、有效许可或荣誉中提出核验方向。
3. `risk_summary`：40 至 120 个汉字。只概括大于零或有明细的命中维度、原始数量、范围和信息限制，不重复列举零值维度；无命中时写“公开资料中暂无可供展示的相关记录”，同时声明不等同于不存在相关事项。
4. `visit_advice`：60 至 150 个汉字。形成一个沟通切入点和 2 至 3 个核验重点，只写“建议了解”“建议核实”“可重点询问”。
5. 每个已显示画像小节的 `*_interpretation`：通常 50 至 140 个汉字，按“事实综合 → 可能的业务含义 → 拜访核验方向”组织。法定代表人兜底场景允许缩短至 30 个汉字，但必须说明公开资料未披露履历、决策权限和具体分工。证据不足时使用“可能表明”“可以作为”“提示关注”“值得进一步了解”等审慎措辞，不得留空。
6. `operations_boundary`：说明公开资料是否披露营收、利润、现金流、客户数量等核心经营指标；没有相关信息时写“公开资料未披露相关核心经营指标，当前表格仅呈现可核验的经营线索”。
7. `risk_interpretation`：50 至 100 个汉字，概括风险事实的主体范围、时点限制和拜访核验重点。
8. `visit_questions`：优先生成 4 至 6 条，问题之间不得同义重复；`basis` 必须引用报告所列事实或明确的信息缺口，`question` 不得预设答案。

质量要求：

- 确定性企业简述、执行摘要和分节信息解读承担不同职责。大模型不得复制、改写或扩写 `D.company_overview`；同一事实可在其他文案中再次提及，但必须改变信息层级和表达目的。
- 所有总结分析必须同时包含事实依据、审慎的业务含义和可执行的拜访核验方向；事实不足时把判断降级为假设或问题。
- 文案必须具体到目标企业和报告所列事实，禁止套用“发展前景广阔”“综合实力较强”“合作空间巨大”等通用评价。
- 禁止推导市场地位、实际控制关系、风险等级、偿债能力、资金需求、授信结论或具体产品适配；不得复制思迈特样稿中的强判断、估算值或模拟数据。
- 最终报告文案必须通过业务语言检查，把内部查询状态、接口结果和数据获取过程改写为公开信息的事实陈述、信息说明或待核实事项。
- 生成后逐项核对 `EVIDENCE`。无法找到证据的句子必须删除或改为待核实问题。
- 大模型只重写除 `D.company_overview`、`D.tangible_assets` 以外的 `D` 文案，不得更改 `B`、`ID`、`OV_*`、`LAND`、`TM` 至 `OP` 原值、查询状态、列表数量、确定性简述、有形资产文案或条件布尔值。

## 报告输出格式（严格填空骨架 · 模型只填值、不造结构）

> **使用约定**：以下是水滴 MCP 唯一数据源模式的完整报告骨架。沿用参考成品的标题名称，直接省略数据源不支持的章节，并按实际可见的大章节连续编号。模型只把占位符替换为本次水滴 MCP 返回值或基于这些原值形成的忠实摘要，禁止自行新增结构。
>
> **结构纪律**：
>
> 1. 禁止新增、改名、合并、拆分或调换章节；禁止创造骨架外的小标题。
> 2. 仅允许按骨架中已经写明的 `{{#if ...}}` 条件隐藏整行、整表或整块。完成显隐判断后必须按实际可见顺序连续填写 `D.section_numbers`；只重编号大章节，不改变小节编号。
> 3. 不输出任何未被替换的占位符、条件标签、工具名、字段路径或内部状态。
> 4. 表格某行所有事实字段均为空时删除该行；某条件板块无有效事实时隐藏整块。不得用模型常识、互联网或示例值补齐。
> 5. “核心观点”和“执行摘要”在工商深度成功后固定显示；核心观点必须使用确定性 `D.company_overview`，不得由模型自由改写。每个已显示画像小节必须生成以“信息解读：”引出的总结分析。这些文案只能使用报告所列事实，不得推导实控人、融资、营收、市场地位、授信结论或产品适配。
> 6. 当前骨架不包含“产业画像与行业洞察”“与我行合作现状”；因此“需求识别与拜访核验”在当前骨架中编号为“四”，“风险预警与合规提示”显示时编号为“五”。未来加入可选大章节时仍按实际可见顺序连续编号。
> 7. “需求识别与拜访核验”只显示“（一）需求线索核验”，把已有事实和数据缺口转成现场问题；不生成银行产品推荐、紧迫度评级或营销方案。
> 8. “风险预警与合规提示”只展示工商深度、近两年统计和目标企业自身负面舆情中明确大于零或有明细的风险事实；明确零值维度只放入表后边界说明，不进入风险表，不生成风险等级；风险表后必须生成综合提示。
> 9. `D.company_overview` 验收失败时按确定性规则重新构建；其他必填总结字段生成失败时才重写对应大模型派生字段。不得交付缺少核心观点、执行摘要或已显示小节信息解读的报告。

```markdown
# 对公客户访前一页纸

报告编号：{{META.report_id}}  ｜  生成时间：{{META.generated_at}}  ｜  密级：机密

客户名称：{{B.basicList[0].orgName}}{{#if D.brand_name}}（品牌：{{D.brand_name}}）{{/if}}

## {{D.section_numbers.core}}、核心观点

{{D.company_overview}}

## {{D.section_numbers.summary}}、执行摘要

**核心价值判断：** {{D.value_judgment}}

**主要机会：** {{D.opportunities}}

**主要风险：** {{D.risk_summary}}

**拜访建议：** {{D.visit_advice}}

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

—————————————————数据来源————————————————

水滴 MCP（{{D.source_dimensions.basic}}）｜数据日期：{{META.generated_at}}

{{#if D.person_representatives}}
### （二）关键决策人信息

{{#each D.person_representatives|max=8}}
- {{name}}：{{#if position}}{{position}}{{#if is_legal_representative}}；{{/if}}{{/if}}{{#if is_legal_representative}}法定代表人{{/if}}
{{/each}}

**信息解读：** {{D.people_interpretation}}

—————————————————数据来源————————————————

水滴 MCP（{{D.source_dimensions.people}}）｜数据日期：{{META.generated_at}}
{{/if}}

{{#if D.has_equity_or_network}}
### （三）股权结构与关联关系

{{#if B.shareholderList}}
| 股东名称 | 持股比例 | 认缴出资额 |
| --- | --- | --- |
{{#each D.shareholder_rows|max=15}}| {{name}} | {{ratio_display}} | {{amount_display}} |{{/each}}
{{/if}}

{{#if D.network_summary}}关联关系：{{D.network_summary}}{{/if}}

**信息解读：** {{D.equity_interpretation}}

—————————————————数据来源————————————————

水滴 MCP（{{D.source_dimensions.equity}}）｜数据日期：{{META.generated_at}}
{{/if}}

{{#if D.has_assets}}
### （四）企业资产状况

{{#if D.tangible_assets}}**有形资产：**

{{D.tangible_assets}}{{/if}}

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

—————————————————数据来源————————————————

水滴 MCP（{{D.source_dimensions.assets}}）｜数据日期：{{META.generated_at}}
{{/if}}

{{#if D.has_core_operations}}
### （五）核心经营数据

信息说明：{{D.operations_boundary}}

| 指标 | 本次数据 | 数据口径 |
| --- | --- | --- |
{{#if D.employee_scale}}| **员工规模** | {{D.employee_scale}} | 工商登记或企业基本信息 |{{/if}}
{{#if D.branch_summary}}| **分支机构** | {{D.branch_summary}} | 工商登记公开记录 |{{/if}}
{{#if D.website_summary}}| **网站与 ICP** | {{D.website_summary}} | 工商登记或 ICP 备案公开记录 |{{/if}}
{{#if D.recent_public_activity}}| **近期公开动态** | {{D.recent_public_activity}} | 目标企业自身公开舆情线索 |{{/if}}

**信息解读：** {{D.operations_interpretation}}

—————————————————数据来源————————————————

水滴 MCP（{{D.source_dimensions.operations}}）｜数据日期：{{META.generated_at}}
{{/if}}

## {{D.section_numbers.needs}}、需求识别与拜访核验

### （一）需求线索核验

**信息解读：** 以下核验主题根据报告所列事实和信息缺口整理，用于帮助业务人员准备现场问题，不构成产品建议。

| 核验主题 | 已知依据与现场问题 |
| --- | --- |
{{#each D.visit_questions}}| **{{topic}}** | {{basis}}；建议现场核实：{{question}} |{{/each}}

{{#if D.has_risks}}
## {{D.section_numbers.risk}}、风险预警与合规提示

| 风险维度 | 关键事实 | 范围与待核实事项 |
| --- | --- | --- |
{{#each D.risks}}| **{{topic}}** | {{detail}} | {{scope}} |{{/each}}

**信息解读：** {{D.risk_interpretation}}

{{#if D.risk_zero_dimensions}}信息说明：近两年公开统计中以下事项记录数为 0：{{D.risk_zero_dimensions}}；仅代表该公开统计范围，不等同于不存在相关事项。{{/if}}

—————————————————数据来源————————————————

水滴 MCP（{{D.source_dimensions.risk}}）｜数据日期：{{META.generated_at}}
{{/if}}

## 报告使用说明

- 报告目的：本报告仅为对公客户经理拜访前准备和沟通参考使用，不作为授信审批的最终依据。
- 信息真实性：报告依据生成时点的公开信息形成；资料缺失或尚待补充不等同于不存在相关事实，建议在拜访中核实关键信息。
- 数据时效性：报告生成后如发生重大变化，建议重新生成报告。
- 保密义务：本报告涉及企业信息，接收方应按所在机构制度妥善保管，未经授权不得对外泄露。

资料范围：{{D.coverage_summary}}
```

### 标题白名单

最终报告只能出现骨架中实际存在的标题，标题名称必须逐字使用，禁止同义替换；大章节的中文数字前缀取自 `D.section_numbers`：`核心观点`、`执行摘要`、`客户全景画像`、`（一）企业基本信息`、`（二）关键决策人信息`、`（三）股权结构与关联关系`、`（四）企业资产状况`、`（五）核心经营数据`、`需求识别与拜访核验`、`（一）需求线索核验`、`风险预警与合规提示`、`报告使用说明`。

## 文档生成

默认 `--format pdf`。先完成统一证据模型、`D` 派生文案、`EVIDENCE` 映射和语义验收，再形成完整 Markdown，最后排版为 PDF。

PDF 是唯一版式验收基准。优先沿用当前环境中最近一次已验收成功的生成路径；没有既有路径时优先直接生成 PDF，直接生成不可用时才使用 DOCX 中转。同一任务中不得因分页不理想在多个渲染器之间反复切换。不同格式必须复用同一证据模型、派生文案和条件删除结果。

### 固定版式

- 页面：Letter，215.9 × 279.4 mm；上、下页边距 20 mm，左、右页边距 25 mm。
- 正文：宋体或可用的等价中文宋体，10.5 pt，单倍行距；表格正文 9 pt。
- 标题：黑体或等价中文黑体；主标题 18 pt 黑色居中，一级标题 14 pt、二级标题 12 pt，标题蓝色 `#4F81BD`。所有 `##` 一级标题段前 12 pt、段后 6 pt；标题位于页首时不额外增加段前空白。
- 元信息：报告编号、生成时间、密级使用 9 pt 居中；客户名称使用 12 pt 加粗居中。
- 数据来源：板块末尾加入灰色 `#808080` 居中分隔线及“水滴 MCP（数据维度）｜数据日期：{generated_at}”。
- 正文段落：核心观点和信息解读正文首行缩进 2 个汉字；执行摘要四项不缩进。普通正文段落段后 4 pt；PDF 使用段后样式控制间距，不插入空白段落，Markdown 回退在自然段之间保留一个空行。
- 字重：黑色正文必须使用宋体或等价中文宋体的常规字重，禁止整段使用字体名含 `Black`、`Bold`、`Semibold` 的变体。核心观点、执行摘要内容、信息解读正文、表格具体数据、股东名、人员名、代表记录、风险说明和报告使用说明均不得加粗。
- 仅主标题、客户名称、蓝色章节标题、表头行、执行摘要的“核心价值判断：”“主要机会：”“主要风险：”“拜访建议：”、各分节“信息解读：”标签，以及表格中的业务标签项允许加粗。业务标签项包括企业基本信息字段名、资产类型、经营指标、需求核验主题和风险维度；股东名、人员名及其他实体名称不属于标签项。
- 表格：黑色 0.5 pt 网格线，无表头底色；表头加粗、左对齐并跨页重复；符合上述定义的业务标签项加粗，其余正文保持常规字重、左对齐，单元格垂直居中。允许表格按可用空间自然分页，较长单元格可跨页拆分。
- 不使用 `KeepTogether`、`keepWithNext`、整块容器或手动分页符保护章节、段落、信息解读、数据来源或表格起始部分；允许这些内容随页面剩余空间自然续页。
- 不因避免断句、孤立标题或来源文字而主动移动整块内容；跨页表格只重复表头，不重复小节标题。
- 不得出现裁切、重叠、乱码或由强制分页造成的异常空白。除最后一页外，若后续仍有连续正文而当前页空白超过可用正文区约三分之一，视为分页失败。
- 页脚不添加页码、公司名或其他参考 DOCX 中不存在的内容。
- 字号不得为压缩页数降至上述规格以下；内容过长时通过自然分页解决。
- “一页纸”是产品名称，不强制压缩到一页。

表格列宽按可用正文宽度 165.9 mm 固定分配：

企业基本信息 35 / 130.9；股东 84 / 32 / 49.9；企业资产状况 34 / 28 / 103.9；核心经营数据 36 / 74 / 55.9；需求线索核验 42 / 123.9；风险预警 38 / 55 / 72.9。单位均为 mm。

### 生成与验收

1. 执行语义验收：确认 `company_overview` 至少包含规范企业全称，执行摘要四项和 `basic_interpretation` 非空；每个已显示画像小节、需求核验和风险综合提示均使用“信息解读：”标签；`has_risks=true` 时存在 `risk_interpretation`。确认所有可见大章节编号从“一”开始连续递增，不跳号、不重号。
2. 核对证据覆盖：每个非空 `D` 文案字段在 `EVIDENCE` 中至少有一个来源；逐句删除无来源判断。检查金额、比例、日期、数量和币种的底层原值完全一致，展示层只进行了允许的无损格式化或满足全部前置条件的土地同类精确合计；检查状态字段互斥，土地供应、土地出让、土地抵押未被合并为单一状态，数据来源行未列入 `empty` 或 `failed` 维度，`D.coverage_summary` 未暴露内部查询步骤。
3. 检查内容边界：不得出现无直接证据的市场地位、实控关系、融资、营收、客户数量、风险评级、授信结论或产品推荐；舆情机会线索必须通过目标企业事件主体过滤。
4. 检查内容质量：`company_overview` 的片段顺序、条件分支、标点和风险空值规则必须符合确定性规范；总结分析不得整句复制核心观点，必须包含事实综合、审慎的业务含义和拜访核验方向，不得出现空泛套话；信息缺口写成自然的信息说明或待核实问题。
5. `company_overview` 或 `tangible_assets` 验收不通过时，只用同一证据模型重新执行对应确定性规则并更新相应 `EVIDENCE`；其他语义验收失败时只重新生成受影响的大模型派生文案。不得重新调用已成功的 MCP 工具，不得让大模型修饰企业简述或有形资产文案。仍无足够证据时使用边界型表述，不得隐藏核心观点或执行摘要。
6. 按“报告输出格式（严格填空骨架 · 模型只填值、不造结构）”替换占位符并执行预定义条件。检查报告中不存在未替换占位符、条件标签、内部字段路径或空表，再开始排版。
7. 使用当前环境已有的文档或 PDF 能力生成 `output/pdf/{company_name}-公司访前一页纸.pdf`。如需 DOCX 中间文件，只把它作为本次临时产物。
8. 逐页渲染或预览最终 PDF，检查中文字体、Letter 页面、页边距、字号、章节和段落间距、首行缩进、表头样式、标签项字重、列宽、自然分页、裁切、重叠和异常空白。检查 PDF 字体元数据和文本样式：除明确允许加粗的标题、标签和表格标签项外，黑色正文若使用 `Black`、`Bold` 或 `Semibold` 字体变体即验收失败。除最后一页外，后续仍有连续正文但当前页空白超过可用正文区约三分之一时，取消强制分页或整块容器后重新渲染。
9. 验收通过后删除本次临时 JSON、DOCX、预览图片及一次性辅助文件，只保留最终 PDF。
10. 不把生成过程中临时编写的代码、命令、`EVIDENCE` 或内部证据 JSON 写入报告或聊天回复。
11. 当前环境无法创建或验收 PDF、中文字体不可用或转换失败时，不循环重试；删除不完整文件并回退完整 Markdown，说明“PDF 生成未完成：{原因}，已回退 Markdown”。

## Markdown 回退

用户指定 `--format md`，或 PDF 流程失败时，直接按“报告输出格式（严格填空骨架 · 模型只填值、不造结构）”输出。Markdown 与 PDF 必须复用同一证据模型中的原值和条件结果。

聊天回复只包含企业规范全称、数据日期、生成格式、最重要的 1 至 3 条资料范围说明，以及 PDF 绝对路径链接或完整 Markdown 正文。

## 输出纪律

1. 使用中文，用户明确要求其他语言时除外。
2. 标题名称逐字使用固定骨架；条件板块隐藏后按实际可见的大章节顺序连续重编号。不得出现跳号、重号、空标题、空表或整排“未披露”。
3. 事实与访谈建议分开。建议使用“建议核实”“可重点了解”，不写“应授信”“建议放款”“可合作”等结论。
4. 报告中统一写“水滴 MCP”，不得写 CISP、产品码、工具名或字段路径。
5. 当前水滴 MCP 唯一数据源模式固定不展示“四、产业画像与行业洞察”“五、与我行合作现状”、授信/存款/代发明细和具体银行产品推荐。
6. “一页纸”是报告产品名称，不限制总页数；内容随有效数据自动增减。
7. 最终 PDF 必须经过逐页渲染验收；无法验收时不得交付 PDF，直接回退 Markdown。
8. 工商深度成功后，最终报告必须包含确定性核心观点、执行摘要四项和企业基本信息解读；不得以数据不足为由删除。简介扩展维度不足时，核心观点至少保留规范企业全称，其余信息缺口在执行摘要或待核实问题中说明。

**SKILL 版本**：v1.9 ｜ **适配数据源**：连接标识为 `cisp-mcp` 的水滴 MCP 当前 25 工具版本 ｜ **页面规格**：Letter 215.9 × 279.4 mm ｜ **默认交付**：PDF，失败回退 Markdown
