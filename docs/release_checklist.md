# PeakDeskSprite Windows Release Checklist

## 目标

第一阶段 release 只解决两件事：可复现构建、发布包内容可审计。

构建脚本默认使用本机已验证的 conda Python：

```powershell
D:\ZXY\Dev\Miniconda3\envs\Dyber_pyside\python.exe
```

输出位置固定为 `release-work\dist`，最终压缩包固定为 `release-work\PeakDeskSprite-windows-x64.zip`。`release-work/` 是构建产物目录，不进入 Git。

## 构建命令

在仓库根目录执行：

```powershell
.\scripts\build_release.ps1
```

脚本会执行：

1. 清理 `release-work\dist`、`release-work\build`、`release-work\spec`。
2. 使用 `python -m PyInstaller --clean --noconfirm` 构建 `run_PeakDeskSprite.py`。
3. 将 PyInstaller 输出写入 `release-work\dist\PeakDeskSprite`。
4. 审计未压缩发布目录。
5. 压缩为 `release-work\PeakDeskSprite-windows-x64.zip`。
6. 审计 zip 包。

如只想重新审计已有包：

```powershell
.\scripts\audit_release_package.ps1 -PackagePath .\release-work\dist\PeakDeskSprite
.\scripts\audit_release_package.ps1 -PackagePath .\release-work\PeakDeskSprite-windows-x64.zip
```

## 内容黑名单

release 包不允许包含：

- `data`
- `logs`
- `build`
- `dist`
- `llm_secrets.json`
- `llm_chat_history.json`
- `.env`、`*.env`
- `__pycache__`
- `*.pyc`
- 旧工具目录 `peakdesk-sprite`

审计脚本只报告命中的相对路径，不读取或输出敏感文件内容。

## 预期产物

- `release-work\dist\PeakDeskSprite\PeakDeskSprite.exe`
- `release-work\PeakDeskSprite-windows-x64.zip`

`data` 属于用户运行态配置目录，不应进入发布包。LLM 服务商地址、模型名、API Key 和聊天记录也不应进入发布包。

## 发布前检查

```powershell
git status --short --branch
git check-ignore -v data logs dist build release-work **/llm_secrets.json **/llm_chat_history.json
git ls-files data logs dist build release-work
D:\ZXY\Dev\Miniconda3\envs\Dyber_pyside\python.exe -m compileall PeakDeskSprite run_PeakDeskSprite.py tools scripts
.\scripts\build_release.ps1
```

构建完成后启动 `release-work\dist\PeakDeskSprite\PeakDeskSprite.exe` 做一次冒烟检查，确认程序能保持运行、设置面板可打开，并且发布目录没有携带 `data`。
