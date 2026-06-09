吕品正（me）  

[全文翻译](https://chat.deepseek.com/share/bngk595gw2mmcn51rt)

# [《LIVECODEBENCH》](https://openreview.net/forum?id=chfJJYC3iL )

## Abstract

#### 1. 问题背景
- 代码领域的大语言模型（LLMs）发展迅速  
- 现有评测基准（如 HUMANEVAL、MBPP）存在问题：
  - 数据污染（训练数据泄漏）
 
  LLM 是在海量且难以探查的语料库上训练的，当前的基准面临着数据污染的风险，因为训练数据可能包含这些基准样本。
  - 过拟合
  
   **过拟合Overfitting**是指：

模型在训练数据上表现很好，但在新数据（没见过的数据）上表现很差。

| 类型        | 特点          |
| --------- | ----------- |
| ✅ 正常（泛化好） | 学到规律，能处理新数据 |
| ❌ 过拟合     | 只记住训练数据     |
| ❌ 欠拟合     | 连训练数据都学不好   |


  - 难度饱和

  难度饱和指的是：

 一个评测数据集已经“太简单”，导致大多数模型都能轻松拿高分，无法区分它们的真实能力差异。
 
  - 仅评测代码生成（不全面）

#### 2. 方法概述
提出新的评测基准：
> **LIVECODEBENCH（LCB）**

##### 核心特点
- 持续从真实平台收集新题：
  - LeetCode
  - AtCoder
  - Codeforces
- 保证评测数据“未被模型见过”（避免污染）
- 覆盖多种代码能力，而非单一生成任务

#### 3. 数据规模
- 题目数量：600+
- 时间范围：2023.05 – 2024.08（我想现在应该还在更新）
- 属于目前规模最大的代码评测之一

#### 4. 评测创新

##### 4.1 时间切片评测
- 使用模型训练截止时间之后的数据进行测试  
- 用于检测数据污染问题

##### 4.2 多维能力评测
评测四种能力：
- Code Generation（代码生成）就是按题目，AI写代码
- Self-Repair（代码修复）就是debug
- Code Execution（代码执行）在脑子里跑一遍代码，自己推理答案
- Test Output Prediction（输出预测）给题目和输入值，自己推理出答案
- 
后两项统称为AI的颅内思考

#### 5. 实验与发现
- 评测了 50+ 大语言模型
- 关键发现：
  - 可以有效检测数据污染
  - 传统 benchmark 存在过拟合
  - 多维评测更真实反映模型能力

#### 6. 一句话总结

> Livecodebench是一个  **动态更新 + 无污染 + 多能力评测** 的新一代代码大模型评测基准。

---
![0b596d97d9bb8bf9c14cb77382306000](https://github.com/user-attachments/assets/0cf86230-50cf-4f8a-9e51-1eccb44c56d2)
![becdbad4e44cd43df9079ae3f6591c3d](https://github.com/user-attachments/assets/7f9cf444-50b0-4cd8-99d4-336d745c79cc)
![40265a89f4703c302c323dceff1a5a30](https://github.com/user-attachments/assets/c043e34d-5e50-4850-b08d-a92cc8521b05)
![aca9d13d69de6aef06bcb1833c4ac81e](https://github.com/user-attachments/assets/649f585e-1352-4ee5-9d3a-440097ad97cd)





## 1. Introduction
一些背景+构建这个数据集的原则+一些发现的综述

原则如下：
* 实时更新以防止污染
- Avoid contamination by using newly released problems
- Evaluate models only on post-cutoff data
* 全面评估
- Code generation
- Self-repair
- Code execution
- Test output prediction
* 高质量的问题和测试
通过实施启发式方法来检测和移除不适合基于输入输出自动评分的问题，提供了大量的测试用例。

- Carefully filtered
- Rich test cases (avg >18)
* 难度引导的问题筛选
- Avoid too-hard problems
- Maintain meaningful model comparison
---
## 2. Motivation
---
## 3. Benchmark Overview
从三个竞赛网站上选，LeetCode，AtCoder，Codeforces

* 数据收集：写了自动化的 HTML 爬虫，解析数学公式并排除包含图像的问题，排除了不适合通过输入输出示例评分的问题
  
* 评级将问题分类为 EASY、MEDIUM 和 HARD，以便进行更细粒度的模型比较，大致根据 HUMANEVAL 分数估算难度。
 
* 随时间推移滚动，根据模型发布时间来筛选问题
---

## 4. Evaluation Scenarios
模型:评估了 52 个不同规模的模型。从1.3B到70B（B表示模型的参数数量，十亿）

评估指标:
**使用pass@1指标**

我们使用温度为 0.2、top_p 为 0.95 的核采样

### 4.1 Code Generation
- Input: problem description
- Output: correct program
- 对于指令微调模型，我们使用零样本提示
- 基础模型使用单样本提示

### 4.2 Self-Repair
- Model fixes incorrect code using feedback，零样本提示

### 4.3 Code Execution
- Predict output of given code，使用少样本提示，有和没有思维链提示（什么叫做CoT？？）

### 4.4 Test Output Prediction
- Predict expected output from ，使用零样本提示，给定problem + input
---
## 5. Key Findings
### 5.1 Contamination Detection
- Performance drops after model cutoff dates
- Confirms training data leakage

- <img width="1127" height="807" alt="image" src="https://github.com/user-attachments/assets/3516b683-212e-412a-952a-fb1414991018" />


### 5.2 Holistic Capability Differences
- Models perform differently across tasks

### 5.3 HUMANEVAL Overfitting
- Some models perform well only on HUMANEVAL
- Poor generalization

### 5.4 Open vs Closed Models
- Closed models generally outperform
- Gap remains significant

---

## 6. Dataset Construction

### Data Collection
- Automated scraping
- Extract:
  - Problem statements
  - Test cases
  - Solutions

### Filtering
- Remove:
  - Multi-answer problems
  - Interactive tasks

---
##### 方法：1.我们根据带有发布日期的标签来评估模型在新问题上的表现
2.我们使用自我修复场景评估基于执行反馈的多轮编码能力（没太看懂？？）
3.高质量的问题和测试，测试样例不足，他们
#### 相关问题：
1. 什么是SQL
2. 用于压力测试解决方案？？hyw
4. 以进行鲁棒的对抗性测试for robust adversarial tests
