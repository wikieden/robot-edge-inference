# AI Infra 扩展 · 机器人端侧推理

**在线阅读：<https://wikieden.github.io/robot-edge-inference/>** · [讲义目录](https://wikieden.github.io/robot-edge-inference/lessons/index.html) · [全部动画](https://wikieden.github.io/robot-edge-inference/animations/index.html) · [复习卡片](https://wikieden.github.io/robot-edge-inference/review.html) · [全部讲义书](https://wikieden.github.io/ai-books/)

> 8 章 · 8 个动画（GIF + 可交互页面）· 10 张静态图 · 16 张复习卡片 · 覆盖 VLA 在机器人机载算力（Jetson Orin / Thor）上部署的约束、选型、估算、量化、推理引擎、实时调度、功耗与端云分工

## 这本书讲什么

《深入理解 AI Infra》主要讲数据中心，端侧只在第 12 章讲了手机和个人电脑。这本扩展讲机器人：同一个 VLA 放到机器人身上，一次只有一个请求、必须准时、电和散热有限、网会断。从"机器人上的推理和云上有什么不同"讲起，一步步走到"给一个 3.3B 的 VLA 挑板子、算预算、定优化顺序、上车前检查什么"。

- **适合谁**：学过 Transformer 基础（q / k / v、多头注意力）、知道 VLA 大致是什么的人；带宽、算力、量化这些概念在用到的那一章现场讲。
- **读完能做什么**：拿到一个 VLA 和一块 Jetson，不跑代码先用几个数估出它最快多少 Hz、放不放得下、余量够不够，并知道按什么顺序优化、怎么验收。
- **怎么读**：按章顺序读。每章先看讲解和动画，再自己做练习，最后用复习卡片隔几天考自己。

## 讲解的特点

