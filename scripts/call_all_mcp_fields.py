from __future__ import annotations

import argparse
import asyncio
import json
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


CALL_SPECS: list[tuple[str, dict[str, Any]]] = [
    (
        "p0010010_query_business_profile",
        {"ent_info": "中国银行股份有限公司"},
    ),
    (
        "p0010058_query_business_basic_deep",
        {"ent_name": "河南省宋河酒业股份有限公司"},
    ),
    (
        "p0010059_query_business_basic_brief",
        {
            "ent_name": "中国银行股份有限公司",
            "types": ["basic"],
        },
    ),
    (
        "p0010068_fuzzy_search_company_name",
        {"ent_name": "宋河酒业"},
    ),
    (
        "p0010073_query_trademark_info",
        {
            "ent_info": "河南省宋河酒业股份有限公司",
            "page_no": "1",
            "page_size": "5",
        },
    ),
    (
        "p0010074_query_software_copyright_info",
        {
            "ent_info": "中国银行股份有限公司",
            "page_no": "1",
            "page_size": "5",
        },
    ),
    (
        "p0010075_query_work_copyright_info",
        {
            "ent_info": "河南省宋河酒业股份有限公司",
            "page_no": "1",
            "page_size": "5",
        },
    ),
    (
        "p0010076_query_icp_filing_info",
        {
            "ent_info": "中国银行股份有限公司",
            "page_no": "1",
            "page_size": "5",
        },
    ),
    (
        "p0010078_query_patent_info",
        {
            "ent_info": "中国银行股份有限公司",
            "page_no": "1",
            "page_size": "5",
        },
    ),
    (
        "p0010084_query_license_info",
        {
            "ent_info": "河南省宋河酒业股份有限公司",
            "license_type": "gs",
            "page_no": "1",
            "page_size": "5",
        },
    ),
    (
        "p0020021_query_single_point_related_info",
        {
            "ent_info": "河南省宋河酒业股份有限公司",
            "relation_direction": "1",
        },
    ),
    (
        "p0050007_query_public_opinion_list",
        {
            "ent_name": ["中国银行股份有限公司"],
            "page_no": "1",
            "page_size": "2",
        },
    ),
    (
        "p0050008_query_public_opinion_detail",
        {"ent_name": ["中国银行股份有限公司"]},
    ),
    (
        "p0050007_p0050008_query_public_opinion_info",
        {
            "ent_name": ["中国银行股份有限公司"],
            "page_no": "1",
            "page_size": "2",
            "max_details": 2,
        },
    ),
    (
        "p0060007_verify_business_two_elements",
        {
            "ent_name": "中国银行股份有限公司",
            "reg_no": "911000001000013428",
        },
    ),
    (
        "p0060008_verify_business_three_elements",
        {
            "ent_name": "中国银行股份有限公司",
            "reg_no": "911000001000013428",
            "fr_name": "葛海蛟",
        },
    ),
    (
        "p0110003_query_honor_qualification_info",
        {"ent_info": "中国银行股份有限公司"},
    ),
    (
        "p0130025_query_company_key_indicators",
        {
            "ent_info": "中国银行股份有限公司",
            "indicator_type": "2",
        },
    ),
    (
        "p0130036_query_land_info",
        {
            "ent_info": "中国银行股份有限公司",
            "page_no": "1",
            "page_size": "5",
        },
    ),
    (
        "p0130038_query_industry_analysis",
        {
            "ent_info": "中国银行股份有限公司",
            "analysis_type": "property",
            "nic_lvl": "n3",
            "region_lvl": "r2",
        },
    ),
    (
        "p0210004_query_listed_company_financial_data",
        {
            "ent_info": "中国银行股份有限公司",
            "financial_type": "fncmfnin",
            "start_date": "2024-01-01",
            "end_date": "2025-12-31",
        },
    ),
    (
        "p0980006_query_advanced_company_filter",
        {
            "eid": "1911000001000013428",
            "page_no": "1",
            "page_size": "2",
        },
    ),
    (
        "p0980008_query_tax_rating",
        {"eid": "1911000001000013428"},
    ),
    (
        "p0980023_query_two_year_risk_summary",
        {"eid": "1911000001000013428"},
    ),
    (
        "p0980033_query_listing_financing_bidding_ipr",
        {"ent_info": "中国银行股份有限公司"},
    ),
    (
        "p0990022_query_supplier_relationships",
        {"ent_info": "中国银行股份有限公司"},
    ),
    (
        "query_cisp_product",
        {
            "prod_code": "P0010010",
            "ent_info": "河南省宋河酒业股份有限公司",
        },
    ),
]


def jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def extract_result(call_result: Any) -> Any:
    structured = jsonable(call_result.structuredContent)
    if structured is not None:
        return structured

    content = jsonable(call_result.content)
    if isinstance(content, list) and len(content) == 1:
        text = content[0].get("text") if isinstance(content[0], dict) else None
        if isinstance(text, str):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {"text": text}
    return {"content": content}


def sample_value(value: Any) -> Any:
    if isinstance(value, str) and len(value) > 160:
        return value[:157] + "..."
    return value


def value_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def collect_fields(
    value: Any,
    path: str,
    fields: dict[str, dict[str, Any]],
) -> None:
    field = fields.setdefault(
        path or "$",
        {"types": set(), "samples": [], "observations": 0},
    )
    field["types"].add(value_type(value))
    field["observations"] += 1
    if len(field["samples"]) < 3:
        candidate = sample_value(value)
        if not isinstance(candidate, (dict, list)) and candidate not in field["samples"]:
            field["samples"].append(candidate)

    if isinstance(value, dict):
        for key, item in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            collect_fields(item, child_path, fields)
    elif isinstance(value, list):
        child_path = f"{path}[]"
        for item in value:
            collect_fields(item, child_path, fields)


async def run(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    server = StdioServerParameters(
        command="uv",
        args=["run", "cisp-mcp"],
        cwd=Path.cwd(),
    )
    started_at = datetime.now(UTC)
    manifest_calls: list[dict[str, Any]] = []
    observed_by_tool: dict[str, list[dict[str, Any]]] = {}

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(
            read_stream,
            write_stream,
            read_timeout_seconds=timedelta(seconds=120),
        ) as session:
            await session.initialize()
            tool_list = await session.list_tools()
            tools = [jsonable(tool) for tool in tool_list.tools]
            registered_names = {tool["name"] for tool in tools}
            expected_names = {name for name, _ in CALL_SPECS}
            if registered_names != expected_names:
                raise RuntimeError(
                    "Tool inventory mismatch: "
                    f"missing={sorted(expected_names - registered_names)}, "
                    f"unexpected={sorted(registered_names - expected_names)}"
                )

            (output_dir / "tool_schemas.json").write_text(
                json.dumps(tools, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            for index, (tool_name, arguments) in enumerate(CALL_SPECS, 1):
                called_at = datetime.now(UTC)
                call_result = await session.call_tool(tool_name, arguments)
                result = extract_result(call_result)
                is_error = bool(call_result.isError)

                record = {
                    "sequence": index,
                    "tool_name": tool_name,
                    "called_at": called_at.isoformat(),
                    "arguments": arguments,
                    "is_error": is_error,
                    "result": result,
                }
                raw_name = f"{index:02d}_{tool_name}.json"
                (raw_dir / raw_name).write_text(
                    json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )

                fields: dict[str, dict[str, Any]] = {}
                collect_fields(result, "", fields)
                observed_by_tool[tool_name] = [
                    {
                        "path": path,
                        "types": sorted(details["types"]),
                        "samples": details["samples"],
                        "observations": details["observations"],
                    }
                    for path, details in sorted(fields.items())
                ]

                summary = result if isinstance(result, dict) else {}
                manifest_calls.append(
                    {
                        "sequence": index,
                        "tool_name": tool_name,
                        "arguments": arguments,
                        "raw_file": f"raw/{raw_name}",
                        "is_error": is_error,
                        "success": summary.get("success"),
                        "has_result": summary.get("has_result"),
                        "result_code": summary.get("result_code"),
                        "product_status": summary.get("product_status"),
                        "field_path_count": len(fields),
                    }
                )
                print(
                    f"[{index:02d}/{len(CALL_SPECS)}] {tool_name}: "
                    f"is_error={is_error}, success={summary.get('success')}, "
                    f"has_result={summary.get('has_result')}, fields={len(fields)}"
                )

    finished_at = datetime.now(UTC)
    manifest = {
        "mcp_server_name": "apimcp",
        "mcp_command": ["uv", "run", "cisp-mcp"],
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "registered_tool_count": len(CALL_SPECS),
        "called_tool_count": len(manifest_calls),
        "all_registered_tools_called": len(manifest_calls) == len(CALL_SPECS),
        "calls": manifest_calls,
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "observed_fields.json").write_text(
        json.dumps(observed_by_tool, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Call every registered cisp-mcp tool and capture returned fields."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("fields_test"),
        help="Output directory (default: fields_test)",
    )
    args = parser.parse_args()
    asyncio.run(run(args.output.resolve()))


if __name__ == "__main__":
    main()
