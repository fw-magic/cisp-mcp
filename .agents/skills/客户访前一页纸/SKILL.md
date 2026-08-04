---
name: client-pre-visit-one-pager
description: 面向银行对公客户经理的高召回访前准备 Skill。使用连接标识为 cisp-mcp 的水滴征信 MCP 锚定中国企业主体并获取工商、股东持股、财务、土地、行业、关联关系、知识产权、许可资质、舆情与风险等内部结构化数据，同时从政府监管、法定披露、企业及交易相关方官网、专业机构、新闻媒体、商业平台、百科问答、社交与内容平台等广义外部公开来源补充企业变化、经营动作、融资触发、综合金融机会、资产、人物、行业与风险线索。采用“全量纳入、分层标注”模式：不因来源等级、证据不完整、历史属性、间接关系、非贷款性质或尚待核验而删除相关线索，而是分别进入 FACT、OPP、LEAD、SERVICE、RISK、WATCH 或 QUESTION，并显示证据等级与边界。报告围绕客户画像、贷款与综合金融机会、潜在线索、风险与观察事项、关键决策人背景和拜访推进形成完整作战材料；产品匹配仅是营销假设，不代替授信审批。默认交付 Letter 尺寸 PDF，失败时回退完整 Markdown。适用于客户访前一页纸、对公贷款营销、综合金融营销、企业融资需求挖掘、风险线索排查、关键人研究和访谈问题设计。
---

> 以证据驱动的银行对公贷款营销访前作战材料。
>
> 面向对公客户经理的访前准备工具。输入企业名称或统一社会信用代码，先通过水滴征信 MCP 锚定主体并取得结构化专业数据，再从广义外部公开来源补充经营变化与融资触发。最终材料不是通用企业介绍，而是把事实翻译成贷款营销路径：融资场景假设、产品族切入、可能还款来源、可核验增信资源、准入缺口、访谈顺序和下一步动作。
>
> 核心能力：
> - 以内部主体事实为底座，回答“为什么值得拜访、为什么此时可能有贷款需求、首选从何种贷款场景切入、主要准入障碍是什么”
> - 先建立贯穿全文的 `OPP-xx` 机会台账和 `RISK-xx` 主要风险台账，再形成“核心特征、主要机会、主要风险、拜访建议”四段式执行摘要
> - 由规则筛选内部事实白名单，再由 AI 组织自然的企业主体描述，失败时回退确定性文本
> - 审慎归因企业官网自述及分级采信的外部来源对企业业务定位的描述
> - 主体工商核验与经营范围事实摘要
> - 以内部人员名单和职务为锚点，使用通过分级采信的外部页面补充关键决策人公开职业背景，并以“姓名｜职务｜背景”三列表格展示
> - 以内外部当前股东、历史股东、穿透关系、实际控制人、最终受益人、一致行动及冲突口径共同形成股权与关联关系视图，按来源、时点和置信度分层展示
> - 全量保留与土地、建筑、生产基地、仓储设施、设备产线、在建工程、经营场所及一般资产宣传相关的事实和线索；直接证据进入 FACT，间接或待核验信息进入 LEAD/WATCH/QUESTION
> - 上市公司年度核心经营数据；缺少可靠财务资料时提供业务化的信息说明
> - 基于省级三级行业范围形成行业数量、财务排名、知识产权排名和风险信号洞察
> - 专利、商标、软件著作权、作品著作权、ICP、许可和荣誉资质盘点
> - 不限时间窗口收集公开舆情、历史事件和人物背景，并对近 12 个月企业动态进行重点标记
> - 每次主体确认后广泛检索企业、人物、股东、关联方、交易对手、资产、行业、机会与风险线索；近 12 个月只是近期标签，不是排除条件
> - 对所有可见事实逐条区分“内部：”与“外部：”来源并保持可追溯
> - 把已确认事实转成融资需求假设，把未知条件转成带对象、顺序和答案影响的拜访问题
> - 同时提出贷款、结算、现金管理、供应链金融、票据、保函、跨境、投行、托管、代发及其他综合金融服务机会；未提供具体银行产品目录时使用产品族或场景名称并明确营销假设边界
> - 为每个贷款候选方向给出用途、匹配逻辑、可能还款来源、可核验增信资源、准入缺口、开场话术和下一步动作
> - 默认生成 PDF；文档环境不可用时完整回退 Markdown
>
> 使用方式：`/client-pre-visit-one-pager 企业名称或信用代码 [--format pdf|md]`

- **命令**：`/client-pre-visit-one-pager`
- **内部数据源**：水滴征信 MCP
- **外部数据源**：AI 网络搜索工具打开并按来源类型、主体、正文、时点和交叉验证规则核验的广义公开页面
- **MCP Server 连接标识**：`cisp-mcp`
- **默认格式**：`pdf`
- **报告定位**：贷款与综合金融营销访前准备；FACT、OPP、LEAD、SERVICE、RISK、WATCH、QUESTION 分层展示，不构成授信审批、定价、法律或财务结论

---

## 开放纳入模式（最高优先级）

本节覆盖后文与“是否列入、是否展示、是否创建编号”有关的所有限制性表述。后文规则如与本节冲突，以本节为准。主体锚定、原值保存、禁止虚构、禁止模拟数据、敏感个人信息保护、来源归因和事实/推断分离仍然有效。

1. 采用“全量纳入、分层呈现”，不采用“证据不足即删除”。任何与目标企业、内部人员、股东、关联主体、所在行业、所在区域或拜访议题存在可说明关系的内部记录、外部页面、搜索摘要线索、历史事件、单方披露、间接关系、冲突事实、行业信号、模型分析或资料缺口，均进入统一候选池；除完全重复、与目标无关、含受保护敏感信息或明显恶意内容外，不作硬排除。
2. 所有候选至少进入以下一个可见层级：
   - `FACT-xx`：内部结构化事实、一级原始事实或完成交叉验证的事实；
   - `OPP-xx`：贷款、融资、供应链、项目、订单、采购、应收、设备、并购或其他可讨论的融资机会；
   - `LEAD-xx`：扩张计划、经营动作、行业传导、资金循环、招聘、门店、产能、库存、渠道、政策或其他尚未形成完整用途/还款闭环的需求发现线索；
   - `SERVICE-xx`：存款、结算、现金管理、票据、收单、代发、银行卡、个人金融、托管、跨境、投行、保险及其他非贷款综合金融机会；
   - `RISK-xx`：主体自身或交易结构中已有直接事实支持、可能影响准入或推进的风险；
   - `WATCH-xx`：历史风险、关联主体风险、行业风险、人物与治理风险、弱来源负面线索、冲突或尚未证实的风险观察；
   - `QUESTION-xx`：只有搜索摘要、同名可能性、资料缺口或无法完成正文核验的线索，转为明确的拜访核验问题。
3. 不设置 OPP、LEAD、SERVICE、RISK、WATCH、人物、股东、资产、舆情或来源数量上限。只删除完全相同的重复记录；同一事实如支持不同产品、用途、还款路径或风险路径，可以分别建立条目并注明关联。
4. 来源等级只决定 `evidence_state` 和展示措辞，不决定是否纳入。每条来源或线索记录：`source_level`、`evidence_state`、`confidence`、`relationship_path`、`time_state`、`inclusion_layer`、`limitations`。允许值：
   - `evidence_state`：`verified_primary|verified_cross_source|company_self_reported|single_source|platform_clue|search_snippet_only|model_inference|conflicting|unverified`；
   - `confidence`：`高|中|低|未知`；
   - `relationship_path`：`direct|verified_alias|two_hop|indirect|ambiguous`；
   - `time_state`：`current|historical|undated|conflicting`。
5. 搜索结果摘要、无法打开的页面、付费墙和登录墙内容可以进入候选池及 `QUESTION/WATCH/LEAD`，但必须明确写“仅检索摘要/正文未核验”，不得写成已确认事实。模型推断可以进入 `LEAD/WATCH/QUESTION`，必须显示“模型分析假设”及推断链，不能进入 `FACT`。
6. 外部人物背景允许两跳或多跳身份桥接：内部人员名单确认目标企业关系，关系页确认“人物—目标企业”，权威履历页确认“同一人物—教育/职业经历”。用姓名、历史任职、机构、职务、时间等至少两项身份键消歧；无法消歧时仍进入 `QUESTION`，不直接删除。
7. 外部股东、关联方、历史管理层、客户、供应商、合作方和潜在实际控制关系均可展示。内部与外部口径分列，不用外部值静默覆盖内部值；冲突时同时列示并标为 `conflicting`。
8. 外部财务、员工、资产面积、产能、市场份额、客户数量、行业排名等数值均可进入报告。内部值、法定披露值、企业自述值、媒体值、平台值和模型估算值必须分列来源与口径；模型估算仅允许作为 `LEAD/WATCH`，不得冒充事实。仍禁止模拟填充不存在的数据。
9. 机会和风险不要求先具备完整金额、用途、期限、第一还款来源、增信或当前状态。缺项不阻止列入，只降低证据强度并转化为核验问题。非贷款产品、行业趋势、品牌荣誉、注册资本、员工数量、扩张计划、历史事件和关联主体线索均可单独创建对应的 `LEAD/SERVICE/WATCH`。
10. 报告必须同时展示“已核实事实”和“开放线索池”，不得为了简洁隐藏低置信度条目。排序按 `FACT/RISK/OPP → LEAD/SERVICE/WATCH → QUESTION`，同层按证据强度、时间新近性和业务相关性排序，不按排除规则删减。
11. 保留脱敏审计文件 `output/audit/{company_name}-客户访前一页纸-audit.json`，记录实际查询词、候选 URL、打开状态、采用层级、身份桥接、冲突、拒绝原因（仅限完全重复/无关/敏感/恶意）及最终编号。不得在验收后删除该文件。

---

## MCP 服务依赖

1. 仅使用客户 Agent 中配置名称或连接标识为 `cisp-mcp` 的 MCP Server。连接方式、认证方式和连接参数由客户 Agent 的 MCP 配置提供，不属于本 Skill 的职责。
2. 执行前检查 `cisp-mcp` 是否已连接，并检查下方绑定的工具名及输入参数 schema。不得只凭“水滴征信 MCP”“CISP MCP”等展示名称，或工具语义相似，改用其他 MCP Server。
3. 客户 Agent 可能把连接标识规范化为工具命名空间，例如将 `cisp-mcp` 显示为 `cisp_mcp`。只有当工具元数据明确归属于原始连接标识 `cisp-mcp` 时，才可把该命名空间下的同名工具视为本 Skill 的目标工具。
4. `p0010058_query_business_basic_deep` 是必需工具。`cisp-mcp` 未连接、该工具不存在或其参数 schema 与本 Skill 不兼容时，立即停止，不生成报告，并提示用户检查或连接 `cisp-mcp`；禁止改用网络搜索、其他 MCP 或同义工具替代内部主体核验。
5. 其余绑定工具为内部扩展维度工具。单个扩展工具不存在、不可用或调用失败时，将对应维度记为 `failed`，继续处理其他维度；不得用其他 MCP 或外部网页填充该内部结构化维度。
6. 始终通过 Agent 已注册的 `cisp-mcp` 工具调用服务。

## AI 网络搜索依赖与来源准入

1. 内部工商深度成功并确认规范企业全称后，使用 Agent 可用的 AI 网络搜索与网页浏览工具。搜索结果摘要、AI 检索摘要和未打开片段进入候选池，标记 `search_snippet_only`；打开正文并核验后再升级证据状态。
2. 每次生成报告都执行定向网络搜索，默认窗口为报告生成日前 12 个月。使用内部确认的规范企业全称、可信曾用名和内部工商行业名称构造查询，至少覆盖：企业官网简介及业务/产品/项目动态、政府或监管公告、交易所公告、正规机构或媒体对企业的介绍、内部已确认关键决策人的公开职业背景、内部已确认机构股东的公开身份或投资关系、生产基地/厂房/仓储/设备产线/在建工程等有形资产线索、采购销售周期、项目建设、设备更新、订单合同、应收账款、存货、季节性备货、并购重整等融资触发、近期公开事件，以及政府/统计机构/行业协会/高校/权威研究机构发布的行业背景。无发布日期的企业官网稳定介绍页、管理团队页、人物介绍页、已确认机构股东官方稳定介绍页或设施介绍页不受 12 个月限制，但必须记录访问日期。
3. 外部来源按以下等级标注，不以等级决定是否纳入：
   - 一级：政府、监管机构、法院、交易所、统计机构、目标企业官方网站，以及仅用于股东说明的已确认机构股东官方网站；用户指定目标银行时，该银行官方网站和正式产品资料仅作为其自身产品事实的一级来源；
   - 二级：具有明确主办单位的正规行业协会、高校和权威研究机构；
   - 三级：具有编辑审核机制的主流媒体。能追溯或交叉验证时升级为 `verified_cross_source`；否则以 `single_source` 纳入并明确边界。
   - 四级：商业企业信息聚合平台、百科、问答、论坛、个人博客、自媒体、社交平台、内容平台、新闻聚合与转载站、招聘、地图、招商和其他开放网络页面。全部可以纳入；完成交叉支持时提升置信度，否则标记 `platform_clue`、`低` 置信度并进入 `LEAD/WATCH/QUESTION`。
4. 所有来源类型、搜索结果和打不开的候选链接都进入 `WEB.candidates`。能打开正文的进入 `WEB.sources`；无法打开、无稳定 URL、付费墙或登录墙页面仍保留候选元数据和限制说明。没有发布日期时记录访问日期并标记 `undated`，不自动删除。
5. 企业官网自述必须写成“企业官网披露”，不得改写为第三方核验结论。外部来源冲突时优先一级来源和直接原始页面；仍无法消解时并列说明冲突和日期，不由模型判断真伪，不把冲突值合并。
6. 网络工具不可用或搜索失败时，将 `WEB.status` 记为 `unavailable`，继续使用内部证据生成报告，并把未完成的主题登记为 `QUESTION`；不得因此降低内部必选工具要求。
7. 每个外部事实或线索绑定唯一 `source_id` 或 `candidate_id`。主体精确匹配、别名匹配、两跳关系、间接关系和歧义关系均可纳入，分别记录 `relationship_path`；只有 `direct/verified_alias/two_hop` 可以直接支持 FACT，`indirect/ambiguous` 进入 LEAD/WATCH/QUESTION。

### 外网搜索范围（广义来源池）

外网检索按“广覆盖搜索、分等级采信”执行。下表中的所有来源类型都可以进入报告证据模型，但必须分别满足对应的正文核验、主体匹配、时点、明确归因和交叉验证规则；来源等级决定其能否独立支持事实，不决定是否一律排除。

