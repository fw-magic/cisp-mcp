<!-- resource-id: cisp://skill/client-pre-visit-one-pager/tool-binding -->
<!-- resource-version: 0-dev -->
<!-- source-skill-version: v5.3-profile-candidate-pool -->

# 内部工具绑定、字段映射与查询顺序

本文件是‘客户访前一页纸’ Skill 的调试期本地资源，也是对应未来 MCP Resource 的唯一正文源。进入主 `SKILL.md` 指定阶段后完整读取本文件。

## 内容索引

- [cisp-mcp 工具绑定]
- [字段别名]
- [关键字段映射]
- [锚定主体]
- [查询扩展维度]

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
| 年度员工信息补充 | `p0130025_query_company_key_indicators` | 主体确认后即调用；`ent_info=规范企业全称`，`indicator_type="2"`；所有年度、员工和金额字段按其自身口径进入经营数据或线索表 |
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
| `FIN_KEY` | `p0130025_query_company_key_indicators.data`；保存全部可用员工与经营指标原值和状态 |
| `TM` | `p0010073_query_trademark_info.data` |
| `IP` | `p0010078_query_patent_info.data` |
| `SW` | `p0010074_query_software_copyright_info.data` |
| `WC` | `p0010075_query_work_copyright_info.data` |
| `ICP` | `p0010076_query_icp_filing_info.data` |
| `LIC` | `p0010084_query_license_info.data` |
| `HON` | `p0110003_query_honor_qualification_info.data` |
| `OP` | `p0050007_p0050008_query_public_opinion_info` |
| `WEB` | AI 网络搜索查询记录、搜索摘要候选及打开的外部原始网页证据；企业简介候选允许保留未打开摘要 |
| `D` | 从内部原值、`WEB.sources` 与 `WEB.candidates` 忠实压缩形成的候选事实池和派生文案，不新增事实 |
| `META` | 查询时间、报告编号、格式等报告元数据 |

占位符语法：

