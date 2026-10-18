#!/usr/bin/env python3
"""第四集练习：选题卡校验脚本。

用法：python3 topic_validator.py
本脚本不联网、不读取密钥、不发送模型请求。
课堂可逐次修改 VALID 示例中的字段，观察不同层的报错。
"""

from pydantic import BaseModel, Field, field_validator

# ---------- 字段模型 ----------


class Topic(BaseModel):
    title: str = Field(min_length=1)
    minutes: int = Field(ge=5, le=10)
    angle: str = Field(min_length=1)
    source_ids: list[str]

    @field_validator("title", "angle")
    @classmethod
    def reject_blank(cls, value):
        if not value.strip():
            raise ValueError("字段不能只包含空白")
        return value


# ---------- 离线教学样例 ----------

VALID = '{"title":"给 AI 一份能执行的任务","minutes":7,"angle":"学会写任务说明","source_ids":["S1"]}'

# 故意制造的错误示例（取消注释后逐个试跑）：

# 1. 时长超出范围 → 字段校验报错
# INVALID_RANGE = '{"title":"标题","minutes":20,"angle":"角度","source_ids":["S1"]}'

# 2. 删除必填字段 → 字段校验报错
# INVALID_MISSING = '{"minutes":7,"angle":"角度","source_ids":["S1"]}'

# 3. 来源编号不存在 → 结构通过，应用层报错
# INVALID_SOURCE = '{"title":"标题","minutes":7,"angle":"角度","source_ids":["S999"]}'

# 4. 不是合法 JSON → 解析报错
# INVALID_JSON = '{"title": "标题", "minutes": 7,}'

# 5. 空白字符串 → field_validator 报错
# INVALID_BLANK = '{"title":"   ","minutes":7,"angle":"角度","source_ids":["S1"]}'

# ---------- 资料库（本课程离线样例） ----------

KNOWN_SOURCES = {"S1", "S2", "S3"}


def validate(raw: str) -> Topic:
    """执行三道检查：解析、字段校验、来源核对。"""
    # 第一道：解析
    topic = Topic.model_validate_json(raw)
    # 第二道已由 Pydantic 完成；这里是第三道：来源核对
    unknown = set(topic.source_ids) - KNOWN_SOURCES
    if unknown:
        raise ValueError("未知来源编号：" + ", ".join(sorted(unknown)))
    return topic


if __name__ == "__main__":
    print("=== 传入合法样例 ===")
    result = validate(VALID)
    print("通过：", result.model_dump())

    print("\n=== 试试取消注释上面的 INVALID_* 变量并传入 validate() ===")
    print("观察每一道检查分别报什么错。")

    # 逐个取消注释试跑（同一时间只运行一行）：
    # validate(INVALID_RANGE)
    # validate(INVALID_MISSING)
    # validate(INVALID_SOURCE)
    # validate(INVALID_JSON)
    # validate(INVALID_BLANK)

    # 来源存在不等于支持观点，证据对应仍需另行检查。
