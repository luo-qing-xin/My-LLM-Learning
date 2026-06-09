# Some Tasks：
## Task 1: Benchmark
在 HumanEval 基准上评测一个模型，与该模型的技术报告评测结果对齐一致

## Task 2: Paper Reading
读一篇论文并分享
要求：2025年1月之后，关键词：LLM，benchmark，basketball，video

读一读审稿人意见和作者回复

用文档或者PPT记录，一句话总结、研究背景和动机、研究方法、实验结果、价值和局限性

## Task 3: Data Collection
#### 目标一：自动化下载豆瓣读书2025年度榜单里的所有图书，并获取对应的详细信息，以jsonl文件形式保存到本地
#### 目标二：自动化下载三个网站来源的篮球比赛视频



谢秉奇       https://arxiv.org/pdf/2107.03374



[CSDN论文精读](https://blog.csdn.net/heroding23/article/details/133189960?

1. 真实场景下代码都是不断迭代debug的结果
2. <img width="1185" height="855" alt="image" src="https://github.com/user-attachments/assets/aa142575-9fd7-4bb1-b546-84d4b73fa4fc" />
3. 作者的代码lexer基于GPT-3文本的tokenizer实现。但是由于代码和文本分布不同，tokenizer并不高效，最大的根源来自于空格和空行，为此作者加入了额外的token集用于表示不同长度的空白，这使得作者能够少用30%的token来表示代码。

4. p值设为0.95。这是什么？？


5. *上图展示的是排序算法的性能，即允许模型生成k的答案，只是根据不同的策略和指标挑选最好的结果进行单元测试，Oracle虽然是最好的策略，但是在现实中，你不可能对每个方案都进行一次测试。因此相对比较合理的方案是对任何一个解，去看每个候选token在softmax中的概率取log算均值，将均值最高的选择出来相对性能较好*。没看懂

6. 用于Codex的监督微调，什么叫做监督微调？？
7. 作者构建环境让代码在沙盒中进行集成测试。？？hyw
8. 现在有一个观点是在大模型的更新迭代前少进行微调，先吃尽版本更新的红利。
9. 因为这些代码看起来会更加准确，用户难以识别出错误，可实际上已经做了有害的事情。，**这说明大模型也会出错！！！**

邱子路            [《Program Synthesis with Large Language Models》](https://arxiv.org/abs/2108.07732)

1. 什么叫做微调fine-tuning？？
2. 什么叫代码上的机器学习 

[论文摘要](https://zhuanlan.zhihu.com/p/1931417730176747302)

