---
name: java-architecture-analyzer
description: "Use when analyzing Java/Spring architecture, 看懂 Java/Spring 项目, 分析架构, 梳理业务链路（下单/鉴权/支付）, 画时序图, 提炼设计模式, or planning refactors/二次开发. Agents read real project files and deliver visual-first reports with SVG/PNG/HTML diagrams."
---

# Java 项目架构分析（四阶段递进法）

## 目的

把"看懂一个 Java 项目"拆成 4 个递进阶段，让 Agent **主动读文件、画时序图、产出报告**，而不是把代码一股脑塞给用户去手动填空。覆盖从宏观架构识别到微观代码穿透、再到设计模式提炼与假设性重构的完整链路。

适用技术栈：Spring Boot / Spring Cloud / Spring Cloud Alibaba / MyBatis / MyBatis-Plus / JPA / Maven / Gradle 等主流 Java 工程。

## 何时触发

当用户出现以下意图之一时启用本 Skill：

- 想快速掌握一个陌生 Java/Spring 项目的整体架构
- 想梳理某条业务链路（如下单、登录、鉴权、支付回调）的代码流转
- 想学习项目中的设计模式与高可用/高性能实践
- 想对某模块做二次开发或技术替换（如本地缓存换 Redis、引入新框架、单体拆微服务）
- 触发关键词：分析架构、看懂项目、梳理链路、画时序图、提炼设计模式、重构、二次开发、源码学习

## 核心工作流：四阶段递进

四阶段**按需启用、逐级深入**，不必每次都跑完四阶段：

- 首次接触项目 → 从**阶段一**开始
- 已有架构认知、想看具体链路 → 直接进**阶段二**
- 想学设计精髓 → 用**阶段三**
- 要动手改造 → 用**阶段四**

每阶段开始前，**先向用户确认目标范围**（哪个项目目录、哪条业务链路、哪个模块），避免一次性吞掉整个代码库导致上下文爆炸。

四个阶段分别对应 `references/` 下四份详细 Prompt 模板，按当前阶段加载对应文件：

| 阶段 | 主题 | 参考文件 |
|------|------|---------|
| 一 | 骨架定位与架构全景 | `references/stage1-skeleton.md` |
| 二 | 关键数据流与时序还原 | `references/stage2-dataflow.md` |
| 三 | 架构设计与模式提炼 | `references/stage3-patterns.md` |
| 四 | 假设性重构与实战演练 | `references/stage4-refactor.md` |

---

## Codex 检索命令

本 skill 的检索示例默认使用 ripgrep：

```bash
rg --version
rg --files -g 'pom.xml'
rg -n '@Transactional' -g '*.java'
```

如果 `rg` 不可用，退回：

```bash
grep -rn '@Transactional' --include='*.java' .
findstr /s /n /c:"@Transactional" *.java
```

### 阶段一：骨架定位与架构全景

**目标：** 厘清技术选型、组件部署与业务边界，避免一上来就陷入细节。

**Agent 主动动作（不要等用户粘贴）：**
1. 用 `rg --files -g 'pom.xml' -g 'build.gradle' -g 'settings.gradle'` 定位构建文件
2. 用 `rg --files -g 'application*.yml' -g 'application*.properties' -g 'bootstrap*.yml'` 定位配置文件
3. 并行 Read 上述文件；多模块项目额外读根 pom 的 `<modules>` 段列出模块树
4. 用 `rg --files -g '*Application.java'` 确认 Spring Boot 主启动类与组件扫描范围

**必答 4 问（写入交付报告）：**
1. **技术栈清单**：分类列出核心框架、数据库、中间件（Redis/MQ/Nacos 等）、工具库，标明作用。
2. **业务模块推断**：根据数据源、包路径、第三方 Service 配置推断核心业务模块。
3. **架构模式分析**：单体 vs 微服务？是否分层架构、DDD、CQRS？给出结论 + 证据。
4. **运行依赖项**：本地拉起最少需要哪些基础设施（MySQL 版本、Redis、MQ、注册中心等）+ 启动顺序建议。

**交付物：** 工作目录写 `架构全景报告.md`。

详细模板见 `references/stage1-skeleton.md`。

---

### 阶段二：关键数据流与时序还原

**目标：** 看清数据在 Controller → Service → DAO/Cache/MQ 的全链路流转，避免逐行死磕代码。

**前置确认：** 问用户"想分析哪条业务主线"（如：用户下单、接口鉴权、支付回调）。

