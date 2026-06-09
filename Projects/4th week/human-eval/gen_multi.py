import json
from human_eval.data import read_problems
from openai import OpenAI
from tqdm import tqdm
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

load_dotenv()
api_key = os.getenv("MY_API_KEY")

models = [
    "deepseek-ai/DeepSeek-V3",
    "Qwen/Qwen3-Coder-30B-A3B-Instruct",
    "zai-org/GLM-4.6",
]

client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

def clean_code(text):
    # 去 markdown
    text = re.sub(r"```.*?\n", "", text)
    text = text.replace("```", "")

    # 删除 import
    text = re.sub(r"^import .*?$", "", text, flags=re.M)
    text = re.sub(r"^from .*? import .*?$", "", text, flags=re.M)

    # 找函数
    lines = text.split("\n")
    func_start = None

    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            func_start = i
            break

    # 提取函数体
    if func_start is not None:
        body = []
        for line in lines[func_start + 1:]:
            if line.strip() == "":
                body.append("")
            else:
                body.append(line)
        text = "\n".join(body)
    else:
        text = text.strip()

    # 修复缩进（关键）
    fixed = []
    for line in text.split("\n"):
        line = line.replace("\t", "    ")
        if line.strip() == "":
            fixed.append("")
        else:
            if line.startswith(" "):
                fixed.append(line)
            else:
                fixed.append("    " + line)

    return "\n".join(fixed)


problems = read_problems()

def process_task(task_id, problem, model_name):
    prompt = problem["prompt"] + """

You must implement the function correctly so that it passes all test cases.

Requirements:
- Use correct logic based on the problem description.
- Do not return undefined variables.
- Do not leave the function incomplete.
- Only output the function body.
- Do not include explanations or markdown.

Think carefully before writing the code.

"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    completion = response.choices[0].message.content or ""
    completion = clean_code(completion)

    if task_id == "HumanEval/0":
        print("==== DEBUG SAMPLE ====")
        print(problem["prompt"] + completion)

    return {
        "task_id": task_id,
        "completion": completion
    }


for model_name in models:
    print(f"\n开始评测模型: {model_name}")

    samples = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(process_task, task_id, problem, model_name)
            for task_id, problem in problems.items()
        ]

        for future in tqdm(as_completed(futures), total=len(futures)):
            samples.append(future.result())

    safe_model_name = model_name.replace("/", "_")
    output_file = f"samples_{safe_model_name}.jsonl"

    with open(output_file, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"{model_name} 生成完成 -> {output_file}")

print("\n所有模型评测完成")