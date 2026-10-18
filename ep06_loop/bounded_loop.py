#!/usr/bin/env python3
"""第六集练习：有界循环模拟器。

用法：python3 bounded_loop.py
本脚本不联网、不读取密钥、不发送模型请求。
模拟一个有限循环的状态管理和四种出口。
"""

MAX_STEPS = 5
MAX_EMPTY_RESULTS = 2

NOTES = [
    {"id": "S1", "text": "工具调用：模型提出请求，程序执行函数并回传结果。", "source": "课程原创示例 A"},
    {"id": "S2", "text": "RAG：先检索相关片段，再结合片段回答问题。", "source": "课程原创示例 B"},
    {"id": "S3", "text": "Agent 循环：有限步数内持续行动，直到触发停止条件。", "source": "课程原创示例 C"},
]


def search_notes(query):
    if not isinstance(query, str) or not query.strip() or len(query) > 200:
        raise ValueError("query 必须是 1 到 200 字符的非空字符串")
    return [x for x in NOTES if query.lower() in x["text"].lower()]


def run_loop(queries):
    """模拟一个有限循环。queries 是预设的搜索关键词列表。"""
    state = {"goal": "为初学者策划选题", "sources": [], "step": 0, "status": "进行中"}
    recent_queries = []
    empty_count = 0

    for i, q in enumerate(queries[:MAX_STEPS]):
        state["step"] = i + 1
        print(f"\n--- 第 {state['step']} 轮，搜索：{q} ---")

        # 检测重复查询
        if q in recent_queries:
            print("⚠ 检测到重复查询，提示换方向或结束")
            state["status"] = "需要人工"
            break
        recent_queries.append(q)

        results = search_notes(q)
        print(f"  返回 {len(results)} 条")

        if results:
            state["sources"].extend(results)
            empty_count = 0
            if len(state["sources"]) >= 2:
                state["status"] = "完成"
                print("  ✅ 已有足够资料，触发完成出口")
                break
        else:
            empty_count += 1
            if empty_count >= MAX_EMPTY_RESULTS:
                state["status"] = "失败"
                print(f"  ❌ 连续 {empty_count} 次空结果，触发失败出口")
                break

    if state["status"] == "进行中":
        state["status"] = "次数用尽"
        print(f"\n⚠ 达到 MAX_STEPS={MAX_STEPS}，触发次数用尽出口")

    print(f"\n===== 最终状态 =====")
    print(f"状态：{state['status']}")
    print(f"步数：{state['step']} / {MAX_STEPS}")
    print(f"已收集 {len(state['sources'])} 条资料")
    for s in state["sources"]:
        print(f"  [{s['id']}] {s['text']}")
    if state["status"] in ("失败", "次数用尽", "需要人工"):
        print(f"提示：还缺少足够的资料来完成选题策划，请补充关键词或资料。")
    return state


if __name__ == "__main__":
    print("=== 场景 1：第一次就找到 ===")
    run_loop(["工具调用", "RAG"])

    print("\n\n=== 场景 2：空结果后换关键词 ===")
    run_loop(["不存在的词", "Agent 循环", "RAG"])

    print("\n\n=== 场景 3：连续空结果 ===")
    run_loop(["不存在A", "不存在B"])

    print("\n\n=== 场景 4：重复查询 ===")
    run_loop(["工具调用", "工具调用"])
