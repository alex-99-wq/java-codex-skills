# 阶段一：骨架定位与架构全景 · 详细 Prompt 模板

> 本文件供 Agent 在执行阶段一时加载，提供详细的角色设定、读取策略、四问模板与交付格式。
> SKILL.md 已给出阶段概览，这里是不必每次加载的细节。

## 角色与目标

你是一名资深 Java 架构师。用户正在学习一个开源/企业级 Java 项目，需要快速掌握其整体架构。你的任务是用工具主动读取项目真实文件，基于事实给出分析，而不是让用户手动粘贴配置。

## Agent 主动读取策略

回答前先用以下方式收集事实，**禁止凭空推断**：

### 1. 构建文件定位（rg --files）

```bash
rg --files -g 'pom.xml' -g 'build.gradle' -g 'settings.gradle' -g 'gradle.properties'
```

目标文件：
- `pom.xml`（Maven 工程主依赖）
- `build.gradle` / `settings.gradle`（Gradle 工程）
- `gradle.properties`（Gradle 版本统一管理）

读取后提取：
- Spring Boot / Spring Cloud / Spring Cloud Alibaba 的 `<parent>` 或 `dependencyManagement` 版本
- `<dependencies>` 中所有业务依赖（按 groupId 分类）
- `<modules>` 段（多模块项目）→ 列出子模块名与层级

### 2. 配置文件定位（rg --files）

```bash
rg --files -g 'application*.yml' -g 'application*.properties' -g 'bootstrap*.yml' -g 'bootstrap*.properties' -g 'nacos-*.properties' -g 'logback*.xml' -g 'sentinel-*.json'
```

目标文件：
- `application*.yml` / `application*.properties`（主配置）
- `bootstrap*.yml` / `bootstrap*.properties`（Spring Cloud 启动配置）
- `application-{profile}.yml`（环境隔离配置）
- `nacos-*.properties` / `logback*.xml` / `sentinel-*.json`

读取后提取：
- `spring.datasource.*`（数据源、连接池类型）
- `spring.redis.*` / `spring.data.redis.*`（缓存）
- `spring.rabbitmq.*` / `spring.kafka.*` / `spring.rocketmq.*`（消息中间件）
- `spring.cloud.nacos.*` / `eureka.client.*`（注册中心）
- `spring.cloud.sentinel.*`（熔断限流）
- `mybatis.*` / `mybatis-plus.*`（ORM 配置）
- 自定义业务配置项（`xxx.*`）→ 推断业务模块

### 3. 启动类定位（rg --files）

```bash
rg --files -g '*Application.java' -g '*Provider*.java' -g '*Consumer*.java'
```

目标文件：
- `*Application.java`（含 `@SpringBootApplication`）
- `*Provider*.java`（Dubbo 服务提供方）
- `*Consumer*.java`（Dubbo 服务消费方）

读取后提取：
- `@SpringBootApplication(scanBasePackages = ...)` → 组件扫描范围
- `@EnableXxx` 系列注解（`@EnableFeignClients`、`@EnableDiscoveryClient`、`@EnableScheduling`、`@EnableAsync`、`@EnableCaching`）

### 4. 多模块结构
若根 pom 含 `<modules>` 段：
- 列出所有子模块名
- 读各子模块 pom 的 `<dependencies>` 提取模块间依赖关系
- 画出模块依赖树：在报告中保留 Mermaid/文本树源码，并按 Codex 可视化规范生成本地 SVG/PNG/HTML 后用绝对路径链接呈现。

## 四问模板

### 1. 技术栈清单

分类列出，每项标明作用。用表格形式：

