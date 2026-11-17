---
title: 树莓派 Android 14 编译 llama.cpp
category: Android 系统
tags: [llama.cpp, NDK, 树莓派]
excerpt: 用 NDK r27 把 llama.cpp 交叉编译到 arm64-v8a（Android 14），并记录 Vulkan 编译可用但运行失败的结论。
---

目标平台：Raspberry Pi 5 上的 Android 14，`TARGET_ARCH_VARIANT=armv8-a`。

## CPU 版编译

使用 NDK r27 的 CMake 工具链交叉编译：

```bash
/usr/local/bin/cmake \
  -DCMAKE_TOOLCHAIN_FILE=/home/zh370208/tools/android-ndk-r27/build//cmake/android.toolchain.cmake \
  -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=android-34 \
  -DCMAKE_C_FLAGS=-march=armv8-a \
  -DCMAKE_CXX_FLAGS=-march=armv8-a \
  -DGGML_OPENMP=OFF \
  -DGGML_LLAMAFILE=OFF \
  -B build-android

/usr/local/bin/cmake --build build-android --config Release
```

## Vulkan 版编译

加上 `-DGGML_VULKAN=ON`：

```bash
/usr/local/bin/cmake \
  -DCMAKE_TOOLCHAIN_FILE=/home/zh370208/tools/android-ndk-r27/build//cmake/android.toolchain.cmake \
  -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=android-34 \
  -DCMAKE_C_FLAGS=-march=armv8-a \
  -DCMAKE_CXX_FLAGS=-march=armv8-a \
  -DGGML_OPENMP=OFF \
  -DGGML_LLAMAFILE=OFF \
  -DGGML_VULKAN=ON \
  -B build-android-vulkan
```

**结论**：Vulkan 版可以编译通过，但实际运行不支持。树莓派 5 硬件本身应该支持 Vulkan，推测是树莓派的 Android 系统对 Vulkan 的驱动支持不友好，CPU 版可用。