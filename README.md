<h1 align="center">
  PeakDeskSprite
</h1>

<p align="center">
  基于 PySide6 的桌面宠物框架，用于构建可换装、可扩展、可陪伴的桌面角色
</p>

<p align="center">
  <a>
    <img src="https://img.shields.io/github/license/VectorPeak/PeakDeskSprite.svg">
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/downloads/VectorPeak/PeakDeskSprite/total.svg">
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg">
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/PeakDeskSprite-v0.8.5-green.svg">
  </a>
</p>

<p align="center">
  简体中文 | <a href="README_EN.md">English</a>
</p>

## 项目简介

PeakDeskSprite 是一只可以住在桌面上的小伙伴，也是一套面向开发者的桌宠框架。它把角色素材、动作状态、交互事件、背包物品、系统通知和可选 LLM 聊天能力组织在同一个 PySide6 桌面运行时里，让桌宠既能被直接使用，也能被继续改造成新的角色、动作和玩法

桌面宠物可以理解为一个“透明窗口上的状态机”：用户看到的是一个角色图片在桌面上移动、跳跃、互动，但程序内部真正运行的是一组状态、事件、定时器和资源配置

从工程上看，它大致是：

\[
\text{桌面宠物} = \text{Qt 窗口} + \text{动画帧} + \text{行为状态机} + \text{用户数据} + \text{事件响应}
\]

这里的“状态机”指的是角色会在不同状态间切换，比如 `stand -> walk -> drag -> fall -> focus`。每个状态对应一组图片帧、刷新间隔、触发条件和可能的副作用。反过来看，如果只把桌宠当成一张会动的图片，就很容易低估它真正的工程复杂度；更准确的理解是，图片只是状态机的可视化输出，配置、事件和数据才是它持续运行的骨架

## 效果演示

