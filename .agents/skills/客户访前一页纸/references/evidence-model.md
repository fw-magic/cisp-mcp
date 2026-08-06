<!-- resource-id: cisp://skill/client-pre-visit-one-pager/evidence-model -->
<!-- resource-version: 0-dev -->
<!-- source-skill-version: v5.5-history-founded-at -->

# 统一证据模型与业务维度整理规则

本文件是‘客户访前一页纸’ Skill 的调试期本地资源，也是对应未来 MCP Resource 的唯一正文源。进入主 `SKILL.md` 指定阶段后完整读取本文件。

## 内容索引

- [统一证据 JSON]
- [整理规则]
- [股权结构与关联关系]
- [有形资产]
- [产业画像]
- [核心经营数据]
- [企业风险与合规证据]

### 4. 构建统一证据模型

先把内部 MCP 原值和合格外部证据整理为以下 UTF-8 JSON，再从同一 JSON 生成所需格式。禁止不同格式分别归纳原始响应或重新搜索。

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
        "inclusion_layer": ["FACT|OPP|RISK"],
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
        "inclusion_layer": ["FACT|OPP|RISK"],
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
      "core": {"internal_dimensions": ["实际进入核心观点的内部业务维度"], "external_source_ids": ["实际进入核心观点的 Wn 或 Cn"]},
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
    "core_profile_candidate_facts": [
      {
        "candidate_fact_id": "CPF-01",
        "fact_type": "positioning|honor|brand_product|business_foundation|operating_scale|history_evolution|registry_support",
        "statement": "可直接用于企业简介的最小事实或候选表述",
        "subject": "目标企业规范名称或已核验别名",
        "period_or_date": null,
        "evidence_state": "verified_primary|verified_cross_source|company_self_reported|single_source|platform_clue|search_snippet_only|conflicting|unverified",
        "confidence": "高|中|低|未知",
        "relationship_path": "direct|verified_alias|two_hop|indirect|ambiguous",
        "source_refs": ["internal:<字段或状态>", "external:Wn", "candidate:Cn"],
        "limitations": null,
        "selection_priority": 1,
        "target_field": "core_company_profile|core_history_evolution",
        "selected_for_profile": true,
        "selected_for_history": false
      }
    ],
    "core_company_profile": "从 core_profile_candidate_facts 中按固定结构选材生成的企业简介第一段；只写稳定定位、荣誉、品牌、产品、业务基础和经营规模，存在合格候选时必须采用，不依赖 core_internal_baseline，工商字段非必显，不显示来源归因",
    "core_history_evolution": "企业简介第二段；按时间组织成立、并购重整、投资人入股、股权与控制权变化、经营管理权交接、管理层调整、重大转折及当前状态；本段生成且成立时间可得时，必须以成立时间作为沿革起点，仅有成立时间时不单独生成本段",
    "core_development_direction": "当前聚焦方向及已经采取的实际行动；无法同时核实方向与行动时说明资料边界",
    "core_risk_prompt": "主要风险事实总结及其带来的关注事项；无明确风险命中时说明资料覆盖边界和基础核验要求",
    "core_visit_objective": "围绕 OPP 提炼贷款及综合金融服务场景；无明确 OPP 时转为融资需求和合作条件诊断",
    "executive_core_features": "用已核实事实概括客户身份、经营阶段、近期转折及贷款营销价值，不提前展开产品方案",
    "opportunity_register": [
      {
        "opportunity_id": "OPP-01",
        "opportunity_type": "贷款机会|融资线索|综合金融机会",
        "opportunity_title": "简洁、客户化的机会名称",
        "executive_summary_sentence": "按‘客户专属经营动作或资金触发＋带来的金融需求、空间或机会’生成的执行摘要精简句，句末不含编号",
        "trigger_signal": "带日期或报告期、阶段和主体边界的企业专属触发事实或信号",
        "financial_direction": "可能的贷款用途、融资需求或非贷款综合金融服务方向",
        "timing": "近期|中期|待核验",
        "evidence_strength": "强线索|中线索|弱线索|仅摘要|模型推断|未知",
        "boundary": "金额、阶段、执行状态或企业确认情况等必要边界",
        "fit_logic": "触发事实或信号如何对应资金用途、融资路径或综合金融服务",
        "verification_focus": "需核实的用途、金额、期限、承担主体、还款来源、现有合作或其他关键条件",
        "evidence_ids": ["internal:<字段或状态>", "external:Wn"]
      }
    ],
    "risk_register": [
      {
        "risk_id": "RISK-01",
        "risk_type": "已核实风险|风险观察|待核实事项",
        "risk_title": "简洁、客户化的风险或待核实事项名称",
        "executive_summary_sentence": "按‘关键事实或风险来源＋风险、历史包袱或不确定性’生成的执行摘要精简句，句末不含编号",
        "fact_or_signal_boundary": "事实或信号、主体范围、日期或期间、来源、当前状态与不确定性边界",
        "affected_opportunity_ids": ["OPP-01"],
        "possible_impact": "对相关机会的准入、用途、期限、还款、增信、资料或推进节奏的条件式影响",
        "evidence_strength": "已核实|强线索|中线索|弱线索|仅摘要|模型推断|未知",
        "verification": "需核实的当前状态、证明材料或缓释方向",
        "evidence_ids": ["internal:<归一化风险事实>", "external:Wn"]
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
        "fact": "直接可核验的精简资产事实",
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
        "opportunity_id": "OPP-01",
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
    "risk_zero_dimensions": "以、连接的明确零值维度",
    "risk_compliance_context": "最新纳税评级、明确许可状态及必要的时间边界",
    "risk_information_boundary": "以业务语言说明无明细、时间较早、资料缺失或不同范围不可合并",
    "risk_interpretation": "命中事实、当前状态边界和贷款营销前置核验；无命中时说明不等同于无风险及应取得的基础资料",
    "visit_objectives": [{"objective": "本次拜访必须达成的可验证目标", "related_opportunity_ids": ["OPP-01"], "related_risk_ids": ["RISK-01"]}],
    "recommended_topics": [
      {"topic": "客户化话题", "opening_basis": "对应企业事实", "transition": "如何自然转入融资需求", "related_opportunity_ids": ["OPP-01"]}
    ],
    "visit_questions": [
      {"question": "开放式问题", "audience": "建议沟通对象", "topic": "经营计划|融资用途|金额期限|还款来源|现有融资|增信资源|风险化解|合作意愿", "basis": "已知事实或信息缺口", "answer_impact": "该答案将如何改变候选贷款方案", "related_opportunity_ids": ["OPP-01"], "related_risk_ids": ["RISK-01"]}
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
    "core_profile_candidate_facts": ["逐项登记 CPF 编号、事实类型、候选原文、主体关系、证据状态、置信度、限制、选择优先级、目标字段、是否进入第一段、是否进入第二段，以及 internal:<字段或状态>、external:Wn 或 candidate:Cn"],
    "core_company_profile": ["逐句登记实际采用的 CPF-xx 及其 internal:<字段或状态>、external:Wn 或 candidate:Cn；存在合格候选时至少映射一项，来源标识只用于内部追溯、不进入核心观点正文"],
    "core_history_evolution": ["按时间逐项登记第二段实际采用的 CPF-xx，以及成立时间、并购重整、投资人入股、股权或控制权变化、经营管理权交接、管理层调整、重大转折和当前状态所使用的 internal:<字段或状态>、external:Wn 或 candidate:Cn；第二段生成且成立时间可得时必须登记并采用该时间，字段为 null 时使用空数组"],
    "core_development_direction": ["逐句登记当前聚焦方向和已采取行动实际使用的 internal:<字段或状态> 与 external:Wn；资料不足回退时登记对应资料边界"],
    "core_risk_prompt": ["逐句登记风险事实、资料边界和由此形成的关注事项所使用的 internal:<归一化风险事实或状态> 与 external:Wn"],
    "core_visit_objective": ["逐句登记服务场景、融资诊断或合作条件所依据的 internal:<字段或资料缺口>、external:Wn 与相关 OPP 主数据"],
    "core_opportunity_ids": ["逐项回指生成重点发展方向或拜访目标时实际使用的 opportunity_register 编号；编号不进入核心观点正文"],
    "core_risk_ids": ["逐项回指生成风险提示时实际使用的 risk_register 编号；编号不进入核心观点正文"],
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
    "opportunity_register": ["逐项登记 OPP 的执行摘要精简句、机会类型、触发事实或信号、金融切入方向、时点、证据强度、边界、匹配逻辑、核验重点及 internal:<字段>、external:Wn 或 candidate:Cn"],
    "risk_register": ["逐项登记 RISK 的执行摘要精简句、风险类型、事实或信号、主体、时点、状态、证据强度、受影响 OPP、可能影响、核验方向及 internal:<字段>、external:Wn 或 candidate:Cn"],
    "executive_visit_strategy": ["登记支持优先 OPP、关键 RISK、切入点、核验事项和下一步的事实及信息缺口"],
    "loan_product_candidates": ["逐项登记所引用的融资需求行、还款来源、增信线索和准入缺口证据"],
    "service_product_candidates": ["逐项登记所引用的“综合金融机会”类 OPP、产品匹配逻辑、合作缺口和开场话术"],
    "marketing_sequence": ["逐阶段登记关联 OPP、RISK 及由候选产品与缺口导出的推进动作"],
    "risk_evidence_groups": ["逐组登记实际使用的 internal:B/OV_RISK/OV_TAX/LAND/LIC/HON/FIN_LISTED/OP 或 external:Wn 及主体、时间、状态和范围"],
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
- 工商深度成功后，七个业务模块固定显示。`opportunity_register`、`risk_register` 和 `visit_questions` 共同构成开放线索池。没有直接融资触发时，仍可从经营结构、行业传导、扩张、人员规模、政策、历史事件或模型分析建立“融资线索”或“综合金融机会”类 OPP，也可建立相应风险类型的 RISK；不得用模拟数据补事实。
- `opportunity_register` 是唯一机会主数据，`risk_register` 是唯一风险主数据。所有营销机会统一按 `OPP-01...` 连续编号，所有风险、观察和风险相关待核实事项统一按 `RISK-01...` 连续编号；发现新证据时可以新增、拆分、合并或重排，但必须同步更新全文引用和审计映射。
- 大章节编号固定为“一、核心观点 → 二、执行摘要 → 三、客户全景画像 → 四、产业画像与行业洞察 → 五、定制化营销方案 → 六、风险预警与合规提示 → 七、拜访建议与话题清单”。客户画像与产业画像必须彼此独立；行业事实表仍可按证据显隐，但不得隐藏、跳号、重号或更名七个大章节；“报告使用说明”不编号。
- `D.has_core_operations` 在工商主体确认后固定为 `true`，用于确保财务数据不足时仍显示业务提示；其他 `D.has_*` 只在对应板块至少存在一项有效内部事实或本 Skill 明确允许的合格外部事实时设为 `true`，不得为了保留版面而设为 `true`。
- `D.source_attributions.<section>.internal_dimensions[]` 列实际提供事实或资料缺口的内部业务维度；`external_source_ids[]` 可以同时登记 `Wn` 与 `Cn`。同一来源可以跨人物、股权、资产、营销、风险与拜访章节复用，不受单一 scope 限制。
- `D.core_profile_candidate_facts` 是企业简介两段的唯一选材池。`positioning/honor/brand_product/business_foundation/operating_scale` 且 `relationship_path=direct|verified_alias` 的候选可进入第一段；荣誉、称号、品牌和行业身份允许使用 `search_snippet_only/platform_clue/unverified/conflicting`，不要求直接、高可靠或交叉验证证据。`history_evolution` 专用于第二段，包括成立时间、并购、破产或重整、投资人入股、增资、股权/控股股东/实际控制人变化、持股比例、经营管理权交接、董事长/法定代表人/管理层调整、上市退市、重大项目转折及由此形成的当前阶段，禁止进入第一段。第二段因其他关键沿革条件生成时，成立时间可得则必须优先作为沿革起点；仅有成立时间不单独触发第二段。存在第一段合格候选时，`D.core_company_profile` 必须至少采用一项；若存在 `positioning/honor/brand_product` 候选，则至少采用其中一项。`registry_support` 仅为低优先级补充，不构成必显项。
- 基本信息只保留非空字段。展示层的无损格式化仅包括：纯数字整数部分增加千分位；严格匹配 `YYYY-MM-DD` 的日期显示为“YYYY年M月D日”；曾用名中的半角逗号、全角逗号或分号统一为“、”；已知币种代码显示其接口同时返回的中文名称；文档明确为比率的 `IND` 十进制值使用任意精度十进制乘以 100、删除无意义尾零后追加 `%`。必须保留全部有效数字和小数位，不得四舍五入；无法可靠识别时直接显示原值。
- `D.registered_capital_display` 使用无损格式化后的 `regCap` 与 `regCapCur` 组合为“金额单位（币种）”；接口明确 `regCap` 单位为万元时追加“万元”，不得重复单位。实缴资本同理。
- 股东表先展示内部直接股东原值，再展示外部股东、历史股东、穿透关系、实际控制人、最终受益人和一致行动候选。人数不设上限；内部与外部口径分列，推断关系标明依据和置信度。
- 整理为 `D.shareholder_rows[] = {name, holding_display, note, note_source_ids}`。内部比例与认缴额保留原值；可以倒算、合计、穿透和换算，必须显示公式、来源和“派生值”标签。
- `D.has_equity_or_network=true` 在存在内部股东、外部股东候选、历史股东、关系网络、实控人/最终受益人候选或资料缺口时成立。`REL` 和外部页面均可扩展关联主体、持股和控制关系候选，并标明口径与置信度。
- 关键决策人不设数量上限。内部人员、法定代表人、外部管理层候选、历史管理层、股东代表和公开活动中的关键角色均可进入 `D.person_rows[]`，以 `person_origin` 区分来源。
- 人物背景可以来自直接关系页或两跳身份桥接。每项背景登记关系来源、履历来源、身份键、置信度和冲突；企业官网、交易所、原任职机构年报、高校、媒体、百科、社交账号均可采用并按等级标注。
- 内外部职务冲突时分列“内部当前口径”“外部披露口径”和日期，不覆盖、不删除。历史任职、教育、专业、创业、行业经验、公开职责、访谈观点和可能决策角色均可展示；推断的决策角色标为“风险观察”或“待核实事项”类 RISK。
- 没有外部背景时保留人员并生成针对该人的背景核验问题；仅有弱来源时照常展示并标记低置信度。
- 有形资产与无形资产均全量展示，不设代表项数量上限；分页元数据和实际明细数量分别说明。
- 荣誉资质只展示本报告采纳的代表记录数量，不得称全量，不得使用“返回”描述。
- 舆情不设数量上限，保留标题、日期、来源、情感标签、主体关系和证据状态。目标企业为主体、关联主体、概念股、行业举例、顺带提及、同名可能或纯市场价格波动均可进入不同层级；只有完全重复项去重。
- 企业风险先按“主体与行政合规 → 司法与执行 → 股权及资产权利负担 → 税务与许可合规 → 财务经营关注 → 交易条款 → 关联方与治理 → 行业与市场 → 近期公开事件”九组归一化到 `D.risk_evidence_groups`，再生成唯一 `D.risk_register`；禁止让大模型直接读取原始响应临场分类。
- 风险事实只写目标企业自身记录；关联主体、股东或人员记录必须单独标明主体范围，不得并入企业自身失信、执行或债务结论。只有明确大于零的统计、非空且主体范围可确认的风险列表、明确异常的许可或资质状态、选定年度财务记录中的直接负值或合格的目标企业自身负面舆情才能进入风险表。
- 明确为零、纳税评级和许可状态均可按证据状态进入相应风险类型的 RISK 或合规观察；零值只能说明对应统计范围内记录数为零，不能证明无风险。
- `D.visit_questions[]` 必须按“经营与计划 → 融资用途 → 金额与期限 → 还款来源 → 现有融资 → 增信资源 → 风险化解 → 合作意愿”的漏斗排序。每个问题都要写明建议沟通对象、已知依据和答案对候选产品的影响；不得预设答案，不得把公开线索写成客户已确认需求。
- `D.coverage_summary` 只用工商登记、关键决策人及公开职业背景、股权与关联关系、上市公司财务、土地及外部设施资产、行业统计与排名、知识产权、备案许可、荣誉资质、纳税评级、近期公开动态、外部企业动态、外部行业背景和近两年风险等业务名称概括资料范围；内部已覆盖内容写“报告已覆盖……”，内部无可展示内容写“公开资料中暂无可供展示的……”，内部失败写“相关资料尚待补充”。`WEB.status="empty"` 时写“外部公开资料未形成可用补充”，`WEB.status="unavailable"` 时写“外部公开资料检索尚待补充”。不得出现企业 ID 解析、工商简项、产品码、工具名、内部别名或原始状态代码。
- “客户全景画像”与“产业画像与行业洞察”可以同时使用内部、外部、候选和模型分析；外部行业定量、竞争对手、上下游、市场与政策信息可以映射为相应类型的 OPP 或 RISK，必须标明从行业到企业的传导假设。
- `D.risk_interpretation` 始终必填；有命中时总结事实、范围、贷款营销影响和需核实事项，无命中时说明资料边界与基础准入材料要求，不评级、不推演未来损失。
- 每个非空 `D` 文案字段都必须在 `EVIDENCE` 中登记来源；内部来源写成 `internal:B/ID/OV_*/LAND/IND/REL/FIN_*/TM...OP.<字段或状态>`，外部来源写成 `external:Wn`。任何 `external:Wn` 都必须能在 `WEB.sources` 找到完整元数据并出现在对应章节的 `D.source_attributions.<section>.external_source_ids[]`。

#### 股权结构与关联关系生成规则

1. 本节展示内部直接股东、外部当前股东候选、历史股东、多层穿透、实际控制人、最终受益人、一致行动、表决权、管理人、出资人、关联交易和控制关系分析，不设层级或数量上限。
2. 内部 `B.shareholderList[]` 原值逐条保留；外部名称、比例、认缴额、出资日期和控制关系作为独立外部口径进入同表或附表。允许计算合计、集中度和穿透比例，但必须展示公式和输入来源。
3. 一级至四级来源、搜索摘要和模型推断均可生成股东或控制关系候选；分别标记证据状态、关系路径、时点和置信度。名称推断、机构性质推断和控制权推断允许进入“风险观察”或“待核实事项”类 RISK。
4. 历史与当前信息分列；内外部冲突全部保留并标记 `conflicting`，不得删除任何一方。只有完全重复项去重。
5. `D.has_shareholder_notes=true` 在存在任何外部说明、推断、冲突或资料缺口时成立。缺少说明的行显示“暂无补充”，不得隐藏其他行。
6. `D.equity_interpretation` 可以分析集中度、控制权、支持能力、关联交易和治理影响，但必须区分事实、外部口径和模型分析。
7. `EVIDENCE.shareholder_rows` 逐行登记内部、外部或候选证据，包含计算公式、身份桥接、冲突和置信度。

#### 有形资产生成规则

1. `D.tangible_asset_rows[] = {asset_type, fact, boundary, source_ids}`，不设数量上限。土地、建筑、设施、设备、产线、项目、地址、门店、服务网点、分支、展厅、客户现场、招商、产能、经营范围和一般资产宣传均可进入，按证据状态和资产明确程度排序。
2. 直接描述具体资产的进入 FACT；行业、经营范围、注册地址、网站、分支、资本、许可、荣誉、知识产权、招投标、客户项目和一般产品信息可以形成“融资线索”类 OPP，不作硬排除。
3. 内部土地记录按页码顺序全量合并；只删除 JSON 内容完全一致的重复对象。每条记录均可成行，并可计算面积、成交价格和抵押金额合计，显示公式、口径和重复处理方法。
4. 土地供应记录按可解析的 `supplyArea` 从大到小排序，面积相同时按有效 `contractDate` 从新到旧排序；土地出让按 `landArea` 从大到小、再按 `pubDate` 从新到旧排序；土地抵押按 `pubDate`、再按 `boardStartDate` 从新到旧排序。排序只决定展示顺序，不删除任何记录或字段，解析值不得替换原值。执行摘要可以引用排序靠前的代表记录，完整资产表必须保留全部记录及全部有值字段。
5. `B` 中的工商抵押、司法协助或其他记录无论是否写明具体抵押物均进入资产或权利负担表；对象不明时标记“资产对象待核验”。
6. 外部有形资产使用 `scopes[]` 包含 `tangible_asset` 的任一来源或候选；主体直接、两跳、间接和歧义关系均可纳入。正文未同时确认企业、资产、角色或时点时降低证据状态并生成核验问题。
7. 外部事实可以展示设施名称、位置、证号、宗地编号、面积、价格、投资额、账面/评估价值、产能、设备数量、抵押金额和权属口径；来源之间分列，企业自述和平台数值注明未独立核验。
8. 企业官网内容必须写“企业官网披露”，并在 `boundary` 写明“企业自述仅确认公开披露的设施或使用场景，不证明产权、租赁关系、账面价值或当前状态”。政府、监管、规划或交易所页面只确认其直接披露的审批、备案、建设、交易或公告节点；未明确完工、投产、使用或持有时不得升级状态。
9. 历史外部页面必须保留原始日期并写成“于{日期}披露/备案/公告”；不得据此使用“现有”“目前”“正在”“已投产”等当前时态。外部来源之间或与内部记录冲突时优先直接一级原始页面作为主口径，同时完整保留其他口径并列写入 `boundary`，不由模型选择性删除产权、面积或状态信息。
10. 地址、行业、经营范围、门店、服务网络、终端数量、分支、展厅、客户现场、合作园区、产品交付、订单、融资、荣誉、招商、“建设基地”“计划投资”和“拟购置设备”均可进入资产线索；不证明产权或当前状态时，其金融机会明确标为“融资线索”类 OPP。
11. 土地供应、土地出让只称“公开土地记录”或“涉及土地供应/土地出让”，不得称为当前产权、当前持有土地或自有土地；土地抵押和具体抵押物只说明公开登记事实，不得推导当前仍有效、已经解除、资产价值或企业偿债能力。不得用任何内部或外部事实推导“轻资产”“重资产”“自有房产”“自有厂房”或“资产实力”。
12. `D.has_assets=true` 仅在 `D.tangible_asset_rows` 至少一行，或任一无形资产事实非空时成立。有形资产没有合格事实、但存在无形资产时，仅显示无形资产；两者均为空时隐藏整个资产章节。不得为了保留“有形资产”标题输出空段、通用边界句或“暂无记录”。
13. `D.assets_interpretation` 接收全部资产事实、线索、地址、经营范围、行业、注册资本、项目宣传、估值和资料缺口，按证据状态分层解释。
14. `EVIDENCE.tangible_asset_rows` 逐行登记 `internal:LAND/B.<字段>`、`external:Wn` 或 `candidate:Cn`、主体、日期、对象、边界、计算和证据状态；空结果、失败状态和未打开候选也可支持资料缺口或“待核实事项”类 RISK。

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
8. `property.data[]` 全量保留全部排名、行业平均值、知识产权维度和 `*RankFour` 字段。有效正整数可直接进入行业对标；零值、空值、非正整数、未知四分位定义或异常值进入“风险观察”或“待核实事项”类 RISK，并保留原字段名、原值和口径限制，不因无法解释而省略。
9. `indLocOpr.data[]` 全年度、全指标展示，不设行数上限；零值、正值、缺失和冲突均可进入行业观察，并注明不能由零值证明无风险。
10. `D.industry_cycle_rows[]` 接收内部、外部、候选和模型分析中的全部周期、季节、库存、账期、回款和资本开支信号；缺项不阻止成行。
11. `D.industry_benchmark_rows[]` 接收跨年度、跨地区、跨口径的内部与外部排名、竞争对手、营收、销量、产能、市场份额和评价；必须显示可比性差异和来源口径。
12. `D.industry_policy_rows[]` 接收现行、历史、拟议、政府、媒体、协会、平台和摘要中的政策或融资环境线索；标明有效期、适用范围和证据状态。可以分析企业可能适用性和申报路径，但不得把分析写成银行正式审批结果。
13. `D.industry_risk_rows[]` 接收内部、外部、候选摘要和模型分析中的全部行业风险；即使缺少传导或企业指标也保留该行，并把缺项转为核验问题。
14. `D.industry_external_context` 接收所有行业来源和候选，可展示市场规模、CAGR、市场份额、竞争对手经营值、上下游名单及对企业的映射；外部事实与模型映射分列。
15. 行业事实可以单独形成“融资线索”或“综合金融机会”类 OPP，也可形成“风险观察”类 RISK 或产品探索建议；缺少企业专属事实时标明“行业到企业的传导假设”和需核验条件。
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
3. 司法与执行同时接收 `OV_RISK.list[0]`、`B.dishonestList`、`executedList`、法院/监管页面、媒体、平台和搜索摘要。主体自身、人员、股东、历史股东及关联主体分别标注关系路径；目标企业直接记录归入“已核实风险”类 RISK，其他主体记录归入“风险观察”类 RISK。统计与明细分列，可提供去重前总量、去重后事项数及去重方法，但不静默覆盖冲突值。
4. 股权及资产权利负担使用 `B.sharFrozList`、`sharePledgList`、`mortReg`、mortgage、judicial aid 和 `LAND.tddy.records[]`。股东质押记录写成“股东股权质押”，不得写成企业自身债务；股权冻结、司法协助和同一案号、金额、日期对应的记录可能指向同一事项，只分别说明各列表列示数量，不得相加为风险总数。没有明确注销、解除或当前状态时，只写登记日期、期限和公开状态，不得写“当前有效”“已经解除”。
5. 税务与许可合规接收内部记录、税务/监管原始公告、媒体、平台和摘要线索；历史评级、欠税、许可状态和冲突口径均展示。原始公告归入“已核实风险”类 RISK，单一媒体或平台归入“风险观察”类 RISK，摘要归入“待核实事项”类 RISK。
6. 财务经营关注同时接收内部财务、法定披露、企业自述、媒体数值、平台数值和模型测算。各口径分列并可计算派生比率、趋势和压力情景；所有计算显示公式、输入和口径，外部或推算结果不得冒充内部审计数据。
7. 交易条款组接收关联交易、定价、付款、账期、退货、退款、回购、担保、质押、排他、终止、违约、验收、付款义务人和回款账户等事实或线索；凡可能改变第一还款来源、现金流闭环或授信结构，均可按证据状态形成相应风险类型的 RISK。
8. 关联方与治理组接收股东、历史股东、实控人候选、管理层履历、跨界经营、关联主体债务、控制权冲突、关键人依赖和决策链不清等事实或分析；行业与市场组接收需求、价格、库存、渠道、竞争、政策和区域风险。直接事实归入“已核实风险”类 RISK，间接或分析性内容归入“风险观察”类 RISK。
9. 近期公开事件接收所有内部舆情、外部正文、搜索摘要、行情、概念股、行业评论、顺带提及和无详情标题；按主体关系与证据状态分层，不作硬排除。
10. 九组整理完成后，全部风险内容进入唯一 `risk_register`：直接且已核实的风险事实标为“已核实风险”，`context`、间接、历史、行业、人物、冲突、弱来源和模型推断标为“风险观察”，只有摘要、同名可能、资料缺口或正文无法核验的标为“待核实事项”。全部按 `RISK-01...` 连续编号，不设数量上限；仅完全重复项去重。允许输出严重、高、中、低、观察等分析等级，但必须同时显示评级依据和非审批结论边界。
11. `D.risk_compliance_context` 汇总内部和外部税务、许可、资质背景及冲突；没有事实时登记资料缺口。
12. 近两年统计中的明确数字 `0`、空字符串、`null`、失败和未调用均可作为资料状态进入说明或“待核实事项”类 RISK，但不得把非零未知改写为零。
13. `D.risk_interpretation` 接收全部风险组、统一 RISK 台账、资料缺口、冲突和模型分析，按“事实/线索 → 主体与时点 → 可能影响 → 核验材料”生成。
14. `EVIDENCE.risk_*` 逐组、逐行登记 `internal:<字段>`、`external:Wn` 或 `candidate:Cn`；统计与明细不一致、跨列表重复、内外部冲突和状态未知均保留并显式展示。
