import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright


DATA_PATH = Path(
    "/Users/qianping/Documents/Source/ascentium/grep-briefing/vietnam-briefing.com.2026-02-27T08_02_49.787Z.json"
)

OUTPUT_DIR = Path(
    "/Users/qianping/Documents/Source/ascentium/grep-briefing/doing-business-pdfs"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_target_links():
    """从 JSON 中筛选 url 含 doing-business-guide 的链接。"""
    raw = DATA_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    links = data.get("links", [])
    targets = [
        link for link in links if "doing-business-guide" in link.get("url", "")
    ]
    return targets


def slugify(url: str, title: str) -> str:
    """根据 URL + 标题生成相对稳定的文件名，避免特殊字符。"""
    if "doing-business-guide/" in url:
        path_part = url.split("doing-business-guide/")[-1].strip("/").replace("/", "_")
    else:
        path_part = ""

    title_part = re.sub(r"[^a-zA-Z0-9一-龥]+", "_", title).strip("_")

    if path_part and title_part:
        base = f"{path_part}__{title_part}"
    elif path_part:
        base = path_part
    else:
        base = title_part or "page"

    return base[:150]


def save_page_as_pdf(page, url: str, title: str):
    """使用已打开的 page，把指定 URL 渲染并导出为 PDF。"""
    filename = slugify(url, title) + ".pdf"
    out_path = OUTPUT_DIR / filename

    if out_path.exists():
        print(f"[skip] 已存在 {out_path.name}")
        return

    print(f"[open] {url}")
    page.goto(url, wait_until="networkidle", timeout=60_000)

    page.set_viewport_size({"width": 1280, "height": 720})

    print(f"[pdf ] 生成 {out_path.name}")
    page.pdf(
        path=str(out_path),
        format="A4",
        print_background=True,
        margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"},
    )


def main():
    targets = load_target_links()
    print(f"共找到 {len(targets)} 条 doing-business-guide 链接")

    if not targets:
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i, link in enumerate(targets, start=1):
            url = link["url"]
            title = link.get("title") or url
            print(f"\n=== [{i}/{len(targets)}] {title} ===")
            try:
                save_page_as_pdf(page, url, title)
            except Exception as e:
                print(f"[err ] {url}: {e}")

        browser.close()


if __name__ == "__main__":
    main()

