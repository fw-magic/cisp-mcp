from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents" / "skills" / "股权结构分析"
SKILL_PATH = SKILL_DIR / "SKILL.md"
REFERENCE_PATH = SKILL_DIR / "references" / "customer-facing-language.md"
VALIDATOR_PATH = SKILL_DIR / "scripts" / "customer_facing_language_validator.py"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "equity_customer_facing_language_validator_test", VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class EquityCustomerFacingLanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_skill_requires_customer_language_reference_and_validation(self) -> None:
        skill = SKILL_PATH.read_text(encoding="utf-8")
        reference = REFERENCE_PATH.read_text(encoding="utf-8")
        self.assertIn("references/customer-facing-language.md", skill)
        self.assertIn("validate_customer_facing_report()", skill)
        self.assertIn("内部证据模型可以保留", skill)
        self.assertIn("不得为了消除内部术语而提高证据强度", skill)
        for expected in (
            "产品识别",
            "本次返回",
            "当前不可用",
            "0 命中",
            "聚合值",
            "数据断点",
            "路径互证",
        ):
            self.assertIn(expected, reference)

    def test_professional_customer_language_passes(self) -> None:
        report = (
            "一句话结论：目标企业股权较为分散，从前十大股东结构看，第一大股东持股18.740000%；"
            "现有股权与控制关系资料指向某国资监管机构为实际控制主体，相关结论已由三条控制链条交叉印证；"
            "最终受益路径尚未完整还原，经营管理人员名单仅反映管理层范围；"
            "从股权集中度与表决权信息看，控制权稳定性偏弱，仍需核验一致行动协议。"
        )
        result = self.validator.validate_customer_facing_report(report)
        self.assertEqual(result["forbidden_findings"], 0)

    def test_validator_rejects_machine_facing_phrases_and_spacing_variants(self) -> None:
        phrases = (
            "产品识别某人为实际控制人",
            "产品 返回14名管理人员",
            "本次返回的前十大股东",
            "52名直接股东完整返回",
            "本次 未完成互证",
            "接口原值为18.740000%",
            "最终受益路径当前不可用",
            "股权冻结0命中",
            "股权冻结 0 命中",
            "控制路径聚合值为18.267524%",
            "境外主体形成数据断点",
            "相关结论已完成路径互证",
            "模型判定控制权脆弱",
            "状态码为4",
            "内部产品码P0020129",
        )
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                with self.assertRaises(self.validator.CustomerFacingLanguageError):
                    self.validator.validate_customer_facing_report(phrase)

    def test_data_service_brand_name_is_allowed(self) -> None:
        text = "数据来源：水滴征信 MCP，资料日期为2026-08-17。"
        self.validator.validate_customer_facing_report(text)
