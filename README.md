# cisp-mcp

`cisp-mcp` 是一个用 Python 编写的 CISP API MCP 服务，用于把 CISP 企业信息接口封装成可被大模型调用的 MCP tools。

项目使用 `uv` 管理依赖，基于 `mcp` Python SDK 的 `FastMCP` 开发，通过 CISP AI 网关 JSON 接口访问后端 API。

## 项目能力

- 支持 Claude Code、Codex、Codex App、OpenClaw、WorkBuddy 等 MCP 客户端接入。
- 每个 CISP 产品接口对应一个独立 MCP tool，工具名包含产品号，方便排查和定位。
- 自动补充 `prodCode`，调用方只需要传业务参数。
- 对 CISP 返回结果做统一归一化，保留原始返回 `raw_response`。
- Streamable HTTP 模式支持每个客户使用自己的 CISP API Key，便于后端按 Key 计费。
- 支持本地 smoke test，验证 MCP 服务和工具注册是否正常。

## 技术栈

- Python `>=3.11`
- uv
- MCP Python SDK / FastMCP
- httpx
- python-dotenv

## 运行环境要求

推荐本机提前安装：

- Python `3.11` 或更高版本
- uv

`uv` 可以管理 Python 版本；如果本机没有符合要求的 Python，`uv` 在部分环境下可以自动下载和管理。但在企业内网、代理或离线环境中，自动下载可能失败，因此建议提前安装好 Python `3.11+`。

## 生产部署

CentOS 7 联网构建、离线包制作、生产部署、升级、回滚和新增依赖的完整流程，请参阅：

- [CISP MCP CentOS 7 离线生产部署与运维手册](OPERATIONS_CENTOS7.md)

## 项目结构

```text
cisp-mcp/
├── src/cisp_mcp/
│   ├── server.py        # MCP tool 定义和服务入口
│   ├── client.py        # CISP JSON 网关客户端
│   ├── config.py        # 环境变量配置
│   └── interfaces.py    # 产品码、接口名称、状态码等定义
├── scripts/
│   └── smoke_test_mcp.py
├── docs/                # 本地接口文档目录
├── .env.example
├── pyproject.toml
└── README.md
```

## 快速开始

### 1. 下载项目

```bash
git clone <your-github-repo-url>
cd cisp-mcp
```

如果是在已有目录：

```bash
cd /path/to/cisp-mcp
```

### 2. 检查 Python 和 uv

检查 Python：

```bash
python3 --version
```

检查 uv：

```bash
uv --version
```

如果没有安装 uv，可以按 uv 官方方式安装，或使用本机已有的 Python 环境安装。

### 3. 安装依赖

```bash
uv sync
```

### 4. 配置环境变量（本地 stdio 模式）

复制模板：

```bash
cp .env.example .env
```

编辑 `.env`：

```text
CISP_ENDPOINT=https://cisp.zenitera.com
CISP_REQUEST_URI=/ectcispserver/api/entcreditapi/query
# 可选；配置后仅 CISP 出站请求使用该代理
# CISP_ENDPOINT_PROXY=http://proxy.example.internal:8080
CISP_API_KEY=替换成真实 API Key
CISP_TIMEOUT_SECONDS=30
CISP_VERIFY_SSL=true
```

`CISP_API_KEY` 只用于本地 stdio 模式。生产 Streamable HTTP 模式不在服务器保存统一 Key，而是要求每个客户发送：

```http
Authorization: Bearer <客户自己的CISP_API_KEY>
```

服务会将当前请求的 Bearer Token转换为调用 CISP 后台所需的：

```http
X-API-Key: <客户自己的CISP_API_KEY>
```

如果访问 `CISP_ENDPOINT` 必须经过代理，配置：

```ini
CISP_ENDPOINT_PROXY=http://proxy.example.internal:8080
```

也支持 `socks5://` 代理。未配置或配置为空时，CISP 请求直接连接目标地址；程序不会继承系统的 `HTTP_PROXY`、`HTTPS_PROXY` 或 `ALL_PROXY`，避免实际路由与配置不一致。

## 本地运行和调试

### smoke test

这个测试验证 MCP 服务能否启动、无 Bearer Key是否返回 `401`、不同客户能否隔离 MCP Session，以及 `tools/list` 是否能看到所有工具。它不会调用真实 CISP API，也不会消耗接口次数。

```bash
uv run python scripts/smoke_test_mcp.py
```

正常结果类似：

