# Java Codex Skills

这个仓库收集了 3 个用于 Codex 的 Java 后端学习与分析 skill：

- `java-backend-vibe-upskill`：Java 后端面试训练、模拟面试、面试复盘与知识卡沉淀。
- `java-architecture-analyzer`：Java/Spring 项目架构分析、业务链路梳理、时序图与重构方案。
- `java-backend-engineering-mentor`：日常后端工程训练、业务模块设计、引导式编码与代码评审。

## 目录

```text
skills/
  java-backend-vibe-upskill/
  java-architecture-analyzer/
  java-backend-engineering-mentor/
```

## 使用

把需要的目录复制到本机 Codex skill 目录：

```powershell
Copy-Item -Recurse .\skills\java-backend-vibe-upskill $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\skills\java-architecture-analyzer $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\skills\java-backend-engineering-mentor $env:USERPROFILE\.codex\skills\
```

然后在 Codex 中通过 skill 名称或自然语言触发对应能力。

## 内容

每个 skill 至少包含：

- `SKILL.md`：主说明与触发规则。
- `references/`：按需加载的工作流、知识库或模板。
- `agents/`：可选 agent 配置。
- `scripts/`：可选辅助脚本。
