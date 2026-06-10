# Week 02:

本周的主要目标是通过三个入门小任务，初步建立对机器学习训练流程、PyTorch 基本写法、Attention 机制以及大模型 Attention 代码结构的直观认识。

本周任务的重点不在于“把代码写完”，而在于通过运行、修改、调参、观察和记录，真正看懂模型在做什么，逐步形成对人工智能模型的直觉与判断。

---

## 一、Goals

通过第二周的学习，需要完成以下目标：

1. 使用 PyTorch 完成一个简单的鸢尾花分类任务，理解线性层、损失函数、优化器和训练循环的基本作用；
2. 使用 PyTorch 实现一个基于 Attention 的手写数字识别模型，记录每一层和关键矩阵的维度变化；
3. 对比手写数字识别中的 Attention 实现与 GPT-2 中的 Attention 实现，理解二者在结构、维度、计算逻辑和应用场景上的异同；
4. 尝试主动修改代码中的参数、层数、维度或训练设置，观察模型表现的变化；
5. 记录自己看懂的部分、没有看懂的部分，以及进一步想探索的问题。

---

## 二、Task List

### 1. 鸢尾花分类任务

**任务内容：**

使用 `sklearn.datasets.load_iris` 加载鸢尾花数据集，并使用 PyTorch 写一个简单的线性分类模型。

**数据集来源：**

```python
from sklearn.datasets import load_iris
```

**参考资料：**

暂无（后续会继续补充）

**重点关注：**

* 鸢尾花数据集中输入特征和标签分别是什么；
* `nn.Linear` 的输入维度和输出维度为什么这样设置；
* 训练循环中 `forward`、`loss`、`backward`、`optimizer.step()` 分别做了什么；
* 学习率、批次大小、训练轮数、优化器等超参数如何影响训练效果；
* 训练集和测试集准确率是否一致，是否存在过拟合或欠拟合现象。

**任务要求：**

1. 使用 PyTorch 实现一个简单线性层完成分类任务；
2. 自行调整一些超参数，例如：
   * learning rate；
   * batch size；
   * epoch；
   * optimizer；
   * train/test split；
3. 记录不同设置下的 loss 和 accuracy 变化；
4. 尝试解释为什么某些设置效果更好或更差。

**产出要求：**

* 一份可以运行的鸢尾花分类代码；
* 一份超参数实验记录；
* 一份简短实验总结，说明自己观察到的现象。

**可记录内容示例：**

```text
实验 1：
learning_rate = 0.01
batch_size = 16
epoch = 100
optimizer = SGD

结果：
train accuracy = ...
test accuracy = ...

观察：
- loss 是否稳定下降；
- accuracy 是否明显提升；
- 学习率是否过大或过小；
- 模型是否出现过拟合。
```

---

### 2. 手写数字识别任务

**任务内容：**

使用 `sklearn.datasets.load_digits()` 加载手写数字数据集，并使用 PyTorch 实现一个基于 Attention 的分类模型。

**数据集来源：**

```python
from sklearn import datasets

digits = datasets.load_digits()
```

**技术栈：**

* PyTorch；
* Attention 网络架构；
* sklearn digits 数据集。

**重点关注：**

* `digits.data` 和 `digits.images` 的维度分别是什么；
* 一张 8×8 的手写数字图片如何被送入模型；
* Attention 中的 `Q`、`K`、`V` 分别是如何计算出来的；
* Attention score 的矩阵维度为什么是这样；
* Softmax 在 Attention 中起什么作用；
* Attention 输出如何进一步用于分类。

**任务要求：**

1. 实现一个基于 Attention 的手写数字识别模型；
2. 记录每一层、每个关键矩阵的维度变化；
3. 看懂代码中每一步在做什么，而不是只运行成功；
4. 尝试修改模型结构或训练参数，观察模型效果变化；
5. 对看不懂的代码、维度变化或训练现象进行记录，并在群里或会议中交流。

**建议重点记录的维度：**

以一种常见实现方式为例，可以将 8×8 图像看成若干个 token，再送入 Attention 模块。实际维度可能因自己的实现方式不同而变化。