```text
Discovered MCP tools:
- p0010010_query_business_profile
- p0010058_query_business_basic_deep
...
- query_cisp_product
Total: 37
Smoke test passed.
```

### stdio 模式

stdio 是给 Claude Code、Codex、OpenClaw、WorkBuddy 等 MCP 客户端使用的模式。

```bash
uv run cisp-mcp
```

手动执行时终端会停住，这是正常现象。stdio 模式通过标准输入/输出和 MCP 客户端通信，不会像 Web 服务一样打印访问地址。

### HTTP 调试模式

如果要用 MCP Inspector 调试，可以启动 Streamable HTTP：

```bash
uv run cisp-mcp --transport streamable-http
```

默认地址：

```text
http://127.0.0.1:8000/mcp
```

然后启动 Inspector：

```bash
npx -y @modelcontextprotocol/inspector
```

在 Inspector 中选择：

```text
Transport: Streamable HTTP
URL: http://127.0.0.1:8000/mcp
Authorization: Bearer <测试用CISP_API_KEY>
```

## 工具列表

| 产品码 | 接口名称 | MCP tool |
| --- | --- | --- |
| `P0010010` | 企业工商照面信息查询 | `p0010010_query_business_profile` |
| `P0010058` | 企业工商基本信息查询（深度） | `p0010058_query_business_basic_deep` |
| `P0010059` | 企业工商基本信息查询（简项） | `p0010059_query_business_basic_brief` |
| `P0010068` | 企业名称模糊查询（简版） | `p0010068_fuzzy_search_company_name` |
| `P0010073` | 企业商标信息查询 | `p0010073_query_trademark_info` |
| `P0010074` | 企业软件著作权信息查询 | `p0010074_query_software_copyright_info` |
| `P0010075` | 企业作品著作权信息查询 | `p0010075_query_work_copyright_info` |
| `P0010076` | 企业 ICP 备案信息查询 | `p0010076_query_icp_filing_info` |
| `P0010078` | 企业专利信息查询 | `p0010078_query_patent_info` |
| `P0010084` | 企业许可信息查询 | `p0010084_query_license_info` |
| `P0020014` | 企业疑似关系信息查询 | `p0020014_query_suspected_relationships` |
| `P0020019` | 企业疑似实际控制人信息查询 | `p0020019_query_suspected_controller` |
| `P0020021` | 企业单点关联信息查询 | `p0020021_query_single_point_related_info` |
| `P0020023` | 企业股权穿透信息查询 | `p0020023_query_equity_penetration` |
| `P0020024` | 企业受益股东详细查询 | `p0020024_query_beneficial_shareholders_detailed` |
| `P0020031` | 企业多点关联信息查询 | `p0020031_query_multi_point_relationships` |
| `P0020044` | 企业间关联关系查询 | `p0020044_query_intercompany_relationship` |
| `P0020129` | 企业实控人和最终受益人查询 | `p0020129_query_controller_and_ubo` |
| `P0050007` | 企业舆情信息列表查询 | `p0050007_query_public_opinion_list` |
| `P0050008` | 企业舆情信息详情查询 | `p0050008_query_public_opinion_detail` |
| `P0050007+P0050008` | 企业舆情信息查询（列表+详情） | `p0050007_p0050008_query_public_opinion_info` |
| `P0060007` | 企业工商二要素验证 | `p0060007_verify_business_two_elements` |
| `P0060008` | 企业工商三要素验证 | `p0060008_verify_business_three_elements` |
| `P0090001` / `P0090012` | 企业最终受益人信息查询（详版/非详版） | `p0090001_p0090012_query_ubo` |
| `P0090008` | 企业实际控制人信息查询 | `p0090008_query_actual_controller` |
| `P0090011` | 企业最终受益人信息查询-全路径版 | `p0090011_query_ubo_full_paths` |
| `P0110003` | 企业荣誉资质信息查询 | `p0110003_query_honor_qualification_info` |
| `P0130025` | 企业关键指标信息查询 | `p0130025_query_company_key_indicators` |
| `P0130036` | 企业土地信息查询 | `p0130036_query_land_info` |
| `P0130038` | 企业画像-行业分析 | `p0130038_query_industry_analysis` |
| `P0210004` | 上市公司财务数据查询 | `p0210004_query_listed_company_financial_data` |
| `P0980006` | 企业高级筛选 | `p0980006_query_advanced_company_filter` |
| `P0980008` | 纳税评级 | `p0980008_query_tax_rating` |
| `P0980023` | 光大-近2年风险分析统计 | `p0980023_query_two_year_risk_summary` |
| `P0980033` | 上市投融资招投标知识产权情况 | `p0980033_query_listing_financing_bidding_ipr` |
| `P0990022` | 供应商关联关系 | `p0990022_query_supplier_relationships` |
| 通用 | CISP JSON 网关调试查询 | `query_cisp_product` |

