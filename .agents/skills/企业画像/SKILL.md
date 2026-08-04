---
name: enterprise-profile
description: 使用客户 Agent 中连接标识为 cisp-mcp 的水滴征信 MCP 锚定中国企业主体并获取工商、财务、土地、行业、关联关系、知识产权、许可资质、舆情与风险等内部结构化数据，同时使用 AI 网络搜索工具从正规网站补充近 12 个月企业动态、关键转折、企业官网自述、正规外部机构描述、关键决策人公开职业背景、生产基地与厂房设备等有形资产线索、近期公开事件和权威行业背景，以内部事实白名单约束 AI 生成自然的主体描述，并形成“内部主体底座＋外部近期观察＋经营阶段边界＋风险约束＋拜访重点”的核心观点；默认交付 Letter 尺寸 PDF，失败时回退完整 Markdown。适用于对公客户经理访前准备、企业拜访简报、客户全景画像、核心经营数据、产业画像与行业洞察、拜访问题清单、合作前背景了解，以及“企业画像”“生成企业画像”“拜访前帮我了解这家公司”“生成企业画像 PDF”等请求。
---

> 内部数据与正规网站公开资料融合的企业画像。
>
> 面向对公客户经理的访前准备工具。输入企业名称或统一社会信用代码，先通过水滴征信 MCP 锚定主体并获取结构化专业数据，再通过 AI 网络搜索工具从正规网站补充企业动态、关键转折、企业官网自述、正规外部机构描述、关键决策人公开职业背景、生产基地与厂房设备等有形资产线索、近期公开事件和权威行业背景，生成与标准成品一致的紧凑 Letter 版式报告。
>
> 核心能力：
> - 以内部主体事实为底座，融合关键转折、近期公开动作、经营阶段边界、风险约束和拜访重点，生成可追溯的综合核心观点
> - 由规则筛选内部事实白名单，再由 AI 组织自然的企业主体描述，失败时回退确定性文本
> - 审慎归因企业官网自述和正规外部机构对企业业务定位的描述
> - 主体工商核验与经营范围事实摘要
> - 以内部人员名单和职务为锚点，使用正规外部页面补充关键决策人公开职业背景，并以“姓名｜职务｜背景”三列表格展示
> - 只保留能够直接证明土地、厂房、生产基地、仓储设施、设备产线或在建工程的有形资产事实，使用内部土地记录与正规外部原始页面形成精简资产表
> - 上市公司年度核心经营数据；缺少可靠财务资料时提供业务化的信息说明
> - 基于省级三级行业范围形成行业数量、财务排名、知识产权排名和风险信号洞察
> - 专利、商标、软件著作权、作品著作权、ICP、许可和荣誉资质盘点
> - 近 90 天公开舆情中的机会线索与风险线索
> - 每次主体确认后定向检索近 12 个月企业动态和权威行业背景
> - 对所有可见事实逐条区分“内部：”与“外部：”来源并保持可追溯
> - 把 MCP 未覆盖的经营、财务和合作信息转成拜访核验问题
> - 按企业画像产品的固定字段和顺序生成确定性企业简述，并生成审慎的信息解读
> - 默认生成 PDF；文档环境不可用时完整回退 Markdown
>
> 使用方式：`/enterprise-profile 企业名称或信用代码 [--format pdf|md]`

- **命令**：`/enterprise-profile`
- **内部数据源**：水滴征信 MCP
- **外部数据源**：AI 网络搜索工具打开并核验的正规网站原始页面
- **MCP Server 连接标识**：`cisp-mcp`
- **默认格式**：`pdf`
- **报告定位**：访前准备，不构成授信、法律、财务、投资或准入结论

---

## MCP 服务依赖

1. 仅使用客户 Agent 中配置名称或连接标识为 `cisp-mcp` 的 MCP Server。连接方式、认证方式和连接参数由客户 Agent 的 MCP 配置提供，不属于本 Skill 的职责。
2. 执行前检查 `cisp-mcp` 是否已连接，并检查下方绑定的工具名及输入参数 schema。不得只凭“水滴征信 MCP”“CISP MCP”等展示名称，或工具语义相似，改用其他 MCP Server。
3. 客户 Agent 可能把连接标识规范化为工具命名空间，例如将 `cisp-mcp` 显示为 `cisp_mcp`。只有当工具元数据明确归属于原始连接标识 `cisp-mcp` 时，才可把该命名空间下的同名工具视为本 Skill 的目标工具。
4. `p0010058_query_business_basic_deep` 是必需工具。`cisp-mcp` 未连接、该工具不存在或其参数 schema 与本 Skill 不兼容时，立即停止，不生成报告，并提示用户检查或连接 `cisp-mcp`；禁止改用网络搜索、其他 MCP 或同义工具替代内部主体核验。
5. 其余绑定工具为内部扩展维度工具。单个扩展工具不存在、不可用或调用失败时，将对应维度记为 `failed`，继续处理其他维度；不得用其他 MCP 或外部网页填充该内部结构化维度。
6. 始终通过 Agent 已注册的 `cisp-mcp` 工具调用服务。

## AI 网络搜索依赖与来源准入

1. 只有内部工商深度成功并确认规范企业全称后，才使用 Agent 可用的 AI 网络搜索与网页浏览工具。该工具必须同时支持搜索结果和打开原始网页；不得把搜索结果页摘要、AI 摘要或未打开的片段作为证据。
2. 每次生成报告都执行定向网络搜索，默认窗口为报告生成日前 12 个月。使用内部确认的规范企业全称、可信曾用名和内部工商行业名称构造查询，至少覆盖：企业官网简介及业务/产品/项目动态、政府或监管公告、交易所公告、正规机构或媒体对企业的介绍、内部已确认关键决策人的公开职业背景、生产基地/厂房/仓储/设备产线/在建工程等有形资产线索、近期公开事件、政府/统计机构/行业协会/高校/权威研究机构发布的行业背景。无发布日期的企业官网稳定介绍页、管理团队页、人物介绍页或设施介绍页不受 12 个月限制，但必须记录访问日期。
3. 外部来源按以下等级准入：
   - 一级：政府、监管机构、法院、交易所、统计机构及目标企业官方网站；
   - 二级：具有明确主办单位的正规行业协会、高校和权威研究机构；
   - 三级：具有编辑审核机制的主流媒体。三级来源必须能追溯到原始采访或一级来源；不能追溯时，必须由第二个相互独立的正规来源交叉印证。
4. 排除百科、问答、论坛、个人博客、自媒体、社交平台、内容农场、商业企业信息聚合页、无原始出处转载、搜索结果页、模型生成内容，以及无法打开正文、无法确认发布主体或 URL 的页面。付费墙或登录墙导致正文不可核验时不得采用。
5. 企业官网自述必须写成“企业官网披露”，不得改写为第三方核验结论。外部来源冲突时优先一级来源和直接原始页面；仍无法消解时并列说明冲突和日期，不由模型判断真伪，不把冲突值合并。
6. 网络工具不可用、搜索失败或没有合格来源时，将 `WEB.status` 记为 `unavailable` 或 `empty`，继续使用内部证据生成报告，并在资料范围中写“外部公开资料未形成可用补充”或“外部公开资料检索尚待补充”；不得因此降低内部必选工具要求。
7. 每个采用的外部事实必须绑定唯一 `source_id`，打开原始页面核验企业主体、正文、发布机构、标题、URL、发布日期和访问日期。只有主体与规范企业全称一致，或正文明确说明别名、品牌与该主体的关系时，才可作为目标企业事实。人物背景还必须同时核验姓名与目标企业关系；姓名相同但正文未明确关联目标企业，或存在无法消解的同名歧义时不得采用。

## 数据纪律

1. 内部结构化事实只使用本次水滴征信 MCP 返回的数据；外部补充事实只使用通过“AI 网络搜索依赖与来源准入”核验并登记到 `WEB` 的原始网页。禁止使用模型记忆、第三方商业数据库、样例企业内容或未登记网页补齐。
2. 先锚定唯一企业主体，再查询扩展维度。工商深度失败、无结果或主体不一致时停止生成。
3. `B`、`ID`、`OV_*`、`LAND`、`IND`、`REL`、`FIN_*`、`TM` 至 `OP` 中的金额、比例、日期、数量和币种必须逐字保存。报告展示层允许做无损格式化，但禁止四舍五入、补零、截断有效小数、换算、加总、相减、相乘或倒算；“产业画像生成规则”允许把文档明确为比率的 `IND` 十进制原值精确乘以 100 后显示为百分比；“核心经营数据生成规则”允许为文档明确为比率的上市公司财务指标原值直接追加 `%`，不得改变数值。有形资产不再计算土地面积、价格或抵押金额合计。
4. 不根据股东、任职或投资关系推导实际控制人、最终受益人、一致行动关系、融资轮次或资本市场状态。
5. 分页接口以 `*ListMeta.totalCount` 表示总量；第一页记录只称“本次首批返回记录”，不得称为“最新”或“全部”。
6. 空数组只表示“本次查询未返回相关公开记录”；调用失败表示“该维度查询未完成”。两者不得互换。
7. 内部舆情和外部网页中的相关内容只称“公开事件线索”；只有一级来源原始公告可按原文陈述其公开事项，仍不得替代内部司法、监管或经营标准字段。
8. 报告正文不得出现工具代码、产品码、JSON 路径、schema、调用失败堆栈、额度或积分信息。
9. 不输出身份证号、手机号、出生日期、年龄、家庭关系、住址、个人联系方式、个人社交账号、API Key、原始响应或其他非必要个人敏感信息；关键决策人背景只保留与企业拜访相关的公开职业履历、教育背景、专业方向和职责信息。
10. 企业名称、信用代码、登记状态、成立时间、法定代表人、注册资本、地址、行业归属等标准基本信息仅使用内部数据。营收、利润、资产负债、现金流、员工规模及其他财务经营数值也仅使用内部数据；即使外部网站或年报披露相关值，也不得补填、覆盖或校正内部字段。
11. 股权、司法执行、土地权利、税务、许可资质、知识产权等现有结构化数量、状态和权属字段继续只使用内部数据。关键决策人的姓名、当前职务、法定代表人身份和展示范围继续只使用内部字段；外部资料只允许补充内部已确认人员的公开职业背景，不得新增人员、覆盖当前职务或推断创始人、实际控制人、最终受益人、决策权限。有形资产允许使用本 Skill 准入的一级外部原始页面补充设施、设备产线或建设项目线索，但不得补填或校正内部土地记录、抵押数量、产权状态、账面价值、评估价值、面积、产能或设备数量。外部监管、法院或媒体页面只能作为“近期公开事件”线索进入核心观点、摘要、风险核验和拜访问句，不得替代内部数量、状态、权属或标准字段。
12. 不生成市场份额、客户数量、客户渗透率、标杆客户、融资金额、授信、存款、代发、贷款建议或银行产品推荐，除非内部数据直接提供对应事实；上市公司营收、利润、资产负债、现金流和收益率仅按“核心经营数据生成规则”展示内部直接数值和明确报告期，行业财务信息仅按产业画像规则展示内部直接数值、精确排名及实际范围，不扩写经营质量或授信判断。
13. 大模型可以归纳、压缩和组织本次内部证据及合格 `WEB` 证据，但不得把数据缺口改写成事实，不得把标题或企业官网自述升级为已经独立核验的业务动作。
14. 未被内部证据或合格外部证据直接支持时，禁止使用“行业领先”“头部企业”“绝对控股”“经营健康”“优质客户”“资本实力强”“建议授信”等判断性表述。
15. 每个大模型派生文案必须在内部证据映射 `EVIDENCE` 中列出至少一个 `internal:<字段或状态>` 或 `external:<source_id>`；`EVIDENCE` 仅用于生成与验收，不写入报告。外部事实的可见正文必须附 `[外部：Wn]` 标记。
16. 先按固定规则构建 `D.company_overview_facts` 内部事实白名单和 `D.company_overview_fallback` 确定性回退文本，再由大模型仅在白名单内生成 `D.core_internal_baseline`；AI 只能改变取舍、语序和连接方式，不得修改原值、吸收外部信息或增加推断。最终展示的 `D.core_viewpoint` 可以在该内部主体描述上使用合格外部事实，但不得以外部资料补填、覆盖或校正企业基本信息、人员姓名与当前职务、股权、财务经营数值、风险数量和标准状态。外部人物背景仅按本 Skill 的关键决策人规则进入背景列。空字段、非数字风险字段、空结果和失败维度不得改写成“无”。
17. 企业官网自述和正规外部机构描述只能作为带明确归因的外部观察。官网内容写“企业官网将其业务定位描述为”或“企业官网披露”，外部内容写明发布机构及其描述场景；不得把“领先、龙头、第一、唯一、实力雄厚、全球化”等宣传或评价标签改写为独立事实，不得据此生成市场地位、经营质量、客户规模、财务表现或授信判断。
18. 内部执行可以使用产品、接口、搜索和查询术语；最终报告事实正文必须改写为业务语言，不得出现“返回”“未取得”“取得”“查询成功”“查询失败”“首批返回”“本次查询”“接口”“字段”“空结果”“统计口径”等调用表述。来源区可使用“内部”“外部”“访问日期”等来源治理术语。商业事件中的“取得订单”改写为“获得订单”。

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
| 上市公司核心经营数据 | `p0210004_query_listed_company_financial_data` | `ent_info=规范企业全称`；先以 `financial_type="mainfinadata"`、`start_date={数据日期年份-3}-01-01`、`end_date=数据日期` 查询；存在年度报告但资产或负债缺失时，以相同 `start_date/end_date` 补查 `financial_type="rgbalance"` |
| 年度员工信息补充 | `p0130025_query_company_key_indicators` | 仅在上市公司财务存在有效年度报告时调用；`ent_info=规范企业全称`，`indicator_type="2"`；只使用与选定年度相同且公示标志有效的员工信息，不使用其金额填充核心经营数据 |
| 土地资产 | `p0130036_query_land_info` | `ent_info=规范企业全称`；分别以 `land_type="tdgy"`、`"tdcr"`、`"tddy"` 调用，`page_no="1"`、`page_size="10"`，再按各类别页数完成分页；默认不查询 `dkgs` |
| 产业画像与行业洞察 | `p0130038_query_industry_analysis` | `ent_info=规范企业全称`；分别以 `analysis_type="financialRegionRank"`、`"locfin"`、`"property"`、`"indLocOpr"` 调用；代码有效时固定 `nic_lvl="n3"`、`region_lvl="r1"` 并传 `nic_id`、`region_id` |
| 关联关系核验 | `p0990022_query_supplier_relationships` | `ent_info=规范企业全称`；仅与工商股东和人员事实交叉核验，不作为供应商、客户或上下游名单 |
| 商标 | `p0010073_query_trademark_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 专利 | `p0010078_query_patent_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 软件著作权 | `p0010074_query_software_copyright_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 作品著作权 | `p0010075_query_work_copyright_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| ICP 备案 | `p0010076_query_icp_filing_info` | `ent_info=规范企业全称`，`page_no="1"`，`page_size="5"` |
| 工商许可 | `p0010084_query_license_info` | `ent_info=规范企业全称`，`license_type="gs"`，`page_no="1"`，`page_size="5"` |
| 荣誉资质 | `p0110003_query_honor_qualification_info` | `ent_info=规范企业全称`；使用本次返回列表，不宣称全量 |
| 近期舆情 | `p0050007_p0050008_query_public_opinion_info` | `ent_name=规范企业全称`；最近 90 个自然日，`page_size="10"`，`max_details=5` |