| 搜索线路 | 广义来源范围 | 重点发现内容 | 采信边界 |
| --- | --- | --- | --- |
| 政府、监管与司法 | 各级政府门户及政务公开平台；市场监管、发展改革、工业和信息化、财政、税务、海关、生态环境、应急管理、自然资源、住房城乡建设、金融监管、证监、知识产权等主管部门；人民法院、人民检察院及其公开平台；信用中国、国家企业信用信息公示系统、中国执行信息公开网；政府采购网、公共资源交易中心及依法设立的招投标公告平台 | 工商变更、政策适用、项目备案/核准、行政许可、处罚整改、欠税、海关信用、环保与安全事项、土地规划、司法重整、诉讼执行、政府采购和公共项目 | 优先采用具体公告、决定、裁定、批复、公示、报告或项目正文；栏目页、检索页和仅有标题的索引页不得作为证据 |
| 资本市场与法定披露 | 证券交易所、全国股转系统、证监会指定信息披露平台、上市公司公告平台、银行间市场交易商协会及依法承担法定披露职能的平台；行情和证券资讯平台 | 定期报告、临时公告、问询回复、投资者关系记录、债券募集及存续公告、重大合同、担保质押、股权和管理层变化 | 法定平台具体公告或报告可作为一级来源；行情和证券资讯页面按三级或四级来源归因并执行回溯或交叉验证，不得用行情快照替代公告原文 |
| 企业及交易相关方官方渠道 | 目标企业官网及官网新闻、关于我们、管理团队、产品服务、项目案例、投资者关系、社会责任/ESG、招标采购、人才招聘页面；股东、客户、供应商、合作方、投资方或项目业主官网和法定公告；能够确认官方主体的公众号、视频号及其他官方社交账号 | 企业自述、人物背景、产品与业务定位、项目/合同阶段、生产基地和设施、组织调整、投资关系、上下游和合作关系 | 目标企业官方渠道按企业自述归因；交易相关方页面可以扩展客户、供应商、合作方和关联方候选，直接点名双方关系时进入 FACT/OPP/RISK，否则进入 LEAD/WATCH |
| 统计、行业与专业机构 | 国家及地方统计机构；具有明确主办单位的行业协会、商会、标准化组织；高校、国家级或省级科研院所、政府研究机构、权威智库 | 行业政策、运行情况、统计口径、标准规范、技术路线、区域产业背景和行业风险背景 | 优先采用原始统计公报、正式报告、政策解读或研究材料；不得从外部行业资料反推目标企业市场份额、行业排名、经营数值、客户或上下游关系 |
| 新闻媒体 | 中央媒体、地方党政媒体、全国性财经媒体、具有采编审核机制的主流媒体，以及能够说明主办单位和编辑责任的垂直行业媒体 | 近期经营动态、关键人物公开访谈、重大转折、项目进展、争议事件和原始披露线索 | 媒体正文须可打开并明确记者/编辑或发布机构；涉及金额、股权、司法、税务、处罚、事故、合同阶段等关键事实时，优先回溯一级来源，无法回溯时由两个相互独立的正规来源交叉印证 |
| 公共业务与技术线索平台 | 政府或法定机构运营的专利、商标、著作权、标准、认证认可、药品器械、建筑资质、排污许可、环评公示、招标投标、政府采购和公共资源交易平台 | 知识产权、专业许可、技术资质、项目招采、建设审批和公共交易线索 | 只有能打开具体记录、公告或证书信息页并确认权利人/申请人/项目主体时才可采信；不得以结果列表数量或搜索摘要代替正文 |
| 银行与政策性金融机构官方渠道 | 用户指定银行、政策性银行、商业银行官网及其正式产品手册、业务规则、公告和分支机构官方页面 | 贷款产品名称、适用对象、用途、期限、担保方式、申请条件和材料要求 | 仅在用户提供目标银行或要求匹配具体银行产品时检索；具体产品事实只采信该银行官方页面或用户提供的有效产品资料。不得用第三方营销页虚构产品参数，不得把公开产品条件写成客户已满足条件 |
| 平台型与开放网络来源 | 商业企业信息聚合平台；百科、问答、论坛、个人博客、社交平台、自媒体、新闻聚合和转载站；招聘、地图、招商及其他内容平台 | 曾用名、品牌名、人物履历、项目名、经营地点、招聘方向、公告线索、事件时间线及平台自身整理的公开信息 | 全量纳入并明确平台属性；招聘、地图、招商、百科和自媒体可单独形成低置信度 LEAD/WATCH/QUESTION，也可在交叉验证后升级 |

执行搜索时至少覆盖以下主题，不得只搜索企业名称或只依赖综合搜索结果：

1. **主体与历史**：规范企业全称、可信曾用名、品牌名、官网、企业简介、发展历程、重整、并购、股权变化、管理调整。
2. **业务与近期动作**：产品、服务、项目、合同、订单、渠道、基地、产线、投产、交付、合作、招投标、招聘及组织变化；招聘页面可按四级规则采信其直接显示的岗位方向、招聘主体、发布时点和工作地点，但必须明确写成招聘信息并完成独立交叉验证，不得据此推导人员规模、产能、项目落地或确定性经营成果。
3. **人物与股东**：只围绕内部已确认的人员和直接股东搜索职业履历、官方任职、机构身份和公开投资事件，不得通过外网扩充名单。
4. **资产与建设**：土地、厂房、生产基地、仓储、研发中心、设备、生产线、在建工程、备案、环评、规划许可、施工和投产节点。
5. **经营现金循环与融资触发**：上市、退市、定期报告、债券、融资事件、担保、质押、回购、重大合同、项目建设、设备更新、订单交付、采购备货、应收账款、存货、季节性周转、重整清偿和投资者关系活动；外部数值只用于理解带来源的公开事件，不得填充或校正内部财务字段。
6. **风险与合规**：处罚、整改、欠税、诉讼、执行、失信、限高、重整、破产、环保、安全生产、产品质量、召回、信用和许可状态。
7. **行业与区域背景**：内部工商行业对应的政策、统计公报、行业运行报告、标准、技术路线和所在区域产业规划；不得使用泛行业材料替代企业事实。
8. **贷款与综合金融产品资料**：无论用户是否指定银行，均可搜索银行官方产品页、正式手册、公开业务规则和市场常见产品；未指定银行时把具体银行产品标记为市场参考，不假定目标银行可提供或客户已满足条件。

候选采信顺序固定为“一级原始来源 → 企业或交易相关方官方来源 → 二级专业机构 → 三级媒体 → 四级平台型与开放网络来源”。同一事实取得更高等级原始页面时，以原始页面作为主证据，较低等级页面仍可作为补充证据并明确归因；只有四级来源且未满足相应交叉验证条件时，将内容转成待核实问题，不写成已确认事实。

## 数据纪律

1. 内部结构化事实使用本次水滴征信 MCP 原值；外部事实、平台页、搜索摘要和模型分析均可进入独立口径。不得用任何外部或模型值静默覆盖内部原值；必须标明来源、证据状态和口径。样例企业内容和模拟数据仍禁止作为目标企业事实。
2. 先锚定唯一企业主体，再查询扩展维度。工商深度失败、无结果或主体不一致时停止生成。
3. `B`、`ID`、`OV_*`、`LAND`、`IND`、`REL`、`FIN_*`、`TM` 至 `OP` 中的金额、比例、日期、数量和币种必须逐字保存。报告展示层允许做无损格式化，但禁止四舍五入、补零、截断有效小数、换算、加总、相减、相乘或倒算；“产业画像生成规则”允许把文档明确为比率的 `IND` 十进制原值精确乘以 100 后显示为百分比；“核心经营数据生成规则”允许为文档明确为比率的上市公司财务指标原值直接追加 `%`，不得改变数值。有形资产不再计算土地面积、价格或抵押金额合计。
4. 不根据股东、任职或投资关系推导实际控制人、最终受益人、一致行动关系、融资轮次或资本市场状态。
5. 分页接口以 `*ListMeta.totalCount` 表示总量；第一页记录只称“本次首批返回记录”，不得称为“最新”或“全部”。
6. 空数组只表示“本次查询未返回相关公开记录”；调用失败表示“该维度查询未完成”。两者不得互换。
7. 内部舆情和外部网页中的相关内容只称“公开事件线索”；只有一级来源原始公告可按原文陈述其公开事项，仍不得替代内部司法、监管或经营标准字段。
8. 报告正文不得出现工具代码、产品码、JSON 路径、schema、调用失败堆栈、额度或积分信息。
9. 不输出身份证号、手机号、出生日期、年龄、家庭关系、住址、个人联系方式、个人社交账号、API Key、原始响应或其他非必要个人敏感信息；关键决策人背景只保留与企业拜访相关的公开职业履历、教育背景、专业方向和职责信息。
10. 企业名称、信用代码、登记状态、成立时间、法定代表人、注册资本、地址、行业归属等标准基本信息仅使用内部数据。营收、利润、资产负债、现金流、员工规模及其他财务经营数值也仅使用内部数据；即使外部网站或年报披露相关值，也不得补填、覆盖或校正内部字段。
11. 内部结构化字段保持原值并作为“内部口径”展示；外部股权、司法、土地、税务、许可、知识产权、人员、财务、资产、产能、客户和市场数据均可作为独立“外部口径”分列，不静默覆盖内部值。外部新增人员、股东、关联方、客户、供应商、实际控制人、最终受益人、一致行动、决策权限和资产权属判断均可进入候选或观察层，必须显示来源、关系路径、时点、置信度和与内部口径的差异。
12. 可以生成市场份额、客户数量、客户渗透率、标杆客户、融资金额、额度测算、期限建议、利率信息、审批影响分析及准入观察，也可以推荐存款、代发、银行卡、个人理财、收单、现金管理、票据、托管、跨境和其他综合金融产品。公开事实与模型估算分列；模型估算必须展示方法、输入、假设和“非银行审批结论”边界，不能伪装成客户已确认或银行正式参数。
13. 大模型可以归纳、压缩和组织本次内部证据及合格 `WEB` 证据，但不得把数据缺口改写成事实，不得把标题或企业官网自述升级为已经独立核验的业务动作。
14. 未被内部证据或合格外部证据直接支持时，禁止使用“行业领先”“头部企业”“绝对控股”“经营健康”“优质客户”“资本实力强”“建议授信”等判断性表述。
15. 每个大模型派生文案必须在内部证据映射 `EVIDENCE` 中列出至少一个 `internal:<字段或状态>` 或 `external:<source_id>`；`EVIDENCE` 仅用于生成与验收，不写入报告。外部事实的可见正文必须附 `[外部：Wn]` 标记。
16. 先按固定规则构建 `D.company_overview_facts` 内部事实白名单和 `D.company_overview_fallback` 确定性回退文本，再由大模型仅在白名单内生成 `D.core_internal_baseline`；AI 只能改变取舍、语序和连接方式，不得修改原值、吸收外部信息或增加推断。最终展示的 `D.core_viewpoint` 可以在该内部主体描述上使用合格外部事实，但不得以外部资料补填、覆盖或校正企业基本信息、人员姓名与当前职务、股权、财务经营数值、风险数量和标准状态。外部人物背景仅按本 Skill 的关键决策人规则进入背景列。空字段、非数字风险字段、空结果和失败维度不得改写成“无”。
17. 企业官网自述及任何外部来源描述只能作为带明确归因的外部观察。官网内容写“企业官网将其业务定位描述为”或“企业官网披露”，其他来源写明发布机构、平台或账号及其描述场景；四级来源还必须保留其平台属性和交叉验证边界。不得把“领先、龙头、第一、唯一、实力雄厚、全球化”等宣传或评价标签改写为独立事实，不得据此生成市场地位、经营质量、客户规模、财务表现或授信判断。
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
| `WEB` | AI 网络搜索查询记录及通过准入核验的外部原始网页证据；只保存允许进入报告的事实和来源元数据 |
| `D` | 从内部原值和合格 `WEB` 证据忠实压缩形成的派生文案，不新增事实 |
| `META` | 查询时间、报告编号、格式等报告元数据 |

占位符语法：

- 直接字段：`{{B.basicList[0].orgName}}`
- 列表循环：`{{#each B.shareholderList}}...{{/each}}`；开放纳入模式不设置条目上限
- 条件板块：`{{#if B.personList}}...{{/if}}`
- 列表计数：`{{count(B.dishonestList)}}`
- 内部来源维度连接：`{{join D.source_attributions.basic.internal_dimensions|separator="、"}}`
- 按来源 ID 解析网页：`{{#eachSource WEB.sources|ids=D.source_attributions.summary.external_source_ids}}...{{/eachSource}}`；严格按 ID 数组顺序输出对应 `WEB.sources` 记录，不得输出未被引用的网页
- 内部主体事实白名单：`D.company_overview_facts`
- 内部确定性回退文本：`{{D.company_overview_fallback}}`
- AI 内部主体描述：`{{D.core_internal_baseline}}`
- 最终综合核心观点：`{{D.core_viewpoint}}`
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

### 3. 定向搜索外部公开资料

内部主体确认后执行，不得提前用搜索结果猜测主体：

