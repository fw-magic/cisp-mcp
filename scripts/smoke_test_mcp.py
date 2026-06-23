from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request


MCP_URL = "http://127.0.0.1:8000/mcp"

EXPECTED_TOOLS = {
    "p0010010_query_business_profile",
    "p0010058_query_business_basic_deep",
    "p0010068_fuzzy_search_company_name",
    "p0010073_query_trademark_info",
    "p0010074_query_software_copyright_info",
    "p0010075_query_work_copyright_info",
    "p0010076_query_icp_filing_info",
    "p0010078_query_patent_info",
    "p0050007_query_public_opinion_list",
    "p0050008_query_public_opinion_detail",
    "p0050007_p0050008_query_public_opinion_info",
    "p0060007_verify_business_two_elements",
    "p0060008_verify_business_three_elements",
    "query_cisp_product",
}


def post_mcp(payload: dict, session_id: str | None = None) -> tuple[object, dict | None]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id

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
        post_mcp(
            {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "cisp-mcp-port-check", "version": "0.1.0"},
                },
            }
        )
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        return

    raise RuntimeError(
        f"{MCP_URL} is already serving an MCP server. Stop the existing server before running this smoke test."
    )


def main() -> int:
    assert_port_is_free()

    env = os.environ.copy()
    env.setdefault("CISP_API_KEY", "smoke-test-key")

    process = subprocess.Popen(
        [sys.executable, "-m", "cisp_mcp.server", "--transport", "streamable-http"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )

    try:
        wait_until_ready(process)
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
