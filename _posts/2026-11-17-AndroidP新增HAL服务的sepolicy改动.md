---
title: Android P 新增 system_server 可访问的 HAL 服务：sepolicy 改动
category: Android 系统
tags: [SELinux, HAL, Android P]
excerpt: 在 device/sepolicy/common 中新增一个允许 system_server 访问的 HIDL HAL 服务，需要改动的 6 个 sepolicy 文件清单。
---

以 HIDL 服务 `android.hardware.newXX@1.0-service`（接口 `android.hardware.newXX::INewXX`）为例，所有改动都在 `device/sepolicy/common` 目录中。

## 1. attributes：声明 HAL 属性

```text
attribute hal_newXX;
attribute hal_newXX_client;
attribute hal_newXX_server;
```

## 2. file_contexts：标记可执行文件

```text
/(vendor|system/vendor)/bin/hw/android.hardware.newXX@1.0-service u:object_r:hal_newXX_default_exec:s0
```

## 3. 新增 hal_newXX_default.te

```text
type hal_newXX_default, domain, mlstrustedsubject;
hal_server_domain(hal_newXX_default, hal_newXX)

type hal_newXX_default_exec, exec_type, vendor_file_type, file_type;
init_daemon_domain(hal_newXX_default)

# Allow hwbinder call from hal client to server
binder_call(hal_newXX_client, hal_newXX_server)

# Add hwservice related rules
add_hwservice(hal_newXX_server, hal_newXX_hwservice)
allow hal_newXX_client hal_newXX_hwservice:hwservice_manager find;

#hwbinder_use(hal_newXX)
get_prop(hal_newXX, hwservicemanager_prop)

allow hal_newXX_default mnt_vendor_file:dir rw_dir_perms;
```

## 4. hwservice.te：声明 hwservice 类型

```text
type hal_newXX_hwservice, hwservice_manager_type;
```

## 5. hwservice_contexts：注册接口

```text
android.hardware.newXX::INewXX    u:object_r:hal_newXX_hwservice:s0
```

## 6. system_server.te：允许 system_server 作为客户端

```text
hal_client_domain(system_server, hal_newXX)
```

完成以上改动后，`system_server` 即可通过 hwbinder 查找并调用 `android.hardware.newXX::INewXX` 服务。