**参数名注意**：主体消歧使用 `ent_name`。工商深度按输入类型使用 `ent_name`、`credit_code`、`reg_no` 或 `org_code`。企业 ID 解析使用 `ent_info`。简述工商补充严格使用 `credit_code` 或 `ent_name` 之一。简述基本信息、纳税和近两年风险使用 `eid`。简述资本与经营线索使用 `ent_info`，但值优先为已核验的 `entId`。上市公司财务、年度员工补充、土地资产、行业分析、关联关系、商标、专利、软件著作权、作品著作权、ICP、许可和荣誉资质使用 `ent_info=规范企业全称`。舆情使用 `ent_name`。参数名不得跨工具混用。

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
| `IND` | `p0130038_query_industry_analysis.data` 按 `financialRegionRank`、`locfin`、`property`、`indLocOpr` 分类保存原值、查询范围和独立状态 |
| `REL` | `p0990022_query_supplier_relationships.data` 删除 `legalPersonCard` 后的必要关系字段和独立状态 |
| `FIN_LISTED` | `p0210004_query_listed_company_financial_data.data` 按 `mainfinadata`、条件补查的 `rgbalance` 分类保存原值和独立状态 |
| `FIN_KEY` | `p0130025_query_company_key_indicators.data`；仅保存上市公司年度员工信息补充所需原值和状态 |
| `TM` | `p0010073_query_trademark_info.data` |
| `IP` | `p0010078_query_patent_info.data` |
| `SW` | `p0010074_query_software_copyright_info.data` |
| `WC` | `p0010075_query_work_copyright_info.data` |
| `ICP` | `p0010076_query_icp_filing_info.data` |
| `LIC` | `p0010084_query_license_info.data` |
| `HON` | `p0110003_query_honor_qualification_info.data` |
| `OP` | `p0050007_p0050008_query_public_opinion_info` |
| `WEB` | AI 网络搜索查询记录及通过准入核验的外部原始网页证据；只保存允许进入报告的事实和来源元数据 |
| `D` | 从内部原值和合格 `WEB` 证据忠实压缩形成的派生文案，不新增事实 |
| `META` | 查询时间、报告编号、格式等报告元数据 |

占位符语法：

- 直接字段：`{{B.basicList[0].orgName}}`
- 列表循环：`{{#each B.shareholderList|max=15}}...{{/each}}`
- 条件板块：`{{#if B.personList}}...{{/if}}`
- 列表计数：`{{count(B.dishonestList)}}`
- 内部来源维度连接：`{{join D.source_attributions.basic.internal_dimensions|separator="、"}}`
- 按来源 ID 解析网页：`{{#eachSource WEB.sources|ids=D.source_attributions.summary.external_source_ids}}...{{/eachSource}}`；严格按 ID 数组顺序输出对应 `WEB.sources` 记录，不得输出未被引用的网页
- 内部主体事实白名单：`D.company_overview_facts`
- 内部确定性回退文本：`{{D.company_overview_fallback}}`
- AI 内部主体描述：`{{D.core_internal_baseline}}`
- 最终综合核心观点：`{{D.core_viewpoint}}`
- 动态大章节编号：`{{D.section_numbers.core}}`、`{{D.section_numbers.summary}}`、`{{D.section_numbers.profile}}`、`{{D.section_numbers.industry}}`、`{{D.section_numbers.needs}}`、`{{D.section_numbers.risk}}`
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
| 土地供应 | `LAND.tdgy.records[].district`, `projectName`, `landPosition`, `purposes`, `supplyArea`, `transactionPrice`, `contractDate`, `yearLimit` |
| 土地出让 | `LAND.tdcr.records[].district`, `projectName`, `landPosition`, `landUse`, `landArea`, `transactionPrice`, `pubDate`, `yearLimit`, `landNo` |
| 土地抵押 | `LAND.tddy.records[].administrativeArea`, `address`, `landNo`, `acreage`, `mortgageAcreage`, `mortgagePrice`, `mortgagorName`, `mortgageName`, `boardStartDate`, `boardEndDate`, `pubDate` |
| 行业查询范围 | `B.basicList[0].industry`, `industryCode`, `regOrgProvince`, `regOrgCode`；`IND.*.data[].lvl`, `regionId`, `nicId` |
| 财务行业排名与企业数 | `IND.financialRegionRank.data[0].rankAndFourRank[].ancheYear`, `orderAssgroRank`, `orderVendincRank`, `orderNetincRank`, `orderRoeRank`, `orderLoarRank`；`numEnts[].ancheyear`, `nument` |
| 行业财务参考 | `IND.locfin.data[].avgLoar`, `avgVendinc`, `medRoe`, `medVendinc`, `medLoar`, `numEnt`, `lvl`, `regionId`, `nicId` |
| 知识产权行业对标 | `IND.property.data[].orderPatentFmRank`, `orderPatentSyRank`, `orderPatentWgRank`, `orderPatentCntRank`, `orderSoftwareNumRank`, `orderProductionNumRank`, `orderTmCntRank`, `orderTmCntValidRank`, `orderCntCopyrightRank` 及对应 `avg*` 字段 |
| 行业风险信号 | `IND.indLocOpr.data[].ancheYear`, `pNEntCanM3/M6/Y1`, `pNEntN2CRatioM3/M6/Y1`, `pNEntNewM3/M6/Y1`, `pNEntNewYoy`, `pNEntCanYoy`, `pNBzxM6/Y1`, `pNSxbzxM6/Y1`, `region`, `indsy`, `lvl` |
| 关联关系交叉核验 | `REL.suppList[].managementName`, `legalPerson`, `zzjgdm`, `kgEnt[].kgName`, `kgRatio`, `kgZzjgdm`；禁止保存或使用 `legalPersonCard` |
| 上市公司主要会计指标 | `FIN_LISTED.mainfinadata.data.mainfinadataInfo[].reportDate`, `reportTimeType`, `startDate`, `latestNoticeDate`, `currency`, `operateIncome`, `totalOperateReVe`, `parentNetProfit`, `cutParentNetProfit`, `netOperateCashFlow`, `sumAsset`, `sumLiab`, `roeWeighted`, `iRobrIncreaseRate`, `toiYoyRatio`, `dpNpYoyRatio` |
| 上市公司资产负债补充 | `FIN_LISTED.rgbalance.data.rgbalanceInfo[].reportDate`, `reportTimeType`, `combineType`, `combineTypeCode`, `currency`, `sumAsset`, `sumLiab` |
| 上市公司年度员工补充 | `FIN_KEY.coreLndicatorInfo[].reportYear`, `empNum`, `empNumDis`；金额字段只保留原值，不进入核心经营数据 |
| 联系和年报 | `email`, `tel`, `ancheYear`, `B.basicInformationList` |
| 股东 | `B.shareholderList[].shareholderName`, `shareholderType`, `fundedRatio`, `subConAmt`, `subConCur`, `conDate` |
| 主要人员 | `B.personList[].perName`, `position`, `isFr`, `personAmount` |
| 分支、投资、网站 | `B.filiationList`, `B.entInvItemList`, `B.websiteOrOnlineList` |
| 主体与行政合规 | `B.basicList[0].orgStatus`, `B.exceptionList`, `illegalList`, `caseInfoList`, `liquidations`；`LIC.detailList[].licName`, `licAuth`, `licStateName`, `valFrom`, `valTo`；`HON.itemNameList[].status`, `revokeDate` |
| 司法与执行 | `OV_RISK.list[0].collect15/collect1/collect2/collect3/collect4/collect5/collect7/collect10/collect8/collect9`；`B.dishonestList`, `executedList` 及司法明细中的主体、案号、法院、日期、状态和金额 |
| 股权及资产权利负担 | `B.sharFrozList`, `sharePledgList`, `mortReg` 及 mortgage、judicial aid 列表；`LAND.tddy.records[]` |
| 税务与许可合规 | `OV_TAX.list[].year`, `rating`；`LIC.detailListMeta.totalCount`, `LIC.detailList[]`；`HON.itemNameList[].status`, `revokeDate` |
| 财务经营关注 | 仅使用按核心经营数据规则选定的 `FIN_LISTED.mainfinadata` 年度记录中的直接负值或明确负增长字段；非上市公司或无有效年度报告只登记为信息边界 |
| 近期公开事件 | `OP` 中通过目标企业主体过滤的事件标题、时间、来源、情感标签和详情；`WEB.sources[]` 中 `applicable_sections` 包含 `core`、`summary`、`needs` 或 `risk` 的合格企业事件 |
| 外部企业动态 | `WEB.sources[]` 中 `scope="company_update"` 的 `source_id`, `site_name`, `title`, `url`, `published_at`, `accessed_at`, `supported_fact`, `subject_match`, `corroboration_status` |
| 企业官网与外部描述 | `WEB.sources[]` 中 `scope="company_description"` 的对应字段；只保留业务定位、产品服务范围、技术或项目角色等可归因描述，不接受宣传排名和外部标准字段 |
| 关键决策人公开背景 | `WEB.sources[]` 中 `scope="person_background"` 的对应字段；只用于内部已确认人员的职业履历、教育背景、专业方向和公开职责介绍，不用于确定姓名、当前职务、人员范围或决策权限 |
| 外部有形资产线索 | `WEB.sources[]` 中 `scope="tangible_asset"` 的对应字段；只保留生产基地、厂房、仓储设施、研发或办公建筑、设备产线及在建工程的直接公开事实，不接收地址、经营范围、门店网络、客户项目或宣传性产能描述 |
| 外部行业背景 | `WEB.sources[]` 中 `scope="industry_context"` 的对应字段；只能形成定性背景，不提供企业标准字段、行业排名、均值、市场规模或增长率 |
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
4. 以规范企业全称调用上市公司财务 `financial_type="mainfinadata"`，`start_date` 为数据日期所在年份向前推三年的 `01-01`，`end_date` 为数据日期。只有存在按“核心经营数据生成规则”选出的有效年度报告时，才调用年度员工信息补充 `indicator_type="2"`；选定年度报告缺少 `sumAsset` 或 `sumLiab` 时，再以相同日期范围补查 `financial_type="rgbalance"`。三次状态分别记录，任一失败不影响报告其他章节。
5. 从 `B.basicList[0]` 构建行业查询范围。`regOrgCode` 严格匹配六位数字时，取前两位并追加四个 `0` 作为省级 `region_id`；`industryCode` 至少包含三位连续数字时，取前三位数字作为三级行业 `nic_id`。两项均有效时，使用 `region_lvl="r1"`、`nic_lvl="n3"`；任一项无效时，不自行猜测代码，省略全部范围参数并以行业分析响应中的 `lvl/regionId/nicId` 为实际范围。
6. 以规范企业全称并行调用行业分析的 `financialRegionRank`、`locfin`、`property`、`indLocOpr` 四种 `analysis_type`，每种类型分别记录 `success/empty/failed`，不得用一个类型的状态覆盖其他类型。行业分析任一类型失败不影响其他类型及报告其他章节。
7. 同时调用关联关系核验。只保留 `managementName`、`legalPerson`、`zzjgdm`、`suppId` 和 `kgEnt[].kgRatio/kgName/kgZzjgdm`；在写入 `REL` 前递归删除所有 `legalPersonCard`，禁止在任何临时证据、报告或回复中保存或展示该字段。
8. 同时并行调用土地资产、商标、专利、软件著作权、作品著作权、ICP、工商许可、荣誉资质和近 90 天舆情。土地资产以规范企业全称分别调用 `land_type="tdgy"`、`"tdcr"`、`"tddy"`，三类第一页均固定 `page_no="1"`、`page_size="10"`；默认不调用 `dkgs`。舆情日期使用执行日为 `end_date`，向前推 90 个自然日为 `start_date`，格式 `yyyy-MM-dd`，不设置情感过滤。
9. 土地供应读取 `detailListMeta.tdgyPageNum`，土地出让读取 `detailListMeta.tdcrPageNum`，土地抵押读取 `detailListMeta.tddyPageNum`。类别页数为有效正整数且大于 1 时，以相同 `ent_info`、`land_type` 和 `page_size` 继续请求第 2 页至末页。不得使用聚合的 `totalPage` 代替类别页数，不得因其他类别还有页数而重复请求当前类别。
10. 土地三类结果和状态相互独立：任一类别失败只将该类别记为 `failed`；成功但对应结果列表为空记为 `empty`；成功且存在有效记录记为 `success`。土地供应、土地出让、土地抵押分别进入 `META`，不得用一个汇总状态覆盖另外两类。

### 3. 定向搜索外部公开资料

内部主体确认后执行，不得提前用搜索结果猜测主体：

1. 将报告生成日向前推 12 个月作为动态搜索窗口，使用规范企业全称分别组合“官网”“公司简介”“关于我们”“企业介绍”“产品”“项目”“业务动态”“机构介绍”“专访”“报道”“重整”“并购”“股权变化”“管理调整”“公告”“处罚”“诉讼”“事故”“整改”等关键词；可信曾用名只用于补充搜索，命中页面仍须核验与当前规范主体的关系。
2. 先从 `B.personList` 整理最多 8 名展示人员；仅当该列表为空时，使用 `B.basicList[0].legRepName` 形成法定代表人兜底行。再对每名内部已确认人员，以“规范企业全称 + 姓名 + 内部职务”组合“简介”“履历”“简历”“管理团队”“董事”“高管”“任职”“教育背景”“工作经历”“专业背景”“公开演讲”等关键词定向搜索。外部搜索不得自行扩大关键决策人名单。
3. 人物背景优先采用目标企业官网管理团队或人物介绍页、交易所公告及定期报告、政府或监管机构页面；其次采用正规行业协会、高校、权威研究机构和满足准入要求的主流媒体。人物介绍页可以不受 12 个月窗口限制，但优先采用最新页面；超过 12 个月的内容只能写成带时间的历史教育或职业经历，不得据此认定当前职务。
4. 使用规范企业全称组合“生产基地”“厂房”“工厂”“产业园”“仓储”“仓库”“研发中心”“办公楼”“设备”“生产线”“在建工程”“项目备案”“环评”“规划许可”“建设进展”等关键词搜索有形资产线索。外部有形资产只接受政府、监管机构、自然资源或规划部门、交易所及目标企业官方网站等一级原始页面；三级媒体、行业协会、招商宣传稿和商业聚合页即使提及资产也不得进入本章节。
5. 外部资产页面必须直接点名规范企业主体，并明确描述特定设施、设备产线或建设项目。注册地址、联系地址、经营范围、所属行业、分支机构、销售门店、服务网点、客户项目现场、荣誉、订单、融资、产品介绍和一般产能宣传均不构成有形资产证据。企业官网稳定设施介绍页可无发布日期但必须记录访问日期；超过 12 个月的政府、交易所或企业公告只能作为带明确日期的历史建设节点，不得据此表述当前仍持有、在建、已投产或正在使用。
6. 使用内部工商行业名称组合“政策”“统计”“运行情况”“行业报告”等关键词，优先限定政府、统计机构、正规行业协会、高校和权威研究机构域名。不得使用外部网页重新判定企业行业归属。
7. 先搜索，再逐页打开候选原始页面，执行来源等级、发布日期、主体匹配、正文事实、URL 和交叉验证检查。人物页面还必须在正文中同时确认人员姓名及其与规范企业全称的关系；资产页面还必须确认资产对象、企业角色和事件时点。仅搜索标题命中、仅同名、只关联曾任其他企业或关系无法确认时排除。合格页面按最终采用顺序分配 `W1`、`W2`……；同一规范 URL 只保留一次。
8. 外部企业动态可以进入 `D.core_turning_point`、`D.core_external_context`、`D.core_viewpoint`、`D.value_judgment`、`D.opportunities`、`D.visit_advice`、`D.visit_questions` 或近期公开事件证据；合格企业官网自述和正规外部机构描述可以进入 `D.core_company_self_description`、`D.core_external_description` 和 `D.core_viewpoint`；合格人物背景只进入对应 `D.person_rows[].background`、`D.people_interpretation`，或作为已引用背景事实进入拜访问句；合格外部有形资产事实只进入 `D.tangible_asset_rows[]`、`D.assets_interpretation`，或作为已引用资产事实进入拜访问句；外部行业背景只进入 `D.industry_external_context`、相关行业定性解读和拜访问句。一般行业政策、市场趋势和宏观背景不得进入核心观点；只有一级来源明确点名目标企业、其项目或其直接业务动作时，才可按企业事件使用。每个使用位置在 `D.source_attributions` 登记对应 `source_id`。
9. 企业官网动态使用“企业官网披露”归因；企业官网人物简介使用“企业官网介绍”归因；企业官网设施或设备信息使用“企业官网披露”并保留自述边界。三级媒体采用交叉验证来源时，把全部支持同一事实的 `source_id` 登记到 `EVIDENCE`，不得只保留其中一条。
10. 网络工具可用且完成搜索但没有合格页面时设 `WEB.status="empty"`；工具不可用、超时或无法打开原始页面时设 `WEB.status="unavailable"`；至少采用一条来源时设 `WEB.status="success"`。搜索失败不改变任何内部维度状态，也不删除内部人员或内部资产记录。

记录每个维度的状态：

- `success`：成功且有有效数据；
- `empty`：成功但返回空列表或无结果；
- `failed`：工具不可用、超时、权限不足或调用失败。