### 返回结构

专用工具会返回归一化字段和原始响应：

- `product_code`：产品码
- `interface_name`：接口名称
- `success`：`resultCode == "00000"`
- `has_result`：产品状态码为 `4`
- `result_code_desc`：结果码说明
- `product_status_desc`：产品状态说明
- `data`：产品数据对象
- `raw_response`：CISP 原始返回

如果产品数据里存在常用列表字段，也会额外透出快捷字段，例如：

- `basicList`
- `fuzzyList`
- `brandList`
- `swList`
- `resultList`
- `icpList`
- `patentsList`
- `detailList`（`P0010084`、`P0130036`）
- `suspectList`
- `controlNodeList`
- `entInvList`
- `nodeList`（`P0020024`）
- `nodes`
- `relationship`
- `dataList`
- `finalList`（`P0090001`、`P0090012`）
- `actualController`（`P0090008`）
- `MatchInfoList`
- `infoList`
- `infoDetail`
- `matchList`
- `itemNameList`
- `coreLndicatorInfo`（`P0130025`，字段名沿用底层接口原始拼写）
- `suppList`（`P0990022`）
- `entList`（`P0980006`）
- `list`（`P0980008`、`P0980023`）
- `data`（`P0980033`）

`P0210004` 会根据 `financial_type` 在 `data` 中填充对应列表：
`rgincomeInfo`、`rgcashflowInfo`、`fncmfninInfo`、`rgbalanceInfo`、
`mainfinadataInfo`、`balanceInfo`、`incomeInfo` 或 `cashflowInfo`。

## 调用示例

### 查询工商照面信息

```json
{
  "ent_info": "证通股份有限公司"
}
```

对应工具：

```text
p0010010_query_business_profile
```

### 查询深度工商信息

```json
{
  "ent_name": "证通股份有限公司"
}
```

对应工具：

```text
p0010058_query_business_basic_deep
```

### 查询简项工商信息

`ent_name`、`credit_code`、`reg_no`、`org_code` 严格四选一；`types` 用于选择需要返回的数据类型。

```json
{
  "ent_name": "证通股份有限公司",
  "types": ["basic", "person", "shareholder"]
}
```

对应工具：

```text
p0010059_query_business_basic_brief
```

### 查询企业受益股东详细信息

`ent_info` 支持企业全称或统一社会信用代码。结果通过 `nodeList` 快捷字段返回；
`benifitTag` 是底层接口原始拼写，可包含“受益股东”“最终受益人”或“实际控制人”。

```json
{
  "ent_info": "证通股份有限公司"
}
```

对应工具：

```text
p0020024_query_beneficial_shareholders_detailed
```

### 查询企业实际控制人

`ent_name` 支持企业全称、统一社会信用代码或工商注册号。结果通过
`actualController` 快捷字段返回，包含实际控制人、产品聚合股权占比和控制路径。

```json
{
  "ent_name": "证通股份有限公司"
}
```

对应工具：

```text
p0090008_query_actual_controller
```

### 查询企业最终受益人（详版/非详版统一入口）

AI 应按任务目的选择 `edition`：完整报告、审计留档或关键管理人员兜底使用
`detailed`；快速识别、独立互证或需要 `bnfCat` 判定依据使用 `standard`。
非详版可将 `include_paths` 设为 `false`，只返回最终受益人。

```json
{
  "ent_name": "证通股份有限公司",
  "edition": "detailed",
  "include_paths": true
}
```

对应工具：

```text
p0090001_p0090012_query_ubo
```

### 企业高级筛选

```json
{
  "eid": "可选的 CISP 企业内部标识",
  "area_prefix": "44",
  "org_scale": "大型",
  "page_no": "1",
  "page_size": "10"
}
```

对应工具：

```text
p0980006_query_advanced_company_filter
```

### 查询上市、投融资、招投标和知识产权概况

```json
{
  "ent_info": "证通股份有限公司"
}
```

对应工具：

```text
p0980033_query_listing_financing_bidding_ipr
```

### 查询纳税评级

