## Task 1: Benchmark
在 HumanEval 基准上评测 DeepSeek 系列模型，与技术报告评测结果对齐


https://github.com/deepseek-ai/DeepSeek-V3?tab=readme-ov-file#4-evaluation-results

DeepSeek-V3 是一个 超大规模 MoE（Mixture-of-Experts，混合专家）语言模型,总参数量 671B，但每个 token 只激活 37B 参数，所以推理更高效,训练使用了 14.8 万亿 tokens
<img width="1108" height="396" alt="image" src="https://github.com/user-attachments/assets/ad5150c9-2301-4b43-b708-cb16570790a0" />
最初的v3版本在硅基流动上被下架了

```
models = [
    "deepseek-ai/DeepSeek-V3",
    "Qwen/Qwen3-Coder-30B-A3B-Instruct",
    "zai-org/GLM-4.6",
]
```
<img width="1105" height="299" alt="image" src="https://github.com/user-attachments/assets/793f8d3c-e29e-433c-a095-7fa28427dd50" />
<img width="994" height="657" alt="image" src="https://github.com/user-attachments/assets/97e51362-739a-4dd4-afac-32fcb0b0550d" />


而我使用的deepseek-ai/DeepSeek-V3是经过优化过的，所以正确率稍高应该正常
<img width="2129" height="274" alt="image" src="https://github.com/user-attachments/assets/110e2fd7-17e1-4bdf-9582-a062c27d7600" />


下面我要找一个经过humaneval测试（v3.2已经是livecodebench的测试集了）的大模型：
https://qwen.ai/blog?id=qwen2.5-llm
<img width="1519" height="737" alt="image" src="https://github.com/user-attachments/assets/eda68072-d1ef-4926-b556-050cfcce2e7c" />
<img width="2046" height="248" alt="image" src="https://github.com/user-attachments/assets/397eb5c6-d43b-43e8-938f-20767d1ab8ba" />

<img width="1509" height="699" alt="image" src="https://github.com/user-attachments/assets/4243fcae-34ea-432e-a493-9a93c9ae55e8" />
<img width="2060" height="256" alt="image" src="https://github.com/user-attachments/assets/45b1c466-0030-43d9-ac48-2a8fc651f408" />








