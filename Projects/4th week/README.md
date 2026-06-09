# Some tasks:
这次的任务从周一开始弄，并且抽空就搞，我就不信还弄不完...

下面这个任务，预计给大家两周时间完成，本周交流时不要求完成，但需要汇报进展:

## 掌握如何调用api来用现有大模型评测benchmark：

### 一、HumanEval Benchmark 简单介绍
HumanEval 是由 OpenAI 于 2021 年 7 月发布的代码生成能力评估基准，核心用途是客观衡量大型语言模型（LLM）从自然语言描述转换为可执行代码的能力，是目前代码生成模型评估的“行业标准”之一。其核心特点是聚焦“功能正确性”而非代码与参考示例的文本相似性，有 164 道人工精心设计的编程题目，每个题目有：
* 函数签名：包括task_id：任务唯一标识（如 HumanEval/0），用于区分 164 道不同题目，方便评估时定位具体任务及结果；
* docstring（题目描述）
* test（单元测试）：每道题平均包含 7.7 个手工设计的单元测试用例，用于验证生成代码的功能正确性，覆盖正常输入、边界情况、异常场景

模型需要生成函数代码，然后运行测试，看是否通过。最终指标一般是 **pass@k**（从模型生成的 k 个候选答案中，至少有 1 个是正确的概率。），例如 pass@1、pass@10

* 数据集：[humaneval: https://huggingface.co/datasets/openai/openai_humaneval ](https://huggingface.co/datasets/openai/openai_humaneval )
###  目标一：在github上找到现有的评测代码，根据这个代码配置相应的环境
#### 官方测评代码[openai/human-eval](https://github.com/openai/human-eval)
[相关步骤](https://chatgpt.com/s/t_69b2c65f15188191b75d6455784a45e8)

注意：
1. 在 HumanEval 评测中：temperature 必须 ≥ 0.8！
2. openai的excutation函数存在windows不兼容问题（setitimer）,必须去掉，否则测评怎么着都是0

本次代码的难度主要在于对于**propmt修改**和对于**大模型输出内容的处理**


### 目标二：掌握多线程/异步的方式调用api
#### (一) 多线程调用api:
之前是一个一个的串行，现在是同时实现

* [原理](https://chatgpt.com/s/t_69bd31a3956c819186d71b551361e618)

1. 线程池 = 控制并发数量
2. submit = 提交任务（不会阻塞）

3. Future = 未来结果占位符

4. as_completed = 谁快用谁（性能核心）

* [有关线程池](https://www.bilibili.com/video/BV1sk4y1P7UM/?spm_id_from=333.337.search-card.all.click&vd_source=216a5780cac38b7278f53c9432c4fe2c)
#### (二) 异步调用：
单线程，通过事件循环（event loop）切换任务，I/O 等待时不阻塞
1.  异步有专门的客户端初始化
2.  进行限流，通过限流器来进行
3. 异步任务函数
```
async def process_task(task_id, problem, model_name):
    async with semaphore:  # 获取限流令牌
        # ...
        response = await client.chat.completions.create(...)
        # await 表示"等待 API 响应，期间让出 CPU 给其他任务"
        completion = response.choices[0].message.content
        return {"task_id": task_id, "completion": completion}
        ```
流程图如下：
```
时间轴如下：
```
任务1: [API调用....... 等待......... 返回]
任务2:            [API调用....... 等待......... 返回]
任务3:                       [API调用....... 等待......... 返回]

任务10:                              [API调用....... 等待......... 返回]
任务11:                                          [API调用....... 等待......... 返回]
                    ↑
                  同时最多 10 个任务运行
```

### 目标三：将推理的结果以json或jsonl的格式存储 
存成 jsonl（JSON Lines）格式主要是为了方便处理大量样本、逐行读取、并符合 HumanEval 评测脚本的输入格式

### 目标四：评测至少三个大模型(或者改变temperature)
```
models = [
    "deepseek-ai/DeepSeek-V3",
    "Qwen/Qwen3-VL-32B-Thinking",
    "Pro/moonshotai/Kimi-K2.5",
]
```
这就是 benchmark 对比实验
