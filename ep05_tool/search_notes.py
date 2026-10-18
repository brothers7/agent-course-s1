#!/usr/bin/env python3
"""第五集练习：本地查询工具。

用法：python3 search_notes.py
本脚本不联网、不读取密钥、不发送模型请求。
课堂可修改 NOTES 和 ALLOWED，观察不同结果。
"""

# ---------- 教学资料库 ----------

NOTES = [
    {"id": "S1", "text": "工具调用：模型提出请求，程序执行函数并回传结果。", "source": "课程原创示例 A"},
    {"id": "S2", "text": "RAG：先检索相关片段，再结合片段回答问题。", "source": "课程原创示例 B"},
]

# ---------- 工具函数 ----------


def search_notes(query):
    """根据关键词搜索 NOTES，返回匹配记录列表。"""
    if not isinstance(query, str) or not query.strip() or len(query) > 200:
        raise ValueError("query 必须是 1 到 200 字符的非空字符串")
    return [x for x in NOTES if query.lower() in x["text"].lower()]


# ---------- 白名单 ----------

ALLOWED = {"search_notes": search_notes}


def execute_request(name, args):
    """执行工具调用前的三道检查，然后运行函数。"""
    # 1. 白名单
    if name not in ALLOWED:
        raise ValueError(f"未知工具：{name}")
    # 2. 参数结构
    if not isinstance(args, dict) or set(args) != {"query"}:
        raise ValueError("参数必须且只能包含 query")
    # 3. 参数值（search_notes 内部检查）
    return ALLOWED[name](args["query"])


# ---------- 演示 ----------

if __name__ == "__main__":
    print("=== 测试 1：命中 ===")
    result = execute_request("search_notes", {"query": "工具调用"})
    print(f"返回 {len(result)} 条：", result)

    print("\n=== 测试 2：空结果 ===")
    result = execute_request("search_notes", {"query": "不存在的关键词"})
    print(f"返回 {len(result)} 条：", result)

    print("\n=== 测试 3：非法参数 ===")
    try:
        execute_request("search_notes", {"query": 123})
    except ValueError as exc:
        print("预期失败：", exc)

    print("\n=== 课后：在 NOTES 里补一条你自己的资料，再跑一遍 ===")
