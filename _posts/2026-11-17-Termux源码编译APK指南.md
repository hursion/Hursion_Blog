---
title: Termux 源码编译 APK 指南
category: 工具与效率
tags: [Termux, APK, 编译]
excerpt: 从克隆 Termux 源码到编译、安装、签名发布 APK 的完整流程，关键在 JDK 与 Android SDK 环境配置。
---

整体流程：**获取源码 → 配置环境 → 编译 APK → 测试调试 → 签名发布**。其中最关键的是配置环境，它决定了源码能否正确编译。

## 1. 获取源码

Termux 源码在 GitHub：[termux/termux-app](https://github.com/termux/termux-app)。

```bash
# 如未安装 git
sudo apt-get install git

git clone https://github.com/termux/termux-app.git
```

## 2. 配置环境

需要 JDK 和 Android SDK。

```bash
# 安装 JDK
sudo apt-get install openjdk-8-jdk
```

从 Android 官网下载 SDK 并解压到目录（例如 `~/android-sdk`），然后设置环境变量：

```bash
export ANDROID_HOME=~/android-sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
```

## 3. 编译 Debug APK

进入源码根目录：

```bash
./gradlew assembleDebug
```

编译成功后，APK 生成在 `app/build/outputs/apk/debug/app-debug.apk`。

编译中常见问题是依赖包缺失、环境变量配置错误，按报错信息逐项检查即可。

## 4. 安装与调试

设备需开启开发者选项和 USB 调试：

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

安装后打开 Termux 检查功能是否正常；有问题可用 Android Studio 的调试工具查看日志。

## 5. 签名发布

先生成签名密钥：

```bash
keytool -genkey -v -keystore termux.keystore -alias termux -keyalg RSA -keysize 2048 -validity 10000
```

再编译并签名 Release 版：

```bash
./gradlew assembleRelease

jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore termux.keystore app-release-unsigned.apk termux
```