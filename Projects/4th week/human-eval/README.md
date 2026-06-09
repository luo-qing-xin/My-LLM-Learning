# LLM Code Generation Evaluation (HumanEval Benchmark)

本项目基于 [HumanEval](https://github.com/openai/human-eval) 数据集，对多个大语言模型（LLMs）的代码生成能力进行自动化评测，支持 **多线程 / 异步 / 多样本生成**，并输出标准 `pass@k` 指标。

## （一）Project Structure

```
.
├── generate.py        # 单线程生成（基础版）
├── gen_multi.py       # 多线程生成
├── gen10_multi.py     # 多样本生成（pass@k）
├── gen_Async.py       # 异步高性能生成 ⭐
├── run_eval.py        # 自动评测             
├── test_dataset.py    # 数据集测试
├── requirements.txt
├── setup.py
└── README.md
```

---
##  （二）各个代码的功能

### `generate.py`
- 单线程逐题生成
- 易调试但速度慢

### `gen_multi.py`
- 多线程并发生成
- 自动清洗代码输出
- 性能与稳定性平衡

### `gen10_multi.py`
- 每题生成多个候选答案（默认10个）
- 用于计算 pass@k

### `gen_Async.py` ⭐
- asyncio 异步高并发
- 支持限流（Semaphore）
- 大规模评测推荐

### `run_eval.py`
- 自动评测所有 `samples_*.jsonl`
- 输出 pass@k 指标

### `test_dataset.py`
- 验证数据集加载是否正确

---


## （三）Usage

### 1.1️⃣ 生成代码

#### ✅ 基础版本（单线程）

```bash
python generate.py
```

#### ⚡ 多线程版本（推荐）

```bash
python gen_multi.py
```

#### 🚀 异步高性能版本（强烈推荐）

```bash
python gen_Async.py
```

#### 🎯 多样本生成（用于 pass@k）

```bash
python gen10_multi.py
```

---

### 2️⃣ 运行评测

```bash
python run_eval.py
```

输出示例：

```
samples_xxx.jsonl 结果:
{'pass@1': 0.35, 'pass@10': 0.62, 'pass@100': 0.78}
```

---

### 2.📊 Output Format

所有生成结果均为标准 JSONL：

```json
{"task_id": "HumanEval/0", "completion": "code here"}
```

---



### 3.🔁 Workflow

```
Generate Code
   ↓
samples_xxx.jsonl
   ↓
run_eval.py
   ↓
pass@k metrics
```
有可能参考到的论文
- HumanEval Paper:  
  *Evaluating Large Language Models Trained on Code*
---


