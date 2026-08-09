---
name: project-ledger
description: "项目台账追踪 — 读取/更新《清风渡》project-ledger.json（8 阶段 46 任务）。与 game-studio skill 强耦合：开发前读台账了解当前阶段与待办任务，验收后更新任务状态/完成日期/产出物/阶段进度；另提供每日简报（进度一句话+下一个就绪任务+阶段可视化）。触发词：项目台账、读取台账、更新台账、任务进度、阶段进度、验收完成、game-studio 配套、每日简报、今天进度、项目状态、进度概览、今日要做什么、daily briefing。"
agent_created: true
---

# Project Ledger — 项目台账追踪

## Overview

本 skill 用于读取和更新《清风渡》项目台账（`project-ledger.json`），跟踪 8 个阶段共 46 项任务的状态。与 `game-studio` skill **强耦合**：开发前读台账了解当前进度，验收后更新台账标记完成。两者必须配套使用，缺一不可。

## When to Use

- **开发前**：在使用 `game-studio` skill 进行任务开发前，先调用本 skill 读取台账，了解当前阶段、待办任务、依赖关系
- **验收后**：任务开发完成并通过验收后，调用本 skill 更新对应任务的 status、completed_date、deliverables
- **阶段切换**：当一个阶段所有任务完成时，更新 phase status 并切换 current_phase
- **每日简报**：当用户说“每日简报”“项目简报”“今日进度”或同义表达时，读取实时台账并按本 skill 的「每日简报」格式汇报

## 每日简报

### 触发与数据来源

当用户请求每日简报时，**必须先读取** `{workspace}/project-ledger.json`，不得沿用对话中的旧进度或猜测数据。简报仅汇报台账已记录的事实；不会修改任务状态。

### 下一任务推荐规则

按以下优先级自动选择一项“最适合做的任务”：

1. 当前阶段中 `in_progress` 的任务（优先推动已启动事项闭环）
2. 当前阶段中 `not_started` 且所有 `dependencies` 均为 `completed` 的任务
3. 若当前阶段没有可启动任务，选择后续阶段中依赖全部完成、且阶段序号最小的任务
4. 若没有可启动任务，明确说明项目被阻塞，并列出阻塞链中最靠前的未完成任务

同一优先级有多项时，按 `task_id` 升序选择；若任务 `notes` 明示需要并行推进，可在“可并行事项”中补充列出，但每日简报只推荐一个主任务。

### 固定输出格式

每日简报必须使用以下四部分，保持简洁、可扫读：

```markdown
## 每日简报 · YYYY-MM-DD

**一句话进度：** 当前位于 P{n}「阶段名」，已完成 X/Y 项任务（Z%）；当前重点是「当前阶段或进行中任务」。

**总体进度：** [████░░░░░░░░░░░░░░░░] Z%（X/Y）

### 下一步建议
**P?-T? · 任务名称**
- 为什么现在做：依赖状态与优先级说明
- 简要描述：引用/提炼该任务 `notes`
- 预期产出：列出 `deliverables`

### 项目位置
✅ P0 阶段名（完成/验收）
▶ P1 阶段名（当前 · 已完成 a/b）
○ P2 阶段名（未开始）
○ P3 阶段名（未开始）
...

**里程碑：** ○ M1 名称（W?） → ○ M2 名称（W?） → ○ M3 名称（W?） → ○ M4 名称（W?）
```

### 可视化规则

- 任务条固定为 **20 格**：`█` = 已完成比例、`░` = 剩余比例；使用四舍五入计算已填充格数，至少保留 0 格、最多 20 格
- 阶段位置图：`✅` = phase.status 为 `completed`，`▶` = `project.current_phase`，`⏸` = `blocked`，`○` = `not_started`；若当前阶段为 `in_progress`，必须显示完成数 `已完成 a/b`
- 里程碑：`✅` = completed，`▶` = 当前阶段关联的 milestone，`○` = not_started，`⏸` = blocked
- 若没有完成阶段，不得虚称“阶段验收完成”；只有 `phase.status: completed` 才显示 `✅`
- “下一步建议”若因依赖未就绪不能启动，必须明确标注 `⏸ 暂不可启动` 并展示缺失依赖；不得把被拦截的任务包装为可执行建议

## How to Use

### 1. 读取台账

读取工作目录下的 `project-ledger.json` 文件。关注以下字段：

- `project.current_phase` — 当前所处阶段（P0-P7）
- `summary` — 全局进度统计（总任务/已完成/进行中/未开始）
- `phases[]` — 按阶段分组的任务列表
- 每个 task 含 `task_id` / `task_name` / `owner` / `status` / `deliverables` / `dependencies`

