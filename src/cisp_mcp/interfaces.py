from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CispInterface:
    product_code: str
    name: str
    description: str
    status_field: str
    data_field: str
    shortcut_field: str | None = None


INTERFACES = {
    "P0010010": CispInterface(
        product_code="P0010010",
        name="企业工商照面信息查询",
        description="根据企业名称、工商注册号或统一社会信用代码查询企业工商注册照面信息及历史名称信息。",
        status_field="P0010010Status",
        data_field="P0010010Data",
        shortcut_field="basicList",
    ),
    "P0010058": CispInterface(
        product_code="P0010058",
        name="企业工商基本信息查询（深度）",
        description="根据企业名称、工商注册号、统一社会信用代码或组织机构代码查询企业深度工商信息。",
        status_field="P0010058Status",
        data_field="P0010058Data",
        shortcut_field="basicList",
    ),
    "P0010059": CispInterface(
        product_code="P0010059",
        name="企业工商基本信息查询（简项）",
        description="根据企业名称、工商注册号、统一社会信用代码或组织机构代码查询指定类型的企业工商信息。",
        status_field="P0010059Status",
        data_field="P0010059Data",
        shortcut_field="basicList",
    ),
    "P0010068": CispInterface(
        product_code="P0010068",
        name="企业名称模糊查询（简版）",
        description="根据企业名称关键字查询最符合条件的企业名称。",
        status_field="P0010068Status",
        data_field="P0010068Data",
        shortcut_field="fuzzyList",
    ),
    "P0010073": CispInterface(
        product_code="P0010073",
        name="企业商标信息查询",
        description="通过企业名称或企业证件号查询商标信息。",
        status_field="P0010073Status",
        data_field="P0010073Data",
        shortcut_field="brandList",
    ),
    "P0010074": CispInterface(
        product_code="P0010074",
        name="企业软件著作权信息查询",
        description="根据企业名称、统一社会信用代码或注册号查询企业软件著作权信息。",
        status_field="P0010074Status",
        data_field="P0010074Data",
        shortcut_field="swList",
    ),
    "P0010075": CispInterface(
        product_code="P0010075",
        name="企业作品著作权信息查询",
        description="根据企业名称、工商注册号或统一社会信用代码查询企业作品著作权信息。",
        status_field="P0010075Status",
        data_field="P0010075Data",
        shortcut_field="resultList",
    ),
    "P0010076": CispInterface(
        product_code="P0010076",
        name="企业ICP备案信息查询",
        description="根据企业名称、工商注册号或统一社会信用代码查询企业 ICP 备案信息。",
        status_field="P0010076Status",
        data_field="P0010076Data",
        shortcut_field="icpList",
    ),
    "P0010078": CispInterface(
        product_code="P0010078",
        name="企业专利信息查询",
        description="根据企业名称查询以企业作为专利申请人的专利信息。",
        status_field="P0010078Status",
        data_field="P0010078Data",
        shortcut_field="patentsList",
    ),
    "P0010084": CispInterface(
        product_code="P0010084",
        name="企业许可信息查询",
        description="根据企业名称、统一社会信用代码或注册号查询工商、食药监、质检、金融监管、环保、医疗等企业许可信息。",
        status_field="P0010084Status",
        data_field="P0010084Data",
        shortcut_field="detailList",
    ),
    "P0020021": CispInterface(
        product_code="P0020021",
        name="企业单点关联信息查询",
        description="根据企业名称、注册号、组织机构代码或统一社会信用代码查询企业投资和任职关联信息。",
        status_field="P0020021Status",
        data_field="P0020021Data",
        shortcut_field="entInvList",
    ),
    "P0050007": CispInterface(
        product_code="P0050007",
        name="企业舆情信息列表查询",
        description="根据企业名称、三级标签、情感方向等条件查询企业舆情列表信息。",
        status_field="P0050007Status",
        data_field="P0050007Data",
        shortcut_field="infoList",
    ),
    "P0050008": CispInterface(
        product_code="P0050008",
        name="企业舆情信息详情查询",
        description="根据企业名称或舆情 ID 查询企业舆情详情信息。",
        status_field="P0050008Status",
        data_field="P0050008Data",
        shortcut_field="infoDetail",
    ),
    "P0060007": CispInterface(
        product_code="P0060007",
        name="企业工商二要素验证",
        description="根据企业名称和工商注册号/统一社会信用代码验证信息是否匹配。",
        status_field="P0060007Status",
        data_field="P0060007Data",
        shortcut_field="matchList",
    ),
    "P0060008": CispInterface(
        product_code="P0060008",
        name="企业工商三要素验证",
        description="根据企业名称、企业法人和社会统一信用代码验证是否一致。",
        status_field="P0060008Status",
        data_field="P0060008Data",
        shortcut_field="matchList",
    ),
    "P0110003": CispInterface(
        product_code="P0110003",
        name="企业荣誉资质信息查询",
        description="根据企业名称、注册号、统一社会信用代码或企业 ID 查询企业荣誉、奖励和认定信息。",
        status_field="P0110003Status",
        data_field="P0110003Data",
        shortcut_field="itemNameList",
    ),
    "P0130036": CispInterface(
        product_code="P0130036",
        name="企业土地信息查询",
        description="根据企业名称、统一社会信用代码或注册号查询土地供应、土地出让、地块公示和土地抵押信息。",
        status_field="P0130036Status",
        data_field="P0130036Data",
        shortcut_field="detailList",
    ),
    "P0130038": CispInterface(
        product_code="P0130038",
        name="企业画像-行业分析",
        description="根据企业、行业和地区条件查询企业排名、行业财务指标、综合经营指标和知识产权排名等行业分析信息。",
        status_field="P0130038Status",
        data_field="P0130038Data",
    ),
    "P0210004": CispInterface(
        product_code="P0210004",
        name="上市公司财务数据查询",
        description="根据企业名称、统一社会信用代码或注册号查询上市企业的利润、现金流量、资产负债和主要财务指标。",
        status_field="P0210004Status",
        data_field="P0210004Data",
    ),
    "P0980006": CispInterface(
        product_code="P0980006",
        name="企业高级筛选",
        description="通过多维度筛选条件查询符合条件的企业列表。",
        status_field="P0980006Status",
        data_field="P0980006Data",
        shortcut_field="entList",
    ),
    "P0980008": CispInterface(
        product_code="P0980008",
        name="纳税评级",
        description="根据企业内部 eid 查询企业纳税评级。",
        status_field="P0980008Status",
        data_field="P0980008Data",
        shortcut_field="list",
    ),
    "P0980023": CispInterface(
        product_code="P0980023",
        name="光大-近2年风险分析统计",
        description="根据企业内部 eid 查询企业近两年风险分析统计。",
        status_field="P0980023Status",
        data_field="P0980023Data",
        shortcut_field="list",
    ),
    "P0980033": CispInterface(
        product_code="P0980033",
        name="上市投融资招投标知识产权情况",
        description="根据企业名称、工商注册号或统一社会信用代码查询上市、投融资、招投标和知识产权情况。",
        status_field="P0980033Status",
        data_field="P0980033Data",
        shortcut_field="data",
    ),
    "P0990022": CispInterface(
        product_code="P0990022",
        name="供应商关联关系",
        description="根据企业名称、工商注册号、组织机构代码或统一社会信用代码查询供应商关联关系。",
        status_field="P0990022Status",
        data_field="P0990022Data",
        shortcut_field="suppList",
    ),
}


