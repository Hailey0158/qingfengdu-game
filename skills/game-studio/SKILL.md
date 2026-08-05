---
name: game-studio
description: "TextAdventure Game Studio — 文字冒险游戏开发工作室。当用户想要创建、开发、设计文字冒险游戏（如橙光式互动阅读小说、AVG、视觉小说）时使用本 skill。触发词包括：文字冒险、互动小说、橙光、AVG、视觉小说、文字游戏、分支叙事、多结局游戏、游戏开发、游戏设计。本 skill 提供完整的 12 角色 4 层开发工作室框架，含角色定义、工作流程、交付物规格和 Agent 调度约定。"
agent_created: true
---

# TextAdventure Game Studio — 文字冒险游戏开发工作室

## Overview

本 skill 将 WorkBuddy 转换为一个完整的文字冒险游戏开发工作室，支持从概念构思到最终发布的完整开发流程。适用于橙光式互动阅读、视觉小说、分支叙事游戏等类型。

## When to Use

当用户表达以下意图时激活本 skill：

- "帮我做一个文字冒险游戏"
- "我想创建一个橙光风格的游戏"
- "写一个互动小说"
- "设计一个多结局的视觉小说"
- "开发一个分支叙事的 AVG 游戏"

## How to Use

### 1. Load the Studio Specification

首先读取完整的 GameStudio 规范文件以了解所有角色和流程：

```
references/game-studio.md
```

该文件定义了 12 个角色、4 层架构、7 个开发阶段、所有交付物规格和 Agent 调度约定。

### 2. Understand the Role Architecture

工作室采用 **"1 + 3 + 6 + 2"** 四层结构：

| 层级 | 角色 | 职责 |
|------|------|------|
| L1 统筹层 | 制作人 (Producer) | 项目规划、任务分派、最终验收 |
| L2 总监层 | 产品设计总监、美术总监、技术总监 | 分领域评审方案、收口质量 |
| L3 执行层 | 剧情设计、角色设定、分支逻辑、UI交互、音频设计、系统工程 | 核心创意设计与技术实现 |
| L4 产出层 | 文案润色、测试工程 | 文本打磨与质量验证 |

### 3. Follow the Development Pipeline

严格按照 7 阶段流程推进，不可跳过：

- **阶段 0 — 立项**：制作人解析用户需求，输出 `project-brief.md` 和 `task-board.md`
- **阶段 1 — 双轨并行设计**：产品设计线（世界观+角色）+ 技术线（技术架构）并行
- **阶段 2 — 场景脚本编写**：剧情设计师主导，编写所有场景脚本
- **阶段 3 — 分支树构建**：分支逻辑工程师设计选择点、状态机、多结局
- **阶段 4 — 四路并行产出**：UI交互、音频设计、存档系统、文案润色同时进行
- **阶段 5 — 技术集成**：系统工程师组装所有资产为可运行游戏
- **阶段 6 — 集成测试**：测试工程师全面验证
- **阶段 7 — 缺陷修复与验收**：制作人闭环管理至发布

### 4. Role Switching

在开发过程中，需要根据当前阶段切换角色身份。每个角色有明确的：

- **使命**：该角色的核心目标
- **输入**：需要什么前置交付物
- **输出**：需要产出的交付物及其格式
- **核心职责**：具体要完成的任务列表
- **协作关系**：与上下游角色的交互方向

角色切换时，声明当前角色标识（如 `[Producer]`），按照该角色的职责和交付规格执行，完成后交给下一个角色。

### 5. Key Design Principles

在开发过程中始终遵循以下原则：

1. **选择有重量**：每个玩家选择必须有可见后果
2. **角色驱动剧情**：剧情因角色性格产生冲突
3. **状态可追溯**：分支状态变更可回溯
4. **文本可独立**：台词/旁白与逻辑解耦
5. **测试先行**：设计阶段即输出测试路径
6. **音频服务叙事**：BGM/SFX 服务场景氛围
7. **关键决策前存档**：避免玩家进度丢失
8. **总监收口制**：执行层产出经总监评审通过方可流转

### 6. Deliverable Format Standards

所有交付物严格遵循规范中定义的格式标准。关键格式示例：

- **场景脚本** (`scenes/*.scene.md`)：`scene_id` / `location` / `characters` / `narration` / `choices[]` / `next_scene` / `plot_tags[]` / `mood_tag`
- **角色档案** (`character-profiles.json`)：`char_id` / `name` / `age` / `personality_tags[]` / `background` / `motivation` / `speech_style` / `arc_stages[]` / `relationships[]`
- **分支树** (`branch-tree.json`)：`node_id` / `scene_ref` / `choices[]` / `save_point`
- **最终台词** (`final-dialogue/*.json`)：`dialogue_id` / `scene_ref` / `speaker` / `text` / `emotion_tag` / `branch_path`

完整交付物规格参考 `references/game-studio.md` 第五章。

## Resources

### references/game-studio.md

完整的 GameStudio 规范文件，包含：
- 12 个角色的详细定义（使命、输入、输出、职责、协作关系）
- 4 层架构和协作关系矩阵
- 7 个开发阶段的完整工作流
- 27 个交付物的格式规格
- 8 条关键设计原则
- Agent 调度约定

当需要了解某个角色的具体职责、交付格式或协作关系时，读取此文件对应章节。
