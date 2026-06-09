# 第二周的tasks
## --有关机器学习与大模型的三个小任务

## 具体任务列表

### 任务1：鸢尾花分类
博客地址：[手把手教你使用Pytorch训练自己的分类模型](https://blog.csdn.net/echoson/article/details/128130360?ops_request_misc=elastic_search_misc&request_id=05ff4476a37de76186deb627e0abf3b5&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-1-128130360-null-null.142^v102^pc_search_result_base1&utm_term=%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E4%BD%A0%E4%BD%BF%E7%94%A8Pytorch%E8%AE%AD%E7%BB%83%E8%87%AA%E5%B7%B1%E7%9A%84%E5%88%86%E7%B1%BB%E6%A8%A1%E5%9E%8B&spm=1018.2226.3001.4187)，当然，配合[视频](https://www.bilibili.com/video/BV13P411K7Dq/?spm_id_from=333.337.search-card.all.click&vd_source=216a5780cac38b7278f53c9432c4fe2c)食用效果更好
#### 任务要求
- 数据集来源：`from sklearn.datasets import load_iris`
- 技术栈：PyTorch
- 核心内容：
  1. 实现一个简单的线性层完成分类任务
  2. 自行调整超参数（学习率、批次大小、迭代次数、优化器等）
  3. 观察不同超参数下的模型表现并记录

### 任务2：手写数字识别
#### 任务要求
- 数据集来源：
  ```python
  from sklearn import datasets
  digits = datasets.load_digits()
- 技术栈：PyTorch + Attention 网络架构
- 核心内容:
 1. 实现基于 Attention 的手写数字识别模型
 2. 记录每一层、每个矩阵的维度变化
 3. 理解 Attention 机制在代码中的具体实现逻辑
 4. 尝试修改网络结构 / 参数，观察模型效果变化

### 任务 3：Attention 机制对比分析
#### 任务要求
1. 对比 GPT-2 的 Attention 实现代码与任务 2 中手写数字识别的 Attention 实现
2. 分析两者的异同点（结构、维度、计算逻辑、应用场景等）

## 任务说明
本系列任务旨在帮助入门者建立对机器学习和大模型的直观认知，重点不在于代码怎么去写，而在于通过调整参数、修改代码、观察结果，形成对人工智能的直觉与把握，激发探索兴趣并产生自己的见解。

**核心原则**：
- 代码可借助大模型生成，但需逐行理解逻辑
- 鼓励修改代码中的参数/语句，"玩起来"才是关键
- 完成基础任务后，务必进行发散探索并记录思考
