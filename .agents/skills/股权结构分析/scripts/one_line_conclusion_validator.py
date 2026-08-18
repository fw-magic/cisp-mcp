#!/usr/bin/env python3
"""Validate the evidence boundaries of an equity-report one-line conclusion."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence


class ConclusionValidationError(ValueError):
    """Raised when a conclusion violates the evidence-compression contract."""


@dataclass(frozen=True)
class ConclusionEvidence:
    required_literals: Sequence[str] = ()
    forbidden_literals: Sequence[str] = ()
    sparse: bool = False
    shareholder_list_complete: bool = False
    ratios_consistent: bool = False
    control_path_complete: bool = False
    controller_cross_verified: bool = False
    snapshot_cross_checked: bool = False
    rights_scope_complete: bool = False
    history_event_correlated: bool = False
    governance_optimization_verified: bool = False


def validate_one_line_conclusion(
    conclusion: str, evidence: ConclusionEvidence
) -> dict[str, int]:
    """Return basic metrics or raise when wording exceeds supplied evidence."""
    text = conclusion.strip()
    if not text:
        raise ConclusionValidationError("一句话结论不能为空")
    if "\n" in text or "\r" in text:
        raise ConclusionValidationError("一句话结论必须是一个连续段落")
    if text.count("一句话结论") != 1:
        raise ConclusionValidationError("一句话结论标签必须且只能出现一次")

    body = text.split("一句话结论", 1)[1].lstrip("：: ")
    machine_patterns = (
        r"产品\s*(?:识别|返回|结论|聚合)",
        r"返回",
        r"本次\s*(?:返回|未返回|未完成|未识别|未取得|路径|穿透)",
        r"(?:0|零)\s*命中",
        r"聚合\s*值",
        r"数据\s*断点",
        r"路径\s*互证",
        r"当前\s*不可用",
        r"(?:模型|系统)\s*(?:识别|判定|显示)",
    )
    leaked_machine_language = [
        pattern for pattern in machine_patterns if re.search(pattern, body)
    ]
    if leaked_machine_language:
        raise ConclusionValidationError(
            f"一句话结论包含客户不可见的内部表达：{leaked_machine_language}"
        )
    clauses = [item.strip() for item in body.rstrip("。； ").split("；") if item.strip()]
    minimum, maximum = (3, 4) if evidence.sparse else (5, 7)
    if not minimum <= len(clauses) <= maximum:
        raise ConclusionValidationError(
            f"当前证据模式要求 {minimum} 至 {maximum} 个分句，实际为 {len(clauses)}"
        )
    if not evidence.sparse and not 220 <= len(body) <= 350:
        raise ConclusionValidationError(
            f"证据充分模式正文建议并强制为 220 至 350 字符，实际为 {len(body)}"
        )

    missing = [value for value in evidence.required_literals if value not in body]
    if missing:
        raise ConclusionValidationError(f"缺少必须逐字保留的证据值：{missing}")
    leaked = [value for value in evidence.forbidden_literals if value in body]
    if leaked:
        raise ConclusionValidationError(f"包含未取得或禁止出现的事实：{leaked}")

    strong_clear = "股权结构清晰透明" in body
    if strong_clear and not (
        evidence.shareholder_list_complete
        and evidence.ratios_consistent
        and evidence.control_path_complete
    ):
        raise ConclusionValidationError("“股权结构清晰透明”的证据门槛未满足")
    control_wording = body.replace("未锁定", "")
    if "锁定" in control_wording and not evidence.controller_cross_verified:
        raise ConclusionValidationError("“锁定”需要产品结论与独立路径互证")
    if any(value in body for value in ("完全一致", "100%一致", "100% 一致")) and not evidence.snapshot_cross_checked:
        raise ConclusionValidationError("一致性强结论需要完成同口径逐项核对")
    if "未发现" in body and not evidence.rights_scope_complete:
        raise ConclusionValidationError("权利受限“未发现”结论需要查询成功且覆盖范围明确")
    if any(value in body for value in ("历史变更有序推进", "与融资节奏一致")) and not evidence.history_event_correlated:
        raise ConclusionValidationError("历史节奏判断缺少事件时间对应证据")
    if "治理优化" in body and not evidence.governance_optimization_verified:
        raise ConclusionValidationError("“治理优化”缺少治理效果互证")
    if any(
        value in body
        for value in ("符合IPO申报条件", "符合 IPO 申报条件", "具备IPO申报资格", "具备 IPO 申报资格")
    ):
        raise ConclusionValidationError("不得输出 IPO 资格或申报条件结论")

    return {"characters": len(body), "clauses": len(clauses)}
