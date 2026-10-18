#!/usr/bin/env python3
"""第十集练习：项目编排脚本。

用法：python3 pipeline.py
本脚本不联网、不读取密钥、不发送模型请求。
模拟内容策划流程的五个阶段，展示固定步骤和动态调研。
"""

MAX_RESEARCH_STEPS = 2

NOTES = [
    {"id": "S1", "text": "工具调用：模型提出请求，程序执行函数并回传结果。", "source": "课程原创示例 A"},
    {"id": "S2", "text": "RAG：先检索相关片段，再结合片段回答问题。", "source": "课程原创示例 B"},
]


def check_requirements(inp):
    """阶段 1：需求检查（固定规则）"""
    missing = []
    if not inp.get("topic"):
        missing.append("topic")
    if not inp.get("audience"):
        missing.append("audience")
    if not inp.get("minutes"):
        missing.append("minutes")
    if missing:
        return {"status": "incomplete", "missing": missing}
    return {"status": "ok", "missing": []}


def research_with_limits(inp):
    """阶段 2：调研（动态决策，有上限）"""
    existing = inp.get("sources", [])
    if len(existing) >= 2:
        return {"status": "skipped", "sources": existing, "steps": 0}
    # 模拟补查
    query = inp.get("topic", "")
    found = [n for n in NOTES if query.lower() in n["text"].lower()]
    steps = min(len(found), MAX_RESEARCH_STEPS)
    all_sources = existing + found[:MAX_RESEARCH_STEPS]
    if len(all_sources) < 1:
        return {"status": "insufficient", "sources": all_sources, "steps": steps}
    return {"status": "ok", "sources": all_sources, "steps": steps}


def generate_outline(sources, topic):
    """阶段 3：策划（模拟模型调用）"""
    if not sources:
        return {"status": "no_sources", "outline": None}
    ids = [s["id"] for s in sources]
    outline = {"title": f"关于{topic}的选题", "source_ids": ids, "minutes": 7}
    return {"status": "ok", "outline": outline}


def validate(outline):
    """阶段 4：校验（固定规则）"""
    if not outline:
        return {"status": "fail", "errors": ["大纲为空"]}
    errors = []
    if not (5 <= outline.get("minutes", 0) <= 10):
        errors.append("时长不在 5–10 范围内")
    if not outline.get("source_ids"):
        errors.append("缺少来源编号")
    if errors:
        return {"status": "fail", "errors": errors}
    return {"status": "ok", "errors": []}


def run_project(inp):
    """项目编排主函数"""
    print("\n===== 阶段 1：需求检查 =====")
    r1 = check_requirements(inp)
    if r1["status"] == "incomplete":
        print(f"  ❌ 缺少字段：{r1['missing']}")
        return r1
    print("  ✅ 通过")

    print("\n===== 阶段 2：调研 =====")
    r2 = research_with_limits(inp)
    if r2["status"] == "skipped":
        print(f"  ⏭ 已有 {len(r2['sources'])} 条资料，跳过调研")
    elif r2["status"] == "insufficient":
        print(f"  ❌ 补查 {r2['steps']} 步后仍不足，缺口：缺少相关资料")
        return {"status": "需人工", "draft": None, "errors": ["资料不足"]}
    else:
        print(f"  ✅ 补查 {r2['steps']} 步，共 {len(r2['sources'])} 条")

    print("\n===== 阶段 3：策划 =====")
    r3 = generate_outline(r2["sources"], inp["topic"])
    if r3["status"] != "ok":
        print("  ❌ 无法生成大纲")
        return r3
    print(f"  ✅ 大纲：{r3['outline']['title']}（引用 {r3['outline']['source_ids']}）")

    print("\n===== 阶段 4：校验 =====")
    r4 = validate(r3["outline"])
    if r4["status"] != "ok":
        print(f"  ❌ 校验失败：{r4['errors']}")
        return {"status": "需人工", "draft": r3["outline"], "errors": r4["errors"]}
    print("  ✅ 通过")

    print("\n===== 阶段 5：待发布 =====")
    print("  ✅ 大纲已通过校验，等待人工确认发布")
    return {"status": "待发布", "draft": r3["outline"], "errors": []}


if __name__ == "__main__":
    print("########## 路径 A：资料完整 ##########")
    run_project({"topic": "工具调用", "audience": "新手", "minutes": 7,
                 "sources": [NOTES[0], NOTES[1]]})

    print("\n\n########## 路径 B：资料不足 ##########")
    run_project({"topic": "RAG", "audience": "新手", "minutes": 7})

    print("\n\n########## 路径 C：需求不完整 ##########")
    run_project({"topic": "", "audience": "新手", "minutes": 7})
