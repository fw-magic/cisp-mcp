from __future__ import annotations

import argparse
from typing import Any

from mcp.server.fastmcp import FastMCP

from .client import CispApiClient
from .config import load_settings
from .interfaces import (
    P0010010,
    P0010058,
    P0010068,
    P0010073,
    P0010074,
    P0010075,
    P0010076,
    P0010078,
    P0060007,
    P0060008,
)

mcp = FastMCP("CISP MCP", json_response=True)


def get_client() -> CispApiClient:
    return CispApiClient(load_settings())


def with_extra_params(params: dict[str, Any], extra_params: dict[str, Any] | None) -> dict[str, Any]:
    if extra_params:
        params.update(extra_params)
    return params


def require_one_of(params: dict[str, Any], names: tuple[str, ...]) -> None:
    for name in names:
        value = params.get(name)
        if isinstance(value, str):
            value = value.strip()
        if value:
            return
    else:
        readable = ", ".join(names)
        raise ValueError(f"At least one of these parameters is required: {readable}")


@mcp.tool()
async def p0010010_query_business_profile(
    ent_info: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业工商照面信息查询。根据企业名称、统一社会信用代码或工商注册号查询工商注册照面信息。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0010010.product_code,
        params=with_extra_params({"entInfo": ent_info}, extra_params),
    )


@mcp.tool()
async def p0010058_query_business_basic_deep(
    ent_name: str | None = None,
    credit_code: str | None = None,
    reg_no: str | None = None,
    org_code: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业工商基本信息查询（深度）。企业名称、统一社会信用代码、注册号、组织机构代码四选一。"""
    params = {
        "entName": ent_name,
        "creditCode": credit_code,
        "regNo": reg_no,
        "orgCode": org_code,
    }
    require_one_of(params, ("entName", "creditCode", "regNo", "orgCode"))
    client = get_client()
    return await client.query_product(
        prod_code=P0010058.product_code,
        params=with_extra_params(params, extra_params),
    )


@mcp.tool()
async def p0010068_fuzzy_search_company_name(
    ent_name: str,
    type: str | None = None,
    region_id: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业名称模糊查询（简版）。根据企业名称关键字查询最符合条件的企业名称。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0010068.product_code,
        params=with_extra_params(
            {
                "entName": ent_name,
                "type": type,
                "regionId": region_id,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0010073_query_trademark_info(
    ent_info: str,
    tm_reg_no: str | None = None,
    page_no: str | None = None,
    page_size: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业商标信息查询。通过企业名称或企业证件号查询商标信息。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0010073.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "tmRegNo": tm_reg_no,
                "pageNo": page_no,
                "range": page_size,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0010074_query_software_copyright_info(
    ent_info: str,
    page_no: str | None = None,
    page_size: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业软件著作权信息查询。根据企业名称、统一社会信用代码或注册号查询软件著作权信息。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0010074.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "pageNo": page_no,
                "range": page_size,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0010075_query_work_copyright_info(
    ent_info: str,
    pub_no: str | None = None,
    page_no: str | None = None,
    page_size: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业作品著作权信息查询。根据企业名称、工商注册号或统一社会信用代码查询作品著作权信息。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0010075.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "pubNo": pub_no,
                "pageNo": page_no,
                "range": page_size,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0010076_query_icp_filing_info(
    ent_info: str,
    page_no: str | None = None,
    page_size: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业 ICP 备案信息查询。根据企业名称、工商注册号或统一社会信用代码查询 ICP 备案信息。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0010076.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "pageNo": page_no,
                "range": page_size,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0010078_query_patent_info(
    ent_info: str,
    start_date: str | None = None,
    end_date: str | None = None,
    ptt_type: str | None = None,
    page_no: str | None = None,
    page_size: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业专利信息查询。根据企业名称查询以企业作为专利申请人的专利信息。日期格式 yyyy-MM-dd。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0010078.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "startDate": start_date,
                "endDate": end_date,
                "pttType": ptt_type,
                "pageNo": page_no,
                "range": page_size,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0060007_verify_business_two_elements(
    ent_name: str,
    reg_no: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业工商二要素验证。根据企业名称和统一社会信用代码/企业注册号验证是否匹配。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0060007.product_code,
        params=with_extra_params(
            {
                "entName": ent_name,
                "regNo": reg_no,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0060008_verify_business_three_elements(
    ent_name: str,
    reg_no: str,
    fr_name: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业工商三要素验证。根据企业名称、统一社会信用代码/注册号和法定代表人姓名验证是否一致。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0060008.product_code,
        params=with_extra_params(
            {
                "entName": ent_name,
                "regNo": reg_no,
                "frName": fr_name,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def query_cisp_product(
    prod_code: str,
    ent_info: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generic CISP JSON gateway query. Prefer product-specific tools when available."""
    client = get_client()
    return await client.query_by_product_code(
        prod_code=prod_code,
        ent_info=ent_info,
        extra_params=extra_params,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the CISP MCP server.")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="MCP transport to use. Use stdio for MCP hosts and streamable-http for Inspector.",
    )
    args = parser.parse_args()
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