`META.successful_dimensions` 只列 `success` 维度，`META.empty_dimensions` 只列 `empty` 维度，`META.failed_dimensions` 只列 `failed` 维度；同一维度不得重复出现在多个状态字段中。

内部扩展维度或外部搜索失败时继续生成其他已取得内容；工商深度失败时终止。

### 4. 构建统一证据模型

先把内部 MCP 原值和合格外部证据整理为以下 UTF-8 JSON，再从同一 JSON 生成 Markdown 和 PDF。禁止让两个格式分别归纳原始响应或重新搜索。

```json
{
  "META": {
    "report_id": "CP-YYYYMMDD-HHMMSS",
    "generated_at": "YYYY-MM-DD HH:MM:SS",
    "classification": "机密",
    "successful_dimensions": "以、连接",
    "empty_dimensions": "以、连接",
    "failed_dimensions": "以、连接",
    "web_search_status": "success|empty|unavailable"
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
  "IND": {
    "query_scope": {"nic_lvl": null, "region_lvl": null, "nic_id": null, "region_id": null},
    "financialRegionRank": {"status": "success|empty|failed", "data": "该分析类型 data 原值"},
    "locfin": {"status": "success|empty|failed", "data": "该分析类型 data 原值"},
    "property": {"status": "success|empty|failed", "data": "该分析类型 data 原值"},
    "indLocOpr": {"status": "success|empty|failed", "data": "该分析类型 data 原值"}
  },
  "REL": {
    "status": "success|empty|failed",
    "suppList": ["删除 legalPersonCard 后的必要关系原值"]
  },
  "FIN_LISTED": {
    "mainfinadata": {"status": "success|empty|failed", "data": "mainfinadata 查询 data 原值"},
    "rgbalance": {"status": "success|empty|failed|not_called", "data": "按条件补查的 rgbalance data 原值"}
  },
  "FIN_KEY": {
    "status": "success|empty|failed|not_called",
    "data": "仅在存在有效上市公司年度报告时查询的企业关键指标 data 原值"
  },
  "TM": "商标工具 data 原值",
  "IP": "专利工具 data 原值",
  "SW": "软件著作权工具 data 原值",
  "WC": "作品著作权工具 data 原值",
  "ICP": "ICP备案工具 data 原值",
  "LIC": "工商许可工具 data 原值",
  "HON": "荣誉资质工具 data 原值",
  "OP": "舆情工具完整返回原值",
  "WEB": {
    "status": "success|empty|unavailable",
    "searched_at": "YYYY-MM-DD HH:MM:SS",
    "window": {"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"},
    "queries": ["实际执行的查询词"],
    "sources": [
      {
        "source_id": "W1",
        "scope": "company_update|company_description|person_background|tangible_asset|industry_context|public_event",
        "site_name": "发布网站或机构名称",
        "source_level": "一级|二级|三级",
        "source_type": "government|regulator|court|exchange|statistics|company_official|association|university|research_institute|mainstream_media",
        "title": "原始页面标题",
        "url": "规范化原始页面 URL",
        "published_at": null,
        "accessed_at": "YYYY-MM-DD",
        "supported_fact": "该页面直接支持的最小事实",
        "applicable_sections": ["core", "summary", "people", "assets"],
        "subject_match": "exact|verified_alias|person_company_match|asset_company_match|industry_scope",
        "corroboration_status": "primary|traced_to_primary|cross_checked|company_self_disclosure",
        "corroborating_source_ids": []
      }
    ]
  },
  "D": {
    "brand_name": null,
    "registered_capital_display": "注册资本和币种原值的可读组合",
    "paid_in_capital_display": null,
    "operating_address": null,
    "employee_scale": null,
    "qualifications": null,
    "source_attributions": {
      "core": {"internal_dimensions": ["实际进入核心观点的内部业务维度"], "external_source_ids": ["实际进入核心观点的 Wn"]},
      "summary": {"internal_dimensions": [], "external_source_ids": []},
      "basic": {"internal_dimensions": ["工商登记"], "external_source_ids": []},
      "people": {"internal_dimensions": [], "external_source_ids": []},
      "equity": {"internal_dimensions": [], "external_source_ids": []},
      "assets": {"internal_dimensions": [], "external_source_ids": []},
      "operations": {"internal_dimensions": [], "external_source_ids": []},
      "industry": {"internal_dimensions": [], "external_source_ids": []},
      "needs": {"internal_dimensions": [], "external_source_ids": []},
      "risk": {"internal_dimensions": [], "external_source_ids": []}
    },
    "coverage_summary": "以业务语言概括资料覆盖范围和待补充事项",
    "section_numbers": {"core": "一", "summary": "二", "profile": "三", "industry": null, "needs": "四", "risk": null},
    "company_overview_facts": {
      "identity": {"org_name": null, "org_status": null, "former_names": [], "established_at": null, "province": null, "scale": null, "industry": null},
      "capital": {"registered_capital": null, "paid_in_capital": null},
      "market_events": [],
      "business_signals": [],
      "tax_context": null,
      "risk_hits": []
    },
    "company_overview_fallback": "按原字段选择和固定顺序确定性拼接的内部回退文本",
    "core_internal_baseline": "AI 仅使用 company_overview_facts 生成的自然内部主体描述",
    "core_capability": "从内部品牌、产品、许可、资质、知识产权、项目或资产事实中归纳的核心能力信号",
    "core_company_self_description": "有合格官网稳定介绍时形成的企业自述归因",
    "core_external_description": "有合格正规外部来源时形成的企业业务定位描述归因",
    "core_turning_point": "有证据时展示的并购、重整、上市退市、重大股权变化或重大项目转折",
    "core_external_context": "近 12 个月最多两项合格企业动态或直接点名企业的一级来源事件",
    "core_operating_stage": "内部经营事实支持的阶段判断，或外部动作与内部量化资料之间的审慎边界",
    "core_risk_constraint": "最重要的内部风险事实、主体范围、时点状态和必要的外部事件线索",
    "core_visit_focus": "由前述变化、风险和信息缺口形成的 2 至 3 项拜访核验重点",
    "core_viewpoint": "按固定叙事顺序融合内部主体底座和合格外部事实形成的最终核心观点",
    "value_judgment": "企业定位、可见能力信号和拜访价值的事实归纳",
    "opportunities": "目标企业自身公开事件、有效荣誉、许可或业务范围形成的访谈机会线索",
    "risk_summary": "命中风险维度、数量、范围和数据边界的摘要",
    "visit_advice": "基于已有事实形成的访前沟通主线和核验重点",
    "basic_interpretation": "基本登记事实与访前含义",
    "person_rows": [
      {
        "name": "内部已确认人员姓名",
        "position": "内部职务与法定代表人身份的去重组合；均缺失时使用固定资料边界说明",
        "is_legal_representative": false,
        "background": "经核验的公开职业背景及来源标记，或固定资料边界说明",
        "background_source_ids": []
      }
    ],
    "people_interpretation": null,
    "has_equity_or_network": false,
    "shareholder_rows": [],
    "network_summary": null,
    "equity_interpretation": null,
    "has_assets": false,
    "tangible_asset_rows": [
      {
        "asset_type": "土地供应|土地出让|土地抵押|生产基地或厂房|仓储设施|研发或办公建筑|设备或生产线|在建工程",
        "fact": "直接可核验的精简资产事实；外部事实句末附来源 ID",
        "boundary": "当前权属、使用状态、项目阶段或价值口径边界",
        "source_ids": []
      }
    ],
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
    "has_core_operations": true,
    "has_core_operation_rows": false,
    "core_operation_rows": [],
    "operations_period": null,
    "operations_boundary": "有年度财务事实时说明报告期和范围；否则显示固定业务提示",
    "operations_interpretation": null,
    "has_industry_insight": false,
    "industry_positioning": null,
    "industry_external_context": null,
    "industry_scope_display": null,
    "industry_climate_rows": [],
    "industry_climate_interpretation": null,
    "industry_benchmark_rows": [],
    "industry_benchmark_interpretation": null,
    "has_industry_risk": false,
    "industry_risk_rows": [],
    "industry_risk_interpretation": null,
    "visit_questions": [],
    "has_risks": false,
    "risk_evidence_groups": {
      "subject_compliance": {"status": "hit|context|empty|unavailable", "facts": []},
      "judicial_enforcement": {"status": "hit|context|empty|unavailable", "facts": []},
      "asset_encumbrance": {"status": "hit|context|empty|unavailable", "facts": []},
      "tax_license_compliance": {"status": "hit|context|empty|unavailable", "facts": []},
      "financial_attention": {"status": "hit|context|empty|unavailable", "facts": []},
      "public_event_clues": {"status": "hit|context|empty|unavailable", "facts": []}
    },
    "risks": [],
    "risk_zero_dimensions": "以、连接的明确零值维度",
    "risk_compliance_context": "最新纳税评级、明确许可状态及必要的时间边界",
    "risk_information_boundary": "以业务语言说明无明细、时间较早、资料缺失或不同范围不可合并",
    "risk_interpretation": null
  },
  "EVIDENCE": {
    "company_overview_facts": ["internal:B.basicList[0].orgName", "实际进入内部事实白名单的 internal:B/OV_BASIC/OV_BRIEF/OV_MARKET/OV_TAX/OV_RISK 字段"],
    "company_overview_fallback": ["实际进入确定性回退文本的 internal:B/OV_BASIC/OV_BRIEF/OV_MARKET/OV_TAX/OV_RISK 字段"],
    "core_internal_baseline": ["AI 主体描述逐句使用的 internal:company_overview_facts 对应原始字段"],
    "core_capability": ["实际支持能力信号的 internal:B/OV_MARKET/LAND/TM/IP/SW/WC/ICP/LIC/HON 字段"],
    "core_company_self_description": ["实际进入企业官网自述的 external:Wn"],
    "core_external_description": ["实际进入正规外部机构描述的 external:Wn"],
    "core_turning_point": ["实际支持关键转折的 internal:B/OV_MARKET 字段或 external:Wn"],
    "core_external_context": ["实际进入近期观察的 external:Wn"],
    "core_operating_stage": ["实际展示的 internal:FIN_LISTED/OP 字段、信息边界或 external:Wn"],
    "core_risk_constraint": ["实际进入核心风险约束的 internal:<归一化风险事实> 或 external:Wn"],
    "core_visit_focus": ["支持核验重点的 internal:<事实和数据缺口> 或 external:Wn"],
    "core_viewpoint": ["逐句登记上述核心观点分项实际使用的 internal:<字段或状态> 与 external:Wn"],
    "coverage_summary": ["internal:META 中各业务维度状态和 web_search_status"],
    "source_attributions": ["逐章节登记实际显示的内部业务维度和 external:Wn；外部 ID 必须存在于 WEB.sources"],
    "person_rows": ["逐行登记姓名和职务对应的 internal:B.personList 或 internal:B.basicList[0].legRepName；背景事实另登记 external:Wn"],
    "people_interpretation": ["实际使用的 internal:<人员字段或资料边界> 与 external:Wn"],
    "tangible_asset_rows": ["逐行登记实际使用的 internal:LAND/B 明确抵押物字段或 external:Wn；不登记行业、经营范围、注册地址和未展示字段"],
    "assets_interpretation": ["实际进入有形或无形资产展示的 internal:<字段和边界> 与 external:Wn"],
    "industry_positioning": ["实际使用的 internal:B.basicList[0] 行业、经营范围和经工商事实交叉验证的 internal:REL 字段"],
    "industry_external_context": ["实际进入定性行业背景的 external:Wn"],
    "industry_scope_display": ["实际用于确定中文地区名和中文行业名的 internal:B/IND 字段，以及仅用于一致性核验的 regionId/nicId"],
    "industry_climate_rows": ["实际使用的 internal:IND.financialRegionRank/locfin 字段"],
    "industry_climate_interpretation": ["进入行业景气表的 internal:<事实字段和信息边界>"],
    "industry_benchmark_rows": ["实际使用的 internal:IND.financialRegionRank/property 字段"],
    "industry_benchmark_interpretation": ["进入行业对标表的 internal:<事实字段和信息边界>"],
    "industry_risk_rows": ["实际使用的 internal:IND.indLocOpr 字段"],
    "industry_risk_interpretation": ["进入行业风险表的 internal:<事实字段和信息边界>"],
    "core_operation_rows": ["实际进入核心经营数据表的 internal:FIN_LISTED/FIN_KEY 原值及选定报告期"],
    "operations_boundary": ["internal:FIN_LISTED.mainfinadata 状态、有效年度报告选择结果和必要的信息边界"],
    "operations_interpretation": ["实际展示的 internal:<核心经营数据字段和选定报告期>"],
    "value_judgment": ["直接支持该归纳的 internal:<字段> 或 external:Wn"],
    "opportunities": ["直接支持该访谈线索的 internal:<字段>、目标企业自身舆情记录或 external:Wn"],
    "risk_summary": ["直接支持该风险摘要的 internal:<列表、数量和范围> 或 external:Wn"],
    "risk_evidence_groups": ["逐组登记实际使用的 internal:B/OV_RISK/OV_TAX/LAND/LIC/HON/FIN_LISTED/OP 或 external:Wn 及主体、时间、状态和范围"],
    "risks": ["逐行登记对应 internal:<归一化风险事实> 或 external:Wn，不以原始响应临场概括"],
    "risk_compliance_context": ["实际使用的 internal:OV_TAX/LIC/HON 字段及其年份、有效期和状态边界"],
    "risk_information_boundary": ["internal:<明细可用性、时间范围、非上市公司财务资料状态及不可合并范围> 或 external:Wn"],
    "risk_interpretation": ["实际进入风险表和合规提示的 internal:<归一化事实> 或 external:Wn"],
    "visit_advice": ["支持该沟通主线的 internal:<事实和数据缺口> 或 external:Wn"],
    "其他 D 文案字段": ["对应 internal:<字段或状态> 或 external:Wn"]
  }
}
```

整理规则：

