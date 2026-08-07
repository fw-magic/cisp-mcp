from __future__ import annotations

import argparse
import hashlib
import json
import os
from typing import Annotated, Any, Literal

from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import AccessToken
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
from pydantic import Field, StringConstraints

from .client import CispApiClient
from .config import load_settings
from .interfaces import (
    P0010010,
    P0010058,
    P0010059,
    P0010068,
    P0010073,
    P0010074,
    P0010075,
    P0010076,
    P0010078,
    P0010084,
    P0020014,
    P0020019,
    P0020021,
    P0020023,
    P0020024,
    P0020031,
    P0020044,
    P0020129,
    P0050007,
    P0050008,
    P0060007,
    P0060008,
    P0090001,
    P0090008,
    P0090011,
    P0090012,
    P0110003,
    P0130025,
    P0130036,
    P0130038,
    P0210004,
    P0980006,
    P0980008,
    P0980023,
    P0980033,
    P0990022,
)


P0010059Type = Literal[
    "basic",
    "person",
    "shareholder",
    "originalShareholder",
    "alter",
    "filiation",
    "exception",
    "liquidation",
    "mortAlt",
    "mortDetail",
    "mortCan",
    "mortPriClaSec",
    "mortguaInfo",
    "mortOrg",
    "mortReg",
    "sharFroz",
    "sharePledg",
    "sharePledgAlt",
    "sharePledgCan",
    "changeRecords",
    "changeStockRights",
    "basicInformation",
    "provideGuarantee",
    "foreignInvestment",
    "yearReportPaidUpCapital",
    "socialInsurance",
    "yearReportSubCapitals",
    "websiteOrOnline",
    "illegal",
    "caseCheck",
    "caseRandomCheck",
    "companyIpr",
    "companyCancelEasy",
]

P0130025IndicatorType = Literal[
    "1",
    "2",
]

P0130036LandType = Literal[
    "tdgy",
    "tdcr",
    "dkgs",
    "tddy",
]

P0130038NicLevel = Literal[
    "n1",
    "n2",
    "n3",
    "n4",
]

P0130038RegionLevel = Literal[
    "r0",
    "r1",
    "r2",
    "r3",
]

P0130038AnalysisType = Literal[
    "finRank",
    "finRankStock",
    "entRegionRank",
    "locfin",
    "indLocOpr",
    "indLocOprFin",
    "property",
    "financialRegionRank",
]

P0210004FinancialType = Literal[
    "rgincome",
    "rgcashflow",
    "fncmfnin",
    "rgbalance",
    "mainfinadata",
    "balance",
    "income",
    "cashflow",
]

P0020014RelationType = Literal[
    "telSus",
    "contactSus",
    "registSus",
    "websiteSus",
    "emailSus",
    "domainSus",
]

RelationshipWeight = Literal[
    "0",
    "1",
    "2",
]

P0020019PathType = Literal[
    "0",
    "1",
]

P0020019FinalFlag = Literal[
    "0",
    "1",
]

P0020023Level = Literal[
    "1",
    "2",
    "3",
    "4",
    "5",
]

UboQueryEdition = Literal[
    "detailed",
    "standard",
]

NonBlankString = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]

EnterpriseIdentifier = Annotated[
    NonBlankString,
    Field(
        description="企业全称、统一社会信用代码或工商注册号；不得传空字符串。",
        examples=["阳光电源股份有限公司", "913401001492097421"],
    ),
]

NameOrCreditCodeIdentifier = Annotated[
    NonBlankString,
    Field(
        description="企业全称或统一社会信用代码；不得传空字符串。",
        examples=["阳光电源股份有限公司", "913401001492097421"],
    ),
]

UboEnterpriseIdentifier = Annotated[
    NonBlankString,
    Field(
        description=(
            "企业全称、统一社会信用代码或工商注册号；映射到底层 entName 字段，"
            "不得传空字符串。"
        ),
        examples=["招商银行股份有限公司", "9144030010001686XA"],
    ),
]

CompanyCollection = Annotated[
    Annotated[
        list[NonBlankString],
        Field(min_length=1, max_length=10),
    ]
    | NonBlankString,
    Field(
        description=(
            "企业全称、统一社会信用代码或工商注册号；可传非空字符串、"
            "中英文逗号分隔字符串或 1 至 10 项的字符串数组。"
        ),
        examples=[
            ["阳光电源股份有限公司", "阳光新能源开发股份有限公司"],
            "阳光电源股份有限公司,阳光新能源开发股份有限公司",
        ],
    ),
]

