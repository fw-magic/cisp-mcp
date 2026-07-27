from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


COMMON_DESCRIPTIONS = {
    "$": "本次 MCP 工具返回对象。",
    "product_code": "CISP 产品码；组合工具使用两个产品码的组合值。",
    "interface_name": "接口中文名称。",
    "success": "调用是否成功。专用工具表示 resultCode 是否为 00000；组合工具还要求已请求的详情均成功。",
    "has_result": "产品状态是否为“查询成功有结果”，即产品状态码为 4。",
    "result_code": "CISP 网关结果码。",
    "result_code_desc": "网关结果码的中文解释。",
    "result_desc": "CISP 网关原始结果说明。",
    "product_status": "产品状态码：4=查询成功有结果，1=查询成功无结果，3=查询失败。",
    "product_status_desc": "产品状态码的中文解释。",
    "order_no": "CISP 查询订单号。",
    "packet_count": "返回数据包数量，对应原始字段 packetCnt。",
    "is_compressed": "压缩标志，对应原始字段 isCompressed；0 通常表示未压缩。",
    "data": "从 raw_response.resultData 中提取的当前产品数据对象。",
    "raw_response": "CISP 网关未经归一化的完整原始响应。",
    "list_success": "组合舆情工具中，列表接口 P0050007 是否调用成功。",
    "list_has_result": "组合舆情工具中，列表接口 P0050007 是否返回结果。",
    "list_result": "组合舆情工具中，P0050007 的完整归一化结果。",
    "detail_count": "组合舆情工具实际请求并返回的详情条数。",
    "details": "组合舆情工具的详情结果列表。",
    "entry_id": "舆情条目 ID，用于关联列表记录和详情记录。",
    "list_item": "触发当前详情查询的原始舆情列表项。",
    "detail": "P0050008 舆情详情接口的完整归一化结果。",
}

GENERIC_DESCRIPTIONS = {
    "orderNo": "CISP 查询订单号。",
    "resultData": "CISP 网关的产品结果容器。",
    "packetCnt": "返回数据包数量。",
    "resultCode": "CISP 网关结果码。",
    "resultDesc": "CISP 网关结果说明。",
    "isCompressed": "压缩标志；0 通常表示未压缩。",
    "actualNo": "当前页实际返回条数。",
    "pageNo": "当前页码。",
    "totalPage": "总页数。",
    "range": "每页条数。",
    "totalCount": "符合条件的总记录数。",
    "no": "序号。",
    "entName": "企业名称。",
    "entId": "内部企业 ID。",
    "creditCode": "统一社会信用代码。",
    "regNo": "工商注册号。",
    "orgName": "企业或机构名称。",
    "legRepName": "法定代表人姓名。",
    "pubDate": "发布日期或公告日期。",
    "status": "当前状态。",
    "type": "记录类型。",
    "url": "原文或详情网页地址。",
    "name": "名称。",
}