`eid` 是 CISP 企业内部标识。如果只有企业名称，应先调用
`p0010010_query_business_profile`，从企业名称准确匹配的
`basicList[].entId` 获取，并将其作为 `eid` 传入。不要根据统一社会信用代码自行推算
`eid`。企业高级筛选查询成功时，也可以使用其返回的 `entList[].eid`。

```json
{
  "ent_info": "证通股份有限公司"
}
```

```json
{
  "eid": "替换成 p0010010 返回的 basicList[].entId"
}
```

对应工具：

```text
p0980008_query_tax_rating
```

### 查询近2年风险分析统计

如果只有企业名称，先调用 `p0010010_query_business_profile`，从企业名称准确匹配的
`basicList[].entId` 获取企业内部标识。不要自行构造或推算 `eid`。

```json
{
  "eid": "替换成 p0010010 返回的 basicList[].entId"
}
```

对应工具：

```text
p0980023_query_two_year_risk_summary
```

### 查询专利信息

```json
{
  "ent_info": "证通股份有限公司",
  "page_no": "1",
  "page_size": "10"
}
```

对应工具：

```text
p0010078_query_patent_info
```

### 查询企业投资和任职关联信息

用户只需要描述查询意图，模型会选择对应的 `relation_direction`：

- `"1"`：同时查询投资和任职关系
- `"2"`：只查询投资关系
- `"3"`：只查询任职关系

```json
{
  "ent_info": "证通股份有限公司",
  "relation_direction": "2"
}
```

对应工具：

```text
p0020021_query_single_point_related_info
```

### 查询企业荣誉资质

```json
{
  "ent_info": "证通股份有限公司"
}
```

对应工具：

```text
p0110003_query_honor_qualification_info
```

### 查询企业关键指标

```json
{
  "ent_info": "证通股份有限公司",
  "indicator_type": "2"
}
```

`indicator_type` 可选值：

- `"1"`：指标等级，默认值
- `"2"`：指标金额

结果列表通过 `coreLndicatorInfo` 快捷字段返回，包含报告年份、资产总额、负债总额、
所有者权益、营业收入、主营业务收入、利润、纳税、从业人数和社保人数等年报关键指标。

对应工具：

```text
p0130025_query_company_key_indicators
```

### 查询企业土地信息

```json
{
  "ent_info": "证通股份有限公司",
  "land_type": "tddy",
  "page_no": "1",
  "page_size": "10"
}
```

`land_type` 可选值：`tdgy`（土地供应）、`tdcr`（土地出让）、`dkgs`（地块公示）、`tddy`（土地抵押）。不传时由底层产品决定返回范围。

对应工具：

```text
p0130036_query_land_info
```

### 查询企业画像行业分析

```json
{
  "ent_info": "证通股份有限公司",
  "analysis_type": "property",
  "nic_lvl": "n3",
  "region_lvl": "r2",
  "region_id": "440300",
  "nic_id": "C391"
}
```

`analysis_type` 可选值：`finRank`、`finRankStock`、`entRegionRank`、`locfin`、`indLocOpr`、`indLocOprFin`、`property`、`financialRegionRank`。不同类型的结果字段不同，统一从返回的 `data` 中读取。

对应工具：

```text
p0130038_query_industry_analysis
```

### 查询上市公司财务数据

```json
{
  "ent_info": "证通股份有限公司",
  "financial_type": "mainfinadata",
  "start_date": "2024-01-01",
  "end_date": "2025-12-31"
}
```

`financial_type` 可选值：

- `rgincome`：通用类利润
- `rgcashflow`：通用类现金流量
- `fncmfnin`：金融公司主要财务指标
- `rgbalance`：通用类资产负债
- `mainfinadata`：主要会计数据和财务指标
- `balance`：一般企业资产负债
- `income`：一般企业利润
- `cashflow`：一般企业现金流量

`start_date`、`end_date` 可选，格式为 `YYYY-MM-DD`。不同类型的结果列表位于
返回值的 `data` 对应 `*Info` 字段中。

对应工具：

```text
p0210004_query_listed_company_financial_data
```

### 查询供应商关联关系

```json
{
  "ent_info": "证通股份有限公司"
}
```

对应工具：

```text
p0990022_query_supplier_relationships
```

### 查询企业许可

```json
{
  "ent_info": "证通股份有限公司",
  "license_type": "ylxk",
  "province": "广东省",
  "page_no": "1",
  "page_size": "10"
}
```

对应工具：