OptionalCompanyCollection = Annotated[
    CompanyCollection | None,
    Field(
        description=(
            "待查询的企业主体；可传非空字符串、中英文逗号分隔字符串或最多 10 项的"
            "字符串数组。与 person_names 至少提供一项，两者合计最多 10 个主体。"
        ),
        examples=[["招商银行股份有限公司", "招商局集团有限公司"]],
    ),
]

OptionalPersonCollection = Annotated[
    Annotated[
        list[NonBlankString],
        Field(min_length=1, max_length=10),
    ]
    | NonBlankString
    | None,
    Field(
        description=(
            "待查询的自然人；每项使用“任职企业全称-姓名”格式。可传非空字符串、"
            "中英文逗号分隔字符串或最多 10 项的字符串数组。与 ent_info 至少提供一项，"
            "两者合计最多 10 个主体。"
        ),
        examples=[["阳光电源股份有限公司-曹仁贤"]],
    ),
]

RelationshipDepth = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^[1-9]\d*$"),
    Field(
        description=(
            "关系查询深度，使用正整数字符串；默认 5。为控制结果规模，股权分析建议"
            "先用 2，不足时再逐级增加。"
        ),
        examples=["2", "5"],
    ),
]

RelationshipWeightParameter = Annotated[
    RelationshipWeight,
    Field(
        description="关系范围：0=投资和任职，1=仅任职，2=仅投资。",
        examples=["2"],
    ),
]

SuspectedRelationshipTypeParameter = Annotated[
    P0020014RelationType | None,
    Field(
        description=(
            "疑似关系类型：telSus=同电话，contactSus=同年报地址，"
            "registSus=同注册地址，websiteSus=同网站，emailSus=同邮箱，"
            "domainSus=同邮箱域名。不传时由底层产品决定返回范围。"
        ),
        examples=["contactSus"],
    ),
]

ControllerPathTypeParameter = Annotated[
    P0020019PathType,
    Field(
        description="控制路径返回方式：0=完整路径，1=简化路径；默认 0。",
        examples=["0"],
    ),
]

ControllerFinalFlagParameter = Annotated[
    P0020019FinalFlag,
    Field(
        description=(
            "控制路径穿透方式：0=返回常规企业级控制候选，1=继续穿透到底层自然人或"
            "国资终点；默认 0。"
        ),
        examples=["1"],
    ),
]

EquityPenetrationLevelParameter = Annotated[
    P0020023Level,
    Field(
        description="向上股东和向下投资的穿透层级：1 至 5，默认 3。",
        examples=["3", "5"],
    ),
]

EquityRatioThresholdParameter = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=r"^(?:100(?:\.0+)?|(?:[0-9]|[1-9][0-9])(?:\.\d+)?)$",
    ),
    Field(
        description=(
            "持股比例过滤阈值，使用 0 至 100 的数字字符串且不带百分号；按产品文档，"
            "只返回持股比例大于等于该值的企业股东节点，默认 5。"
        ),
        examples=["5", "0", "30.5"],
    ),
]

UboQueryEditionParameter = Annotated[
    UboQueryEdition,
    Field(
        description=(
            "最终受益人产品版本：detailed=详版 P0090001，适合完整 UBO 报告、"
            "审计留档和关键管理人员兜底；standard=非详版 P0090012，适合快速识别、"
            "独立互证或需要 bnfCat 判定依据时。由 AI 按任务目的选择。"
        ),
        examples=["detailed", "standard"],
    ),
]

UboIncludePathsParameter = Annotated[
    bool,
    Field(
        description=(
            "是否返回股权穿透路径。standard 模式下设为 false 会向底层发送 "
            "onlyFinalBef=1，仅返回最终受益人；detailed 模式固定包含路径，必须为 true。"
        ),
        examples=[True, False],
    ),
]

AdvancedExtraParams = Annotated[
    dict[str, Any] | None,
    Field(
        description=(
            "仅用于产品文档未暴露的高级 camelCase 参数；不得重复或覆盖本工具已声明的"
            "核心请求字段。通常保持为空。"
        ),
        examples=[{}],
    ),
]


def read_mcp_port() -> int:
    return int(os.getenv("PORT") or os.getenv("MCP_PORT") or "8000")


class CispApiKeyTokenVerifier:
    """Accept a CISP API key as the MCP Bearer credential.

    The CISP API remains the authority that determines whether the opaque key is
    active and billable. Locally we only reject malformed credentials and use a
    one-way fingerprint as the MCP principal so the raw key is never used as an
    identity or written to logs.
    """

    async def verify_token(self, token: str) -> AccessToken | None:
        if not token or token != token.strip() or len(token) > 4096:
            return None
        if any(character.isspace() or ord(character) < 0x20 for character in token):
            return None

        fingerprint = hashlib.sha256(token.encode("utf-8")).hexdigest()
        principal = f"cisp-key:{fingerprint[:24]}"
        return AccessToken(
            token=token,
            client_id=principal,
            subject=principal,
            scopes=["cisp:query"],
        )


