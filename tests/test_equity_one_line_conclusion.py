from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents" / "skills" / "股权结构分析"
SKILL_PATH = SKILL_DIR / "SKILL.md"
STYLE_PATH = SKILL_DIR / "references" / "one-line-conclusion-style.md"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "one_line_conclusion_validator.py"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "equity_one_line_conclusion_validator_test", VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class EquityOneLineConclusionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_skill_links_complete_reference_and_keeps_scope_narrow(self) -> None:
        skill = SKILL_PATH.read_text(encoding="utf-8")
        style = STYLE_PATH.read_text(encoding="utf-8")
        self.assertIn("references/one-line-conclusion-style.md", skill)
        self.assertIn("必须完整读取并执行", skill)
        self.assertIn("不改变报告篇章、表格、工具链、比例原值纪律或 PDF 样式", skill)
        for expected in (
            "证据充足",
            "部分路径或披露快照缺失",
            "未识别实际控制人或股权较分散",
            "股权结构清晰透明",
            "100%一致",
            "客户报告不得使用“0 命中”",
            "具备 IPO 申报资格",
        ):
            self.assertIn(expected, style)

    def test_evidence_rich_conclusion_keeps_raw_literals(self) -> None:
        text = (
            "一句话结论：目标企业股权结构清晰透明，直接股东资料完整且控制路径不存在重大缺口；"
            "股权与控制关系资料锁定张明远为实际控制人和最终受益人（7.123456% 直接持股 + 34.567891% 总持股 + 51.234567% 表决权）；"
            "工商股东与法定披露快照的股东及持股数据 100%一致；"
            "2015-01-15 至 2025-06-30 共回溯 18 条工商变更，已核验事件与融资及治理节点存在明确时间对应，历史变更有序推进；"
            "员工持股平台、产业资本与机构投资者构成股东结构，治理安排由合伙协议及公开披露支持；"
            "截至 2026-08-17，在已核验的股权出质与冻结范围内未发现相关记录，历史两条担保解除状态已有资料支持；"
            "按本报告阈值控制权稳定，未见明显影响股权稳定性的事项，仍需律师、审计师及保荐机构结合申报口径核验。"
        )
        evidence = self.validator.ConclusionEvidence(
            required_literals=("7.123456%", "34.567891%", "51.234567%"),
            shareholder_list_complete=True,
            ratios_consistent=True,
            control_path_complete=True,
            controller_cross_verified=True,
            snapshot_cross_checked=True,
            rights_scope_complete=True,
            history_event_correlated=True,
        )
        metrics = self.validator.validate_one_line_conclusion(text, evidence)
        self.assertEqual(metrics["clauses"], 7)
        self.assertGreaterEqual(metrics["characters"], 220)
        self.assertLessEqual(metrics["characters"], 350)

    def test_sparse_evidence_uses_short_degraded_conclusion(self) -> None:
        text = (
            "一句话结论：目标企业在可核验股东范围内的股权结构基本可识别，第一大股东持股 18.740000%；"
            "现有资料尚未明确实际控制人，表决权与一致行动安排尚待交叉核验；"
            "前十大股东以机构主体为主，当前控制权稳定性无法判断，仍需取得股东协议和表决权委托材料。"
        )
        evidence = self.validator.ConclusionEvidence(
            required_literals=("18.740000%",),
            forbidden_literals=("52 名", "18 条", "法定披露快照"),
            sparse=True,
        )
        metrics = self.validator.validate_one_line_conclusion(text, evidence)
        self.assertEqual(metrics["clauses"], 3)

    def test_validator_rejects_unsupported_facts_and_strong_claims(self) -> None:
        cases = (
            (
                "一句话结论：目标企业股权结构清晰透明；产品识别控制候选；历史变更可回溯。",
                self.validator.ConclusionEvidence(sparse=True),
            ),
            (
                "一句话结论：目标企业股权结构基本可识别；产品识别结果待互证；法定披露快照 100%一致。",
                self.validator.ConclusionEvidence(sparse=True),
            ),
            (
                "一句话结论：目标企业股权结构基本可识别；产品未识别控制人；股权冻结当前 0 命中。",
                self.validator.ConclusionEvidence(sparse=True),
            ),
            (
                "一句话结论：目标企业股权结构基本可识别；历史变更可回溯；具备 IPO 申报资格。",
                self.validator.ConclusionEvidence(sparse=True),
            ),
            (
                "一句话结论：目标企业股权结构基本可识别；产品未识别控制人；本次未完成快照互证。",
                self.validator.ConclusionEvidence(
                    forbidden_literals=("快照",), sparse=True
                ),
            ),
        )
        for conclusion, evidence in cases:
            with self.subTest(conclusion=conclusion):
                with self.assertRaises(self.validator.ConclusionValidationError):
                    self.validator.validate_one_line_conclusion(conclusion, evidence)
