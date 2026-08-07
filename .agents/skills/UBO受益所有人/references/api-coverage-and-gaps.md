# API 覆盖、字段映射与接口缺口

本文件基于仓库 `docs/prod_list.json`、`src/cisp_mcp/interfaces.py`、`src/cisp_mcp/server.py` 及当前 MCP 工具清单整理。它约束取数和缺失处理，不代表未下载接口文档中尚未核验的字段一定存在。

## 目录

1. 当前可用专用工具
2. 报告章节覆盖
3. 关键字段映射
4. UBO 证据优先级
5. 当前能力边界
6. 数据源准入复核记录
7. 明确不建议优先接入的接口

## 1. 当前可用专用工具

| 产品码 | MCP 工具 | 本报告用途 | 必要性 |
| --- | --- | --- | --- |
| P0010058 | `p0010058_query_business_basic_deep` | 主体、股东、主要人员、投资、分支、变更和基本信息底座 | 必选 |
| P0010010 | `p0010010_query_business_profile` | 主体交叉核验、读取真实 `entId` | 推荐 |
| P0010068 | `p0010068_fuzzy_search_company_name` | 简称或同名企业消歧 | 条件必选 |
| P0010059 | `p0010059_query_business_basic_brief` | 按主题补齐工商列表与变更总量 | 必选 |
| P0020129 | `p0020129_query_controller_and_ubo` | 实际控制人与最终受益人的名称型直接结论 | 必选 |
| P0090011 | `p0090011_query_ubo_full_paths` | 最终受益人、低于阈值节点和完整受益路径 | 必选，失败可降级 |
| P0090001 / P0090012 | `p0090001_p0090012_query_ubo` | 详版完整受益人及递归路径，或非详版快速识别与 `bnfCat` 判定依据 | 按任务二选一 |
| P0020024 | `p0020024_query_beneficial_shareholders_detailed` | 受益股东、最终受益人和实际控制人标签节点的独立互证 | 推荐 |
| P0090008 | `p0090008_query_actual_controller` | 实际控制人、聚合股权占比和控制路径的直接明细 | 必选，失败可降级 |
| P0020019 | `p0020019_query_suspected_controller` | 疑似实际控制人、控制比例和控制路径 | 推荐 |
| P0020023 | `p0020023_query_equity_penetration` | 向上股东树、向下投资树和路径互证 | 推荐 |

只使用以上专用工具。当前服务虽然存在通用 `query_cisp_product`，本 Skill 明确禁止使用它调用产品目录中的其他产品。

## 2. 报告章节覆盖

| 报告位置 | 当前数据来源 | 覆盖情况 |
| --- | --- | --- |
| 报告头部 | P0010058、P0090001/P0090012、P0020129、P0090011、P0090008 | 主体与名称结论可覆盖；表决权、形成日期不稳定 |
| 执行摘要 | 工商底座 + UBO/实控产品 | 可覆盖，必须按证据删减推演 |
| §1 报告用途 | 固定模板 | 不获取企业数据 |
| §2.1 识别方法 | 固定模板 + P0090011 聚合值 | 可覆盖 |
| §2.2 受益所有人 | P0090001/P0090012、P0090011、P0020024、P0020129 | 姓名、类型、职务、判定依据、聚合比例和路径可覆盖；表决权/形成日期可能缺失 |
| §2.3 实际控制人 | P0090008、P0020129、P0020024、P0020019 | 可覆盖直接实控人、聚合股权占比和控制路径；不能稳定拆分直接持股、总持股和表决权 |
| §2.4 日常经营管理人员 | P0090011/P0020129 明确名单 + P0010058 人员职务 | 只有 UBO 产品明确返回名单时可覆盖，不得用工商人员自行扩充 |
| §3.1 工商注册 | P0010058、P0010059 | 大部分覆盖；纳税人识别号、组织机构代码、参保范围等以实际字段为准 |
| §3.2 股东 | P0010058、P0010059 | 名称、类型、直接比例、认缴额可覆盖；“持股数（股）”通常不足 |
| §3.3 主要人员 | P0010058、P0010059 | 姓名、职务可覆盖；个人持股比例通常不足 |
| §3.4 对外投资 | P0010058、P0010059 | 企业、状态、比例、金额可覆盖；日期、省份、行业可能缺失 |
| §3.5 分支机构 | P0010058、P0010059 | 名称、代码、登记机关可覆盖；负责人、日期、状态可能缺失 |
| §3.6 变更 | P0010058、P0010059 | 日期、事项、前后值可覆盖；精确累计总量以实际元数据为准 |

## 3. 关键字段映射

字段名按当前已接入产品和仓库实测记录整理。上游可能返回字符串、数字或空值，解析时兼容类型并保留原值。

