from __future__ import annotations

import inspect
import json
import unittest
from typing import Any, get_args, get_type_hints
from unittest.mock import patch

from mcp.server.fastmcp.exceptions import ToolError

from cisp_mcp import client as client_module
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
    def test_portrait_product_metadata(self) -> None:
        expected = {
            "P0010059": ("P0010059Status", "P0010059Data", "basicList"),
            "P0980006": ("P0980006Status", "P0980006Data", "entList"),
            "P0980008": ("P0980008Status", "P0980008Data", "list"),
            "P0980023": ("P0980023Status", "P0980023Data", "list"),
            "P0980033": ("P0980033Status", "P0980033Data", "data"),
        }

        for product_code, fields in expected.items():
            with self.subTest(product_code=product_code):
                interface = interfaces.INTERFACES[product_code]
                self.assertEqual(
                    (interface.status_field, interface.data_field, interface.shortcut_field),
                    fields,
                )

    def test_portrait_product_responses_are_normalized(self) -> None:
        shortcut_values = {
            "P0010059": ("basicList", [{"orgName": "测试企业"}]),
            "P0980006": ("entList", [{"eid": "1910000000000000000"}]),
            "P0980008": ("list", [{"year": "2025", "rating": "A"}]),
            "P0980023": ("list", [{"collect1": "1", "collect15": "0"}]),
            "P0980033": ("data", [{"listed": [], "investmentFin": []}]),
        }

        for product_code, (shortcut_field, shortcut_value) in shortcut_values.items():
            with self.subTest(product_code=product_code):
                interface = interfaces.INTERFACES[product_code]
                raw_response = {
                    "orderNo": f"order-{product_code}",
                    "resultData": {
                        interface.data_field: {
                            shortcut_field: shortcut_value,
                        },
                        interface.status_field: "4",
                    },
                    "packetCnt": 1,
                    "resultCode": "00000",
                    "resultDesc": "成功",
                    "isCompressed": 0,
                }

                normalized = client_module.normalize_interface_response(
                    raw_response,
                    interface,
                )

                self.assertEqual(normalized["product_code"], product_code)
                self.assertTrue(normalized["success"])
                self.assertTrue(normalized["has_result"])
                self.assertEqual(normalized[shortcut_field], shortcut_value)
                self.assertIs(normalized["raw_response"], raw_response)

    def test_p0020021_metadata(self) -> None:
        self.assertIn("P0020021", interfaces.INTERFACES)
        interface = interfaces.INTERFACES["P0020021"]
        self.assertEqual(interface.status_field, "P0020021Status")
        self.assertEqual(interface.data_field, "P0020021Data")
        self.assertEqual(interface.shortcut_field, "entInvList")

    def test_equity_analysis_product_metadata(self) -> None:
        expected = {
            "P0020014": ("P0020014Status", "P0020014Data", "suspectList"),
            "P0020019": ("P0020019Status", "P0020019Data", "controlNodeList"),
            "P0020023": ("P0020023Status", "P0020023Data", "upList"),
            "P0020031": ("P0020031Status", "P0020031Data", "nodes"),
            "P0020044": ("P0020044Status", "P0020044Data", "relationship"),
            "P0020129": ("P0020129Status", "P0020129Data", "dataList"),
            "P0090011": ("P0090011Status", "P0090011Data", "MatchInfoList"),
        }

        for product_code, fields in expected.items():
            with self.subTest(product_code=product_code):
                interface = interfaces.INTERFACES[product_code]
                self.assertEqual(
                    (interface.status_field, interface.data_field, interface.shortcut_field),
                    fields,
                )

    def test_equity_analysis_product_responses_are_normalized(self) -> None:
        for product_code in (
            "P0020014",
            "P0020019",
            "P0020023",
            "P0020031",
            "P0020044",
            "P0020129",
            "P0090011",
        ):
            with self.subTest(product_code=product_code):
                interface = interfaces.INTERFACES[product_code]
                shortcut_value = [{"source": product_code}]
                raw_response = {
                    "resultCode": "00000",
                    "resultData": {
                        interface.status_field: "4",
                        interface.data_field: {
                            interface.shortcut_field: shortcut_value,
                        },
                    },
                }

                normalized = client_module.normalize_interface_response(
                    raw_response,
                    interface,
                )

                self.assertTrue(normalized["success"])
                self.assertTrue(normalized["has_result"])
                self.assertEqual(
                    normalized[interface.shortcut_field],
                    shortcut_value,
                )

    def test_p0020023_preserves_both_recursive_trees(self) -> None:
        interface = interfaces.INTERFACES["P0020023"]
        up_list = [
            {
                "grade": "1",
                "name": "自然人股东",
                "type": "0",
                "fundedRatio": "60.00",
                "hasNextNode": "0",
                "count": "0",
                "nodeList": [],
            }
        ]
        down_list = [
            {
                "grade": "1",
                "name": "一级子公司",
                "type": "1",
                "fundedRatio": "100.00",
                "hasNextNode": "1",
                "count": "1",
                "nodeList": [
                    {
                        "grade": "2",
                        "name": "二级子公司",
                        "type": "1",
                        "fundedRatio": "80.00",
                        "hasNextNode": "0",
                        "count": "0",
                        "nodeList": [],
                    }
                ],
            }
        ]
        raw_response = {
            "resultCode": "00000",
            "resultData": {
                "P0020023Status": "4",
                "P0020023Data": {
                    "upList": up_list,
                    "downList": down_list,
                },
            },
        }

        normalized = client_module.normalize_interface_response(
            raw_response,
            interface,
        )

        self.assertEqual(normalized["upList"], up_list)
        self.assertEqual(normalized["data"]["downList"], down_list)
        self.assertEqual(
            normalized["data"]["downList"][0]["nodeList"][0]["grade"],
            "2",
        )

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

    def test_p0130025_metadata_and_normalized_response(self) -> None:
        self.assertIn("P0130025", interfaces.INTERFACES)
        interface = interfaces.INTERFACES["P0130025"]
        self.assertEqual(interface.status_field, "P0130025Status")
        self.assertEqual(interface.data_field, "P0130025Data")
        self.assertEqual(interface.shortcut_field, "coreLndicatorInfo")

        indicator_list = [
            {
                "reportYear": "2025",
                "totalAss": "二十四档",
                "totalLia": "二十三档",
                "busIncome": "二十三档",
                "empNum": "213",
                "socialSecurityNum": "213",
            }
        ]
        raw_response = {
            "orderNo": "order-P0130025",
            "resultData": {
                "P0130025Data": {
                    "coreLndicatorInfo": indicator_list,
                },
                "P0130025Status": "4",
            },
            "packetCnt": 1,
            "resultCode": "00000",
            "resultDesc": "成功",
            "isCompressed": 0,
        }

        normalized = client_module.normalize_interface_response(
            raw_response,
            interface,
        )

        self.assertEqual(normalized["product_code"], "P0130025")
        self.assertTrue(normalized["success"])
        self.assertTrue(normalized["has_result"])
        self.assertEqual(normalized["coreLndicatorInfo"], indicator_list)
        self.assertIs(normalized["raw_response"], raw_response)

    def test_p0130036_metadata_and_normalized_response(self) -> None:
        self.assertIn("P0130036", interfaces.INTERFACES)
        interface = interfaces.INTERFACES["P0130036"]
        self.assertEqual(interface.status_field, "P0130036Status")
        self.assertEqual(interface.data_field, "P0130036Data")
        self.assertEqual(interface.shortcut_field, "detailList")

        detail_list = [
            {
                "tdgyResults": [{"projectName": "测试土地供应项目"}],
                "tdcrResults": [],
                "dkgsResults": [],
                "tddyResults": [],
            }
        ]
        raw_response = {
            "orderNo": "order-P0130036",
            "resultData": {
                "P0130036Data": {
                    "detailListMeta": {"totalCount": "1"},
                    "detailList": detail_list,
                },
                "P0130036Status": "4",
            },
            "packetCnt": 1,
            "resultCode": "00000",
            "resultDesc": "成功",
            "isCompressed": 0,
        }

        normalized = client_module.normalize_interface_response(
            raw_response,
            interface,
        )

        self.assertEqual(normalized["product_code"], "P0130036")
        self.assertTrue(normalized["success"])
        self.assertTrue(normalized["has_result"])
        self.assertEqual(normalized["data"]["detailListMeta"]["totalCount"], "1")
        self.assertEqual(normalized["detailList"], detail_list)
        self.assertIs(normalized["raw_response"], raw_response)

    def test_p0130038_metadata_and_normalized_response(self) -> None:
        self.assertIn("P0130038", interfaces.INTERFACES)
        interface = interfaces.INTERFACES["P0130038"]
        self.assertEqual(interface.status_field, "P0130038Status")
        self.assertEqual(interface.data_field, "P0130038Data")
        self.assertIsNone(interface.shortcut_field)

        industry_data = {
            "property": [
                {
                    "orderPatentCntRank": "12",
                    "avgCntPatentAll": "8.5",
                }
            ]
        }
        raw_response = {
            "orderNo": "order-P0130038",
            "resultData": {
                "P0130038Data": industry_data,
                "P0130038Status": "4",
            },
            "packetCnt": 1,
            "resultCode": "00000",
            "resultDesc": "成功",
            "isCompressed": 0,
        }

        normalized = client_module.normalize_interface_response(
            raw_response,
            interface,
        )

        self.assertEqual(normalized["product_code"], "P0130038")
        self.assertTrue(normalized["success"])
        self.assertTrue(normalized["has_result"])
        self.assertEqual(normalized["data"], industry_data)
        self.assertIs(normalized["raw_response"], raw_response)

    def test_p0210004_metadata_and_normalized_response(self) -> None:
        self.assertIn("P0210004", interfaces.INTERFACES)
        interface = interfaces.INTERFACES["P0210004"]
        self.assertEqual(interface.status_field, "P0210004Status")
        self.assertEqual(interface.data_field, "P0210004Data")
        self.assertIsNone(interface.shortcut_field)

        financial_data = {
            "fncmfninInfo": [
                {
                    "companyName": "测试银行股份有限公司",
                    "reportDate": "2025-12-31",
                    "totalAssets": "1000000.000000",
                    "currency": "CNY",
                }
            ],
            "mainfinadataInfo": [],
            "incomeInfo": [],
            "cashflowInfo": [],
            "rgcashflowInfo": [],
            "rgbalanceInfo": [],
            "balanceInfo": [],
            "rgincomeInfo": [],
        }
        raw_response = {
            "orderNo": "order-P0210004",
            "resultData": {
                "P0210004Data": financial_data,
                "P0210004Status": "4",
            },
            "packetCnt": 1,
            "resultCode": "00000",
            "resultDesc": "成功",
            "isCompressed": 0,
        }

        normalized = client_module.normalize_interface_response(
            raw_response,
            interface,
        )

        self.assertEqual(normalized["product_code"], "P0210004")
        self.assertTrue(normalized["success"])
        self.assertTrue(normalized["has_result"])
        self.assertEqual(normalized["data"], financial_data)
        self.assertNotIn("fncmfninInfo", normalized)
        self.assertIs(normalized["raw_response"], raw_response)

    def test_p0990022_metadata_and_normalized_response(self) -> None:
        self.assertIn("P0990022", interfaces.INTERFACES)
        interface = interfaces.INTERFACES["P0990022"]
        self.assertEqual(interface.status_field, "P0990022Status")
        self.assertEqual(interface.data_field, "P0990022Data")
        self.assertEqual(interface.shortcut_field, "suppList")

        supplier_list = [
            {
                "suppId": "supplier-1",
                "zzjgdm": "91440000123456789X",
                "kgEnt": [],
            }
        ]
        raw_response = {
            "orderNo": "order-P0990022",
            "resultData": {
                "P0990022Data": {
                    "suppListMeta": {"totalCount": "1"},
                    "suppList": supplier_list,
                },
                "P0990022Status": "4",
            },
            "packetCnt": 1,
            "resultCode": "00000",
            "resultDesc": "成功",
            "isCompressed": 0,
        }

        normalized = client_module.normalize_interface_response(
            raw_response,
            interface,
        )

        self.assertEqual(normalized["product_code"], "P0990022")
        self.assertTrue(normalized["success"])
        self.assertTrue(normalized["has_result"])
        self.assertEqual(normalized["suppList"], supplier_list)
        self.assertIs(normalized["raw_response"], raw_response)


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

    async def test_equity_conclusion_tools_map_exact_upstream_fields(self) -> None:
        await server.p0020129_query_controller_and_ubo(
            ent_info="证通股份有限公司",
        )
        await server.p0090011_query_ubo_full_paths(
            ent_name="911000001000013428",
        )
        await server.p0020014_query_suspected_relationships(
            ent_info="证通股份有限公司",
            relation_type="emailSus",
        )
        await server.p0020019_query_suspected_controller(
            ent_info="证通股份有限公司",
            path_type="1",
            final_flag="1",
        )

        self.assertEqual(
            self.client.calls,
            [
                ("P0020129", {"entInfo": "证通股份有限公司"}),
                ("P0090011", {"entName": "911000001000013428"}),
                (
                    "P0020014",
                    {"entInfo": "证通股份有限公司", "type": "emailSus"},
                ),
                (
                    "P0020019",
                    {
                        "entInfo": "证通股份有限公司",
                        "type": "1",
                        "finalFlag": "1",
                    },
                ),
            ],
        )

    async def test_p0020023_maps_penetration_defaults_and_filters(self) -> None:
        default_result = await server.p0020023_query_equity_penetration(
            ent_info="阳光电源股份有限公司",
        )
        filtered_result = await server.p0020023_query_equity_penetration(
            ent_info="913401001492097421",
            level="5",
            ratio="30.5",
            extra_params={"customParam": "custom-value"},
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0020023",
                    {
                        "entInfo": "阳光电源股份有限公司",
                        "level": "3",
                        "ratio": "5",
                    },
                ),
                (
                    "P0020023",
                    {
                        "entInfo": "913401001492097421",
                        "level": "5",
                        "ratio": "30.5",
                        "customParam": "custom-value",
                    },
                ),
            ],
        )
        self.assertEqual(default_result["prod_code"], "P0020023")
        self.assertEqual(filtered_result["prod_code"], "P0020023")

    async def test_relationship_tools_normalize_lists_and_defaults(self) -> None:
        await server.p0020044_query_intercompany_relationship(
            ent_info=[" 企业甲 ", "企业乙"],
        )
        await server.p0020031_query_multi_point_relationships(
            ent_info="企业甲， 企业乙",
            person_names=["企业甲-张三", " 企业乙-李四 "],
            depth="3",
            relation_type="2",
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0020044",
                    {"entInfo": "企业甲,企业乙", "depth": "5", "weight": "0"},
                ),
                (
                    "P0020031",
                    {
                        "entInfo": "企业甲,企业乙",
                        "persName": "企业甲-张三,企业乙-李四",
                        "depth": "3",
                        "weight": "2",
                    },
                ),
            ],
        )

    async def test_relationship_tools_validate_subject_limits(self) -> None:
        with self.assertRaisesRegex(ValueError, "at most 10"):
            await server.p0020044_query_intercompany_relationship(
                ent_info=[f"企业{index}" for index in range(11)],
            )

        with self.assertRaisesRegex(ValueError, "At least one"):
            await server.p0020031_query_multi_point_relationships()

        with self.assertRaisesRegex(ValueError, "at most 10"):
            await server.p0020031_query_multi_point_relationships(
                ent_info=[f"企业{index}" for index in range(6)],
                person_names=[f"企业{index}-人员" for index in range(5)],
            )

        with self.assertRaisesRegex(ValueError, "must not override"):
            await server.p0020044_query_intercompany_relationship(
                ent_info="企业甲",
                extra_params={
                    "entInfo": [f"覆盖企业{index}" for index in range(11)],
                },
            )

        self.assertEqual(self.client.calls, [])

    async def test_equity_tool_schemas_expose_documented_enums(self) -> None:
        tools = {tool.name: tool for tool in await server.mcp.list_tools()}

        suspected_schema = tools[
            "p0020014_query_suspected_relationships"
        ].inputSchema["properties"]["relation_type"]["anyOf"]
        self.assertEqual(
            next(item["enum"] for item in suspected_schema if "enum" in item),
            list(get_args(server.P0020014RelationType)),
        )

        for tool_name in (
            "p0020031_query_multi_point_relationships",
            "p0020044_query_intercompany_relationship",
        ):
            with self.subTest(tool_name=tool_name):
                schema = tools[tool_name].inputSchema["properties"]
                self.assertEqual(
                    schema["relation_type"]["enum"],
                    list(get_args(server.RelationshipWeight)),
                )
                self.assertEqual(schema["relation_type"]["default"], "0")
                self.assertEqual(schema["depth"]["default"], "5")

        controller_schema = tools[
            "p0020019_query_suspected_controller"
        ].inputSchema["properties"]
        self.assertEqual(controller_schema["path_type"]["enum"], ["0", "1"])
        self.assertEqual(controller_schema["final_flag"]["enum"], ["0", "1"])
        self.assertIn(
            "data.MatchInfoList[]",
            tools["p0090011_query_ubo_full_paths"].description or "",
        )

    async def test_equity_tool_input_schemas_are_self_describing(self) -> None:
        tools = {tool.name: tool for tool in await server.mcp.list_tools()}
        tool_names = (
            "p0020014_query_suspected_relationships",
            "p0020019_query_suspected_controller",
            "p0020023_query_equity_penetration",
            "p0020031_query_multi_point_relationships",
            "p0020044_query_intercompany_relationship",
            "p0020129_query_controller_and_ubo",
            "p0090011_query_ubo_full_paths",
        )

        for tool_name in tool_names:
            with self.subTest(tool_name=tool_name):
                properties = tools[tool_name].inputSchema["properties"]
                for parameter_name, parameter_schema in properties.items():
                    with self.subTest(parameter_name=parameter_name):
                        self.assertTrue(parameter_schema.get("description"))
                        self.assertTrue(parameter_schema.get("examples"))
                self.assertIn(
                    "不得重复或覆盖",
                    properties["extra_params"]["description"],
                )

        for tool_name, identifier_name in (
            ("p0020014_query_suspected_relationships", "ent_info"),
            ("p0020019_query_suspected_controller", "ent_info"),
            ("p0020023_query_equity_penetration", "ent_info"),
            ("p0020129_query_controller_and_ubo", "ent_info"),
            ("p0090011_query_ubo_full_paths", "ent_name"),
        ):
            with self.subTest(tool_name=tool_name):
                tool_schema = tools[tool_name].inputSchema
                self.assertIn(identifier_name, tool_schema["required"])
                self.assertEqual(
                    tool_schema["properties"][identifier_name]["minLength"],
                    1,
                )

        intercompany_schema = tools[
            "p0020044_query_intercompany_relationship"
        ].inputSchema["properties"]
        company_array = next(
            item
            for item in intercompany_schema["ent_info"]["anyOf"]
            if item.get("type") == "array"
        )
        self.assertEqual(company_array["minItems"], 1)
        self.assertEqual(company_array["maxItems"], 10)
        self.assertEqual(company_array["items"]["minLength"], 1)
        self.assertEqual(intercompany_schema["depth"]["pattern"], r"^[1-9]\d*$")
        self.assertIn("0=投资和任职", intercompany_schema["relation_type"]["description"])

        multi_schema = tools[
            "p0020031_query_multi_point_relationships"
        ].inputSchema["properties"]
        self.assertIn("至少提供一项", multi_schema["ent_info"]["description"])
        self.assertIn("合计最多 10", multi_schema["person_names"]["description"])
        self.assertIn("任职企业全称-姓名", multi_schema["person_names"]["description"])
        self.assertIn("建议先用 2", multi_schema["depth"]["description"])

        penetration_schema = tools[
            "p0020023_query_equity_penetration"
        ].inputSchema["properties"]
        self.assertEqual(
            penetration_schema["level"]["enum"],
            list(get_args(server.P0020023Level)),
        )
        self.assertEqual(penetration_schema["level"]["default"], "3")
        self.assertEqual(penetration_schema["ratio"]["default"], "5")
        self.assertIn("0 至 100", penetration_schema["ratio"]["description"])
        self.assertIn("pattern", penetration_schema["ratio"])

    async def test_equity_tools_reject_core_extra_param_overrides(self) -> None:
        calls = (
            server.p0020014_query_suspected_relationships(
                "测试企业",
                extra_params={"type": "telSus"},
            ),
            server.p0020019_query_suspected_controller(
                "测试企业",
                extra_params={"finalFlag": "1"},
            ),
            server.p0020023_query_equity_penetration(
                "测试企业",
                extra_params={"level": "1"},
            ),
            server.p0020031_query_multi_point_relationships(
                ent_info="测试企业",
                extra_params={"depth": "2"},
            ),
            server.p0020044_query_intercompany_relationship(
                ent_info="测试企业",
                extra_params={"weight": "2"},
            ),
            server.p0020129_query_controller_and_ubo(
                "测试企业",
                extra_params={"entInfo": "覆盖企业"},
            ),
            server.p0090011_query_ubo_full_paths(
                "测试企业",
                extra_params={"entName": "覆盖企业"},
            ),
        )

        for call in calls:
            with self.assertRaisesRegex(ValueError, "must not override"):
                await call

        self.assertEqual(self.client.calls, [])

    async def test_equity_tool_schemas_reject_invalid_mcp_inputs(self) -> None:
        invalid_calls = (
            (
                "p0020129_query_controller_and_ubo",
                {"ent_info": ""},
            ),
            (
                "p0020044_query_intercompany_relationship",
                {"ent_info": [f"企业{index}" for index in range(11)]},
            ),
            (
                "p0020044_query_intercompany_relationship",
                {"ent_info": ["企业甲"], "depth": "0"},
            ),
            (
                "p0020023_query_equity_penetration",
                {"ent_info": "测试企业", "level": "6"},
            ),
            (
                "p0020023_query_equity_penetration",
                {"ent_info": "测试企业", "ratio": "100.01"},
            ),
        )

        for tool_name, arguments in invalid_calls:
            with self.subTest(tool_name=tool_name, arguments=arguments):
                with self.assertRaises(ToolError):
                    await server.mcp.call_tool(tool_name, arguments)

        self.assertEqual(self.client.calls, [])

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

    async def test_p0130025_maps_indicator_type_and_extra_params(
        self,
    ) -> None:
        self.assertTrue(
            hasattr(server, "p0130025_query_company_key_indicators")
        )

        explicit_result = await server.p0130025_query_company_key_indicators(
            ent_info="证通股份有限公司",
            indicator_type="2",
        )
        default_result = await server.p0130025_query_company_key_indicators(
            ent_info="证通股份有限公司",
        )
        override_result = await server.p0130025_query_company_key_indicators(
            ent_info="证通股份有限公司",
            extra_params={
                "type": "2",
                "customParam": "custom-value",
            },
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0130025",
                    {
                        "entInfo": "证通股份有限公司",
                        "type": "2",
                    },
                ),
                (
                    "P0130025",
                    {
                        "entInfo": "证通股份有限公司",
                        "type": "1",
                    },
                ),
                (
                    "P0130025",
                    {
                        "entInfo": "证通股份有限公司",
                        "type": "2",
                        "customParam": "custom-value",
                    },
                ),
            ],
        )
        self.assertEqual(explicit_result["prod_code"], "P0130025")
        self.assertEqual(default_result["prod_code"], "P0130025")
        self.assertEqual(override_result["prod_code"], "P0130025")

    async def test_p0130025_schema_exposes_default_type_enum(
        self,
    ) -> None:
        tools = await server.mcp.list_tools()
        tool = next(
            item
            for item in tools
            if item.name == "p0130025_query_company_key_indicators"
        )

        self.assertIn("ent_info", tool.inputSchema["required"])
        self.assertNotIn("indicator_type", tool.inputSchema["required"])
        indicator_schema = tool.inputSchema["properties"]["indicator_type"]
        self.assertEqual(
            indicator_schema["enum"],
            list(get_args(server.P0130025IndicatorType)),
        )
        self.assertEqual(indicator_schema["default"], "1")
        self.assertIn("1=指标等级、2=指标金额", tool.description or "")
        self.assertIn("coreLndicatorInfo", tool.description or "")
        self.assertIn("底层接口原始拼写", tool.description or "")

    async def test_p0130036_maps_land_filter_pagination_and_extra_params(
        self,
    ) -> None:
        self.assertTrue(hasattr(server, "p0130036_query_land_info"))

        result = await server.p0130036_query_land_info(
            ent_info="证通股份有限公司",
            land_type="tddy",
            page_no="2",
            page_size="20",
            extra_params={
                "range": "25",
                "customParam": "custom-value",
            },
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0130036",
                    {
                        "entInfo": "证通股份有限公司",
                        "type": "tddy",
                        "pageNo": "2",
                        "range": "25",
                        "customParam": "custom-value",
                    },
                )
            ],
        )
        self.assertEqual(result["prod_code"], "P0130036")

    async def test_p0130036_schema_exposes_required_identifier_and_type_enum(
        self,
    ) -> None:
        tools = await server.mcp.list_tools()
        tool = next(
            item
            for item in tools
            if item.name == "p0130036_query_land_info"
        )

        self.assertIn("ent_info", tool.inputSchema["required"])
        self.assertNotIn("land_type", tool.inputSchema["required"])
        variants = tool.inputSchema["properties"]["land_type"]["anyOf"]
        enum_schema = next(item for item in variants if "enum" in item)
        self.assertEqual(
            enum_schema["enum"],
            list(get_args(server.P0130036LandType)),
        )
        self.assertIn("tdgy=土地供应", tool.description or "")
        self.assertIn("tddy=土地抵押", tool.description or "")

    async def test_p0130038_maps_industry_filters_and_extra_params(
        self,
    ) -> None:
        self.assertTrue(hasattr(server, "p0130038_query_industry_analysis"))

        result = await server.p0130038_query_industry_analysis(
            ent_info="证通股份有限公司",
            analysis_type="property",
            nic_lvl="n3",
            region_lvl="r2",
            region_id="440300",
            nic_id="C391",
            extra_params={
                "regionId": "440100",
                "customParam": "custom-value",
            },
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0130038",
                    {
                        "entInfo": "证通股份有限公司",
                        "type": "property",
                        "nicLvl": "n3",
                        "regionLvl": "r2",
                        "regionId": "440100",
                        "nicId": "C391",
                        "customParam": "custom-value",
                    },
                )
            ],
        )
        self.assertEqual(result["prod_code"], "P0130038")

    async def test_p0130038_schema_exposes_required_fields_and_enums(
        self,
    ) -> None:
        tools = await server.mcp.list_tools()
        tool = next(
            item
            for item in tools
            if item.name == "p0130038_query_industry_analysis"
        )

        self.assertIn("ent_info", tool.inputSchema["required"])
        self.assertIn("analysis_type", tool.inputSchema["required"])
        self.assertEqual(
            tool.inputSchema["properties"]["analysis_type"]["enum"],
            list(get_args(server.P0130038AnalysisType)),
        )

        nic_variants = tool.inputSchema["properties"]["nic_lvl"]["anyOf"]
        nic_enum = next(item["enum"] for item in nic_variants if "enum" in item)
        self.assertEqual(nic_enum, list(get_args(server.P0130038NicLevel)))

        region_variants = tool.inputSchema["properties"]["region_lvl"]["anyOf"]
        region_enum = next(
            item["enum"] for item in region_variants if "enum" in item
        )
        self.assertEqual(
            region_enum,
            list(get_args(server.P0130038RegionLevel)),
        )
        self.assertIn(
            "property=企业知识产权区域行业排名",
            tool.description or "",
        )
        self.assertIn("不同分析类型返回的数据字段不同", tool.description or "")

    async def test_p0210004_maps_financial_filters_and_extra_params(
        self,
    ) -> None:
        self.assertTrue(
            hasattr(server, "p0210004_query_listed_company_financial_data")
        )

        result = await server.p0210004_query_listed_company_financial_data(
            ent_info="测试银行股份有限公司",
            financial_type="fncmfnin",
            start_date="2024-01-01",
            end_date="2025-12-31",
            extra_params={
                "endDate": "2026-06-30",
                "customParam": "custom-value",
            },
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0210004",
                    {
                        "entInfo": "测试银行股份有限公司",
                        "type": "fncmfnin",
                        "startDate": "2024-01-01",
                        "endDate": "2026-06-30",
                        "customParam": "custom-value",
                    },
                )
            ],
        )
        self.assertEqual(result["prod_code"], "P0210004")

    async def test_p0210004_schema_exposes_required_type_enum_and_dates(
        self,
    ) -> None:
        tools = await server.mcp.list_tools()
        tool = next(
            item
            for item in tools
            if item.name == "p0210004_query_listed_company_financial_data"
        )

        self.assertIn("ent_info", tool.inputSchema["required"])
        self.assertIn("financial_type", tool.inputSchema["required"])
        self.assertNotIn("start_date", tool.inputSchema["required"])
        self.assertNotIn("end_date", tool.inputSchema["required"])
        self.assertEqual(
            tool.inputSchema["properties"]["financial_type"]["enum"],
            list(get_args(server.P0210004FinancialType)),
        )
        self.assertEqual(len(get_args(server.P0210004FinancialType)), 8)
        self.assertIn("fncmfnin=金融公司主要财务指标", tool.description or "")
        self.assertIn("格式均为 YYYY-MM-DD", tool.description or "")
        self.assertIn("data.rgincomeInfo", tool.description or "")

    async def test_p0990022_maps_enterprise_identifier_and_extra_params(
        self,
    ) -> None:
        self.assertTrue(hasattr(server, "p0990022_query_supplier_relationships"))

        result = await server.p0990022_query_supplier_relationships(
            ent_info="证通股份有限公司",
            extra_params={"customParam": "custom-value"},
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0990022",
                    {
                        "entInfo": "证通股份有限公司",
                        "customParam": "custom-value",
                    },
                )
            ],
        )
        self.assertEqual(result["prod_code"], "P0990022")

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

    async def test_p0010059_maps_identifier_and_types(self) -> None:
        result = await server.p0010059_query_business_basic_brief(
            credit_code=" 911000001000013428 ",
            types=["basic", "shareholder", "companyCancelEasy"],
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0010059",
                    {
                        "entName": None,
                        "creditCode": " 911000001000013428 ",
                        "regNo": None,
                        "orgCode": None,
                        "type": "basic,shareholder,companyCancelEasy",
                    },
                )
            ],
        )
        self.assertEqual(result["prod_code"], "P0010059")

    async def test_p0010059_requires_exactly_one_identifier(self) -> None:
        with self.assertRaisesRegex(ValueError, "Exactly one"):
            await server.p0010059_query_business_basic_brief(types=["basic"])

        with self.assertRaisesRegex(ValueError, "Exactly one"):
            await server.p0010059_query_business_basic_brief(
                ent_name="测试企业",
                credit_code="911000000000000000",
                types=["basic"],
            )

        with self.assertRaisesRegex(ValueError, "Exactly one"):
            await server.p0010059_query_business_basic_brief(
                ent_name="测试企业",
                extra_params={"creditCode": "911000000000000000"},
            )

        self.assertEqual(self.client.calls, [])

    async def test_p0010059_schema_exposes_all_type_values(self) -> None:
        tools = await server.mcp.list_tools()
        tool = next(
            item
            for item in tools
            if item.name == "p0010059_query_business_basic_brief"
        )
        variants = tool.inputSchema["properties"]["types"]["anyOf"]
        array_schema = next(item for item in variants if item.get("type") == "array")

        self.assertEqual(
            array_schema["items"]["enum"],
            list(get_args(server.P0010059Type)),
        )
        self.assertEqual(len(array_schema["items"]["enum"]), 33)

    async def test_p0010059_metadata_has_only_input_schema(self) -> None:
        tools = await server.mcp.list_tools()
        tool = next(
            item
            for item in tools
            if item.name == "p0010059_query_business_basic_brief"
        )

        input_properties = tool.inputSchema["properties"]
        self.assertEqual(
            set(input_properties),
            {
                "ent_name",
                "credit_code",
                "reg_no",
                "org_code",
                "types",
                "extra_params",
            },
        )
        for parameter_name, parameter_schema in input_properties.items():
            with self.subTest(parameter_name=parameter_name):
                self.assertTrue(parameter_schema.get("description"))

        self.assertIn("严格四选一", input_properties["ent_name"]["description"])
        self.assertIn(
            "companyCancelEasy=简易注销公告",
            input_properties["types"]["description"],
        )
        self.assertIn("camelCase", input_properties["extra_params"]["description"])

        self.assertIsNone(tool.outputSchema)

        description = tool.description or ""
        self.assertIn("summary", description)
        self.assertIn("中文", description)
        self.assertIn("structured_data", description)
        self.assertIn("不是工具原始 JSON 中新增的顶层字段", description)
        self.assertIn("raw_response", description)
        self.assertIn("data.caseRandomCheckList[].detail[]", description)
        self.assertIn(
            "data.companyIprList[].companyIprChange[]",
            description,
        )
        self.assertIn(
            "data.companyCancelEasyList[].companyCancelEasyObjections[]",
            description,
        )
        self.assertIn("标注为万元", description)
        self.assertIn("不得自行乘以 100", description)
        self.assertIn("YYYY-MM-DD", description)

        expected_data_paths = {
            "data.basicList[]",
            "data.personList[]",
            "data.shareholderList[]",
            "data.originalShareholderList[]",
            "data.alterList[]",
            "data.filiationList[]",
            "data.exceptionList[]",
            "data.liquidationList[]",
            "data.mortAltList[]",
            "data.mortDetailList[]",
            "data.mortCanList[]",
            "data.mortPriClaSec[]",
            "data.mortguaInfoList[]",
            "data.mortOrgList[]",
            "data.mortRegList[]",
            "data.sharFrozList[]",
            "data.sharePledgList[]",
            "data.sharePledgAltList[]",
            "data.sharePledgCanList[]",
            "data.changeRecordsList[]",
            "data.changeStockRightsList[]",
            "data.basicInformationList[]",
            "data.provideGuaranteeList[]",
            "data.foreignInvestmentList[]",
            "data.yearReportPaidUpCapitalList[]",
            "data.socialInsuranceList[]",
            "data.yearReportSubCapitals[]",
            "data.websiteOrOnlineList[]",
            "data.illegalList[]",
            "data.caseCheckList[]",
            "data.caseRandomCheckList[]",
            "data.companyIprList[]",
            "data.companyCancelEasyList[]",
        }
        for data_path in expected_data_paths:
            with self.subTest(data_path=data_path):
                self.assertIn(data_path, description)

    async def test_p0010059_unstructured_output_preserves_payload_shape(self) -> None:
        payload = {
            "product_code": "P0010059",
            "interface_name": "企业工商基本信息查询（简项）",
            "success": True,
            "has_result": True,
            "result_code": "00000",
            "result_code_desc": "查询成功",
            "result_desc": "成功",
            "product_status": "4",
            "product_status_desc": "查询成功有结果",
            "order_no": None,
            "packet_count": 1,
            "is_compressed": 0,
            "data": {
                "caseRandomCheckList": [
                    {
                        "no": 1,
                        "detail": [
                            {
                                "checkItem": "企业投资项目监督检查",
                                "checkResult": None,
                            }
                        ],
                        "unknownNested": {"source": "upstream"},
                    }
                ],
                "unknownBlock": [{"value": 1}],
            },
            "raw_response": {"custom": None},
        }

        class StaticResponseClient:
            async def query_product(
                self,
                prod_code: str,
                params: dict[str, Any],
            ) -> dict[str, Any]:
                return payload

        with patch.object(server, "get_client", return_value=StaticResponseClient()):
            content = await server.mcp.call_tool(
                "p0010059_query_business_basic_brief",
                {"ent_name": "测试企业", "types": ["caseRandomCheck"]},
            )

        self.assertEqual(len(content), 1)
        unstructured_output = json.loads(content[0].text)
        self.assertEqual(unstructured_output, payload)
        self.assertIsNone(unstructured_output["order_no"])
        self.assertIsInstance(
            unstructured_output["data"]["caseRandomCheckList"][0]["no"],
            int,
        )
        self.assertNotIn("basicList", unstructured_output)
        self.assertNotIn("mortOrgList", unstructured_output["data"])

    async def test_p0980006_maps_filters_defaults_and_extra_overrides(self) -> None:
        result = await server.p0980006_query_advanced_company_filter(
            eid="1911000001000013428",
            area_prefix="11",
            org_scale="大型",
            est_date_start="2000-01-01",
            extra_params={
                "eid": "19144030010001686XA",
                "range": "25",
                "customFilter": "custom-value",
            },
        )

        product_code, params = self.client.calls[0]
        self.assertEqual(product_code, "P0980006")
        self.assertEqual(params["eid"], "19144030010001686XA")
        self.assertEqual(params["areaPrefix"], "11")
        self.assertEqual(params["orgScale"], "大型")
        self.assertEqual(params["estDateStart"], "2000-01-01")
        self.assertEqual(params["pageNo"], "1")
        self.assertEqual(params["range"], "25")
        self.assertEqual(params["customFilter"], "custom-value")
        self.assertEqual(result["prod_code"], "P0980006")

    async def test_p0980006_schema_exposes_eid_without_keyword(self) -> None:
        tools = await server.mcp.list_tools()
        tool = next(
            item
            for item in tools
            if item.name == "p0980006_query_advanced_company_filter"
        )

        self.assertIn("eid", tool.inputSchema["properties"])
        self.assertNotIn("eid", tool.inputSchema.get("required", []))
        self.assertNotIn("keyword", tool.inputSchema["properties"])

    async def test_eid_resolution_guidance_is_exposed_to_ai(self) -> None:
        tools = {
            tool.name: tool
            for tool in await server.mcp.list_tools()
        }
        resolver_description = tools[
            "p0010010_query_business_profile"
        ].description
        self.assertIn("basicList[].entId", resolver_description)
        self.assertIn("准确匹配", resolver_description)
        self.assertIn("不得", resolver_description)

        for tool_name in (
            "p0980008_query_tax_rating",
            "p0980023_query_two_year_risk_summary",
        ):
            with self.subTest(tool_name=tool_name):
                description = tools[tool_name].description
                self.assertIn(
                    "p0010010_query_business_profile",
                    description,
                )
                self.assertIn("basicList[].entId", description)
                self.assertIn("不得自行推算 eid", description)

        self.assertIn(
            "p0010010_query_business_profile",
            server.mcp.instructions,
        )
        self.assertIn("basicList[].entId", server.mcp.instructions)
        self.assertIn("不得", server.mcp.instructions)

    async def test_portrait_tools_map_simple_identifiers(self) -> None:
        await server.p0980008_query_tax_rating(
            eid="1911000001000013428",
            extra_params={"source": "test"},
        )
        await server.p0980023_query_two_year_risk_summary(
            eid="1911000001000013428",
        )
        await server.p0980033_query_listing_financing_bidding_ipr(
            ent_info="中国银行股份有限公司",
        )

        self.assertEqual(
            self.client.calls,
            [
                (
                    "P0980008",
                    {
                        "eid": "1911000001000013428",
                        "source": "test",
                    },
                ),
                (
                    "P0980023",
                    {"eid": "1911000001000013428"},
                ),
                (
                    "P0980033",
                    {"entInfo": "中国银行股份有限公司"},
                ),
            ],
        )

    async def test_all_tool_descriptions_come_from_function_docstrings(self) -> None:
        tool_functions = {
            "p0010010_query_business_profile": server.p0010010_query_business_profile,
            "p0010058_query_business_basic_deep": (
                server.p0010058_query_business_basic_deep
            ),
            "p0010059_query_business_basic_brief": (
                server.p0010059_query_business_basic_brief
            ),
            "p0010068_fuzzy_search_company_name": (
                server.p0010068_fuzzy_search_company_name
            ),
            "p0010073_query_trademark_info": server.p0010073_query_trademark_info,
            "p0010074_query_software_copyright_info": (
                server.p0010074_query_software_copyright_info
            ),
            "p0010075_query_work_copyright_info": (
                server.p0010075_query_work_copyright_info
            ),
            "p0010076_query_icp_filing_info": server.p0010076_query_icp_filing_info,
            "p0010078_query_patent_info": server.p0010078_query_patent_info,
            "p0010084_query_license_info": server.p0010084_query_license_info,
            "p0020014_query_suspected_relationships": (
                server.p0020014_query_suspected_relationships
            ),
            "p0020019_query_suspected_controller": (
                server.p0020019_query_suspected_controller
            ),
            "p0020021_query_single_point_related_info": (
                server.p0020021_query_single_point_related_info
            ),
            "p0020023_query_equity_penetration": (
                server.p0020023_query_equity_penetration
            ),
            "p0020031_query_multi_point_relationships": (
                server.p0020031_query_multi_point_relationships
            ),
            "p0020044_query_intercompany_relationship": (
                server.p0020044_query_intercompany_relationship
            ),
            "p0020129_query_controller_and_ubo": (
                server.p0020129_query_controller_and_ubo
            ),
            "p0050007_query_public_opinion_list": (
                server.p0050007_query_public_opinion_list
            ),
            "p0050008_query_public_opinion_detail": (
                server.p0050008_query_public_opinion_detail
            ),
            "p0050007_p0050008_query_public_opinion_info": (
                server.p0050007_p0050008_query_public_opinion_info
            ),
            "p0060007_verify_business_two_elements": (
                server.p0060007_verify_business_two_elements
            ),
            "p0060008_verify_business_three_elements": (
                server.p0060008_verify_business_three_elements
            ),
            "p0090011_query_ubo_full_paths": server.p0090011_query_ubo_full_paths,
            "p0110003_query_honor_qualification_info": (
                server.p0110003_query_honor_qualification_info
            ),
            "p0130025_query_company_key_indicators": (
                server.p0130025_query_company_key_indicators
            ),
            "p0130036_query_land_info": server.p0130036_query_land_info,
            "p0130038_query_industry_analysis": (
                server.p0130038_query_industry_analysis
            ),
            "p0210004_query_listed_company_financial_data": (
                server.p0210004_query_listed_company_financial_data
            ),
            "p0980006_query_advanced_company_filter": (
                server.p0980006_query_advanced_company_filter
            ),
            "p0980008_query_tax_rating": server.p0980008_query_tax_rating,
            "p0980023_query_two_year_risk_summary": (
                server.p0980023_query_two_year_risk_summary
            ),
            "p0980033_query_listing_financing_bidding_ipr": (
                server.p0980033_query_listing_financing_bidding_ipr
            ),
            "p0990022_query_supplier_relationships": (
                server.p0990022_query_supplier_relationships
            ),
            "query_cisp_product": server.query_cisp_product,
        }
        tools = {
            tool.name: tool
            for tool in await server.mcp.list_tools()
        }

        self.assertEqual(set(tools), set(tool_functions))
        for tool_name, tool_function in tool_functions.items():
            with self.subTest(tool_name=tool_name):
                self.assertEqual(
                    (tools[tool_name].description or "").rstrip(),
                    inspect.getdoc(tool_function),
                )

    async def test_mcp_lists_all_thirty_four_tools(self) -> None:
        tools = await server.mcp.list_tools()
        names = {tool.name for tool in tools}

        self.assertEqual(len(names), 34)
        self.assertTrue(
            {
                "p0010059_query_business_basic_brief",
                "p0020014_query_suspected_relationships",
                "p0020019_query_suspected_controller",
                "p0020023_query_equity_penetration",
                "p0020031_query_multi_point_relationships",
                "p0020044_query_intercompany_relationship",
                "p0020129_query_controller_and_ubo",
                "p0090011_query_ubo_full_paths",
                "p0130025_query_company_key_indicators",
                "p0130036_query_land_info",
                "p0130038_query_industry_analysis",
                "p0210004_query_listed_company_financial_data",
                "p0980006_query_advanced_company_filter",
                "p0980008_query_tax_rating",
                "p0980023_query_two_year_risk_summary",
                "p0980033_query_listing_financing_bidding_ipr",
                "p0990022_query_supplier_relationships",
            }.issubset(names)
        )


if __name__ == "__main__":
    unittest.main()
