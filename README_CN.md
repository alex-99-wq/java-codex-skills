<h1 align="center">☕ Java Codex Skills</h1>
<h3 align="center">面向 Java 后端面试、Spring 架构分析与工程训练的 Codex Skills</h3>
<h3 align="center">模拟面试 · 架构拆解 · 工程训练</h3>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/platform-Codex-orange" alt="platform">
  <img src="https://img.shields.io/badge/language-%E4%B8%AD%E6%96%87%20%2F%20English-brightgreen" alt="language">
</p>

<p align="center">
  <a href="README.md">English</a>
</p>

---

## 1. 项目简介

### 一句话简介

**这是一个 Java 后端 Codex 本地 skill 集合，用来做面试训练、项目架构分析和日常工程能力训练。**

当前包含 3 个 skill：

| Skill | 用途 |
|------|------|
| `java-backend-vibe-upskill` | Java 后端模拟面试、面试复盘、场景案例、知识卡片和间隔复习。 |
| `java-architecture-analyzer` | 阅读 Java/Spring 项目、分析架构、梳理业务链路、生成图和报告。 |
| `java-backend-engineering-mentor` | 日常后端工程训练、业务模块设计、引导式编码和代码评审。 |

这个仓库的目标不是让 Codex 只帮你写代码，而是把真实 Java 后端开发与项目阅读过程转化为可复用、可复述、可长期积累的工程能力。

---

## 2. 目录

| 章节 | 内容 |
|------|------|
| [1. 项目简介](#1-项目简介) | 这个仓库提供什么 |
| [2. 目录](#2-目录) | 本目录 |
| [3. 快速开始](#3-快速开始) | 快速安装和首次使用 |
| [4. 核心 Skill](#4-核心-skill) | 每个 skill 的能力 |
| [5. 安装方式](#5-安装方式) | 手动安装和更新命令 |
| [6. 使用示例](#6-使用示例) | 常见触发方式 |
| [7. 文件结构](#7-文件结构) | 仓库目录说明 |
| [8. MIT License 合规说明](#8-mit-license-合规说明) | 许可证和上游声明 |
| [9. 致谢](#9-致谢) | 上游项目与灵感来源 |

---

## 3. 快速开始

### 3.1 前置依赖

| 依赖 | 说明 |
|------|------|
| Codex desktop 或 Codex CLI | 需要支持本地 skills 的 Codex 环境。 |
| Git | 推荐用于克隆和更新仓库。 |
| Java 后端学习上下文 | 可选，但很有用：简历、项目目录、目标岗位、代码仓库等。 |

### 3.2 让 Codex 自动安装

直接把下面这句话发给 Codex：

```text
帮我安装这些 Java Codex skills：https://github.com/alex-99-wq/java-codex-skills
```

Codex 可以自动克隆仓库、复制 skill 到本机目录，并验证安装结果。

### 3.3 Windows 手动安装

```powershell
git clone https://github.com/alex-99-wq/java-codex-skills.git
cd java-codex-skills

Copy-Item -Recurse .\skills\java-backend-vibe-upskill $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\skills\java-architecture-analyzer $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\skills\java-backend-engineering-mentor $env:USERPROFILE\.codex\skills\
```

复制完成后，重启 Codex 或开启一个新任务，让 Codex 重新加载 skill 列表。

---

## 4. 核心 Skill

### 4.1 Java Backend Vibe Upskill

当你想做 Java 后端面试准备时，用这个 skill。

它支持：

- Java 后端模拟面试
- Redis、JVM、Spring、MySQL、并发、项目表达拷打
- 面试复盘和知识沉淀
- 从真实项目经历生成面试场景案例
- 面试卡片与间隔复习工作流

示例：

```text
用 java-backend-vibe-upskill 帮我做一场 Java 后端应届面试模拟。
```

### 4.2 Java Architecture Analyzer

当你想看懂一个 Java/Spring 项目时，用这个 skill。

它支持：

- Spring Boot / Spring Cloud 架构分析
- 构建文件、配置文件、模块边界识别
- 从 Controller 到 Service、Mapper、Redis、DB、MQ 的业务链路追踪
- Mermaid/SVG/HTML 架构图和时序图
- 设计模式提炼与重构方案

示例：

```text
用 java-architecture-analyzer 分析这个 Spring Boot 项目，并梳理下单链路。
```

### 4.3 Java Backend Engineering Mentor

当你想做日常后端工程训练，而不是面试模拟时，用这个 skill。

它支持：

- 后端业务模块设计训练
- 引导式编码练习
- 企业级代码评审
- 每日后端训练题
- 数据库、缓存、事务、一致性、性能推理

示例：

```text
用 java-backend-engineering-mentor 帮我设计一个优惠券模块，重点考虑并发和一致性。
```

---

## 5. 安装方式

### 只安装某一个 skill

```powershell
# 面试训练
Copy-Item -Recurse .\skills\java-backend-vibe-upskill $env:USERPROFILE\.codex\skills\

# 架构分析
Copy-Item -Recurse .\skills\java-architecture-analyzer $env:USERPROFILE\.codex\skills\

# 工程训练
Copy-Item -Recurse .\skills\java-backend-engineering-mentor $env:USERPROFILE\.codex\skills\
```

### 更新已有安装

```powershell
git pull

Copy-Item -Recurse -Force .\skills\java-backend-vibe-upskill $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse -Force .\skills\java-architecture-analyzer $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse -Force .\skills\java-backend-engineering-mentor $env:USERPROFILE\.codex\skills\
```

---

## 6. 使用示例

### 示例一：模拟面试

```text
我正在准备 Java 后端实习面试，用 java-backend-vibe-upskill 拷打我 Redis、JVM、Spring、MySQL 和项目表达。
```

### 示例二：项目架构分析

```text
用 java-architecture-analyzer 读这个 Spring Cloud 项目，识别模块并写一份架构全景报告。
```

### 示例三：业务链路梳理

```text
帮我梳理用户登录链路，从 Controller 到 Service、Redis、数据库、Token 校验都画出来。
```

### 示例四：工程训练题

```text
给我一个 Java 后端每日训练题，主题是高并发库存扣减。
```

### 示例五：代码评审

```text
用 java-backend-engineering-mentor 从分层、事务、缓存、SQL、并发角度 review 这个 Service 实现。
```

---

## 7. 文件结构

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

## 8. MIT License 合规说明

本仓库使用 MIT License，见 [LICENSE](LICENSE)。

部分内容派生或参考了上游 MIT 许可项目。对应的版权和许可声明保留在：

- [skills/java-backend-vibe-upskill/LICENSE](skills/java-backend-vibe-upskill/LICENSE)
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

MIT 合规要点：

- 保留原始 copyright 声明。
- 保留 MIT permission notice。
- 在复制或分发软件及其实质性部分时包含这些声明。
- 在 README 中明确说明改编来源。

---

## 9. 致谢

特别感谢：

- [Hazehacker/java-backend-interview-simulator](https://github.com/Hazehacker/java-backend-interview-simulator)：提供 Java 后端模拟面试资源基础。
- [bb-cccc/vibe-upskill](https://github.com/bb-cccc/vibe-upskill)：提供从 AI Agent 对话中提炼真实工程能力的学习工作流。

`java-backend-vibe-upskill` 将两个来源的思路整合为一个面向 Codex 本地 skill 机制的 Java 后端面试训练工具。

