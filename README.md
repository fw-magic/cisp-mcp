# cisp-mcp

`cisp-mcp` 是一个用 Python 编写的 CISP API MCP 服务，用于把 CISP 企业信息接口封装成可被大模型调用的 MCP tools。

项目使用 `uv` 管理依赖，基于 `mcp` Python SDK 的 `FastMCP` 开发，通过 CISP AI 网关 JSON 接口访问后端 API。

## 项目能力

- 支持 Claude Code、Codex、Codex App、WorkBuddy 等 MCP 客户端接入。
- 每个 CISP 产品接口对应一个独立 MCP tool，工具名包含产品号，方便排查和定位。
- 自动补充 `prodCode`，调用方只需要传业务参数。
- 对 CISP 返回结果做统一归一化，保留原始返回 `raw_response`。
- 支持本地 smoke test，验证 MCP 服务和工具注册是否正常。

## 技术栈

- Python `>=3.11`
- uv
- MCP Python SDK / FastMCP
- httpx
- python-dotenv

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

### 2. 安装 uv

如果本机已经有 `uv`，可以跳过：

```bash
uv --version
```

如果没有，可以按 uv 官方方式安装，或使用你本机已有的 Python 环境安装。

### 3. 安装依赖

```bash
uv sync
```

### 4. 配置环境变量

复制模板：

```bash
cp .env.example .env
```

编辑 `.env`：

```text
CISP_ENDPOINT=https://cisp.zenitera.com
CISP_REQUEST_URI=/ectcispserver/api/entcreditapi/query
CISP_API_KEY=替换成真实 API Key
CISP_TIMEOUT_SECONDS=30
CISP_VERIFY_SSL=true
```

## 本地运行和调试

### smoke test

这个测试只验证 MCP 服务能否启动、`tools/list` 是否能看到所有工具，不会调用真实 CISP API，也不会消耗接口次数。

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
Total: 11
Smoke test passed.
```

### stdio 模式

stdio 是给 Claude Code、Codex、WorkBuddy 等 MCP 客户端使用的模式。

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
```

## 工具列表

| 产品码 | 接口名称 | MCP tool |
| --- | --- | --- |
| `P0010010` | 企业工商照面信息查询 | `p0010010_query_business_profile` |
| `P0010058` | 企业工商基本信息查询（深度） | `p0010058_query_business_basic_deep` |
| `P0010068` | 企业名称模糊查询（简版） | `p0010068_fuzzy_search_company_name` |
| `P0010073` | 企业商标信息查询 | `p0010073_query_trademark_info` |
| `P0010074` | 企业软件著作权信息查询 | `p0010074_query_software_copyright_info` |
| `P0010075` | 企业作品著作权信息查询 | `p0010075_query_work_copyright_info` |
| `P0010076` | 企业 ICP 备案信息查询 | `p0010076_query_icp_filing_info` |
| `P0010078` | 企业专利信息查询 | `p0010078_query_patent_info` |
| `P0060007` | 企业工商二要素验证 | `p0060007_verify_business_two_elements` |
| `P0060008` | 企业工商三要素验证 | `p0060008_verify_business_three_elements` |
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
- `matchList`

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

推荐使用 stdio 模式，让 Claude Code 自动启动 MCP 服务。

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

Codex CLI 和 Codex App 使用同一份 MCP 配置。推荐用命令添加：

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

也可以手动配置：

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

## 集成到 WorkBuddy

如果 WorkBuddy 支持 MCP stdio server，推荐配置：

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

如果 WorkBuddy 只支持 HTTP MCP，可以先手动启动：

```bash
uv run cisp-mcp --transport streamable-http
```

然后在 WorkBuddy 中配置：

```text
http://127.0.0.1:8000/mcp
```

建议优先使用 stdio。stdio 不需要常驻端口，客户端会自动启动和管理进程。

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
- 不要在代码、README、MCP 客户端配置里写死 API Key。
- 建议通过环境变量或 `.env` 管理敏感配置。
