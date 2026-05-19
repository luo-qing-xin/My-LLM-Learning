# VMware + 硅基流动 API 评测 Qwen/Qwen2.5-72B-Instruct on LiveCodeBench

本文档记录一种**不使用本地 GPU** 的 LiveCodeBench 评测流程：通过 VMware Ubuntu 运行 LiveCodeBench，本地只负责加载题目、调用硅基流动 API、保存生成结果、执行测试和计算分数；模型推理由硅基流动 API 完成。

> 适用场景：本地没有 NVIDIA GPU，无法使用 vLLM 加载 72B 模型，但希望在 LiveCodeBench 上评测 `Qwen/Qwen2.5-72B-Instruct`。

---

## 1. 实验目标

| 项目 | 配置 |
|---|---|
| Benchmark | LiveCodeBench |
| Scenario | `codegeneration` |
| Release Version | `release_v4` |
| 模型 | `Qwen/Qwen2.5-72B-Instruct` |
| 推理方式 | 硅基流动 SiliconFlow API |
| 本地环境 | VMware Ubuntu |
| 是否使用本地 GPU | 否 |
| 输出格式 | LiveCodeBench `custom_output_file` |
| 评分方式 | `lcb_runner.runner.custom_evaluator` |

`release_v4` 覆盖 2023-05 到 2024-09 的题目集合，共 713 道题，适合与 Qwen2.5 系列报告中的 LiveCodeBench 2305–2409 设置对齐。

[Qwen/Qwen2.5-72B-Instruct技术报告](https://arxiv.org/pdf/2412.15115)

<img width="636" height="346" alt="image" src="https://github.com/user-attachments/assets/363e8947-175c-4152-b446-f4085fe85b53" />



---

## 2. 整体流程

```text
在电脑上安装 VMware Ubuntu
        ↓
安装 LiveCodeBench
        ↓
加载 release_v4 codegeneration 题目
        ↓
调用硅基流动 API：Qwen/Qwen2.5-72B-Instruct
        ↓
保存 custom_outputs/qwen25_72b_release_v4_n1.json
        ↓
使用 custom_evaluator 本地执行测试
        ↓
计算 Pass@1
```

注意：不要直接运行如下命令评测 72B 模型：

```bash
python -m lcb_runner.runner.main \
  --model Qwen/Qwen2.5-72B-Instruct \
  --scenario codegeneration \
  --evaluate \
  --release_version release_v4
```

原因是 LiveCodeBench 对开源模型默认使用 vLLM 进行本地推理，而 VMware Ubuntu 没有 NVIDIA CUDA，无法本地加载 72B 模型。本文档采用 API 生成 + 本地评测的方式规避 GPU 需求。

---

## 3. 环境准备

### 3.1 安装系统依赖

在 VMware Ubuntu 终端执行：

```bash
sudo apt update
sudo apt install -y git curl build-essential python3 python3-venv python3-dev
```

检查 Python 版本：

```bash
python3 --version
```

建议使用 Python 3.10 或 3.11。

---

### 3.2 克隆 LiveCodeBench

```bash
cd ~
git clone https://github.com/LiveCodeBench/LiveCodeBench.git
cd LiveCodeBench
```

---

### 3.3 创建虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
```

以后每次重新进入项目时，都需要先激活环境：

```bash
cd ~/LiveCodeBench
source .venv/bin/activate
```

---

### 3.4 安装依赖

因为本实验不使用 GPU，也不需要 vLLM 本地推理，所以建议先安装本流程需要的核心依赖：

```bash
pip install -U openai tqdm tenacity numpy pandas pebble datasets transformers sentencepiece
```

安装 CPU 版 PyTorch：

```bash
pip install --index-url https://download.pytorch.org/whl/cpu "torch>=2.3"
```

再以 editable 方式安装 LiveCodeBench 代码，但不额外安装 vLLM 等 GPU 推理依赖：

```bash
pip install -e . --no-deps
```

检查是否安装成功：

```bash
python - <<'PY'
import lcb_runner
print("LiveCodeBench import OK")
PY
```

如果后续加载数据集时出现 `trust_remote_code is not supported anymore` 之类报错，可以尝试将 `datasets` 降级到兼容版本：

```bash
pip install "datasets==2.21.0"
```

---

## 4. 配置硅基流动 API

### 4.1 设置环境变量

在终端执行：

```bash
export SILICONFLOW_API_KEY="你的硅基流动API_KEY"
export SILICONFLOW_BASE_URL="https://api.siliconflow.cn/v1"
export SILICONFLOW_MODEL="Qwen/Qwen2.5-72B-Instruct"
```

检查变量是否存在：

```bash
python - <<'PY'
import os
print("BASE_URL:", os.environ.get("SILICONFLOW_BASE_URL"))
print("MODEL:", os.environ.get("SILICONFLOW_MODEL"))
print("API_KEY exists:", bool(os.environ.get("SILICONFLOW_API_KEY")))
PY
```

---

### 4.2 测试 API 是否可用

```bash
python - <<'PY'
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["SILICONFLOW_API_KEY"],
    base_url=os.environ.get("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1"),
)

