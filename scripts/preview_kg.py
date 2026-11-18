#!/usr/bin/env python3
"""本地预览知识图谱页面（无需 Jekyll/Ruby）。

用 python-liquid 模拟 Jekyll 渲染 knowledge-graph.html 与 default 布局，
输出 _kg_preview.html 供浏览器打开。仅验证模板逻辑与前端交互；
正式站点 URL 以 Jekyll 构建时的 post.url 为准。

用法: pip install python-liquid && python scripts/preview_kg.py
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_knowledge_graph import load_posts, CATEGORY_ORDER  # noqa: E402

try:
    from liquid import Environment, DictLoader
except ImportError:
    sys.exit("缺少依赖: pip install python-liquid")

ROOT = Path(__file__).resolve().parent.parent


def strip_markdown(text):
    text = re.sub(r"```.*?```", "", str(text), flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[#*`>]", "", text)
    return text


def make_env():
    env = Environment()
    env.filters["jsonify"] = lambda ctx, v: json.dumps(v, ensure_ascii=False)
    env.filters["push"] = lambda ctx, arr, item: list(arr) + [item]
    env.filters["strip_markdown"] = lambda ctx, text: strip_markdown(text)
    return env


def load_categories():
    cats, cur = [], {}
    for line in (ROOT / "_data" / "categories.yml").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- name:\s*(.+)$", line)
        if m:
            if cur:
                cats.append(cur)
            cur = {"name": m.group(1).strip()}
            continue
        m = re.match(r"^\s+(slug|icon|desc):\s*(.+)$", line)
        if m and cur:
            cur[m.group(1)] = m.group(2).strip()
    if cur:
        cats.append(cur)
    return cats


def main():
    posts = load_posts(ROOT / "_posts")
    site_posts = []
    for p in posts:
        site_posts.append({
            "title": p["title"],
            "category": p["category"],
            "tags": p["tags"],
            "excerpt": p["excerpt"],
            "content": p["body"],
            "date": datetime.fromisoformat(p["date"]) if p["date"] else datetime(2000, 1, 1),
            "published": p["published"],
            "url": "/" + p["stem"] + "/",
            "path": "_posts/" + p["file"],
        })
    tags = {}
    for p in site_posts:
        for t in p["tags"]:
            tags.setdefault(t, []).append(p)
    categories = load_categories()
    site = {
        "posts": site_posts,
        "tags": tags,
        "data": {"categories": categories},
        "time": datetime.now(),
        "baseurl": "/Hursion_Blog",
        "title": "Hursion's Blog",
        "description": "Android 系统开发笔记",
        "url": "",
        "author-img": "hursion_zhang.jpg",
        "social-github": "hursion",
        "social-email": "zhanghursion@gmail.com",
    }
    page = {"title": "知识图谱", "url": "/knowledge-graph/"}

    env = make_env()
    page_text = (ROOT / "knowledge-graph.html").read_text(encoding="utf-8")
    page_text = re.sub(r"^---.*?---\s*", "", page_text, count=1, flags=re.S)
    env.loader = DictLoader({"page": page_text})
    body = env.get_template("page").render({"site": site, "page": page})

    layout = (ROOT / "_layouts" / "default.html").read_text(encoding="utf-8")
    layout = layout.replace("{% include head.html %}", (ROOT / "_includes" / "head.html").read_text(encoding="utf-8"))
    layout = layout.replace("{% include javascripts.html %}", (ROOT / "_includes" / "javascripts.html").read_text(encoding="utf-8"))
    layout = layout.replace("{% include analytics.html %}", "")
    layout = layout.replace("{{ content }}", body)
    env.loader = DictLoader({"layout": layout})
    html = env.get_template("layout").render({"site": site, "page": page})
    html = html.replace("/Hursion_Blog/assets/", "assets/")

    out = ROOT / "_kg_preview.html"
    out.write_text(html, encoding="utf-8")
    print(f"预览已生成: {out}")


if __name__ == "__main__":
    main()