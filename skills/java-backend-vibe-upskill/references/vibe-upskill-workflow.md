# Vibe Upskill Workflow For Java Backend Interviews

## Purpose

Turn an interview, Codex session, or project walkthrough into reusable interview preparation material. Prefer real evidence from the user's transcript, code, resume, or answers. Do not fabricate advanced-looking lessons when the source material is thin.

## Input Modes

| Mode | Inputs | Use when |
|---|---|---|
| Interview transcript | Current chat or pasted interview record | The user just practiced or provides mock-interview history |
| Agent session review | Codex/vibe-coding transcript, commits, logs, or project directory | The user wants to learn from agent-assisted development |
| Resume/JD bridge | Resume, target JD, and interview report | The user wants targeted Java backend preparation |
| Cold start | No transcript yet | Run a short mock interview first |

If the transcript is very long, split by stage: requirements, architecture, implementation, debugging, deployment, interview Q&A, or final feedback.

## Extraction Schema

For each high-signal point, write:

```text
【上下文】项目或面试阶段是什么？
【问题/决策】要解决什么问题或解释什么技术点？
【原始表现】用户怎么答、Codex/Agent 怎么做、或代码怎么体现？
【底层原理】为什么这个做法有效？
【替代方案】还能怎么做？各自权衡是什么？
【可迁移教训】换到另一个 Java 后端项目是否适用？适用条件是什么？
【状态】已掌握 / 未复述 / 待复习 / 待确认 / 待深挖
```

Use `[待确认]` when the reason is inferred. Use `[待深挖]` when the user relied on black-box tool behavior or only named a concept.

## Filter Rules

Keep:

- architecture tradeoffs
- Java concurrency, JVM, Spring, MySQL, Redis, messaging, distributed-systems reasoning
- debugging paths and root causes
- coding challenge mistakes
- project-expression gaps
- testing, deployment, observability, and operations lessons
- AI-assisted development patterns that are useful to explain in interviews

Drop:

- greetings and confirmations
- repeated failed commands unless the final root cause matters
- formatting-only edits
- mechanical file moves with no design decision
- generic textbook questions not grounded in the source

## Card Format

```markdown
### Q-{number}: {title}

- **类型**：场景设计题 / Bug 排查题 / 深挖原理题 / 代码审查题 / 项目表达题 / 系统设计题 / 运维排障题 / 方案对比题 / 复盘反思题 / 测试质量题
- **难度**：基础 / 进阶 / 高级
- **标签**：#Java #Spring #MySQL
- **来源**：{project/session/stage}
- **状态**：已掌握 / 未复述 / 待复习 / 待确认 / 待深挖
- **创建日期**：YYYY-MM-DD
- **技术栈版本**：unknown or exact versions
- **最后审查日期**：未审查

#### 场景描述
...

#### 问题
...

#### 参考思路
1. ...
2. ...
3. ...

#### 参考答案要点
- ...

#### 反事实推理
- 如果规模扩大 100 倍，瓶颈会在哪里？
- 如果把当前技术换成另一个方案，需要改什么？
- 如果关键组件宕机、超时或产生脏数据，系统如何降级和恢复？

#### 深挖追问
- ...
```

## Scenario Case Format（场景案例 = 面试答题骨架）

当素材覆盖一个完整场景（选型 → 实现 → 踩坑 → 落地 → 复盘）时，除面试卡外还必须产出场景案例，写入 `<knowledge_root>/scenario-cases/{场景名}.md`。案例每一节对应一类固定面试问法（🎤 标注）——攒案例即攒答案：