mcp = FastMCP(
    "CISP MCP",
    instructions=(
        "CISP 企业数据查询工具。若目标工具要求 eid 或 entId，但用户只提供了企业名称，"
        "应先调用 p0010010_query_business_profile，将企业名称传入 ent_info，"
        "从 orgName 准确匹配的 basicList[].entId 获取企业内部标识，再传给目标工具。"
        "不得根据统一社会信用代码或其他字段自行推算 eid/entId。"
    ),
    json_response=True,
    host=os.getenv("MCP_HOST", "127.0.0.1"),
    port=read_mcp_port(),
    token_verifier=CispApiKeyTokenVerifier(),
    auth=AuthSettings(
        issuer_url=os.getenv("CISP_ENDPOINT", "https://cisp.zenitera.com"),
        required_scopes=["cisp:query"],
        resource_server_url=None,
    ),
)


def get_client() -> CispApiClient:
    access_token = get_access_token()
    request_api_key = access_token.token if access_token is not None else None
    return CispApiClient(load_settings(api_key=request_api_key))


def with_extra_params(params: dict[str, Any], extra_params: dict[str, Any] | None) -> dict[str, Any]:
    if extra_params:
        params.update(extra_params)
    return params


def with_guarded_extra_params(
    params: dict[str, Any],
    extra_params: dict[str, Any] | None,
    protected_fields: tuple[str, ...],
) -> dict[str, Any]:
    if not extra_params:
        return params

    conflicts = sorted(set(extra_params).intersection(protected_fields))
    if conflicts:
        readable = ", ".join(conflicts)
        raise ValueError(
            f"extra_params must not override declared core parameters: {readable}"
        )

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


def require_exactly_one_of(params: dict[str, Any], names: tuple[str, ...]) -> None:
    provided = []
    for name in names:
        value = params.get(name)
        if isinstance(value, str):
            value = value.strip()
        if value:
            provided.append(name)

    if len(provided) != 1:
        readable = ", ".join(names)
        raise ValueError(f"Exactly one of these parameters is required: {readable}")


def normalize_string_list(value: list[str] | None) -> str | None:
    if not value:
        return None
    cleaned = [item.strip() for item in value if item and item.strip()]
    return ",".join(cleaned) or None


def normalize_comma_separated(value: list[str] | str | None) -> str | None:
    if value is None:
        return None
    items = value if isinstance(value, list) else value.replace("，", ",").split(",")
    cleaned = [item.strip() for item in items if item and item.strip()]
    return ",".join(cleaned) or None


def require_at_most_items(value: str | None, maximum: int, parameter: str) -> None:
    if value and len(value.split(",")) > maximum:
        raise ValueError(f"{parameter} accepts at most {maximum} comma-separated items")


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
    """企业工商照面信息查询。

    根据企业名称、统一社会信用代码或工商注册号查询工商注册照面信息及历史名称信息。
    返回的 basicList[].entId 是 CISP 企业内部标识：当其他工具要求 eid 或 entId、
    而用户只提供企业名称时，应优先调用本工具，并从 orgName 准确匹配的记录中取 entId。
    不得根据统一社会信用代码或其他字段自行推算 eid/entId。
    """
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
    """企业工商基本信息查询（深度）。

    根据企业名称、工商注册号、统一社会信用代码或组织机构代码查询企业深度工商信息；
    企业名称、统一社会信用代码、注册号、组织机构代码四选一。
    """
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
async def p0010059_query_business_basic_brief(
    ent_name: str | None = None,
    credit_code: str | None = None,
    reg_no: str | None = None,
    org_code: str | None = None,
    types: list[P0010059Type] | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业工商基本信息查询（简项）。

    根据企业名称、工商注册号、统一社会信用代码或组织机构代码查询指定类型的企业工商信息。
    ent_name、credit_code、reg_no、org_code 严格四选一。
    types 用于选择工商照面、主要人员、股东、变更、年报和风险等数据类型；
    不传 types 时由底层产品决定返回范围。
    """
    params = with_extra_params(
        {
            "entName": ent_name,
            "creditCode": credit_code,
            "regNo": reg_no,
            "orgCode": org_code,
            "type": normalize_string_list(types),
        },
        extra_params,
    )
    require_exactly_one_of(params, ("entName", "creditCode", "regNo", "orgCode"))
    client = get_client()
    return await client.query_product(
        prod_code=P0010059.product_code,
        params=params,
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
    """企业软件著作权信息查询。根据企业名称、统一社会信用代码或注册号查询企业软件著作权信息。"""
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
    """企业作品著作权信息查询。根据企业名称、工商注册号或统一社会信用代码查询企业作品著作权信息。"""
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
    """企业 ICP 备案信息查询。根据企业名称、工商注册号或统一社会信用代码查询企业 ICP 备案信息。"""
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

    根据企业名称、统一社会信用代码或注册号查询工商、质检、食药监、金融监管、
    环保、医疗等许可信息。
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
async def p0020014_query_suspected_relationships(
    ent_info: EnterpriseIdentifier,
    relation_type: SuspectedRelationshipTypeParameter = None,
    extra_params: AdvancedExtraParams = None,
) -> dict[str, Any]:
    """企业疑似关系信息查询。

    根据企业名称、统一社会信用代码或注册号查询疑似关联企业。
    relation_type 可选：telSus=同电话、contactSus=同年报地址、
    registSus=同注册地址、websiteSus=同网站、emailSus=同邮箱、
    domainSus=同邮箱域名；不传时由底层产品决定返回范围。
    结果位于 data.suspectList[]：sus.<关系类型> 是目标企业被匹配的电话、地址、
    网站、邮箱或域名值；相应同名数组（如 telSus、registSus）是疑似关联候选，
    relationContent 是关联依据。候选数组可能为空；domainSus 结果量可能很大。
    这些结果属于关联线索，不应直接表述为已确认的控制或交易关系。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0020014.product_code,
        params=with_guarded_extra_params(
            {
                "entInfo": ent_info,
                "type": relation_type,
            },
            extra_params,
            ("entInfo", "type"),
        ),
    )


