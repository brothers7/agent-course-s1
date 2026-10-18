"""第 2 集 DeepSeek 官方 API 样例。只有主动运行 main 才会发送请求。"""
import argparse
import os
import sys
import warnings
from getpass import GetPassWarning, getpass

import requests

BASE_URL = "https://api.deepseek.com"
API_URL = BASE_URL + "/chat/completions"
DEFAULT_MODEL = "deepseek-flash"
PROMPT_BASE = "为第一次接触 Agent 的创作者生成 3 个视频选题，只输出编号和标题。"
PROMPT_DEMO = "为第一次接触 Agent 的创作者生成 3 个视频选题，每个附一个可录屏的演示建议。"


def make_payload(model, prompt):
    return {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "thinking": {"type": "disabled"},
        "max_tokens": 800,
    }


def extract_text(data):
    try:
        choice = data["choices"][0]
        text = choice["message"]["content"]
        finish_reason = choice["finish_reason"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("响应结构不符合本课约定。") from exc
    if finish_reason != "stop":
        raise ValueError("生成未正常结束，请检查输出上限、内容过滤或服务状态。")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("响应未包含非空文字。")
    return text.strip()


def request_text(url, api_key, payload):
    # 教学版只允许官方端点，不接受转发站或任意地址。
    if url != API_URL:
        raise ValueError("本课仅支持 DeepSeek 官方对话端点。")
    headers = {"Authorization": "Bearer " + api_key}
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=(10, 90),
        allow_redirects=False,
    )
    if 300 <= response.status_code < 400:
        raise ValueError("服务返回重定向，不自动转发凭证。")
    response.raise_for_status()
    return extract_text(response.json())


def read_config():
    model = os.getenv("DEEPSEEK_MODEL", DEFAULT_MODEL).strip()
    if not model:
        raise ValueError("模型名不能为空。")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        with warnings.catch_warnings():
            warnings.simplefilter("error", GetPassWarning)
            api_key = getpass("API Key: ")
    if not api_key.strip():
        raise ValueError("密钥不能为空。")
    return API_URL, api_key.strip(), model


def main():
    parser = argparse.ArgumentParser(description="第 2 集：调用 DeepSeek 官方 API")
    parser.add_argument("--variant", choices=["base", "demo"], default="base")
    args = parser.parse_args()
    prompt = PROMPT_DEMO if args.variant == "demo" else PROMPT_BASE
    try:
        url, api_key, model = read_config()
        payload = make_payload(model, prompt)
        text = request_text(url, api_key, payload)
    except GetPassWarning:
        print("当前终端不能隐藏密钥输入，已停止。请使用系统终端。", file=sys.stderr)
        return 1
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "未知"
        hints = {
            400: "请求格式错误，请检查请求体。",
            401: "认证失败，请检查 DeepSeek API Key。",
            402: "账户余额不足，请检查开放平台余额。",
            422: "参数错误，请核对模型标识与请求参数。",
            429: "请求速率达到上限，请降低调用频率。",
            500: "服务端故障，请稍后再试。",
            503: "服务繁忙，请稍后再试。",
        }
        print(f"请求失败：HTTP {status}。" + hints.get(status, "请按 DeepSeek 官方文档检查。"), file=sys.stderr)
        return 1
    except requests.Timeout:
        print("请求超时，请检查网络与服务状态，不要盲目重复请求。", file=sys.stderr)
        return 1
    except requests.exceptions.JSONDecodeError:
        print("返回内容不是有效 JSON，请检查服务状态。", file=sys.stderr)
        return 1
    except requests.RequestException:
        print("网络请求失败，请检查连接、TLS 与服务状态。", file=sys.stderr)
        return 1
    except (ValueError, EOFError):
        print("配置或返回不符合本课约定。请检查模型名、非空密钥、响应格式与输出是否正常结束。", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n已取消。", file=sys.stderr)
        return 130
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
