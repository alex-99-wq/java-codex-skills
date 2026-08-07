<h1 align="center">☕ Java Codex Skills</h1>
<h3 align="center">Codex Skills for Java Backend Interviews, Spring Architecture Analysis, and Engineering Practice</h3>
<h3 align="center">Mock interviews · Architecture walkthroughs · Engineering drills</h3>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/platform-Codex-orange" alt="platform">
  <img src="https://img.shields.io/badge/language-English%20%2F%20%E4%B8%AD%E6%96%87-brightgreen" alt="language">
</p>

<p align="center">
  <a href="README_CN.md">中文版</a>
</p>

---

## 1. Project Overview

### One-Liner

**A collection of local Codex skills for learning, practicing, and explaining Java backend engineering.**

This repository packages three Codex skills:

| Skill | Purpose |
|------|---------|
| `java-backend-vibe-upskill` | Java backend mock interviews, interview review, scenario cards, and spaced review. |
| `java-architecture-analyzer` | Read Java/Spring projects, map architecture, trace business flows, and generate diagrams. |
| `java-backend-engineering-mentor` | Daily backend engineering drills, module design practice, guided implementation, and code review. |

The goal is simple: use Codex not only to write code, but to turn real Java backend work into durable engineering ability.

---

## 2. Table of Contents

| Section | Content |
|---------|---------|
| [1. Project Overview](#1-project-overview) | What this repository provides |
| [2. Table of Contents](#2-table-of-contents) | This section |
| [3. Quick Start](#3-quick-start) | Fast installation and first use |
| [4. Core Skills](#4-core-skills) | What each skill does |
| [5. Installation](#5-installation) | Manual install and update commands |
| [6. Usage Examples](#6-usage-examples) | Common prompts |
| [7. Project Structure](#7-project-structure) | Repository layout |
| [8. License Compliance](#8-license-compliance) | MIT license notes and upstream notices |
| [9. Acknowledgments](#9-acknowledgments) | Upstream projects and inspirations |

---

## 3. Quick Start

### 3.1 Prerequisites

| Requirement | Details |
|-------------|---------|
| Codex desktop or Codex CLI | A Codex environment that supports local skills. |
| Git | Recommended for cloning and updating this repository. |
| Java backend learning context | Optional, but useful: a resume, project directory, interview target, or codebase. |

### 3.2 Install with Codex

Send this to Codex:

```text
Help me install these Java Codex skills: https://github.com/alex-99-wq/java-codex-skills
```

Codex can clone the repository, copy the skill folders to your local Codex skills directory, and verify the installation.

### 3.3 Manual Install on Windows

```powershell
git clone https://github.com/alex-99-wq/java-codex-skills.git
cd java-codex-skills

Copy-Item -Recurse .\skills\java-backend-vibe-upskill $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\skills\java-architecture-analyzer $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\skills\java-backend-engineering-mentor $env:USERPROFILE\.codex\skills\
```

After copying, restart Codex or open a new Codex task so the skill list reloads.

---

## 4. Core Skills

### 4.1 Java Backend Vibe Upskill

Use this when you want interview-oriented Java backend practice.

It supports:

- Java backend mock interviews
- Redis, JVM, Spring, MySQL, concurrency, and project-expression drilling
- Interview replay and post-interview distillation
- Scenario case building from real project experience
- Interview cards and spaced review workflows

Example:

```text
Use java-backend-vibe-upskill to run a Java backend mock interview for a new-grad role.
```

### 4.2 Java Architecture Analyzer

Use this when you want to understand a Java/Spring project.

It supports:

- Spring Boot / Spring Cloud architecture analysis
- Build file, configuration, and module boundary discovery
- Business-flow tracing from Controller to Service, Mapper, Redis, DB, and MQ
- Mermaid/SVG/HTML architecture and sequence diagrams
- Design pattern extraction and refactoring plans

Example:

```text
Use java-architecture-analyzer to analyze this Spring Boot project and trace the order creation flow.
```

### 4.3 Java Backend Engineering Mentor

Use this when you want daily engineering practice instead of interview simulation.

It supports:

- Backend business module design training
- Guided implementation practice
- Enterprise-style code review
- Daily backend drills
- Database, cache, transaction, consistency, and performance reasoning

Example:

```text
Use java-backend-engineering-mentor to design a coupon module with concurrency and consistency constraints.
```

---

## 5. Installation

### Install One Skill Only

```powershell
# Interview training
Copy-Item -Recurse .\skills\java-backend-vibe-upskill $env:USERPROFILE\.codex\skills\

# Architecture analysis
Copy-Item -Recurse .\skills\java-architecture-analyzer $env:USERPROFILE\.codex\skills\

# Engineering mentoring
Copy-Item -Recurse .\skills\java-backend-engineering-mentor $env:USERPROFILE\.codex\skills\
```

### Update Existing Install

```powershell
git pull

Copy-Item -Recurse -Force .\skills\java-backend-vibe-upskill $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse -Force .\skills\java-architecture-analyzer $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse -Force .\skills\java-backend-engineering-mentor $env:USERPROFILE\.codex\skills\
```

---

## 6. Usage Examples

### Example 1: Mock Interview

```text
I am preparing for a Java backend internship interview. Use java-backend-vibe-upskill to interview me on Redis, JVM, Spring, MySQL, and project explanation.
```

### Example 2: Project Architecture Walkthrough

```text
Use java-architecture-analyzer to read this Spring Cloud project, identify the modules, and write an architecture overview report.
```

### Example 3: Business Flow Tracing

```text
Trace the user login flow from Controller to Service, Redis, database, and token validation. Generate a sequence diagram.
```

### Example 4: Engineering Drill

```text
Give me a daily Java backend engineering drill about inventory deduction under high concurrency.
```

### Example 5: Code Review

```text
Use java-backend-engineering-mentor to review this service implementation from layering, transaction, cache, SQL, and concurrency perspectives.
```

---

## 7. Project Structure

```text
java-codex-skills/
├── README.md
├── README_CN.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
└── skills/
    ├── java-backend-vibe-upskill/
    │   ├── SKILL.md
    │   ├── LICENSE
    │   ├── agents/
    │   ├── references/
    │   └── scripts/
    ├── java-architecture-analyzer/
    │   ├── SKILL.md
    │   ├── agents/
    │   └── references/
    └── java-backend-engineering-mentor/
        ├── SKILL.md
        ├── agents/
        └── references/
```

---

## 8. License Compliance

This repository is released under the MIT License. See [LICENSE](LICENSE).

Some materials are derived from or inspired by upstream MIT-licensed work. Their copyright and license notices are preserved in:

- [skills/java-backend-vibe-upskill/LICENSE](skills/java-backend-vibe-upskill/LICENSE)
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

MIT compliance checklist:

- Keep the original copyright notices.
- Keep the MIT permission notice.
- Include those notices in copies or substantial portions of the software.
- Clearly credit adapted upstream work.

---

## 9. Acknowledgments

Special thanks to:

- [Hazehacker/java-backend-interview-simulator](https://github.com/Hazehacker/java-backend-interview-simulator), which provided the Java backend mock interview resource foundation.
- [bb-cccc/vibe-upskill](https://github.com/bb-cccc/vibe-upskill), which provided the learning workflow for extracting real engineering skills from AI Agent conversations.

`java-backend-vibe-upskill` adapts ideas from both sources into a Codex-local skill focused on Java backend interview readiness.