P0010010 = INTERFACES["P0010010"]
P0010058 = INTERFACES["P0010058"]
P0010059 = INTERFACES["P0010059"]
P0010068 = INTERFACES["P0010068"]
P0010073 = INTERFACES["P0010073"]
P0010074 = INTERFACES["P0010074"]
P0010075 = INTERFACES["P0010075"]
P0010076 = INTERFACES["P0010076"]
P0010078 = INTERFACES["P0010078"]
P0010084 = INTERFACES["P0010084"]
P0020021 = INTERFACES["P0020021"]
P0050007 = INTERFACES["P0050007"]
P0050008 = INTERFACES["P0050008"]
P0060007 = INTERFACES["P0060007"]
P0060008 = INTERFACES["P0060008"]
P0110003 = INTERFACES["P0110003"]
P0130036 = INTERFACES["P0130036"]
P0130038 = INTERFACES["P0130038"]
P0210004 = INTERFACES["P0210004"]
P0980006 = INTERFACES["P0980006"]
P0980008 = INTERFACES["P0980008"]
P0980023 = INTERFACES["P0980023"]
P0980033 = INTERFACES["P0980033"]
P0990022 = INTERFACES["P0990022"]


RESULT_CODE_DESCRIPTIONS = {
    "00000": "查询成功",
}


PRODUCT_STATUS_DESCRIPTIONS = {
    "4": "查询成功有结果",
    "1": "查询成功无结果",
    "3": "查询失败",
}


ERROR_CODE_DESCRIPTIONS = {
    "E0001": "系统异常",
    "E0102": "预检查不通过",
    "E0110": "产品码不存在",
    "E0111": "交易渠道非法",
    "E0112": "未获得产品使用权限",
    "E0400": "查询征信数据出错",
    "E0401": "超出试用期间数量",
    "E0407": "处理征信数据出错",
    "E0408": "未查询到数据",
    "E0504": "超出查询笔数限制",
    "E1000": "查询参数校验不通过",
    "E1003": "请提供查询条件",
    "E1004": "查询产品编号错误",
    "E1005": "版本号错误",
    "E1006": "MSGID错误",
    "E1007": "交易时间错误",
    "E1008": "签名时间错误",
    "E1009": "accessKeyId错误",
    "E1010": "signature错误",
    "E1012": "机构代码错误",
    "E1013": "IP错误",
    "E1014": "timestamp过期",
    "E1015": "queryMode错误",
    "E1016": "订单不存在",
    "E1017": "订单失败",
    "E1018": "订单处理中",
    "E1019": "订单等待中",
    "E1020": "Packet数量超出",
    "E1021": "操作渠道非法",
    "E1022": "该查询条件重复查询不存在",
    "E1023": "重复查询日期超出可查询范围",
    "E1024": "历史查询日期超出可查询范围",
    "E1025": "个人风控报告申请身份验证不通过",
    "E1026": "查询并发超出限制",
    "E1027": "机构授权码无效",
}


def describe_result_code(result_code: object) -> str | None:
    if result_code is None:
        return None
    code = str(result_code)
    return RESULT_CODE_DESCRIPTIONS.get(code) or ERROR_CODE_DESCRIPTIONS.get(code)


def describe_product_status(status: object) -> str | None:
    if status is None:
        return None
    return PRODUCT_STATUS_DESCRIPTIONS.get(str(status))
