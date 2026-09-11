# 咖啡赛事台 Coffee Circuit

为咖啡从业者与爱好者整理的赛事信息站：杯测、冲煮、拉花、咖啡师、烘焙赛事聚合，含主办方、含金量、历史规模与选手介绍，卡片可直接跳转官方报名页。

## 工作原理（全自动）

```
每天 10:15（北京时间）
  └─ GitHub Actions 定时触发 daily.yml
      ├─ scripts/update.py 抓取 HOTELEX 官方咖啡赛事栏目
      ├─ 新赛事自动合并进 data.json（id 顺延、标记 NEW）
      └─ 有变更则自动 commit + push
          └─ 触发 pages.yml → 自动部署 GitHub Pages
              └─ 线上网站即时更新，全程无人值守
```

- 数据文件：`data.json`（唯一数据源，前端 `index.html` 运行时加载；本地打开时自动回退到内置快照）
- 更新脚本：`scripts/update.py`（标准库实现，无需第三方依赖）
- 自动部署：`.github/workflows/pages.yml`（GitHub Pages）

## 手动维护赛事

`data.json` 的 `events` 数组是唯一数据源，直接编辑并 push 即可（部署会自动触发）。

字段说明：

| 字段 | 含义 |
|---|---|
| id | 数字，顺延递增 |
| name | 赛事名称 |
| cat | tasting / sensory / barista / latte / brew / roast |
| lv | 级别（国际·中国区 / 城市赛 / 民间等） |
| date / place / fee | 时间 / 地点 / 费用 |
| status | open（可报）/ soon（即将或待确认）/ done（已完赛） |
| statusTxt | 状态徽标文字 |
| region | 江浙沪 / 西南 / 华南 / 华中 / 北方 / 全国 |
| desc / route / ch | 描述 / 晋级路径 / 报名渠道 |
| link / linkTxt | 报名或官方发布链接（卡片按钮） |
| src | 信息来源 |
| isNew | true 时显示 NEW 徽标 |

## 手动触发更新

仓库 Actions 页面 → Daily Update → Run workflow（无需等定时）。

## 数据口径

- 自动抓取仅收录标题含当年年份（2026/2027）的咖啡类赛事，来源为 HOTELEX 官网咖啡赛事栏目；
- 抓取失败时保留现有数据不中断；
- 报名信息以主办方官方发布为准。
