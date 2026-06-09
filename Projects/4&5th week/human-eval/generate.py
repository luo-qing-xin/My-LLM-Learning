import json
from human_eval.data import read_problems
from openai import OpenAI
from tqdm import tqdm  #.auto

import os
from dotenv import load_dotenv
load_dotenv() # 加载 .env 文件中的环境变量
api_key = os.getenv("MY_API_KEY")

# ===== 在这里修改要评测的模型 =====
models = [
    "deepseek-ai/DeepSeek-V3",
    "Qwen/Qwen3-Coder-30B-A3B-Instruct",
    "zai-org/GLM-4.6",
]

client = OpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)


problems = read_problems() 
''' 
读取 HumanEval 题目,这个函数来自： human_eval.data 模块
数据结构类似于：
{
 "HumanEval/0": {
    "prompt": "def add(a, b): ..."
 },
 "HumanEval/1": {...}
}
'''

# ===== 小规模测试 =====
#problems = dict(list(problems.items())[:10]) #到时候可以直接注释掉这一行，评测全部问题

# ===== 逐个模型评测 =====
for model_name in models:

    print(f"\n开始评测模型: {model_name}")

    samples = []

    for task_id, problem in tqdm(problems.items()):


        prompt = problem["prompt"] + "\n# Write the function body only."

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt + "\nOnly complete the function. Do not include explanations."}
            ],
            temperature=0.8
        )

        completion = response.choices[0].message.content
        completion = completion.replace("```python", "").replace("```", "")
        '''
        防止模型返回：

        ```python
        def solution():
        '''

        samples.append({
            "task_id": task_id,
            "completion": completion
        })

    # 文件名根据模型自动生成
    safe_model_name = model_name.replace("/", "_")
    output_file = f"samples_{safe_model_name}.jsonl"

    with open(output_file, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"{model_name} 生成完成 -> {output_file}")

print("\n所有模型评测完成")



'''import json
from human_eval.data import read_problems
from openai import OpenAI
from tqdm import tqdm

client = OpenAI(
    api_key="sk-olcrkbxpwgseittqcnsqhokycublteikefzvehwhnjyslzma",
    base_url="https://api.siliconflow.cn/v1"
)

problems = read_problems()

samples = []

for task_id, problem in tqdm(problems.items()):

    prompt = problem["prompt"]

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    completion = response.choices[0].message.content

    samples.append({
        "task_id": task_id,
        "completion": completion
    })

with open("samples.jsonl", "w") as f:
    for s in samples:
        f.write(json.dumps(s) + "\n")
print("生成完成")'''