| 类别 | 组件 | 版本 | 作用 |
|------|------|------|------|
| 核心框架 | Spring Boot | 2.7.18 | 应用骨架、自动配置 |
| 核心框架 | Spring Cloud Alibaba | 2021.0.5.0 | 微服务套件 |
| 数据库 | MySQL | 8.0（驱动版本推断） | 主库 |
| 数据库连接池 | Druid | 1.2.20 | 数据源监控 |
| ORM | MyBatis-Plus | 3.5.5 | 持久层 |
| 中间件 | Redis | 6.x | 缓存、分布式锁 |
| 中间件 | RabbitMQ | 3.11 | 异步解耦 |
| 中间件 | Nacos | 2.2 | 注册中心 + 配置中心 |
| 中间件 | Sentinel | 1.8.6 | 熔断限流 |
| 工具库 | Lombok | - | 样板代码消除 |
| 工具库 | MapStruct | 1.5.5 | DTO/DO 转换 |
| 工具库 | Hutool | 5.8.25 | 工具集 |

### 2. 业务模块推断

依据三类信号：
- **数据源配置**：多数据源 → 多业务域；`spring.datasource.dynamic.datasource.*` 命名
- **包路径**：`com.xxx.user`、`com.xxx.order`、`com.xxx.payment`、`com.xxx.inventory`
- **第三方 Service 配置**：`aliyun.oss.*`（对象存储）、`aliyun.sms.*`（短信）、`wechat.pay.*`（支付）、`tencent.im.*`（IM）

输出模块树 + 每模块职责说明。

### 3. 架构模式分析

判断维度：

| 维度 | 单体特征 | 微服务特征 |
|------|---------|-----------|
| 注册中心 | 无 nacos/eureka 配置 | 有 `spring.cloud.nacos.discovery.*` |
| 服务调用 | 同 JVM 直接 `@Autowired` | `@FeignClient`、`RestTemplate` + `@LoadBalanced` |
| 配置中心 | 仅 `application.yml` | `bootstrap.yml` + Nacos Config |
| 网关 | 无 | `spring-cloud-starter-gateway` |
| 数据库 | 单库 | 每服务一库 |

进一步判断：
- **分层架构**：Controller/Service/Mapper 标准三层 → 是
- **DDD**：`domain/`（聚合根、值对象）、`application/`（应用服务）、`infrastructure/`（基础设施）、`interfaces/`（接口适配）四包结构 → 是
- **CQRS**：查询用 MyBatis 读从库、写用 JPA 写主库、`query/` 与 `command/` 分离 → 是

给出结论 + 代码证据。

### 4. 运行依赖项

从配置反推本地拉起最少依赖：

- **MySQL**：从 `mysql-connector-java` 版本推断兼容的 MySQL Server 版本（5.7 / 8.0+）
- **Redis**：是否必须？是否用于 session、缓存、分布式锁
- **MQ**：RabbitMQ / Kafka / RocketMQ / Pulsar，是否必须
- **注册中心**：Nacos / Consul / Eureka，版本要求
- **配置中心**：是否依赖 Nacos Config（启动时拉取配置）
- **其他**：Elasticsearch、MinIO、Seata、Zipkin、SkyWalking、Sentinel Dashboard

输出**启动顺序建议**：例如 Nacos → MySQL → Redis → RabbitMQ → 用户服务 → 订单服务 → 网关。

## 交付格式

写入工作目录 `架构全景报告.md`：

```markdown
# {项目名} 架构全景报告

> 生成时间：{timestamp}
> 分析范围：{项目根路径}

## 一、技术栈清单
（表格）

## 二、业务模块推断
### 模块树
（树形或依赖图）
### 模块职责
（每模块一段说明）

## 三、架构模式分析
- 架构类型：{单体 / 微服务 / 模块化单体}
- 设计范式：{分层 / DDD / CQRS}
- 证据：（配置片段 + 包结构）

## 四、本地运行依赖
### 基础设施清单
- MySQL 8.0+
- Redis 6.x
- ...
### 启动顺序建议
1. 启动 Nacos
2. 启动 MySQL、Redis、RabbitMQ
3. ...
```

## 注意事项

- **不要凭空推断版本**：所有版本号必须来自 pom.xml 或 yml 的真实内容。
- **多模块项目优先列模块树**：用户最关心的是"这个项目由哪些部分组成"。
- **运行依赖项要给可执行命令**：如能给出 `docker run` 命令更佳，但不要臆造镜像名。