- `B`、`ID`、`OV_*`、`LAND`、`IND`、`REL`、`FIN_*`、`TM` 至 `OP` 保存对应工具的必要原值；`REL` 必须先删除个人证件号。`WEB` 只保存实际执行的查询和通过来源准入、正文核验且可能进入报告的网页证据；被排除的候选页不得进入 `WEB.sources`。`D` 只保存确定性简述、忠实压缩文案、条件布尔值和固定表格所需的派生展示项。
- 工商深度成功后，`D.company_overview_facts`、`D.company_overview_fallback`、`D.core_internal_baseline`、`D.core_capability`、`D.core_operating_stage`、`D.core_visit_focus`、`D.core_viewpoint`、`D.value_judgment`、`D.opportunities`、`D.risk_summary`、`D.visit_advice`、`D.basic_interpretation` 和 `D.visit_questions` 为必填；`D.core_company_self_description`、`D.core_external_description`、`D.core_turning_point`、`D.core_external_context`、`D.core_risk_constraint` 有证据时填写，没有证据时保持 `null`。不得因生成困难隐藏“一、核心观点”“二、执行摘要”或需求核验问题。
- 完成所有条件板块显隐判断后，按“核心观点 → 执行摘要 → 客户全景画像 → 产业画像与行业洞察（可选）→ 需求识别与拜访核验 → 风险预警与合规提示（可选）”过滤不可见板块，再从“一”开始连续填写 `D.section_numbers`。产业画像显示时依次为“一、二、三、四、五”，风险章节显示时继续为“六”；产业画像隐藏时需求识别仍为“四”，风险章节显示时为“五”。不得跳号、重号或根据历史编号保留空位；“报告使用说明”不编号，小节“（一）～（五）”不参与重编号。
- `D.has_core_operations` 在工商主体确认后固定为 `true`，用于确保财务数据不足时仍显示业务提示；其他 `D.has_*` 只在对应板块至少存在一项有效内部事实或本 Skill 明确允许的合格外部事实时设为 `true`，不得为了保留版面而设为 `true`。
- `D.source_attributions.<section>.internal_dimensions[]` 只列实际为该章节提供可见事实的内部业务维度，不得列入 `empty`、`failed`、`not_called` 或未展示维度；`external_source_ids[]` 只列实际进入该章节正文的 `WEB.sources[].source_id`，按首次出现顺序去重。人员表展示时 `people.internal_dimensions[]` 必须包含实际使用的“工商登记（主要人员）”或“工商登记（法定代表人）”。`basic/equity/operations` 的 `external_source_ids[]` 固定为空；`people.external_source_ids[]` 只允许登记实际进入人员背景列或人员信息解读的 `scope="person_background"` 来源，`assets.external_source_ids[]` 只允许登记实际进入有形资产表或资产解读的 `scope="tangible_asset"` 来源，其他外部事实登记到 `core/summary/industry/needs/risk`。核心观点只接收符合“综合核心观点生成规则”的企业级事实。
- 外部事实所在句末必须附 `[外部：Wn]`；同一事实由多个外部来源支持时附全部 ID，例如 `[外部：W2、W3]`。企业官网自述必须在正文中同时出现“企业官网披露”。内部事实不添加行内 ID，通过章节的“内部：”来源行追溯。
- 基本信息只保留非空字段。展示层的无损格式化仅包括：纯数字整数部分增加千分位；严格匹配 `YYYY-MM-DD` 的日期显示为“YYYY年M月D日”；曾用名中的半角逗号、全角逗号或分号统一为“、”；已知币种代码显示其接口同时返回的中文名称；文档明确为比率的 `IND` 十进制值使用任意精度十进制乘以 100、删除无意义尾零后追加 `%`。必须保留全部有效数字和小数位，不得四舍五入；无法可靠识别时直接显示原值。
- `D.registered_capital_display` 使用无损格式化后的 `regCap` 与 `regCapCur` 组合为“金额单位（币种）”；接口明确 `regCap` 单位为万元时追加“万元”，不得重复单位。实缴资本同理。
- 股东最多展示 15 名，整理为 `D.shareholder_rows[] = {name, ratio_display, amount_display}`。比例可解析时仅用于排序；比例、认缴额和币种在展示层只允许上述无损格式化，不可解析时保持接口顺序和原值。
- 关键决策人最多展示 8 名，先完全按内部字段整理为 `D.person_rows[] = {name, position, is_legal_representative, background, background_source_ids}`。只有 `isFr` 原值明确表示真时，才将布尔字段设为 `true`；`position` 由内部 `position` 与“法定代表人”去重组合，外部网页不得修改；两者均缺失时固定写“内部资料未列明职务”，不得留空。`B.personList` 为空但 `B.basicList[0].legRepName` 非空时，生成一条 `{name: legRepName, position: "法定代表人", is_legal_representative: true, background: "公开资料未形成可核验的职业背景介绍。", background_source_ids: []}` 作为兜底。外部搜索不得新增人员行。
- 对每条 `D.person_rows`，只从 `scope="person_background"` 且 `subject_match="person_company_match"` 的合格页面提炼与访前准备有关的教育背景、公开职业履历、专业方向、历史任职和页面明确披露的职责介绍；每项外部事实在单元格句末附 `[外部：Wn]`，并把相同 ID 写入该行 `background_source_ids[]`、`EVIDENCE.person_rows` 和 `D.source_attributions.people.external_source_ids[]`。企业官网内容写“企业官网介绍”，其他来源写明发布机构；不得照搬宣传评价。
- 人物背景优先采用最新、直接、原始页面。外部页面披露的当前职务与内部 `position` 不一致时，职务列仍使用内部值；背景列只可写“{来源}于{日期}曾披露其担任……，与当前内部登记职务存在时间或口径差异，建议核实”并附来源 ID，不得由模型选择或合并。历史任职必须带可核验时间或明确写“曾任”，不得改写为现任。
- 如果某行没有合格外部背景，`background` 固定写“公开资料未形成可核验的职业背景介绍。”，不得留空、不得根据姓名或职务推测。`D.people_interpretation` 按“内部人员构成与公开职业背景概括 → 信息边界 → 拜访核验方向”生成；不得根据职务名称或履历推断真实决策权、控制关系或具体分工。全部人员均无背景来源时，明确说明公开资料未形成可核验的职业背景补充，并建议现场确认业务、财务及技术议题的实际参与人。
- 有形资产按下方“有形资产生成规则”整理为精简事实表；无形资产各类型最多展示 3 个代表名称。无形资产总量使用分页元数据，最终报告统一称“代表记录”或“样本记录”。
- 荣誉资质只展示本报告采纳的代表记录数量，不得称全量，不得使用“返回”描述。
- 舆情最多展示 5 条，保留标题、日期、来源和接口情感标签。只有目标企业是事件主体，且标题或详情明确涉及其产品、项目、许可、荣誉、业务动作或风险事项时，才可进入 `D.opportunities` 或风险文案；舆情、融资、荣誉和客户线索均不得混入核心经营数据表。
- 排除只把目标企业作为概念股、行情标的、行业举例或顺带提及的文章；排除无法确认主体、重复标题和纯市场价格波动内容。
- 企业风险先按“主体与行政合规 → 司法与执行 → 股权及资产权利负担 → 税务与许可合规 → 财务经营关注 → 近期公开事件”六组归一化到 `D.risk_evidence_groups`，再生成 `D.risks[] = {topic, detail, scope}`；禁止让大模型直接读取原始响应临场分类。
- 风险事实只写目标企业自身记录；关联主体、股东或人员记录必须单独标明主体范围，不得并入企业自身失信、执行或债务结论。只有明确大于零的统计、非空且主体范围可确认的风险列表、明确异常的许可或资质状态、选定年度财务记录中的直接负值或合格的目标企业自身负面舆情才能进入风险表。
- 明确为零的近两年风险字段名称按固定顺序以“、”连接后写入 `D.risk_zero_dimensions`，不得进入风险表或写成“无风险”；最新纳税评级和明确许可状态只进入 `D.risk_compliance_context`，不得据此生成守法、低风险或信用结论。
- `D.visit_questions[] = {topic, basis, question}`，可询问主营收入结构、客户集中度、现金流、融资需求、研发投入和合作诉求，但不得预设答案或推荐具体银行产品。
- `D.coverage_summary` 只用工商登记、关键决策人及公开职业背景、股权与关联关系、上市公司财务、土地及外部设施资产、行业统计与排名、知识产权、备案许可、荣誉资质、纳税评级、近期公开动态、外部企业动态、外部行业背景和近两年风险等业务名称概括资料范围；内部已覆盖内容写“报告已覆盖……”，内部无可展示内容写“公开资料中暂无可供展示的……”，内部失败写“相关资料尚待补充”。`WEB.status="empty"` 时写“外部公开资料未形成可用补充”，`WEB.status="unavailable"` 时写“外部公开资料检索尚待补充”。不得出现企业 ID 解析、工商简项、产品码、工具名、内部别名或原始状态代码。
- “产业画像与行业洞察”的企业行业归属、经营范围、排名、均值、比率和其他量化表格只使用本次 `B`、`IND` 和经工商事实交叉验证的 `REL` 证据；允许合格 `WEB` 证据形成定性政策、行业运行背景和访谈方向，但不得用网络搜索、模型知识或参考样稿补充企业标准字段、市场规模、CAGR、竞争格局、上下游名单、交易关系或任何缺失量化值。“与我行合作现状”“（二）产品精准匹配”和“（三）定制化营销方案”仍不进入当前骨架。
- `D.has_risks=true` 时必须生成 `D.risk_interpretation`；只总结命中事实、范围和需核实事项，不评级、不推演未来损失。
- 每个非空 `D` 文案字段都必须在 `EVIDENCE` 中登记来源；内部来源写成 `internal:B/ID/OV_*/LAND/IND/REL/FIN_*/TM...OP.<字段或状态>`，外部来源写成 `external:Wn`。任何 `external:Wn` 都必须能在 `WEB.sources` 找到完整元数据并出现在对应章节的 `D.source_attributions.<section>.external_source_ids[]`。

#### 有形资产生成规则

1. `D.tangible_asset_rows[] = {asset_type, fact, boundary, source_ids}`，最多展示 6 行，固定按“土地供应 → 土地出让 → 土地抵押 → 生产基地或厂房 → 仓储设施 → 研发或办公建筑 → 设备或生产线 → 在建工程”排序。同类多条事实优先保留时间较近、对象更具体、主体关系更明确的一条；不得把事实拆成冗长背景叙述。
2. 有形资产的准入条件是证据直接描述具体土地、建筑物、设施、机器设备、生产线或建设项目。`B.basicList[0].industryClas`、`industry`、`operateScope`、`regAddr`、`websiteOrOnlineList`、`filiationList`、企业规模、注册资本、许可、荣誉、知识产权、招投标、客户项目和一般产品信息固定不得进入 `D.tangible_asset_rows`，也不得触发 `D.has_assets`。
3. 内部土地记录按页码顺序合并对应 `tdgyResults[]`、`tdcrResults[]`、`tddyResults[]`；只删除同一类别内 JSON 内容完全一致的重复对象并保留首次出现项，不得跨类别合并。每类最多形成一行：使用对应 `detailListMeta.*Count` 作为记录数，并选择一条代表记录；不再概括主要区域或主要用途，不再计算面积、成交价格或抵押金额合计。
4. 土地供应代表记录按可解析的 `supplyArea` 从大到小选择，面积相同时按有效 `contractDate` 从新到旧选择；土地出让按 `landArea` 从大到小、再按 `pubDate` 从新到旧选择；土地抵押按 `pubDate`、再按 `boardStartDate` 从新到旧选择。排序解析值不得替换原值。代表事实只保留项目或宗地名称、位置或编号、用途、单条面积或金额、日期中有值且与识别资产直接相关的字段，连续字段不超过 5 项。
5. `B` 中的工商抵押、司法协助或其他记录只有在目标企业主体明确，且抵押物或权利对象明确写明房产、土地、厂房、机器设备、生产线等具体有形资产时，才可形成一行；只有登记编号、债权金额、当事人或状态而没有具体资产对象时只进入风险证据，不进入有形资产表。
6. 外部有形资产只使用 `scope="tangible_asset"`、`source_level="一级"`、`subject_match="asset_company_match"` 的政府、监管、自然资源或规划部门、交易所及目标企业官网原始页面。正文必须同时确认规范企业全称、具体资产或建设项目、企业角色和事件时点；每行外部事实句末附 `[外部：Wn]`，并把相同 ID 登记到该行 `source_ids[]`、`EVIDENCE.tangible_asset_rows` 和 `D.source_attributions.assets.external_source_ids[]`。
7. 外部事实仅允许写设施或项目名称、设施类型、城市或园区级位置、公开建设/投产/使用节点和设备产线类别。禁止从外部网页补填土地或房产证号、宗地编号、面积、交易价格、投资额、账面价值、评估价值、产能、设备数量、抵押金额、当前权属及内部结构化数量；页面即使披露这些数值也不得进入报告。
8. 企业官网内容必须写“企业官网披露”，并在 `boundary` 写明“企业自述仅确认公开披露的设施或使用场景，不证明产权、租赁关系、账面价值或当前状态”。政府、监管、规划或交易所页面只确认其直接披露的审批、备案、建设、交易或公告节点；未明确完工、投产、使用或持有时不得升级状态。
9. 历史外部页面必须保留原始日期并写成“于{日期}披露/备案/公告”；不得据此使用“现有”“目前”“正在”“已投产”等当前时态。外部来源之间或与内部记录冲突时优先直接一级原始页面；仍无法消解时并列写入 `boundary` 或只保留内部事实，不由模型选择产权、面积或状态。
10. 地址、行业、经营范围、销售门店、服务网络、终端数量、分支机构、展厅、客户现场、合作园区、产品交付、订单、融资、荣誉和招商宣传均与资产权属或设施事实不足以直接关联，固定排除。仅提及“建设基地”“计划投资”“拟购置设备”但没有明确备案、审批、公告或实施节点时，也不得进入有形资产表。
11. 土地供应、土地出让只称“公开土地记录”或“涉及土地供应/土地出让”，不得称为当前产权、当前持有土地或自有土地；土地抵押和具体抵押物只说明公开登记事实，不得推导当前仍有效、已经解除、资产价值或企业偿债能力。不得用任何内部或外部事实推导“轻资产”“重资产”“自有房产”“自有厂房”或“资产实力”。
12. `D.has_assets=true` 仅在 `D.tangible_asset_rows` 至少一行，或任一无形资产事实非空时成立。有形资产没有合格事实、但存在无形资产时，仅显示无形资产；两者均为空时隐藏整个资产章节。不得为了保留“有形资产”标题输出空段、通用边界句或“暂无记录”。
13. `D.assets_interpretation` 只接收已经展示的 `D.tangible_asset_rows` 和无形资产代表事实，按“可见资产事实 → 权属与时点边界 → 拜访核验方向”生成；不得重新引入被排除的地址、经营范围、行业、注册资本或项目宣传。只有无形资产时只解释无形资产，不补写有形资产缺口。
14. `EVIDENCE.tangible_asset_rows` 逐行登记实际进入表格的最小 `internal:LAND/B.<字段>` 或 `external:Wn`、主体、日期、对象和边界。没有进入表格的字段、空结果、失败状态、被排除网页和用于排序但未展示的值不得作为有形资产证据。

#### 产业画像生成规则

1. 满足以下任一条件时设置 `D.has_industry_insight=true`：`IND.financialRegionRank`、`IND.locfin`、`IND.property` 或 `IND.indLocOpr` 至少一类存在可展示内部事实；或 `B.basicList[0].industry` 非空且 `WEB.sources` 至少存在一条 `scope="industry_context"` 的合格来源。`REL` 单独成功、仅有工商行业字段但无合格外部行业背景，均不得触发产业画像章节。
2. 用 `B.basicList[0].industry` 说明企业工商行业层级，用 `operateScope` 概括与主营活动相关的经营范围原文；只称“行业归属”“经营环节线索”，不得据此断言企业位于产业链上游、中游或下游。外部网页不得决定或更改企业行业归属。
3. 确定性生成 `D.industry_scope_display`，统一供行业景气、行业对标、行业风险的表格和解读使用：
   - 中文地区名优先使用与所选行业记录一致、含中文且不含对应 `regionId` 代码片段的 `IND.indLocOpr.data[].region`；该字段缺失或夹带内部编码时，只有当查询的省级 `region_id` 确由同一主体的 `B.basicList[0].regOrgCode` 构建，或行业记录的 `regionId` 与查询范围一致时，才使用 `B.basicList[0].regOrgProvince`。不得根据行政区划代码自行猜测地区名。
   - 中文行业名优先使用与所选行业记录一致、含中文且不含对应 `nicId` 代码片段的 `IND.indLocOpr.data[].indsy`；该字段缺失或夹带内部编码时，只有当三级 `nic_id` 确由同一主体的 `B.basicList[0].industryCode` 构建，且 `B.basicList[0].industry` 按半角连字符 `-` 切分后至少有三个非空层级时，才使用第三级中文名称。不得使用互联网、模型记忆或样例映射行业代码。
   - 同时取得中文地区名和中文行业名时直接拼接；行业名以“行业”或“业”结尾时不再追加，其他名称追加“行业”。例如地区为“安徽省”、三级行业名为“输配电及控制设备制造”时，固定显示“安徽省输配电及控制设备制造行业”。
   - 只有中文地区名时显示“{地区}相关三级行业”；只有中文行业名时显示“{行业名按上述后缀规则处理}”；二者都无法核验时显示“相关三级行业”。不得为追求完整而猜测名称。
