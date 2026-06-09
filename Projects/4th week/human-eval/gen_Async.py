import json
import asyncio
from human_eval.data import read_problems
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm_asyncio
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MY_API_KEY")

models = [
    "deepseek-ai/DeepSeek-V3",
    "Qwen/Qwen3-Coder-30B-A3B-Instruct",
    "zai-org/GLM-4.6",
]

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)
#为什么
problems = read_problems()


# ===== 限流（很重要）=====
semaphore = asyncio.Semaphore(10)


async def process_task(task_id, problem, model_name):
    async with semaphore:
        prompt = problem["prompt"] + "\n# Write the function body only."

        response = await client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt + "\nOnly complete the function. Do not include explanations."}
            ],
            temperature=0.3
        )

        completion = response.choices[0].message.content
        completion = completion.replace("```python", "").replace("```", "")

        return {
            "task_id": task_id,
            "completion": completion
        }


async def run_model(model_name):
    print(f"\n开始评测模型: {model_name}")

    tasks = [
        process_task(task_id, problem, model_name)
        for task_id, problem in problems.items()
    ]

    samples = await tqdm_asyncio.gather(*tasks)

    safe_model_name = model_name.replace("/", "_")
    output_file = f"samples_{safe_model_name}.jsonl"

    with open(output_file, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"{model_name} 生成完成 -> {output_file}")


async def main():
    for model_name in models:
        await run_model(model_name)

    print("\n所有模型评测完成")


if __name__ == "__main__":
    asyncio.run(main())