resp = client.chat.completions.create(
    model=os.environ.get("SILICONFLOW_MODEL", "Qwen/Qwen2.5-72B-Instruct"),
    messages=[
        {"role": "user", "content": "用 Python 写一个读取两个整数并输出和的程序，只输出代码。"}
    ],
    temperature=0.2,
    top_p=0.95,
    max_tokens=512,
)

print(resp.choices[0].message.content)
PY
```

如果能返回 Python 代码，说明 API 配置正常。

---

## 5. 编写生成脚本

创建目录：

```bash
mkdir -p scripts custom_outputs
```

新建脚本：

```bash
nano scripts/generate_siliconflow_lcb.py
```

写入以下内容：

```python
import argparse
import json
import os
import time
from pathlib import Path

from openai import OpenAI
from tqdm import tqdm

from lcb_runner.benchmarks.code_generation import load_code_generation_dataset
from lcb_runner.prompts import format_prompt_generation
from lcb_runner.lm_styles import LMStyle
from lcb_runner.utils.extraction_utils import extract_code


def load_existing(path: Path):
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    existing = {}
    for item in data:
        existing[str(item["question_id"])] = item.get("code_list", [])
    return existing


def save_outputs(path: Path, benchmark, existing):
    data = []
    for q in benchmark:
        qid = str(q.question_id)
        if qid in existing:
            data.append({"question_id": qid, "code_list": existing[qid]})

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp.json")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp_path.replace(path)


def call_siliconflow(client, model, messages, temperature, top_p, max_tokens, retries, sleep):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=False,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            last_error = e
            wait = sleep * attempt
            print(f"[WARN] API failed on attempt {attempt}/{retries}: {repr(e)}")
            print(f"[WARN] sleep {wait:.1f}s then retry")
            time.sleep(wait)

    raise RuntimeError(f"API failed after {retries} retries: {repr(last_error)}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--release_version", default="release_v4")
    parser.add_argument("--start_date", default=None)
    parser.add_argument("--end_date", default=None)

    parser.add_argument("--model", default=os.environ.get("SILICONFLOW_MODEL", "Qwen/Qwen2.5-72B-Instruct"))
    parser.add_argument("--base_url", default=os.environ.get("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1"))
    parser.add_argument("--api_key", default=os.environ.get("SILICONFLOW_API_KEY"))

    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--max_tokens", type=int, default=2000)

    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--sleep", type=float, default=1.0)
    parser.add_argument("--retries", type=int, default=5)

    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", default="custom_outputs/qwen25_72b_release_v4_n1.json")

    args = parser.parse_args()

    if not args.api_key:
        raise RuntimeError("Missing SILICONFLOW_API_KEY. Please export SILICONFLOW_API_KEY first.")

    client = OpenAI(
        api_key=args.api_key,
        base_url=args.base_url,
        timeout=args.timeout,
    )

    benchmark = load_code_generation_dataset(
        release_version=args.release_version,
        start_date=args.start_date,
        end_date=args.end_date,
    )
    benchmark = sorted(benchmark, key=lambda x: str(x.question_id))

    if args.limit is not None:
        benchmark = benchmark[: args.limit]

    output_path = Path(args.output)
    existing = load_existing(output_path)

    print(f"Model: {args.model}")
    print(f"Base URL: {args.base_url}")
    print(f"Problems: {len(benchmark)}")
    print(f"Samples per problem: {args.n}")
    print(f"Output: {output_path}")

    for q in tqdm(benchmark):
        qid = str(q.question_id)
        code_list = existing.get(qid, [])

        if len(code_list) >= args.n:
            continue

        messages = format_prompt_generation(q, LMStyle.OpenAIChat)

        while len(code_list) < args.n:
            raw_output = call_siliconflow(
                client=client,
                model=args.model,
                messages=messages,
                temperature=args.temperature,
                top_p=args.top_p,
                max_tokens=args.max_tokens,
                retries=args.retries,
                sleep=args.sleep,
            )

            code = extract_code(raw_output, LMStyle.OpenAIChat)
            if not code or not code.strip():
                code = raw_output

            code_list.append(code)
            existing[qid] = code_list
            save_outputs(output_path, benchmark, existing)
            time.sleep(args.sleep)

    save_outputs(output_path, benchmark, existing)
    print("Done.")