读取后，向用户简要汇报：
- 当前阶段名称与进度
- 该阶段有哪些任务待开始 / 进行中 / 已完成
- 下一步应该做什么任务

**启动任务前的依赖校验（强制拦截）**：在用户选定要启动的任务后、正式开工前，**必须**校验该任务的 `dependencies` 是否已全部 `completed`：

- ✅ **依赖全部 `completed`** → 允许启动。将任务 `status` 改为 `in_progress`，更新 `project.last_updated`，向用户确认开始并说明预期产出物
- ❌ **存在未完成的依赖** → **拦截，不启动**。向用户报告：
  - 列出未完成的依赖（`task_id` + 当前 `status` + `task_name`）
  - 建议先推进哪些前置任务
  - **仅当用户明确确认要并行/提前启动**（例如美术验证与引擎验证实际无强依赖）时，方可将 `status` 改为 `in_progress`，并在 `notes` 标注"依赖未完成，用户确认并行启动"

> 这是硬性拦截点：依赖未就绪的任务默认不应启动，避免做了白功或产出无法集成。

### 2. 更新台账

任务完成后，使用 Edit 工具修改 `project-ledger.json`：

**更新任务状态**：
```json
{
  "task_id": "P1-T2",
  "status": "completed",
  "completed_date": "2026-08-10",
  "deliverables": ["scenes/001_rain.scene.md", ...]
}
```

将 `"status"` 从 `"not_started"` 改为 `"completed"`（或 `"in_progress"` / `"blocked"`），并填写 `completed_date`。

**更新阶段状态**：
当某阶段所有任务均为 `completed` 时，将该 phase 的 `status` 改为 `completed`，并将 `project.current_phase` 更新为下一阶段。

**更新汇总**：
每次更新后重新计算 `summary` 中的计数和百分比：
```json
{
  "total_tasks": 46,
  "completed": 3,
  "in_progress": 1,
  "not_started": 42,
  "blocked": 0,
  "overall_progress": "6.5%"
}
```

**更新时间戳**：
将 `project.last_updated` 更新为当前时间。

### 3. 状态值定义

| status | 含义 | 何时使用 |
|--------|------|----------|
| `not_started` | 未开始 | 任务尚未启动 |
| `in_progress` | 进行中 | 正在开发中 |
| `completed` | 已完成 | 任务完成且通过验收 |
| `blocked` | 阻塞 | 因依赖未完成或发现问题无法推进 |

### 4. 与 game-studio 的协作流程

```
用户调用 game-studio → game-studio 激活角色
    ↓
本 skill 读取 project-ledger.json
    ↓
汇报当前阶段 + 待办任务
    ↓
game-studio 按角色执行任务
    ↓
任务完成 → 验收
    ↓
本 skill 更新 project-ledger.json
    ↓
提交 git（可选）
```

### 5. 台账文件位置

- **台账文件**：`{workspace}/project-ledger.json`（项目根目录）
- **本 skill**：`~/.workbuddy/skills/project-ledger/SKILL.md`（用户级）
- **项目内副本**：`{workspace}/skills/project-ledger/SKILL.md`（随 git 提交）

## 台账结构概览

```
project-ledger.json
├── project          # 项目元信息（名称/引擎/周期/当前阶段/更新时间）
├── summary          # 全局统计（总任务/已完成/进度百分比）
├── milestones[]     # 4 个里程碑（MVP/内测/Demo/发布）
└── phases[]         # 8 个阶段
    └── tasks[]      # 每阶段 3-10 个任务
        ├── task_id      # P0-T1 格式
        ├── task_name    # 任务名称
        ├── owner        # 负责角色
        ├── status       # not_started/in_progress/completed/blocked
        ├── deliverables # 产出物文件列表
        ├── dependencies # 前置任务 ID 列表
        └── notes        # 备注
```

## 注意事项

1. **不要删除任务**：即使任务取消，也改为 `blocked` 并在 notes 说明原因
2. **依赖检查（两层）**：
   - **启动前拦截**：开始一个任务前，校验其 `dependencies` 是否全部 `completed`；未完成则拦截（见上文「启动任务前的依赖校验」）
   - **验收前复核**：标记任务 `completed` 前，再次确认其 `dependencies` 全部 `completed`，并核对所有 `deliverables` 已实际产出
3. **阶段切换**：只有当前阶段所有任务 completed 后，才切换 current_phase
4. **Git 提交**：建议每次更新台账后执行 `git add project-ledger.json && git commit -m "chore: 更新项目台账"`
