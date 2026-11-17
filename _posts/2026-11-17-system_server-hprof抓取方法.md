---
title: system_server hprof 抓取方法
category: Android 系统
tags: [调试, 内存, hprof]
excerpt: 用 am dumpheap 抓取 system_server 堆快照，再通过 Dominator Tree 与 Histogram 分析内存占用。
---

## 抓取 hprof

需要 **debug 版本** 的系统。

```bash
# 获取 system_server 的 pid
adb shell pidof system_server

# 抓取堆快照（707 替换为实际 pid）
adb shell am dumpheap 707 /data/local/tmp/system_server.hprof
```

## 分析内存占用

用 MAT / Android Studio 打开 hprof 后，重点看两个视图：

1. **Dominator Tree**：看哪些对象占内存最多
2. **Histogram**：按类查看实例数量