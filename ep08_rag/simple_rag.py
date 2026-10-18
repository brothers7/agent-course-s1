#!/usr/bin/env python3
"""第八集练习：最小关键词检索脚本。

用法：python3 simple_rag.py
本脚本不联网、不读取密钥、不发送模型请求。
用关键词匹配实现检索，找到相关片段并展示来源。
"""

import os
import re

# ---------- 教学文档（替换为你自己的笔记） ----------

DOCUMENTS = [
    {"file": "笔记_工具调用.md", "heading": "工具调用 / 结果回传",
     "text": "程序执行函数并把结果回传给模型，模型根据结果生成最终回答。"},
    {"file": "笔记_结构化输出.md", "heading": "结构化输出 / JSON",
     "text": "让模型输出 JSON 格式，用 Pydantic 校验字段和类型。"},
    {"file": "笔记_RAG.md", "heading": "RAG / 检索增强生成",
     "text": "先从资料中找到相关片段，再把片段和问题一起发给模型。"},
]


def search(query, docs=None, k=3):
    """按关键词匹配文档，返回最相关的 k 条。"""
    if docs is None:
        docs = DOCUMENTS
    keywords = [w for w in re.split(r'[\s，？？、]+', query) if w]
    # 用 2 字滑窗生成子关键词，提高匹配率
    subkeys = set()
    for w in keywords:
        for i in range(len(w) - 1):
            subkeys.add(w[i:i + 2])
    keywords = list(subkeys) if subkeys else keywords
    scored = []
    for d in docs:
        combined = f"{d['heading']} {d['text']}"
        score = sum(1 for w in keywords if w.lower() in combined.lower())
        if score >= 2:
            scored.append((score, d))
    scored.sort(key=lambda x: -x[0])
    return [d for _, d in scored[:k]]


def show(query, docs=None, k=3):
    hits = search(query, docs, k)
    if not hits:
        print(f"  ❌ 没有命中（资料不足）")
        return
    for i, d in enumerate(hits, 1):
        print(f"  [{i}] 来源：{d['file']} > {d['heading']}")
        print(f"      {d['text']}")


if __name__ == "__main__":
    tests = [
        ("工具结果怎么回传？", DOCUMENTS),
        ("JSON 输出怎么校验？", DOCUMENTS),
        ("RAG 是什么？", DOCUMENTS),
        ("今天的模型价格是多少？", DOCUMENTS),  # 超出范围
        ("工具结果怎么回传？", [d for d in DOCUMENTS if "工具" not in d["file"]]),
    ]
    for q, docs in tests:
        print(f"\n=== 问：{q} ===")
        show(q, docs)
        if docs is not DOCUMENTS:
            print("  （已删除相关笔记后的对照）")
