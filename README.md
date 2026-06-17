# cisp-mcp

`cisp-mcp` is a Python MCP server for exposing CISP API calls to LLM clients.

The first tool mirrors the Java JSON gateway example:

- endpoint: `https://cisp.zenitera.com`
- path: `/ectcispserver/api/entcreditapi/query`
- auth header: `X-API-Key`
- body type: `application/json;charset=UTF-8`

## 1. Create the project

```bash
cd "/Users/fangwei/Documents/MCP Server"
uv init cisp-mcp --package --python 3.11
cd cisp-mcp
uv add "cryptography<49" "mcp[cli]" httpx python-dotenv
```

`cryptography<49` is pinned because this Intel Mac needs a macOS x86_64/universal2 wheel. The latest `cryptography 49.0.0` resolved by `mcp` does not provide a matching macOS x86_64 wheel here, so `uv` falls back to a slow source build.

## 2. Configure secrets

```bash
cp .env.example .env
```

Then edit `.env` and fill in `CISP_API_KEY`.

Do not commit `.env` or hard-code API keys in source files.

## 3. Run locally

Use stdio when an MCP host starts the server:

```bash
uv run cisp-mcp
```

Use Streamable HTTP when debugging with MCP Inspector:

```bash
uv run cisp-mcp --transport streamable-http
```

The default HTTP endpoint is:

```text
http://localhost:8000/mcp
```

Or start the official MCP Inspector directly:

```bash
uv run mcp dev server.py:mcp --with-editable .
```

## 4. Tools exposed

The product-specific tools are generated from the PDF documents under `docs/`.

| Product code | API document | MCP tool |
| --- | --- | --- |
| `P0010010` | 企业工商照面信息查询 | `p0010010_query_business_profile` |
| `P0010058` | 企业工商基本信息查询（深度） | `p0010058_query_business_basic_deep` |
| `P0010068` | 企业名称模糊查询（简版） | `p0010068_fuzzy_search_company_name` |
| `P0010073` | 企业商标信息查询 | `p0010073_query_trademark_info` |
| `P0010074` | 企业软件著作权信息查询 | `p0010074_query_software_copyright_info` |
| `P0010075` | 企业作品著作权信息查询 | `p0010075_query_work_copyright_info` |
| `P0010076` | 企业ICP备案信息查询 | `p0010076_query_icp_filing_info` |
| `P0010078` | 企业专利信息查询 | `p0010078_query_patent_info` |
| `P0060007` | 企业工商二要素验证 | `p0060007_verify_business_two_elements` |
| `P0060008` | 企业工商三要素验证 | `p0060008_verify_business_three_elements` |

Each product-specific tool fixes its own `prodCode`, so the LLM only needs to provide business parameters.

Example:

```json
{
  "ent_info": "证通股份有限公司"
}
```

Optional fields that are not modeled yet can be passed through `extra_params`.

The normalized response includes both model-friendly fields and the original response:

- `success`: `resultCode == "00000"`
- `has_result`: product status is `4`
- `result_code_desc`: appendix description for `resultCode`
- `product_status_desc`: appendix description for product status
- product shortcut list, for example `basicList`, `fuzzyList`, `brandList`, `matchList`, `summaryInfo`
- `raw_response`: original CISP response

### `query_cisp_product`

Generic JSON gateway query for debugging or products that do not have a dedicated tool yet.

```json
{
  "prod_code": "P0010010",
  "ent_info": "证通股份有限公司"
}
```

## 5. Add more CISP APIs later

For each new API:

1. Put the interface document in `docs/`.
2. Add the product definition and appendix mappings in `src/cisp_mcp/interfaces.py`.
3. Add one method in `src/cisp_mcp/client.py`.
4. Add one `@mcp.tool()` wrapper in `src/cisp_mcp/server.py`.
5. Keep API keys and endpoint config in environment variables.

Current convention:

- Tool names start with the lower-case product code, for example `p0010010_query_business_profile`.
- PDF field names stay in the outgoing payload, for example `entInfo`, `regNo`, `pageNo`.
- MCP argument names use Python-friendly snake_case, for example `ent_info`, `reg_no`, `page_no`.
- The PDF field `range` is exposed as `page_size` and mapped back to `range` before sending the request.

## 6. Test locally

Run a no-cost smoke test. It starts the MCP server locally, checks `tools/list`, verifies all 12 tools are registered, and then stops the server.

```bash
uv run python scripts/smoke_test_mcp.py
```

For manual business testing, start the service:

```bash
uv run cisp-mcp --transport streamable-http
```

Then open MCP Inspector:

```bash
npx -y @modelcontextprotocol/inspector
```

Connect with:

```text
Transport: Streamable HTTP
URL: http://127.0.0.1:8000/mcp
```

Use `Tools` to call each product-specific tool. These calls hit the real CISP API and may consume quota.
