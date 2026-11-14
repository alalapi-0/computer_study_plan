# Architecture · 问题工作台

> 2026-10-13 · 实现/验收状态见PROJECT_STATE。

## 边界与复用

`index.html` / `practice_ui.js` / `practice_ui.css` 是主问题清单和练习工作区；`progress.html` 及原JS/CSS继续承载历史课程，避免把80任务的done混成独立解决。现有Python服务同时提供受控静态材料、旧进度API和独立 `/api/lab/*`。无数据库、账号、前端框架、云依赖或在线判官。

`content/scenarios/<id>/scenario.json` 是版本化题面，含id/version、症状/目标/约束、真实环境组合、来源改编、提示步骤与解答；`setup.sh` 和 `check.py` 是可信维护者审查后运行的包。目录名必须匹配稳定id；不允许symlink包。全运行门禁成功后生成 `content/scenarios/publication.json`，绑定包摘要和实际工具版本；缺记录或内容/环境变化时显示待复验并禁止启动。受信维护者可用 `python3 scripts/validate_scenarios.py --runtime --publish`重新发布；不是上传或签名服务。测试与发布验证显式validation_mode，只用临时数据，不作为正常服务绕过入口。运行时保存内容摘要和工具版本，后续包更新不改变历史题目身份。

## 环境与会话

`LabManager` 独占本任务state root的文件锁，进程内序列化生命周期；一次一个实验。启动其他题会结束旧环境且保留Attempt。Bubblewrap建立独立user/PID/net/IPC/UTS等namespace，丢弃capability，禁止嵌套userns，只读系统工具、清空继承环境。只有 `/workspace` 可持久写入题目数据，`/tmp`是临时；没有宿主home、仓库、etc、run、socket、密钥或真实设备挂载。只用已有工具，无安装和宿主Shell回退。

setup在同等隔离中挂载题包；用户Shell不挂载题包/解答/检查器。独立检查namespace挂载可信检查器、只读原工作副本和可丢弃的验证快照，判定目标和保护数据；通过有界no-follow复制保留必要模式，实际代码只在验证快照中运行，不能修改live题目或获得管理端权限。无用户HTML预览服务，因此没有将实验脚本放入管理会话执行的路径。后续预览须分离origin/权限。

PTY由系统pseudo-terminal连接真实Bash，用xterm解析终端控制序列；HTTP输入、输出游标、resize、CtrlC和快照不伪造Shell结果。浏览器刷新只获取当前同一live Attempt快照；结束/失效历史只能作为历史，不能当活会话。终端文本/题面/证据用安全文本节点呈现，关闭链接执行。系统VM/macOS/Windows、双节点网络不在此adapter范围。

限制必须按实际语义显示：每进程地址空间/CPU/文件/进程数/FD限制、总会话寿命、输出与工作副本64MiB/10000条目监测；不是完整cgroup总RAM/CPU硬配额，也不保证所有恶意代码绝对安全。面向可信本机学习，不开放公网/多用户。

## 数据与恢复

新Attempt和幂等身份以原子replace+fsync存于Git忽略的 `.lab-runtime/attempts.json`，workspace在该root的owned attempt目录；保留scenario版本/摘要、时间、环境状态、提示/解答使用与检查证据。输入的投递事实不能冒充命令执行成功。生命周期保留操作身份，不确定响应同输入重试，换输入不能复用id。服务重启不能重建旧PTY，原active转lost；reset生成新Attempt并保留旧记录，停止与回收仅处理已核实任务目录/进程。

旧 `progress.json`/镜像、`records/action_logs`/feedback/terminal/saves、revision和CLI继续由原progress_lib维护。启动新服务不自动sync写入旧进度；旧API仍按原事务恢复。旧存档不包含新Attempt，不覆盖其历史。原done不迁成新尝试、检查通过、无提示独立解题或Mastery。生成镜像仅原生成器更新。

## HTTP与浏览器权限

服务只绑定 `127.0.0.1`；Host必须是本端口的127.0.0.1或localhost，Origin精确匹配且拒绝cross-site。写请求必须JSON；实验API使用服务器内存能力token，bootstrap仅同源可读，token不进入URL/磁盘。允许本机可信CLI发无Origin请求，非多用户鉴权方案。静态白名单拒绝遍历、symlink、私有状态/Git/服务代码/题目检查器/实验文件，HEAD同样受限。CSP、nosniff、frame拒绝、无referrer；新页面不需inline脚本。旧页面保留inline脚本的兼容CSP。

## 契约与验证

GET `/api/lab/bootstrap` 提供token/capabilities/scenarios；GET history与Attempt cursor；POST start和Attempt input/resize/check/view/stop/reset。JSON严格字段和操作身份，正式API由HTTP安全测试覆盖。场景schema/发布门禁见validate_scenarios；真实环境/PTY/状态见test_lab_runtime；旧进度与运行事务保留；浏览器分别用内存fixture与临时真实runtime验证。既有fixedUI沙箱禁止nested userns，故真实PTY联调单独以守卫核验后的固定Python/Chromium、headless专属context和临时state运行，原UI隔离守卫不变；测试仅请求任务本地服务，不能宣称这条额外联调具有原外层网络namespace隔离。根控制面最终以精确候选摘要绑定Judge与Governor，结果只记入PROJECT_STATE。

选型依据：[Bubblewrap边界说明](https://github.com/containers/bubblewrap)、[Python PTY](https://docs.python.org/3/library/pty.html)、[xterm安全指导](https://xtermjs.org/docs/guides/security/)、[Killercoda题包机制](https://killercoda.com/creators)。组件与Shell/环境分层，实际边界必须本机实测；这些资料不是运行证据。
