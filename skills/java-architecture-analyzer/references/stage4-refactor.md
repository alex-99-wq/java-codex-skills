# 阶段四：假设性重构与实战演练 · 详细 Prompt 模板

> 本文件供 Agent 在执行阶段四时加载，提供影响面分析方法、Spring 容器避坑清单与最小化改造步骤模板。

## 角色与目标

你是一名技术导师。用户已基本看懂某模块的业务逻辑，现在想做二次开发或技术替换改造。你的任务是给出可落地的改造方案、列出潜在踩坑、提供 IDE 可直接执行的最小步骤清单。

## 前置确认

阶段四开始前**必须问用户**：

> "改造目标是什么？常见类型：
> - 缓存替换：本地 JVM 缓存（Caffeine/Guava）→ 分布式 Redis 缓存
> - 框架引入：引入 LangChain4j 实现对话记忆 / 引入 Seata 分布式事务 / 引入 ShardingSphere 分库分表
> - 架构演进：单体拆微服务 / 引入网关 / 引入配置中心
> - 协议替换：HTTP 调用 → Dubbo RPC / WebSocket → SSE
> - 数据源切换：单库 → 读写分离 / 多数据源动态切换
> - 其他自定义需求
>
> 告诉我你的目标，并指出现有代码位置。"

## Agent 主动动作

### 1. 定位改造影响面

Read 原相关代码，识别"改造前"的实现细节：
- 接口签名（什么方法、什么入参、什么返回值）
- 实现类（具体类还是接口多实现）
- 配置项（yml / properties）
- 调用方（哪些类调用了它）

### 2. 用 rg 扫描所有引用点

```bash
# 字段注入引用
rg -n '@Autowired.*oldService|@Resource.*oldService' -g '**/*.java'

# 构造注入引用
rg -n 'private final.*OldService|OldService\s+\w+;' -g '**/*.java'

# 直接调用
rg -n 'oldService\.\w+\(' -g '**/*.java'
```

每个引用点记录：所在类、方法、调用方式，用于波及范围评估。

### 3. Bean 注册与生命周期预判

```bash
# 注册方式
rg -n '@Bean|@Component|@Service|@Configuration|@Import|@ImportResource' -g '**/*.java'

# 生命周期钩子
rg -n '@PostConstruct|@PreDestroy|DisposableBean|InitializingBean|SmartInitializingSingleton' -g '**/*.java'

# 配置覆盖优先级线索
rg -n '@ConfigurationProperties|@Value' -g '**/*.java'
rg -n 'spring\.profiles\.active' -g '**/*.yml'
```

## 必答 3 问

### 1. 改造方案设计

输出"改造前 vs 改造后"对比：

#### 改造前
```
- 接口：CacheService (本地缓存接口)
- 实现：LocalCacheServiceImpl (用 Caffeine)
- 配置：spring.cache.type=simple
- 调用方：OrderService#saveOrder 中调用 cacheService.get(key)
```

#### 改造后
```
- 接口：CacheService (保持不变，对调用方透明)
- 实现：RedisCacheServiceImpl (用 RedisTemplate)
- 新增：RedisConfig（连接池、序列化器、Key 前缀）
- 修改：application.yml 增加 spring.redis.host/port/password
- 调用方：无需改动（接口不变）
```

#### 类与配置清单
| 类型 | 操作 | 名称 | 说明 |
|------|------|------|------|
| 新增 | 类 | RedisConfig | Redis 连接配置 + 序列化 |
| 新增 | 类 | RedisCacheServiceImpl | 实现 CacheService |
| 删除 | 类 | LocalCacheServiceImpl | 注释掉或物理删除 |
| 修改 | yml | application.yml | 增加 spring.redis.* |

#### 改造前后对比图
按 Codex 可视化规范生成改造前 vs 改造后的结构对比图（左右两栏），优先落盘为 `改造前后对比图.svg`，让用户一眼看清差异；报告中同时保留 Mermaid/Graphviz/文本图源码。

### 2. 避坑指南

按场景给出可能的坑：

#### Spring 容器 DI 坑

- **循环依赖**：A 注入 B、B 注入 A。Spring Boot 2.6+ 默认禁用循环依赖，会启动失败。
  - 解法：用 `@Lazy`、改构造注入为 setter 注入、或重构为事件解耦。
- **Bean 重名冲突**：`@Service("cacheService")` 同名 Bean。
  - 解法：起不同名（`@Service("redisCache")`），或用 `@Primary` 标记默认实现。
- **`@Conditional` 失效**：条件 Bean 的条件在 `@Configuration` 解析时才评估，迟于 `@Import`。
  - 解法：检查 `@ConditionalOnProperty` 的 `matchIfMissing` 配置。
- **配置覆盖优先级**：命令行参数 > 环境变量 > `application-{profile}.yml` > `application.yml` > 默认值。
  - 解法：调试时用 `actuator/env` 端点查看生效配置。