### 3.1 工商深度 P0010058

| 展示项 | 当前数据路径或字段 |
| --- | --- |
| 企业名称 | `data.basicList[0].orgName` |
| 英文名 | `data.basicList[0].ogrNameEng`（底层原始拼写） |
| 曾用名 | `data.basicList[0].orgNameUsed`，必要时与 P0010010 历史名称互证 |
| 状态 | `orgStatus` |
| 信用代码、注册号 | `creditCode`、`regNo` |
| 法定代表人 | `legRepName` |
| 注册资本、币种、实缴资本 | `regCap`、`regCapCur`、`paidInCap` |
| 行业 | `industry`、`industryClas`、`industryCode` |
| 企业类型 | `orgType` |
| 成立、核准、营业期限 | `estDate`、`apprDate`、`openFrom`、`openTo` |
| 登记机关、地址、范围 | `regOrg`、`regAddr`、`operateScope` |
| 股东 | `data.shareholderList[]` |
| 股东名称、类型 | `shareholderName`、`shareholderType` 或 `invType` |
| 直接持股比例 | `fundedRatio` |
| 认缴额、币种、日期 | `subConAmt`、`subConCur`、`conDate` |
| 主要人员 | `data.personList[]` 的 `perName`、`position`、`isFr` |
| 对外投资 | `data.entInvItemList[]` |
| 被投企业、状态、比例 | `orgName`、`orgStatus`、`fundedRatio` |
| 投资金额、币种 | `subConAmt`、`subConCur` |
| 分支机构 | `data.filiationList[]` |
| 分支名称、代码、登记机关 | `brName`、`brnCreditCode`、`brRegNo`、`brnRegOrg` |
| 变更 | `data.alterList[]` |
| 变更日期、事项、前后值 | `busAltDate`、`busAltItem`、`busAltBef`、`busAltAft` |

### 3.2 工商简项 P0010059

基础批次使用：

```text
types=["basic","shareholder","person","alter","filiation","foreignInvestment","yearReportPaidUpCapital"]
```

需要补充累计变更或变更专题时单独使用：

```text
types=["changeRecords"]
```

可用列表包括 `basicList`、`shareholderList`、`personList`、`alterList`、`filiationList`、`foreignInvestmentList`、`yearReportPaidUpCapitalList`、`changeRecordsList`。同一业务主题的字段优先沿用 P0010058 映射；不同产品字段不一致时保留原值并在内部做别名映射，不把空字段覆盖非空字段。

### 3.3 实控与 UBO 产品

| 产品 | 关键路径 | 使用方式 |
| --- | --- | --- |
| P0020129 | `data.dataList[].controllerList[].controller` | 实际控制人名称型直接结论 |
| P0020129 | `data.dataList[].finalBefList[].beneficiary` | 最终受益人名称型直接结论 |
| P0090011 | `data.MatchInfoList[]` | 目标主体的 UBO 结果集合 |
| P0090011 | `finalList[].finalBefList[]` | `beneficiary`、`orgName`、`type`、`percent`、`title` 等产品直接字段 |
| P0090011 | `finalList[].equlityProcessList[]` | 完整受益路径；`equlity` 为底层原始拼写 |
| P0090011 | `lessProcessList[]` | 低于产品阈值的穿透节点 |
| P0090001 | `data.finalList[].finalBefList[]` | 详版受益所有人；包含 `beneficiary`、`type`、`percent`、`title`，可返回关键管理人员兜底 |
| P0090001 | `data.finalList[].equlityProcessList[]` | 详版递归股权路径；`stockHolderList[]` 可继续嵌套，`equlity` 为底层原始拼写 |
| P0090012 | `data.finalList[].finalBefList[]` | 非详版受益所有人；除名称、类型、比例和职务外可返回判定依据 `bnfCat` |
| P0090012 | `data.finalList[].equlityProcessList[]` | 非详版可选路径；请求 `onlyFinalBef=1` 时不返回路径 |
| P0020024 | `data.basicList[]` | 目标企业照面，用于响应主体一致性核验 |
| P0020024 | `data.nodeList[]` | 聚合穿透节点；`percentTotal` 为间接占比，`pathLevel` 为出现层级，`pathCount` 为路径数，`type` 为 P=自然人/E=非自然人 |
| P0020024 | `data.nodeList[].benifitTag` | 底层原始拼写；可包含“受益股东”“最终受益人”“实际控制人”，只作产品标签证据 |
| P0090008 | `data.actualController[].controllerList[]` | `controller` 为实际控制人，`percent` 为产品聚合股权占比 |
| P0090008 | `data.actualController[].controllerList[].controlPathList[]` | 控制路径段；包含 `stockHolderName`、`investedCompanyName`、`shouldCapital` 和该段 `percent` |
| P0020019 | `data.controlNodeList[]` | 疑似控制节点及间接控制比例 `percent` |
| P0020019 | `data.linkList[]` | `startId`、`endId`、`direction`、`directPercent` 控制路径边 |
| P0020019 | `data.rootNodeList[]`、`nodeList[]` | 路径节点名称与类型 |
| P0020023 | `data.upList[]` | 向上股东树，节点比例为 `fundedRatio` |
| P0020023 | `data.downList[]` | 向下投资树，节点比例为 `fundedRatio` |