4. `IND.query_scope.region_id/nic_id` 及各行业记录的 `regionId/nicId` 仅用于查询、范围一致性核验和 `EVIDENCE`，禁止进入最终报告的可见表格、`period_scope`、信息解读或其他正文；不得显示“三级行业C382”“行业代码 C382”或在中文行业名后括注内部编码。
5. `REL.suppList[].kgEnt[]` 不具有可直接展示的上下游交易语义。对 `kgName` 和 `B.shareholderList[].shareholderName` 先执行 Unicode NFKC、删除空白及中英文括号等仅影响书写的符号后比较；名称相同且 `kgRatio` 与 `fundedRatio` 可解析为完全相等的十进制比例时，只记为股东事实的交叉验证，不新增或重复展示。未匹配记录不得称为供应商、客户、控股企业、上下游企业或交易对手，不展示主体名称和比例，只把客户结构、供应商结构、采购与销售关系列为拜访核验问题。
6. `financialRegionRank.data[0].rankAndFourRank[]` 只保留 `ancheYear` 为四位年份、且至少一个 `orderAssgroRank/orderVendincRank/orderNetincRank/orderRoeRank/orderLoarRank` 为正整数的记录；同时要求 `numEnts[]` 中存在相同年份且 `nument` 为正整数。按年度从大到小选择第一条作为财务对标年度，排名和企业数必须成对展示。
7. `numEnts[]` 的行业企业数趋势只使用早于报告生成年份的完整年度，按年度倒序取最近两条正整数记录。只写“公开统计企业数由{较早年度数量}变为{较晚年度数量}”，不得把数量变化解释为市场规模、行业收入、市场份额、景气指数或增长率。
8. `locfin.data[]` 只保留 `numEnt` 为正整数且 `avgLoar/avgVendinc/medRoe/medVendinc/medLoar` 至少一个为有效数字的记录。金额保留“万元”单位和原始精度；比率按本 Skill 的精确百分比展示规则处理。该类型没有年度字段时，时间与范围固定写“时间未标明；以{D.industry_scope_display}范围为准”，不得与指定年度的企业财务值作同口径比较。
9. `property.data[]` 仅展示有效正整数排名和对应行业平均值。可使用的排名限于发明专利、实用新型专利、外观专利、专利总数、软件著作权、作品著作权、商标总数、有效期内商标和著作权；空值、非正整数及所有 `*RankFour` 字段直接省略，不解释四分位含义。
10. `indLocOpr.data[]` 只选择 `ancheYear` 最新、且至少存在一个有效风险比率的年度记录。行业风险最多展示四行并固定按“注吊销 → 新注册与注吊销 → 被执行人 → 失信被执行人”排列；每个主题优先使用近 12 个月字段，缺失时依次回退近 6 个月、近 3 个月字段，其中被执行人和失信被执行人没有近 3 个月字段。只有文档明确为比率、原值为有效非负十进制数且大于零的选中字段进入 `D.industry_risk_rows`；明确为零只表示该行业统计项原值为零，不生成“行业无风险”结论。
11. `D.industry_climate_rows[] = {topic, fact, period_scope}`；来源限于企业数趋势、`locfin` 行业财务参考和 `indLocOpr` 中不属于风险判断的有效行业结构指标。`D.industry_benchmark_rows[] = {topic, company_position, industry_reference, period_scope}`；来源限于匹配年度的财务排名及 `property` 有效排名和行业平均值。两个表格的 `period_scope` 必须使用 `D.industry_scope_display`，不得临场拼接地区或行业代码。`D.industry_risk_rows[] = {signal, fact, verification}`；来源限于 `indLocOpr` 明确大于零的风险比率，行业范围表述同样必须使用 `D.industry_scope_display`。
12. 产业链定位固定按“内部工商行业层级 → 内部经营范围中的业务活动 → 关联信息边界 → 拜访核验方向”生成 `D.industry_positioning`。必须明确现有资料不能确认客户、供应商、采购金额、销售金额及交易集中度，不得虚构产业链图谱。
13. `D.industry_external_context` 只使用合格 `scope="industry_context"` 来源，按“权威发布主体及日期 → 与内部行业归属相关的定性背景 → 拜访核验方向”生成；每个事实附 `[外部：Wn]`。不得从外部网页抽取或计算企业标准字段、企业财务值、行业排名、行业均值、市场规模、增长率、CAGR、市场份额、竞争对手或上下游名单。没有合格来源时设为 `null`。
14. 内部行业解读只能陈述精确排名、企业数量、行业平均值和风险比率，并按“事实综合 → 可能的业务含义 → 拜访核验方向”组织。允许写“在{D.industry_scope_display}统计范围内排名第 N”，禁止改写为“行业领先”“头部企业”“龙头企业”“竞争优势明显”或其他市场地位结论。外部行业背景只能作为独立定性段落或访谈方向，不得与内部量化值混写成统一口径。
15. 仅由外部行业背景触发章节时，`D.industry_positioning` 和 `D.industry_external_context` 必须非空，`industry_climate_rows`、`industry_benchmark_rows`、`industry_risk_rows` 保持空数组，不显示对应量化小节；不得为满足旧验收条件生成空表或模拟值。
16. `EVIDENCE.industry_*` 逐项登记实际进入表格和文案的 `internal:B/IND/REL` 字段、采用的年度与地区行业范围；`EVIDENCE.industry_scope_display` 同时登记中文地区名、中文行业名的内部来源字段和用于一致性核验的代码字段；`EVIDENCE.industry_external_context` 只登记实际使用的 `external:Wn`。未显示的排名、平均值、比率、空结果、失败状态和未采用网页不得作为行业结论证据。

#### 核心经营数据生成规则

1. “核心经营数据”只展示明确报告期的上市公司财务事实及同年度员工信息，不再展示分支机构、网站、ICP备案、近期舆情、融资、荣誉、客户数量、客户渗透率或标杆客户。不得使用舆情、行业均值、注册资本、融资金额或模型知识估算营业收入、利润、资产负债、现金流或客户数量。
2. 从 `FIN_LISTED.mainfinadata.data.mainfinadataInfo[]` 中筛选 `reportDate` 严格匹配 `YYYY-12-31`、`reportTimeType` 明确为“年度报告”、`reportDate` 不晚于数据日期，且 `operateIncome/totalOperateReVe/parentNetProfit/cutParentNetProfit/netOperateCashFlow/sumAsset/sumLiab/roeWeighted` 至少一个非空的记录。按 `reportDate` 从新到旧选择最新年度；不得把一季度、半年度、三季度或单季度记录当作年度数据。
3. 同一 `reportDate` 存在多条记录时，先计算上述八个核心字段的非空数量并选择数量最多者；数量相同则优先 `startDate` 为同年 `01-01` 的记录，再选择有效 `latestNoticeDate` 最新者。若仍有多条且核心字段值相互冲突，不自行猜测，冲突字段不展示并在 `operations_boundary` 说明同年度公开记录存在口径差异。
4. `operateIncome` 非空时作为营业收入；仅当其为空时使用 `totalOperateReVe`，不得同时展示为两个收入指标。其余指标按“归属于母公司股东的净利润 → 扣除非经常性损益后归属于母公司股东的净利润 → 经营活动产生的现金流量净额 → 资产总计 → 总负债 → 加权平均净资产收益率 → 营业收入同比 → 归母净利润同比”的顺序整理。
5. 选定年度记录的 `sumAsset` 或 `sumLiab` 为空时，才读取同一 `reportDate` 的 `FIN_LISTED.rgbalance.data.rgbalanceInfo[]`。存在 `combineTypeCode="001"` 或 `combineType="合并"` 的记录时只使用合并记录；没有明确合并口径时不使用资产负债补充记录。合并记录重复时同样按目标字段非空数量、有效 `latestNoticeDate` 从新到旧选择；不得使用 `combineType="母公司"` 或 `combineTypeCode="002"` 补充合并经营数据。
6. 金额与币种严格使用同一条记录的原值；整数部分只增加千分位，不换算为万元、亿元，不舍入或补零。`currency` 为已知代码时显示中文币种名称，未知代码保留原值；没有币种时不得自行补写“元”。`roeWeighted/iRobrIncreaseRate/toiYoyRatio/dpNpYoyRatio` 为有效数字时保留原值并直接追加 `%`，不得乘以 100。
7. `FIN_KEY.coreLndicatorInfo[]` 只选择 `reportYear` 与选定年度报告年份完全一致的记录。仅当 `empNumDis` 明确为 `"1"`、`empNum` 为非负整数且不是 `N/A` 时，增加“员工规模”行；`socialSecurityNum` 不等同集团员工数，不进入核心经营数据表。`FIN_KEY` 中的 `busIncome/mainBusIncome/netProfit/totalProfit/totalAss/totalLia/totalOwnEquity/totalTax` 不进入本章节，也不得用于填补 `FIN_LISTED` 空字段，因为该产品只给年份、没有报告期间且金额单位未明确。
8. `D.core_operation_rows[] = {metric, value, period_basis}`。每个非空指标单独成行；`period_basis` 必须写明选定年度报告日期、报告类型和币种，资产负债补充项另写“合并资产负债表”，员工信息写“{reportYear}年度公开员工信息”。`D.has_core_operation_rows` 仅在至少存在一行时设为 `true`。
9. 有表格时，`operations_boundary` 固定说明“以下数据来自{reportDate}年度报告，金额、比率及币种按公开资料原值展示，不同报告期不可直接混同比较。”；存在冲突、字段缺失或使用合并资产负债补充时追加对应事实边界，不使用“接口”“返回”“查询”等技术措辞。
10. 没有符合条件的上市公司年度报告时，`D.has_core_operation_rows=false`，不展示空表、不使用 `P0130025` 金额，也不生成 `operations_interpretation`。`operations_boundary` 固定为：“现有资料暂不包含可核验的营业收入、利润、资产负债及现金流数据，本章节不作量化判断。建议拜访时结合企业近三年财务报表、纳税申报资料及主要客户、订单结构进一步了解。”只有公开事实明确表明企业为非上市公司时，才允许在句首增加“该企业为非上市公司”；不得仅因财务数据为空推断其未上市。
11. 有表格时才生成 `operations_interpretation`，按“所选年度核心指标事实 → 可见同比或现金流信号 → 拜访核验方向”组织。只解释表格已展示数据，不计算利润率、资产负债率、增长额或其他派生指标，不作经营健康、偿债能力、行业地位、风险等级或授信判断。
12. `EVIDENCE.core_operation_rows` 逐行登记选定记录、选取规则、实际字段、报告日期、报告类型、币种和必要的合并口径；`EVIDENCE.operations_boundary` 登记年度报告选择结果或无有效年度报告状态；`EVIDENCE.operations_interpretation` 只登记已展示表格行。样例企业实测数据不得写入 Skill、证据模板或固定文案。

#### 企业风险与合规证据生成规则

1. 先构建 `D.risk_evidence_groups`，固定顺序为“主体与行政合规 → 司法与执行 → 股权及资产权利负担 → 税务与许可合规 → 财务经营关注 → 近期公开事件”。每组只保存 `{status, facts[]}`；每条 `fact` 至少包含 `subject`、`fact_type`、`detail`、`period_or_date`、`current_status`、`source_scope` 和 `detail_available`，缺失项保持空值，不得猜测。`status` 只允许：
   - `hit`：存在可进入风险表的明确事实；
   - `context`：只有纳税评级、有效许可等合规背景，或只有财务资料边界；
   - `empty`：对应工具成功且该组明确无可展示记录；
   - `unavailable`：工具失败、未调用或无法确认主体。
2. 主体与行政合规使用 `B.basicList[0].orgStatus`、`exceptionList`、`illegalList`、`caseInfoList`、`liquidations`，以及许可、资质中明确写明撤销、吊销、注销、暂停、失效、过期、异常或整改的记录。主体状态正常、列表为空或许可明确有效只作为背景，不生成“合规良好”“无行政风险”等结论。
3. 司法与执行以 `OV_RISK.list[0]` 的近两年统计为数量事实，以 `B.dishonestList`、`executedList` 等补充明细；`caseInfoList` 归入主体与行政合规，`judicialAidList` 归入股权及资产权利负担，不得重复归类。统计与明细必须分别注明“近两年公开统计”和“工商深度公开记录”，不得相加、互相覆盖或强行解释差异。只有明细主体字段与规范企业全称一致，或记录明确载明企业在案件中的身份时，才可作为目标企业事实；人员、股东或关联主体记录必须单列主体范围，不得写成企业自身失信或被执行。
4. 股权及资产权利负担使用 `B.sharFrozList`、`sharePledgList`、`mortReg`、mortgage、judicial aid 和 `LAND.tddy.records[]`。股东质押记录写成“股东股权质押”，不得写成企业自身债务；股权冻结、司法协助和同一案号、金额、日期对应的记录可能指向同一事项，只分别说明各列表列示数量，不得相加为风险总数。没有明确注销、解除或当前状态时，只写登记日期、期限和公开状态，不得写“当前有效”“已经解除”。
5. 税务与许可合规取 `OV_TAX.list[]` 中年份最大的有效 `year/rating`，并整理 `LIC.detailList[]` 中明确状态和有效期。纳税评级只作为年度合规背景，不翻译为信用优劣；许可分页未完整获取时，总量可以使用 `detailListMeta.totalCount`，但状态结论只能针对实际展示的代表记录，不得概括全部许可。`HON.status` 为未解释代码时不得自行翻译，只有 `revokeDate` 或明确中文状态可以形成事实。
6. 财务经营关注只使用“核心经营数据生成规则”选出的同一年度报告。只有表格中直接展示的负数净利润、负数经营活动现金流量净额或明确为负的营业收入/归母净利润同比可以形成关注事实；不得计算新比率、比较不同报告期或推导偿债能力、流动性紧张和授信风险。无有效年度报告或企业为非上市公司时只写入 `D.risk_information_boundary`，不得作为风险命中或风险表行。
7. 近期公开事件可使用通过目标企业事件主体过滤、且标题或详情明确描述处罚、诉讼、执行、违约、事故、整改或其他负面事项的内部 `OP` 记录，以及 `WEB.sources` 中 `scope="public_event"` 的合格外部证据。外部监管、法院网页只有一级原始公告可单独采用；三级媒体必须满足追溯或交叉验证规则。外部事件只进入 `public_event_clues`，不得回填主体与行政合规、司法与执行等内部结构化组的数量或状态。接口情感标签只能辅助筛选，不能代替正文事实；纯行情、概念股、行业评论、企业顺带提及和无详情的标题不得形成风险结论。
8. 六组整理完成后，只把 `status=hit` 的组转为 `D.risks[]`，最多六行且顺序固定；同一组内优先展示时间较近、状态较明确、金额或案号信息较完整的事实，最多列举三项代表事实，其余仅保留原始数量和范围。表格使用“关注维度｜关键事实｜范围与待核实事项”，不生成风险等级。
9. `D.risk_compliance_context` 确定性汇总最新内部纳税评级和实际展示许可记录的明确状态；没有有效事实时为 `null`。`D.risk_information_boundary` 确定性说明统计无明细、历史记录状态不明、非上市公司财务资料不足、外部事件只作线索或不同来源范围不可合并；不得出现产品码、工具名、原始状态代码或“接口返回”等技术语言。
10. 近两年统计中的明确数字 `0` 仍只进入 `D.risk_zero_dimensions`；空字符串、`null`、非数字、失败或未调用不得当作零。`D.has_risks` 仅在 `D.risks` 至少一行时设为 `true`，合规背景和信息边界本身不触发风险章节。
11. `D.risk_interpretation` 只接收已归一化的 `D.risk_evidence_groups`、`D.risks`、`D.risk_compliance_context` 和 `D.risk_information_boundary`，不得读取其他原始响应。按“事实综合 → 可能的业务含义 → 拜访核验方向”生成，不重复整表，不使用“高风险”“中风险”“低风险”，不预测损失。
12. `EVIDENCE.risk_*` 逐组、逐行登记实际使用的 `internal:<字段>` 或 `external:Wn`、主体、日期、状态和范围。外部事件事实在正文附对应 `[外部：Wn]`；统计与明细不一致、同一事项可能跨列表重复、外部与内部口径不同或缺少当前状态时，必须在证据和可见范围说明中保留，不得由大模型消解。

### 4. 构建内部主体事实白名单与确定性回退

先把原固定简述规则允许使用的内部事实整理到 `D.company_overview_facts`。该对象只保存已经通过主体匹配、空值过滤和无损格式化的事实，不保存完整原始响应：

- `identity`：规范企业全称和内部登记状态为必选；曾用名、成立时间、所在省份、企业规模、内部工商行业按有效值保存。
- `capital`：注册资本和实缴资本按内部原值及币种保存；不生成资本实力判断。
- `market_events`：只保存下方规则选中的上市、退市或融资事件。
- `business_signals`：只保存下方规则选中的招投标和知识产权事实，不把数量改写为能力结论。
- `tax_context`：只保存最新有效年度纳税评级，不翻译为信用高低。
- `risk_hits`：只保存近两年明确大于零的风险数量及资料边界，不保存零值、空值和失败状态。

同时按原固定公式生成 `D.company_overview_fallback`，只在 `D.core_internal_baseline` 生成失败或验收失败时使用。先分别构建以下五个片段，删除空片段后按固定顺序直接连接：

```text
D.company_overview_fallback =
    基本信息片段
    + 上市/融资片段
    + 招投标/知识产权片段
    + 纳税片段
    + 近两年风险片段
```

