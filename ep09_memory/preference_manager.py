#!/usr/bin/env python3
"""第九集练习：偏好管理脚本。

用法：python3 preference_manager.py
本脚本不联网、不读取密钥、不发送模型请求。
演示偏好档案的保存、读取、更新、删除和临时覆盖。
"""

import json
import os

PROFILE_FILE = "preferences.json"

DEFAULT_PROFILE = {
    "audience": "新手创作者",
    "style": "表达直接，优先可录屏例子",
    "demo_first": True,
    "source": "user_set",
    "updated": "2026-10-16"
}


def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return dict(DEFAULT_PROFILE)


def save_profile(profile):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def update_profile(profile, key, value):
    profile[key] = value
    profile["updated"] = "2026-10-16"
    save_profile(profile)
    print(f"  ✅ 已更新 {key} = {value}")


def delete_profile(profile, key):
    if key in profile:
        del profile[key]
        save_profile(profile)
        print(f"  ✅ 已删除 {key}")
    else:
        print(f"  ⚠ {key} 不存在")


def resolve(profile, override=None):
    """合并默认偏好和本次覆盖。"""
    result = dict(profile)
    result.pop("source", None)
    result.pop("updated", None)
    if override:
        result.update(override)
    return result


if __name__ == "__main__":
    print("=== 1. 读取默认偏好 ===")
    p = load_profile()
    print(json.dumps(p, ensure_ascii=False, indent=2))

    print("\n=== 2. 更新受众 ===")
    update_profile(p, "audience", "开发者")
    print("  当前受众：", p["audience"])

    print("\n=== 3. 临时覆盖（不改档案） ===")
    effective = resolve(p, {"audience": "资深工程师"})
    print("  本次生效受众：", effective["audience"])
    print("  档案中受众（未变）：", load_profile()["audience"])

    print("\n=== 4. 删除字段 ===")
    delete_profile(p, "demo_first")

    print("\n=== 5. 清理演示文件 ===")
    if os.path.exists(PROFILE_FILE):
        os.remove(PROFILE_FILE)
        print("  已删除 preferences.json（恢复默认状态）")
