## Vietnam Briefing Doing Business Guide 抓取任务

这个小项目用于：

- 从 `vietnam-briefing.com.2026-02-27T08_02_49.787Z.json` 中筛选出所有 `url` 包含 `doing-business-guide` 且带有 `title` 的条目；
- 使用 Playwright + Chromium 打开这些页面，并“打印”为 PDF 文件，方便离线阅读和存档。

### 环境准备

```bash
cd /Users/qianping/Documents/Source/ascentium/grep-briefing

python3 -m venv .venv  # 可选：创建虚拟环境
source .venv/bin/activate  # macOS / Linux

pip install -r requirements.txt
playwright install chromium
```

### 运行抓取脚本

```bash
cd /Users/qianping/Documents/Source/ascentium/grep-briefing
python3 crawl_doing_business_pdfs.py
```

运行完成后：

- 所有匹配到的页面会以 PDF 形式保存在 `doing-business-pdfs/` 目录下；
- 文件名由 URL 的路径和页面标题组合而成，便于识别。

# grep-briefing # 这句如果你已经有内容，可以酌情省略
