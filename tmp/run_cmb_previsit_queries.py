from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


COMPANY = "招商银行股份有限公司"
OUTPUT = Path("tmp/cmb_previsit_raw.json")


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
            return json.loads(text)
    return {"content": content}


async def main() -> None:
    server = StdioServerParameters(command="uv", args=["run", "cisp-mcp"])
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            basic_call = await session.call_tool(
                "p0010058_query_business_basic_deep",
                {"ent_name": COMPANY},
            )
            basic = extract_result(basic_call)
            basic_data = basic.get("data") if isinstance(basic, dict) else None
            basic_list = basic_data.get("basicList") if isinstance(basic_data, dict) else None
            if not isinstance(basic_list, list) or not basic_list:
                raise RuntimeError("工商深度查询未返回可锚定主体")
            canonical = basic_list[0].get("orgName")
            if canonical != COMPANY:
                raise RuntimeError(f"工商主体不一致：{canonical!r}")

            specs = {
                "TM": (
                    "p0010073_query_trademark_info",
                    {"ent_info": canonical, "page_no": "1", "page_size": "5"},
                ),
                "IP": (
                    "p0010078_query_patent_info",
                    {"ent_info": canonical, "page_no": "1", "page_size": "5"},
                ),
                "SW": (
                    "p0010074_query_software_copyright_info",
                    {"ent_info": canonical, "page_no": "1", "page_size": "5"},
                ),
                "WC": (
                    "p0010075_query_work_copyright_info",
                    {"ent_info": canonical, "page_no": "1", "page_size": "5"},
                ),
                "ICP": (
                    "p0010076_query_icp_filing_info",
                    {"ent_info": canonical, "page_no": "1", "page_size": "5"},
                ),
                "LIC": (
                    "p0010084_query_license_info",
                    {
                        "ent_info": canonical,
                        "license_type": "gs",
                        "page_no": "1",
                        "page_size": "5",
                    },
                ),
                "HON": (
                    "p0110003_query_honor_qualification_info",
                    {"ent_info": canonical},
                ),
                "OP": (
                    "p0050007_p0050008_query_public_opinion_info",
                    {
                        "ent_name": canonical,
                        "start_date": "2026-04-28",
                        "end_date": "2026-07-27",
                        "page_no": "1",
                        "page_size": "10",
                        "max_details": 5,
                    },
                ),
            }

            async def call(name: str, args: dict[str, Any]) -> Any:
                try:
                    return extract_result(await session.call_tool(name, args))
                except Exception as exc:
                    return {"_query_failed": True, "_error_type": type(exc).__name__}

            values = await asyncio.gather(
                *(call(tool_name, args) for tool_name, args in specs.values())
            )
            result = {"B": basic}
            result.update({key: value for key, value in zip(specs, values, strict=True)})
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")

            status = {
                key: {
                    "success": value.get("success") if isinstance(value, dict) else None,
                    "has_result": value.get("has_result") if isinstance(value, dict) else None,
                    "failed": value.get("_query_failed", False) if isinstance(value, dict) else True,
                }
                for key, value in result.items()
            }
            print(json.dumps({"canonical": canonical, "status": status}, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