```text
p0010084_query_license_info
```

### 查询企业舆情信息

```json
{
  "ent_name": ["证通股份有限公司", "水滴科技服务有限公司"],
  "page_no": "1",
  "page_size": "10",
  "max_details": 10
}
```

对应工具：

```text
p0050007_p0050008_query_public_opinion_info
```

说明：该工具会先调用 `P0050007` 查询舆情列表，再用列表返回的 `entryId` 和用户传入的 `ent_name` 调用 `P0050008` 查询舆情详情。

### 只查询企业舆情列表

```json
{
  "ent_name": ["证通股份有限公司", "水滴科技服务有限公司"],
  "page_no": "1",
  "page_size": "10"
}
```

对应工具：

```text
p0050007_query_public_opinion_list
```

### 查询企业舆情详情

```json
{
  "entry_id": "替换成舆情列表返回的 entryId"
}
```

对应工具：

```text
p0050008_query_public_opinion_detail
```

如果只传 `ent_name`，服务会先查询该企业第一页舆情列表，再取第一条 `entryId` 查询详情。

### 二要素验证

```json
{
  "ent_name": "证通股份有限公司",
  "reg_no": "替换成真实统一社会信用代码"
}
```

对应工具：

```text
p0060007_verify_business_two_elements
```

## 集成到 Claude Code

生产环境使用远程 Streamable HTTP。在启动 Claude Code 的环境中设置客户自己的 Key：

```bash
export CISP_API_KEY='<客户自己的CISP_API_KEY>'
```

项目级 `.mcp.json`：

```json
{
  "mcpServers": {
    "cisp-mcp": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${CISP_API_KEY}"
      }
    }
  }
}
```

本地开发也可以使用 stdio 模式，让 Claude Code 自动启动 MCP 服务；此时 Key来自项目 `.env`：

```bash
claude mcp add --transport stdio --scope user cisp-mcp -- uv --directory /path/to/cisp-mcp run cisp-mcp
```

检查配置：

```bash
claude mcp list
claude mcp get cisp-mcp
```

进入 Claude Code 后输入：

```text
/mcp
```

看到 `cisp-mcp` connected 后即可使用。

示例问题：

```text
查询一下证通股份有限公司的工商照面信息。

查询一下证通股份有限公司的专利信息。

帮我从工商信息、知识产权、网站备案几个角度快速了解证通股份有限公司。
```

## 集成到 Codex CLI / Codex App

Codex CLI 和 Codex App 使用同一份 MCP 配置。生产远程服务配置如下：

```toml
[mcp_servers.cisp-mcp]
url = "https://mcp.example.com/mcp"
bearer_token_env_var = "CISP_API_KEY"
startup_timeout_sec = 20
tool_timeout_sec = 120
enabled = true
```

启动 Codex 前设置：

```bash
export CISP_API_KEY='<客户自己的CISP_API_KEY>'
```

本地开发可以使用 stdio 模式：

```bash
codex mcp add cisp-mcp -- uv --directory /path/to/cisp-mcp run cisp-mcp
```

检查配置：

```bash
codex mcp list
codex mcp get cisp-mcp
```

配置会写入：

```text
~/.codex/config.toml
```

对应的本地手动配置：

```toml
[mcp_servers.cisp-mcp]
command = "uv"
args = ["--directory", "/path/to/cisp-mcp", "run", "cisp-mcp"]
startup_timeout_sec = 20
tool_timeout_sec = 120
enabled = true
```

配置后重新打开 Codex App，或新建一个 thread，在 Codex 中输入：

```text
/mcp
```

确认 `cisp-mcp` 已连接。

## 集成到 OpenClaw（小龙虾）

OpenClaw 可以通过 `openclaw mcp set` 保存 MCP Server 定义。推荐使用 stdio 模式，让 OpenClaw 在需要时启动 `cisp-mcp`。

### 本地项目方式

先确保项目目录下已经配置好 `.env`，然后执行：

```bash
openclaw mcp set cisp-mcp '{"command":"uv","args":["--directory","/path/to/cisp-mcp","run","cisp-mcp"]}'
```

检查配置：

```bash
openclaw mcp list
openclaw mcp show cisp-mcp --json
```

如果 OpenClaw Gateway 已经在运行，保存 MCP 配置后建议重启 Gateway 或新建会话：

```bash
openclaw gateway restart
```

### 直接配置环境变量

如果不想依赖项目目录下的 `.env`，也可以把运行所需环境变量写入 OpenClaw MCP 配置：