1. 先按“外网搜索范围（广义来源池）”依次覆盖政府监管与司法、资本市场与法定披露、企业及交易相关方官方渠道、统计行业与专业机构、新闻媒体、公共业务与技术线索平台，以及平台型与开放网络来源；所有线路均可按对应规则形成证据。将报告生成日向前推 12 个月作为动态搜索窗口，使用规范企业全称分别组合“官网”“公司简介”“关于我们”“企业介绍”“产品”“项目”“业务动态”“机构介绍”“专访”“报道”“重整”“并购”“股权变化”“管理调整”“公告”“处罚”“诉讼”“事故”“整改”等关键词；可信曾用名只用于补充搜索，命中页面仍须核验与当前规范主体的关系。
2. 为贷款营销摘要增加专项搜索：上市公司优先检索交易所公告、定期报告、业绩说明会和投资者关系活动记录；所有企业优先检索重大项目或合同原始公告及对手方页面、工厂或基地建设进度、设备更新、采购备货、订单交付、应收账款安排、重整清偿、担保/质押/回购/股权事件、监管处罚与整改状态。候选页必须打开具体公告、活动记录或事件正文；新闻列表、公告索引、搜索结果和站内栏目首页不能作为唯一证据。外部财务数值仍不得回填、覆盖或校正内部财务字段，外部页面只可支持明确披露的事件阶段、融资触发、用途线索、交易安排和归因说明。
3. 先从 `B.personList` 整理全部内部人员，并以 `B.basicList[0].legRepName` 补充法定代表人。再对每名人员执行“目标企业关系检索”和“全网职业履历检索”；同时从企业官网、公告、媒体、活动、交易相关方和平台页面发现外部关键人候选。外部新增人员进入人员表并标记“外部候选”，不覆盖内部名单。
4. 人物背景不限来源等级和时间窗口。优先使用直接页面；允许“内部人员锚点/目标企业关系页 + 原任职机构年报、招股书、官网、高校校友页或媒体履历页”的两跳身份桥接。保存 `identity_keys`、`relationship_source_ids`、`biography_source_ids` 和 `identity_confidence`；冲突履历并列展示，无法消歧的同名线索进入 QUESTION。
5. 对全部内部股东、外部股东候选、历史股东、自然人股东、机构股东、管理人、出资人和可能控制方执行定向搜索。外部名单、比例、控制关系和股权事件作为独立外部口径展示；与内部冲突时并列，不删除任一口径。
6. 股东说明优先使用政府、国资监管、金融监管、交易所、目标企业官网或已确认机构股东官网等一级原始页面；二级、三级和四级来源也可按分级规则采信。页面必须同时确认内部股东名称、规范企业全称及二者关系；可提炼机构性质、公开投资角色、公开披露的隶属/投资关系，以及带明确日期的增资、受让、战略投资或股权变更事件。二级或三级来源必须追溯至原始披露或与另一条独立来源交叉验证；商业信息聚合页、基金销售页、个人主页、媒体概括或转载等四级来源必须由至少一条独立的一级至三级来源支持，并只作为补充说明。机构股东官网内容写“股东官网披露”，其他页面明确写发布机构或平台，不得据此证明目标企业当前股东名册或持股比例。
7. 使用规范企业全称组合“生产基地”“厂房”“工厂”“产业园”“仓储”“仓库”“研发中心”“办公楼”“设备”“生产线”“在建工程”“项目备案”“环评”“规划许可”“建设进展”等关键词搜索有形资产线索。政府、监管机构、自然资源或规划部门、交易所及目标企业官方网站等一级来源可以独立支持其正文直接披露的资产节点；二级、三级和四级来源也可进入本章节，但必须确认具体资产对象、企业角色和时点。二级或三级来源须追溯原始页面或独立交叉验证；招商宣传、商业聚合、地图、招聘、自媒体及其他四级来源须由至少一条独立的一级至三级来源支持，并按发布主体归因，不得单独证明产权、当前持有、投资额、面积、产能或设备数量。
8. 外部资产候选可以直接、别名、两跳、间接或歧义关联目标企业。注册地址、联系地址、经营范围、行业、分支机构、门店、服务网点、客户项目、荣誉、订单、融资、产品介绍、一般产能宣传和历史页面均可进入资产线索表；分别标记是否证明具体资产、权属、当前状态和估值，不能确认的部分转为 LEAD/WATCH/QUESTION。
9. 使用内部工商行业名称组合“政策”“统计”“运行情况”“行业报告”等关键词，优先限定政府、统计机构、正规行业协会、高校和权威研究机构域名。不得使用外部网页重新判定企业行业归属。
10. 先搜索，再尽量打开候选具体页面。所有候选分配 `candidate_id`；能打开正文的另分配 `Wn`。人物、股东、资产、交易和主体关系可以通过直接、别名、两跳、间接或歧义路径纳入，分别标记 `relationship_path`。同一 URL 支持多个主题时使用 `scopes[]` 和 `applicable_sections[]`，不因单一 scope 限制复用。
11. 外部企业动态、行业政策、市场趋势、宏观背景、品牌荣誉、扩张计划、人员与股东变化、招聘、门店、地图、招商、资产宣传和平台线索均可进入核心观点之外的 OPP/LEAD/SERVICE/RISK/WATCH/QUESTION。缺少企业专属资金占用或第一还款来源时降低为 LEAD 或观察级 OPP，不删除。每个使用位置在 `D.source_attributions` 登记对应 `source_id/candidate_id`。
12. 企业官网动态使用“企业官网披露”归因；企业官网人物简介使用“企业官网介绍”归因；企业或股东官网的股东说明分别使用“企业官网披露”或“股东官网披露”；企业官网设施或设备信息使用“企业官网披露”并保留自述边界。其他来源统一写明发布机构、平台或账号；四级来源不得省略平台属性。重大合同、项目或合作优先用交易所、政府、监管、目标企业或对手方原始页面交叉验证；无法取得第二个原始页面时可保留企业单方披露，但必须明确单方披露边界。二级至四级来源按规则采用交叉验证时，把全部支持同一事实的 `source_id` 登记到 `EVIDENCE`，不得只保留其中一条。
13. 网络工具可用且完成搜索时设 `WEB.status="success"`，即使只有摘要候选；工具不可用或完全未执行时设 `WEB.status="unavailable"`。页面打不开只影响候选的证据状态，不删除候选，也不改变内部维度状态。

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
    "rgbalance": {"status": "success|empty|failed", "data": "rgbalance 全部可用 data 原值"}
  },
  "FIN_KEY": {
    "status": "success|empty|failed",
    "data": "主体确认后查询的企业关键指标全部可用 data 原值"
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
    "candidates": [
      {
        "candidate_id": "C1",
        "query": "命中的查询词",
        "title_or_snippet": "搜索标题或摘要",
        "url": null,
        "open_status": "opened|failed|paywalled|login_required|snippet_only",
        "evidence_state": "search_snippet_only|platform_clue|unverified",
        "confidence": "高|中|低|未知",
        "relationship_path": "direct|verified_alias|two_hop|indirect|ambiguous",
        "time_state": "current|historical|undated|conflicting",
        "inclusion_layer": ["FACT|OPP|LEAD|SERVICE|RISK|WATCH|QUESTION"],
        "limitations": "正文、主体、时点、冲突或登录限制"
      }
    ],
    "sources": [
      {
        "source_id": "W1",
        "scopes": ["company_update|company_description|person_background|shareholder_context|tangible_asset|industry_context|financing_trigger|repayment_source|credit_enhancement|financial_metric|market_metric|customer_supplier|service_opportunity|transaction_terms|loan_product_reference|public_event"],
        "site_name": "发布网站或机构名称",
        "source_level": "一级|二级|三级|四级",
        "source_type": "government|regulator|court|tax_authority|official_disclosure_platform|exchange|statistics|company_official|counterparty_official|shareholder_official|bank_official|official_social_media|association|university|research_institute|state_media|mainstream_media|professional_media|commercial_aggregator|encyclopedia|qa_forum|personal_blog|self_media|social_media|news_aggregator|repost_site|recruitment_platform|map_platform|investment_promotion|content_platform",
        "title": "原始页面标题",
        "url": "规范化原始页面 URL",
        "published_at": null,
        "accessed_at": "YYYY-MM-DD",
        "supported_fact": "该页面直接支持的最小事实",
        "applicable_sections": ["core", "summary", "profile", "industry", "marketing", "risk", "visit"],
        "subject_match": "exact|verified_alias|person_company_match|person_identity_bridge|shareholder_company_match|asset_company_match|industry_scope|indirect|ambiguous",
        "corroboration_status": "primary|traced_to_primary|cross_checked|company_self_disclosure|cross_checked_secondary|attributed_platform_statement",
        "evidence_role": "primary|corroborating|attributed_statement",
        "corroborating_source_ids": [],
        "evidence_state": "verified_primary|verified_cross_source|company_self_reported|single_source|platform_clue|model_inference|conflicting|unverified",
        "confidence": "高|中|低|未知",
        "relationship_path": "direct|verified_alias|two_hop|indirect|ambiguous",
        "relationship_source_ids": [],
        "identity_keys": [],
        "time_state": "current|historical|undated|conflicting",
        "inclusion_layer": ["FACT|OPP|LEAD|SERVICE|RISK|WATCH|QUESTION"],
        "limitations": null
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
      "marketing": {"internal_dimensions": [], "external_source_ids": []},
      "risk": {"internal_dimensions": [], "external_source_ids": []},
      "visit": {"internal_dimensions": [], "external_source_ids": []}
    },
    "coverage_summary": "以业务语言概括资料覆盖范围和待补充事项",
    "section_numbers": {"core": "一", "summary": "二", "profile": "三", "industry": "四", "marketing": "五", "risk": "六", "visit": "七"},
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
    "core_external_description": "有通过分级采信的外部来源时形成的企业业务定位描述归因",
    "core_turning_point": "有证据时展示的并购、重整、上市退市、重大股权变化或重大项目转折",
    "core_external_context": "全部外部企业动态、历史事件、行业与候选线索的分层概括",
    "core_operating_stage": "内部经营事实支持的阶段判断，或外部动作与内部量化资料之间的审慎边界",
    "core_risk_constraint": "最重要的内部风险事实、主体范围、时点状态和必要的外部事件线索",
    "core_financing_trigger": "由项目、采购、订单、设备、建设、重整、季节性或现金循环事实形成的融资触发；没有事实时保持 null",
    "core_repayment_logic": "已有证据可支持的经营回款、合同回款或其他可能还款来源；无证据时明确待核验",
    "core_credit_support": "已有证据可支持的抵押、质押、保证或交易闭环线索；只写待核验资源，不作价值或可用性判断",
    "core_visit_focus": "围绕需求金额、用途、期限、还款来源、现有融资、增信资源和准入障碍形成的 2 至 3 项拜访核验重点",
    "core_opportunity_ids": ["OPP-01"],
    "core_risk_ids": ["RISK-01"],
    "core_viewpoint": "按‘客户与经营阶段→OPP 机会主线→用途与还款增信→RISK 约束→本次拜访目标’形成的最终贷款营销核心观点，并显式引用相关编号",
    "executive_core_features": "用已核实事实概括客户身份、经营阶段、近期转折及贷款营销价值，不提前展开产品方案",
    "opportunity_register": [
      {
        "opportunity_id": "OPP-01",
        "opportunity_title": "简洁、客户化的贷款机会名称",
        "trigger_fact": "带日期或报告期、阶段和主体边界的企业专属融资触发",
        "need_scenario": "流动资金周转|采购备货|订单履约|应收账款周转|项目建设|设备更新|并购重整|其他企业贷款场景",
        "likely_use_of_funds": "由触发事实直接指向的可能贷款用途",
        "timing": "近期|中期|待核验",
        "evidence_strength": "强线索|中线索|弱线索",
        "boundary": "金额、阶段、执行状态或企业确认情况等必要边界",
        "evidence_ids": ["internal:<字段或状态>", "external:Wn"]
      }
    ],
    "lead_register": [
      {
        "lead_id": "LEAD-01",
        "lead_title": "尚未形成完整融资闭环的需求发现线索",
        "signal": "企业动作、行业传导、扩张、门店、招聘、政策、资产或资金循环信号",
        "possible_financial_need": "可能对应的融资或综合金融需求",
        "missing_links": "用途、金额、期限、还款来源、承担主体等缺口",
        "evidence_strength": "强线索|中线索|弱线索|仅摘要|模型推断",
        "evidence_ids": []
      }
    ],
    "service_register": [
      {
        "service_id": "SERVICE-01",
        "service_title": "非贷款综合金融机会",
        "service_type": "存款|结算|现金管理|票据|收单|代发|银行卡|个人金融|托管|跨境|投行|保险|其他",
        "trigger_signal": "客户专属或行业/人员规模等触发信号",
        "fit_logic": "为什么值得在拜访中讨论",
        "verification": "需核实的现状和合作条件",
        "evidence_ids": []
      }
    ],
    "major_risk_register": [
      {
        "risk_id": "RISK-01",
        "risk_title": "会改变贷款准入、结构或推进顺序的主要风险",
        "fact_boundary": "已核实事实、主体、日期或期间、当前状态与资料边界",
        "affected_opportunity_ids": ["OPP-01"],
        "loan_impact": "对相关机会的准入、用途、期限、还款、增信、资料或推进节奏的条件式影响",
        "verification": "需核实的当前状态、证明材料或缓释方向",
        "evidence_ids": ["internal:<归一化风险事实>", "external:Wn"]
      }
    ],
    "watch_register": [
      {
        "watch_id": "WATCH-01",
        "watch_title": "历史、关联、行业、人物、治理、弱来源或冲突风险观察",
        "signal_boundary": "信号、主体范围、时点、来源与不确定性",
        "possible_impact": "对经营、融资、准入或推进的潜在影响",
        "verification": "核验问题或所需材料",
        "evidence_strength": "强线索|中线索|弱线索|仅摘要|模型推断",
        "evidence_ids": []
      }
    ],
    "executive_visit_strategy": "围绕优先 OPP、关键 RISK、建议切入点、必须核验事项和预期下一步形成的拜访建议",
    "basic_interpretation": "基本登记事实与访前含义",
    "person_rows": [
      {
        "name": "内部已确认人员或外部候选人员姓名",
        "person_origin": "internal|external_candidate|both",
        "position": "内部职务与外部职务分列并标明时点",
        "is_legal_representative": false,
        "background": "直接或两跳身份桥接取得的教育、职业、专业与职责背景",
        "relationship_source_ids": [],
        "background_source_ids": [],
        "identity_keys": [],
        "identity_confidence": "高|中|低|未知",
        "conflicts": []
      }
    ],
    "people_interpretation": null,
    "has_equity_or_network": false,
    "has_shareholder_notes": false,
    "shareholder_rows": [
      {
        "name": "内部直接股东名称",
        "holding_display": "内部持股比例，比例缺失时按规则使用认缴出资信息或固定边界说明",
        "note": null,
        "note_source_ids": []
      }
    ],
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
    "industry_positioning": "企业行业归属、产业链经营环节线索与上下游信息边界",
    "industry_business_model_interpretation": "行业经营模式、现金循环特征及需要向企业核验的资金占用环节",
    "industry_external_context": null,
    "industry_scope_display": null,
    "has_industry_cycle": false,
    "industry_cycle_rows": [
      {"signal": "周期、季节、库存、账期、回款或资本开支信号", "verified_fact": "带来源的最小行业事实", "period_scope": "期间与地区行业范围", "cashflow_transmission": "对企业经营现金流的条件式传导假设", "enterprise_verification": "需向企业核验的指标或材料"}
    ],
    "industry_cycle_interpretation": "行业事实如何可能传导至备货、库存、账期、回款或资本开支，以及对企业的核验要求",
    "has_industry_benchmark": false,
    "industry_benchmark_rows": [
      {"topic": "同口径对标维度", "company_position": "内部企业行业位置", "industry_reference": "内部行业参考", "period_scope": "同期间与同范围", "lending_implication": "对资料核验或贷款结构的条件式启示"}
    ],
    "industry_benchmark_interpretation": "同范围、同期间行业参照对经营核验和贷款结构设计的启示",
    "has_industry_policy": false,
    "industry_policy_rows": [
      {"policy_or_environment": "现行官方政策或融资环境事实", "applicable_scope": "地区、行业、期限与对象范围", "financing_relevance": "与贷款营销的辅助关系", "enterprise_verification": "企业适用资格、项目或申报状态待核事项"}
    ],
    "industry_policy_interpretation": "现行政策或融资环境的适用边界及客户应补充的证明条件",
    "has_industry_risk": false,
    "industry_risk_rows": [
      {"signal": "行业风险信号", "verified_fact": "带期间和范围的已核实事实", "cashflow_transmission": "对销量、毛利、库存、应收或现金流的条件式传导", "enterprise_verification": "企业专属核验指标", "lending_implication": "对用途、期限、还款、增信或资料的条件式启示"}
    ],
    "industry_risk_interpretation": "行业风险经经营现金流传导后可能影响的用途、期限、还款或增信安排",
    "industry_information_boundary": "行业资料与企业专属经营事实、融资需求和授信准入之间的边界",
    "financing_need_rows": [
      {
        "opportunity_id": "OPP-01",
        "need_scenario": "贷款需求场景",
        "trigger_fact": "带日期/报告期和阶段的企业专属触发事实",
        "likely_use_of_funds": "由事实直接指向的可能贷款用途",
        "timing": "近期|中期|待核验",
        "evidence_strength": "强线索|中线索|弱线索",
        "verification_focus": "为形成贷款方案必须现场确认的问题",
        "evidence_ids": ["与 opportunity_register 中同一 OPP 完全一致的证据 ID"]
      }
    ],
    "loan_product_candidates": [
      {
        "priority": "首选|备选|观察",
        "opportunity_id": "OPP-01",
        "product_family": "流动资金贷款|循环额度贷款|订单融资|应收账款融资|供应链融资|固定资产贷款|项目贷款|设备更新贷款|并购贷款|其他企业贷款产品族|融资需求诊断（不推荐具体产品）",
        "fit_logic": "触发事实→资金用途→产品族的匹配逻辑",
        "possible_repayment_source": "可被现场及材料验证的第一还款来源假设",
        "possible_credit_enhancement": "可被核验的抵押、质押、保证或交易闭环线索；无证据写待核验",
        "qualification_gaps": "额度、期限、用途、现金流、现有融资、担保、合规等关键缺口",
        "opening_pitch": "不承诺审批结果的一句话客户化开场"
      }
    ],
    "service_product_candidates": [
      {
        "priority": "首选|备选|观察|探索",
        "service_id": "SERVICE-01",
        "product_family": "存款|结算|现金管理|票据|收单|代发|银行卡|个人金融|托管|跨境|投行|保险|其他综合金融产品",
        "fit_logic": "触发信号→客户场景→产品或服务的匹配逻辑",
        "qualification_gaps": "现有合作、授权、交易规模、系统和合规缺口",
        "opening_pitch": "不承诺结果的一句话客户化开场"
      }
    ],
    "marketing_sequence": [
      {"stage": "本次拜访", "related_opportunity_ids": ["OPP-01"], "related_risk_ids": ["RISK-01"], "objective": "确认需求与准入基础", "actions": "要问、要看、要取得的材料", "exit_criteria": "进入下一步的明确条件"},
      {"stage": "拜访后 3 个工作日", "related_opportunity_ids": ["OPP-01"], "related_risk_ids": ["RISK-01"], "objective": "形成初步融资结构", "actions": "内部预审与客户补件", "exit_criteria": "产品、用途、金额、期限、还款与增信要素可描述"},
      {"stage": "后续推进", "related_opportunity_ids": ["OPP-01"], "related_risk_ids": [], "objective": "提交正式业务流程", "actions": "按银行制度推进", "exit_criteria": "客户授权且基础资料齐备"}
    ],
    "marketing_boundary": "产品方向均为访前营销假设，具体产品名称、额度、期限、利率、担保和准入以目标银行制度及审批为准",
    "has_risks": false,
    "risk_evidence_groups": {
      "subject_compliance": {"status": "hit|context|empty|unavailable", "facts": []},
      "judicial_enforcement": {"status": "hit|context|empty|unavailable", "facts": []},
      "asset_encumbrance": {"status": "hit|context|empty|unavailable", "facts": []},
      "tax_license_compliance": {"status": "hit|context|empty|unavailable", "facts": []},
      "financial_attention": {"status": "hit|context|empty|unavailable", "facts": []},
      "transaction_terms": {"status": "hit|context|empty|unavailable", "facts": []},
      "related_party_and_governance": {"status": "hit|context|empty|unavailable", "facts": []},
      "industry_and_market": {"status": "hit|context|empty|unavailable", "facts": []},
      "public_event_clues": {"status": "hit|context|empty|unavailable", "facts": []}
    },
    "risks": [
      {
        "risk_id": "RISK-01",
        "affected_opportunity_ids": ["OPP-01"],
        "topic": "关注事项",
        "detail": "已核实事实、主体、日期/期间、状态和范围边界",
        "sales_implication": "对产品准入、担保结构、期限、资料或推进顺序的条件式影响",
        "verification": "应核实的当前状态、证明材料或可讨论缓释方向"
      }
    ],
    "risk_zero_dimensions": "以、连接的明确零值维度",
    "risk_compliance_context": "最新纳税评级、明确许可状态及必要的时间边界",
    "risk_information_boundary": "以业务语言说明无明细、时间较早、资料缺失或不同范围不可合并",
    "risk_interpretation": "命中事实、当前状态边界和贷款营销前置核验；无命中时说明不等同于无风险及应取得的基础资料",
    "visit_objectives": [{"objective": "本次拜访必须达成的可验证目标", "related_opportunity_ids": ["OPP-01"], "related_risk_ids": ["RISK-01"]}],
    "recommended_topics": [
      {"topic": "客户化话题", "opening_basis": "对应企业事实", "transition": "如何自然转入融资需求", "related_opportunity_ids": ["OPP-01"]}
    ],
    "visit_questions": [
      {"sequence": 1, "related_opportunity_ids": ["OPP-01"], "related_risk_ids": ["RISK-01"], "audience": "建议沟通对象", "topic": "经营计划|融资用途|金额期限|还款来源|现有融资|增信资源|风险化解|合作意愿", "basis": "已知事实或信息缺口", "question": "开放式问题", "answer_impact": "该答案将如何改变候选贷款方案"}
    ],
    "document_checklist": [
      {"document": "建议取得或请客户后续提供的资料", "purpose": "用于核验需求、还款、增信或准入", "related_opportunity_ids": ["OPP-01"], "related_risk_ids": ["RISK-01"]}
    ],
    "taboo_notes": ["应避免的措辞、承诺或敏感切入方式"]
  },
  "EVIDENCE": {
    "company_overview_facts": ["internal:B.basicList[0].orgName", "实际进入内部事实白名单的 internal:B/OV_BASIC/OV_BRIEF/OV_MARKET/OV_TAX/OV_RISK 字段"],
    "company_overview_fallback": ["实际进入确定性回退文本的 internal:B/OV_BASIC/OV_BRIEF/OV_MARKET/OV_TAX/OV_RISK 字段"],
    "core_internal_baseline": ["AI 主体描述逐句使用的 internal:company_overview_facts 对应原始字段"],
    "core_capability": ["实际支持能力信号的 internal:B/OV_MARKET/LAND/TM/IP/SW/WC/ICP/LIC/HON 字段"],
    "core_company_self_description": ["实际进入企业官网自述的 external:Wn"],
    "core_external_description": ["实际进入外部来源描述的 external:Wn"],
    "core_turning_point": ["实际支持关键转折的 internal:B/OV_MARKET 字段或 external:Wn"],
    "core_external_context": ["实际进入近期观察的 external:Wn"],
    "core_operating_stage": ["实际展示的 internal:FIN_LISTED/OP 字段、信息边界或 external:Wn"],
    "core_risk_constraint": ["实际进入核心风险约束的 internal:<归一化风险事实> 或 external:Wn"],
    "core_financing_trigger": ["实际支持资金占用场景的 internal:<字段> 或 external:Wn"],
    "core_repayment_logic": ["实际支持可能还款来源的 internal:<字段> 或 external:Wn；无事实时登记资料缺口"],
    "core_credit_support": ["实际支持可核验增信资源的 internal:<字段> 或 external:Wn；不得登记推测"],
    "core_visit_focus": ["支持核验重点的 internal:<事实和数据缺口> 或 external:Wn"],
    "core_viewpoint": ["逐句登记上述核心观点分项实际使用的 internal:<字段或状态> 与 external:Wn"],
    "core_opportunity_ids": ["逐项回指 opportunity_register 中实际进入核心观点的 OPP 编号"],
    "core_risk_ids": ["逐项回指 major_risk_register 中实际进入核心观点的 RISK 编号"],
    "coverage_summary": ["internal:META 中各业务维度状态和 web_search_status"],
    "source_attributions": ["逐章节登记实际显示的内部业务维度和 external:Wn；外部 ID 必须存在于 WEB.sources"],
    "person_rows": ["逐行登记姓名和职务对应的 internal:B.personList 或 internal:B.basicList[0].legRepName；背景事实另登记 external:Wn"],
    "people_interpretation": ["实际使用的 internal:<人员字段或资料边界> 与 external:Wn"],
    "shareholder_rows": ["逐行登记股东名称和持股情况对应的 internal:B.shareholderList 字段；说明事实另登记 external:Wn"],
    "equity_interpretation": ["实际使用的 internal:B.shareholderList/REL 字段、资料边界与 external:Wn"],
    "tangible_asset_rows": ["逐行登记实际使用的 internal:LAND/B 明确抵押物字段或 external:Wn；不登记行业、经营范围、注册地址和未展示字段"],
    "assets_interpretation": ["实际进入有形或无形资产展示的 internal:<字段和边界> 与 external:Wn"],
    "industry_positioning": ["实际使用的 internal:B.basicList[0] 行业与经营范围字段，以及上下游资料边界"],
    "industry_business_model_interpretation": ["支持经营模式、现金循环与资金占用核验方向的 internal:B/IND 字段或 external:Wn"],
    "industry_external_context": ["实际进入定性行业背景的 external:Wn"],
    "industry_scope_display": ["实际用于确定中文地区名和中文行业名的 internal:B/IND 字段，以及仅用于一致性核验的 regionId/nicId"],
    "industry_cycle_rows": ["实际使用的 internal:IND.financialRegionRank/locfin/indLocOpr 字段或 external:Wn"],
    "industry_cycle_interpretation": ["进入行业周期与资金占用表的事实、传导边界和企业核验缺口"],
    "industry_benchmark_rows": ["实际使用的 internal:IND.financialRegionRank/property 字段"],
    "industry_benchmark_interpretation": ["进入行业对标表的同范围同期间事实、口径边界和贷款启示"],
    "industry_policy_rows": ["实际使用的现行有效 external:Wn 及适用范围"],
    "industry_policy_interpretation": ["政策适用条件、与融资的关系和企业待核验条件"],
    "industry_risk_rows": ["实际使用的 internal:IND.indLocOpr 字段"],
    "industry_risk_interpretation": ["行业风险事实、经营现金流传导、企业核验与贷款结构启示"],
    "industry_information_boundary": ["internal:<行业资料可用性和口径状态> 或 external:Wn，以及企业专属资料缺口"],
    "core_operation_rows": ["实际进入核心经营数据表的 internal:FIN_LISTED/FIN_KEY 原值及选定报告期"],
    "operations_boundary": ["internal:FIN_LISTED.mainfinadata 状态、有效年度报告选择结果和必要的信息边界"],
    "operations_interpretation": ["实际展示的 internal:<核心经营数据字段和选定报告期>"],
    "executive_core_features": ["逐句登记支持客户身份、经营阶段、近期转折和拜访价值的 internal:<字段> 或 external:Wn"],
    "opportunity_register": ["逐项登记 OPP 的企业专属触发、日期或报告期、阶段、用途、边界及 internal:<字段> 或 external:Wn"],
    "lead_register": ["逐项登记 LEAD 的信号、推断链、缺失环节及 internal:<字段>、external:Wn 或 candidate:Cn"],
    "service_register": ["逐项登记 SERVICE 的综合金融触发、匹配逻辑及 internal:<字段>、external:Wn 或 candidate:Cn"],
    "major_risk_register": ["逐项登记 RISK 的归一化风险事实、主体、时点、状态、受影响 OPP 和 internal:<字段> 或 external:Wn"],
    "watch_register": ["逐项登记 WATCH 的历史、关联、行业、人物、冲突、弱来源或推断线索及证据状态"],
    "executive_visit_strategy": ["登记支持优先 OPP、关键 RISK、切入点、核验事项和下一步的事实及信息缺口"],
    "financing_need_rows": ["逐行回指 opportunity_register 中同一 OPP，触发事实、用途、时点、强度和证据不得改变"],
    "loan_product_candidates": ["逐项登记所引用的融资需求行、还款来源、增信线索和准入缺口证据"],
    "service_product_candidates": ["逐项登记所引用的 SERVICE、产品匹配逻辑、合作缺口和开场话术"],
    "marketing_sequence": ["逐阶段登记关联 OPP、RISK 及由候选产品与缺口导出的推进动作"],
    "risk_evidence_groups": ["逐组登记实际使用的 internal:B/OV_RISK/OV_TAX/LAND/LIC/HON/FIN_LISTED/OP 或 external:Wn 及主体、时间、状态和范围"],
    "risks": ["逐行回指 major_risk_register 中同一 RISK 及其 affected_opportunity_ids，不以原始响应临场新增或改号"],
    "risk_compliance_context": ["实际使用的 internal:OV_TAX/LIC/HON 字段及其年份、有效期和状态边界"],
    "risk_information_boundary": ["internal:<明细可用性、时间范围、非上市公司财务资料状态及不可合并范围> 或 external:Wn"],
    "risk_interpretation": ["实际进入风险表和合规提示的 internal:<归一化事实> 或 external:Wn"],
    "visit_objectives": ["逐项登记目标对应的 OPP、RISK 和验收条件"],
    "recommended_topics": ["逐项登记话题开场依据和关联 OPP"],
    "visit_questions": ["逐项登记问题依据、关联 OPP/RISK 和答案影响"],
    "document_checklist": ["逐项登记材料与 OPP/RISK、还款、增信或准入缺口的对应关系"],
    "其他 D 文案字段": ["对应 internal:<字段或状态> 或 external:Wn"]
  }
}
```

整理规则：

- `B`、`ID`、`OV_*`、`LAND`、`IND`、`REL`、`FIN_*`、`TM` 至 `OP` 保存对应工具的必要原值；`REL` 必须先删除个人证件号。`WEB.candidates` 保存全部搜索候选和打开状态，`WEB.sources` 保存能打开的页面；除重复、无关、敏感或恶意内容外不删除候选。`D` 保存事实、线索、综合金融机会、风险观察、问题和受约束推断。
- 工商深度成功后，七个业务模块固定显示。`opportunity_register`、`lead_register`、`service_register`、`major_risk_register`、`watch_register` 和 `visit_questions` 共同构成开放线索池。没有直接融资触发时，仍可从经营结构、行业传导、扩张、人员规模、政策、历史事件或模型分析建立 LEAD/SERVICE/WATCH/QUESTION；不得用模拟数据补事实。
- `opportunity_register/lead_register/service_register` 是机会主数据，`major_risk_register/watch_register` 是风险主数据。后续章节按编号引用；发现新证据时可以新增、拆分、合并或重排，但必须同步更新全文引用和审计映射。
- 大章节编号固定为“一、核心观点 → 二、执行摘要 → 三、客户全景画像 → 四、产业画像与行业洞察 → 五、定制化营销方案 → 六、风险预警与合规提示 → 七、拜访建议与话题清单”。客户画像与产业画像必须彼此独立；行业事实表仍可按证据显隐，但不得隐藏、跳号、重号或更名七个大章节；“报告使用说明”不编号。
- `D.has_core_operations` 在工商主体确认后固定为 `true`，用于确保财务数据不足时仍显示业务提示；其他 `D.has_*` 只在对应板块至少存在一项有效内部事实或本 Skill 明确允许的合格外部事实时设为 `true`，不得为了保留版面而设为 `true`。
- `D.source_attributions.<section>.internal_dimensions[]` 列实际提供事实或资料缺口的内部业务维度；`external_source_ids[]` 可以同时登记 `Wn` 与 `Cn`。同一来源可以跨人物、股权、资产、营销、风险与拜访章节复用，不受单一 scope 限制。
- 外部事实所在句末必须附 `[外部：Wn]`；同一事实由多个外部来源支持时附全部 ID，例如 `[外部：W2、W3]`。企业官网自述必须在正文中同时出现“企业官网披露”。内部事实不添加行内 ID，通过章节的“内部：”来源行追溯。
- 基本信息只保留非空字段。展示层的无损格式化仅包括：纯数字整数部分增加千分位；严格匹配 `YYYY-MM-DD` 的日期显示为“YYYY年M月D日”；曾用名中的半角逗号、全角逗号或分号统一为“、”；已知币种代码显示其接口同时返回的中文名称；文档明确为比率的 `IND` 十进制值使用任意精度十进制乘以 100、删除无意义尾零后追加 `%`。必须保留全部有效数字和小数位，不得四舍五入；无法可靠识别时直接显示原值。
- `D.registered_capital_display` 使用无损格式化后的 `regCap` 与 `regCapCur` 组合为“金额单位（币种）”；接口明确 `regCap` 单位为万元时追加“万元”，不得重复单位。实缴资本同理。
- 股东表先展示内部直接股东原值，再展示外部股东、历史股东、穿透关系、实际控制人、最终受益人和一致行动候选。人数不设上限；内部与外部口径分列，推断关系标明依据和置信度。
- 整理为 `D.shareholder_rows[] = {name, holding_display, note, note_source_ids}`。内部比例与认缴额保留原值；可以倒算、合计、穿透和换算，必须显示公式、来源和“派生值”标签。
- `D.has_equity_or_network=true` 在存在内部股东、外部股东候选、历史股东、关系网络、实控人/最终受益人候选或资料缺口时成立。`REL` 和外部页面均可扩展关联主体、持股和控制关系候选，并标明口径与置信度。
- 关键决策人不设数量上限。内部人员、法定代表人、外部管理层候选、历史管理层、股东代表和公开活动中的关键角色均可进入 `D.person_rows[]`，以 `person_origin` 区分来源。
- 人物背景可以来自直接关系页或两跳身份桥接。每项背景登记关系来源、履历来源、身份键、置信度和冲突；企业官网、交易所、原任职机构年报、高校、媒体、百科、社交账号均可采用并按等级标注。
- 内外部职务冲突时分列“内部当前口径”“外部披露口径”和日期，不覆盖、不删除。历史任职、教育、专业、创业、行业经验、公开职责、访谈观点和可能决策角色均可展示；推断的决策角色标为 WATCH/QUESTION。
- 没有外部背景时保留人员并生成针对该人的背景核验问题；仅有弱来源时照常展示并标记低置信度。
- 有形资产与无形资产均全量展示，不设代表项数量上限；分页元数据和实际明细数量分别说明。
- 荣誉资质只展示本报告采纳的代表记录数量，不得称全量，不得使用“返回”描述。
- 舆情不设数量上限，保留标题、日期、来源、情感标签、主体关系和证据状态。目标企业为主体、关联主体、概念股、行业举例、顺带提及、同名可能或纯市场价格波动均可进入不同层级；只有完全重复项去重。
- 企业风险先按“主体与行政合规 → 司法与执行 → 股权及资产权利负担 → 税务与许可合规 → 财务经营关注 → 近期公开事件”六组归一化到 `D.risk_evidence_groups`，再生成 `D.risks[] = {topic, detail, sales_implication, verification}`；禁止让大模型直接读取原始响应临场分类。
- 风险事实只写目标企业自身记录；关联主体、股东或人员记录必须单独标明主体范围，不得并入企业自身失信、执行或债务结论。只有明确大于零的统计、非空且主体范围可确认的风险列表、明确异常的许可或资质状态、选定年度财务记录中的直接负值或合格的目标企业自身负面舆情才能进入风险表。
- 明确为零、纳税评级和许可状态均可进入 RISK/WATCH 或合规观察；零值只能说明对应统计范围内记录数为零，不能证明无风险。
- `D.visit_questions[]` 必须按“经营与计划 → 融资用途 → 金额与期限 → 还款来源 → 现有融资 → 增信资源 → 风险化解 → 合作意愿”的漏斗排序。每个问题都要写明建议沟通对象、已知依据和答案对候选产品的影响；不得预设答案，不得把公开线索写成客户已确认需求。
- `D.coverage_summary` 只用工商登记、关键决策人及公开职业背景、股权与关联关系、上市公司财务、土地及外部设施资产、行业统计与排名、知识产权、备案许可、荣誉资质、纳税评级、近期公开动态、外部企业动态、外部行业背景和近两年风险等业务名称概括资料范围；内部已覆盖内容写“报告已覆盖……”，内部无可展示内容写“公开资料中暂无可供展示的……”，内部失败写“相关资料尚待补充”。`WEB.status="empty"` 时写“外部公开资料未形成可用补充”，`WEB.status="unavailable"` 时写“外部公开资料检索尚待补充”。不得出现企业 ID 解析、工商简项、产品码、工具名、内部别名或原始状态代码。
- “客户全景画像”与“产业画像与行业洞察”可以同时使用内部、外部、候选和模型分析；外部行业定量、竞争对手、上下游、市场与政策信息可以映射为 OPP/LEAD/SERVICE/RISK/WATCH，必须标明从行业到企业的传导假设。
- `D.risk_interpretation` 始终必填；有命中时总结事实、范围、贷款营销影响和需核实事项，无命中时说明资料边界与基础准入材料要求，不评级、不推演未来损失。
- 每个非空 `D` 文案字段都必须在 `EVIDENCE` 中登记来源；内部来源写成 `internal:B/ID/OV_*/LAND/IND/REL/FIN_*/TM...OP.<字段或状态>`，外部来源写成 `external:Wn`。任何 `external:Wn` 都必须能在 `WEB.sources` 找到完整元数据并出现在对应章节的 `D.source_attributions.<section>.external_source_ids[]`。

#### 股权结构与关联关系生成规则

1. 本节展示内部直接股东、外部当前股东候选、历史股东、多层穿透、实际控制人、最终受益人、一致行动、表决权、管理人、出资人、关联交易和控制关系分析，不设层级或数量上限。
2. 内部 `B.shareholderList[]` 原值逐条保留；外部名称、比例、认缴额、出资日期和控制关系作为独立外部口径进入同表或附表。允许计算合计、集中度和穿透比例，但必须展示公式和输入来源。
3. 一级至四级来源、搜索摘要和模型推断均可生成股东或控制关系候选；分别标记证据状态、关系路径、时点和置信度。名称推断、机构性质推断和控制权推断允许进入 WATCH/QUESTION。
4. 历史与当前信息分列；内外部冲突全部保留并标记 `conflicting`，不得删除任何一方。只有完全重复项去重。
5. `D.has_shareholder_notes=true` 在存在任何外部说明、推断、冲突或资料缺口时成立。缺少说明的行显示“暂无补充”，不得隐藏其他行。
6. `D.equity_interpretation` 可以分析集中度、控制权、支持能力、关联交易和治理影响，但必须区分事实、外部口径和模型分析。
7. `EVIDENCE.shareholder_rows` 逐行登记内部、外部或候选证据，包含计算公式、身份桥接、冲突和置信度。

#### 有形资产生成规则

1. `D.tangible_asset_rows[] = {asset_type, fact, boundary, source_ids}`，不设数量上限。土地、建筑、设施、设备、产线、项目、地址、门店、服务网点、分支、展厅、客户现场、招商、产能、经营范围和一般资产宣传均可进入，按证据状态和资产明确程度排序。
2. 直接描述具体资产的进入 FACT；行业、经营范围、注册地址、网站、分支、资本、许可、荣誉、知识产权、招投标、客户项目和一般产品信息可以形成资产 LEAD，不作硬排除。
3. 内部土地记录按页码顺序全量合并；只删除 JSON 内容完全一致的重复对象。每条记录均可成行，并可计算面积、成交价格和抵押金额合计，显示公式、口径和重复处理方法。
4. 土地供应记录按可解析的 `supplyArea` 从大到小排序，面积相同时按有效 `contractDate` 从新到旧排序；土地出让按 `landArea` 从大到小、再按 `pubDate` 从新到旧排序；土地抵押按 `pubDate`、再按 `boardStartDate` 从新到旧排序。排序只决定展示顺序，不删除任何记录或字段，解析值不得替换原值。执行摘要可以引用排序靠前的代表记录，但完整资产表和审计文件必须保留全部记录及全部有值字段。
5. `B` 中的工商抵押、司法协助或其他记录无论是否写明具体抵押物均进入资产或权利负担表；对象不明时标记“资产对象待核验”。
6. 外部有形资产使用 `scopes[]` 包含 `tangible_asset` 的任一来源或候选；主体直接、两跳、间接和歧义关系均可纳入。正文未同时确认企业、资产、角色或时点时降低证据状态并生成核验问题。
7. 外部事实可以展示设施名称、位置、证号、宗地编号、面积、价格、投资额、账面/评估价值、产能、设备数量、抵押金额和权属口径；来源之间分列，企业自述和平台数值注明未独立核验。
8. 企业官网内容必须写“企业官网披露”，并在 `boundary` 写明“企业自述仅确认公开披露的设施或使用场景，不证明产权、租赁关系、账面价值或当前状态”。政府、监管、规划或交易所页面只确认其直接披露的审批、备案、建设、交易或公告节点；未明确完工、投产、使用或持有时不得升级状态。
9. 历史外部页面必须保留原始日期并写成“于{日期}披露/备案/公告”；不得据此使用“现有”“目前”“正在”“已投产”等当前时态。外部来源之间或与内部记录冲突时优先直接一级原始页面作为主口径，同时完整保留其他口径并列写入 `boundary`，不由模型选择性删除产权、面积或状态信息。
10. 地址、行业、经营范围、门店、服务网络、终端数量、分支、展厅、客户现场、合作园区、产品交付、订单、融资、荣誉、招商、“建设基地”“计划投资”和“拟购置设备”均可进入资产线索；不证明产权或当前状态时明确标为 LEAD。
11. 土地供应、土地出让只称“公开土地记录”或“涉及土地供应/土地出让”，不得称为当前产权、当前持有土地或自有土地；土地抵押和具体抵押物只说明公开登记事实，不得推导当前仍有效、已经解除、资产价值或企业偿债能力。不得用任何内部或外部事实推导“轻资产”“重资产”“自有房产”“自有厂房”或“资产实力”。
12. `D.has_assets=true` 仅在 `D.tangible_asset_rows` 至少一行，或任一无形资产事实非空时成立。有形资产没有合格事实、但存在无形资产时，仅显示无形资产；两者均为空时隐藏整个资产章节。不得为了保留“有形资产”标题输出空段、通用边界句或“暂无记录”。
13. `D.assets_interpretation` 接收全部资产事实、线索、地址、经营范围、行业、注册资本、项目宣传、估值和资料缺口，按证据状态分层解释。
14. `EVIDENCE.tangible_asset_rows` 逐行登记 `internal:LAND/B.<字段>`、`external:Wn` 或 `candidate:Cn`、主体、日期、对象、边界、计算和证据状态；空结果、失败状态和未打开候选也可支持资料缺口或 QUESTION。

#### 产业画像生成规则

1. “产业画像与行业洞察”是独立且固定显示的大章节，位于“客户全景画像”之后。`D.has_industry_insight=true` 仅表示存在超出工商行业归属的有效内部行业事实或合格外部行业背景，不控制大章节显隐；资料不足时仍填写 `D.industry_positioning`、`D.industry_business_model_interpretation` 和 `D.industry_information_boundary`，把行业经营机制写成待企业确认的访谈假设，不生成事实表。
2. 模块固定按“产业链位置与经营模式 → 行业周期与资金占用 → 行业对标与经营参照 → 政策与融资环境 → 行业风险与贷款启示”组织。每个结论遵循“已核实行业事实 → 可能的经营现金流传导 → 企业专属核验事项 → 对贷款用途、期限、还款或增信结构的条件式启示”；不得把行业常识直接改写为企业事实或贷款需求。
3. 用内部行业、经营范围、REL、外部页面和模型分析生成产业链定位。可以列示上中下游、供应商、客户、经销商、采购销售额、账期和集中度；直接事实、间接线索与模型推断分列。
4. 确定性生成 `D.industry_scope_display`，统一供行业周期、行业对标和行业风险表使用：
   - 中文地区名优先使用与所选行业记录一致、含中文且不含对应 `regionId` 代码片段的 `IND.indLocOpr.data[].region`；该字段缺失或夹带内部编码时，只有当查询的省级 `region_id` 确由同一主体的 `B.basicList[0].regOrgCode` 构建，或行业记录的 `regionId` 与查询范围一致时，才使用 `B.basicList[0].regOrgProvince`。不得根据行政区划代码自行猜测地区名。
   - 中文行业名优先使用与所选行业记录一致、含中文且不含对应 `nicId` 代码片段的 `IND.indLocOpr.data[].indsy`；该字段缺失或夹带内部编码时，只有当三级 `nic_id` 确由同一主体的 `B.basicList[0].industryCode` 构建，且 `B.basicList[0].industry` 按半角连字符 `-` 切分后至少有三个非空层级时，才使用第三级中文名称。不得使用互联网、模型记忆或样例映射行业代码。
   - 同时取得中文地区名和中文行业名时直接拼接；行业名以“行业”或“业”结尾时不再追加，其他名称追加“行业”。例如地区为“安徽省”、三级行业名为“输配电及控制设备制造”时，固定显示“安徽省输配电及控制设备制造行业”。
   - 只有中文地区名时显示“{地区}相关三级行业”；只有中文行业名时显示“{行业名按上述后缀规则处理}”；二者都无法核验时显示“相关三级行业”。不得为追求完整而猜测名称。
5. `IND.query_scope.region_id/nic_id` 及各行业记录的 `regionId/nicId` 仅用于查询、范围一致性核验和 `EVIDENCE`，禁止进入最终报告。不得显示“三级行业C382”“行业代码 C382”或在中文行业名后括注内部编码。
6. `financialRegionRank` 和其他行业数据全量展示有效及缺失记录，可计算企业数变化、市场结构、增长率和景气观察；所有计算显示期间、范围和公式。
7. `locfin.data[]` 全量保留并展示全部记录、字段、零值、缺失值、异常值和冲突值；分别标记 `valid|zero|missing|anomalous|conflicting`。金额保留“万元”单位和原始精度，比率按精确百分比规则展示。没有年度字段时固定标注“时间未标明；以{D.industry_scope_display}范围为准”，跨口径比较必须同时显示不可比边界。
8. `property.data[]` 全量保留全部排名、行业平均值、知识产权维度和 `*RankFour` 字段。有效正整数可直接进入行业对标；零值、空值、非正整数、未知四分位定义或异常值进入 WATCH/QUESTION，并保留原字段名、原值和口径限制，不因无法解释而省略。
9. `indLocOpr.data[]` 全年度、全指标展示，不设行数上限；零值、正值、缺失和冲突均可进入行业观察，并注明不能由零值证明无风险。
10. `D.industry_cycle_rows[]` 接收内部、外部、候选和模型分析中的全部周期、季节、库存、账期、回款和资本开支信号；缺项不阻止成行。
11. `D.industry_benchmark_rows[]` 接收跨年度、跨地区、跨口径的内部与外部排名、竞争对手、营收、销量、产能、市场份额和评价；必须显示可比性差异和来源口径。
12. `D.industry_policy_rows[]` 接收现行、历史、拟议、政府、媒体、协会、平台和摘要中的政策或融资环境线索；标明有效期、适用范围和证据状态。可以分析企业可能适用性和申报路径，但不得把分析写成银行正式审批结果。
13. `D.industry_risk_rows[]` 接收内部、外部、候选摘要和模型分析中的全部行业风险；即使缺少传导或企业指标也保留该行，并把缺项转为核验问题。
14. `D.industry_external_context` 接收所有行业来源和候选，可展示市场规模、CAGR、市场份额、竞争对手经营值、上下游名单及对企业的映射；外部事实与模型映射分列。
15. 行业事实可以单独形成 LEAD、SERVICE、WATCH，也可以形成观察级 OPP 或产品探索建议；缺少企业专属事实时标明“行业到企业的传导假设”和需核验条件。
16. `EVIDENCE.industry_*` 逐项登记实际进入表格和文案的 `internal:B/IND` 字段、采用年度与地区行业范围及 `external:Wn`；`EVIDENCE.industry_scope_display` 同时登记中文地区名、中文行业名的内部来源字段和仅用于一致性核验的代码字段。未显示的排名、平均值、比率、空结果、失败状态和未采用网页不得作为行业结论证据。每行行业表都必须能够回指最小事实证据、范围和期间。

#### 核心经营数据生成规则

开放纳入模式下，本节后续关于“只使用某内部年度报告、不得展示外部值、不得估算、不得计算”的限制均改为口径分层要求，不构成排除。内部、法定披露、企业自述、媒体、平台、行业参照和模型估算均可展示；每行增加“来源口径｜报告期｜证据状态｜计算/估算方法”。

1. “核心经营数据”展示所有可获得的财务、经营、员工、客户、渠道、融资、资产、负债、现金流、产销、库存和行业参照数据。直接事实与估算值分表或分列，模型估算不得使用虚构输入。
2. 从 `FIN_LISTED.mainfinadata.data.mainfinadataInfo[]` 中筛选 `reportDate` 严格匹配 `YYYY-12-31`、`reportTimeType` 明确为“年度报告”、`reportDate` 不晚于数据日期，且 `operateIncome/totalOperateReVe/parentNetProfit/cutParentNetProfit/netOperateCashFlow/sumAsset/sumLiab/roeWeighted` 至少一个非空的记录。按 `reportDate` 从新到旧选择最新年度；不得把一季度、半年度、三季度或单季度记录当作年度数据。
3. 同一 `reportDate` 存在多条记录时全部保留；可以标记首选口径，但冲突字段必须并列展示，不得隐藏。
4. `operateIncome` 非空时作为营业收入；仅当其为空时使用 `totalOperateReVe`，不得同时展示为两个收入指标。其余指标按“归属于母公司股东的净利润 → 扣除非经常性损益后归属于母公司股东的净利润 → 经营活动产生的现金流量净额 → 资产总计 → 总负债 → 加权平均净资产收益率 → 营业收入同比 → 归母净利润同比”的顺序整理。
5. `FIN_LISTED.rgbalance` 的合并、母公司、季度、半年度和年度记录全部可以展示；报告期与合并口径分列，不混算时点不同的数据。
6. 金额与币种严格使用同一条记录的原值；整数部分只增加千分位，不换算为万元、亿元，不舍入或补零。`currency` 为已知代码时显示中文币种名称，未知代码保留原值；没有币种时不得自行补写“元”。`roeWeighted/iRobrIncreaseRate/toiYoyRatio/dpNpYoyRatio` 为有效数字时保留原值并直接追加 `%`，不得乘以 100。
7. `FIN_KEY.coreLndicatorInfo[]` 全部记录和字段进入相应口径；`empNum`、`socialSecurityNum` 分列，金额字段缺少期间或单位时仍展示并明确“期间/单位待核验”。
8. `D.core_operation_rows[] = {metric, value, period_basis}`。每个非空指标单独成行；`period_basis` 必须写明选定年度报告日期、报告类型和币种，资产负债补充项另写“合并资产负债表”，员工信息写“{reportYear}年度公开员工信息”。`D.has_core_operation_rows` 仅在至少存在一行时设为 `true`。
9. 有表格时，`operations_boundary` 固定说明“以下数据来自{reportDate}年度报告，金额、比率及币种按公开资料原值展示，不同报告期不可直接混同比较。”；存在冲突、字段缺失或使用合并资产负债补充时追加对应事实边界，不使用“接口”“返回”“查询”等技术措辞。
10. 没有符合条件的内部或法定年度报告时，继续使用企业自述、媒体、平台、行业参照和模型估算形成经营数据线索表，`D.has_core_operation_rows=true`；每项注明“非审计口径/待核验”。完全无数值时展示资料缺口和现场取数清单。
11. 有表格时才生成 `operations_interpretation`，按“所选年度核心指标事实 → 可见同比或现金流信号 → 拜访核验方向”组织。只解释表格已展示数据，不计算利润率、资产负债率、增长额或其他派生指标，不作经营健康、偿债能力、行业地位、风险等级或授信判断。
12. `EVIDENCE.core_operation_rows` 逐行登记选定记录、选取规则、实际字段、报告日期、报告类型、币种和必要的合并口径；`EVIDENCE.operations_boundary` 登记年度报告选择结果或无有效年度报告状态；`EVIDENCE.operations_interpretation` 只登记已展示表格行。样例企业实测数据不得写入 Skill、证据模板或固定文案。

#### 企业风险与合规证据生成规则

1. 构建 `D.risk_evidence_groups`，顺序为“主体与行政合规 → 司法与执行 → 股权及资产权利负担 → 税务与许可合规 → 财务经营关注 → 交易条款 → 关联方与治理 → 行业与市场 → 近期公开事件”。每组保存 `{status, facts[]}`；每条 `fact` 至少包含 `subject`、`fact_type`、`detail`、`period_or_date`、`current_status`、`source_scope`、`detail_available`、`evidence_state`、`confidence` 和 `relationship_path`。缺失项保持空值并转为核验问题。`status` 允许：
   - `hit`：存在可进入风险表的明确事实；
   - `context`：只有纳税评级、有效许可等合规背景，或只有财务资料边界；
   - `empty`：对应工具成功且该组明确无可展示记录；
   - `unavailable`：工具失败、未调用或无法确认主体。
2. 主体与行政合规使用 `B.basicList[0].orgStatus`、`exceptionList`、`illegalList`、`caseInfoList`、`liquidations`，以及许可、资质中明确写明撤销、吊销、注销、暂停、失效、过期、异常或整改的记录。主体状态正常、列表为空或许可明确有效只作为背景，不生成“合规良好”“无行政风险”等结论。
3. 司法与执行同时接收 `OV_RISK.list[0]`、`B.dishonestList`、`executedList`、法院/监管页面、媒体、平台和搜索摘要。主体自身、人员、股东、历史股东及关联主体分别标注关系路径；目标企业直接记录进入 RISK，其他主体记录进入 WATCH。统计与明细分列，可提供去重前总量、去重后事项数及去重方法，但不静默覆盖冲突值。
4. 股权及资产权利负担使用 `B.sharFrozList`、`sharePledgList`、`mortReg`、mortgage、judicial aid 和 `LAND.tddy.records[]`。股东质押记录写成“股东股权质押”，不得写成企业自身债务；股权冻结、司法协助和同一案号、金额、日期对应的记录可能指向同一事项，只分别说明各列表列示数量，不得相加为风险总数。没有明确注销、解除或当前状态时，只写登记日期、期限和公开状态，不得写“当前有效”“已经解除”。
5. 税务与许可合规接收内部记录、税务/监管原始公告、媒体、平台和摘要线索；历史评级、欠税、许可状态和冲突口径均展示。原始公告进入 RISK，单一媒体或平台进入 WATCH，摘要进入 QUESTION。
6. 财务经营关注同时接收内部财务、法定披露、企业自述、媒体数值、平台数值和模型测算。各口径分列并可计算派生比率、趋势和压力情景；所有计算显示公式、输入和口径，外部或推算结果不得冒充内部审计数据。
7. 交易条款组接收关联交易、定价、付款、账期、退货、退款、回购、担保、质押、排他、终止、违约、验收、付款义务人和回款账户等事实或线索；凡可能改变第一还款来源、现金流闭环或授信结构，均可形成 RISK 或 WATCH。
8. 关联方与治理组接收股东、历史股东、实控人候选、管理层履历、跨界经营、关联主体债务、控制权冲突、关键人依赖和决策链不清等事实或分析；行业与市场组接收需求、价格、库存、渠道、竞争、政策和区域风险。直接事实进入 RISK，间接或分析性内容进入 WATCH。
9. 近期公开事件接收所有内部舆情、外部正文、搜索摘要、行情、概念股、行业评论、顺带提及和无详情标题；按主体关系与证据状态分层，不作硬排除。
10. 九组整理完成后，所有 `hit` 事实进入 `major_risk_register`，所有 `context`、间接、历史、行业、人物、冲突、弱来源和模型推断进入 `watch_register`。不设数量上限；仅完全重复项去重。允许输出严重、高、中、低、观察等分析等级，但必须同时显示评级依据和非审批结论边界。
11. `D.risk_compliance_context` 汇总内部和外部税务、许可、资质背景及冲突；没有事实时登记资料缺口。
12. 近两年统计中的明确数字 `0`、空字符串、`null`、失败和未调用均可作为资料状态进入说明或 QUESTION，但不得把非零未知改写为零。
13. `D.risk_interpretation` 接收全部风险组、RISK、WATCH、资料缺口、冲突和模型分析，按“事实/线索 → 主体与时点 → 可能影响 → 核验材料”生成。
14. `EVIDENCE.risk_*` 逐组、逐行登记 `internal:<字段>`、`external:Wn` 或 `candidate:Cn`；统计与明细不一致、跨列表重复、内外部冲突和状态未知均保留并显式展示。

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
4. `entScaleName` 与 `groupName` 均可进入核心观点；集团归属属于内部字段时直接陈述，属于外部或推断时标明口径与置信度。
5. `industry` 非空时按半角连字符 `-` 切分：至少三层时只保留前三层并用 `-` 连接，不足三层时保留完整原值；拼接“，所属行业为{行业}”。
6. `regCap` 非空时拼接“，注册资本{无损格式化后的regCap}万元”；`regCapCur` 非空时按无损格式化规则追加币种。`paidInCap` 非空时拼接“，实缴资本{无损格式化后的paidInCap}万元”。字段已带单位时不得重复追加单位。
7. 片段末尾追加“。”。

#### 4.2 上市、退市或融资片段

1. 合并 `OV_MARKET.data[0].listed[]`、`deListed[]` 和 `investmentFin[]`；三类记录同时存在时全部保留，分别标记上市、退市和股权融资口径，不因任一列表非空而忽略其他列表。
2. 上市、退市记录按 `listdate` 原值升序排列。上市记录拼接“企业于{listdate}在{trademarket}上市”；退市记录拼接“企业于{listdate}从{trademarket}退市”；`securitycode` 非空时追加“，股票代码是：{securitycode}”。
3. 无论是否存在上市或退市记录，都按接口顺序处理 `investmentFin[]`：
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

#### 4.7 生成贷款营销核心观点

`D.core_viewpoint` 不是企业简介，而是客户经理在 30 秒内应掌握的贷款营销判断。固定按下列顺序组织，缺少证据的条件项不补造：

```text
D.core_viewpoint =
    客户身份、业务基础与经营阶段
    + 优先 OPP 的融资触发
    + 对应贷款需求场景与可能用途
    + 可能还款来源和增信资源边界
    + 相关 RISK 准入约束
    + 本次拜访目标