@mcp.tool()
async def p0020019_query_suspected_controller(
    ent_info: EnterpriseIdentifier,
    path_type: ControllerPathTypeParameter = "0",
    final_flag: ControllerFinalFlagParameter = "0",
    extra_params: AdvancedExtraParams = None,
) -> dict[str, Any]:
    """企业疑似实际控制人信息查询。

    根据企业名称、统一社会信用代码或注册号查询疑似实际控制人和控制路径。
    path_type：0=完整路径，1=简化路径；final_flag：0=常规结果，
    1=将路径继续穿透到底层。默认查询完整路径且不强制穿透到底层。
    data.controlNodeList[] 给出疑似控制节点及间接控制比例 percent；
    data.linkList[] 给出 startId、endId、direction 和 directPercent；
    data.rootNodeList[] 与 data.nodeList[] 用于还原路径。实测 direction=-1 时通常需将
    endId 作为持股方、startId 作为被投企业，且 linkList 可能重复相同边，使用前应
    结合节点名称校验方向并去重。结论为“疑似”口径，应与工商股东、最终受益人和
    其他控制权产品交叉验证。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0020019.product_code,
        params=with_guarded_extra_params(
            {
                "entInfo": ent_info,
                "type": path_type,
                "finalFlag": final_flag,
            },
            extra_params,
            ("entInfo", "type", "finalFlag"),
        ),
    )


@mcp.tool()
async def p0020021_query_single_point_related_info(
    ent_info: str,
    relation_direction: Literal["1", "2", "3"],
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业单点关联信息查询。

    根据企业名称、注册号、组织机构代码或统一社会信用代码查询企业投资和任职关联信息。
    根据用户意图选择 relation_direction：
    "1" 表示同时查询投资和任职关系；
    "2" 表示只查询投资关系；
    "3" 表示只查询任职关系。
    最终用户无需了解码值，由模型根据“投资”“任职”或“两者都查”的自然语言选择。
    如果用户没有明确要查询投资、任职还是两者都查，必须先向用户确认，确认后再调用本工具。
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
async def p0020023_query_equity_penetration(
    ent_info: NameOrCreditCodeIdentifier,
    level: EquityPenetrationLevelParameter = "3",
    ratio: EquityRatioThresholdParameter = "5",
    extra_params: AdvancedExtraParams = None,
) -> dict[str, Any]:
    """企业股权穿透信息查询。

    根据企业全称或统一社会信用代码，同时查询向上股东和向下对外投资的递归结构。
    level 为穿透层级，允许 1 至 5，默认 3；ratio 为 0 至 100 的持股比例阈值，
    使用不带百分号的数字字符串，默认 5。按产品文档，底层产品只返回达到阈值的
    企业股东节点。

    data.upList[] 是向上股东树：节点 fundedRatio 表示该节点对其下一级企业的持股；
    data.downList[] 是向下投资树：节点 fundedRatio 表示其上一级企业对该节点的持股。
    两棵树都通过 nodeList[] 递归，grade 从与目标企业直接相邻的第 1 层开始。
    hasNextNode 为 1/0，count 为子节点数量，type 为 0=自然人、1=非自然人。
    文档把部分字段标为 number，但接口样例实际返回字符串；解析时应兼容两种类型。
    目标企业本身不在 upList/downList 中，生成图时需以本次 ent_info 对应的已核验主体
    作为根节点。比例阈值会隐藏低于阈值的节点，不能把未返回节点解释为不存在。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0020023.product_code,
        params=with_guarded_extra_params(
            {
                "entInfo": ent_info,
                "level": level,
                "ratio": ratio,
            },
            extra_params,
            ("entInfo", "level", "ratio"),
        ),
    )


