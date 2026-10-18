# 大模型 Agent 从 0 到 1：完整项目代码

课程配套代码。每个目录对应一集，按顺序学习即可逐步搭建一个完整的内容策划 Agent。

所有脚本**不联网、不读取密钥、不调用模型**，可安全离线运行。

## 项目结构

```
agent-course-project/
├── ep02_deepseek/         第 2 集  DeepSeek API 调用
├── ep03_prompt/           第 3 集  提示词组装
├── ep04_structured/       第 4 集  结构化输出与校验
├── ep05_tool/             第 5 集  工具调用
├── ep06_loop/             第 6 集  有限循环
├── ep07_citation/         第 7 集  引用检查
├── ep08_rag/              第 8 集  最小 RAG
├── ep09_memory/           第 9 集  偏好记忆
├── ep10_pipeline/         第 10 集 项目编排
├── ep11_multi_agent/      第 11 集 多角色对照
├── ep12_eval/             第 12 集 评估
├── ep13_security/         第 13 集 安全边界
├── ep14_perf/             第 14 集 性能与成本
└── ep15_ui/               第 15 集 网页界面
```

## 快速开始

```bash
# 安装依赖（仅第 4 集和第 15 集需要）
python -m pip install "pydantic>=2,<3" streamlit

# 第 2 集：调用 DeepSeek API（唯一会联网的脚本，需要你的 API Key）
python3 ep02_deepseek/app.py

# 第 3 集起离线运行
python3 ep03_prompt/prompt_builder.py
python3 ep04_structured/topic_validator.py
python3 ep05_tool/search_notes.py
python3 ep06_loop/bounded_loop.py
python3 ep07_citation/citation_checker.py
python3 ep08_rag/simple_rag.py
python3 ep09_memory/preference_manager.py
python3 ep10_pipeline/pipeline.py
python3 ep11_multi_agent/multi_agent_compare.py
python3 ep12_eval/evaluator.py
python3 ep13_security/boundary_test.py
python3 ep14_perf/usage_tracker.py

# 第 15 集界面（需要 streamlit）
cd ep15_ui && python -m streamlit run app.py
```

## 能力递进

| 集数 | 新增能力 | 核心文件 |
| --- | --- | --- |
| 2 | 调用 DeepSeek API，获取模型回复 | app.py |
| 3 | 把宽泛需求写成结构化提示词 | prompt_builder.py |
| 4 | 用 JSON + Pydantic 校验模型输出 | topic_validator.py |
| 5 | 模型提请求，程序执行工具 | search_notes.py |
| 6 | 多步行动 + 停止条件 | bounded_loop.py |
| 7 | 来源编号映射 + 引用核对 | citation_checker.py |
| 8 | 从个人资料中检索相关段落 | simple_rag.py |
| 9 | 偏好保存、读取、更新、删除 | preference_manager.py |
| 10 | 固定步骤 + 动态调研的编排 | pipeline.py |
| 11 | 单角色 vs 多角色对照实验 | multi_agent_compare.py |
| 12 | 五题测试集 + 硬检查 | evaluator.py |
| 13 | 白名单 + 注入测试 | boundary_test.py |
| 14 | 分阶段计时 + 用量统计 | usage_tracker.py |
| 15 | Streamlit 网页界面 | app.py |

## 依赖

| 包 | 用在哪 | 最低版本 |
| --- | --- | --- |
| requests | ep02 | 2.32+ |
| pydantic | ep04, ep12 | 2.x |
| streamlit | ep15 | 1.x |

除 ep02 外，其余脚本仅使用 Python 标准库，Python 3.8+ 即可运行。ep02 需要 API Key 才会发送请求。

## 接入真实模型

所有脚本均可安全离线运行。接入真实模型时：

1. 将脚本中的模拟函数替换为你的 API 调用。
2. 准备 API 密钥（环境变量，不要写死在代码里）。
3. 使用第 12 集的测试集验证替换后质量是否退步。
4. 参考 Ep13 的边界检查确保权限不被绕过。

## 许可

课程原创教学样例。可自由修改和分发用于学习。