INFERRED_BY_PRODUCT = {
    "P0010084": {
        "detailList": "企业许可明细列表。",
        "licAuth": "许可机关。",
        "licCode": "许可编码。",
        "licName": "许可证或许可事项名称。",
        "licNo": "许可证号或行政许可决定文书编号。",
        "licStateName": "许可状态名称。",
        "licType": "许可类型。",
        "licVontent": "许可内容；原始字段名疑似将 licContent 拼写为 licVontent。",
        "vDate": "许可决定、批准或发证日期。",
        "valForm": "有效期自；原始字段名疑似将 valFrom 拼写为 valForm。",
        "valTo": "有效期至。",
        "wName": "许可文书名称。",
        "wNo": "许可文书编号。",
    },
    "P0020021": {
        "manInvAndPos": "主要人员的投资及任职关系列表。",
        "basicInfoList": "关联企业基本信息列表。",
        "shaInvAndPos": "股东的投资及任职关系列表。",
        "entInvList": "目标企业对外投资列表。",
        "frInvAndPos": "法定代表人的投资及任职关系列表。",
        "name": "关联主体名称（人员或股东）。",
        "manId": "主要人员内部 ID。",
        "shaId": "股东内部 ID。",
        "frId": "法定代表人内部 ID。",
        "entList": "该关联主体关联的企业列表。",
        "position": "任职职位。",
        "type": "关联主体类型；样例中 P.个人、E.企业。",
        "estDate": "企业成立日期。",
        "entStatus": "企业经营状态。",
        "invType": "投资人或股东类型。",
        "shaRatio": "股东持股比例。",
        "relationType": "关系类型，如投资或任职。",
        "subConDate": "认缴出资日期。",
        "subConCurCode": "认缴出资币种代码。",
        "subConCurName": "认缴出资币种名称。",
        "subConAmt": "认缴出资金额。",
        "fundedRatio": "出资比例。",
        "relatedOrgName": "关联机构名称。",
    },
    "P0050007": {
        "infoList": "企业舆情列表。",
        "infoListMeta": "舆情列表分页信息。",
        "relId": "舆情关联 ID；本次样例与 entryId 相同。",
        "groupName": "信息来源大类，如网页。",
        "pubTime": "舆情发布时间。",
        "channel": "信息渠道。",
        "siteName": "来源站点名称。",
        "abstract": "舆情摘要。",
        "infoLabelList": "舆情标签列表。",
        "infoCategory1": "一级舆情分类代码。",
        "infoCategory2": "二级舆情分类代码。",
        "infoCategory3": "三级舆情分类代码。",
        "entityType": "命中实体类型，如主体。",
        "infoEmotion": "情感倾向，如正面、中性、负面。",
        "title": "舆情标题。",
        "entryId": "舆情条目 ID。",
    },
    "P0050008": {
        "infoDetail": "企业舆情详情列表。",
        "groupName": "信息来源大类，如网页。",
        "urlContent": "网页正文或网页内容补充字段。",
        "groupDepartmentName": "企业所属集团或部门名称。",
        "pubTime": "舆情发布时间。",
        "channel": "信息渠道。",
        "siteName": "来源站点名称。",
        "infoList": "舆情分类及命中信息列表。",
        "infoCategory1": "一级舆情分类代码。",
        "infoCategory2": "二级舆情分类代码。",
        "infoCategory3": "三级舆情分类代码。",
        "infoCategory1Name": "一级舆情分类名称。",
        "infoCategory2Name": "二级舆情分类名称。",
        "infoLine": "命中信息所在行或位置。",
        "infoRange": "命中内容在正文中的字符范围。",
        "infoTypeKey": "信息类型关键字。",
        "entityType": "命中实体类型，如主体。",
        "source": "标签或命中信息来源。",
        "entNameKey": "企业名称命中关键字。",
        "infoEmotion": "情感倾向，如正面、中性、负面。",
        "title": "舆情标题。",
        "content": "舆情正文。",
        "entryId": "舆情条目 ID。",
    },
    "P0110003": {
        "itemNameList": "企业荣誉、奖励和资质认定列表。",
        "secondCategory": "二级荣誉或资质类别。",
        "year": "所属年度。",
        "declareType": "申报类型。",
        "level": "荣誉或资质级别。",
        "batch": "批次。",
        "firstCategory": "一级荣誉或资质类别。",
        "sort": "数据排序值。",
        "revokeDate": "撤销日期。",
        "rewardCategory": "奖励类别。",
        "government": "授予或发布政府部门。",
        "name": "荣誉、奖励或资质名称。",
        "rewardAmount": "奖励金额。",
        "projectName": "关联项目名称。",
    },
}

EXTRA_INFERRED = {
    "udate": "更新日期；接口 PDF 字段表写作 update，实际返回为 udate。",
    "womenNum": "女性从业人数。",
    "accIsPublic": "本期实际缴费金额是否公示。",
    "amIsPublic": "单位累计欠缴金额是否公示。",
    "baseIsPublic": "单位缴费基数是否公示。",
    "isPublic": "该组年报社会保险信息是否公示。",
    "pctInterPub": "PCT 国际公布信息；接口 PDF 字段表写作 pcttInterPub，实际返回为 pctInterPub。",
    "infoListMeta": "列表分页信息。",
    "brandListMeta": "商标列表分页信息。",
    "swListMeta": "软件著作权列表分页信息。",
    "resultListMeta": "作品著作权列表分页信息。",
    "icpListMeta": "ICP备案列表分页信息。",
    "patentsListMeta": "专利列表分页信息。",
    "detailListMeta": "许可明细列表分页信息。",
    "matchList": "要素匹配结果列表。",
    "orgNameMatch": "企业名称是否匹配；1 表示匹配。",
    "regNoMatch": "统一社会信用代码或注册号是否匹配；1 表示匹配。",
    "frNameMatch": "法定代表人姓名是否匹配；1 表示匹配。",
}