```

1. 首句直接使用已验收的 `D.core_internal_baseline`，再选择 1 至 2 项 `D.core_capability` 解释业务基础；不得用宣传称号替代经营事实。
2. 先完成全部开放台账再生成核心观点。核心观点引用所有高相关 OPP/LEAD/SERVICE/RISK/WATCH；正文过长时概括分组并列出完整编号范围，后文保留全量明细。
3. `D.core_financing_trigger`、用途、时点和边界必须与所引 OPP 的主数据完全一致；`D.core_risk_constraint` 必须与所引 RISK 的事实和影响一致。核心观点不得创造执行摘要未登记的机会或风险编号。
4. `D.core_repayment_logic` 优先使用可核验的主营经营回款、合同/订单回款或项目经营现金流线索；`D.core_credit_support` 只列内部土地抵押、明确资产对象、应收账款、保证主体或交易闭环等待核验资源。不能确认时写“第一还款来源/增信可用性待结合材料核实”，不得把注册资本、地址、知识产权数量或公开设施直接认定为担保物。
5. `D.core_risk_constraint` 可以使用 RISK、WATCH、资料缺口和模型分析，说明其可能影响产品准入、担保结构、资料要求或推进顺序；允许给出分析等级，但不得冒充银行审批结论。
6. `D.core_visit_focus` 必须落到需求金额、贷款用途、期限、还款来源、现有融资、增信资源、风险事项当前状态和决策流程中的 2 至 3 项。
7. 全文 260 至 420 字、5 至 8 句。外部事实逐句附 `[外部：Wn]`；`EVIDENCE.core_*` 与 `source_attributions.core` 必须逐句闭环。核心观点可以提出“首选从某产品族场景切入”，但必须同时出现“待核验”边界，禁止承诺授信结果。

#### 4.8 从零构建执行摘要与开放编号台账

执行摘要是全文决策索引，固定回答“客户有什么特征、有哪些可谈的贷款机会、什么风险会阻断这些机会、本次怎样推进”，不得写成五段散文式结论。

1. 先生成 `D.executive_core_features`，用 2 至 4 项已核实事实概括客户身份、经营阶段、近期关键转折和贷款营销价值，80 至 160 字；至少一项来自内部主体事实。不得在本段提前推荐产品、作授信判断或重复机会表。
2. 从内部事实、外部正文、搜索摘要、行业机制、品牌荣誉、注册资本、员工数量、扩张计划、招聘、门店、产能、政策、历史事件和模型分析中全量构建机会候选。贷款或融资路径较明确者进入 `OPP`；缺少用途、金额、期限、承担主体或还款闭环者进入 `LEAD`；存款、结算、现金管理、票据、收单、代发、个人金融、银行卡、托管、跨境、投行、保险等进入 `SERVICE`。
3. 每个 OPP/LEAD/SERVICE 完整记录触发信号、可能产品、时点、证据状态、置信度、缺口和证据 ID。允许 `仅摘要`、`模型推断` 和 `未知`，缺失字段转成核验问题，不阻止创建编号。
4. 不设数量上限。同一触发事实支持不同用途、产品、客户角色、还款路径或业务团队时可以拆分；完全相同的重复项才合并。分别按 `OPP-01...`、`LEAD-01...`、`SERVICE-01...` 连续编号，并在全文保持稳定。
5. `opportunity_register`、`lead_register` 和 `service_register` 共同构成机会主数据。营销方案、推进路径、推荐话题、拜访问题和资料清单可以引用任一编号；贷款产品候选对应 OPP/LEAD，综合金融方案对应 SERVICE。
6. 所有直接风险事实进入 `major_risk_register`，所有历史、关联、行业、人物、治理、弱来源、冲突和推断性风险进入 `watch_register`。不设数量上限，分别连续编号 `RISK-01...` 与 `WATCH-01...`，允许显示分析等级及依据。
7. 每个 RISK/WATCH 填写主体、时点、来源、证据状态、可能影响、关联 OPP/LEAD/SERVICE、核验方向和证据 ID；无法绑定具体机会时标记企业级或行业级。
8. `major_risk_register` 与 `watch_register` 共同构成风险主数据。风险章节、问题和材料可以引用两类编号，事实与推断必须分列。
9. 生成 `D.executive_visit_strategy`，覆盖优先 OPP、值得追问的 LEAD、可快速切入的 SERVICE、必须先处理的 RISK 和需温和核实的 WATCH；不限制条目数量，但摘要正文优先展示相关性最高的项目并指向后文全量台账。
10. 执行摘要展示完整编号台账；外部正文附 `[外部：Wn]`，摘要候选附 `[候选：Cn｜正文未核验]`，模型推断附“模型分析假设”。

#### 4.9 保留客户全景画像

“客户全景画像”保持独立，不与产业画像合并，不追求企业大事记或资料堆砌。各小节的 `*_interpretation` 必须把客户事实翻译成贷款营销核验含义：

1. 企业基本信息：说明业务主体、经营阶段和贷款主体核验重点，不把注册资本解释为偿债能力。
2. 关键决策人：识别本次应沟通的经营、财务、采购、项目和法务角色；职务与决策权限未知时明确待确认。
3. 股权结构：说明直接股东与可能的担保/支持核验对象，不推断实际控制人、支持意愿或代偿能力。
4. 企业资产：区分“公开资产线索”和“可用于增信的合格资产”。只有权属、价值、可处分性、是否已抵质押均经材料核验后，才能进入正式担保方案。
5. 核心经营数据：围绕营业收入、现金流、资产负债和员工等已展示事实说明还款来源核验重点；没有可靠财务数据时列出近三年财务报表、纳税申报和银行流水等资料需求。
6. 本模块不得引入行业景气、产业链通用结构、市场容量、政策支持或竞争对手数据；这些内容只进入下一独立模块“产业画像与行业洞察”。

#### 4.10 生成产业画像与行业洞察

本模块站在银行客户经理贷款营销视角，不写百科式行业综述，而是把行业资料转化为可验证的融资讨论入口：

1. 先写“产业链位置与经营模式”：只用企业行业归属与经营范围定位经营环节，说明常见采购、生产、库存、销售和回款机制，并把未获企业证实的内容明确标为访谈假设。
2. 再写“行业周期与资金占用”：选择能够解释备货、库存、账期、订单履约、回款或资本开支的事实，逐项给出现金流传导路径和企业专属核验指标；不以市场规模或增长口号代替现金流分析。
3. 再写“行业对标与经营参照”：仅用同地区行业范围、同期间、同指标口径的内部排名或均值，解释企业应补充何种经营材料以及贷款结构需要验证什么；不做异口径竞争对手排行榜。
4. 再写“政策与融资环境”：只采用现行有效官方政策，说明政策适用条件、企业待核验资格和对融资沟通的辅助作用；不得将行业支持政策等同于企业获贷资格。
5. 最后写“行业风险与贷款启示”：按“风险事实 → 销量/毛利/库存/应收/现金流传导 → 企业核验 → 用途/期限/还款/增信启示”展开，不输出空泛行业风险口号。
6. 行业事实既可提供产品设计背景，也可独立形成 LEAD、SERVICE、WATCH 或观察级 OPP；缺少企业专属融资触发和第一还款来源时，标明传导假设和待核验条件。

#### 4.11 生成定制化营销方案

先汇总 OPP、LEAD、SERVICE，再生成贷款与综合金融产品候选，最后生成推进路径。允许从行业、经营范围、人员规模、扩张、历史事件和模型分析形成低置信度候选，但必须显示推断链和核验缺口。

1. `financing_need_rows` 不是二次识别机会，而是 `opportunity_register` 的逐项深化视图；必须保持相同 OPP 顺序和完整编号集合，并增加 `verification_focus`。不得在营销章节新增、删除、换号或改变触发事实、用途、时点和证据强度。
2. 每条 OPP/LEAD/SERVICE 记录“编号 → 触发事实/信号 → 可能用途或服务 → 时点 → 证据状态 → 核验重点”。缺少直接触发时照常成行并标记 `模型推断/仅摘要/待发现`；仍禁止虚构或模拟客户数据。
3. 每个 OPP/LEAD 可以生成一个或多个 `loan_product_candidates`，每个 SERVICE 可以生成一个或多个 `service_product_candidates`，均不设数量上限。优先级允许“首选、备选、观察、探索”；缺少第一还款来源时标为“观察/探索”。产品族映射包括但不限于：
   - 日常经营、采购备货、季节性周转 → 流动资金贷款或循环额度贷款；
   - 明确订单/合同履约 → 订单融资；
   - 明确应收账款和付款义务人 → 应收账款融资或供应链融资；
   - 新建、改扩建、长期建设项目 → 固定资产贷款或项目贷款；
   - 明确设备购置或技术改造 → 设备更新贷款；
   - 明确并购交易 → 并购贷款。
   不完全满足场景时可以提出探索性匹配，必须列明缺口和替代方案。
4. 每项候选写出 `fit_logic`、`possible_repayment_source`、`possible_credit_enhancement`、`qualification_gaps` 和 `opening_pitch`。字段缺失时写“待发现/待核验”，不阻止提出首选、备选、观察或探索方案；模型假设必须显式标注。
5. 未指定目标银行时只写通用产品族。指定银行时，具体产品名称、用途、期限、担保方式和材料要求只采信该银行官方资料或用户提供的产品文档，并在正文标注来源；公开条件不等于客户已经满足。
6. `marketing_sequence` 固定为“本次拜访 → 拜访后 3 个工作日 → 后续推进”，每阶段必须填写实际推进的 `related_opportunity_ids` 和需先处理的 `related_risk_ids`，再写目标、动作和退出条件。不得引用主台账外编号，不得用短中长期套话替代可执行动作。
7. 主动推荐与线索匹配的存款、代发、个人金融、银行卡、收单、现金管理、票据结算、托管、跨境、投行、保险和其他综合金融产品，并与贷款机会分栏展示。

#### 4.12 生成风险预警与合规提示

1. 保留六组归一化风险证据。风险表使用“风险编号｜影响机会｜关注事项｜已核实事实与边界｜对贷款营销的可能影响｜现场核验与缓释方向”。
2. `D.risks[]` 与 `watch_register` 分别深化 RISK 和 WATCH；可以来自事实、上下文、历史、关联、行业、摘要、冲突或模型分析。允许条件式分析准入影响和风险等级，但不得写成银行已经拒绝或必然审批结果。
3. 明确零值、纳税评级、有效许可和资料缺口继续放在表后边界说明，不得据此生成低风险或合规结论。
4. `risk_interpretation` 回答三件事：哪些是已发生事实、哪些当前状态待核实、客户经理在介绍贷款前应先取得什么证明或化解材料。

#### 4.13 生成拜访建议与话题清单

1. `visit_objectives` 不设数量上限，覆盖所有 OPP、LEAD、SERVICE、RISK、WATCH 和关键 QUESTION。
2. `recommended_topics` 不设数量上限；每项关联至少一个开放台账编号，并说明如何从事实或线索转入金融需求。
3. `visit_questions` 不设数量上限，按漏斗顺序排列；所有开放台账条目至少有一个核验问题，重要 OPP 至少覆盖用途、金额期限和还款来源。
4. `document_checklist` 不设数量上限，可列完整授信、交易、人员、股权、资产、合规和经营资料清单，并关联开放台账编号。
5. `taboo_notes` 生成 2 至 4 项，至少包括不承诺额度/利率/审批结果、不把公开线索当成客户确认、不用敏感负面细节直接压迫客户。

### 5. 生成大模型派生文案

先完成内部原值、外部候选、来源正文、风险归一化和事实表，再按“内部主体描述 → OPP/LEAD/SERVICE → RISK/WATCH → 核心观点 → 执行摘要 → 逐项营销方案 → 风险深化 → 按编号生成拜访脚本”的顺序生成。发现新证据时允许重建台账并同步全部编号引用。

质量要求：

- 每个结论都必须属于“已知事实、营销假设、待核验事项”之一；三者不得混写。营销假设必须同时给出事实依据和验证方法。
- 核心观点回答“为什么现在谈贷款”；执行摘要回答“谈什么、受什么约束”；客户全景画像回答“客户自身有哪些已核实事实”；产业画像与行业洞察回答“行业机制如何可能影响资金占用与贷款结构”；营销方案回答“用什么产品族切入”；风险回答“先核实什么”；拜访清单回答“现场怎么推进”。
- 禁止虚构和模拟填充；允许有来源的客户数量、外部财务值、行业均值、派生计算和模型估算进入报告，必须展示来源、公式、假设、证据状态和非事实边界。样例企业内容不得当作目标企业事实。
- 禁止使用“优质客户、授信空间大、建议授信、预计可批、风险可控”等审批式结论；产品候选统一写成“营销方向/待核验”。
- 未能说明贷款用途或第一还款来源时仍可给出探索性产品，必须列出缺口和核验问题。
- 所有外部正文附 `[外部：Wn]`，候选摘要附 `[候选：Cn]`，模型分析附“模型分析假设”。无法绑定直接证据的内容进入 LEAD/WATCH/QUESTION，不删除。
- 大模型不得更改 `B`、`ID`、`OV_*`、`LAND`、`IND`、`REL`、`FIN_*`、`TM` 至 `OP` 原值、`WEB` 元数据、事实白名单、风险分组、事实表格或条件布尔值。

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
> 11. 每个来源区先按实际使用的内部维度判断是否输出固定内部来源行，再按正文首次引用顺序输出外部来源。外部事实必须带 `[外部：Wn]`，内部证据模型仍须能用同一 ID 解析到网站、标题、发布日期、访问日期和原始链接；报告可见外部来源行只展示来源 ID、网站名称、发布日期和链接，不展示标题与访问日期。不得输出未被正文引用的网页。
> 12. 骨架中的 `<p align="center">—————————————————数据来源————————————————</p>` 是来源分隔线语义标记。Markdown 回退保留该居中标记；PDF 或 DOCX 排版时必须转换为下方规定的全宽居中分隔组件，禁止作为普通左对齐正文段落或依赖空格定位。

```markdown
# 客户访前一页纸（贷款及综合金融营销版）