if __name__ == "__main__":
    main()
```

保存并退出：

```text
Ctrl + O
Enter
Ctrl + X
```

---

## 6. 小样本测试

先生成 3 道题，确认流程正常：

```bash
python scripts/generate_siliconflow_lcb.py \
  --release_version release_v4 \
  --n 1 \
  --limit 3 \
  --output custom_outputs/test_qwen25_72b_3.json
```
查看输出：

```bash
cat custom_outputs/test_qwen25_72b_3.json
```

输出格式应类似：

```json
[
  {
    "question_id": "1873_A",
    "code_list": [
      "import sys\n..."
    ]
  }
]
```

小样本文件只用于检查生成是否正常，不用于正式评分。`custom_evaluator` 要求输出文件中的题目数量与 benchmark 题目数量一致。
## 7. 容易出现的问题
### 7.1 超时问题
如果出现超时现象，终端大概是如下的：
```bash
timed out thrown while requesting HEAD https://huggingface.co/datasets/livecodebench/code_generation_lite/resolve/main/README.md Retrying in 1s [Retry 1/5].
```
**这是 Hugging Face 数据集下载超时的问题**

按照如下方法解决：
设置 Hugging Face 镜像
```bash
export HF_ENDPOINT="https://hf-mirror.com"
```
然后在终端再执行单独的将数据集下载到本地的代码：
```bash
python - <<'PY'
from datasets import load_dataset

ds = load_dataset("livecodebench/code_generation_lite", split="test")
print(ds)
print(ds[0].keys())
PY
```
### 7.2 版本不兼容问题
如果出现不兼容现象，终端大概是如下的：
```
trust_remote_code is not supported anymore. Please check that the Hugging Face dataset 'livecodebench/code_generation_lite' isn't based on a loading script and remove trust_remote_code. If the dataset is based on a loading script, please ask the dataset author to remove it and convert it to a standard format like Parquet.
```
**这是LiveCodeBench + Hugging Face datasets 版本不兼容导致的问题**

原因是：datasets>=4.0.0 已经不再支持 trust_remote_code，而 livecodebench/code_generation_lite 仍然依赖 Hugging Face dataset loading script。

LiveCodeBench 官方 issue 里也有人遇到同样问题，建议使用 datasets<4.0。

进行降级 datasets：
```
pip uninstall -y datasets
pip install "datasets==3.6.0"
```
---

## 8. 正式生成全量结果

### 8.1 低成本版本：n=1

建议先跑 `n=1`，即每道题只生成 1 个答案。release_v4 共 713 道题，因此约 713 次 API 调用。

```bash
python scripts/generate_siliconflow_lcb.py \
  --release_version release_v4 \
  --n 1 \
  --temperature 0.2 \
  --top_p 0.95 \
  --max_tokens 2000 \
  --sleep 1.0 \
  --output custom_outputs/qwen25_72b_release_v4_n1.json
