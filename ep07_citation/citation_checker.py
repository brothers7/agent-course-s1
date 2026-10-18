#!/usr/bin/env python3
"""第七集练习：引用检查脚本。

用法：python3 citation_checker.py
本脚本不联网、不读取密钥、不发送模型请求。
检查模型输出的引用编号是否都在已核实的来源集合里。
"""

# ---------- 来源表（程序维护，不是模型生成） ----------

SOURCES = {
    "S1": {"url": "https://example.com/docs/function-calling", "verified": True},
    "S2": {"url": "https://example.com/docs/structured-output", "verified": True},
    "S3": {"url": "https://example.com/docs/retrieval", "verified": False},  # 尚未核实
}

# ---------- 教学样例 ----------

# 通过：只引用已有编号
VALID = '{"conclusions": [{"claim": "工具函数由应用程序执行", "source_ids": ["S1"]}]}'

# 失败 1：引用了不存在的编号
# INVALID_ID = '{"conclusions": [{"claim": "性能提升30%", "source_ids": ["S999"]}]}'

# 失败 2：引用了未核实的编号
# UNVERIFIED = '{"conclusions": [{"claim": "RAG 效果更好", "source_ids": ["S3"]}]}'

# 失败 3：结论过度延伸（程序可以提示，但不自动判断语义）
# OVERREACHED = '{"conclusions": [{"claim": "所有模型都支持此功能", "source_ids": ["S1"]}]}'


def check_citations(raw):
    """检查引用编号是否存在且已核实。"""
    import json
    data = json.loads(raw)
    errors = []
    for c in data.get("conclusions", []):
        for sid in c.get("source_ids", []):
            if sid not in SOURCES:
                errors.append(f"编号 {sid} 不在来源表中")
            elif not SOURCES[sid]["verified"]:
                errors.append(f"编号 {sid} 尚未核实")
    return errors


if __name__ == "__main__":
    print("=== 传入合法引用 ===")
    errors = check_citations(VALID)
    print("错误：", errors if errors else "无，通过 ✓")

    print("\n=== 试试取消注释上面的 INVALID_* 变量并传入 check_citations() ===")
    print("观察每种错误分别报什么。注意：过度延伸需要人工判断，脚本只能提醒。")

    # 取消注释试跑（同一时间只运行一行）：
    # print(check_citations(INVALID_ID))
    # print(check_citations(UNVERIFIED))
