# Project Ledger — 项目台账追踪

## Overview

本 skill 用于读取和更新《清风渡》项目台账（`project-ledger.json`），跟踪 8 个阶段共 46 项任务的状态。与 `game-studio` skill 配套使用：开发前读台账了解当前进度，验收后更新台账标记完成。

## When to Use

- **开发前**：在使用 `game-studio` skill 进行任务开发前，先调用本 skill 读取台账，了解当前阶段、待办任务、依赖关系
- **验收后**：任务开发完成并通过验收后，调用本 skill 更新对应任务的 status、completed_date、deliverables
- **阶段切换**：当一个阶段所有任务完成时，更新 phase status 并切换 current_phase

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
2. **依赖检查**：更新任务状态前，检查其 dependencies 是否已全部 completed
3. **阶段切换**：只有当前阶段所有任务 completed 后，才切换 current_phase
4. **Git 提交**：建议每次更新台账后执行 `git add project-ledger.json && git commit -m "chore: 更新项目台账"`
