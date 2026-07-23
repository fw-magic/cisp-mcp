# Three CISP Interfaces MCP Integration Design

## Goal

Add product-specific MCP tools for the three CISP products that have local PDF documentation but are not yet integrated:

- `P0020021` 企业单点关联信息查询
- `P0110003` 企业荣誉资质信息查询
- `P0010084` 企业许可信息查询

The tools must follow the existing `FastMCP` integration pattern, preserve the complete CISP response, and expose each product's most useful list as a top-level shortcut.

## Tool Contracts

### P0020021 企业单点关联信息查询

Tool name:

`p0020021_query_single_point_related_info`

Parameters:

- `ent_info: str`: enterprise name, registration number, organization code, or unified social credit code.
- `relation_direction: Literal["1", "2", "3"]`: required relation scope selected by the model from the user's natural-language intent.
- `extra_params: dict[str, Any] | None`: optional passthrough parameters, consistent with existing tools.

Intent mapping:

- `"1"`: query investment and position relations.
- `"2"`: query investment relations only.
- `"3"`: query position relations only.

The tool description must explain this mapping so the model chooses the code. End users are not expected to know or provide the numeric value directly. If the user's intent does not distinguish investment, position, or both, the model should clarify before invoking the tool.

Request mapping:

```json
{
  "prodCode": "P0020021",
  "entInfo": "<ent_info>",
  "relationDirection": "<relation_direction>"
}
```

Response configuration:

- Status field: `P0020021Status`
- Data field: `P0020021Data`
- Shortcut field: `entInvList`
- The remaining `basicInfoList`, `shaInvAndPos`, `frInvAndPos`, and `manInvAndPos` values remain available under `data` and `raw_response`.

### P0110003 企业荣誉资质信息查询

Tool name:

`p0110003_query_honor_qualification_info`

Parameters:

- `ent_info: str`: enterprise name, registration number, unified social credit code, or enterprise ID.
- `extra_params: dict[str, Any] | None`: optional passthrough parameters.

Request mapping:

```json
{
  "prodCode": "P0110003",
  "entInfo": "<ent_info>"
}
```

Response configuration:

- Status field: `P0110003Status`
- Data field: `P0110003Data`
- Shortcut field: `itemNameList`

### P0010084 企业许可信息查询

Tool name:

`p0010084_query_license_info`

Parameters:

- `ent_info: str`: enterprise name, unified social credit code, or registration number.
- `license_type: str | None`: optional CISP license category. Supported document values are `gs`, `zjzj`, `syj-xk`, `syj-old`, `syj-drug`, `yjh`, `bjh`, `gdzj-gy`, `gdzj-dsj`, `pwxk`, `pwxk-dj`, and `ylxk`.
- `province: str | None`: optional province name used only for `ylxk` medical-license queries.
- `page_no: str | None`: optional page number; CISP defaults to page 1.
- `page_size: str | None`: optional page size; mapped to CISP's `range` parameter, whose default is 10.
- `extra_params: dict[str, Any] | None`: optional passthrough parameters.

Request mapping:

```json
{
  "prodCode": "P0010084",
  "entInfo": "<ent_info>",
  "type": "<license_type>",
  "province": "<province>",
  "pageNo": "<page_no>",
  "range": "<page_size>"
}
```

Unset optional values are removed by the existing `clean_payload` behavior.

Response configuration:

- Status field: `P0010084Status`
- Data field: `P0010084Data`
- Shortcut field: `detailList`
- Pagination metadata remains available as `data.detailListMeta`.

## Architecture and Files

The implementation follows the existing product-tool architecture:

1. Add three `CispInterface` entries and exported constants in `src/cisp_mcp/interfaces.py`.
2. Import those constants and register three `@mcp.tool()` async functions in `src/cisp_mcp/server.py`.
3. Reuse `CispApiClient.query_product`, `with_extra_params`, `clean_payload`, and `normalize_interface_response` without changing the transport architecture.
4. Add focused unit tests for interface metadata and request mappings.
5. Add the three tool names to `scripts/smoke_test_mcp.py`.
6. Update `README.md` with the tool table, shortcut fields, request examples, and extension count.

No new client class, endpoint, authentication method, or environment variable is required.

## Validation and Error Handling

- `relation_direction` uses a `Literal["1", "2", "3"]` annotation so the generated MCP schema restricts it to documented values.
- `ent_info` remains required for all three tools.
- Optional blank strings are removed by `clean_payload`.
- Existing HTTP errors and CISP result normalization behavior remain unchanged.
- Existing `extra_params` behavior remains available for undocumented forward-compatible parameters.

## Testing

Tests will use the standard library and existing project dependencies:

- Assert all three interface definitions have the correct product, status, data, and shortcut fields.
- Replace `get_client` with a recording fake and call each async tool.
- Assert the exact product code and camelCase request payload produced by each tool.
- Assert omitted optional license parameters are accepted.
- Verify the generated MCP registry includes the three new tool names.
- Run Python compilation and the existing HTTP smoke test on a free alternate port.

No real CISP product request is required for automated verification, so tests do not consume API quota.

## Documentation Source

The contract is based on the PDFs placed under `docs/`:

- `企业单点关联信息查询.pdf`
- `企业荣誉资质信息查询.pdf`
- `企业许可信息查询.pdf`
