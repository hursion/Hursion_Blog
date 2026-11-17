---
title: SSH 窗口保持：screen 用法
category: 工具与效率
tags: [SSH, screen, Linux]
excerpt: 用 screen 保持 SSH 会话不因断线丢失：创建、分离、恢复、查询命令速查。
---

SSH 断线后进程会被杀掉，用 `screen` 可以让会话在后台保持运行。

| 操作 | 命令 / 快捷键 |
| --- | --- |
| 创建会话 | `screen -S hursion` |
| 分离会话（detach） | `Ctrl + a`，然后按 `d` |
| 恢复会话（attach） | `screen -r hursion` |
| 查询会话列表 | `screen -ls` |

## 参考

- [linux screen 命令详解](https://www.cnblogs.com/mchina/archive/2013/01/30/2880680.html)