# Java Codex Skills

用于 Codex 的 Java 后端技能包集合，覆盖 Java 后端面试训练、Spring 项目架构分析、日常工程设计训练三类场景。

## About

这个仓库适合想用 Codex 系统学习 Java 后端的人：既能做面试向的模拟拷打和复盘，也能读真实 Java/Spring 项目、梳理业务链路，还能做日常后端业务模块设计与工程训练。

当前包含 3 个 skill：

- `java-backend-vibe-upskill`：Java 后端面试训练、模拟面试、面试复盘、知识卡沉淀。
- `java-architecture-analyzer`：Java/Spring 项目架构分析、业务链路梳理、时序图、设计模式提炼、重构方案。
- `java-backend-engineering-mentor`：日常后端工程训练、业务模块设计、引导式编码、代码评审。

## Directory

```text
skills/
  java-backend-vibe-upskill/
  java-architecture-analyzer/
  java-backend-engineering-mentor/
```

每个 skill 通常包含：

- `SKILL.md`：主说明、触发规则、工作流。
- `references/`：按需加载的知识库、模板或详细执行说明。
- `agents/`：可选 agent 配置。
- `scripts/`：可选辅助脚本。

## Install

### 方法一：复制全部 skill

在 PowerShell 中进入仓库目录，然后执行：

```powershell
Copy-Item -Recurse .\skills\java-backend-vibe-upskill $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\skills\java-architecture-analyzer $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\skills\java-backend-engineering-mentor $env:USERPROFILE\.codex\skills\
```

复制完成后，重启 Codex 或开启一个新任务，让 Codex 重新加载 skill 列表。

### 方法二：只安装某一个 skill

如果只想安装面试训练 skill：

```powershell
Copy-Item -Recurse .\skills\java-backend-vibe-upskill $env:USERPROFILE\.codex\skills\
```

如果只想安装项目架构分析 skill：

```powershell
Copy-Item -Recurse .\skills\java-architecture-analyzer $env:USERPROFILE\.codex\skills\
```

如果只想安装工程训练 skill：

```powershell
Copy-Item -Recurse .\skills\java-backend-engineering-mentor $env:USERPROFILE\.codex\skills\
```

## How To Use

安装后，在 Codex 里直接用 skill 名称或自然语言描述目标即可触发。

### Java 面试训练

可以这样说：

```text
用 java-backend-vibe-upskill 帮我做一场 Java 后端模拟面试
```

也可以这样说：

```text
我想准备 Java 后端实习面试，重点拷打 Redis、JVM、Spring 和项目表达
```

适合场景：

- Java 后端模拟面试
- 八股和项目拷打
- 面试复盘
- 把真实项目经历沉淀成面试案例
- 生成知识卡和复习计划

### Java/Spring 架构分析

可以这样说：

```text
用 java-architecture-analyzer 帮我分析这个 Spring Boot 项目的整体架构
```

也可以指定一条业务链路：

```text
帮我梳理用户下单链路，从 Controller 到 Service、Mapper、Redis、MQ 全部画出来
```

适合场景：

- 看懂陌生 Java/Spring 项目
- 分析模块边界和技术栈
- 梳理登录、下单、支付、鉴权等业务流程
- 画时序图和架构图
- 提炼设计模式、高并发设计、重构方案

### Java 后端工程训练

可以这样说：

```text
用 java-backend-engineering-mentor 帮我做一个优惠券模块的业务设计训练
```

也可以这样说：

```text
给我一个今天的 Java 后端工程训练题，重点考并发一致性和数据库设计
```

适合场景：

- 后端业务模块设计训练
- 引导式编码练习
- 企业级代码评审
- 每日后端训练题
- 数据库、缓存、事务、并发一致性训练

## Update

如果本仓库后续有更新，可以重新拉取并覆盖本地 skill：

```powershell
git pull
Copy-Item -Recurse -Force .\skills\java-backend-vibe-upskill $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse -Force .\skills\java-architecture-analyzer $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse -Force .\skills\java-backend-engineering-mentor $env:USERPROFILE\.codex\skills\
```

## Acknowledgments

特别感谢 `java-backend-vibe-upskill` 的两个原始灵感与资源来源：

- [Hazehacker/java-backend-interview-simulator](https://github.com/Hazehacker/java-backend-interview-simulator)：提供 Java 后端模拟面试相关资源与题库思路。
- `vibe-upskill` 的原作者：提供从 Agent 开发过程提炼知识、生成面试卡片和持续复习的学习工作流。

这个仓库中的 `java-backend-vibe-upskill` 是在上述两个工作的基础上，面向 Codex 本地 skill 机制做的整合与适配。

## Notes

- 这些 skill 面向 Codex 的本地 skill 机制，不是普通 Java 依赖包。
- `java-backend-vibe-upskill` 偏面试准备。
- `java-architecture-analyzer` 偏真实项目阅读和架构理解。
- `java-backend-engineering-mentor` 偏日常工程训练和代码实践。
- 如果一个任务同时涉及多个 skill，建议先明确目标：面试表达、项目分析、还是工程训练。
