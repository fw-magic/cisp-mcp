# CISP MCP 全接口实测报告

- 测试日期：2026-07-31（Asia/Shanghai）
- Connector：`cisp-mcp`
- 测试企业：阳光电源股份有限公司
- 统一社会信用代码：`913401001492097421`
- 法定代表人：曹仁贤
- CISP `entId`：`1913401001492097421`
- 测试范围：当前服务注册的全部 27 个 MCP 工具

## 判定口径

- **调用正常**：工具 schema 校验、MCP 传输、Bearer 鉴权和 CISP 网关请求均正常完成。
- **业务正常**：除调用正常外，产品返回成功且取得业务数据；组合工具按其独立返回结构判断。
- **产品异常**：MCP 和网关调用成功，但具体产品状态为失败或没有形成有效业务结果。

## 结论

- 27/27 个工具均可被实际调用，没有出现 MCP schema、连接、鉴权或传输错误。
- 26/27 个工具取得符合预期的成功业务结果。
- `p0980033_query_listing_financing_bidding_ipr` 的 MCP 封装可调用，但上游 `P0980033` 产品持续返回状态 `3`（查询失败），属于产品级异常。

## 逐接口结果

| 序号 | 工具 | 主要实测参数 | 结果 | 关键证据 |
| --- | --- | --- | --- | --- |
| 1 | `p0010010_query_business_profile` | `ent_info=阳光电源股份有限公司` | 业务正常 | `basicList=1`，精确取得信用代码、法定代表人及 `entId` |
| 2 | `p0010058_query_business_basic_deep` | `ent_name=阳光电源股份有限公司` | 业务正常 | `basicList=1`、`shareholderList=10`、`personList=8`，并返回变更、投资、年报等数据 |
| 3 | `p0010059_query_business_basic_brief` | `ent_name`；`types=[basic,person,shareholder]` | 业务正常 | `basicList=1`、`personList=8`、`shareholderList=10` |
| 4 | `p0010068_fuzzy_search_company_name` | `ent_name=阳光电源` | 业务正常 | `fuzzyList=10`，首条为阳光电源股份有限公司 |
| 5 | `p0010073_query_trademark_info` | 企业名称；第 1 页 2 条 | 业务正常 | `brandList=2` |
| 6 | `p0010074_query_software_copyright_info` | 企业名称；第 1 页 2 条 | 业务正常 | `swList=2` |
| 7 | `p0010075_query_work_copyright_info` | 企业名称；第 1 页 2 条 | 业务正常 | `resultList=2` |
| 8 | `p0010076_query_icp_filing_info` | 企业名称；第 1 页 2 条 | 业务正常 | `icpList=2` |
| 9 | `p0010078_query_patent_info` | 企业名称；第 1 页 2 条 | 业务正常 | `patentsList=2` |
| 10 | `p0010084_query_license_info` | `license_type=gs`；第 1 页 2 条 | 业务正常 | `detailList=2` |
| 11 | `p0020021_query_single_point_related_info` | `relation_direction=1` | 业务正常 | 投资与任职数据均返回，`entInvList=95` |
| 12 | `p0050007_query_public_opinion_list` | 企业名称；第 1 页 2 条 | 业务正常 | `infoList=2`，取得可用于详情查询的真实 `entryId` |
| 13 | `p0050008_query_public_opinion_detail` | 使用列表返回的真实 `entryId` | 业务正常 | `infoDetail=1` |
| 14 | `p0050007_p0050008_query_public_opinion_info` | 第 1 页 2 条；`max_details=1` | 业务正常 | 列表成功，`infoList=2`、`details=1`、`detail_count=1` |
| 15 | `p0060007_verify_business_two_elements` | 企业名称 + 真实信用代码 | 业务正常 | `orgNameMatch=1`、`regNoMatch=1` |
| 16 | `p0060008_verify_business_three_elements` | 企业名称 + 真实信用代码 + 曹仁贤 | 业务正常 | 企业名称、信用代码、法定代表人三项均匹配 |
| 17 | `p0110003_query_honor_qualification_info` | 企业名称 | 业务正常 | `itemNameList=45` |
| 18 | `p0130025_query_company_key_indicators` | `indicator_type=2` | 业务正常 | `coreLndicatorInfo=19` |
| 19 | `p0130036_query_land_info` | `land_type=tdgy`；第 1 页 2 条 | 业务正常 | `detailList=1` |
| 20 | `p0130038_query_industry_analysis` | `entRegionRank`；使用工商返回的地区和行业代码 | 业务正常 | `entRegionRank=3` |
| 21 | `p0210004_query_listed_company_financial_data` | `mainfinadata`；2024-01-01 至 2025-12-31 | 业务正常 | `mainfinadataInfo=13` |
| 22 | `p0980006_query_advanced_company_filter` | 真实 `eid`；第 1 页 2 条 | 业务正常 | `entList=1` |
| 23 | `p0980008_query_tax_rating` | 真实 `eid` | 业务正常 | 纳税评级 `list=9` |
| 24 | `p0980023_query_two_year_risk_summary` | 真实 `eid` | 业务正常 | 风险统计 `list=1` |
| 25 | `p0980033_query_listing_financing_bidding_ipr` | 企业名称、`entId`、信用代码分别重试 | **产品异常** | 三种输入均为 `resultCode=00000`，但产品状态 `3`、`has_result=false` |
| 26 | `p0990022_query_supplier_relationships` | 企业名称 | 业务正常 | `suppList=1` |
| 27 | `query_cisp_product` | `prod_code=P0010010`；企业名称 | 业务正常 | `basicList=1`、`entHisList=2` |

## P0980033 复核

为排除参数和封装问题，进行了以下复核：

1. 专用工具分别传入阳光电源股份有限公司的企业全称、真实 `entId`、统一社会信用代码，结果一致。
2. 通过 `query_cisp_product` 直接调用 `P0980033`，结果一致。
3. 使用“中国银行股份有限公司”作为控制样本调用专用工具，结果仍一致。
4. 所有调用均无 MCP、HTTP 或鉴权错误，CISP 网关 `resultCode` 均为 `00000`，但 `P0980033Status` 为 `3`。

因此，当前证据更支持 `P0980033` 的账号产品权限或上游产品服务异常，而不是阳光电源主体识别、参数格式或 MCP 专用工具封装错误。建议携带测试时间和服务端订单号，在受控日志中向 CISP 上游核查产品开通状态及失败原因；不要在对话或公开报告中暴露 API Key。
