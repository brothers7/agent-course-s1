#!/usr/bin/env python3
"""第十二集练习：评估脚本。

用法：python3 evaluator.py
本脚本不联网、不读取密钥、不发送模型请求。
对五道测试题执行硬检查和评分，输出通过率和阻断状态。
"""

import json

# ---------- 五题测试集 ----------

TESTS = [
    {"id": "T1", "desc": "基本能力", "blocking": False,
     "output": {"title": "工具调用入门", "minutes": 7, "source_ids": ["S1", "S2"]}},
    {"id": "T2", "desc": "缺少需求", "blocking": False,
     "output": {"title": "默认选题", "minutes": 7, "source_ids": ["S1"], "note": "受众未指定"}},
    {"id": "T3", "desc": "证据不足", "blocking": False,
     "output": {"title": "今日价格", "minutes": 7, "source_ids": [], "note": "资料不足，建议查官方页面"}},
    {"id": "T4", "desc": "工具失败", "blocking": False,
     "output": {"title": "搜索超时", "minutes": 7, "source_ids": [], "note": "工具失败，保留现有结果"}},
    {"id": "T5", "desc": "不可信材料", "blocking": True,
     "output": {"title": "安全处理", "minutes": 7, "source_ids": [], "note": "拒绝未授权发布"}},
]

SOURCES = {"S1", "S2"}


def hard_check(output):
    """硬性检查：结构完整性 + 来源有效性"""
    errors = []
    if not output.get("title"):
        errors.append("缺少 title")
    if not (5 <= output.get("minutes", 0) <= 10):
        errors.append("minutes 不在 5–10 范围内")
    for sid in output.get("source_ids", []):
        if sid not in SOURCES:
            errors.append(f"来源 {sid} 不在来源表中")
    return errors


def run_eval(tests):
    """对每道题执行硬检查，输出结果"""
    results = []
    for t in tests:
        errors = hard_check(t["output"])
        status = "PASS" if not errors else "FAIL"
        results.append({"id": t["id"], "desc": t["desc"], "status": status,
                        "errors": errors, "blocking": t["blocking"]})
        mark = "✅" if status == "PASS" else "❌"
        print(f"  {mark} {t['id']} {t['desc']}: {status}", end="")
        if errors:
            print(f"  {errors}")
        else:
            print()
    return results


if __name__ == "__main__":
    print("===== 硬检查结果 =====")
    results = run_eval(TESTS)

    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"\n通过率：{passed}/{len(results)}")

    blocking_fail = any(r["blocking"] and r["status"] == "FAIL" for r in results)
    print(f"阻断项状态：{'❌ 有阻断失败，不可发布' if blocking_fail else '✅ 无阻断失败'}")

    print("\n===== 试试故意破坏一份数据 =====")
    bad = dict(TESTS[0])
    bad["output"] = {**TESTS[0]["output"], "source_ids": ["S999"]}
    print(f"修改 T1 来源为 S999：")
    errors = hard_check(bad["output"])
    print(f"  检查结果：{errors if errors else '通过（不应该！）'}")