**Agent 主动动作：**
1. 用 `rg` 定位入口 Controller：`@RestController` + 业务关键词，或 `@RequestMapping("/xxx")` 路径
2. 沿调用链用 `rg` 追踪：Controller 调用的 Service 方法名 → Service 调用的 Mapper/Cache/MQ 方法
3. 并行 Read 链路上的核心类（Controller、Service Impl、Mapper、DTO、Entity）
4. 用 `rg` 扫描链路关键注解：`@Transactional`、`@Cacheable`/`@CacheEvict`、`@Async`、`@RabbitListener`/`@KafkaListener`、`@Scheduled`、分布式锁（Redisson `RLock`、`@Lock4j`、Redis `SETNX`）

**必答 3 问：**
1. **链路时序图**：用 Mermaid `sequenceDiagram` 语法，标明 Client → Controller → Service → Cache(Redis) → DB(MySQL) → MQ 之间的消息传递。按“Codex 可视化规范”生成可打开、可放大阅读的本地图像或 HTML；Mermaid 源码仅作为附录保留。
2. **数据流变**：说明输入参数（DTO/VO）如何校验、转换、最终映射为持久化对象（DO/Entity）。
3. **关键逻辑节点**：点出事务边界、并发锁、幂等性处理、异常兜底逻辑。

**交付物：** `链路时序分析.md`（含 Mermaid 源码 + 文字解读）。

详细模板见 `references/stage2-dataflow.md`。

---

### 阶段三：架构设计与模式提炼

**目标：** 反查高手的设计意图，学习可复用的模式与调优策略。

**前置确认：** 问用户"想重点剖析哪个模块/类"。

**Agent 主动动作：**
1. Read 用户指定的核心类/包代码
2. 用 `rg` 验证模式特征：
   - 工厂：`@Bean` + 接口、`FactoryBean`、`*Factory`
   - 策略：`Map<String, Strategy>`、`@Qualifier` 动态注入、`@Conditional`
   - 责任链：`@Order`/`@Component` + `next.handle()` 链式
   - 代理：AOP `@Aspect`、`InvocationHandler`、`Proxy.*newProxyInstance`
   - 模板方法：`abstract class` + `templateMethod()` + `doExecute()` 钩子
   - 观察者：`ApplicationEvent` + `@EventListener`/`@TransactionalEventListener`
   - 单例：`@Component`/`@Bean` 默认单例、双重检查锁 `volatile`
3. 用 `rg` 扫描性能/可用性代码：`@Cacheable`/`@CacheEvict`/`Caffeine`、`BloomFilter`/`@Preview`、`Semaphore`/`RateLimiter`/`@Sentinel`、`@Retryable`/`RetryTemplate`、`@Transactional(isolation=..., propagation=...)`

**必答 3 问：**
1. **设计模式识别**：用了哪些模式？分别解决什么解耦问题？给出类名 + 代码片段佐证。
2. **高可用/高性能设计**：如何处理缓存穿透/雪崩/击穿、高并发锁竞争、DB 压力、限流降级？
3. **亮点与瑕疵**：值得借鉴的优雅写法 + Code Review 发现的潜在性能瓶颈或不规范。

**交付物：** `设计模式与调优分析.md`。

详细模板见 `references/stage3-patterns.md`。

---

### 阶段四：假设性重构与实战演练

**目标：** 通过引入新需求或更换底层实现，在动手改造中检验对项目的掌握度。

**前置确认：** 问用户"改造目标是什么"（如：本地 JVM 缓存换 Redis、引入 LangChain4j 做对话记忆、单体拆微服务、引入 Seata 分布式事务）。

**Agent 主动动作：**
1. Read 原相关代码，定位改造影响面（哪些类/接口/配置要动）
2. 用 `rg` 找出被改造代码的所有引用点（`@Autowired`、`@Resource`、`@Qualifier`、构造注入），评估波及范围
3. 列出 Bean 注册方式（`@Bean`/`@Component`/`@Configuration`/`@Import`）和生命周期钩子（`@PostConstruct`/`DisposableBean`/`@PreDestroy`），预判容器坑

**必答 3 问：**
1. **改造方案设计**：要修改/新增哪些接口、类、配置？画出"改造前 vs 改造后"对比图，按“Codex 可视化规范”交付可打开、可放大阅读的本地 SVG/PNG/HTML。
2. **避坑指南**：Spring 容器依赖注入可能踩的坑——循环依赖、Bean 重名、`@Conditional` 失效、配置覆盖优先级（`application.yml` > `application-{profile}.yml` > 启动参数）、`@Transactional` 自调用失效、`@Async` 线程池耗尽、序列化兼容。
3. **步骤清单**：1-2-3-4 最小化修改步骤，可直接在 IDE 开 `feature/my-refactor` 分支实施。

