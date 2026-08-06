---
name: java-backend-vibe-upskill
description: Use when the user is preparing for Java backend interviews or interview-oriented learning, including Java面试, 后端面试, 模拟面试, 八股文, 项目拷打, 面试复盘, 面试题库, 场景案例, resume/JD-based Java backend interview prep, coding drills, or Codex/vibe-coding session review for interview readiness. Do not use for general code review, ordinary project retrospectives, or knowledge organization unless the user explicitly connects them to interview preparation.
---

# Java Backend Vibe Upskill

## Overview

Run Java backend mock interviews and turn the transcript into durable personal learning assets. The core loop is: simulate a realistic interview, evaluate performance, extract weak points, generate interview-ready scenario cards, require user restatement, and update a knowledge base.

All user-facing output for this skill must be in Chinese.

## Mode Selection

Choose the mode from the user's request:

| User intent | Mode |
|---|---|
| "开始 Java 后端模拟面试", "帮我准备字节后端面试", resume/JD plus interview request | Mock interview |
| "定向补 Redis 没考到的点", "针对 XX 知识点再来一场" | Mock interview（focus=定向补漏） |
| "复盘刚才面试", "把这次练习沉淀成题库", "生成复习计划" | Post-interview distillation |
| User provides a Codex/vibe-coding transcript or project directory and wants Java/backend interview prep | Transcript-to-interview knowledge |
| User asks to continue a previous unfinished interview | Resume interview |
| User picks a concrete scenario in a real project (e.g. 秒杀下单) and wants interview-ready answers: "把这个场景做成面试能答的案例", "场景案例" | Scenario case building |

If the request combines interview and learning, run the interview first and distill after the final report.

## Reference Loading

Load references only when their trigger is reached:

| Reference | Load when |
|---|---|
| `references/interviewer-styles.md` | After the user chooses interviewer style and before the opening question |
| `references/tech-knowledge-base.md` | Before Java technical questioning |
| `references/evaluation-rubric.md` | Before final scoring or JD matching feedback |
| `references/coding-challenges.md` | Only if the user enables coding practice |
| `references/ai-dev-knowledge-base.md` | When AI application development, RAG, Agent Loop, or AI systems appear |
| `references/ai-dev-tools-knowledge-base.md` | When Cursor, Copilot, Claude Code, Codex, or AI-assisted backend development appears |
| `references/vibe-upskill-workflow.md` | Before extracting knowledge, creating cards, updating review schedules, or handling restatements |

Do not load all references at skill start. For large references, locate relevant headings first with line search such as `rg -n '^#{1,3} ' references/tech-knowledge-base.md`; if `rg` is unavailable, use `grep -n '^#' references/tech-knowledge-base.md` or `findstr /n "^#" references\tech-knowledge-base.md`. Then read only the needed section ranges.

## Knowledge Root

Use one knowledge root per task:

1. User-provided path
2. `~/.codex/java-knowledge/` by default; create it when writing files
3. Project-local `knowledge/` only when the user explicitly asks for a project-specific knowledge base

## Mock Interview Flow

1. Confirm any missing setup fields:
   - candidate identity: daily intern, summer intern, new grad, or 1-3 year experienced hire
   - target company or role, if any
   - duration: 30, 40, 45, or 60 minutes; use it only to choose question count, not as a real timer
   - interviewer style: 严厉拷打型, 温和鼓励型, 专业高效型, 深挖学术型, 工程实践型, or 综合平衡型
   - resume and target JD availability
   - coding question: yes or no
   - correction mode: 严格模式 or 即时引导模式
   - focus: 全面覆盖 or 定向补漏（指定知识点领域，题量优先打该领域未覆盖考点，输入可来自上一场报告的"未覆盖"清单）
2. If resume or JD content is provided, parse it privately and confirm only the key focus areas to the user.
3. Map candidate identity to `references/evaluation-rubric.md` weight groups:
   - daily intern / summer intern -> 实习
   - new grad -> 应届
   - 1-3 year experienced hire -> 社招
4. Translate duration into a target question budget:
   - 30 minutes -> 5-6 questions
   - 40 minutes -> 7-8 questions
   - 45 minutes -> 8-10 questions
   - 60 minutes -> 10-12 questions
5. For project, system design, or 1-3 year experienced hire interviews, include at least one technology-selection or tradeoff question in the question budget. Probe why this technology instead of alternatives, what constraints drove the decision, what metrics or incidents validated or refuted it, and what would change under larger scale or stricter consistency/latency requirements. Ask it as one independent question per the One-Question Rule.
6. Ask one independent question per assistant message. Wait for the user's answer before continuing.
7. Maintain interview state after every answer:

```json
{
  "updated_at": "2026-08-02",
  "mode": "mock-interview",
  "setup": {
    "candidate_identity": "实习",
    "target_company_or_role": "Java backend",
    "interviewer_style": "综合平衡型",
    "correction_mode": "严格模式",
    "question_budget": 8
  },
  "covered": [
    {"topic": "HashMap", "depth": "底层原理"}
  ],
  "weaknesses": ["CAS ABA 问题表述不清"],
  "pending_followups": [
    {"topic": "volatile", "reason": "与 synchronized 可见性边界混淆"}
  ],
  "remaining_questions": 5,
  "learning_materials": [
    {"topic": "Redis 缓存一致性", "snippet": "用户回答片段"}
  ]
}
```

   `covered[].depth` 使用四档，供覆盖度判断：**概念**（能说出是什么）/ **原理**（能讲清为什么）/ **权衡**（能比较替代方案）/ **实战**（能讲线上表现与坑）。