报告编号：{{META.report_id}}  ｜  生成时间：{{META.generated_at}}  ｜  密级：机密

客户名称：{{B.basicList[0].orgName}}{{#if D.brand_name}}（品牌：{{D.brand_name}}）{{/if}}

## {{D.section_numbers.core}}、核心观点

{{D.core_viewpoint}}

<p align="center">—————————————————数据来源————————————————</p>

内部：水滴征信 MCP｜数据日期：{{META.generated_at}}
{{#eachSource WEB.sources|ids=D.source_attributions.core.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜链接：{{url}}{{/eachSource}}

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
{{#eachSource WEB.sources|ids=D.source_attributions.summary.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜链接：{{url}}{{/eachSource}}

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
{{#eachSource WEB.sources|ids=D.source_attributions.people.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜链接：{{url}}{{/eachSource}}
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
{{#eachSource WEB.sources|ids=D.source_attributions.equity.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜链接：{{url}}{{/eachSource}}
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
{{#eachSource WEB.sources|ids=D.source_attributions.assets.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜链接：{{url}}{{/eachSource}}
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
{{#eachSource WEB.sources|ids=D.source_attributions.industry.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜链接：{{url}}{{/eachSource}}

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
{{#eachSource WEB.sources|ids=D.source_attributions.marketing.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜链接：{{url}}{{/eachSource}}

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
{{#eachSource WEB.sources|ids=D.source_attributions.risk.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜链接：{{url}}{{/eachSource}}

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
{{#eachSource WEB.sources|ids=D.source_attributions.visit.external_source_ids}}外部：{{source_id}}｜{{site_name}}｜{{#if published_at}}发布日期：{{published_at}}{{else}}发布日期：未标明{{/if}}｜链接：{{url}}{{/eachSource}}

## 报告使用说明

- 报告目的：本报告用于对公客户经理贷款营销访前准备；融资需求、产品方向、还款来源与增信资源均为待核验假设，不作为授信审批依据。
- 信息真实性：报告依据生成时点的公开信息形成；资料缺失或尚待补充不等同于不存在相关事实，建议在拜访中核实关键信息。
- 数据时效性：报告生成后如发生重大变化，建议重新生成报告。
- 保密义务：本报告涉及企业信息，接收方应按所在机构制度妥善保管，未经授权不得对外泄露。
```

### 标题白名单

最终报告只能出现骨架中实际存在的标题，标题名称必须逐字使用，禁止同义替换：`核心观点`、`执行摘要`、`核心特征`、`主要机会`、`主要风险`、`拜访建议`、`客户全景画像`、`（一）企业基本信息`、`（二）关键决策人信息`、`（三）股权结构与关联关系`、`（四）企业资产状况`、`（五）核心经营数据`、`产业画像与行业洞察`、`（一）产业链位置与经营模式`、`（二）行业周期与资金占用`、`（三）行业对标与经营参照`、`（四）政策与融资环境`、`（五）行业风险与贷款启示`、`定制化营销方案`、`（一）融资需求线索`、`（二）贷款产品候选`、`（三）推进路径`、`风险预警与合规提示`、`拜访建议与话题清单`、`（一）本次拜访目标`、`（二）推荐话题`、`（三）关键问题`、`（四）建议取得的资料`、`（五）禁忌提示`、`报告使用说明`。

## 文档生成

默认 `--format pdf`。先完成统一证据模型、`D` 派生文案、`EVIDENCE` 映射和语义验收，再形成完整 Markdown，最后排版为 PDF。

PDF 是唯一版式验收基准。优先沿用当前环境中最近一次已验收成功的生成路径；没有既有路径时优先直接生成 PDF，直接生成不可用时才使用 DOCX 中转。同一任务中不得因分页不理想在多个渲染器之间反复切换。不同格式必须复用同一证据模型、派生文案和条件删除结果。

### 固定版式

- 页面：Letter，215.9 × 279.4 mm；上、下页边距 20 mm，左、右页边距 25 mm。
- 正文：宋体或可用的等价中文宋体，10.5 pt，固定行高 15 pt；表格正文 9 pt，固定行高 12 pt。不得使用渲染器默认行高或单倍行距。
- 标题：黑体或等价中文黑体；主标题 18 pt 黑色居中，一级标题 14 pt、二级标题 12 pt，章节标题蓝固定为 `#4F81BD`。所有 `##` 一级标题段前 12 pt、段后 6 pt；标题位于页首时不额外增加段前空白。
- 元信息：报告编号、生成时间、密级使用 9 pt、固定行高 12 pt 并居中；客户名称使用 12 pt 加粗居中。
- 数据来源：板块末尾加入灰色 `#808080` 来源分隔组件。组件宽度必须等于当前正文可用宽度 165.9 mm，“数据来源”文字的水平中心必须与正文可用区域中心重合，左右线段等长；文字两侧各保留 4 mm 间距，线宽 0.5 pt。禁止把连续破折号作为普通左对齐段落，也禁止用空格、制表符或可变字符数模拟居中。ReportLab 使用自定义 `Flowable` 或无边框三列全宽表格实现，标题列居中、左右线段列等宽；DOCX 或其他渲染器使用等效的全宽三段式组件。内部行固定使用“内部：水滴征信 MCP｜数据日期：{generated_at}”，不得在 MCP 后添加业务维度括注；外部行固定使用“外部：Wn｜网站名称｜发布日期：日期或未标明｜链接：URL”，不得展示页面标题和访问日期。每条来源单独成段，使用 9 pt、固定行高 12 pt、常规字重；长 URL 允许自然换行，不得截断链接或压缩字号。页面标题和访问日期仍须保留在 `WEB.sources` 与内部验收记录中。
- 报告使用说明正文：严格复用参考成品样式。四条说明各自作为独立项目，使用实心圆点 `•`，宋体或等价中文宋体常规字重，9 pt，固定行高 12 pt，文字和圆点统一为灰色 `#666666`（RGB `102, 102, 102`），左对齐且不作首行缩进；圆点左边缘与正文可用区域左边界对齐，项目正文起点相对圆点左边缘右移约 5.5 pt，发生换行时使用相同位置的悬挂缩进。四项之间 `spaceBefore=0`、`spaceAfter=0`，不得插入空白段落；“报告目的：”“信息真实性：”“数据时效性：”“保密义务：”及其后正文全部保持常规字重，不得只加粗标签。`报告使用说明` 标题仍使用 14 pt、`#4F81BD` 的一级标题样式，不随正文缩小或变灰。
- 正文段落：核心观点、执行摘要核心特征与拜访建议、信息解读、贷款视角解读、普通说明、人员列表、产业与行业说明、营销边界和风险说明统一使用 15 pt 行高。核心观点、信息解读和贷款视角解读正文首行缩进 2 个汉字；执行摘要核心特征与拜访建议不缩进。普通正文段落段后 4 pt；PDF 使用段后样式控制间距，不插入空白段落，Markdown 回退在自然段之间保留一个空行。
- 字重：黑色正文必须使用宋体或等价中文宋体的常规字重，禁止整段使用字体名含 `Black`、`Bold`、`Semibold` 的变体。核心观点、执行摘要正文、信息解读标签后的正文、表格具体数据、股东名、人员名、代表记录、风险说明和报告使用说明均不得加粗。
- 主标题、客户名称、蓝色章节标题和表头行必须加粗。各分节标签和业务标签项也必须加粗；业务标签项包括 `FACT-xx`、`OPP-xx`、`LEAD-xx`、`SERVICE-xx`、`RISK-xx`、`WATCH-xx`、`QUESTION-xx` 及各表字段名。
- 表格：所有可见表格的表头行统一使用参考成品中的浅蓝色底纹 `#D9EAF7`（RGB `217, 234, 247`），表头文字固定为黑色；该颜色是独立的“表头蓝”，不得替换为章节标题蓝 `#4F81BD`、渲染器主题色或近似色。黑色 0.5 pt 网格线；表头和表格正文统一使用 12 pt 行高。表头必须使用实际中文粗体字形、左对齐并跨页重复，跨页重复的表头必须保持相同浅蓝底纹；符合上述定义的业务标签项必须使用实际中文粗体字形，其余正文保持常规字重、左对齐，单元格垂直居中。除表头外，普通数据行不使用 `#D9EAF7` 底纹。允许表格按可用空间自然分页，较长单元格可跨页拆分。
- 不使用 `KeepTogether`、`keepWithNext`、整块容器或手动分页符保护章节、段落、信息解读、数据来源或表格起始部分；允许这些内容随页面剩余空间自然续页。
- 不因避免断句、孤立标题或来源文字而主动移动整块内容；跨页表格只重复表头，不重复小节标题。
- 不得出现裁切、重叠、乱码或由强制分页造成的异常空白。除最后一页外，若后续仍有连续正文而当前页空白超过可用正文区约三分之一，视为分页失败。
- 页脚不添加页码、公司名或其他参考 DOCX 中不存在的内容。
- 字号不得为压缩页数降至上述规格以下；内容过长时通过自然分页解决。
- 内容不强制压缩到单页，篇幅随有效数据自然分页。

表格列宽按可用正文宽度 165.9 mm 固定分配：

执行摘要主要机会 18 / 28 / 48 / 33 / 18 / 20.9；执行摘要主要风险 18 / 28 / 55 / 25 / 39.9；企业基本信息 35 / 130.9；关键决策人信息 27 / 38 / 100.9；股东三列表 50 / 40 / 75.9，股东两列表 75 / 90.9；有形资产 30 / 80 / 55.9；无形资产 34 / 28 / 103.9；核心经营数据 36 / 74 / 55.9；行业周期与资金占用 27 / 35 / 29 / 38 / 36.9；行业对标与经营参照 26 / 30 / 34 / 30 / 45.9；政策与融资环境 36 / 35 / 44 / 50.9；行业风险与贷款启示 25 / 32 / 36 / 34 / 38.9；融资需求线索 16 / 24 / 34 / 26 / 15 / 18 / 32.9；贷款产品候选 35 / 36 / 30 / 30 / 34.9；推进路径 24 / 30 / 32 / 45 / 34.9；风险预警 16 / 20 / 25 / 40 / 32 / 32.9；推荐话题 25 / 30 / 50 / 60.9；关键问题 10 / 27 / 23 / 32 / 38 / 35.9；建议取得资料 40 / 60 / 30 / 35.9。单位均为 mm。

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

- 行内标签不得把带 `**` 的 Markdown 原样交给 ReportLab。只对骨架中的静态粗体标签和表格中的 OPP/RISK 编号转换为实际中文粗体，动态正文先执行 XML 转义后再拼接；`信息解读：`、`贷款视角解读：`、`有形资产：`、`无形资产：`后的正文必须回到常规字体。
- 表头行必须显式使用已注册的中文粗体字体；若单元格使用 `Paragraph`，使用粗体 Paragraph 样式或 `<b>...</b>`；若使用普通字符串，使用 `TableStyle(("FONTNAME", (0, 0), (-1, 0), "SongtiSC-Bold"))`。ReportLab 必须同时为首行设置 `TableStyle(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")))` 和黑色文字，并使用 `repeatRows=1` 保证跨页表头重复；DOCX 中转或其他渲染器必须为每个表头单元格设置等效的 `D9EAF7` 实色填充，禁止透明度、渐变、主题色或自动配色。表格业务标签单元格也必须显式指定粗体，不能只保留 Markdown 的 `**`。
- 使用 ReportLab 时，除报告使用说明外的非标题正文 `ParagraphStyle` 必须显式设置 `fontSize=10.5, leading=15`。报告使用说明必须删除 Markdown 行首的 `- `，对 XML 转义后的每条正文显式添加 `• ` 前缀，再分别构造为 `Paragraph("• " + text, usage_style)`；禁止使用 `bulletText` 或 ReportLab 默认列表组件，因为其自动字形间距会使正文起点偏离参考成品。`usage_style` 至少显式设置 `fontName="SongtiSC"`、`fontSize=9`、`leading=12`、`textColor=colors.HexColor("#666666")`、`leftIndent=5.5`、`firstLineIndent=-5.5`、`spaceBefore=0`、`spaceAfter=0`。段落容器从正文左边界开始：首行以负缩进把圆点拉回左边界，`•` 加半角空格后的正文起点距圆点左边缘约 5.5 pt，续行从 `leftIndent` 位置继续。DOCX 中转或其他渲染器使用等效的实心圆点、5.5 pt 悬挂缩进、固定 12 pt 行高和零段间距，不得使用默认列表主题、自动颜色或相对行距。表格单元格 `ParagraphStyle` 必须显式设置 `fontSize=9, leading=12`；元信息和数据来源样式必须显式设置 `fontSize=9, leading=12`。
- 开始排版正式报告前，先用最终字体配置生成仅含“正文测试”“粗体测试”的临时 PDF。用 PDF 字体元数据确认两段分别映射到常规和粗体 PostScript 字形，并渲染预览确认肉眼可辨；预检失败时不得继续生成正式 PDF。

### 生成与验收

来源分隔线专项验收纳入下方第 9 步：逐页渲染后测量“数据来源”文字包围盒中心与正文可用区域中心，水平偏差不得超过 2 pt；左右线段长度差不得超过 2 pt，且不得与标题文字相交。任一来源分隔线仍从左页边距起排、仅占半幅、左右线段明显不等长或依赖破折号字符自然宽度时，视为版式验收失败并重新排版。

1. 执行语义验收：确认 `OPP/LEAD/SERVICE/RISK/WATCH/QUESTION` 各自连续编号且全文引用存在对应主台账。每项至少有信号或资料缺口、证据状态、置信度、边界和核验方向；字段不完整允许存在，但必须转化为问题。所有台账条目至少在一个营销/风险模块和一个拜访问题中出现。
2. 核对内部与外部口径：内部原值保持不变；外部新增人员、股东、资产、财务、客户、供应商、市场和控制关系允许存在，但必须分列来源和时点。派生计算可以进行，必须保存公式、输入和精度。唯一绝对禁止项是伪造、模拟填充、静默覆盖内部值和保留敏感个人信息；`REL` 必须不含 `legalPersonCard`。
3. 核对开放来源覆盖：`WEB.queries` 保存全部查询，`WEB.candidates` 保存全部候选和打开状态，`WEB.sources` 保存可打开正文。每个 `[外部：Wn]`、`[候选：Cn]` 和模型分析都能回指来源、候选或推断链。没有交叉验证、主体间接、同名歧义、历史、无日期和正文未打开均不删除，只降低证据状态并进入 LEAD/WATCH/QUESTION。
4. 检查分层边界：直接事实、企业自述、单一媒体、平台线索、搜索摘要、冲突和模型推断使用不同标签。允许从关联关系推断上下游、从行业数据推演市场、从履历分析决策角色、从股权分析控制关系、从资产线索估算增信价值；推断必须展示方法和待核验条件，不得冒充银行审批结论。
5. 检查内容质量：核心观点优先引用高相关 OPP/RISK，同时指向完整 LEAD/SERVICE/WATCH；执行摘要展示开放台账；营销方案覆盖贷款和综合金融产品；风险模块覆盖交易条款、关联治理和行业市场。弱线索不得因不完整而丢失。
6. 任一台账或来源验收不通过时，优先补充字段、降级证据状态或转入 QUESTION，不删除条目。发现新证据可以重新搜索、重建台账并同步编号；只对完全重复、无关、敏感或恶意内容执行删除，并在 audit.json 记录原因。
7. 按“报告输出格式（严格填空骨架 · 模型只填值、不造结构）”替换占位符并执行预定义条件。检查报告中不存在未替换占位符、条件标签、内部字段路径、空表或未解析的来源 ID；检查所有内部来源行严格采用“内部：水滴征信 MCP｜数据日期：{generated_at}”，没有 MCP 后的维度括注；检查所有外部来源行严格采用“外部：Wn｜网站名称｜发布日期｜链接”，没有页面标题和访问日期，再开始排版。`WEB.sources` 中的标题与访问日期仍必须完整并通过内部证据验收。
8. 使用当前环境已有的文档或 PDF 能力生成 `output/pdf/{company_name}-客户访前一页纸.pdf`。如需 DOCX 中间文件，只把它作为本次临时产物。
9. 逐页渲染或预览最终 PDF，检查中文字体、Letter 页面、页边距、字号、行高、章节间距、表头样式、字重、列宽、来源 URL、自然分页、裁切、重叠和异常空白。逐表确认执行摘要主要机会与主要风险、企业基本信息、关键决策人、股权、资产、核心经营数据、行业表、融资需求线索、贷款产品候选、推进路径、风险预警、推荐话题、关键问题和资料清单均按骨架显示，所有表头及跨页重复表头使用 `#D9EAF7` 实色底纹和中文粗体，普通数据行不使用该底纹；所有 OPP/RISK 编号使用中文粗体且清晰可辨。继续按固定规则验收来源分隔线、报告使用说明、常规/粗体 PostScript 字形、字号和行高。除最后一页外，后续仍有连续正文但当前页空白超过可用正文区约三分之一时，视为分页失败并重新排版。
10. 验收通过后删除临时 DOCX、预览图片及一次性代码，但保留最终 PDF、统一证据 JSON 和脱敏审计文件 `output/audit/{company_name}-客户访前一页纸-audit.json`。
11. 审计文件必须包含 `EVIDENCE`、查询词、全部候选、采用层级、两跳身份桥接、冲突、计算与推断链；报告正文展示所有业务相关线索，技术命令和敏感信息仍不展示。
12. 当前环境无法创建或验收 PDF、中文字体不可用或转换失败时，不循环重试；删除不完整文件并回退完整 Markdown，说明“PDF 生成未完成：{原因}，已回退 Markdown”。

## Markdown 回退

用户指定 `--format md`，或 PDF 流程失败时，直接按“报告输出格式（严格填空骨架 · 模型只填值、不造结构）”输出。Markdown 与 PDF 必须复用同一证据模型中的原值和条件结果。

聊天回复只包含企业规范全称、数据日期、生成格式、最重要的 1 至 3 条资料范围说明，以及 PDF 绝对路径链接或完整 Markdown 正文。

## 输出纪律

1. 使用中文，用户明确要求其他语言时除外。
2. 七个大章节名称和编号逐字使用固定骨架，不得隐藏、跳号、重号、改名或输出空表；客户画像与产业画像必须独立，内部事实表按证据显隐。
3. 已知事实、贷款营销假设和待核验事项必须分开。允许推荐通用贷款产品族，但不得写“应授信”“建议放款”“预计可批”或承诺额度、利率、期限和审批结果。
4. 内部来源统一写“内部：水滴征信 MCP｜数据日期：{generated_at}”，不得显示业务维度括注；外部来源统一写“外部：Wn｜网站名称｜发布日期｜链接”，不得显示页面标题和访问日期；不得写 CISP、产品码、工具名或字段路径。标题和访问日期只保留在内部证据模型中。
5. “客户全景画像”和“产业画像与行业洞察”均固定展示。行业资料可以独立触发 LEAD/SERVICE/WATCH 或观察级 OPP；行内合作、授信、存款、结算、代发及其他用户授权数据均可展示。未指定目标银行时也可引用各银行公开产品作为市场参考，并明确非目标银行承诺。
6. “客户访前一页纸（贷款营销版）”是报告产品名称，不限制总页数；内容随有效数据自动增减。
7. 最终 PDF 必须经过逐页渲染验收；无法验收时不得交付 PDF，直接回退 Markdown。
8. 工商深度成功后，最终报告必须包含贷款及综合金融核心观点、开放式执行摘要、客户全景画像、产业画像与行业洞察、定制化营销方案、风险预警与观察、拜访建议与话题清单。OPP/LEAD/SERVICE/RISK/WATCH/QUESTION 必须贯穿后续章节；扩展事实不足时保留模型分析和资料缺口，但不得使用模拟数据或样例企业事实补齐。

**SKILL 版本**：v4.0-open ｜ **适配数据源**：连接标识为 `cisp-mcp` 的水滴征信 MCP 当前工具版本 + AI 网络搜索的全部来源与候选 ｜ **纳入模式**：全量纳入、分层标注、不设数量上限 ｜ **外部窗口**：近期检索默认 12 个月，同时不限期检索历史、人物、股东、资产与风险 ｜ **页面规格**：Letter 215.9 × 279.4 mm ｜ **默认交付**：PDF + 脱敏 audit.json，失败回退 Markdown