`P0020019` 是“疑似实际控制人”产品，其候选不能替代 P0090008 或 P0020129 的直接控制人结论。P0090001、P0090012、P0090011 和 P0090008 的比例均为产品结果，禁止用路径比例重算或覆盖。P0020024 的 `nodeList[]` 是聚合标签节点，不是完整有向路径。

## 4. UBO 证据优先级

按结论类型使用：

1. 最终受益人：按任务选择 P0090001 详版或 P0090012 非详版 → P0090011 聚合结论与完整路径 → P0020024 标签节点 → P0020129 名称型直接结论 → 工商直接股东事实。
2. 实际控制人：P0090008 直接明细、聚合比例和控制路径 → P0020129 名称型直接结论 → P0020024 实际控制人标签节点 → P0020019 疑似控制人和路径 → P0020023 股权穿透树。
3. 工商底座：P0010058/P0010059 当前直接股东和主要人员事实，只用于主体、直接持股和职务互证。

高优先级产品失败时可以降级，但必须改变措辞：路径和工商事实只能支持“候选”“直接持股事实”或“本次未完成识别”，不能伪装成直接 UBO 结论。

## 5. 当前能力边界

现有专用 MCP 工具不能稳定保证以下企查查模板字段：

- UBO 的表决权比例、收益权比例和受益所有权形成日期。
- 实际控制人的直接持股、总持股、表决权三列独立聚合值。
- 产品官方定义的完整日常经营管理人员兜底名单及兜底原因摘要。
- 股份公司的精确持股数（股）；当前工商字段更多是认缴金额。
- 分支机构负责人、成立日期、状态等完整照面字段。
- 对外投资的认缴出资日期、所属省份和所属行业完整字段。
- 未披露的一致行动协议、表决权委托、代持、协议控制和境外终点。

这些字段缺失时写“未披露”或相应状态，不得从其他字段推导。

## 6. 数据源准入复核记录

2026-08-07 首次依据 `/Users/ice/Desktop/项目管理/API agent/API数据资产设计表 (1).xlsx` 核验时，P0090001 和 P0090012 的旧组件记录仍含第三方编码。随后用户人工检查最新数据源文档，确认两产品后期均已替换为 `N300` 内部数据源；本次接入以该最新人工复核结果覆盖旧资产表记录。

| 产品码 | 产品名称 | 最新准入口径 | 接入结论 |
| --- | --- | --- | --- |
| P0090001 | 企业最终受益人信息查询-详版 | 用户人工复核最新文档：已替换为 `N300` | 已通过统一工具接入 |
| P0090012 | 企业最终受益人信息查询 | 用户人工复核最新文档：已替换为 `N300` | 已通过统一工具接入 |
| P0090008 | 企业实际控制人信息查询 | 旧资产表 `API企业编码上线!C601:K601`：仅 `N000` | 已接入 |
| P0020024 | 企业受益股东详细查询 | 旧资产表 `API企业编码上线!C339:K340`：仅 `N300` | 已接入 |

P0090001 与 P0090012 只暴露一个专用 MCP 工具。调用方必须按任务明确选择 `detailed` 或 `standard`，不得通过通用产品网关绕过该选择规则。

## 7. 明确不建议优先接入的接口

| 产品码 | 产品名称 | 暂不优先原因 |
| --- | --- | --- |
| P0090002 | 企业最终受益人信息查询-简版 | 预计与详版/全路径版高度重叠，不能优先解决精细字段缺口 |
| P0020020 | 企业受益股东信息查询 | P0020024 详版已接入，简版不能优先增加独立证据价值 |
| P0990068 | 企业受益人信息查询（乐山商业银行定制） | 客户定制产品，不应作为通用 UBO Skill 的默认依赖 |
| P0990067 | 企业实际控制权接口（中证定制） | 客户定制产品，通用性和授权边界需另行评估 |
| P0090010 | 企业控股股东图谱（图片）信息查询 | 图片图谱不是 Markdown 事实表的核心缺口，且现有结构化穿透工具已可提供路径 |