![Interface](https://raw.githubusercontent.com/VectorPeak/PeakDeskSprite/main/docs/PeakDeskSprite.png)

> 这里后续可以补充更多演示图片，例如桌宠主界面、角色导入、背包、通知气泡、设置面板、LLM 聊天和素材开发流程截图

## 快速上手

### Windows 用户

1. 打开 [GitHub Releases](https://github.com/VectorPeak/PeakDeskSprite/releases)
2. 下载当前版本的 Windows 发布包，文件名通常类似 `PeakDeskSprite-vX.Y.Z-windows-x64.zip`
3. 解压后双击 `PeakDeskSprite.exe` 启动桌宠

### 从源码运行

推荐使用 Python 3.9 环境运行源码版本。项目依赖写在 [requirements.txt](requirements.txt) 中：

```txt
apscheduler
pynput
PySide6-Fluent-Widgets
PySide6
tendo
Pillow>=11.0.0
```

安装和启动示例：

```powershell
conda create --name PeakDeskSprite_pyside python=3.9.18 -y
conda activate PeakDeskSprite_pyside
python -m pip install -r requirements.txt
python -m PeakDeskSprite
```

如果本机已经安装了兼容的 Python 3.9+，也可以使用虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m PeakDeskSprite
```

`Pillow>=11.0.0` 表示 Pillow 的最低版本要求是 11.0.0，不是只能安装 11.0.0。实际安装时 pip 可能会选择更新版本，只要满足 `>=11.0.0` 就符合要求

## 项目架构

PeakDeskSprite 的主线可以分成三层：最外层是用户能看到的透明 Qt 窗口和控制面板，中间层是动作、通知、背包、任务、LLM 等运行时功能，最内层是角色素材、配置文件和本机运行态数据

| 类别 | 模块 | 说明 |
| --- | --- | --- |
| 启动与应用生命周期 | `PeakDeskSprite/__main__.py` | 创建 `QApplication`，加载宠物、通知、附件、系统面板、仪表盘，并通过 Qt Signal 把它们连接起来 |
| 启动与应用生命周期 | 单实例控制 | 使用 `tendo.singleton.SingleInstance()` 防止重复启动；如果已有实例，后启动的进程会静默退出 |
| 启动与应用生命周期 | 多屏与午夜定时器 | 启动时读取屏幕列表，优先主屏，并设置跨日定时器，用于触发日常状态或事件刷新 |
| 桌面宠物运行时 | `PeakDeskSprite/PeakDeskSprite.py` | 主宠物窗口和运行时协调器，负责角色显示、动作切换、状态变化、鼠标交互和信号分发 |
| 桌面宠物运行时 | 动画动作系统 | 角色动作由 `act_conf.json` 与 `pet_conf.json` 配置，PNG 序列帧负责实际视觉表现 |
| 桌面宠物运行时 | 交互行为 | 支持点击、拖拽、跟随、掉落、拍打、专注动作等桌宠常见行为 |
| 角色与素材系统 | `res/role` | 角色主要放在这里，每个角色通常包含 `pet_conf.json`、`act_conf.json`、`action/*.png`、`info` 等内容 |
| 角色与素材系统 | `res/pet` | 兼容旧的迷你宠物结构，说明项目经历过从宠物素材到角色模块的结构演进 |
| 角色与素材系统 | `PeakDeskSprite/conf.py` | 负责读取角色、动作、物品、存档等配置，是项目的领域配置核心 |
| 通知与气泡 | `PeakDeskSprite/Notification.py` | 管理弹窗通知、气泡显示、日志转发等 |
| 通知与气泡 | `PeakDeskSprite/bubbleManager.py` | 管理不同事件触发的对话气泡，例如饱食度、好感度、点击、专注等 |
| 通知与气泡 | LLM 气泡接入 | 气泡系统可以在特定事件下请求 LLM 生成短文本，再回填到桌宠气泡中 |
| 附件与子宠物 | `PeakDeskSprite/Accessory.py` | 管理装饰物、掉落物、子宠物、鼠标装饰等窗口对象 |
| 附件与子宠物 | 子宠物跟随 | 子宠物可以跟随主宠物、关闭跟随、回收或独立显示，是“主角色 + 附属对象”的扩展模型 |
| 仪表盘功能 | `PeakDeskSprite/Dashboard/DashboardUI.py` | 提供状态、背包、商店、每日任务、动画管理几个页签 |
| 仪表盘功能 | 状态与 Buff | 状态页显示 HP、FV、金币、Buff 等，背包物品可以影响这些状态 |
| 仪表盘功能 | 背包与商店 | 背包管理物品，商店负责购买和出售，二者通过信号同步金币和物品数量 |
| 仪表盘功能 | 任务与专注 | 任务页包含番茄钟、专注时间、进度任务、每日任务，并可以发放金币奖励 |
| 系统设置面板 | `PeakDeskSprite/SpriteSettings/SpriteControlPanel.py` | 系统设置主窗口，包含设置、聊天、大模型服务、存档、角色、物品 MOD、迷你宠物等页签 |
| 系统设置面板 | `CharCardUI.py` | 负责角色导入、切换和卡片展示 |
| 系统设置面板 | `ItemCardUI.py` | 负责物品 MOD 管理 |
| 系统设置面板 | `GameSaveUI.py` | 支持存档、读取、回退和删除 |
| LLM 功能 | `PeakDeskSprite/llm_client.py` | 内置 OpenAI、DeepSeek、Ollama、Custom 四类 OpenAI-compatible Provider 预设 |
| LLM 功能 | `LLMChatUI.py` | 提供宠物聊天界面，支持保存聊天记录 |
| LLM 功能 | 安全边界 | API Key 优先从环境变量读取，也可以保存到运行时数据目录的 `llm_secrets.json` |
| 打包与工具 | PyInstaller 打包 | 发布流程围绕 Windows 可执行文件和发布包审计展开 |
| 打包与工具 | `tools/` | 包含 HatchPet 转换辅助，用于把其他宠物素材转换成 PeakDeskSprite 结构 |
| 打包与工具 | `docs/` | 包含源码结构、依赖结构、素材开发、发布清单等开发文档 |

更详细的源码结构和依赖关系可以阅读 [源码结构说明](docs/source_architecture.md) 与 [依赖结构图](docs/source_dependency_map.md)

## 配置

项目配置大致分为三类：仓库内的默认资源配置、本机运行态配置、以及可选的 LLM 服务配置

| 类型 | 位置 | 说明 |
| --- | --- | --- |
| 默认角色与素材 | `res/role`、`res/pet`、`res/icons` | 随项目分发，包含角色动作、头像、气泡、图标、物品等默认资源 |
| 角色动作配置 | `pet_conf.json`、`act_conf.json` | 描述角色基础属性、动作集合、帧刷新、移动、锚点和触发条件 |
| 运行态配置 | Windows 下默认位于 `%APPDATA%\PeakDeskSprite` | 存放用户设置和运行态数据；可以通过 `PEAKDESKSPRITE_CONFIG_DIR` 覆盖 |
| 运行态数据 | `%APPDATA%\PeakDeskSprite\data` | 存放 `settings.json`、`pet_data.json`、`act_data.json`、`task_data.json` 等用户数据 |
| LLM API Key | 环境变量 `PEAKDESKSPRITE_LLM_API_KEY` 或 `llm_secrets.json` | 环境变量优先，未配置时才读取本机运行态数据目录里的密钥文件 |
| LLM 聊天记录 | `llm_chat_history.json` | 保存在本机运行态数据目录，不应提交到公开仓库或公开 issue |

如果要开发新的宠物形象、动作、道具或迷你宠物，请先阅读 [素材开发文档](docs/art_dev.md) 和 [HatchPet 转换说明](docs/hatchpet_converter.md)

如果要修改运行时、设置面板、通知、背包、LLM 或发布流程，请先阅读 [源码结构说明](docs/source_architecture.md)、[依赖结构图](docs/source_dependency_map.md)、[参与贡献](CONTRIBUTING.md)、[Windows 发布清单](docs/release_checklist.md)、[安全报告](SECURITY.md) 与 [第三方与素材授权说明](NOTICE.md)

## 常见问题

### 这是一个网页项目吗

不是。PeakDeskSprite 是 PySide6 桌面 GUI 应用，启动后显示的是桌面窗口、系统面板和托盘相关交互，不会提供 localhost 网页地址

### 为什么推荐 Python 3.9

Qt 桌面应用对 Python、PySide6 和本机 DLL 兼容性更敏感。Python 3.9 是当前更稳妥的运行环境；过新的 Python 版本可能遇到 QtCore 等动态库加载问题

### `Pillow>=11.0.0` 是什么意思

这是版本下界，含义是安装 Pillow 11.0.0 或更高版本。它不是精确锁定版本，也不表示必须手动安装 11.0.0。Pillow 主要用于图片读取、处理和素材相关流程

### 为什么启动第二次没有反应

项目使用 `tendo.singleton.SingleInstance()` 做单实例保护。如果已经有一个 PeakDeskSprite 进程在运行，后启动的进程会退出，避免桌面上同时出现多个互相争用配置和资源的实例

### LLM 会把哪些内容发给服务商

LLM 功能是可选功能。启用后，桌宠会把用户输入、必要的聊天上下文、角色提示词和事件文本发送到用户配置的 LLM 服务商。API Key 优先从环境变量读取，也可保存在本机运行态配置目录，聊天记录保存在本机运行态数据目录

请不要在公开 issue、日志、截图或 PR 中粘贴 API Key、聊天记录、服务商返回体或未脱敏的本机路径

### 素材授权需要注意什么

项目代码遵循仓库内的 [LICENSE](LICENSE)。默认素材、示例素材、第三方角色/物品模组、外部字体/图标/音频和用户自行导入的素材可能有独立授权边界。分发或二次创作前请阅读 [NOTICE.md](NOTICE.md)

## 开发者文档与贡献边界

公开仓库欢迎以下类型的贡献：

- 反馈桌宠启动、资源加载、角色导入、背包、通知或设置面板问题
- 补充角色、物品模组、迷你宠物、文档示例或截图说明
- 修复路径兼容、发布包审计、资源定位、UI 行为和 smoke test 问题
- 讨论 LLM 聊天、角色气泡、上下文管理和本地隐私边界

提交代码前请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。如果你发现安全或隐私相关问题，请优先按照 [SECURITY.md](SECURITY.md) 的说明私下报告

PeakDeskSprite 的定位不是一个只绑定某个形象的小程序，而是一个可以不断换衣服、换动作、换道具、换性格的桌宠底座。使用者可以把它当作桌面陪伴应用，素材作者可以把它当作角色素材实验室，开发者则可以把它当作交互 Demo 原型或轻量桌面工具的起点

## 致谢

- 基于 [ChaozhongLiu/DyberPet](https://github.com/ChaozhongLiu/DyberPet) 底座进行二次开发
- UI 重构基于 [Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)，感谢作者 [zhiyiYo](https://github.com/zhiyiYo) 的指导和帮助
- Demo 中的部分素材来自 [daywa1kr](https://github.com/daywa1kr/Desktop-Cat)
- 框架早期的动画模块逻辑参考了 [yanji255](https://toscode.gitee.com/yanji255/desktop_pet/)
- 框架拖拽掉落的计算逻辑参考了 [WolfChen1996](https://github.com/WolfChen1996/DesktopPet)
