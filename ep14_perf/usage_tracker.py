#!/usr/bin/env python3
"""第十四集练习：用量统计脚本。

用法：python3 usage_tracker.py
本脚本不联网、不读取密钥、不发送模型请求。
模拟一次任务的分阶段计时和用量统计，输出运行账单。
"""

import time


class Stage:
    """记录单个阶段的耗时和用量。"""

    def __init__(self, name):
        self.name = name
        self.seconds = 0.0
        self.input_tokens = 0
        self.output_tokens = 0
        self.tool_calls = 0

    def __repr__(self):
        return (f"{self.name:12s} {self.seconds:6.1f}s  "
                f"in:{self.input_tokens:6d} out:{self.output_tokens:6d}  "
                f"tools:{self.tool_calls}")


def simulate_task():
    """模拟一次内容策划任务（离线数据，非实测）。"""
    stages = []

    # 阶段 1：需求检查
    s1 = Stage("需求检查")
    t0 = time.time()
    time.sleep(0.01)  # 模拟
    s1.seconds = round(time.time() - t0, 2)
    s1.input_tokens = 200
    s1.output_tokens = 50
    stages.append(s1)

    # 阶段 2：资料调研
    s2 = Stage("资料调研")
    t0 = time.time()
    time.sleep(0.05)  # 模拟
    s2.seconds = round(time.time() - t0, 2)
    s2.input_tokens = 2000
    s2.output_tokens = 800
    s2.tool_calls = 2
    stages.append(s2)

    # 阶段 3：策划生成
    s3 = Stage("策划生成")
    t0 = time.time()
    time.sleep(0.03)  # 模拟
    s3.seconds = round(time.time() - t0, 2)
    s3.input_tokens = 1500
    s3.output_tokens = 1200
    stages.append(s3)

    return stages


def print_bill(stages):
    total_time = sum(s.seconds for s in stages)
    total_in = sum(s.input_tokens for s in stages)
    total_out = sum(s.output_tokens for s in stages)
    total_tools = sum(s.tool_calls for s in stages)

    print(f"{'阶段':12s} {'耗时':>8s} {'输入tokens':>10s} {'输出tokens':>10s} {'工具调用':>8s}")
    print("-" * 60)
    for s in stages:
        print(f"{s.name:12s} {s.seconds:6.1f}s  {s.input_tokens:10d} {s.output_tokens:10d} {s.tool_calls:8d}")
    print("-" * 60)
    print(f"{'合计':12s} {total_time:6.1f}s  {total_in:10d} {total_out:10d} {total_tools:8d}")

    # 找出最贵的阶段
    slowest = max(stages, key=lambda s: s.seconds)
    print(f"\n最耗时的阶段：{slowest.name}（{slowest.seconds}s）")
    print("提示：先优化这一步。")

    # 简单费用估算（价格仅为示例，以实际账单为准）
    example_in_price = 1.0   # 每百万 tokens
    example_out_price = 2.0  # 每百万 tokens
    cost = (total_in / 1_000_000) * example_in_price + (total_out / 1_000_000) * example_out_price
    print(f"\n示例费用估算（价格仅为演示）：{cost:.6f} 元")
    print("实际费用以所用服务的计费文档和账单为准。")


if __name__ == "__main__":
    print("===== 模拟运行账单 =====\n")
    stages = simulate_task()
    print_bill(stages)
    print("\n这是模拟数据。真实使用时，在每个阶段加上计时器和用量记录。")