- **一次一小步**：每个概念按"白话类比 → 公式（每个符号说清楚怎么读）→ 小数字亲手算一遍"讲。
- **每章一个动画**：关键原理配可交互页面（▶ 播放、→ 单步、↺ 从头，带滑块），GIF 嵌在讲义里。
- **数字都有出处**：论文数字标本地文本行号（π0、OpenVLA、GR00T N1、SmolVLA、GR00T 2 白皮书），硬件参数来自 NVIDIA 官方页面（[附录 · 材料来源](https://wikieden.github.io/robot-edge-inference/lessons/appendix-sources.html)，2026-11-26 核对）；编的数都写明"编的"。
- **保留真实的学习过程**：练习与作答记录里是学习时的原话、对错和点评（目前练习都待作答）。
- **术语不设门槛**：缩写第一次出现就给英文全称并逐词解释，全书缩写见[缩写与术语表](https://wikieden.github.io/robot-edge-inference/lessons/appendix-glossary.html)。
- **每章都有代码对照**：纯 Python 把讲义里的数字算一遍，配测试核对和讲义一致；只算讲过的例子，不提前给练习答案。
- **每章收尾有口诀**：全部口诀汇总在本页末尾。

## 示例动画

| | | |
|---|---|---|
| ![](https://wikieden.github.io/robot-edge-inference/animations/01-robot-constraints.gif) | ![](https://wikieden.github.io/robot-edge-inference/animations/03-lower-bounds.gif) | ![](https://wikieden.github.io/robot-edge-inference/animations/06-realtime-scheduling.gif) |
| **第 1 章 控制节拍与推理时限**：控制 50 Hz，推理只要 2 Hz。[讲义](https://wikieden.github.io/robot-edge-inference/lessons/01-robot-constraints.html) · [▶ 交互](https://wikieden.github.io/robot-edge-inference/animations/01-robot-constraints.html) | **第 3 章 带宽下限**：OpenVLA 一步把 15 GB 读 7 遍。[讲义](https://wikieden.github.io/robot-edge-inference/lessons/03-lower-bounds.html) · [▶ 交互](https://wikieden.github.io/robot-edge-inference/animations/03-lower-bounds.html) | **第 6 章 同步与异步**：提前发起，动作不断档。[讲义](https://wikieden.github.io/robot-edge-inference/lessons/06-realtime-scheduling.html) · [▶ 交互](https://wikieden.github.io/robot-edge-inference/animations/06-realtime-scheduling.html) |
| ![](https://wikieden.github.io/robot-edge-inference/animations/04-quantization.gif) | ![](https://wikieden.github.io/robot-edge-inference/animations/05-inference-engines.gif) | ![](https://wikieden.github.io/robot-edge-inference/animations/08-case-study.gif) |
| **第 4 章 量化**：位数越少格子越粗。[讲义](https://wikieden.github.io/robot-edge-inference/lessons/04-quantization.html) · [▶ 交互](https://wikieden.github.io/robot-edge-inference/animations/04-quantization.html) | **第 5 章 推理引擎**：Thor 上 720 → 124 ms。[讲义](https://wikieden.github.io/robot-edge-inference/lessons/05-inference-engines.html) · [▶ 交互](https://wikieden.github.io/robot-edge-inference/animations/05-inference-engines.html) | **第 8 章 综合案例**：三块板子的下限和余量。[讲义](https://wikieden.github.io/robot-edge-inference/lessons/08-case-study.html) · [▶ 交互](https://wikieden.github.io/robot-edge-inference/animations/08-case-study.html) |

## 目录

| 章 | 主题 | 一句话精要 | 动画 | 卡片 | 状态 |
|---|---|---|---|---|---|
| [01](https://wikieden.github.io/robot-edge-inference/lessons/01-robot-constraints.html) | 机器人上的推理：和云上有什么不同 | 一次 1 个请求、必须准时；动作块把 2 Hz 推理接到 50 Hz 控制上 | [▶](https://wikieden.github.io/robot-edge-inference/animations/01-robot-constraints.html) | E01–E02 | 📝 已写，练习待作答 |
| [02](https://wikieden.github.io/robot-edge-inference/lessons/02-edge-chips.html) | 端侧芯片：看懂 Jetson 的三个数 | 统一内存先扣系统；TOPS 稀疏先除二再乘利用率 | [▶](https://wikieden.github.io/robot-edge-inference/animations/02-edge-chips.html) | E03–E04 | 📝 已写，练习待作答 |
| [03](https://wikieden.github.io/robot-edge-inference/lessons/03-lower-bounds.html) | 先算下限 | OpenVLA 在 AGX Orin 上最多 1.95 Hz；前缀算力卡、生成带宽卡 | [▶](https://wikieden.github.io/robot-edge-inference/animations/03-lower-bounds.html) | E05–E06 | 📝 已写，练习待作答 |
| [04](https://wikieden.github.io/robot-edge-inference/lessons/04-quantization.html) | 量化 | 位数减半字节减半；OpenVLA int8 变慢反而做坏 | [▶](https://wikieden.github.io/robot-edge-inference/animations/04-quantization.html) | E07–E08 | 📝 已写，练习待作答 |
| [05](https://wikieden.github.io/robot-edge-inference/lessons/05-inference-engines.html) | 推理引擎 | TensorRT 砍掉一半；GR00T 2 在 Thor 上 720 → 124 ms | [▶](https://wikieden.github.io/robot-edge-inference/animations/05-inference-engines.html) | E09–E10 | 📝 已写，练习待作答 |
| [06](https://wikieden.github.io/robot-edge-inference/lessons/06-realtime-scheduling.html) | 实时调度 | 异步 L ≤ g·H·Δt；新旧块用 RTC 接平；按 p99 留余量 | [▶](https://wikieden.github.io/robot-edge-inference/animations/06-realtime-scheduling.html) | E11–E12 | 📝 已写，练习待作答 |
| [07](https://wikieden.github.io/robot-edge-inference/lessons/07-power-and-cloud.html) | 功耗、散热和端云分工 | E = P·t；上云平均快、拖尾长；危险的留身上 | [▶](https://wikieden.github.io/robot-edge-inference/animations/07-power-and-cloud.html) | E13–E14 | 📝 已写，练习待作答 |
| [08](https://wikieden.github.io/robot-edge-inference/lessons/08-case-study.html) | 综合案例：π0 级 VLA 上车 | 余量 = 预算 ÷ 下限，不到 5 倍先优化；三条退路 | [▶](https://wikieden.github.io/robot-edge-inference/animations/08-case-study.html) | E15–E16 | 📝 已写，练习待作答 |

## 联系与合作

欢迎来信：<wikieden@gmail.com>。可以合作的方向：

- 讲义勘误与建议
- 课程 / 企业内训
- 内容合作与转载授权
- 赞助本系列持续更新

赞助请发邮件联系。

---

本仓库由私有学习仓库里的脚本 `tools/publish-transformer/build.py` 自动生成，内容摘自讲义目录，不要直接修改这里的文件。
