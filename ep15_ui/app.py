#!/usr/bin/env python3
"""第十五集练习：内容策划助手离线界面。

启动：python -m streamlit run app.py
本示例使用模拟结果，不需要 API 密钥，不调用模型。
接入真实功能时，将 demo_plan 替换为已实现的策划函数。
"""

import streamlit as st

st.set_page_config(page_title="内容策划助手", layout="centered")
st.title("内容策划助手")
st.info("离线界面演示：当前结果是模拟内容，没有调用大模型。")


def demo_plan(topic, audience, minutes):
    """模拟策划函数（真实接入时替换此函数）。"""
    return (
        f"# {topic}\n\n"
        f"受众：{audience}\n"
        f"目标时长：{minutes} 分钟\n\n"
        f"此为模拟草稿。\n\n"
        f"1. 用一个具体结果开场\n"
        f"2. 解释本集核心概念\n"
        f"3. 演示操作与常见错误\n"
        f"4. 留下一个练习\n\n"
        f"资料与事实需要另行核对。"
    )


with st.form("brief"):
    topic = st.text_input("主题")
    audience = st.text_input("目标受众", value="零基础内容创作者")
    minutes = st.slider("目标时长（分钟）", 5, 10, 7)
    simulate_error = st.checkbox("测试：模拟后端失败")
    submitted = st.form_submit_button("生成模拟草稿")

if submitted:
    st.session_state.pop("draft", None)
    if not topic.strip() or not audience.strip():
        st.warning("请填写主题和目标受众。")
    else:
        try:
            with st.spinner("正在生成离线示例…"):
                if simulate_error:
                    raise RuntimeError("教学用模拟失败")
                st.session_state["draft"] = demo_plan(topic.strip(), audience.strip(), minutes)
        except RuntimeError:
            st.error("模拟后端暂时失败，请取消测试选项后重试。输入仍保留在表单中。")

if "draft" in st.session_state:
    st.subheader("待审核草稿（模拟）")
    st.markdown(st.session_state["draft"])
    st.download_button(
        "下载模拟草稿",
        st.session_state["draft"],
        file_name="video_plan_demo.md",
        mime="text/markdown",
    )