def leaf_name(path: str) -> str:
    part = path.rsplit(".", 1)[-1]
    return part[:-2] if part.endswith("[]") else part


def product_parts(product_code: str) -> list[str]:
    return re.findall(r"P\d{7}", product_code)


def official_lookup(
    official: dict[str, Any],
    product_code: str,
    path: str,
) -> tuple[str, str] | None:
    field = leaf_name(path)
    path_parts = {
        part[:-2] if part.endswith("[]") else part
        for part in path.split(".")
    }
    for product in product_parts(product_code):
        source = official.get(product)
        if not source:
            continue
        entries = [item for item in source["fields"] if item["field"] == field]
        contextual = [
            item
            for item in entries
            if item.get("context") and item["context"] in path_parts
        ]
        if contextual:
            entries = contextual
        described = [item for item in entries if item["description"]]
        chosen = described[0] if described else (entries[0] if entries else None)
        if not chosen:
            continue
        description = chosen["description"]
        if not description:
            if chosen["type"] == "object[]":
                description = f"{field} 列表。"
            elif chosen["type"] == "object":
                description = f"{field} 对象。"
            else:
                description = f"{field} 字段。"
        source_text = (
            f"官方PDF：{source['source_filename']} 第 {chosen['page']} 页"
        )
        return description, source_text
    return None


def infer_description(
    path: str,
    product_code: str,
    official: dict[str, Any],
) -> tuple[str, str]:
    field = leaf_name(path)

    if path == "$":
        return COMMON_DESCRIPTIONS["$"], "MCP 返回结构"

    if "." not in path and field in COMMON_DESCRIPTIONS:
        return COMMON_DESCRIPTIONS[field], "MCP 归一化层"

    if field in {"data", "raw_response"}:
        return COMMON_DESCRIPTIONS[field], "MCP 归一化层"

    if re.fullmatch(r"P\d{7}Status", field):
        return "该产品的状态码：4=有结果，1=无结果，3=失败。", "CISP 通用状态定义"
    if re.fullmatch(r"P\d{7}Data", field):
        return "该产品在 CISP 原始响应中的数据对象。", "CISP 原始返回结构"

    common_wrapper = COMMON_DESCRIPTIONS.get(field)
    if common_wrapper and (
        "details[]" in path
        or path.startswith("list_")
        or path.startswith("list_result")
    ):
        return common_wrapper, "组合工具结构"

    for product in product_parts(product_code):
        inferred = INFERRED_BY_PRODUCT.get(product, {}).get(field)
        if inferred:
            return inferred, "实际返回样例与字段命名推断"

    official_match = official_lookup(official, product_code, path)
    if official_match:
        return official_match

    if field in EXTRA_INFERRED:
        return EXTRA_INFERRED[field], "接口样例与字段命名推断"
    if field in GENERIC_DESCRIPTIONS:
        return GENERIC_DESCRIPTIONS[field], "字段命名与实际样例"
    if field.endswith("Meta"):
        return f"{field[:-4]} 的分页或统计信息。", "字段命名推断"
    if field.endswith("List"):
        return f"{field} 返回记录列表。", "字段命名推断"
    if field.endswith("Status"):
        return f"{field} 状态字段。", "字段命名推断"

    return (
        f"`{field}` 返回字段；当前资料未给出明确中文口径，需以该产品最新官方字段文档为准。",
        "待官方文档确认",
    )


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def sample_text(samples: list[Any]) -> str:
    if not samples:
        return ""
    value = json.dumps(samples[0], ensure_ascii=False)
    if len(value) > 100:
        value = value[:97] + "..."
    return value


