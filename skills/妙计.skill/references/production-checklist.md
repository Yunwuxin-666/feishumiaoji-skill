# 妙计课程制作清单

## 来源映射记录模板

| 课表序号 | 课节主题 | 来源营次 | 飞书标题 | 资源类型 | 飞书链接/token | 媒体时长 | 采用时间段 | 选择理由 | 重复/独有信息 | 配套资料 | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 |  |  |  | 妙记/会议/文档/课件 |  |  | 00:00–00:00 |  |  |  | 待核实 |

一条课节如有多个来源，逐条列出并标记主素材/补充素材。时间段使用源视频时间码，注明由转写或章节定位，并经媒体复核。

## 全量检索清单

- [ ] 记录大纲来源、版本、课程顺序与检索日期。
- [ ] 提取课程主题、同义词、软件名、营次标签、讲师/项目名。
- [ ] 搜索飞书文档、课件与配套资料，记录链接与可访问状态。
- [ ] 搜索妙记列表，按主题词、营次与时间范围分批执行；遍历分页并按 minute token 去重。
- [ ] 搜索历史课程会议，遍历分页；对候选 meeting ID 查询录制并关联 minute token。
- [ ] 覆盖用户指定的全部历史范围；未指定范围且沿用用户已确认的项目带练历史时，从 6.0 起检索。
- [ ] 记录未检索时间窗、无录制会议、权限不可见资源和其他限制。
- [ ] 比较每节课的候选版本，确认主素材、时间戳、质量理由与重复内容处理方式。

## 常用 CLI 形态

每次执行前先读取 CLI 当前版本的 lark-shared 和对应 shortcut reference；以下为命令形态，具体参数以当前 CLI help/schema 为准。

```powershell
# 搜索一批妙记；按月份切分时间窗并补齐分页
lark-cli minutes +search --query "<主题词>" --start "<YYYY-MM-DD>" --end "<YYYY-MM-DD>" --page-size 30 --format json --as user

# 搜索已结束的历史课程会议并补齐分页
lark-cli vc +search --query "<营次或主题>" --start "<YYYY-MM-DD>" --end "<YYYY-MM-DD>" --page-size 30 --format json --as user

# 用会议 ID 取得录制关联的 minute token
lark-cli vc +recording --meeting-ids "<meeting_id>" --format json --as user

# 下载对应妙记媒体；实际参数按当前 download reference 校准
lark-cli minutes +download --minute-tokens "<minute_token>" --output-dir "./source-recordings" --as user

# 上传成片到 Drive，再创建妙记
lark-cli drive +upload --file "./AIGC营-主题.mp4" --name "AIGC营-主题.mp4" --as user --format json
lark-cli minutes +upload --file-token "<file_token>" --as user --format json

# 设置妙记标题并复核
lark-cli minutes +update --minute-token "<minute_token>" --topic "AIGC营-主题" --as user --format json
lark-cli minutes minutes get --params "{\"minute_token\":\"<minute_token>\"}" --as user --format json
```

分钟搜索有最大时间窗时按月拆分；分别完成妙记搜索和会议搜索，最后按 token 去重。下载、上传和标题更新的选项以当前 lark-minutes、lark-drive reference 为准。缺权限时使用 lark-shared 最小 scope split-flow，不保存授权 URL 或 device code。

## 成片验收清单

- [ ] 课节顺序符合课程大纲，重复主题已去重或明确标记补充内容。
- [ ] 时间戳与下载的源媒体一致；每段选择理由和配套资料有记录。
- [ ] 音视频共用同一时间线；删减后语义、演示因果与必要等待仍完整。
- [ ] 抽查开头、中段、章节边界、关键操作和结尾；在最终导出中核对字幕、音画同步、章节标题、进度条及课程产出。
- [ ] 最终文件成功解码，记录时长、分辨率、帧率和音轨。
- [ ] 文件名为 `AIGC营-主题.mp4`，不含期数或内部修订后缀。
- [ ] Drive 上传成功并核实 file token 与链接。
- [ ] 妙记生成后核实标题为 `AIGC营-主题`；未 ready 或缺 scope 时准确记录状态。
- [ ] 回传实际可用的妙记 URL；需要时附 Drive 文件 URL。

## 对外命名约定

- 视频：`AIGC营-<简洁主题>.mp4`。
- 妙记：`AIGC营-<简洁主题>`。
- 可读主题沿用大纲课名，如 `ComfyUI入门`；不写 `10.0`、`剪辑版`、`修改版`、`视觉修正版`、`灰底概括进度条版`、日期批次或内部版本号。
- 本地中间文件可保留内部标识；对外 Drive 文件和妙记标题必须遵守上面的规范。