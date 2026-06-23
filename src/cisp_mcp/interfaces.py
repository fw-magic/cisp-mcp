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
}


P0010010 = INTERFACES["P0010010"]
P0010058 = INTERFACES["P0010058"]
P0010068 = INTERFACES["P0010068"]
P0010073 = INTERFACES["P0010073"]
P0010074 = INTERFACES["P0010074"]
P0010075 = INTERFACES["P0010075"]
P0010076 = INTERFACES["P0010076"]
P0010078 = INTERFACES["P0010078"]
P0050007 = INTERFACES["P0050007"]
P0050008 = INTERFACES["P0050008"]
P0060007 = INTERFACES["P0060007"]
P0060008 = INTERFACES["P0060008"]


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
