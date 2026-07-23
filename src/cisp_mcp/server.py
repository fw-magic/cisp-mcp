from __future__ import annotations

import argparse
import json
import os
from typing import Any, Literal

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
    P0010084,
    P0020021,
    P0050007,
    P0050008,
    P0060007,
    P0060008,
    P0110003,
)

def read_mcp_port() -> int:
    return int(os.getenv("PORT") or os.getenv("MCP_PORT") or "8000")


mcp = FastMCP(
    "CISP MCP",
    json_response=True,
    host=os.getenv("MCP_HOST", "127.0.0.1"),
    port=read_mcp_port(),
)


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


def normalize_public_opinion_ent_name(value: list[str] | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        if value.startswith("["):
            return value
        return json.dumps([value], ensure_ascii=False)

    cleaned = [item.strip() for item in value if item and item.strip()]
    if not cleaned:
        return None
    return json.dumps(cleaned, ensure_ascii=False)


def extract_first_value(value: Any, keys: tuple[str, ...]) -> str | None:
    if isinstance(value, dict):
        for key in keys:
            item = value.get(key)
            if item:
                return str(item)
        for item in value.values():
            found = extract_first_value(item, keys)
            if found:
                return found
    if isinstance(value, list):
        for item in value:
            found = extract_first_value(item, keys)
            if found:
                return found
    return None


def parse_positive_int(value: int | str | None, default: int) -> int:
    if value is None:
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


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
async def p0010084_query_license_info(
    ent_info: str,
    license_type: str | None = None,
    province: str | None = None,
    page_no: str | None = None,
    page_size: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业许可信息查询。

    查询工商、质检、食药监、金融监管、环保、医疗等许可信息。
    license_type 可选值包括 gs、zjzj、syj-xk、syj-old、syj-drug、yjh、
    bjh、gdzj-gy、gdzj-dsj、pwxk、pwxk-dj、ylxk。
    province 仅在 license_type 为 ylxk（医疗许可）时使用。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0010084.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "type": license_type,
                "province": province,
                "pageNo": page_no,
                "range": page_size,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0020021_query_single_point_related_info(
    ent_info: str,
    relation_direction: Literal["1", "2", "3"],
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业单点关联信息查询。

    根据用户意图选择 relation_direction：
    "1" 表示同时查询投资和任职关系；
    "2" 表示只查询投资关系；
    "3" 表示只查询任职关系。
    最终用户无需了解码值，由模型根据“投资”“任职”或“两者都查”的自然语言选择。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0020021.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "relationDirection": relation_direction,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0050007_query_public_opinion_list(
    ent_name: list[str] | str | None = None,
    group_name: str | None = None,
    info_label: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    info_emotion: str | None = None,
    page_no: str | None = None,
    page_size: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业舆情信息列表查询。ent_name 使用企业名称数组，如 ["证通股份有限公司"]，支持多个企业。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0050007.product_code,
        params=with_extra_params(
            {
                "entName": normalize_public_opinion_ent_name(ent_name),
                "groupName": group_name,
                "infoLabel": info_label,
                "startDate": start_date,
                "endDate": end_date,
                "infoEmotion": info_emotion,
                "pageNo": page_no,
                "range": page_size,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0050008_query_public_opinion_detail(
    ent_name: list[str] | str | None = None,
    entry_id: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业舆情信息详情查询。优先使用 entry_id；只传 ent_name 时会先查列表，再取第一条舆情详情。"""
    client = get_client()
    if not entry_id and ent_name:
        list_result = await client.query_product(
            prod_code=P0050007.product_code,
            params={
                "entName": normalize_public_opinion_ent_name(ent_name),
                "pageNo": "1",
                "range": "1",
            },
        )
        entry_id = extract_first_value(list_result.get("infoList"), ("entryId",))

    params = {
        "entryId": entry_id,
        "entName": normalize_public_opinion_ent_name(ent_name),
    }
    require_one_of(params, ("entryId",))
    return await client.query_product(
        prod_code=P0050008.product_code,
        params=with_extra_params(params, extra_params),
    )


@mcp.tool()
async def p0050007_p0050008_query_public_opinion_info(
    ent_name: list[str] | str,
    group_name: str | None = None,
    info_label: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    info_emotion: str | None = None,
    page_no: str | None = "1",
    page_size: str | None = "10",
    max_details: int | None = 10,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业舆情信息查询。先查 P0050007 列表，再用 entryId 和 ent_name 调 P0050008 查询详情。"""
    client = get_client()
    normalized_ent_name = normalize_public_opinion_ent_name(ent_name)
    list_result = await client.query_product(
        prod_code=P0050007.product_code,
        params=with_extra_params(
            {
                "entName": normalized_ent_name,
                "groupName": group_name,
                "infoLabel": info_label,
                "startDate": start_date,
                "endDate": end_date,
                "infoEmotion": info_emotion,
                "pageNo": page_no,
                "range": page_size,
            },
            extra_params,
        ),
    )

    info_list = list_result.get("infoList")
    if not isinstance(info_list, list):
        info_list = []

    detail_limit = min(parse_positive_int(max_details, 10), len(info_list))
    details = []
    for list_item in info_list[:detail_limit]:
        entry_id = extract_first_value(list_item, ("entryId",))
        if not entry_id:
            details.append(
                {
                    "entry_id": None,
                    "list_item": list_item,
                    "success": False,
                    "error": "entryId not found in list item",
                }
            )
            continue

        detail_result = await client.query_product(
            prod_code=P0050008.product_code,
            params={
                "entryId": entry_id,
                "entName": normalized_ent_name,
            },
        )
        details.append(
            {
                "entry_id": entry_id,
                "list_item": list_item,
                "success": detail_result.get("success"),
                "detail": detail_result,
            }
        )

    return {
        "product_code": "P0050007+P0050008",
        "interface_name": "企业舆情信息查询（列表+详情）",
        "success": bool(list_result.get("success")) and all(item.get("success") for item in details),
        "list_success": list_result.get("success"),
        "list_has_result": list_result.get("has_result"),
        "list_result": list_result,
        "infoList": info_list,
        "detail_count": len(details),
        "details": details,
    }


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
async def p0110003_query_honor_qualification_info(
    ent_info: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业荣誉资质信息查询。根据企业名称、注册号、统一社会信用代码或企业 ID 查询荣誉、奖励和认定信息。"""
    client = get_client()
    return await client.query_product(
        prod_code=P0110003.product_code,
        params=with_extra_params({"entInfo": ent_info}, extra_params),
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
