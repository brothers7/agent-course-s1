#!/usr/bin/env python3
"""第十一集练习：单角色 vs 多角色对照实验。

用法：python3 multi_agent_compare.py
本脚本不联网、不读取密钥、不发送模型请求。
模拟单角色和多角色两种方案，记录事实错误、结构错误和步骤数。
"""

import time

NOTES = [
    {"id": "S1", "text": "工具调用：模型提出请求，程序执行函数并回传结果。"},
    {"id": "S2", "text": "RAG：先检索相关片段，再结合片段回答问题。"},
]


def fact_check(outline):
    """检查事实错误：引用的编号是否在来源表中。"""
    known = {n["id"] for n in NOTES}
    errors = [sid for sid in outline.get("source_ids", []) if sid not in known]
    return len(errors)


def structure_check(outline):
    """检查结构错误：必填字段是否完整。"""
    errors = []
    if not outline.get("title"):
        errors.append("title")
    if not outline.get("minutes"):
        errors.append("minutes")
    if not outline.get("source_ids"):
        errors.append("source_ids")
    return len(errors)


def run_single(task):
    """单角色：一次调用完成所有事（模拟）"""
    start = time.time()
    # 模拟：单角色容易遗漏
    outline = {"title": f"关于{task['topic']}的选题", "minutes": 7, "source_ids": ["S1", "S999"]}
    fact_errors = fact_check(outline)
    struct_errors = structure_check(outline)
    elapsed = round(time.time() - start, 2)
    return {"plan": "单角色", "fact_errors": fact_errors, "struct_errors": struct_errors,
            "steps": 1, "seconds": elapsed, "outline": outline}


def run_multi(task):
    """多角色：分三步（模拟）"""
    start = time.time()
    # 步骤 1：调研
    sources = [n["id"] for n in NOTES]
    # 步骤 2：策划
    outline = {"title": f"关于{task['topic']}的选题", "minutes": 7, "source_ids": sources}
    # 步骤 3：审核（模拟审核发现并修正一个错误）
    fact_errors = fact_check(outline)
    struct_errors = structure_check(outline)
    elapsed = round(time.time() - start, 2)
    return {"plan": "三角色", "fact_errors": fact_errors, "struct_errors": struct_errors,
            "steps": 3, "seconds": elapsed, "outline": outline}


if __name__ == "__main__":
    task = {"topic": "工具调用", "audience": "新手", "minutes": 7}

    print("===== 运行单角色 =====")
    r1 = run_single(task)
    print(f"  事实错误：{r1['fact_errors']}  结构错误：{r1['struct_errors']}")
    print(f"  步骤数：{r1['steps']}  耗时：{r1['seconds']}s")

    print("\n===== 运行三角色 =====")
    r2 = run_multi(task)
    print(f"  事实错误：{r2['fact_errors']}  结构错误：{r2['struct_errors']}")
    print(f"  步骤数：{r2['steps']}  耗时：{r2['seconds']}s")

    print("\n===== 比较结果 =====")
    print(f"  {'指标':12s} {'单角色':8s} {'三角色':8s}")
    print(f"  {'事实错误':12s} {r1['fact_errors']:<8d} {r2['fact_errors']:<8d}")
    print(f"  {'结构错误':12s} {r1['struct_errors']:<8d} {r2['struct_errors']:<8d}")
    print(f"  {'步骤数':12s} {r1['steps']:<8d} {r2['steps']:<8d}")
    print(f"  {'耗时(s)':12s} {r1['seconds']:<8} {r2['seconds']:<8}")
    print("\n注意：这是模拟演示。真实实验需要接入模型并用你的任务记录结果。")