@mcp.tool()
async def p0020024_query_beneficial_shareholders_detailed(
    ent_info: NameOrCreditCodeIdentifier,
    extra_params: AdvancedExtraParams = None,
) -> dict[str, Any]:
    """企业受益股东详细查询。

    根据企业全称或统一社会信用代码查询企业照面、受益股东、最终受益人和实际控制人
    节点。data.basicList[] 是目标企业照面；data.nodeList[] 是穿透节点，其中
    percentTotal 为间接占比，pathLevel 为节点出现的路径层数，pathCount 为路径总数，
    type 为 P=自然人、E=非自然人，benifitTag（底层接口原始拼写）可包含“受益股东”、
    “最终受益人”或“实际控制人”。节点列表是聚合标签结果，不应据此自行重算比例或
    还原产品未返回的完整有向路径。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0020024.product_code,
        params=with_guarded_extra_params(
            {"entInfo": ent_info},
            extra_params,
            ("entInfo",),
        ),
    )


@mcp.tool()
async def p0020031_query_multi_point_relationships(
    ent_info: OptionalCompanyCollection = None,
    person_names: OptionalPersonCollection = None,
    depth: RelationshipDepth = "5",
    relation_type: RelationshipWeightParameter = "0",
    extra_params: AdvancedExtraParams = None,
) -> dict[str, Any]:
    """企业多点关联信息查询。

    查询多个企业或自然人之间的关联网络。ent_info 接受企业名称、统一社会信用代码
    或注册号；person_names 中每个人按“企业名称-姓名”传入。两类输入至少提供一类，
    合计最多 10 个主体，列表或中英文逗号分隔字符串均可。
    depth 默认 5；relation_type：0=投资和任职、1=仅任职、2=仅投资。
    data.nodes[] 是企业/人员节点，data.table[] 按 roadId 组织路径明细，
    data.relation[] 是关系边；同一条边可能因出现在多条路径中而重复，图上可去重，
    但路径分析必须保留 roadId。
    上游 relationType 还可能出现 Gurantee（担保，底层接口原始拼写）、Lawsuit
    和 Client_Supplier。输出是关系网络线索，不等同于关联交易事实。
    """
    params = with_guarded_extra_params(
        {
            "entInfo": normalize_comma_separated(ent_info),
            "persName": normalize_comma_separated(person_names),
            "depth": depth,
            "weight": relation_type,
        },
        extra_params,
        ("entInfo", "persName", "depth", "weight"),
    )
    params["entInfo"] = normalize_comma_separated(params.get("entInfo"))
    params["persName"] = normalize_comma_separated(params.get("persName"))
    require_one_of(params, ("entInfo", "persName"))
    total_items = sum(
        len(params[name].split(",")) if params.get(name) else 0
        for name in ("entInfo", "persName")
    )
    if total_items > 10:
        raise ValueError("entInfo and persName accept at most 10 items in total")

    client = get_client()
    return await client.query_product(
        prod_code=P0020031.product_code,
        params=params,
    )


@mcp.tool()
async def p0020044_query_intercompany_relationship(
    ent_info: CompanyCollection,
    depth: RelationshipDepth = "5",
    relation_type: RelationshipWeightParameter = "0",
    extra_params: AdvancedExtraParams = None,
) -> dict[str, Any]:
    """企业间关联关系查询。

    查询最多 10 家企业之间的关联关系。ent_info 接受企业名称、统一社会信用代码
    或注册号，列表或中英文逗号分隔字符串均可；depth 默认 5；
    relation_type：0=投资和任职、1=仅任职、2=仅投资。
    data.relationship[] 逐主体给出 haveAnyConnection 和 connections[]；
    connections[].relations[] 的关系类型包括“股权投资”和“人员任职”。
    """
    params = with_guarded_extra_params(
        {
            "entInfo": normalize_comma_separated(ent_info),
            "depth": depth,
            "weight": relation_type,
        },
        extra_params,
        ("entInfo", "depth", "weight"),
    )
    params["entInfo"] = normalize_comma_separated(params.get("entInfo"))
    require_one_of(params, ("entInfo",))
    require_at_most_items(params["entInfo"], 10, "entInfo")

    client = get_client()
    return await client.query_product(
        prod_code=P0020044.product_code,
        params=params,
    )


@mcp.tool()
async def p0020129_query_controller_and_ubo(
    ent_info: EnterpriseIdentifier,
    extra_params: AdvancedExtraParams = None,
) -> dict[str, Any]:
    """企业实控人和最终受益人查询。

    根据企业名称、统一社会信用代码或注册号查询实际控制人和最终受益人。
    data.dataList[].controllerList[].controller 是实际控制人直接结论，
    data.dataList[].finalBefList[].beneficiary 是最终受益人直接结论。
    本产品返回名称型结论；控制比例、完整路径和计算口径应使用其他股权穿透产品补证。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0020129.product_code,
        params=with_guarded_extra_params(
            {"entInfo": ent_info},
            extra_params,
            ("entInfo",),
        ),
    )