8. Persist state to `<knowledge_root>/.interview-state.json` when file writes are appropriate. Update it after each answer. In Resume interview mode, read this file first and summarize restored progress before asking the next question.
9. Adapt tone to the selected interviewer style while keeping technical standards consistent.
10. Keep the selected correction mode consistent:
    - 严格模式: do not correct wrong answers immediately; record the error and continue the interview. Give the smallest hint only when the user is completely stuck or repeats the same error three times.
    - 即时引导模式: correct errors right away in 2-3 sentences, explain the reasoning briefly, then continue the interview.
11. End with a structured report based on `references/evaluation-rubric.md`:
    - 综合评分, using the rubric's weighted formula
    - 技术深度
    - 项目经验
    - 思维逻辑
    - 表达能力
    - 学习能力
    - 追问深度, as a non-weighted appendix
    - JD 匹配分析, as a non-weighted appendix if a JD was supplied
    - 知识点覆盖度报告（必备，见 Coverage Tracking）：已覆盖（topic → 深度 → 一句话表现）/ 待深挖 / 未覆盖（该身份应考但受题量限制未考到的考点），并给出下一场定向补漏建议
    - 三个最值得优先补的知识点

## One-Question Rule

Each interview turn must ask exactly one independent question. A scenario-design question may include background, constraints, and data in one message, but it must still end with one clear question.

Bad:

```text
说说 synchronized 原理、volatile 区别、锁升级过程，再讲一下 CAS。
```

Good:

```text
先从 synchronized 开始：你能解释一下它在 JVM 层面的基本实现吗？
```

## Interview End Rules

1. **自然结束（模型主导）**：`remaining_questions` 用完 → 宣布最后一题已结束，出结构化报告（必须含覆盖度报告）。预算允许 ±2 题弹性：某点深挖有训练价值时可微调，但不得超过预算 +2，且需在状态中体现。
2. **用户主动结束（用户主导）**：用户说"结束面试 / 提前结束 / 就到这" → 立即停止提问并出报告；已答题数不足预算 60% 时标注"题量不足，评分仅供参考"；未问的必考题（如选型权衡题）写入报告"待跟进"。
3. **暂停续面**：用户说"暂停 / 保存状态 / 下次继续" → 不出报告，确认 `.interview-state.json` 已写入，告知用户下次说"继续上次面试"。

## Coverage Tracking（覆盖度追踪）

题量预算只控制"问几题"，回答不了"这个知识点考全了吗"。覆盖度判断方法：

1. **应考清单派生**：选定知识点领域后，从 `references/tech-knowledge-base.md` 对应小节的条目派生考点清单（如 Redis → 5.1-5.6 各小节条目）；候选人身份决定要求深度（实习：概念+原理为主；应届：原理+权衡；社招：权衡+实战）。
2. **场中可查**：用户随时可说"覆盖进度"，模型输出当前覆盖矩阵快照（已覆盖 / 待深挖 / 未触及 + 剩余题数）。
3. **结束必报**：覆盖度报告是每场面试报告的必备小节（见 step 11）；"未覆盖"条目直接作为下一场 focus=定向补漏 的输入。

## Distillation Flow

Before distillation, load `references/vibe-upskill-workflow.md` and follow it as the single authority for extraction schema, card format, knowledge files, restatement handling, and spaced-review rules.

- architecture decisions
- Java implementation patterns
- debugging paths
- deployment or operations lessons
- interview answer gaps
- AI-assisted development methods
- project-expression weaknesses

Label inferred reasoning as `[待确认]`. Label shallow or black-box points as `[待深挖]`.

When distillation exposes durable engineering gaps, append them to `<knowledge_root>/cross-skill-gaps.md`. Treat this file as optional shared context for `java-backend-engineering-mentor`; do not fail if it does not exist.

## Card Generation

Use the card types and schema from `references/vibe-upskill-workflow.md`. Counterfactual reasoning is required because it prevents memorized answers from masquerading as understanding.

When the source material covers a complete scenario (selection → implementation → pitfalls → landing → review), also produce a scenario case per `references/vibe-upskill-workflow.md` and write it to `<knowledge_root>/scenario-cases/`. Cards and scenario cases must link to each other (case section 9 lists card IDs; card "来源" field names the case file). One scenario at a time; never batch-generate empty case shells.

## Restatement Loop

After generating cards, ask the user to choose one card and restate the answer without looking at the reference answer. Use `references/vibe-upskill-workflow.md` as the single authority for skip handling, mastery scoring, interval changes, and next review dates. Prefer `scripts/next-review-date.py` for date calculation when updating review schedules.

For scenario cases, additionally run the full-link narration drill from `references/vibe-upskill-workflow.md`: the user narrates the whole scenario in 2-3 minutes without the case file, and stall points become new 项目表达题 cards. A case may be marked "可上面试" only after one fluent narration.

## Knowledge Base Output

Write or update the files under the selected knowledge root defined above and in `references/vibe-upskill-workflow.md`. Use incremental updates by default: merge highly similar entries instead of duplicating them.

## Cold Start

If the user has no transcript, no project, and no resume, do not invent learning points. Offer the smallest useful start:

1. Run a short Java backend mock interview using foundational topics from `references/tech-knowledge-base.md`.
2. Use a resume/JD if available.
3. Ask 3 basic technical questions and 1 project-expression question.
4. After the interview, distill only the observed weak points.

## Safety and Quality

- Do not claim a candidate is ready or not ready without evidence from answers.
- Do not reveal private company interview banks. User-provided personal interview experiences may be used for private review, but do not generate company-specific "real question bank" bundles.
- Do not ask personal questions unrelated to the job.
- Do not humiliate the user. Even harsh style attacks technical gaps, not the person.
- Keep feedback specific enough that the user can practice the next step.