如果所有简介扩展维度均失败或为空，基本信息片段仍必须使用 `B.basicList[0].orgName` 生成“{企业名称}。”，确保回退文本至少输出“{企业名称}。”。每个非空片段以句号结束，不重复添加句号。

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

`EVIDENCE.company_overview_facts` 逐项列出实际进入白名单的字段，`EVIDENCE.company_overview_fallback` 逐项列出实际进入回退文本的字段。不得登记空结果、失败状态或未展示字段来为简述背书。财务片段固定不构建。

#### 4.6 AI 生成内部主体描述

1. 仅把 `D.company_overview_facts.identity`、`capital` 和必要的 `market_events` 交给大模型生成 `D.core_internal_baseline`，不得把 `business_signals`、`tax_context`、`risk_hits`、`WEB`、未筛选的原始响应或其他企业样例同时作为输入；业务信号进入 `D.core_capability`，税务与风险分别进入合规和风险分项，避免重复。通常生成 1 至 2 句、80 至 150 个汉字；证据稀少时可以缩短，不得凑字数。
2. 首句必须以规范企业全称为主语。除企业全称和登记状态外，从曾用名、成立时间、所在省份、内部工商行业、企业规模、资本和对当前身份有影响的资本市场事件中选择 2 至 4 项最有区分度的事实；不得为完整而列出所有字段。
3. 优先写成“企业是谁、处于何种登记或资本状态、具有哪些可见业务信号”的自然表达。内部行业只能写“内部工商行业归属于”“登记行业为”或同等审慎表述；仅有行业字段而无经营范围、产品或项目证据时，不得写“主营”“专注于”或“核心业务是”。
4. AI 只能调整取舍、语序、连接词和句式。企业名称、状态、日期、金额、比例、数量和币种必须与白名单原值一致；不得计算、换算、补零、舍入、改写单位或把空值写成“无”。不得加入“领先、龙头、优质、实力雄厚、经营稳健、资本实力强”等评价。
5. `D.core_internal_baseline` 必须通过逐事实反查：包含规范企业全称，没有 `[外部：` 标记，每项事实均存在于允许输入的 `identity/capital/market_events`，数值和日期完全一致，且没有把行业、规模、资本或资本市场事件升级为推断结论。验收失败时只重写一次；仍失败则直接使用 `D.company_overview_fallback`，不得修改白名单或调用外部搜索补齐。
6. `EVIDENCE.core_internal_baseline` 按句登记实际采用的白名单字段；使用回退时同时登记 `internal:D.company_overview_fallback` 和回退原因，但不在报告中显示技术原因。

#### 4.7 生成综合核心观点

`D.core_internal_baseline` 作为内部主体底座，最终报告的“核心观点”展示 `D.core_viewpoint`。先分别生成以下受约束分项，再删除空的条件分项并按固定顺序组织；不得让模型脱离分项和证据自由撰写企业故事：

```text
D.core_viewpoint =
    AI 内部主体描述
    + 核心资产与能力信号
    + 企业官网或正规外部描述（可选）
    + 关键发展转折（可选）
    + 近期企业动作（可选）
    + 当前经营阶段与证据边界
    + 主要风险与约束（可选）
    + 拜访核验重点
```

1. **内部主体定位**：直接使用已经验收的 `D.core_internal_baseline`，不得再次改写其中数值、日期或标准字段。不得用外部网页补充或修正名称、行业、资本、地址、人员姓名与当前职务或股权状态。
2. **核心资产与能力信号**：生成 `D.core_capability`，从内部经营范围、品牌与代表商标、有效许可、荣誉资质、知识产权、招投标、土地或重大项目事实中选择 1 至 2 项最能解释企业业务基础的信号。数量只能作为事实，不得自动改写为竞争优势、市场地位或经营实力；没有可用能力信号时，以自然语言说明现有资料主要确认了主体和业务范围，不为满足篇幅补造亮点。
3. **企业官网自述**：有 `scope="company_description"` 的目标企业官网稳定介绍页时，可以生成 `D.core_company_self_description`，最多一句。必须写“企业官网将其业务定位描述为……”或同等明确归因，只概括页面正文直接描述的产品服务范围、技术方向、品牌定位或项目角色；不得采用宣传排名、荣誉称号、客户数量、产能、营收、市场份额、覆盖范围和未来目标，不得把官网自述与内部事实混写成独立核验结论。无发布日期的稳定介绍页必须显示访问日期。
4. **正规外部描述**：有政府、监管机构、交易所、正规行业协会、高校、权威研究机构或合格主流媒体对目标企业的直接描述时，可以生成 `D.core_external_description`，最多一句。必须写明“{机构名称}在{公告/报道/研究材料}中将企业描述为……”或同等归因，只保留与业务定位、产品服务、技术或项目角色相关的内容；三级媒体仍须满足追溯或交叉验证规则。外部来源中的“领先、龙头、第一、唯一、核心企业”等评价标签一律不进入正文，即使带归因也不采用。
5. 官网自述与外部描述内容重复时优先保留等级更高、表述更具体的来源；二者均有独立信息时最多各保留一句。每句附 `[外部：Wn]`，不得借这些描述补填内部行业、经营范围、资质、荣誉、人员姓名与当前职务、股权、财务或风险标准字段。
6. **关键发展转折**：仅在存在对当前判断有实质影响的并购、重整、上市退市、重大股权变化、管理机制调整或重大项目节点时生成 `D.core_turning_point`。内部标准状态仍以内部字段为准；外部只采用政府、法院、监管机构、交易所或企业官网原始页面，并用“发布/公告/披露了某项事件”描述。外部任职或资本变动公告不得改写为已经更新的当前标准字段；历史节点最多保留两个，禁止写成企业大事记。
7. **近期企业动作**：生成 `D.core_external_context`，从近 12 个月合格外部企业动态中最多选择两项真正改变访前判断的产品、项目、产能建设、品牌、渠道、组织或合作动作。企业官网内容必须写“企业官网披露”；只描述动作和公开安排，不把宣传目标写成既成成效。禁止采用外部营收、利润、资产负债、现金流、员工、客户、终端、门店、产销量、市场份额、融资金额等经营数值，也不得采用一般行业政策、市场规模、增长率或竞争格局填充本分项。
8. **当前经营阶段与证据边界**：生成 `D.core_operating_stage`。只有内部年度财务、内部经营记录或其他直接内部事实能够支持时，才可使用“增长、恢复、扩张、收缩、扭亏”等阶段判断，并同时写明报告期；只有外部动作时，写成“企业正在推进某项动作，实际经营成效仍需结合财务、产销、订单或回款资料核实”，不得直接写“进入高速增长期”“处于重整后爬坡期”等结论。
9. **主要风险与约束**：仅从 `D.risk_evidence_groups` 中 `status=hit` 的内部归一化事实和合格 `public_event` 外部线索生成 `D.core_risk_constraint`，优先选择最影响当前访谈的 1 至 2 项，保留主体、时间、数量、当前状态和资料范围。区分历史遗留事项与近 12 个月新增事件；无法确认是否解除、履行或结案时明确写“当前状态待核实”。不得使用“问题突出”“风险较高”“债务沉重”等评级式概括。无命中事实时本分项保持 `null`，不得生成安全性结论。
10. **拜访核验重点**：生成 `D.core_visit_focus`，用一句话提出 2 至 3 项核验重点，优先覆盖近期动作的实际成效、交易或协同关系边界、经营数据、历史事项处置和当前资金安排。只写“建议了解”“建议核实”“可重点询问”，不得写综合金融服务空间、授信建议、产品方案或合作结论。
11. `D.core_viewpoint` 通常控制在 250 至 420 个汉字、5 至 8 句；证据极少时允许缩短，但不得用宣传语、一般行业背景或无证据判断凑字数。内部主体定位和能力信号在前，可归因描述、转折和近期动作居中，经营边界、风险约束和核验重点在后；同一句连续列举的数量不超过 3 个。
12. 每个外部事实在事实句末附 `[外部：Wn]`，同一事实有多条交叉验证来源时列出全部 ID。`D.source_attributions.core.external_source_ids[]` 按正文首次引用顺序去重；没有采用外部事实时保持空数组，不生成外部来源行。网络不可用或无合格资料时，仍用内部事实生成完整核心观点，并在经营阶段边界中自然说明近期外部资料未形成有效补充。
13. 核心观点负责形成“企业身份与能力 → 可归因外部观察 → 当前变化 → 经营和风险边界 → 拜访重点”的综合判断；执行摘要负责分别展开核心价值、机会、风险和拜访建议。两者可以引用同一证据，但不得整句重复。不得在核心观点中堆砌全部基本信息、风险数量、知识产权数量或执行摘要四项。
14. `EVIDENCE.core_capability/core_company_self_description/core_external_description/core_turning_point/core_external_context/core_operating_stage/core_risk_constraint/core_visit_focus` 分别登记实际使用的最小内部字段或 `external:Wn`；`EVIDENCE.core_viewpoint` 按句登记对应分项证据。无法绑定证据的句子必须删除或改为待核实事项。

### 5. 生成大模型派生文案

先完成确定性字段整理，单独让大模型从 `D.company_overview_facts` 生成并验收 `D.core_internal_baseline`，再让大模型基于已经归一化的核心观点分项和其他证据一次性生成 `D.core_viewpoint` 及其余 `D` 文案，最后执行语义验收。不得直接把原始响应交给排版阶段临场概括。`D.company_overview_facts`、`D.company_overview_fallback`、`D.tangible_asset_rows`、`D.core_operation_rows` 和事实表格不属于模型派生分析；`D.core_internal_baseline`、`D.core_viewpoint`、执行摘要、各画像解读、需求核验说明和风险综合提示属于受证据约束的总结分析。除各分节统一使用“信息解读：”作为业务标签外，不添加模型来源标识。

生成要求：

1. `core_internal_baseline`：严格按“AI 生成内部主体描述”规则，只使用 `D.company_overview_facts` 生成自然内部描述；验收失败时使用 `D.company_overview_fallback`。
2. `core_viewpoint`：严格按“综合核心观点生成规则”形成企业身份、能力信号、企业官网或正规外部描述、关键转折、近期动作、经营阶段边界、风险约束和拜访重点的连贯叙事；条件分项没有证据时直接省略，不得让模型补齐。引用外部事实时附来源 ID。
3. `core_company_self_description` 和 `core_external_description`：仅在存在合格 `company_description` 来源时生成，逐句保留官网或外部机构归因，过滤宣传排名、经营数值、未来目标和标准字段，引用外部事实时附来源 ID。
4. `value_judgment`：60 至 120 个汉字。按“企业是什么、有哪些可见能力信号、为什么值得本次拜访进一步了解”的顺序，归纳内部登记、行业、许可、资质、知识产权及内部或合格外部公开经营线索；不得退化为数量清单，同一句中连续列举的数量不超过 3 个，不使用市场地位、经营质量或授信判断。引用外部事实时附来源 ID。
5. `opportunities`：60 至 150 个汉字。写 1 至 3 条“访谈机会线索”；有目标企业自身内部事件或合格外部动态时说明事件、归因和待了解事项，外部事实附来源 ID；没有合格事件时明确写“本次未形成可直接核验的近期机会事件”，再从内部业务范围、有效许可或荣誉中提出核验方向。
6. `risk_summary`：50 至 140 个汉字。只使用 `D.risk_evidence_groups` 中 `status=hit` 的事实，概括最需要关注的 1 至 3 个维度、原始数量、主体范围和信息限制，不重复列举零值维度；无命中时写“公开资料中暂无可供展示的相关记录”，同时声明不等同于不存在相关事项。
7. `visit_advice`：60 至 150 个汉字。形成一个沟通切入点和 2 至 3 个核验重点，只写“建议了解”“建议核实”“可重点询问”；引用外部事实时附来源 ID。
8. 每个已显示画像小节的 `*_interpretation`：通常 50 至 140 个汉字，按“事实综合 → 可能的业务含义 → 拜访核验方向”组织。`people_interpretation` 只能使用内部人员事实和表中已引用的合格人物背景；不得把职业履历升级为决策权判断。法定代表人兜底或全部背景缺失场景允许缩短至 30 个汉字，但必须说明公开资料未形成可核验的职业背景补充，且决策权限和具体分工仍待拜访确认。证据不足时使用“可能表明”“可以作为”“提示关注”“值得进一步了解”等审慎措辞，不得留空。
9. `tangible_asset_rows`、`operations_boundary` 和 `core_operation_rows`：分别按“有形资产生成规则”和“核心经营数据生成规则”确定性生成，不进入大模型重写；`assets_interpretation` 只能读取已展示资产行，只有 `D.has_core_operation_rows=true` 时才生成 `operations_interpretation`。
10. `industry_climate_interpretation` 和 `industry_benchmark_interpretation`：各 50 至 140 个汉字，只解释已展示的行业统计、精确排名和范围，指出可用于访谈的业务含义；不得把企业数变化解释为市场增长，不得把排名改写为市场地位。
11. `industry_risk_interpretation`：仅在 `D.has_industry_risk=true` 时生成，50 至 100 个汉字，说明行业风险比率的年份、地区行业范围和拜访核验方向，不生成风险评级或企业自身风险结论。
12. `risk_interpretation`：80 至 180 个汉字，只使用归一化后的六组企业风险与合规证据，按“事实综合 → 可能的业务含义 → 拜访核验方向”概括目标企业命中事实、主体范围、时点限制和核验重点；不得混入行业风险比率，不得把纳税评级、有效许可、抵押、质押或资料缺失直接改写为风险结论。
13. `visit_questions`：优先生成 4 至 6 条，问题之间不得同义重复；`basis` 必须引用报告所列内部事实、附来源 ID 的外部事实或明确的信息缺口，`question` 不得预设答案。产业链信息不足时至少包含一条客户结构、供应商结构、采购或销售关系核验问题。

质量要求：

- 内部事实白名单、AI 内部主体描述、综合核心观点、执行摘要和分节信息解读承担不同职责。大模型不得更改 `D.company_overview_facts` 或 `D.company_overview_fallback`，只能按规则从白名单选择和组织事实；同一事实可在其他文案中再次提及，但必须改变信息层级和表达目的。
- 所有总结分析必须同时包含事实依据、审慎的业务含义和可执行的拜访核验方向；事实不足时把判断降级为假设或问题。
- 文案必须具体到目标企业和报告所列事实，禁止套用“发展前景广阔”“综合实力较强”“合作空间巨大”等通用评价。
- 除行业分析明确提供的精确排名外，禁止推导市场地位；任何排名均不得扩写成“行业领先”“头部企业”或“龙头企业”。禁止推导实际控制关系、风险等级、偿债能力、资金需求、授信结论或具体产品适配；不得复制思迈特样稿中的市场规模、CAGR、竞争对手、政策判断、强判断、估算值或模拟数据。
- 最终报告文案必须通过业务语言检查，把内部查询状态、接口结果、搜索过程改写为公开信息的事实陈述、信息说明或待核实事项；来源区保留必要的“内部/外部”标签、发布日期、访问日期和链接。
- 生成后逐项核对 `EVIDENCE`。无法找到证据的句子必须删除或改为待核实问题。
- 大模型只重写除 `D.company_overview_facts`、`D.company_overview_fallback`、`D.tangible_asset_rows`、`D.core_operation_rows`、`D.operations_boundary` 和行业事实表格以外的 `D` 文案；`D.core_internal_baseline` 只能使用内部白名单，`D.core_viewpoint` 只能使用已经整理并绑定证据的核心观点分项。不得更改 `B`、`ID`、`OV_*`、`LAND`、`IND`、`REL`、`FIN_*`、`TM` 至 `OP` 原值、`WEB` 来源元数据、查询状态、列表数量、内部事实白名单、确定性回退文本、有形资产表、核心经营数据表、行业表格或条件布尔值。

## 报告输出格式（严格填空骨架 · 模型只填值、不造结构）