```bash
openclaw mcp set cisp-mcp '{"command":"uv","args":["--directory","/path/to/cisp-mcp","run","cisp-mcp"],"env":{"CISP_ENDPOINT":"https://cisp.zenitera.com","CISP_REQUEST_URI":"/ectcispserver/api/entcreditapi/query","CISP_API_KEY":"填写自己的真实 API Key","CISP_TIMEOUT_SECONDS":"30","CISP_VERIFY_SSL":"true"}}'
```

### 直接从 GitHub 运行

如果不想本地 clone 项目，可以使用 `uvx` 从 GitHub 运行：

```bash
openclaw mcp set cisp-mcp '{"command":"uvx","args":["--from","git+https://github.com/fw-magic/cisp-mcp.git","cisp-mcp"],"env":{"CISP_ENDPOINT":"https://cisp.zenitera.com","CISP_REQUEST_URI":"/ectcispserver/api/entcreditapi/query","CISP_API_KEY":"填写自己的真实 API Key","CISP_TIMEOUT_SECONDS":"30","CISP_VERIFY_SSL":"true"}}'
```

配置完成后，可以在 OpenClaw 中直接提问：

```text
查询一下证通股份有限公司的工商照面信息。

查询证通股份有限公司和水滴科技服务有限公司的舆情信息。
```

## 集成到 WorkBuddy

生产环境进入“连接器 → 自定义连接器 → 配置 MCP”，填写：

```json
{
  "mcpServers": {
    "cisp-mcp": {
      "type": "streamable-http",
      "url": "https://mcp.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <客户自己的CISP_API_KEY>"
      },
      "disabled": false
    }
  }
}
```

WorkBuddy 未明确支持环境变量展开时，应使用其凭据输入框或直接填写 Key，不要填写字面量 `${CISP_API_KEY}`。

本地开发且 WorkBuddy 支持 stdio server 时，可以配置：

```json
{
  "mcpServers": {
    "cisp-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/cisp-mcp",
        "run",
        "cisp-mcp"
      ]
    }
  }
}
```

本地 HTTP 调试可以先手动启动：

```bash
uv run cisp-mcp --transport streamable-http
```

然后在 WorkBuddy 中配置 URL 和请求头：

```text
URL: http://127.0.0.1:8000/mcp
Authorization: Bearer <客户自己的CISP_API_KEY>
```

## 新增接口开发流程

后续如果要新增 CISP 产品接口：

1. 把 PDF 接口文档放到本地 `docs/` 目录。
2. 阅读基本信息、请求参数、返回字段和附录状态码。
3. 在 `src/cisp_mcp/interfaces.py` 中新增产品定义。
4. 在 `src/cisp_mcp/server.py` 中新增一个 `@mcp.tool()`。
5. 工具名格式建议为：`p产品号_英文语义名`，例如 `p0010010_query_business_profile`。
6. 更新 `scripts/smoke_test_mcp.py` 的 `EXPECTED_TOOLS`。
7. 运行 smoke test：

```bash
uv run python scripts/smoke_test_mcp.py
```

## 常见问题

### 1. 手动运行 `uv run cisp-mcp` 后终端不动，是不是卡住了？

不是。默认 stdio 模式会等待 MCP 客户端通过标准输入/输出通信，手动运行时看起来像停住。调试时请用：

```bash
uv run cisp-mcp --transport streamable-http
```

### 2. 真实调用报证书错误怎么办？

本地联调时可以临时设置：

```text
CISP_VERIFY_SSL=false
```

生产环境建议保持：

```text
CISP_VERIFY_SSL=true
```

## 安全说明

- 不要提交 `.env`。
- Streamable HTTP 生产入口必须使用 HTTPS。
- 不要在代码、README、日志或聊天消息中写入 API Key。
- Claude Code、Codex 优先通过环境变量管理 Key；WorkBuddy 优先使用凭据管理界面。
- Nginx 和应用日志不得记录 `Authorization` 或转发给 CISP 的 `X-API-Key`。
- HTTP 模式下每个请求都必须携带 Bearer Key；缺失或格式错误时返回 `401`。
- MCP 服务只做 Bearer格式校验；格式正确但已失效的 Key会在实际调用 CISP 时由 CISP 后台拒绝。
- 代理账号密码属于敏感信息；如果 `CISP_ENDPOINT_PROXY` 包含凭据，不得提交 Git或打印到日志。
