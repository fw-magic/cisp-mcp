# PDF 证据模型

生成 PDF 前，把已核验事实整理为 UTF-8 JSON。渲染器只负责排版，不调用 CISP、不补写事实。

## 调用

```bash
uv run python <skill-dir>/scripts/render_company_profile_pdf.py \
  --input tmp/pdfs/{report-id}.json \
  --output output/pdf/{企业名称}-企业画像-{模式}-{YYYY-MM-DD}.pdf
```

`<skill-dir>` 是当前 `SKILL.md` 所在目录；skill 安装位置可能变化，不得写死仓库路径。

成功后删除 `tmp/pdfs/` 下本次 JSON。不得删除最终 PDF。

渲染器优先读取环境变量 `CISP_PROFILE_FONT` 指向的 TTF/OTF 中文字体，其次查找常见 macOS、Linux 和 Windows 中文字体。找不到可嵌入字体时会明确失败；此时按 skill 规则回退 Markdown，不得交付缺字 PDF。

## 顶层结构

```json
{
  "schema_version": "1.0",
  "report": {},
  "summary": {},
  "subject": {},
  "shareholders": [],
  "personnel": [],
  "network": [],
  "assets": [],
  "relations": {},
  "public_opinion": {},
  "risks": [],
  "changes": [],
  "evidence": {}
}
```

`relations`、`public_opinion` 仅完整版使用；没有数据时省略。其他空数组允许保留。

## 必填报告元数据

```json
{
  "report": {
    "title": "企业一页纸画像｜标准版",
    "company_name": "规范企业全称",
    "credit_code": "统一社会信用代码或未披露",
    "query_time": "YYYY-MM-DD HH:MM:SS",
    "mode": "精简版/标准版/完整版",
    "report_id": "CISP-CP-{统一社会信用代码}-{YYYYMMDD-HHMMSS}",
    "data_source": "CISP MCP"
  }
}
```

## 摘要与主体

```json
{
  "summary": {
    "one_sentence": "只包含有直接证据支持的一句话画像",
    "business_position": "登记行业与经营范围的事实摘要",
    "scale_and_tenure": "成立日期、年限和注册资本原值",
    "attention": ["最多三条重点或提示关注事实"]
  },
  "subject": {
    "registration_status": "登记状态",
    "legal_representative": "法定代表人",
    "company_type": "企业类型",
    "established_date": "YYYY-MM-DD",
    "registered_capital": "原值 + 原币种",
    "paid_in_capital": "原值",
    "registered_address": "注册地址",
    "registration_authority": "登记机关",
    "industry": "行业",
    "operating_period": "经营期限",
    "former_names": "曾用名",
    "business_scope_summary": "忠实压缩后的经营范围"
  }
}
```

缺失的可选主体字段直接省略或传空字符串；渲染器会删除对应行。

## 股权、人员和经营网络

```json
{
  "shareholders": [
    {
      "name": "股东名称",
      "type": "股东类型",
      "ratio": "接口原始比例字符串",
      "subscription": "金额/币种/日期"
    }
  ],
  "personnel": [
    {
      "name": "姓名",
      "position": "职务",
      "note": "兼任等必要说明"
    }
  ],
  "network": [
    {
      "dimension": "对外投资/分支机构/网站或网店",
      "count_display": "接口返回数量或本次返回数量",
      "status": "success/empty/failed",
      "examples": ["最多五个代表项"]
    }
  ]
}
```

股东最多五名并遵循原 skill 的排序规则。图表只使用可解析比例，标签仍展示原始字符串。

## 资产与资质

```json
{
  "assets": [
    {
      "dimension": "商标",
      "status": "success/empty/failed",
      "count": 1505,
      "count_display": "1,505",
      "records": [
        {
          "title": "代表记录名称",
          "detail": "类别/编号/日期/状态"
        }
      ],
      "note": "总量口径或失败原因"
    }
  ]
}
```

`count_display` 优先展示；应由证据整理阶段根据接口原值生成。荣誉资质只能写“本次返回 N 项”。

## 关联、舆情、风险和变更

```json
{
  "relations": {
    "summary": "按关系类型统计",
    "examples": ["最多五个公开关联线索"]
  },
  "public_opinion": {
    "summary": "时间窗、命中总量和数据边界",
    "records": [
      {
        "title": "标题",
        "date": "发布日期",
        "source": "来源"
      }
    ]
  },
  "risks": [
    {
      "topic": "经营异常/严重违法",
      "result": "异常历史 1 条；严重违法 0 条",
      "facts": ["最多三条有明确日期、案号、机关或状态的事实"],
      "level": "critical/attention/neutral",
      "scope": "目标企业自身/关联主体"
    }
  ],
  "changes": [
    {
      "date": "YYYY-MM-DD",
      "item": "变更事项",
      "summary": "忠实压缩后的变更前后内容"
    }
  ]
}
```

关联主体风险必须在 `scope` 明示，不得与目标企业自身记录合并。舆情只称“公开舆情线索”。

## 最小证据链

```json
{
  "evidence": {
    "successful_dimensions": ["工商深度", "商标"],
    "empty_dimensions": ["企业自身失信被执行"],
    "failed_dimensions": [
      {
        "dimension": "专利",
        "reason": "超时"
      }
    ],
    "limitations": [
      "分页接口首批记录仅作为示例",
      "历史登记不代表查询时点仍然有效"
    ]
  }
}
```

空结果、字段缺失和查询失败不得互换。JSON 中不得包含身份证号、手机号、API Key、原始响应或工具内部错误堆栈。
