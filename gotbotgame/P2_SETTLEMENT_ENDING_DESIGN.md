# P2 结算页 · 走水夜 · 结局路由 衔接设计

> 日期：2026-08-09
> 依据：《清风渡-MVP文案总汇》、P2_T6_INNKEEPER_REVIEW.md（伙计暗线+隐藏线）、P2_T8_FIRE_NIGHT_REVIEW.md（走水夜）、numerical-design.json（结局条件与优先级）、endings-full.json（20 结局叙事）、PDD 分支流程（scene_040 走水夜 / scene_050 路线分歧 / scene_200+ 结局）
> 状态：设计稿（待总监评审与实现）

---

## 一、目标与衔接点

在 MVP 现有流程末端（`scene_day3_close` 当前为 terminal）接入完整收束链：

```
[第三章·三天九时段]（不变）
  → scene_day3_close（第三日夜收束，取消 terminal）
  → ★ scene_day3_summary　结算页：三日回顾 + 洞察/碎片(线索)/三好感统计 + 关键发现
  → ★ scene_fire_night_transition　过渡（几句话）
  → ★ scene_fire_night　走水夜（复用 P2_T8 fire_night.scene.md 四选项）
  → ★ scene_fire_night_outcome　走水夜结果（死亡分支 / 正常）
  → ★ scene_post_fire_night　走水夜后·隐藏线探查（得闲饮茶入口）
  → ★ scene_route_split　路线分歧（合作线 / 独行线，含信错了人陷阱）
  → ★ scene_ending_gate　结局路由（按数值设计优先级 → 17 个结局节点）
```

**衔接原则**：三天九时段全部内容零改动；P2_T6 伙计暗线/隐藏线的 flag（`recognized_scar`/`hidden_line_unlocked`/`bait_marked`/`observed_account_book` 等）在结算页与结局路由中生效；P2_T8 走水夜场景直接复用。

---

## 二、结算页设计（scene_day3_summary）

**位置**：`scene_day3_close` 之后（收束文本「是时候去观澜阁了。」后接结算）。
**形式**：旁白 + 数值统计文本（MVP 对话框展示，状态栏数值同步实时刷新，无需新 UI 组件）。
**save_point**：true（关键决策前存档）。

### 文案（旁白）

```
三日一瞬。
你坐在灯下，把这三日的人和事，细细理了一遍。

　洞察　　X
　线索　　碎片 Y
　柳陆书　好感 A
　黎客颍　好感 B
　归汉　　好感 C
```

### 关键发现差分（按 flag 条件逐条显示）

| flag | 显示文案 |
| --- | --- |
| `recognized_scar` | 你一直记得伙计右手虎口那道旧疤——那不是干粗活留下的。 |
| `hidden_line_unlocked` | 你总想起靠门第三张桌那壶没人喝的茶，茶还是温的。 |
| `watched` | 你隐约觉得，有双眼睛一直在暗处看着你。 |
| `fire_night_warned` | 你想起那夜闻到的灯油味——那味道不对。 |
| `bait_marked` | 你记下了伙计说的那棵歪脖子老槐树。 |

### 收尾（进入过渡）

```
天亮就该动身去观澜阁了。
可这一夜，注定不太平。
```

**效果**：无数值变化，仅展示。选项：「熄灯睡下」→ 过渡节点。

---

## 三、过渡文案（scene_fire_night_transition · 几句话）

衔接 P2_T8 走水夜场景入口（与 P2_T8 REVIEW 一致：夜半起火、柳陆书第一个冲进去、黎客颍楼下接应）：

```
你在客栈又歇了两日。雨停了又下，青石板上积水映着灯笼，一晃就是一夜。
入夜你早早躺下，盘算着明日动身去观澜阁的事。
夜半，一阵急促的脚步声把你惊醒。走廊尽头，火光冲天——
「走水了——」
```

→ 直接进入 `scene_fire_night`（P2_T8 场景正文与四选项）。

---

## 四、走水夜接入（scene_fire_night + outcome）

复用 `scenes/fire_night.scene.md`（P2_T8 交付，已通过评审）：

| 选项 | 条件 | 效果 | 后续 |
| --- | --- | --- | --- |
| 冲上楼跟柳陆书救人 | — | 归+5 柳+5 洞察+1 | 若 `exposed && 三好感均<0` → **死亡·替人挡了刀** |
| 留楼下帮黎接应 | — | 黎+10 碎片+1 | 正常 |
| 先看火势（灯油警觉） | `fire_night_warned` | 洞察+1 黎+5 | 正常 |
| 跑去找伙计要水桶 | — | 行动+1 | 正常 |

**scene_fire_night_outcome**（走水夜结果，旁白）：
```
火灭了。归汉房间的门框烧黑了大半，人没事。
柳陆书靠墙坐着，扇子燎黑了一角，被烟呛得说不出话；黎客颍在院子里拧湿毛巾。
你站在走廊里，看着观澜阁的方向。
```
- 死亡分支 → `ending_sacrifice`（替人挡了刀，P2_T8 已定义触发）
- 正常 → `scene_post_fire_night`

---

## 五、走水夜后·隐藏线探查（scene_post_fire_night）

对齐 PDD 4.6 / P2_T6：走水夜后可继续探查第三张桌。

| 选项 | 条件 | 目标 |
| --- | --- | --- |
| 再去看看靠门第三张桌 | `hidden_line_unlocked` | `ending_tea`（得闲饮茶：账本「等他回来。」→ 伙计现身 → 连夜离开） |
| 回房休息 | — | `scene_route_split` |