> **使用约定**：以下是“内部结构化数据 + 合格外部公开资料”模式的完整报告骨架。沿用参考成品的标题名称，直接省略没有可见证据的条件章节，并按实际可见的大章节连续编号。模型只把占位符替换为统一证据模型中的内部原值、合格 `WEB` 事实或基于这些证据形成的忠实摘要，禁止自行新增结构。
>
> **结构纪律**：
>
> 1. 禁止新增、改名、合并、拆分或调换章节；禁止创造骨架外的小标题。
> 2. 仅允许按骨架中已经写明的 `{{#if ...}}` 条件隐藏整行、整表或整块。完成显隐判断后必须按实际可见顺序连续填写 `D.section_numbers`；只重编号大章节，不改变小节编号。
> 3. 不输出任何未被替换的占位符、条件标签、工具名、字段路径或内部状态。
> 4. 表格某行所有事实字段均为空时删除该行；某条件板块无有效事实时隐藏整块。不得用模型常识、未通过准入的网页或示例值补齐。
> 5. “核心观点”和“执行摘要”在工商深度成功后固定显示；核心观点必须以内部事实白名单约束生成的 `D.core_internal_baseline` 为主体底座，验收失败时使用 `D.company_overview_fallback`，再按受约束分项生成 `D.core_viewpoint`。可以纳入附来源 ID 且明确归因的企业官网自述、正规外部机构描述和合格企业动态，但不得由模型自由补造或让外部资料改写标准字段。每个已显示且包含事实的画像小节必须生成以“信息解读：”引出的总结分析；核心经营数据只有业务提示而没有表格时不生成信息解读。这些文案只能使用报告所列内部事实或附来源 ID 的合格外部事实，不得推导实控人、融资、授信结论或产品适配。
> 6. “产业画像与行业洞察”在 `D.has_industry_insight=true` 时显示并编号为“四”；有效内部行业事实或“内部工商行业已确认 + 合格外部行业背景”均可触发。仅外部背景触发时只显示产业链定位和定性外部背景，不显示量化小节。产业章节显示时需求识别编号为“五”，风险章节显示时编号为“六”；产业画像隐藏时需求识别仍为“四”，风险章节显示时编号为“五”。“与我行合作现状”仍不进入当前骨架。
> 7. “需求识别与拜访核验”只显示“（一）需求线索核验”，把已有事实和数据缺口转成现场问题；不生成银行产品推荐、紧迫度评级或营销方案。
> 8. “风险预警与合规提示”按“主体与行政合规、司法与执行、股权及资产权利负担、税务与许可合规、财务经营关注、近期公开事件”六组整理证据，只展示其中明确命中的企业事实；明确零值维度只放入表后边界说明，最新纳税评级和许可状态只作合规提示，不生成风险等级；风险表后必须生成综合提示。
> 9. `D.company_overview_facts` 或 `D.company_overview_fallback` 验收失败时按确定性规则重新构建；`D.core_internal_baseline` 验收失败时只允许基于同一事实白名单重写一次，仍失败则使用回退文本；`D.core_viewpoint` 验收失败时只基于已经通过证据验收的核心观点分项重新生成，禁止重新搜索或补造事实；其他必填总结字段生成失败时才重写对应大模型派生字段。不得交付缺少核心观点、执行摘要或已显示小节信息解读的报告。
> 10. 每个来源区先输出实际使用的内部维度，再按正文首次引用顺序输出外部来源。外部事实必须带 `[外部：Wn]`，来源区必须能用同一 ID 解析到网站、标题、发布日期、访问日期和原始链接；不得输出未被正文引用的网页。

```markdown
# 企业画像

报告编号：{{META.report_id}}  ｜  生成时间：{{META.generated_at}}  ｜  密级：机密

客户名称：{{B.basicList[0].orgName}}{{#if D.brand_name}}（品牌：{{D.brand_name}}）{{/if}}

## {{D.section_numbers.core}}、核心观点

{{D.core_viewpoint}}

—————————————————数据来源————————————————

内部：水滴征信 MCP（{{join D.source_attributions.core.internal_dimensions|separator="、"}}）｜数据日期：{{META.generated_at}}
{{#eachSource WEB.sources|ids=D.source_attributions.core.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{title}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜访问日期：{{accessed_at}}｜链接：{{url}}{{/eachSource}}

## {{D.section_numbers.summary}}、执行摘要

**核心价值判断：** {{D.value_judgment}}

**主要机会：** {{D.opportunities}}

**主要风险：** {{D.risk_summary}}

**拜访建议：** {{D.visit_advice}}

—————————————————数据来源————————————————

{{#if D.source_attributions.summary.internal_dimensions}}内部：水滴征信 MCP（{{join D.source_attributions.summary.internal_dimensions|separator="、"}}）｜数据日期：{{META.generated_at}}{{/if}}
{{#eachSource WEB.sources|ids=D.source_attributions.summary.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{title}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜访问日期：{{accessed_at}}｜链接：{{url}}{{/eachSource}}

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

内部：水滴征信 MCP（{{join D.source_attributions.basic.internal_dimensions|separator="、"}}）｜数据日期：{{META.generated_at}}

{{#if D.person_rows}}
### （二）关键决策人信息

| 姓名 | 职务 | 背景 |
| --- | --- | --- |
{{#each D.person_rows|max=8}}| {{name}} | {{position}} | {{background}} |{{/each}}

**信息解读：** {{D.people_interpretation}}

—————————————————数据来源————————————————

内部：水滴征信 MCP（{{join D.source_attributions.people.internal_dimensions|separator="、"}}）｜数据日期：{{META.generated_at}}
{{#eachSource WEB.sources|ids=D.source_attributions.people.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{title}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜访问日期：{{accessed_at}}｜链接：{{url}}{{/eachSource}}
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

内部：水滴征信 MCP（{{join D.source_attributions.equity.internal_dimensions|separator="、"}}）｜数据日期：{{META.generated_at}}
{{/if}}

{{#if D.has_assets}}
### （四）企业资产状况

{{#if D.tangible_asset_rows}}**有形资产：**

| 资产类型 | 可核验事实 | 权利与口径边界 |
| --- | --- | --- |
{{#each D.tangible_asset_rows|max=6}}| **{{asset_type}}** | {{fact}} | {{boundary}} |{{/each}}
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

—————————————————数据来源————————————————

{{#if D.source_attributions.assets.internal_dimensions}}内部：水滴征信 MCP（{{join D.source_attributions.assets.internal_dimensions|separator="、"}}）｜数据日期：{{META.generated_at}}{{/if}}
{{#eachSource WEB.sources|ids=D.source_attributions.assets.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{title}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜访问日期：{{accessed_at}}｜链接：{{url}}{{/eachSource}}
{{/if}}

{{#if D.has_core_operations}}
### （五）核心经营数据

信息说明：{{D.operations_boundary}}

{{#if D.has_core_operation_rows}}
| 指标 | 本次数据 | 数据口径 |
| --- | --- | --- |
{{#each D.core_operation_rows}}| **{{metric}}** | {{value}} | {{period_basis}} |{{/each}}

**信息解读：** {{D.operations_interpretation}}

—————————————————数据来源————————————————

内部：水滴征信 MCP（{{join D.source_attributions.operations.internal_dimensions|separator="、"}}）｜数据日期：{{META.generated_at}}
{{/if}}
{{/if}}

{{#if D.has_industry_insight}}
## {{D.section_numbers.industry}}、产业画像与行业洞察

### （一）产业链定位

{{D.industry_positioning}}

{{#if D.industry_external_context}}行业外部背景：{{D.industry_external_context}}{{/if}}

{{#if D.industry_climate_rows}}
### （二）行业景气度

| 观察维度 | 公开统计 | 时间与范围 |
| --- | --- | --- |
{{#each D.industry_climate_rows}}| **{{topic}}** | {{fact}} | {{period_scope}} |{{/each}}

**信息解读：** {{D.industry_climate_interpretation}}
{{/if}}

{{#if D.industry_benchmark_rows}}
### （三）行业对标

| 对标维度 | 企业行业位置 | 行业参考 | 时间与范围 |
| --- | --- | --- | --- |
{{#each D.industry_benchmark_rows}}| **{{topic}}** | {{company_position}} | {{industry_reference}} | {{period_scope}} |{{/each}}

**信息解读：** {{D.industry_benchmark_interpretation}}
{{/if}}

{{#if D.has_industry_risk}}
### （四）行业风险

| 风险信号 | 公开统计 | 拜访核验方向 |
| --- | --- | --- |
{{#each D.industry_risk_rows}}| **{{signal}}** | {{fact}} | {{verification}} |{{/each}}

**信息解读：** {{D.industry_risk_interpretation}}
{{/if}}

—————————————————数据来源————————————————

{{#if D.source_attributions.industry.internal_dimensions}}内部：水滴征信 MCP（{{join D.source_attributions.industry.internal_dimensions|separator="、"}}）｜数据日期：{{META.generated_at}}{{/if}}
{{#eachSource WEB.sources|ids=D.source_attributions.industry.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{title}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜访问日期：{{accessed_at}}｜链接：{{url}}{{/eachSource}}
{{/if}}

## {{D.section_numbers.needs}}、需求识别与拜访核验

### （一）需求线索核验

**信息解读：** 以下核验主题根据报告所列事实和信息缺口整理，用于帮助业务人员准备现场问题，不构成产品建议。

| 核验主题 | 已知依据与现场问题 |
| --- | --- |
{{#each D.visit_questions}}| **{{topic}}** | {{basis}}；建议现场核实：{{question}} |{{/each}}

—————————————————数据来源————————————————

{{#if D.source_attributions.needs.internal_dimensions}}内部：水滴征信 MCP（{{join D.source_attributions.needs.internal_dimensions|separator="、"}}）｜数据日期：{{META.generated_at}}{{/if}}
{{#eachSource WEB.sources|ids=D.source_attributions.needs.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{title}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜访问日期：{{accessed_at}}｜链接：{{url}}{{/eachSource}}

{{#if D.has_risks}}
## {{D.section_numbers.risk}}、风险预警与合规提示

| 关注维度 | 关键事实 | 范围与待核实事项 |
| --- | --- | --- |
{{#each D.risks}}| **{{topic}}** | {{detail}} | {{scope}} |{{/each}}

**信息解读：** {{D.risk_interpretation}}

{{#if D.risk_compliance_context}}合规提示：{{D.risk_compliance_context}}{{/if}}

{{#if D.risk_zero_dimensions}}信息说明：近两年公开统计中以下事项记录数为 0：{{D.risk_zero_dimensions}}；仅代表该公开统计范围，不等同于不存在相关事项。{{/if}}

{{#if D.risk_information_boundary}}资料范围：{{D.risk_information_boundary}}{{/if}}

—————————————————数据来源————————————————

{{#if D.source_attributions.risk.internal_dimensions}}内部：水滴征信 MCP（{{join D.source_attributions.risk.internal_dimensions|separator="、"}}）｜数据日期：{{META.generated_at}}{{/if}}
{{#eachSource WEB.sources|ids=D.source_attributions.risk.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{title}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜访问日期：{{accessed_at}}｜链接：{{url}}{{/eachSource}}
{{/if}}

## 报告使用说明

- 报告目的：本报告仅为对公客户经理拜访前准备和沟通参考使用，不作为授信审批的最终依据。
- 信息真实性：报告依据生成时点的公开信息形成；资料缺失或尚待补充不等同于不存在相关事实，建议在拜访中核实关键信息。
- 数据时效性：报告生成后如发生重大变化，建议重新生成报告。
- 保密义务：本报告涉及企业信息，接收方应按所在机构制度妥善保管，未经授权不得对外泄露。
```

### 标题白名单

最终报告只能出现骨架中实际存在的标题，标题名称必须逐字使用，禁止同义替换；大章节的中文数字前缀取自 `D.section_numbers`：`核心观点`、`执行摘要`、`客户全景画像`、`（一）企业基本信息`、`（二）关键决策人信息`、`（三）股权结构与关联关系`、`（四）企业资产状况`、`（五）核心经营数据`、`产业画像与行业洞察`、`（一）产业链定位`、`（二）行业景气度`、`（三）行业对标`、`（四）行业风险`、`需求识别与拜访核验`、`（一）需求线索核验`、`风险预警与合规提示`、`报告使用说明`。

## 文档生成

默认 `--format pdf`。先完成统一证据模型、`D` 派生文案、`EVIDENCE` 映射和语义验收，再形成完整 Markdown，最后排版为 PDF。

PDF 是唯一版式验收基准。优先沿用当前环境中最近一次已验收成功的生成路径；没有既有路径时优先直接生成 PDF，直接生成不可用时才使用 DOCX 中转。同一任务中不得因分页不理想在多个渲染器之间反复切换。不同格式必须复用同一证据模型、派生文案和条件删除结果。

### 固定版式

- 页面：Letter，215.9 × 279.4 mm；上、下页边距 20 mm，左、右页边距 25 mm。
- 正文：宋体或可用的等价中文宋体，10.5 pt，固定行高 15 pt；表格正文 9 pt，固定行高 12 pt。不得使用渲染器默认行高或单倍行距。
- 标题：黑体或等价中文黑体；主标题 18 pt 黑色居中，一级标题 14 pt、二级标题 12 pt，标题蓝色 `#4F81BD`。所有 `##` 一级标题段前 12 pt、段后 6 pt；标题位于页首时不额外增加段前空白。
- 元信息：报告编号、生成时间、密级使用 9 pt、固定行高 12 pt 并居中；客户名称使用 12 pt 加粗居中。
- 数据来源：板块末尾加入灰色 `#808080` 居中分隔线。内部行使用“内部：水滴征信 MCP（数据维度）｜数据日期：{generated_at}”；外部行使用“外部：Wn｜网站名称｜标题｜发布日期：日期或未标明｜访问日期：日期｜链接：URL”。每条来源单独成段，使用 9 pt、固定行高 12 pt、常规字重；长标题和 URL 允许自然换行，不得截断链接或压缩字号。
- 报告使用说明正文：四条说明单独使用宋体或等价中文宋体 9 pt、固定行高 12 pt，常规字重；“报告使用说明”标题仍使用一级标题样式，不随正文缩小。
- 正文段落：核心观点、执行摘要、信息解读、普通说明、人员列表、产业链定位和风险说明统一使用 15 pt 行高。核心观点和信息解读正文首行缩进 2 个汉字；执行摘要四项不缩进。普通正文段落段后 4 pt；PDF 使用段后样式控制间距，不插入空白段落，Markdown 回退在自然段之间保留一个空行。
- 字重：黑色正文必须使用宋体或等价中文宋体的常规字重，禁止整段使用字体名含 `Black`、`Bold`、`Semibold` 的变体。核心观点、执行摘要标签后的内容、信息解读标签后的正文、表格具体数据、股东名、人员名、代表记录、风险说明和报告使用说明均不得加粗。
- 主标题、客户名称、蓝色章节标题和表头行必须加粗。执行摘要的“核心价值判断：”“主要机会：”“主要风险：”“拜访建议：”，各分节“信息解读：”，资产段的“有形资产：”“无形资产：”，以及表格中的业务标签项也必须加粗；只允许这些元素使用粗体。业务标签项包括企业基本信息字段名、资产类型、经营指标、行业观察或对标维度、行业风险信号、需求核验主题和企业风险维度；股东名、人员名及其他实体名称不属于标签项。
- 表格：黑色 0.5 pt 网格线，无表头底色；表头和表格正文统一使用 12 pt 行高。表头必须使用实际中文粗体字形、左对齐并跨页重复；符合上述定义的业务标签项必须使用实际中文粗体字形，其余正文保持常规字重、左对齐，单元格垂直居中。允许表格按可用空间自然分页，较长单元格可跨页拆分。
- 不使用 `KeepTogether`、`keepWithNext`、整块容器或手动分页符保护章节、段落、信息解读、数据来源或表格起始部分；允许这些内容随页面剩余空间自然续页。
- 不因避免断句、孤立标题或来源文字而主动移动整块内容；跨页表格只重复表头，不重复小节标题。
- 不得出现裁切、重叠、乱码或由强制分页造成的异常空白。除最后一页外，若后续仍有连续正文而当前页空白超过可用正文区约三分之一，视为分页失败。
- 页脚不添加页码、公司名或其他参考 DOCX 中不存在的内容。
- 字号不得为压缩页数降至上述规格以下；内容过长时通过自然分页解决。
- 内容不强制压缩到单页，篇幅随有效数据自然分页。

表格列宽按可用正文宽度 165.9 mm 固定分配：

企业基本信息 35 / 130.9；关键决策人信息 27 / 38 / 100.9；股东 84 / 32 / 49.9；有形资产 30 / 80 / 55.9；无形资产 34 / 28 / 103.9；核心经营数据 36 / 74 / 55.9；行业景气度 38 / 58 / 69.9；行业对标 34 / 38 / 42 / 51.9；行业风险 38 / 55 / 72.9；需求线索核验 42 / 123.9；风险预警 38 / 55 / 72.9。单位均为 mm。

