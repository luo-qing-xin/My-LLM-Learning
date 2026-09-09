<div align="center">
  <img src="./assets/images/title.png" width="720" alt="LLM 自学路线与实践记录">
</div>

# LLM 自学路线与实践记录

> From LLM fundamentals to hands-on projects.
> 一个面向 LLM 初学者的学习路线、实验记录与项目实践仓库。

[![License](https://img.shields.io/github/license/luo-qing-xin/my-LLM-learning)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/luo-qing-xin/my-LLM-learning)](https://github.com/luo-qing-xin/my-LLM-learning)
[![Last Commit](https://img.shields.io/github/last-commit/luo-qing-xin/my-LLM-learning)](https://github.com/luo-qing-xin/my-LLM-learning)
[![Issues](https://img.shields.io/github/issues/luo-qing-xin/my-LLM-learning)](https://github.com/luo-qing-xin/my-LLM-learning/issues)

## 为什么会有这个仓库？

大语言模型相关内容更新很快：Transformer、预训练、指令微调、Prompt Engineering、RAG、Agent、模型评测、部署与应用开发等主题相互交织。对于初学者来说，常见困难不是“没有资料”，而是资料过于分散：论文、课程、代码、API 文档和项目实践之间缺少一条清晰的学习路径。

这个仓库用来记录我学习 LLM 的全过程：从基础概念和经典论文开始，到 API 调用、Prompt 实验、小模型实践、模型评测，再到实际项目开发。它首先是我的个人学习档案，同时也希望逐渐沉淀成一份可复用、可复现、适合初学者参考的 LLM 自学路线。

目前仓库仍在持续建设中，内容会随着学习进度不断补充和调整。

## 这个仓库适合谁？

* 想系统入门大语言模型，但不知道从哪里开始的同学；
* 已经学过一点 Python / 机器学习，希望进一步理解 LLM 的同学；
* 想把论文、代码、API 调用和项目实践串起来学习的同学；
* 想参考一份真实学习过程记录，而不是只收藏资料链接的同学。

如果你已经熟悉大模型训练、分布式并行和模型部署，本仓库可能更适合作为入门资料整理方式的参考，而不是高级技术手册。

## 学习路线

| 阶段 | 主题                      | 学习目标                        | 阶段产出                          |
| -- | ----------------------- | --------------------------- | ----------------------------- |
| 01 | LLM 基础概念                | 建立对大语言模型整体技术路线的认识           | 技术路线图、核心模块总结                  |
| 02 | Transformer 与 Attention | 理解 Transformer 架构和注意力机制     | 论文精读、核心公式整理、代码复现              |
| 03 | LLM 核心技术模块              | 了解预训练、指令微调、对齐、RAG、Agent 等模块 | 模块笔记、概念对比、学习清单                |
| 04 | API 调用与参数实验             | 掌握 API 调用方式和关键参数影响          | 参数 case、实验记录、结果对比             |
| 05 | Prompt 分类实验             | 用 Prompt 完成简单分类任务并分析效果      | Iris 分类实验、Prompt 对比、准确率记录     |
| 06 | GPT-2 小模型实验             | 观察小模型在分类任务中的能力边界            | GPT-2 实验、与先进 LLM 的对比分析        |
| 07 | 模型评测                    | 学习如何用 benchmark 评估模型能力      | LiveCodeBench / Qwen API 评测记录 |
| 08 | 自选探索项目                  | 围绕感兴趣问题完成一次主动探索             | 数据集、模型、实验报告、复盘总结              |

## 推荐阅读顺序

建议按照下面的顺序使用这个仓库：

1. 先阅读 LLM 技术路线图，了解整个学习框架；
2. 再学习 Transformer 和 Attention，补齐模型结构基础；
3. 接着阅读 LLM 核心模块笔记，理解预训练、微调、对齐、RAG 和 Agent；
4. 然后完成 API 参数实验，观察不同参数对模型输出的影响；
5. 再做 Prompt 分类实验和 GPT-2 小模型实验，对比不同模型能力边界；
6. 最后进入模型评测和自选探索项目，把学习内容落到可复现的实验中。

## 仓库导航

| 模块              | 内容                         | 状态   | 入口               |
| --------------- | -------------------------- | ---- | ---------------- |
| Projects        | LLM 相关代码实践、实验项目和阶段任务       | 持续更新 | [进入](./Projects) |
| Notes           | 核心概念、论文精读、课程笔记             | 计划补充 | 待补充              |
| Resources       | 课程、论文、博客、工具和开源项目整理         | 计划补充 | 待补充              |
| Troubleshooting | 环境配置、依赖安装、API 使用和 Git 问题记录 | 计划补充 | 待补充              |
| Roadmap         | 阶段学习计划与任务清单                | 计划补充 | 待补充              |
| Naming Rules    | 文件、分支、提交等命名规范              | 已补充  | [查看](./命名规范.md)  |

> 如果某些入口暂时显示“待补充”，说明对应内容还在整理中。后续会随着学习进度逐步完善。

## 当前仓库结构

```text
my-LLM-learning/
├── Projects/              # LLM 相关代码实践与项目记录
├── README.md              # 仓库说明文档
├── LICENSE                # 开源协议
├── .gitignore             # Git 忽略规则
└── 命名规范.md             # 文件、分支、提交等命名规范
```

后续计划补充：

```text
my-LLM-learning/
├── Notes/                 # 学习笔记与论文精读
├── Resources/             # 学习资源整理
├── Troubleshooting/       # 踩坑记录
└── Roadmap.md             # 学习路线与阶段计划
```

## 内容规划

这个仓库后续会重点整理以下内容：

| 类型     | 内容说明                            | 目标               |
| ------ | ------------------------------- | ---------------- |
| 学习笔记   | LLM 基础概念、模型结构、训练方法和应用技术         | 帮助建立系统知识框架       |
| 论文精读   | Attention is All You Need 等经典论文 | 理解关键思想，而不是只记结论   |
| 代码实践   | Transformer、GPT-2、分类实验、模型评测等实践  | 把理论落实到可运行代码      |
| API 实验 | 参数设置、Prompt 格式、模型输出差异分析         | 理解 API 使用方式和输出规律 |
| 学习资源   | 课程、书籍、博客、开源项目和工具链接              | 减少资料搜索成本         |
| 踩坑记录   | 环境配置、依赖冲突、Git、API 调用等问题         | 保留可复现的问题和解决方法    |
| 阶段总结   | 每一阶段的学习收获、问题和后续计划               | 方便复盘和调整路线        |

## 维护原则

为了避免这个仓库变成简单的链接收藏夹，我会尽量遵循以下原则：

* 每个学习任务尽量说明：学什么、为什么学、怎么学、产出是什么；
* 每个实验尽量保留：任务描述、运行方式、关键代码、结果和分析；
* 每份笔记尽量区分：概念解释、公式推导、个人理解和易错点；
* 每条踩坑记录尽量包含：错误现象、原因分析、解决步骤和参考链接；
* 所有内容会随着学习进度持续修正，不保证一开始就是最终版本。

## 如何参与或反馈

这个仓库目前以个人学习记录为主。如果你发现内容中有错误，或者有更好的资料、课程、论文和实践项目推荐，欢迎通过 Issue 或 Pull Request 交流。

提交建议时，可以尽量说明：

* 你发现的问题是什么；
* 为什么需要修改；
* 推荐资料或修改内容的来源；
* 如果是代码问题，请尽量提供复现步骤。

## 更新日志

* 2026-01-29：仓库初始化，添加 README 与基础配置，添加 Projects 文档。
* 2026-06-10：添加命名规范文档，完善 Projects 及其内部文件夹命名。
* 2026-06-12：重构 README，调整为路线型学习仓库结构。

## 参考项目

本 README 的组织方式参考了 [PKUFlyingPig/cs-self-learning](https://github.com/PKUFlyingPig/cs-self-learning) 的项目说明结构：先说明项目动机，再给出使用入口、参与方式和许可说明。

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

本仓库整理、编写的原创内容遵循仓库开源协议；其中引用到的课程、论文、书籍、博客、开源项目等外部资料，版权和许可归原作者或原项目所有。
