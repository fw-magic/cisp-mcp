from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request


MCP_URL = "http://127.0.0.1:8000/mcp"
SMOKE_TEST_API_KEY = "smoke-test-cisp-api-key"

EXPECTED_TOOLS = {
    "p0010010_query_business_profile",
    "p0010058_query_business_basic_deep",
    "p0010059_query_business_basic_brief",
    "p0010068_fuzzy_search_company_name",
    "p0010073_query_trademark_info",
    "p0010074_query_software_copyright_info",
    "p0010075_query_work_copyright_info",
    "p0010076_query_icp_filing_info",
    "p0010078_query_patent_info",
    "p0010084_query_license_info",
    "p0020014_query_suspected_relationships",
    "p0020019_query_suspected_controller",
    "p0020021_query_single_point_related_info",
    "p0020031_query_multi_point_relationships",
    "p0020044_query_intercompany_relationship",
    "p0020129_query_controller_and_ubo",
    "p0050007_query_public_opinion_list",
    "p0050008_query_public_opinion_detail",
    "p0050007_p0050008_query_public_opinion_info",
    "p0060007_verify_business_two_elements",
    "p0060008_verify_business_three_elements",
    "p0090011_query_ubo_full_paths",
    "p0110003_query_honor_qualification_info",
    "p0130025_query_company_key_indicators",
    "p0130036_query_land_info",
    "p0130038_query_industry_analysis",
    "p0210004_query_listed_company_financial_data",
    "p0980006_query_advanced_company_filter",
    "p0980008_query_tax_rating",
    "p0980023_query_two_year_risk_summary",
    "p0980033_query_listing_financing_bidding_ipr",
    "p0990022_query_supplier_relationships",
    "query_cisp_product",
}


def post_mcp(
    payload: dict,
    session_id: str | None = None,
    api_key: str | None = SMOKE_TEST_API_KEY,
) -> tuple[object, dict | None]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    request = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        body = response.read().decode("utf-8")
        return response.headers, json.loads(body) if body else None


def wait_until_ready(process: subprocess.Popen[str]) -> None:
    deadline = time.time() + 15
    last_error: Exception | None = None

    while time.time() < deadline:
        if process.poll() is not None:
            output = process.stdout.read() if process.stdout else ""
            raise RuntimeError(f"MCP server exited early with code {process.returncode}\n{output}")

        try:
            headers, _ = post_mcp(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-06-18",
                        "capabilities": {},
                        "clientInfo": {"name": "cisp-mcp-smoke-test", "version": "0.1.0"},
                    },
                }
            )
            if headers.get("Mcp-Session-Id"):
                return
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = exc
            time.sleep(0.5)

    raise RuntimeError(f"MCP server did not become ready: {last_error}")


def list_tools() -> list[str]:
    headers, _ = post_mcp(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "cisp-mcp-smoke-test", "version": "0.1.0"},
            },
        }
    )
    session_id = headers["Mcp-Session-Id"]
    post_mcp({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}, session_id)
    _, body = post_mcp({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, session_id)
    assert body is not None
    return [tool["name"] for tool in body["result"]["tools"]]


def assert_port_is_free() -> None:
    try:
        with socket.create_connection(("127.0.0.1", 8000), timeout=1):
            pass
    except OSError:
        return

    raise RuntimeError(
        f"{MCP_URL} is already serving an MCP server. Stop the existing server before running this smoke test."
    )


def assert_auth_is_required() -> None:
    try:
        post_mcp(
            {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "cisp-mcp-auth-check", "version": "0.1.0"},
                },
            },
            api_key=None,
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            return
        raise RuntimeError(f"Expected HTTP 401 without a CISP API key, got {exc.code}") from exc

    raise RuntimeError("MCP server accepted a request without a CISP API key")


def assert_session_is_bound_to_api_key() -> None:
    headers, _ = post_mcp(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "cisp-mcp-session-check", "version": "0.1.0"},
            },
        },
        api_key="smoke-test-customer-a-key",
    )
    session_id = headers["Mcp-Session-Id"]

    try:
        post_mcp(
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
            session_id,
            api_key="smoke-test-customer-b-key",
        )
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403, 404):
            return
        raise RuntimeError(f"Expected cross-customer session rejection, got HTTP {exc.code}") from exc

    raise RuntimeError("A second CISP API key reused the first customer's MCP session")


def main() -> int:
    assert_port_is_free()

    env = os.environ.copy()
    env.pop("CISP_API_KEY", None)

    process = subprocess.Popen(
        [sys.executable, "-m", "cisp_mcp.server", "--transport", "streamable-http"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )

    try:
        wait_until_ready(process)
        assert_auth_is_required()
        assert_session_is_bound_to_api_key()
        tools = list_tools()
        tool_set = set(tools)

        missing = EXPECTED_TOOLS - tool_set
        unexpected = tool_set - EXPECTED_TOOLS

        print("Discovered MCP tools:")
        for tool in tools:
            print(f"- {tool}")
        print(f"Total: {len(tools)}")

        if missing or unexpected:
            if missing:
                print(f"Missing tools: {sorted(missing)}")
            if unexpected:
                print(f"Unexpected tools: {sorted(unexpected)}")
            return 1

        print("Smoke test passed.")
        return 0
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


if __name__ == "__main__":
    raise SystemExit(main())
