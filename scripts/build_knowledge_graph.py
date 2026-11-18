#!/usr/bin/env python3
"""从 Jekyll 博客 _posts 提取知识图谱，生成 Obsidian MOC 与博客可视化页面。

用法: python scripts/build_knowledge_graph.py [--repo-root PATH]

产物:
  _knowledge/知识图谱总览.md      Obsidian MOC（wikilink 连接全部文章）
  assets/data/knowledge-graph.json 图谱数据（站点资产）
  knowledge-graph.html            交互式图谱页面（由 scripts/graph_page.template.html 注入数据生成）
  ~/.knowledge-graph/cache/blog_graph.json 本地缓存
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

CATEGORY_SLUGS = {
    "Android 系统": "android",
    "多媒体": "media",
    "测试与认证": "testing",
    "工具与效率": "tools",
    "随笔与学习": "notes",
}
CATEGORY_ORDER = list(CATEGORY_SLUGS)
BASEURL = "/Hursion_Blog"
DATE_RE = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})-")


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")
    fm = {}
    for line in fm_text.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            fm[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        else:
            fm[key] = val.strip("'\"")
    return fm, body


def load_posts(posts_dir):
    posts = []
    for path in sorted(posts_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_frontmatter(text)
        if not fm.get("title"):
            continue
        m = DATE_RE.match(path.name)
        post_date = None
        if m:
            try:
                post_date = date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
            except ValueError:
                pass
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        posts.append({
            "file": path.name,
            "stem": path.stem,
            "title": fm["title"],
            "category": fm.get("category", ""),
            "tags": tags,
            "excerpt": fm.get("excerpt", ""),
            "date": post_date,
            "published": fm.get("published", "true").lower() != "false",
            "body": body,
        })
    return posts


def build_graph(posts):
    nodes, edges = [], []
    seen = set()

    def add_node(name, ntype, **extra):
        if name in seen:
            return
        seen.add(name)
        nodes.append({"name": name, "type": ntype, **extra})

    for cat in CATEGORY_ORDER:
        add_node(f"分类：{cat}", "topic", summary=f"博客分类：{cat}")
    all_tags = sorted({t for p in posts for t in p["tags"]})
    for tag in all_tags:
        count = sum(1 for p in posts if tag in p["tags"])
        add_node(f"标签：{tag}", "concept", summary=f"共 {count} 篇文章", source_count=count)

    for p in posts:
        summary = p["excerpt"] or re.sub(r"[#*`\[\]]", "", p["body"])[:120].strip()
        add_node(
            p["title"], "post",
            summary=summary,
            tags=", ".join(p["tags"]),
            category=p["category"],
            date=p["date"] or "",
            published=p["published"],
            source_file=f"_posts/{p['file']}",
        )
        if p["category"]:
            edges.append({"source": p["title"], "target": f"分类：{p['category']}",
                          "relType": "belongs_to", "strength": "strong"})
        for tag in p["tags"]:
            edges.append({"source": p["title"], "target": f"标签：{tag}",
                          "relType": "tagged", "strength": "medium"})

    # 文章互链：正文提及其他文章标题，或共享 >=2 个标签
    for i, a in enumerate(posts):
        for b in posts[i + 1:]:
            if a["title"] in b["body"] or b["title"] in a["body"]:
                edges.append({"source": a["title"], "target": b["title"],
                              "relType": "relates_to", "strength": "strong",
                              "description": "正文互相引用"})
            elif len(set(a["tags"]) & set(b["tags"])) >= 2:
                shared = ", ".join(sorted(set(a["tags"]) & set(b["tags"])))
                edges.append({"source": a["title"], "target": b["title"],
                              "relType": "relates_to", "strength": "weak",
                              "description": f"共享标签：{shared}"})

    metadata = {
        "source": "Hursion_Blog/_posts",
        "exported_at": date.today().isoformat(),
        "post_count": len(posts),
        "category_count": len(CATEGORY_ORDER),
        "tag_count": len(all_tags),
    }
    return {"nodes": nodes, "edges": edges, "metadata": metadata}


def inline_tag(t):
    return "#" + t.replace(" ", "-")


def build_moc(posts):
    lines = [
        "---",
        "title: 知识图谱总览",
        "tags: [MOC, 知识图谱]",
        "---",
        "",
        "# 知识图谱总览",
        "",
        "> 本笔记由 `scripts/build_knowledge_graph.py` 自动生成，是 Obsidian 图谱的入口 hub。",
        f"> 生成日期：{date.today().isoformat()}，共 {len(posts)} 篇文章。",
        "> 在线交互式图谱：博客导航「知识图谱」页面（knowledge-graph.html）。",
        "",
    ]
    for cat in CATEGORY_ORDER:
        cat_posts = [p for p in posts if p["category"] == cat]
        if not cat_posts:
            continue
        lines.append(f"## {cat}")
        lines.append("")
        for p in sorted(cat_posts, key=lambda x: x["date"] or ""):
            draft = "" if p["published"] else "（草稿）"
            tag_str = " ".join(inline_tag(t) for t in p["tags"])
            lines.append(f"- [[{p['stem']}|{p['title']}]]{draft} {tag_str}")
        lines.append("")
    uncategorized = [p for p in posts if not p["category"]]
    if uncategorized:
        lines.append("## 未分类")
        lines.append("")
        for p in uncategorized:
            lines.append(f"- [[{p['stem']}|{p['title']}]]")
        lines.append("")
    lines.append("## 标签索引")
    lines.append("")
    all_tags = sorted({t for p in posts for t in p["tags"]})
    lines.append(" ".join(inline_tag(t) for t in all_tags))
    lines.append("")
    return "\n".join(lines)


def render_page(template_path, output_path):
    # 页面数据由 Liquid 在 Jekyll 构建时生成（post.url 与站点 permalink 一致），
    # 这里只做原样复制；本地预览用 scripts/preview_kg.py 渲染。
    output_path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parent.parent))
    args = parser.parse_args()
    root = Path(args.repo_root)
    posts_dir = root / "_posts"
    if not posts_dir.is_dir():
        sys.exit(f"未找到文章目录: {posts_dir}")

    posts = load_posts(posts_dir)
    graph = build_graph(posts)

    moc_dir = root / "_knowledge"
    moc_dir.mkdir(exist_ok=True)
    (moc_dir / "知识图谱总览.md").write_text(build_moc(posts), encoding="utf-8")

    data_dir = root / "assets" / "data"
    data_dir.mkdir(exist_ok=True)
    data_json = json.dumps(graph, ensure_ascii=False, indent=2)
    (data_dir / "knowledge-graph.json").write_text(data_json, encoding="utf-8")

    cache_dir = Path.home() / ".knowledge-graph" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / "blog_graph.json").write_text(data_json, encoding="utf-8")

    render_page(root / "scripts" / "graph_page.template.html",
                root / "knowledge-graph.html")

    m = graph["metadata"]
    print(f"文章 {m['post_count']} 篇 | 分类 {m['category_count']} | 标签 {m['tag_count']}")
    print(f"节点 {len(graph['nodes'])} | 关系 {len(graph['edges'])}")
    print("已生成: _knowledge/知识图谱总览.md, assets/data/knowledge-graph.json, knowledge-graph.html")


if __name__ == "__main__":
    main()