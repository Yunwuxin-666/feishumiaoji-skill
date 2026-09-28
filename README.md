# 妙记课程剪辑技能包

把 AIGC 课程制作流程整理成可复用技能：从课程大纲和飞书资料中选录播、定位片段，精剪课程视频，上传云盘生成妙记，并回传单节课文档。

## 包含什么

| 路径 | 用途 |
|---|---|
| `skills/妙计.skill/` | 编排完整制作流程：大纲、资料检索、选材、剪辑、妙记和文档回传 |
| `skills/口播剪辑.skill/` | 课程视频的语义精剪、口癖清理、字幕、章节进度条与验收 |
| `skills/剪辑.skill/` | 可选：需要叙事转场或多镜头衔接时使用 |
| `dependencies/lark-cli-skill-snapshots/` | Lark CLI 技能和参考文档快照，供离线查阅；不是要复制到 Codex 技能目录的技能 |
| `妙计剪辑流程技能包.zip` | 同一套文件的压缩包 |

## Windows 安装（Git）

需要先安装 Git 和 Codex。打开 PowerShell，依次运行：

```powershell
$repo = Join-Path $env:USERPROFILE '.codex\skill-sources\feishumiaoji-skill'
$skills = Join-Path $env:USERPROFILE '.codex\skills'
New-Item -ItemType Directory -Force -Path (Split-Path $repo) | Out-Null
New-Item -ItemType Directory -Force -Path $skills | Out-Null
git clone https://github.com/Yunwuxin-666/feishumiaoji-skill.git $repo
Copy-Item "$repo\skills\妙计.skill" $skills -Recurse -Force
Copy-Item "$repo\skills\口播剪辑.skill" $skills -Recurse -Force
Copy-Item "$repo\skills\剪辑.skill" $skills -Recurse -Force
```

安装后，技能目录应直接位于 `%USERPROFILE%\.codex\skills\` 下，例如 `%USERPROFILE%\.codex\skills\妙计.skill\SKILL.md`。如果 Codex 尚未识别新技能，重启 Codex。

以上命令会覆盖同名已安装技能。若本机改过这些技能文件，先备份再安装。

## 更新

重新打开 PowerShell，运行：

```powershell
$repo = Join-Path $env:USERPROFILE '.codex\skill-sources\feishumiaoji-skill'
$skills = Join-Path $env:USERPROFILE '.codex\skills'
git -C $repo pull
Copy-Item "$repo\skills\妙计.skill" $skills -Recurse -Force
Copy-Item "$repo\skills\口播剪辑.skill" $skills -Recurse -Force
Copy-Item "$repo\skills\剪辑.skill" $skills -Recurse -Force
```

更新会覆盖已安装目录里的同名技能。只需课程制作流程时，至少安装 `妙计.skill` 和 `口播剪辑.skill`；`剪辑.skill` 是可选项。

## 使用流程

在 Codex 中说明要处理的课程主题或课节，并提供当前课程大纲、飞书文档或录播范围。例如：

> 使用妙计.skill，按课程大纲处理“AI生成原理与常用工具选择”：查找对应飞书录播和资料，筛选片段并精剪，生成妙记和单节课文档。

只需要某个环节时，直接说明要检索录播、剪辑视频、生成妙记或整理单节课文档。完整流程以 `妙计.skill/SKILL.md` 为准。

## 运行前准备

- 安装并登录 `lark-cli`，完成飞书授权；Lark CLI 不包含在本仓库中。
- 本仓库附带的 Lark 技能快照来自 `lark-cli 1.0.50`。实际操作前，以本机命令 `lark-cli skills read <skill>` 显示的当前规则为准，快照可能落后于 CLI 更新。
- 本地剪辑需要 FFmpeg。录播、文档和云盘权限仍由飞书账号控制；本仓库不包含账号凭证、学员信息或课程录播媒体。
- 单节课文档使用妙计技能中记录的飞书模板；使用者需拥有该模板的访问权限。

## 成片验收要求

每个剪点都要对照逐字稿和原音记录删减依据。“是吧”等高频口癖逐次判断，保留有确认或互动作用的用法，清理习惯性填充。导出后正常速度完整听审全片；发现口癖残留、气口突兀、断句或拼接不连贯，就返修重导并复听通过后再上传。