（未解锁隐藏线时仅显示「回房休息」，直接进入路线分歧。）

---

## 六、路线分歧（scene_route_split）

对齐 PDD scene_050（合作线/独行线）：

```
是时候去观澜阁了。你打算——
```

| 选项 | 目标 | 效果 |
| --- | --- | --- |
| 与三人同行 | `scene_ending_gate` | `route_coop` |
| 独自先行 | `scene_solo_gate` | `route_solo` |

**scene_solo_gate**（独行线判定）：

| 选项 | 条件 | 目标 |
| --- | --- | --- |
| 按伙计说的密道走（夜探） | `bait_marked` | `ending_betrayed`（信错了人，P2_T6 陷阱线） |
| 绕大路，天亮了再走 | — | `scene_ending_gate` |
| 独自摸黑进观澜阁 | — | `scene_ending_gate`（`route_solo` 已置，供「独行者」判定） |

---

## 七、结局路由（scene_ending_gate）

按 numerical-design `ending_resolution_priority`（death → hidden → truth → cp → cb → neutral → distant）顺序判定，选项按此顺序排列、条件互斥（先判定的优先级高；区间用顺序裁剪实现，如 cb 只需 `>=30`，因 cp `>=70` 已先行过滤）。

| # | 结局 | 条件（MVP 可判定格式） | 优先级 |
| --- | --- | --- | --- |
| 1 | 三人反目 | `liu_affection<-10` && `li_affection<-10` && `gui_affection<-10` | death |
| 2 | 封印破碎 | `fragments<4` | death |
| 3 | 错过真相 | `fragments<3` | death |
| 4 | 一知半解 | `fragments>=3` && `fragments<5` && `insight<4` | death |
| 5 | 被真相压垮 | `fragments>=6` && `insight<2` | death |
| 6 | 得闲饮茶 | `hidden_line_unlocked` && `observed_account_book` | hidden |
| 7 | 真相达成 | `fragments>=8` && `insight>=6` | truth |
| 8 | 扇底风（柳CP） | `liu_affection>=70` | cp |
| 9 | 归刀入鞘（黎CP） | `li_affection>=70` | cp |
| 10 | 长剑有穗（归CP） | `gui_affection>=70` | cp |
| 11 | 旧友新茶（柳CB） | `liu_affection>=30` | cb |
| 12 | 同路之人（黎CB） | `li_affection>=30` | cb |
| 13 | 不冻泉（归CB） | `gui_affection>=30` | cb |
| 14 | 独行者 | `route_solo` && `insight>=6` | solo |
| 15 | 清风过客 | `fragments>=4`（兜底·中立） | neutral |
| 16 | 陌生人 | 三好感均 `<=29` | distant |

**前置已处理、不入结算路由**：`前方无路`（开场彩蛋）、`淹死在自己的好奇心里`（三天内第三次闲逛死亡）、`信错了人`（走水夜后独行密道，第五节）、`替人挡了刀`（走水夜 outcome）。

**结局节点**：`ending_xxx` 共 17 个（含独行线 2 个前置死亡），`terminal=true`，叙事文本取自 endings-full.json（已写文案零改动），speaker=旁白。

---

## 八、分支树/数据改动清单（实现阶段）

1. `data/branch-tree-mvp.json`：
   - `scene_day3_close`：移除 `terminal: true`，新增 choice → `scene_day3_summary`
   - 新增节点：`scene_day3_summary`、`scene_fire_night_transition`、`scene_fire_night`、`scene_fire_night_outcome`、`scene_post_fire_night`、`scene_route_split`、`scene_solo_gate`、`scene_ending_gate`、17 个 `ending_*` 节点
   - 节点约 33 → 57（增量 24）
2. `data/final-dialogue/mvp/liu_lushu_day1.json`：新增结算页/过渡/走水夜结果/结局节点文案（结局叙事取自 endings-full.json，零改写）
3. `scripts/mvp_ui_controller.gd`：
   - `BACKGROUND_TEXTURES` / `BACKGROUND_COLORS` / 角色可见性：补充新节点映射（结算页/走水夜用现有客栈背景；结局节点隐藏角色）
   - 无需改动核心渲染/选择逻辑（条件路由已由 runner 支持）
4. `scenes/main.tscn`：无需改动

**数值兼容性**：`_conditions_met` 已支持简写 int（>=）与完整 op（gte/lte/eq/neq）多键 AND；区间用顺序裁剪实现，无需改引擎。

---

## 九、一致性核对

- ✅ 三天九时段内容零改动（衔接在 day3_close 之后）
- ✅ 走水夜复用 P2_T8 已评审场景（四选项 + fire_night_warned 差分 + 死亡分支）
- ✅ 伙计暗线/隐藏线 flag（P2_T6）在结算页差分、得闲饮茶入口、信错了人陷阱中全部生效
- ✅ 20 结局全覆盖（4 个前置流程 + 16 个路由 + 走水夜/独行前置 2 个死亡入口，均可达）
- ✅ 文本取自已写文案（endings-full / P2_T8 / PDD），零自由发挥
- ⚠️ 待确认：结算页以「对话框文本」展示（MVP 现状）而非独立结算面板——如需独立面板 UI，另行立项

---

## 十、评审与下一步

- 待评审：产品设计总监（剧情衔接/文案一致性）→ 技术总监（条件路由/节点结构）→ 制作人终审
- 评审通过后：按第八节实现到 branch-tree-mvp.json + final-dialogue JSON，静态校验后提交