| 位置 | 含义 | 示例维度 |
|---|---|---|
| 原始图片 | 一张 8×8 手写数字图像 | `[8, 8]` |
| batch 输入 | 一个 batch 的图片 | `[batch_size, 8, 8]` |
| token 表示 | 将图片拆成 token 后的输入 | `[batch_size, seq_len, input_dim]` |
| Q 矩阵 | Query | `[batch_size, seq_len, hidden_dim]` |
| K 矩阵 | Key | `[batch_size, seq_len, hidden_dim]` |
| V 矩阵 | Value | `[batch_size, seq_len, hidden_dim]` |
| Attention score | Q 和 K 相乘后的注意力分数 | `[batch_size, seq_len, seq_len]` |
| Attention output | 加权求和后的输出 | `[batch_size, seq_len, hidden_dim]` |
| 分类输出 | 10 个数字类别的 logits | `[batch_size, 10]` |

**产出要求：**

* 一份可以运行的*手写数字*识别代码；
* 一份模型结构说明；
* 一份维度变化记录表；
* 一份调参或改结构后的观察记录。

**可记录内容示例：**

```text
输入维度：
x.shape = ...

经过 Linear 得到 Q/K/V：
Q.shape = ...
K.shape = ...
V.shape = ...

Attention score：
score.shape = ...

输出分类结果：
logits.shape = ...

观察：
- seq_len 改变后，Attention score 的维度如何变化；
- hidden_dim 改变后，模型参数量和准确率是否变化；
- batch_size 改变后，训练速度和稳定性是否变化。
```

---

### 3. Attention 机制对比分析

**任务内容：**

对比 GPT-2 的 Attention 实现代码和任务 2 中手写数字识别的 Attention 实现，分析二者的异同。

**重点关注：**

* 二者是否都使用了 `Q`、`K`、`V`；
* 二者的输入数据有什么不同；
* 手写数字识别中的 Attention 是如何用于图像分类的；
* GPT-2 中的 Attention 是如何用于语言建模和文本生成的；
* GPT-2 为什么需要 causal mask；
* Multi-Head Attention 相比单头 Attention 有什么作用；
* GPT-2 的 Attention 为什么还需要和残差连接、LayerNorm、MLP 等模块配合使用。

**任务要求：**

1. 找到 GPT-2 中 Attention 的相关实现代码；
2. 阅读其中和 `Q`、`K`、`V`、mask、softmax、head split / merge 有关的部分；
3. 和自己在任务 2 中写的 Attention 代码进行对比；
4. 总结二者至少 3 个相同点和 3 个不同点；
5. 写出自己目前对 Attention 的理解，以及仍然不理解的问题。

**建议对比角度：**

| 对比角度 | 手写数字识别 Attention | GPT-2 Attention |
|---|---|---|
| 输入对象 | 8×8 手写数字图像或图像 token | 文本 token 序列 |
| 任务目标 | 图像分类 | 下一个 token 预测 |
| Attention 类型 | 可以是普通 self-attention | causal self-attention |
| 是否需要 mask | 通常不一定需要 | 需要 causal mask，防止看到未来 token |
| 输出结果 | 分类 logits | 每个位置的 hidden states，再用于预测词表分布 |
| 复杂度重点 | 帮助理解 Attention 基本计算 | 更接近真实大语言模型结构 |

**产出要求：**

* 一份 GPT-2 Attention 代码阅读笔记；
* 一份数字识别 Attention 与 GPT-2 Attention 的对比表；



---

## 三、Learning Notes

本周任务不是传统意义上的作业，而是一次入门探索。代码可以借助大模型生成，但需要尽量做到：

1. 知道每一行关键代码的作用；
2. 知道每个 tensor 的维度为什么这样变化；
3. 能主动修改参数或语句并观察结果；
4. 能说出模型效果变化背后的可能原因；
5. 能提出自己没看懂的问题；
6. 能从小模型实验逐步联想到大模型的核心思想。

完成基础任务后，可以进一步思考：

* 为什么一个简单线性层就能完成鸢尾花分类；
* Attention 是否真的适合手写数字识别这个小数据集；
* Attention 和普通 MLP、CNN 相比有什么优势和劣势；
* GPT-2 的 Attention 为什么要限制模型只能看前面的 token；
* 小任务中的 Attention 和真实大模型中的 Attention 差距在哪里；
* 如果要把这个任务做得更有研究性，还可以从哪些方向继续探索。
