# 第 4 集：结构化输出与校验

## 运行
```bash
python3 topic_validator.py
# 依赖: pip install "pydantic>=2,<3"
```
## 做什么
用 Pydantic 定义选题卡模型，对 JSON 输出执行解析、字段校验和来源核对三道检查。
## 在项目中的位置
模型输出不再是自由文本，而是可程序检查的数据。后续评估和安全检查都依赖这个基础。