- 直接字段：`{{B.basicList[0].orgName}}`
- 列表循环：`{{#each B.shareholderList}}...{{/each}}`；开放纳入模式不设置条目上限
- 循环内一基序号：`{{add @index 1}}`；当前 `each` 循环第一项输出 `1`，每进入一个新的 `each` 循环重新从 `1` 起编
- 条件板块：`{{#if B.personList}}...{{/if}}`
- 列表计数：`{{count(B.dishonestList)}}`
- 内部来源维度连接：`{{join D.source_attributions.basic.internal_dimensions|separator="、"}}`
- 外部网站名称汇总：`{{joinUniqueSourceSiteNames WEB.sources|ids=D.source_attributions.summary.external_source_ids|separator="、"|quote="《》"}}`；按 ID 顺序解析并去重 `site_name`
- 内部主体事实白名单：`D.company_overview_facts`
- 内部确定性回退文本：`{{D.company_overview_fallback}}`
- AI 内部主体描述：`{{D.core_internal_baseline}}`
- 核心观点企业简介候选事实池：`D.core_profile_candidate_facts`；仅用于生成和验收，不直接渲染
- 核心观点企业简介：`{{D.core_company_profile}}`
- 核心观点关键沿革（可选）：`{{D.core_history_evolution}}`
- 核心观点重点发展方向：`{{D.core_development_direction}}`
- 核心观点风险提示：`{{D.core_risk_prompt}}`
- 核心观点拜访目标：`{{D.core_visit_objective}}`
- 固定大章节编号：`{{D.section_numbers.core}}`、`{{D.section_numbers.summary}}`、`{{D.section_numbers.profile}}`、`{{D.section_numbers.industry}}`、`{{D.section_numbers.marketing}}`、`{{D.section_numbers.risk}}`、`{{D.section_numbers.visit}}`
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
| 年度员工与经营补充 | `FIN_KEY.coreLndicatorInfo[]` 的全部可用字段；原值进入对应口径，缺少期间或单位时标记边界 |
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
| 外部企业动态 | `WEB.sources[].scopes[]` 包含 `company_update` 或相关主题的全部来源及 `WEB.candidates[]` 候选 |
| 企业官网与外部描述 | `WEB.sources[].scopes[]` 包含 `company_description` 的事实、自述、宣传、排名、数值和模型解读；按证据状态分层 |
| 关键决策人公开背景 | `WEB.sources[].scopes[]` 包含 `person_background` 的内部人员与外部候选人员履历、教育、职务、观点和决策角色分析，支持两跳身份桥接 |
| 外部股东说明 | `WEB.sources[].scopes[]` 包含 `shareholder_context` 的当前/历史股东、比例、控制关系、实际控制人和最终受益人候选 |
| 外部有形资产线索 | `WEB.sources[].scopes[]` 包含 `tangible_asset` 的设施、地址、门店、项目、宣传产能、权属和估值线索 |
| 外部行业背景 | `WEB.sources[]` 中 `scopes[]` 包含 `industry_context` 的对应字段；可以形成定性和定量背景，包括行业排名、均值、市场规模、增长率、竞争格局及其对企业的推演，分别标注事实与模型分析 |
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
4. 以规范企业全称调用上市公司财务 `mainfinadata` 和 `rgbalance`，并无条件调用年度员工与经营指标补充 `indicator_type="2"`。日期范围至少向前推三年；有更早历史数据时继续获取。各状态分别记录，任一失败不影响其他章节。
5. 从 `B.basicList[0]` 构建行业查询范围。`regOrgCode` 严格匹配六位数字时，取前两位并追加四个 `0` 作为省级 `region_id`；`industryCode` 至少包含三位连续数字时，取前三位数字作为三级行业 `nic_id`。两项均有效时，使用 `region_lvl="r1"`、`nic_lvl="n3"`；任一项无效时，不自行猜测代码，省略全部范围参数并以行业分析响应中的 `lvl/regionId/nicId` 为实际范围。
6. 以规范企业全称并行调用行业分析的 `financialRegionRank`、`locfin`、`property`、`indLocOpr` 四种 `analysis_type`，每种类型分别记录 `success/empty/failed`，不得用一个类型的状态覆盖其他类型。行业分析任一类型失败不影响其他类型及报告其他章节。
7. 同时调用关联关系核验。只保留 `managementName`、`legalPerson`、`zzjgdm`、`suppId` 和 `kgEnt[].kgRatio/kgName/kgZzjgdm`；在写入 `REL` 前递归删除所有 `legalPersonCard`，禁止在任何临时证据、报告或回复中保存或展示该字段。
8. 同时并行调用土地资产、商标、专利、软件著作权、作品著作权、ICP、工商许可、荣誉资质和近 90 天舆情。土地资产以规范企业全称分别调用 `land_type="tdgy"`、`"tdcr"`、`"tddy"`，三类第一页均固定 `page_no="1"`、`page_size="10"`；默认不调用 `dkgs`。舆情日期使用执行日为 `end_date`，向前推 90 个自然日为 `start_date`，格式 `yyyy-MM-dd`，不设置情感过滤。
9. 土地供应读取 `detailListMeta.tdgyPageNum`，土地出让读取 `detailListMeta.tdcrPageNum`，土地抵押读取 `detailListMeta.tddyPageNum`。类别页数为有效正整数且大于 1 时，以相同 `ent_info`、`land_type` 和 `page_size` 继续请求第 2 页至末页。不得使用聚合的 `totalPage` 代替类别页数，不得因其他类别还有页数而重复请求当前类别。
10. 土地三类结果和状态相互独立：任一类别失败只将该类别记为 `failed`；成功但对应结果列表为空记为 `empty`；成功且存在有效记录记为 `success`。土地供应、土地出让、土地抵押分别进入 `META`，不得用一个汇总状态覆盖另外两类。