```markdown
# 场景案例：{场景名}（{项目名}）

> 状态：草稿 / 已复述 / 可上面试 ｜ 创建：YYYY-MM-DD ｜ 更新：YYYY-MM-DD

## 1. 背景与约束
业务是什么、量级、一致性/延迟要求。
🎤 对应面试题："介绍一下这个项目/你做得最深的模块"

## 2. 技术选型
| 候选方案 | 优点 | 缺点 | 为什么选/不选 |
🎤 对应面试题："为什么用 X 不用 Y？"

## 3. 实现要点
关键类/代码路径/配置，不贴全量代码，标（类名#方法:L行号）。
🎤 对应面试题："具体怎么实现的？"

## 4. 踩坑记录
现象 → 根因 → 解法。跟练项目没有亲历坑时写推演坑并标注 [推演]；禁止把推演坑讲成亲历坑。
🎤 对应面试题："遇到过什么困难/坑？"

## 5. 落地验证
怎么证明生效：压测数据 / 日志 / 接口返回对比。
🎤 对应面试题："怎么确认方案有效？"

## 6. 复盘
做得好的 / 可以更好的 / 重来一次怎么改。
🎤 对应面试题："这个项目有什么问题？重来你怎么做？"

## 7. 可迁移教训
什么条件下能复用到别的项目。
🎤 对应面试题："这个经验换个场景还适用吗？"

## 8. 反事实推演
规模 ×100 / 关键组件宕机 / 产生脏数据时的系统行为与降级。
🎤 对应面试题："QPS 上来怎么办？X 挂了怎么办？"

## 9. 面试转化
关联面试卡号（Q-xx）；本场景最容易被拷打的 3 个点。
```

规则：

- 一次只做一个场景，禁止批量生成空壳案例
- 每节内容必须来自真实代码或真实回答的证据；证据不足标 `[待确认]` / `[待深挖]`
- 案例与面试卡双向链接：案例第 9 节列卡号，卡片"来源"字段写场景案例文件名

## Knowledge Files

Determine the knowledge root once per task:

1. User-provided path
2. `~/.codex/java-knowledge/` by default; create it when writing files
3. Project-local `knowledge/` only when the user explicitly asks for a project-specific knowledge base

Use these files under the selected root unless the user chooses another structure:

- `interview-qa.md`: interview cards grouped by type and difficulty
- `scenario-cases/`: one file per scenario; interview answering skeletons for real projects (see Scenario Case Format)
- `pitfall-checklist.md`: pitfalls grouped by architecture, coding, debugging, deployment, interview expression
- `architecture-notes.md`: decisions and tradeoffs
- `debugging-playbook.md`: symptom -> diagnosis path -> root cause -> prevention
- `review-schedule.md`: spaced review table
- `knowledge-index.md`: counts, last update, source sessions, weak-point summary

## Spaced Review

Use a simple three-score schedule:

| Score | Meaning | Next interval |
|---|---|---|
| 0 | 完全卡住 | 1 day |
| 1 | 部分回忆 | halve current interval, minimum 1 day |
| 2 | 流畅复述 | double current interval, maximum 120 days |

Default interval sequence: 1 day, 3 days, 7 days, 14 days, 30 days, 60 days, 120 days.

When writing `review-schedule.md`, calculate the next review date with `scripts/next-review-date.py` when available. If the script cannot be run, apply the table mechanically and show the current interval used.

## Restatement Handling

Show the question without the reference answer. Ask the user to answer in their own words. Then reveal answer points and ask for score 0, 1, or 2.

If the user skips, mark the card `未复述`. After three skips, recommend practicing one easy card. After ten skips in one session, pause card generation and ask the user to either restate one card or end the current review.

## Full-Link Narration Drill（全链路叙述训练）

面试中"介绍项目/模块"要求 2-3 分钟连续表达——只看卡片答点练不出这种题感。每个场景案例在标记"可上面试"之前，至少进行一次口述训练：

1. 用户**不看案例文件**，用 2-3 分钟口述完整链路：背景约束 → 选型理由 → 实现要点 → 踩坑 → 验证 → 复盘
2. 不给稿子、不提示，让用户完整讲完再反馈
3. 记录卡壳点、跳过点、讲错点；每个卡壳点转成一张面试卡（类型：项目表达题，状态：未复述）
4. 按 `references/evaluation-rubric.md` 的思维逻辑与表达能力维度给一句话反馈
5. 能流畅讲满 2 分钟且覆盖案例 1-6 节骨架 → 案例标记"可上面试"

## Output Language

Use Chinese for all interview, feedback, card, and knowledge-base content. English is acceptable only in file paths, frontmatter field names, code, commands, and technology names.
