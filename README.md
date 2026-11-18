# Hursion's Blog

Android 系统开发笔记：Framework、多媒体、测试认证与工具效率。
Jekyll 博客 + Obsidian 知识库 + 交互式个人知识图谱，同一份 Markdown，三种形态。

在线地址：<https://hursion.github.io/Hursion_Blog/>

## 内容分类

| 分类 | 范围 |
|------|------|
| Android 系统 | Framework、Native 服务、内核与系统构建 |
| 多媒体 | Audio / Video / Camera 调试与源码分析 |
| 测试与认证 | CTS / GMS / CTA 认证测试与问题定位 |
| 工具与效率 | Vim、Systrace、bugreport 与日常提效 |
| 随笔与学习 | 学习方法、知识体系与博客搭建 |

分类定义见 [_data/categories.yml](_data/categories.yml)，新增分类需同步该文件与
[scripts/build_knowledge_graph.py](scripts/build_knowledge_graph.py) 中的 `CATEGORY_SLUGS`。

## 目录结构

```
_posts/       博客文章，同时是 Obsidian 笔记（YYYY-MM-DD-标题.md）
_knowledge/   知识图谱 MOC 入口（仅 Obsidian 可见，不发布）
_data/        分类定义
_includes/    页面片段（head、导航脚本等）
_layouts/     页面模板
assets/       样式、字体、图片与图谱数据（data/knowledge-graph.json）
scripts/      图谱构建与本地预览脚本
.obsidian/    Obsidian 库配置（忽略 _site、模板目录等）
```

## 写文章

在 `_posts/` 新建 `YYYY-MM-DD-标题.md`，frontmatter 示例：

```yaml
---
title: 文章标题
category: 多媒体        # 须为上表已有分类
tags: [Audio, 调试]
excerpt: 一句话摘要，显示在列表与图谱详情中
published: false       # 可选；false 为草稿，Obsidian 可见、站点不发布
---
```

推送后由 GitHub Pages（`gh-pages` 分支）自动构建发布。

## 本地预览

站点整体预览需要 Ruby 环境：

```bash
bundle install
bundle exec jekyll serve   # http://localhost:4000/Hursion_Blog/
```

无 Ruby 时可用 python-liquid 单独预览知识图谱页：

```bash
pip install python-liquid
python scripts/preview_kg.py   # 生成 _kg_preview.html，浏览器打开
```

## 知识图谱 × Obsidian

本仓库同时是一个 Obsidian 库：用 Obsidian「打开文件夹作为仓库」选择本目录，
入口笔记为 [_knowledge/知识图谱总览.md](_knowledge/知识图谱总览.md)
（MOC，wikilink 连接全部文章，图谱视图按分类着色）。

博客导航「知识图谱」页（`/knowledge-graph/`）为 D3 交互式力导向图：

- 节点 = 文章 / 分类 / 标签；边 = 归属 / 标签 / 相关（正文互引或共享 ≥2 标签）
- 支持搜索、分类筛选、悬停高亮、详情面板跳转文章/分类/标签页，适配深浅色主题
- 数据在 Jekyll 构建时由 Liquid 生成，文章链接与站点 permalink 始终一致

更新图谱（新增/修改文章后执行，再提交）：

```bash
python scripts/build_knowledge_graph.py
```

重新生成 MOC、`assets/data/knowledge-graph.json` 与本地缓存
`~/.knowledge-graph/cache/blog_graph.json`。

## 许可

主题基于 [Flexible-Jekyll](https://github.com/artemsheludko/flexible-jekyll)（GPL-3.0，见 [LICENSE](LICENSE)）；
文章内容为作者原创，转载请注明出处。