#### `@Transactional` 失效场景

- 自调用：同类内 A 方法调 B 方法，B 的 `@Transactional` 失效（未走代理）。
  - 解法：拆到两个类、或注入自身代理 `((XxxService) AopContext.currentProxy()).b()`。
- `private` / `final` 方法：CGLIB 无法代理。
- 异常被吞：`try-catch` 内吞了异常未再抛，事务不回滚。
- 抛非 RuntimeException：默认不回滚，需 `rollbackFor = Exception.class`。
- 异步方法：`@Async` + `@Transactional` 异步线程无事务上下文。

#### `@Async` 坑

- 线程池耗尽：默认 `SimpleAsyncTaskExecutor` 每次新建线程，高并发 OOM。
  - 解法：自定义 `ThreadPoolTaskExecutor` 并 `@Bean("taskExecutor")`。
- 跨线程上下文丢失：`ThreadLocal` / `RequestContextHolder` / Security 上下文丢失。
  - 解法：用 `TaskDecorator` 复制上下文。

#### 序列化兼容

- Redis 序列化器：默认 JdkSerializationRedisSerializer 需实现 Serializable，且跨语言不友好。
  - 推荐：`GenericJackson2JsonRedisSerializer` + 类型信息。
- 字段增删导致反序列化失败：旧缓存 value 反序列化新类报错。
  - 解法：版本号字段 + 兼容反序列化、或灰度期间换 Key 前缀。

#### 数据迁移与平滑过渡

- 数据从本地缓存迁 Redis：上线时是否要预热？是否双写一段时间？
- 单体拆微服务：先 Strangler Pattern 渐进式替换，不要一刀切。

### 3. 步骤清单

输出**可直接在 IDE 执行**的最小化步骤，每步给文件级粒度：

```
1. 开分支
   git checkout -b feature/cache-to-redis

2. 新增 Redis 配置类
   路径：src/main/java/com/xxx/config/RedisConfig.java
   内容：
   - @Configuration
   - @Bean RedisTemplate<String, Object>（GenericJackson2JsonRedisSerializer）
   - @Bean StringRedisTemplate
   - @Bean CacheManager（spring-cache 集成）

3. 新增 Redis 实现类
   路径：src/main/java/com/xxx/service/impl/RedisCacheServiceImpl.java
   内容：实现 CacheService 接口，所有方法委托 RedisTemplate
   - @Service("redisCache")
   - @Primary （让 Spring 优先注入此实现）

4. 修改 application.yml
   增加：
   spring:
     redis:
       host: ${REDIS_HOST:127.0.0.1}
       port: 6379
       password: ${REDIS_PASSWORD:}
       lettuce:
         pool:
           max-active: 8

5. （可选）删除/注释旧实现
   路径：src/main/java/com/xxx/service/impl/LocalCacheServiceImpl.java
   操作：类上加 @Profile("local") 仅本地启用，避免删除影响他人

6. 启动验证
   - 启动 Redis（docker run -p 6379:6379 redis:7）
   - 启动应用
   - 调用接口验证缓存生效
   - 用 redis-cli 查 Key 验证数据结构

7. 单元测试补充
   路径：src/test/java/com/xxx/service/RedisCacheServiceImplTest.java
   - 用 embedded redis（it.ozimov:embedded-redis）或 Testcontainers
   - 覆盖：get 命中、get 未命中、set、evict、TTL 过期
```

要点：
- 每步**给绝对路径**，用户在 IDE 中可直接定位
- 步骤之间**有依赖顺序**（先建配置再建实现、先实现再调用、最后验证）
- **每步可独立 commit**，便于回滚
- 给出**验证方式**（命令、端点、断点）

## 交付格式

写入工作目录 `重构方案.md`：

```markdown
# {改造目标} 重构方案

> 改造目标：{一句话描述}
> 影响模块：{列表}
> 风险等级：低/中/高

## 一、改造方案设计
### 改造前
### 改造后
### 类与配置清单
### 改造前后对比图
（本地 SVG/PNG/HTML 链接 + 图中关键变化说明）

## 二、避坑指南
### Spring 容器 DI 坑
### @Transactional 失效场景
### @Async 坑
### 序列化兼容
### 数据迁移

## 三、步骤清单
1. ...
2. ...
（每步：路径、操作、验证方式）

## 四、回滚方案
（若改造失败如何快速回退）
```

## 注意事项

- **不要只给理论**：所有步骤必须有具体类名、路径、关键代码片段，可直接在 IDE 落地。
- **波及范围要算清**：改一个 Bean 可能影响 N 个调用方，必须用 `rg` 找出所有引用点告知用户。
- **风险等级要标**：低（接口不变，实现替换）/ 中（接口扩展，部分调用方需改）/ 高（接口破坏性变更或架构级重构）。
- **回滚方案必备**：用户在 IDE 里动手可能有报错，必须给回退路径（如保留旧实现加 `@Profile`、或开 feature 分支失败就删）。