def canonical_paths(
    tool_name: str,
    result: dict[str, Any],
    fields: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    shortcut_names = {
        key
        for key in (
            "basicList",
            "fuzzyList",
            "brandList",
            "swList",
            "resultList",
            "icpList",
            "patentsList",
            "detailList",
            "entInvList",
            "infoList",
            "infoDetail",
            "matchList",
            "itemNameList",
        )
        if key in result
    }
    selected = []
    for field in fields:
        path = field["path"]
        if path == "$":
            selected.append(field)
            continue
        if path == "raw_response" or path.startswith("raw_response."):
            continue
        if ".raw_response" in path:
            continue
        if any(path == name or path.startswith(f"{name}.") or path.startswith(f"{name}[]") for name in shortcut_names):
            if tool_name != "p0050007_p0050008_query_public_opinion_info":
                continue
        selected.append(field)
    return selected


def write_docs(root: Path) -> None:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    observed = json.loads((root / "observed_fields.json").read_text(encoding="utf-8"))
    official = json.loads(
        (root / "reference" / "official_pdf_fields.json").read_text(encoding="utf-8")
    )
    tool_schemas = {
        item["name"]: item
        for item in json.loads((root / "tool_schemas.json").read_text(encoding="utf-8"))
    }
    raw_records = {}
    for call in manifest["calls"]:
        record = json.loads((root / call["raw_file"]).read_text(encoding="utf-8"))
        raw_records[call["tool_name"]] = record

    fields_dir = root / "fields"
    fields_dir.mkdir(parents=True, exist_ok=True)

    csv_path = root / "field_catalog.csv"
    fallback_count = 0
    total_rows = 0
    with csv_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "sequence",
                "tool_name",
                "product_code",
                "path",
                "types",
                "meaning",
                "meaning_source",
                "sample",
                "observations",
            ],
        )
        writer.writeheader()
        for call in manifest["calls"]:
            tool_name = call["tool_name"]
            result = raw_records[tool_name]["result"]
            product_code = str(result.get("product_code", ""))
            for field in observed[tool_name]:
                meaning, source = infer_description(
                    field["path"], product_code, official
                )
                if source == "待官方文档确认":
                    fallback_count += 1
                total_rows += 1
                writer.writerow(
                    {
                        "sequence": call["sequence"],
                        "tool_name": tool_name,
                        "product_code": product_code,
                        "path": field["path"],
                        "types": "|".join(field["types"]),
                        "meaning": meaning,
                        "meaning_source": source,
                        "sample": sample_text(field["samples"]),
                        "observations": field["observations"],
                    }
                )

    readme_rows = []
    for call in manifest["calls"]:
        tool_name = call["tool_name"]
        record = raw_records[tool_name]
        result = record["result"]
        product_code = str(result.get("product_code", ""))
        fields = observed[tool_name]
        canonical = canonical_paths(tool_name, result, fields)
        schema = tool_schemas[tool_name]

        field_lines = [
            f"# {tool_name}",
            "",
            f"- 产品码：`{product_code or '通用/组合'}`",
            f"- 工具说明：{schema.get('description') or ''}",
            f"- 实际入参：`{markdown_escape(json.dumps(record['arguments'], ensure_ascii=False))}`",
            f"- 调用结果：`is_error={str(record['is_error']).lower()}`，"
            f"`success={result.get('success')}`，"
            f"`has_result={result.get('has_result', result.get('list_has_result'))}`",
            f"- 完整原始记录：[`../{call['raw_file']}`](../{call['raw_file']})",
            "",
            "下表是去除 `raw_response` 镜像和顶层快捷字段重复项后的可读字段表。"
            "所有原始路径仍完整保存在 `../field_catalog.csv` 与 `../observed_fields.json`。",
            "",
            "| 字段路径 | 类型 | 字段含义 | 含义来源 | 样例 |",
            "| --- | --- | --- | --- | --- |",
        ]
        for field in canonical:
            meaning, source = infer_description(field["path"], product_code, official)
            field_lines.append(
                "| `{}` | `{}` | {} | {} | `{}` |".format(
                    markdown_escape(field["path"]),
                    markdown_escape(" / ".join(field["types"])),
                    markdown_escape(meaning),
                    markdown_escape(source),
                    markdown_escape(sample_text(field["samples"])),
                )
            )

        fields_filename = f"{call['sequence']:02d}_{tool_name}.md"
        (fields_dir / fields_filename).write_text(
            "\n".join(field_lines) + "\n",
            encoding="utf-8",
        )

        arguments = record["arguments"]
        company = (
            arguments.get("ent_info")
            or arguments.get("ent_name")
            or arguments.get("prod_code")
            or "-"
        )
        if isinstance(company, list):
            company = "、".join(company)
        has_result = result.get("has_result", result.get("list_has_result"))
        readme_rows.append(
            "| {} | `{}` | `{}` | {} | {} | {} | {} | [字段文档](fields/{}) | [{}]({}) |".format(
                call["sequence"],
                tool_name,
                product_code,
                markdown_escape(str(company)),
                result.get("success"),
                has_result,
                len(fields),
                fields_filename,
                call["raw_file"].split("/")[-1],
                call["raw_file"],
            )
        )

    readme = [
        "# cisp-mcp 全工具返回字段实测",
        "",
        f"- MCP 服务配置名：`{manifest['mcp_server_name']}`",
        f"- 实际发现并调用：`{manifest['called_tool_count']}/{manifest['registered_tool_count']}` 个工具",
        f"- 是否覆盖全部已注册工具：`{manifest['all_registered_tools_called']}`",
        f"- 调用开始（UTC）：`{manifest['started_at']}`",
        f"- 调用结束（UTC）：`{manifest['finished_at']}`",
        f"- 完整字段路径数（按工具累计，含镜像路径）：`{total_rows}`",
        f"- 未给出含义、需待官方确认的字段路径数：`{fallback_count}`",
        *(
            ["- 补充调用说明：" + "；".join(manifest["notes"])]
            if manifest.get("notes")
            else []
        ),
        "",
        "## 文件说明",
        "",
        "- `manifest.json`：17 个工具的调用入参、结果状态、原始文件位置与字段数。",
        "- `tool_schemas.json`：通过 MCP `tools/list` 实际发现的全部工具定义。",
        "- `raw/*.json`：每个工具的完整调用记录和真实返回数据。",
        "- `observed_fields.json`：从真实返回递归提取的全部 JSON 路径、类型、样例与出现次数。",
        "- `field_catalog.csv`：全部字段路径及中文含义，UTF-8 BOM，可直接用 Excel 打开。",
        "- `fields/*.md`：每个工具的可读字段文档；去除了原始响应镜像和快捷字段重复项。",
        "- `reference/official_pdf_fields.json`：从仓库 Git 历史中的 10 份官方接口 PDF 提取的字段表。",
        "",
        "## 路径与重复字段约定",
        "",
        "- `data.*` 是 MCP 归一化后的产品数据。",
        "- `raw_response.resultData.<产品码>Data.*` 是 CISP 原始响应中的同一份产品数据，因此字段会重复。",
        "- 顶层 `basicList`、`brandList`、`infoList` 等是 MCP 为常用列表提供的快捷字段，也与 `data` 中对应列表重复。",
        "- `field_catalog.csv` 和 `observed_fields.json` 保留所有实际返回路径；每工具 Markdown 只展示去重后的可读路径。",
        "- 空数组只能确认数组字段本身，无法凭本次返回观察其子字段；有数据的列表则递归提取所有实际出现的子字段。",
        "",
        "## 字段含义来源",
        "",
        "- P0010010、P0010058、P0010068、P0010073、P0010074、P0010075、P0010076、P0010078、P0060007、P0060008：优先采用仓库历史中的官方接口 PDF。",
        "- P0010084、P0020021、P0050007、P0050008、P0110003：当前仓库没有对应 PDF，含义根据实际返回样例、工具实现与字段命名推断，并在 `meaning_source` 中标注。",
        "- 标记为“待官方文档确认”的字段未强行编造业务口径。",
        "",
        "## 调用结果",
        "",
        "| # | MCP 工具 | 产品码 | 主要企业入参 | success | has_result | 字段路径数 | 字段文档 | 原始返回 |",
        "| --- | --- | --- | --- | --- | --- | ---: | --- | --- |",
        *readme_rows,
        "",
        "## 复现",
        "",
        "在项目根目录运行：",
        "",
        "```bash",
        "uv run python scripts/call_all_mcp_fields.py --output fields_test",
        "uv run python scripts/generate_field_docs.py --output fields_test",
        "```",
        "",
        "首次脚本会真实调用全部 CISP MCP 工具并可能消耗接口次数；它不会自动重试。",
    ]
    (root / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print(
        f"Generated {len(manifest['calls'])} tool docs, {total_rows} catalog rows, "
        f"{fallback_count} paths awaiting official descriptions."
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate readable field documentation from captured MCP results."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("fields_test"),
        help="Capture directory (default: fields_test)",
    )
    args = parser.parse_args()
    write_docs(args.output.resolve())


if __name__ == "__main__":
    main()