```

如果中途断开，重新执行同一条命令即可。脚本会读取已有 JSON，并跳过已经生成完成的题目。

---

### 8.2 更接近 LiveCodeBench 默认生成设置：n=10

LiveCodeBench 默认生成设置是 `n=10`、`temperature=0.2`。如果预算允许，可以生成 `n=10`：

```bash
python scripts/generate_siliconflow_lcb.py \
  --release_version release_v4 \
  --n 10 \
  --temperature 0.2 \
  --top_p 0.95 \
  --max_tokens 2000 \
  --sleep 1.0 \
  --output custom_outputs/qwen25_72b_release_v4_n10.json
```

注意：`n=10` 需要约 `713 × 10 = 7130` 次 API 调用，耗时和费用都更高。建议先完成 `n=1` 版本。

---

## 9. 使用 custom_evaluator 评分

### 9.1 对 n=1 结果评分

```bash
python -m lcb_runner.runner.custom_evaluator \
  --scenario codegeneration \
  --release_version release_v4 \
  --custom_output_file custom_outputs/qwen25_72b_release_v4_n1.json \
  --num_process_evaluate 4 \
  --timeout 20
```

如果 VMware 分配的 CPU 核心较少，建议降低并行度：

```bash
python -m lcb_runner.runner.custom_evaluator \
  --scenario codegeneration \
  --release_version release_v4 \
  --custom_output_file custom_outputs/qwen25_72b_release_v4_n1.json \
  --num_process_evaluate 2 \
  --timeout 30
```
如果还是不行的话，建议开一个内存大一点的虚拟机（最好在16GB以上），或者直接在云服务器上跑

---

### 9.2 对 n=10 结果评分

```bash
python -m lcb_runner.runner.custom_evaluator \
  --scenario codegeneration \
  --release_version release_v4 \
  --custom_output_file custom_outputs/qwen25_72b_release_v4_n10.json \
  --num_process_evaluate 4 \
  --timeout 20
```

---

## 10. 查看和计算最终分数

评分后会在 `custom_outputs/` 下生成类似文件：

```text
qwen25_72b_release_v4_n1_codegeneration_output.json
qwen25_72b_release_v4_n1_codegeneration_output_eval.json
qwen25_72b_release_v4_n1_codegeneration_output_eval_all.json
```

查看输出文件：

```bash
ls -lh custom_outputs/
```

使用 `compute_scores.py` 重新计算总分：

```bash
python -m lcb_runner.evaluation.compute_scores \
  --eval_all_file custom_outputs/qwen25_72b_release_v4_n1_codegeneration_output_eval_all.json
```

如果是 n=10：

```bash
python -m lcb_runner.evaluation.compute_scores \
  --eval_all_file custom_outputs/qwen25_72b_release_v4_n10_codegeneration_output_eval_all.json
```

记录终端输出中的 `pass@1`。

---

如果输出经常被截断，可以增大生成长度：

```bash
--max_tokens 4096
```

---

## 11. 一键命令汇总

进入项目：

```bash
cd ~/LiveCodeBench
source .venv/bin/activate
```

配置 API：

```bash
export SILICONFLOW_API_KEY="你的硅基流动API_KEY"
export SILICONFLOW_BASE_URL="https://api.siliconflow.cn/v1"
export SILICONFLOW_MODEL="Qwen/Qwen2.5-72B-Instruct"
```

生成结果：

```bash
python scripts/generate_siliconflow_lcb.py \
  --release_version release_v4 \
  --n 1 \
  --temperature 0.2 \
  --top_p 0.95 \
  --max_tokens 2000 \
  --sleep 1.0 \
  --output custom_outputs/qwen25_72b_release_v4_n1.json
```

评分：

```bash
python -m lcb_runner.runner.custom_evaluator \
  --scenario codegeneration \
  --release_version release_v4 \
  --custom_output_file custom_outputs/qwen25_72b_release_v4_n1.json \
  --num_process_evaluate 4 \
  --timeout 20
```

计算分数：

```bash
python -m lcb_runner.evaluation.compute_scores \
  --eval_all_file custom_outputs/qwen25_72b_release_v4_n1_codegeneration_output_eval_all.json
```