@mcp.tool()
async def p0090008_query_actual_controller(
    ent_name: UboEnterpriseIdentifier,
    extra_params: AdvancedExtraParams = None,
) -> dict[str, Any]:
    """企业实际控制人信息查询。

    根据企业全称、统一社会信用代码或工商注册号查询实际控制人、股权占比和控制路径；
    注意底层请求字段是 entName。data.actualController[].controllerList[] 给出实际控制人
    controller 及聚合股权占比 percent；controlPathList[] 给出每段股东名称
    stockHolderName、被投资企业名称 investedCompanyName、认缴出资额 shouldCapital 和
    该段股权占比 percent。应逐字保留产品比例，不自行相乘、求和或改写控制口径。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0090008.product_code,
        params=with_guarded_extra_params(
            {"entName": ent_name},
            extra_params,
            ("entName",),
        ),
    )


@mcp.tool()
async def p0090001_p0090012_query_ubo(
    ent_name: UboEnterpriseIdentifier,
    edition: UboQueryEditionParameter,
    include_paths: UboIncludePathsParameter = True,
    extra_params: AdvancedExtraParams = None,
) -> dict[str, Any]:
    """企业最终受益人查询（详版/非详版二选一）。

    这是 P0090001 与 P0090012 的统一入口。完整报告、审计留档、关键管理人员兜底或
    需要完整递归股权树时选 edition="detailed"；快速识别、独立互证或需要受益所有人
    判定依据 bnfCat 时选 edition="standard"。两版均返回 data.finalList[]，其中
    finalBefList[] 是受益所有人，equlityProcessList[] 是股权穿透过程（equlity 为底层
    原始拼写）。standard 可用 include_paths=false 发送 onlyFinalBef=1 省略路径；详版
    固定包含路径。保留原始比例和角色，不自行重算或把关键管理人员改写为持股受益人。
    """
    if edition == "detailed" and not include_paths:
        raise ValueError("detailed edition always includes paths")

    interface = P0090001 if edition == "detailed" else P0090012
    params: dict[str, Any] = {"entName": ent_name}
    if edition == "standard" and not include_paths:
        params["onlyFinalBef"] = "1"

    client = get_client()
    return await client.query_product(
        prod_code=interface.product_code,
        params=with_guarded_extra_params(
            params,
            extra_params,
            ("entName", "onlyFinalBef"),
        ),
    )


@mcp.tool()
async def p0090011_query_ubo_full_paths(
    ent_name: UboEnterpriseIdentifier,
    extra_params: AdvancedExtraParams = None,
) -> dict[str, Any]:
    """企业最终受益人信息查询-全路径版。

    根据企业名称、统一社会信用代码或注册号查询最终受益人及完整路径。
    注意底层请求字段是 entName。结果位于 data.MatchInfoList[]（底层接口原始大小写）：
    lessProcessList[] 是低于 25% 的递归穿透节点；finalList[].equlityProcessList[]
    是受益路径（equlity 为底层接口原始拼写）；finalList[].finalBefList[] 给出
    beneficiary、orgName、type、percent 和 title。应保留原始路径与比例，不自行改写口径。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0090011.product_code,
        params=with_guarded_extra_params(
            {"entName": ent_name},
            extra_params,
            ("entName",),
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
    """企业舆情信息列表查询。

    根据企业名称、三级标签、情感方向等条件查询企业舆情列表信息。
    ent_name 使用企业名称数组，如 ["证通股份有限公司"]，支持多个企业。
    """
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
    """企业舆情信息详情查询。

    根据企业名称或舆情 ID 查询企业舆情详情信息。
    优先使用 entry_id；只传 ent_name 时会先查列表，再取第一条舆情详情。
    """
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
    """企业工商二要素验证。根据企业名称和工商注册号/统一社会信用代码验证信息是否匹配。"""
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
async def p0130025_query_company_key_indicators(
    ent_info: str,
    indicator_type: P0130025IndicatorType = "1",
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业关键指标信息查询。

    ent_info 支持企业名称、工商注册号或统一社会信用代码。
    indicator_type 可选：1=指标等级、2=指标金额，默认 1。
    返回企业年报中的报告年份、资产总额、负债总额、所有者权益、营业收入、
    主营业务收入、利润、纳税、从业人数和社保人数等关键指标。
    响应列表位于 coreLndicatorInfo；该字段名沿用底层接口原始拼写。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0130025.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "type": indicator_type,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0130036_query_land_info(
    ent_info: str,
    land_type: P0130036LandType | None = None,
    page_no: str | None = None,
    page_size: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业土地信息查询。

    ent_info 支持企业名称、统一社会信用代码或企业注册号。
    land_type 可选：tdgy=土地供应、tdcr=土地出让、dkgs=地块公示、tddy=土地抵押；
    不传时由底层产品决定返回范围。page_no 为页码，page_size 为每页条数。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0130036.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "type": land_type,
                "pageNo": page_no,
                "range": page_size,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0130038_query_industry_analysis(
    ent_info: str,
    analysis_type: P0130038AnalysisType,
    nic_lvl: P0130038NicLevel | None = None,
    region_lvl: P0130038RegionLevel | None = None,
    region_id: str | None = None,
    nic_id: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业画像行业分析查询。

    根据企业、行业和地区条件查询企业排名、行业财务指标、综合经营指标和知识产权排名等
    行业分析信息。ent_info 支持企业名称、统一社会信用代码或企业注册号。
    analysis_type 可选：finRank=企业财务指标最新排序；
    finRankStock=上市公司财务指标最新排序；entRegionRank=企业区域行业排名；
    locfin=行业地区财务指标；indLocOpr=年度行业地区指标；
    indLocOprFin=行业地区综合指标；property=企业知识产权区域行业排名；
    financialRegionRank=财务指标区域行业排名。
    nic_lvl 可选 n1 至 n4，region_lvl 可选 r0 至 r3；region_id 和 nic_id
    分别为行政区划代码和国标行业代码。不同分析类型返回的数据字段不同，请从 data 中读取。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0130038.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "type": analysis_type,
                "nicLvl": nic_lvl,
                "regionLvl": region_lvl,
                "regionId": region_id,
                "nicId": nic_id,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0210004_query_listed_company_financial_data(
    ent_info: str,
    financial_type: P0210004FinancialType,
    start_date: str | None = None,
    end_date: str | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """上市公司财务数据查询。

    根据企业名称、统一社会信用代码或注册号查询上市企业的利润、现金流量、资产负债和
    主要财务指标。ent_info 支持企业名称、统一社会信用代码或企业注册号。
    financial_type 可选：rgincome=通用类利润、rgcashflow=通用类现金流量、
    fncmfnin=金融公司主要财务指标、rgbalance=通用类资产负债、
    mainfinadata=主要会计数据和财务指标、balance=一般企业资产负债、
    income=一般企业利润、cashflow=一般企业现金流量。
    start_date 和 end_date 为可选报表起止日期，格式均为 YYYY-MM-DD。
    不同类型分别返回 data.rgincomeInfo、rgcashflowInfo、fncmfninInfo、
    rgbalanceInfo、mainfinadataInfo、balanceInfo、incomeInfo 或 cashflowInfo。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0210004.product_code,
        params=with_extra_params(
            {
                "entInfo": ent_info,
                "type": financial_type,
                "startDate": start_date,
                "endDate": end_date,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0980006_query_advanced_company_filter(
    eid: str | None = None,
    reg_cap_bak: str | None = None,
    tm_type_all: str | None = None,
    bond_date_scope: str | None = None,
    bond_trademarket: str | None = None,
    bond_eid_rating: str | None = None,
    tax_stype: str | None = None,
    crr_score_adj: str | None = None,
    cnt_ibid_list: str | None = None,
    cnt_wbid_list: str | None = None,
    office_park_id: str | None = None,
    reg_cap_cur_bak: str | None = None,
    copy_right_bak: str | None = None,
    listed_bak: str | None = None,
    employees_num_bak: str | None = None,
    so_num: str | None = None,
    feature_label: str | None = None,
    tax_rating: str | None = None,
    shld_bg: str | None = None,
    uco_bg: str | None = None,
    bnf_bg: str | None = None,
    team_member: str | None = None,
    science_technology: str | None = None,
    advanced_label: str | None = None,
    monthly_focus_label: str | None = None,
    patent_size: str | None = None,
    copy_right_size: str | None = None,
    industry_ranking: str | None = None,
    financial_target: str | None = None,
    contact_cnt: str | None = None,
    vci_org: str | None = None,
    listed_sub: str | None = None,
    green_ctf_type: str | None = None,
    area_prefix: str | None = None,
    industy_prefix: str | None = None,
    org_status: str | None = None,
    org_scale: str | None = None,
    new_industry: str | None = None,
    est_date_start: str | None = None,
    est_date_end: str | None = None,
    page_no: str | None = "1",
    page_size: str | None = "10",
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """企业高级筛选。

    通过地区、行业、规模、资本、上市、融资、招投标、知识产权等多维度条件筛选
    符合条件的企业列表。
    eid 为可选的 CISP 企业内部标识，传入后原样映射到底层 eid 字段。
    筛选码值按产品约定原样传递；成立日期格式为 yyyy-MM-dd。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0980006.product_code,
        params=with_extra_params(
            {
                "eid": eid,
                "regCapBak": reg_cap_bak,
                "tmTypeAll": tm_type_all,
                "bondDateScope": bond_date_scope,
                "bondTrademarket": bond_trademarket,
                "bondEidRating": bond_eid_rating,
                "taxStype": tax_stype,
                "crrScoreAdj": crr_score_adj,
                "cntIbidList": cnt_ibid_list,
                "cntWbidList": cnt_wbid_list,
                "officeParkId": office_park_id,
                "regCapCurBak": reg_cap_cur_bak,
                "copyRightBak": copy_right_bak,
                "listedBak": listed_bak,
                "employeesNumBak": employees_num_bak,
                "soNum": so_num,
                "featureLabel": feature_label,
                "taxRating": tax_rating,
                "shldBg": shld_bg,
                "ucoBg": uco_bg,
                "bnfBg": bnf_bg,
                "teamMember": team_member,
                "scienceTechnology": science_technology,
                "advancedLabel": advanced_label,
                "monthlyFocusLabel": monthly_focus_label,
                "patentSize": patent_size,
                "copyRightSize": copy_right_size,
                "industryRanking": industry_ranking,
                "financialTarget": financial_target,
                "contactCnt": contact_cnt,
                "vciOrg": vci_org,
                "listedSub": listed_sub,
                "greenCtfType": green_ctf_type,
                "areaPrefix": area_prefix,
                "industyPrefix": industy_prefix,
                "orgStatus": org_status,
                "orgScale": org_scale,
                "newIndustry": new_industry,
                "estDateStart": est_date_start,
                "estDateEnd": est_date_end,
                "pageNo": page_no,
                "range": page_size,
            },
            extra_params,
        ),
    )


@mcp.tool()
async def p0980008_query_tax_rating(
    eid: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """纳税评级查询。

    根据企业内部 eid 查询企业纳税评级。eid 为 CISP 企业内部标识。
    若用户只提供企业名称，应先调用 p0010010_query_business_profile，将企业名称传入
    ent_info，再从 orgName 准确匹配的 basicList[].entId 获取值并作为本工具的 eid。
    不得自行推算 eid。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0980008.product_code,
        params=with_extra_params({"eid": eid}, extra_params),
    )


@mcp.tool()
async def p0980023_query_two_year_risk_summary(
    eid: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """近2年风险分析统计。

    根据企业内部 eid 查询企业近两年风险分析统计，返回 collect1 至 collect15 风险统计。
    eid 为 CISP 企业内部标识。若用户只提供企业名称，应先调用
    p0010010_query_business_profile，将企业名称传入 ent_info，再从 orgName
    准确匹配的 basicList[].entId 获取值并作为本工具的 eid。不得自行推算 eid。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0980023.product_code,
        params=with_extra_params({"eid": eid}, extra_params),
    )


@mcp.tool()
async def p0980033_query_listing_financing_bidding_ipr(
    ent_info: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """上市投融资招投标知识产权情况查询。

    根据企业名称、工商注册号或统一社会信用代码查询上市、投融资、招投标和知识产权情况。
    ent_info 支持企业名称、统一社会信用代码或工商注册号。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0980033.product_code,
        params=with_extra_params({"entInfo": ent_info}, extra_params),
    )


@mcp.tool()
async def p0990022_query_supplier_relationships(
    ent_info: str,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """供应商关联关系查询。

    ent_info 支持企业名称、工商注册号、组织机构代码或统一社会信用代码。
    返回供应商关联主体、法定代表人、董监高和控股企业等公开关联信息。
    """
    client = get_client()
    return await client.query_product(
        prod_code=P0990022.product_code,
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
