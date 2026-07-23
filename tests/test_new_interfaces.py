from __future__ import annotations

import unittest
from typing import Any, get_args, get_type_hints
from unittest.mock import patch

from cisp_mcp import interfaces, server


class RecordingClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def query_product(
        self,
        prod_code: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        self.calls.append((prod_code, params))
        return {"prod_code": prod_code, "params": params}


class NewInterfaceMetadataTests(unittest.TestCase):
    def test_p0020021_metadata(self) -> None:
        self.assertIn("P0020021", interfaces.INTERFACES)
        interface = interfaces.INTERFACES["P0020021"]
        self.assertEqual(interface.status_field, "P0020021Status")
        self.assertEqual(interface.data_field, "P0020021Data")
        self.assertEqual(interface.shortcut_field, "entInvList")

    def test_p0110003_metadata(self) -> None:
        self.assertIn("P0110003", interfaces.INTERFACES)
        interface = interfaces.INTERFACES["P0110003"]
        self.assertEqual(interface.status_field, "P0110003Status")
        self.assertEqual(interface.data_field, "P0110003Data")
        self.assertEqual(interface.shortcut_field, "itemNameList")

    def test_p0010084_metadata(self) -> None:
        self.assertIn("P0010084", interfaces.INTERFACES)
        interface = interfaces.INTERFACES["P0010084"]
        self.assertEqual(interface.status_field, "P0010084Status")
        self.assertEqual(interface.data_field, "P0010084Data")
        self.assertEqual(interface.shortcut_field, "detailList")


class NewInterfaceToolTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = RecordingClient()
        self.client_patch = patch(
            "cisp_mcp.server.get_client",
            return_value=self.client,
        )
        self.client_patch.start()

    def tearDown(self) -> None:
        self.client_patch.stop()

    async def test_p0020021_maps_relation_direction(self) -> None:
        self.assertTrue(
            hasattr(server, "p0020021_query_single_point_related_info")
        )
        tool = server.p0020021_query_single_point_related_info
        annotation = get_type_hints(tool)["relation_direction"]
        self.assertEqual(get_args(annotation), ("1", "2", "3"))

        result = await tool(
            ent_info="证通股份有限公司",
            relation_direction="2",
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0020021",
                    {
                        "entInfo": "证通股份有限公司",
                        "relationDirection": "2",
                    },
                )
            ],
        )
        self.assertEqual(result["prod_code"], "P0020021")

    async def test_p0020021_schema_requires_clarifying_ambiguous_intent(self) -> None:
        tools = await server.mcp.list_tools()
        tool = next(
            item
            for item in tools
            if item.name == "p0020021_query_single_point_related_info"
        )

        self.assertEqual(
            tool.inputSchema["properties"]["relation_direction"]["enum"],
            ["1", "2", "3"],
        )
        self.assertIn("必须先向用户确认", tool.description or "")

    async def test_p0110003_maps_enterprise_identifier(self) -> None:
        self.assertTrue(
            hasattr(server, "p0110003_query_honor_qualification_info")
        )

        result = await server.p0110003_query_honor_qualification_info(
            ent_info="证通股份有限公司",
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0110003",
                    {"entInfo": "证通股份有限公司"},
                )
            ],
        )
        self.assertEqual(result["prod_code"], "P0110003")

    async def test_p0010084_maps_filters_and_pagination(self) -> None:
        self.assertTrue(hasattr(server, "p0010084_query_license_info"))

        result = await server.p0010084_query_license_info(
            ent_info="证通股份有限公司",
            license_type="ylxk",
            province="广东省",
            page_no="2",
            page_size="20",
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0010084",
                    {
                        "entInfo": "证通股份有限公司",
                        "type": "ylxk",
                        "province": "广东省",
                        "pageNo": "2",
                        "range": "20",
                    },
                )
            ],
        )
        self.assertEqual(result["prod_code"], "P0010084")

    async def test_p0010084_accepts_omitted_optional_filters(self) -> None:
        self.assertTrue(hasattr(server, "p0010084_query_license_info"))

        await server.p0010084_query_license_info(
            ent_info="证通股份有限公司",
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0010084",
                    {
                        "entInfo": "证通股份有限公司",
                        "type": None,
                        "province": None,
                        "pageNo": None,
                        "range": None,
                    },
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
