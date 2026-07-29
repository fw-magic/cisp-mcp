from __future__ import annotations

import unittest
from typing import Any, get_args, get_type_hints
from unittest.mock import patch

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

    async def test_mcp_lists_all_twenty_six_tools(self) -> None:
        tools = await server.mcp.list_tools()
        names = {tool.name for tool in tools}

        self.assertEqual(len(names), 26)
        self.assertTrue(
            {
                "p0010059_query_business_basic_brief",
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