### 中文字体与加粗渲染（强制）

Markdown 中的 `**文本**` 只是语义标记，不代表 PDF 已经使用粗体。排版前必须解析实际字体文件并注册一套彼此不同的中文常规字形和中文粗体字形；不得把同一个 Regular 字形同时注册为 normal 和 bold，也不得依赖 PDF 阅读器合成粗体、描边、重复绘制或加大字号模拟粗体。

- macOS 存在 `/System/Library/Fonts/Supplemental/Songti.ttc` 时，ReportLab 首选使用 `STSongti-SC-Regular`（`subfontIndex=6`）作为正文，使用 `STSongti-SC-Bold`（`subfontIndex=1`）作为粗体；章节标题可使用 `/System/Library/Fonts/STHeiti Medium.ttc` 中的 `STHeitiSC-Medium`（`subfontIndex=1`）。
- 其他环境必须选择一套实际包含简体中文 Regular 与 Bold 两个字形的宋体或等价字体，并通过字体元数据确认二者 PostScript 名不同。只有 Regular、没有 Bold，或粗体不覆盖本报告中文字符时，视为中文字体不可用，按 Markdown 回退处理。
- 使用 ReportLab 时必须分别注册字体并建立字体族映射。macOS 的等价实现如下；正文 `ParagraphStyle.fontName` 使用已注册的常规字体名 `SongtiSC`：

```python
songti = "/System/Library/Fonts/Supplemental/Songti.ttc"
pdfmetrics.registerFont(TTFont("SongtiSC", songti, subfontIndex=6))
pdfmetrics.registerFont(TTFont("SongtiSC-Bold", songti, subfontIndex=1))
pdfmetrics.registerFontFamily(
    "SongtiSC",
    normal="SongtiSC",
    bold="SongtiSC-Bold",
    italic="SongtiSC",
    boldItalic="SongtiSC-Bold",
)
```

- 行内标签不得把带 `**` 的 Markdown 原样交给 ReportLab。只对骨架中的静态粗体标签转换为 `<b>标签</b>`，动态正文先执行 XML 转义后再拼接。例如执行摘要必须按 `<b>核心价值判断：</b> {常规正文}` 构造同一个 `Paragraph`；`信息解读：`、`有形资产：`、`无形资产：`同理。标签后的正文必须回到常规字体。
- 表头行必须显式使用已注册的中文粗体字体；若单元格使用 `Paragraph`，使用粗体 Paragraph 样式或 `<b>...</b>`；若使用普通字符串，使用 `TableStyle(("FONTNAME", (0, 0), (-1, 0), "SongtiSC-Bold"))`。表格业务标签单元格也必须显式指定粗体，不能只保留 Markdown 的 `**`。
- 使用 ReportLab 时，除报告使用说明外的非标题正文 `ParagraphStyle` 必须显式设置 `fontSize=10.5, leading=15`；报告使用说明四条正文必须使用独立样式并显式设置 `fontSize=9, leading=12`；表格单元格 `ParagraphStyle` 必须显式设置 `fontSize=9, leading=12`；元信息和数据来源样式必须显式设置 `fontSize=9, leading=12`。使用 DOCX 中转或其他渲染器时设置等效固定行高，不得用“单倍”“多倍”等由渲染器自行解释的相对行距。
- 开始排版正式报告前，先用最终字体配置生成仅含“正文测试”“粗体测试”的临时 PDF。用 PDF 字体元数据确认两段分别映射到常规和粗体 PostScript 字形，并渲染预览确认肉眼可辨；预检失败时不得继续生成正式 PDF。

### 生成与验收

1. 执行语义验收：确认 `company_overview_facts.identity.org_name` 与规范企业全称一致，`company_overview_fallback` 至少包含规范企业全称且没有 `[外部：`；`core_internal_baseline` 非空、首句包含规范企业全称、没有外部事实或来源标记，并且每个事实都存在于白名单且原值一致。确认 `core_viewpoint` 非空、首句使用已经验收的内部主体描述、结构顺序符合综合核心观点规则，并且每个 `[外部：Wn]` 都能解析到合格来源。确认 `core_capability`、`core_operating_stage`、`core_visit_focus`、执行摘要四项和 `basic_interpretation` 非空；`core_company_self_description`、`core_external_description`、`core_turning_point`、`core_external_context`、`core_risk_constraint` 仅在有证据时出现。存在内部主要人员或法定代表人兜底时，`person_rows` 必须非空且只包含内部确认人员，报告必须展示“姓名｜职务｜背景”三列表格；每行 `name/position` 可追溯到内部字段，`background` 不得为空。`has_assets=true` 时必须存在至少一行 `tangible_asset_rows` 或一项无形资产事实；有形资产表每行 `asset_type/fact/boundary` 非空且最多 6 行，没有合格有形资产时不得显示“有形资产”标签。每个已显示且包含事实的画像小节、行业景气、行业对标、行业风险、需求核验和企业风险综合提示均按骨架使用“信息解读：”标签；`has_core_operation_rows=true` 时核心经营数据表非空且 `operations_interpretation` 非空，`has_core_operation_rows=false` 时只显示固定业务提示且 `operations_interpretation=null`；`has_industry_insight=true` 时存在 `industry_positioning`，并满足“至少一类内部行业事实表非空”或“内部工商行业非空且 `industry_external_context` 非空”之一；仅外部背景触发时三个行业量化表保持为空。`has_industry_risk=true` 时存在 `industry_risk_interpretation`；`has_risks=true` 时必须存在至少一行 `risks`、完整的六组 `risk_evidence_groups`、非空 `risk_interpretation`，并且每行都能追溯到 `status=hit` 的同名证据组。确认所有可见大章节编号从“一”开始连续递增，不跳号、不重号。
2. 核对内部证据覆盖：每个非空 `D` 文案字段在 `EVIDENCE` 中至少有一个来源；逐句删除无来源判断。检查金额、比例、日期、数量和币种的底层原值完全一致，展示层只进行了允许的无损格式化、财务比率直接追加 `%` 或行业比率精确百分比展示；有形资产没有计算土地面积、价格或抵押金额合计。检查企业基本信息、行业归属、核心经营数据、员工规模、人员姓名、当前职务和法定代表人身份没有使用 `WEB`，核心经营数据只使用同一内部年度报告和同日期合并资产负债补充、没有混入季度、母公司报表或外部年报；逐行确认 `person_rows` 没有外部新增人员、没有用网页覆盖职务。逐行确认内部有形资产只来自 `LAND` 或 `B` 中明确点名具体有形资产对象的记录，未使用行业、经营范围、注册地址、网站、分支、资本、许可、荣誉、知识产权或招投标。检查状态字段互斥，上市公司主要会计指标、资产负债补充、年度员工补充、土地供应、土地出让、土地抵押和四类行业分析未被合并为单一状态，`REL` 不含 `legalPersonCard`，内部来源行未列入 `empty`、`failed` 或 `not_called` 维度，`D.coverage_summary` 未暴露内部查询步骤。检查产业画像内部量化范围统一使用 `D.industry_scope_display`，且不含 `regionId/nicId` 原值、代码括注或“三级行业C382”式内部编码。
3. 核对外部证据覆盖：检查 `WEB.status`、12 个月窗口、实际查询词和每条 `WEB.sources` 的 `source_id/site_name/source_level/source_type/title/url/accessed_at/supported_fact/applicable_sections/subject_match/corroboration_status` 完整；无发布日期只允许企业官网稳定介绍、管理团队、人物介绍或设施介绍页并显示“未标明”。检查每个 `[外部：Wn]` 都存在于 `WEB.sources`、`EVIDENCE` 和当前章节 `external_source_ids[]`，每个可见外部来源都被正文实际引用，同一章节没有重复来源。对 `scope="person_background"` 逐条确认内部姓名、目标企业关系和正文事实同时匹配；同名歧义、仅搜索摘要、个人或社交页面不得采用，历史任职带时间或“曾任”，冲突职务没有覆盖内部列。对 `scope="tangible_asset"` 逐条确认来源为一级原始页面、规范企业主体、具体资产对象、企业角色和时点同时匹配；企业官网自述带“企业官网披露”，历史资产节点没有升级为当前状态，且没有采用外部面积、价格、价值、产能、设备数量、抵押金额或产权结论。检查三级媒体可追溯到一级来源或至少有两个独立正规来源，企业官网人物背景带“企业官网介绍”，百科、自媒体、社交平台、聚合页、招商宣传、无出处转载、搜索摘要和模型生成内容均未采用。检查冲突来源按规则保留边界，没有由模型合并冲突值。
4. 检查内容边界：不得把 `REL` 主体写成供应商、客户、控股企业或上下游，不得把行业企业数写成市场规模或增长率，不得把精确排名扩写为市场地位；人物背景不得包含出生日期、年龄、家庭关系、住址、联系方式、个人社交账号等非必要个人信息，不得从教育或履历推断决策权限、控制关系或具体分工；有形资产不得出现仅由行业、经营范围、地址、门店、分支、客户项目、订单、产品或宣传推导的资产结论，不得把土地公开记录或设施使用场景写成自有产权、当前持有或账面价值；外部行业背景不得产生企业标准字段、企业财务值、行业排名、行业均值、市场规模、增长率、CAGR、市场份额、竞争对手或上下游名单；核心经营数据不得包含估算值、行业均值倒推值、客户数量、客户渗透率、标杆客户、融资或荣誉；不得出现无直接证据的实控关系、融资、客户数量、风险评级、授信结论或产品推荐；内部舆情和外部事件线索必须通过目标企业事件主体过滤，外部监管或司法事件不得回填内部结构化数量与状态。
5. 检查内容质量：`company_overview_facts` 的字段准入及 `company_overview_fallback` 的片段顺序、条件分支、标点和风险空值规则必须符合确定性规范；`core_internal_baseline` 必须是白名单事实的自然表达，不得变更原值或增加判断。`core_viewpoint` 必须形成“身份与能力 → 可归因外部观察 → 当前变化 → 经营和风险边界 → 拜访重点”的综合叙事，官网与外部描述最多各一句、外部动态不超过两项、历史节点不超过两个；官网与外部描述必须有明确归因，不得包含宣传排名、外部经营数值、未来目标、外部标准字段、一般行业背景或无证据阶段判断。人物背景必须是短句式职业简介，保留来源归因和时间边界；无合格资料时使用固定边界说明，不得留空或补造。有形资产必须使用三列精简表，每行只保留可核验资产事实和必要权利边界，不生成经营背景段、地址段、主要区域/用途概括、土地合计或通用缺口长句。执行摘要和分节总结不得整句复制核心观点，必须包含事实综合、审慎的业务含义和拜访核验方向，不得出现空泛套话；信息缺口写成自然的信息说明或待核实问题。
6. `company_overview_facts`、`company_overview_fallback`、`tangible_asset_rows`、`core_operation_rows`、`operations_boundary` 或内部行业事实表格验收不通过时，只用同一证据模型重新执行对应确定性规则并更新相应 `EVIDENCE`；`core_internal_baseline` 验收不通过时按规则重写一次后回退，`core_viewpoint` 验收不通过时只使用已经验收的核心分项重新生成。外部来源或事实验收不通过时删除对应 `WEB.sources`、正文事实、来源 ID 和章节引用，不重新搜索补造；其他语义验收失败时只重新生成受影响的大模型派生文案。不得重新调用已成功的 MCP 工具，不得让大模型修改内部事实白名单、确定性回退文本、有形资产表、核心经营数据表或内部行业事实表格。仍无足够证据时使用边界型表述，不得隐藏核心观点或执行摘要。
7. 按“报告输出格式（严格填空骨架 · 模型只填值、不造结构）”替换占位符并执行预定义条件。检查报告中不存在未替换占位符、条件标签、内部字段路径、空表或未解析的来源 ID；检查所有内部来源行以“内部：”开头，所有外部来源行以“外部：”开头并包含标题、发布日期、访问日期和链接，再开始排版。
8. 使用当前环境已有的文档或 PDF 能力生成 `output/pdf/{company_name}-企业画像.pdf`。如需 DOCX 中间文件，只把它作为本次临时产物。
9. 逐页渲染或预览最终 PDF，检查中文字体、Letter 页面、页边距、字号、正文 15 pt 行高、报告使用说明正文 9 pt 字号与 12 pt 行高、表格 12 pt 行高、章节和段落间距、首行缩进、表头样式、标签项字重、列宽、来源 URL 自然换行、自然分页、裁切、重叠和异常空白。正文连续多行必须肉眼可见稳定行间留白，不得出现字形上下紧贴；不得通过减小字号、字符缩放或压缩段后间距抵消行高。使用 `pdfplumber` 或等价工具逐字符检查字体元数据：主标题、客户名称、全部蓝色章节标题、每个表头、每处“核心价值判断：”“主要机会：”“主要风险：”“拜访建议：”“信息解读：”“有形资产：”“无形资产：”以及每个可见表格业务标签必须映射到本次注册的实际粗体 PostScript 字形；任一目标仍使用 Regular 即验收失败。相邻的执行摘要内容、信息解读正文、来源正文和表格数据必须映射到常规字形；报告使用说明四条正文必须映射到常规字形且字号为 9 pt；除白名单元素外，黑色正文使用 `Black`、`Bold` 或 `Semibold` 字形也验收失败。字体元数据通过后仍须检查逐页 PNG，确认粗体与正文肉眼可辨，并确认正文与表格行高符合固定值。除最后一页外，后续仍有连续正文但当前页空白超过可用正文区约三分之一时，取消强制分页或整块容器后重新渲染。
10. 验收通过后删除本次临时 JSON、DOCX、预览图片及一次性辅助文件，只保留最终 PDF。
11. 不把生成过程中临时编写的代码、命令、`EVIDENCE`、统一证据 JSON 或未采用的网页候选写入报告或聊天回复。
12. 当前环境无法创建或验收 PDF、中文字体不可用或转换失败时，不循环重试；删除不完整文件并回退完整 Markdown，说明“PDF 生成未完成：{原因}，已回退 Markdown”。

## Markdown 回退

用户指定 `--format md`，或 PDF 流程失败时，直接按“报告输出格式（严格填空骨架 · 模型只填值、不造结构）”输出。Markdown 与 PDF 必须复用同一证据模型中的原值和条件结果。

聊天回复只包含企业规范全称、数据日期、生成格式、最重要的 1 至 3 条资料范围说明，以及 PDF 绝对路径链接或完整 Markdown 正文。

## 输出纪律

1. 使用中文，用户明确要求其他语言时除外。
2. 标题名称逐字使用固定骨架；条件板块隐藏后按实际可见的大章节顺序连续重编号。不得出现跳号、重号、空标题、空表或整排“未披露”。
3. 事实与访谈建议分开。建议使用“建议核实”“可重点了解”，不写“应授信”“建议放款”“可合作”等结论。
4. 内部来源统一写“内部：水滴征信 MCP（业务维度）”，外部来源统一写“外部：Wn｜网站名称｜标题｜发布日期｜访问日期｜链接”；不得写 CISP、产品码、工具名或字段路径。
5. “产业画像与行业洞察”只在存在有效内部行业分析事实，或内部工商行业已确认且存在合格外部行业背景时展示；仅外部触发时不显示量化表格。“与我行合作现状”、授信/存款/代发明细和具体银行产品推荐固定不展示。
6. “企业画像”是报告产品名称，不限制总页数；内容随有效数据自动增减。
7. 最终 PDF 必须经过逐页渲染验收；无法验收时不得交付 PDF，直接回退 Markdown。
8. 工商深度成功后，最终报告必须包含以内部事实为底座的综合核心观点、执行摘要四项和企业基本信息解读；不得以数据不足为由删除。扩展维度不足时，核心观点至少保留规范企业全称、已确认的内部业务基础、信息边界和拜访核验重点，不得用外部网页或模型常识补齐标准事实。

**SKILL 版本**：v2.12 ｜ **适配数据源**：连接标识为 `cisp-mcp` 的水滴征信 MCP 当前 34 工具版本 + AI 网络搜索工具核验的正规网站原始页面 ｜ **外部默认窗口**：企业动态与资产节点近 12 个月；官网稳定人物/设施页及带明确日期的可核验历史事实不限于该窗口 ｜ **页面规格**：Letter 215.9 × 279.4 mm ｜ **默认交付**：PDF，失败回退 Markdown