**交付物：** `重构方案.md`（含步骤清单 + 风险提示）。

详细模板见 `references/stage4-refactor.md`。

---

## 工具使用要点

| 阶段 | 主要工具 | 典型用法 |
|------|---------|---------|
| 一 | `rg --files` + Read | 定位并读取 pom.xml / yml / 主启动类 |
| 二 | `rg` + Read + 本地 SVG/PNG/HTML | 沿调用链检索 + 生成 Mermaid 时序图和可打开图像 |
| 三 | `rg` + Read | 模式特征检索 + 代码精读 |
| 四 | `rg` + Read + 本地 SVG/PNG/HTML | 影响面分析 + 引用点扫描 + 改造前后对比图 |

**Context 控制：** 每次只选**一条完整业务主线**做阶段二/三，不要把整个项目代码塞进上下文。AI 上下文窗口有限，贪多必失。

## Codex 可视化规范

Codex App 的可视化主要依靠 **Markdown 渲染 + 工作区落盘文件 + 可点击绝对路径链接/图片标签**，而不是外部 widget 渲染器。当需要图形化表达时：

### 交付顺序

1. 先展示可读图：在报告和最终答复中，把 SVG/PNG/HTML 链接与图片预览放在 Mermaid 源码之前。
2. 再给文字解读：用 5-9 条要点解释主路径、分支、事务/缓存/MQ 等关键判断。
3. 最后放源码：Mermaid `.mmd` 只作为"可编辑源码/附录"，不要让用户第一眼看到源码块。

### 可视化文件

1. 必须生成可打开的本地可视化文件，优先级为：
   - `.svg`：适合架构图、时序图、模块依赖图、改造前后对比图。
   - `.png`：适合最终截图或需要固定像素展示的图。
   - `.html`：适合交互式图表、可折叠调用链、可搜索依赖图。
2. 在最终答复里使用 Markdown 链接引用本地文件：`[链路时序图.svg](</abs/path/链路时序图.svg>)`。若需要直接显示图片，可用 `![链路时序图](/abs/path/链路时序图.svg)`。
3. 渲染优先级：手写简洁 SVG（适合 10 个以内节点）→ 生成内嵌 Mermaid CDN 的自包含 HTML → Mermaid CLI。
4. 仅当本机已确认 `mmdc` 或 `npx -y @mermaid-js/mermaid-cli` 可用时再使用 Mermaid CLI。若用户明确要求交互式可视化，优先生成自包含 HTML 文件（内嵌 Mermaid/ECharts CDN 与必要交互脚本），让用户直接在浏览器打开。

### 可读性底线

1. 不要把复杂时序图压成一张小字横向泳道图。超过 6 个参与者、10 条消息、或 2 个条件分支时，优先改成"纵向分阶段链路图"或同时提供"总览图 + 详细图"。
2. 手写 SVG 时默认使用宽 1400-1800、高 1200-2400 的画布，正文最小 16px，关键节点 18-22px；每个阶段最多放 5-7 个视觉块。
3. 长标签必须换行，不要依赖用户放大才能读清；箭头文字短句化，把代码证据放到旁边说明或报告表格里。
4. Mermaid 源码保留完整调用细节；可视化图负责让用户看懂路径，不要求塞下每一行调用。

**交付物落盘：** 每阶段产出的 `.md` 报告写入工作目录；涉及图形的阶段同时写入 `.svg`/`.png`/`.html` 文件，并在最终答复中用可点击绝对路径链接呈现。

**进度可见：** 多阶段任务使用当前 Codex 可用的 `update_plan` 跟踪；每完成一阶段立刻标记 completed。

## 与面试准备的接力

若分析目的是面试项目准备，阶段二（链路时序）与阶段三（选型/模式决策）的报告可直接作为素材交接给 `java-backend-vibe-upskill`：把链路转化为"选型 → 实现 → 踩坑 → 落地 → 复盘"的场景案例与面试卡（用户说"把 XX 链路做成面试场景案例"，或 `$java-backend-vibe-upskill`）。本 skill 只负责"看懂"，不负责产出面试弹药。

## 触发示例

| 用户输入 | 启用阶段 |
|---------|---------|
| "分析这个 Spring Cloud 项目的整体架构" | 阶段一 |
| "帮我梳理用户下单的完整链路并画时序图" | 阶段二 |
| "学习这个项目里用的设计模式和高并发处理" | 阶段三 |
| "把本地缓存改成 Redis 分布式缓存，给我改造方案" | 阶段四 |
| "我想系统看懂这个开源项目" | 一 → 二 → 三 → 四 全流程 |
