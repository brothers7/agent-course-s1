# 第 2 集：第一次调用 DeepSeek API

## 运行

```bash
# 安装依赖
python -m pip install -r requirements.txt

# 运行（会提示输入 API Key，或设置环境变量 DEEPSEEK_API_KEY）
python3 app.py

# 第二次调用（额外要求演示建议）
python3 app.py --variant demo
```

## 做什么

用 `requests` 直接调用 DeepSeek 官方对话端点 `https://api.deepseek.com/chat/completions`。

- 默认模型：`deepseek-flash`
- 密钥：环境变量 `DEEPSEEK_API_KEY` 或本地隐藏输入
- 非流式 + 关闭思考模式
- 检查 `finish_reason` 为 `stop`，输出非空文字
- 覆盖 HTTP 400/401/402/422/429/500/503 错误码排查

## ⚠️ 唯一会联网的脚本

本项目其他所有脚本均不联网。**只有这个脚本在你主动运行时才会发送 API 请求。** 需要你自己的 DeepSeek API Key（在 [DeepSeek 开放平台](https://platform.deepseek.com/) 创建）。课程代码不包含真实密钥。

## 在项目中的位置

这是整个项目与模型交互的第一步。后续所有集的工具调用、结构化输出、RAG 检索，都建立在这个基本 API 调用之上。
