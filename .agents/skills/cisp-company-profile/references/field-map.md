# CISP 企业一页纸画像字段映射

本参考只列画像编排需要的路径。字段语义以项目 `fields_test/fields/` 下各工具的完整字段文档为准。

## 1. 工商深度

工具：`p0010058_query_business_basic_deep`

### 主体照面

主要读取 `data.basicList[0]`：

| 展示项 | 字段 |
| --- | --- |
| 企业名称 | `orgName` |
| 统一社会信用代码 | `creditCode` |
| 登记状态 | `orgStatus` |
| 法定代表人 | `legRepName` |
| 企业类型 | `orgType` |
| 成立日期 | `estDate` |
| 注册资本 | `regCap` + `regCapCur` |
| 实收资本 | `paidInCap` |
| 注册地址 | `regAddr` |
| 登记机关 | `regOrg` |
| 行业 | `industry`，其次 `industryClas` |
| 经营期限 | `openFrom` + `openTo` |
| 经营范围 | `operateScope` |
| 曾用名 | `orgNameUsed` |
| 注销/吊销日期 | `cancelDate` / `revokeDate` |
| 核准日期 | `apprDate` |

注册资本和币种按响应原样组合，不自行换算单位。

### 股权、人员和经营网络

| 维度 | 列表 | 优先字段 |
| --- | --- | --- |
| 股东 | `data.shareholderList` | `shareholderName`, `shareholderType`, `fundedRatio`, `subConAmt`, `subConCur`, `conDate`, `conForm` |
| 历史股东 | `data.originalShareholderList` | 仅在用户要求历史沿革时展开 |
| 主要人员 | `data.personList` | `perName`, `position`, `isFr`, `personAmount` |
| 对外投资 | `data.entInvItemList` | 企业名称、状态、持股或出资相关返回字段 |
| 分支机构 | `data.filiationList` | 分支名称、负责人、状态相关返回字段 |
| 工商变更 | `data.alterList` | `busAltItem`, `busAltBef`, `busAltAft`, `busAltDate` |
| 网站/网店 | `data.websiteOrOnlineList` | `websiteName`, `website`, `websiteType`, `reportYear` |
| 社保信息 | `data.socialInsuranceList` | 年度与参保人数相关返回字段 |
| 实缴/认缴年报 | `data.yearReportPaidUpCapitalList`, `data.yearReportSubCapitalList` | 金额、日期、方式相关返回字段 |

一页纸最多展示 5 名股东、5 名主要人员和合计数量。股东比例可解析时按比例降序，无法解析时维持接口顺序。

### 风险事实

| 风险主题 | 列表 |
| --- | --- |
| 行政处罚 | `data.caseInfoList` |
| 经营异常 | `data.exceptionList` |
| 严重违法 | `data.illegalList` |
| 失信被执行 | `data.dishonestList` |
| 被执行 | `data.executedList` |
| 关联失信/执行 | `data.relateDishonestList`, `data.relatedExecutedList` |
| 股权冻结 | `data.sharFrozList` |
| 股权出质 | `data.sharePledgList` |
| 动产抵押 | 响应中各 mortgage 相关列表 |
| 司法协助 | 响应中 judicial aid 相关列表 |
| 清算 | 响应中 liquidation 相关列表 |
| 简易注销 | `data.companyCancelEasyList` |

先报告每类记录数，再选最多 3 条有明确日期、案号、机关或状态的事实。不要把关联主体记录描述成目标企业自身记录。

## 2. 知识产权、许可和资质

标准版分页工具统一请求第一页、每页 5 条。

| 维度 | 工具 | 总量路径 | 首批记录路径 |
| --- | --- | --- | --- |
| 商标 | `p0010073_query_trademark_info` | `data.brandListMeta.totalCount` | `data.brandList` |
| 专利 | `p0010078_query_patent_info` | `data.patentsListMeta.totalCount` | `data.patentsList` |
| 软件著作权 | `p0010074_query_software_copyright_info` | `data.swListMeta.totalCount` | `data.swList` |
| 作品著作权 | `p0010075_query_work_copyright_info` | `data.resultListMeta.totalCount` | `data.resultList` |
| 许可 | `p0010084_query_license_info` | `data.detailListMeta.totalCount` | `data.detailList` |
| ICP 备案 | `p0010076_query_icp_filing_info` | `data.icpListMeta.totalCount` | `data.icpList` |
| 荣誉资质 | `p0110003_query_honor_qualification_info` | 使用 `data.itemNameList` 长度 | `data.itemNameList` |

`totalCount` 在不同工具中可能为字符串或整数，展示时按数值含义读取，但不修改原始业务值。荣誉资质接口没有分页总量元数据，因此只能说“本次返回 N 项”，不能宣称为全量。

优先展示：

- 知识产权：总量、名称、类型/分类、申请或登记日期、状态；
- 许可：许可名称/类型、证号、发证机关、有效期、状态；
- ICP：网站名称、域名、备案号、审核日期；
- 荣誉资质：`name`, `firstCategory`, `secondCategory`, `level`, `government`, `pubDate`, `status`, `revokeDate`。

## 3. 投资与任职关联

工具：`p0020021_query_single_point_related_info`

| 路径 | 含义 |
| --- | --- |
| `data.basicInfoList` | 主体基础信息 |
| `data.entInvList` | 企业投资关系 |
| `data.frInvAndPos` | 法定代表人投资与任职 |
| `data.manInvAndPos` | 主要人员投资与任职 |
| `data.shaInvAndPos` | 股东投资与任职 |

完整版使用 `relation_direction="1"`。将这些结果称为“公开关联线索”，按关系类型统计并最多展示 5 个代表性主体。不得据此推导最终受益人、实际控制人或隐含控制关系。

## 4. 近期舆情

工具：`p0050007_p0050008_query_public_opinion_info`

| 展示项 | 路径/处理 |
| --- | --- |
| 命中总量 | `list_result.data.infoListMeta.totalCount` |
| 列表 | `list_result.data.infoList` |
| 详情 | 组合工具返回的详情结果，最多 3 条 |
| 时间窗 | 默认执行日期向前 90 个自然日 |

优先提取标题、发布日期、来源、标签/分类、情感标记和摘要。清楚标注“舆情线索”，不要将媒体或网页内容升级为已确认事实。详情缺失时仅基于列表字段摘要。

## 5. 状态判定

每个维度都记录以下状态之一：

| 状态 | 输出措辞 |
| --- | --- |
| 成功且有数据 | 报告总量或关键事实 |
| 成功但空列表 | “本次查询未返回相关公开记录” |
| 字段缺失/空字符串 | “未披露”或省略 |
| 工具失败/不可用 | “该维度查询未完成：原因” |

不要把空列表、零记录、字段缺失和调用失败混为一谈。
