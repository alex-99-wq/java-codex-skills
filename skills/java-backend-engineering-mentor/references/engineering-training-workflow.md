# Engineering Training Workflow

## Core Principle

Train engineering judgment before code volume. In training modes, make the user decide requirements, data model, consistency, concurrency, and failure handling before receiving complete implementation code.

## Mode Routing

| Mode | Load when | Output shape |
|---|---|---|
| Engineering design training | User wants to design a backend business module | Seven-step guided design |
| Guided implementation | User wants to practice writing a feature | Next implementation step + partial examples |
| Enterprise code review | User asks to review user-written code | Severity-ordered findings |
| Daily engineering drill | User asks for a practice task | One six-part drill |

## Shared Knowledge

Gap file locations, in priority order:

1. Project: `knowledge/cross-skill-gaps.md`
2. Global: `~/.codex/java-knowledge/cross-skill-gaps.md`

Append format:

```markdown
## 2026-08-02 Source: mentor training
- Redis cache consistency: Could not explain delayed double delete timing or binlog subscription tradeoff.
- Comment system design: Missed idempotency for repeated like requests.
```

If the file does not exist, continue normally. Create it only when writing a new durable gap.

## Engineering Design Training

Run one design topic at a time. Start by restating the target module and constraints in 2-4 bullets, then move through the seven steps.

### Step 1: Requirement Analysis

Prompt for:

- Business object and owner: article, product, order, video, user, coupon, or generic `targetType + targetId`
- User actions: create, query, edit, delete, like, reply, audit, report
- Read/write ratio and expected scale
- Auth and permission boundaries
- Product constraints: sorting, visibility, moderation, pagination, audit trail

Expected output: requirement assumptions and open questions.

### Step 2: Database Design

Prompt for:

- Tables and primary keys
- Essential indexes and query paths
- Soft delete, audit fields, status fields
- Parent/child relationships: one-level reply, multi-level tree, or flat threaded model
- Counter fields and whether they are source of truth or denormalized cache

Push on tradeoffs:

- Why this index order?
- Which query must stay fast?
- What breaks if data grows 100x?

### Step 3: Redis and Cache Design

Prompt for:

- What to cache and at what granularity
- Key design and TTL policy
- Cache penetration, breakdown, avalanche, and hot key handling
- Consistency strategy: delete cache after DB commit, delayed double delete, message queue, binlog subscription, or no cache
- Whether Redis is source of truth for counters, ranking, or idempotency

Require the user to name the consistency window and failure mode they accept.

### Step 4: API Design

Prompt for:

- Endpoint list and method semantics
- DTO/VO shape
- Pagination style: page/size, cursor, or keyset
- Idempotency key, request validation, and error codes
- Permission checks and rate limits

Expected output: concise API table.

### Step 5: Core Business Flow

Prompt for:

- Controller -> Service -> Repository/Mapper -> Cache/MQ call sequence
- Transaction boundary
- Event publication timing
- Synchronous vs asynchronous work
- Data validation order

Expected output: numbered flow or sequence outline.

### Step 6: Exception and Boundary Handling

Prompt for:

- Empty result, deleted target, unauthorized user, duplicate operation
- DB timeout, Redis timeout, MQ failure
- Retry policy and compensation
- User-facing error codes vs internal logs

Expected output: boundary-case table.

### Step 7: Concurrency and Consistency Analysis

Prompt for:

- Concurrent likes, repeated submissions, inventory deduction, coupon claiming, duplicate payment callbacks
- Optimistic lock, distributed lock, Redis atomic operation, unique constraint, or idempotency table
- Lost update and double-write risks
- Lock granularity and timeout

Expected output: concurrency risk list with chosen mitigation.

## Guided Implementation Rules

Use this decision table:

| User situation | Response |
|---|---|
| User is practicing and asks for full code immediately | Give design skeleton and ask for the next missing decision; do not promise a full code bundle as the next step |
| User is stuck on syntax or framework use | Give a small local example, not a whole module |
| User has completed key design decisions | Provide the next narrow file, method, SQL, or test implementation |
| User explicitly confirms delivery is the goal after the training tradeoff is named | Full implementation is allowed, following normal engineering practice |

Partial example size guideline:

- One method, one SQL snippet, one DTO, or one configuration block is usually enough.
- Avoid generating complete Controller + Service + Mapper + XML bundles in training mode.

## Enterprise Code Review

Lead with findings. Use severity labels:

| Severity | Meaning |
|---|---|
| P0 | Data corruption, security issue, severe production outage risk |
| P1 | Likely bug, transaction/concurrency failure, serious performance risk |
| P2 | Maintainability, scalability, or edge-case risk |
| P3 | Style, naming, cleanup, or optional improvement |

Review dimensions:

1. Maintainability: method size, duplicate logic, hidden coupling, magic values
2. Layering: Controller business logic, Service doing persistence details, Mapper leaking domain rules
3. Naming: names hide business meaning, DTO/VO/Entity boundaries unclear
4. SQL: N+1 query, missing index, full scan, unsafe dynamic SQL, wrong pagination
5. Redis/cache: key design, TTL, consistency, hot key, penetration, serialization
6. Concurrency: lost updates, repeated requests, duplicate callbacks, lock scope, idempotency
7. Transactions: `@Transactional` self-invocation, non-public method, swallowed exception, long transaction, wrong propagation
8. Performance: batch operations, remote calls in loops, large payloads, synchronous slow work

Output contract:

```markdown
**Findings**
- [P1] Title - file:line
  Impact: ...
  Fix: ...

**Open Questions**
- ...

**Test Gaps**
- ...
```

If no issues are found, state that clearly and still mention residual test gaps or assumptions.

## Daily Engineering Drill

Generate one drill by default. Required six parts:

1. Business background
2. Product requirements
3. Feature list
4. Technical constraints
5. Thinking questions
6. Acceptance criteria

Drill rules:

- Do not provide a standard answer up front.
- Do not provide complete project code up front.
- Include at least one tradeoff question.
- Include at least one capacity or data-volume assumption.
- Include at least one boundary or failure case.
- If shared gaps exist, choose a task that targets the most recent high-value gap.

Good thinking questions:

- Which data is the source of truth and why?
- Which query path determines your index design?
- What consistency window can the product accept?
- What fails when QPS increases 10x?
- Where does idempotency live?

Bad thinking questions:

- "What is Redis?"
- "Write the standard CRUD."
- "List the steps from the tutorial."

## Mentor State

When persisting progress, use:

```json
{
  "updated_at": "2026-08-02",
  "mode": "daily-engineering-drill",
  "current_topic": "comment system",
  "completed_steps": ["requirement-analysis", "database-design"],
  "observed_gaps": [
    {
      "topic": "Redis cache consistency",
      "evidence": "User chose cache-aside but could not explain failure after DB commit.",
      "next_drill_hint": "Design delayed cache deletion with MQ retry."
    }
  ]
}
```

Use `.mentor-state.json` for progress only. Do not mix it with `.interview-state.json`.
