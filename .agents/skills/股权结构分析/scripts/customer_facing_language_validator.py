#!/usr/bin/env python3
"""Reject machine-facing execution language in a customer-visible equity report."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Pattern, Sequence


class CustomerFacingLanguageError(ValueError):
    """Raised when customer-visible text leaks internal execution language."""


@dataclass(frozen=True)
class ForbiddenPattern:
    label: str
    pattern: Pattern[str]


FORBIDDEN_PATTERNS: Sequence[ForbiddenPattern] = (
    ForbiddenPattern("产品过程表述", re.compile(r"产品\s*(?:识别|返回|结论|聚合)")),
    ForbiddenPattern("返回术语", re.compile(r"返回")),
    ForbiddenPattern("本次执行表述", re.compile(r"本次\s*(?:返回|未返回|未完成|未识别|未取得|路径|穿透)")),
    ForbiddenPattern("接口过程表述", re.compile(r"接口\s*(?:显示|返回|原值)")),
    ForbiddenPattern("查询失败状态", re.compile(r"查询\s*失败")),
    ForbiddenPattern("不可用状态", re.compile(r"当前\s*不可用")),
    ForbiddenPattern("命中术语", re.compile(r"(?:0|零)\s*命中")),
    ForbiddenPattern("聚合值术语", re.compile(r"聚合\s*值")),
    ForbiddenPattern("数据断点术语", re.compile(r"数据\s*断点")),
    ForbiddenPattern("路径互证术语", re.compile(r"路径\s*互证")),
    ForbiddenPattern("模型或系统判断", re.compile(r"(?:模型|系统)\s*(?:识别|判定|显示)")),
    ForbiddenPattern("状态码", re.compile(r"状态\s*码")),
    ForbiddenPattern("产品码", re.compile(r"P\d{7}")),
)


def find_machine_facing_language(text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for item in FORBIDDEN_PATTERNS:
        for match in item.pattern.finditer(text):
            findings.append({"label": item.label, "text": match.group(0)})
    return findings


def validate_customer_facing_report(text: str) -> dict[str, int]:
    findings = find_machine_facing_language(text)
    if findings:
        raise CustomerFacingLanguageError(f"客户报告包含内部执行语言：{findings}")
    return {"characters": len(text), "forbidden_findings": 0}
