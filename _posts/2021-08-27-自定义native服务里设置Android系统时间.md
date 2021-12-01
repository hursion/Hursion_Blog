# 代码实现

```c
#define LOG_TAG "timeTest"

#include <ctype.h>
#include <cutils/log.h>
#include <cutils/properties.h>
#include <cutils/sockets.h>
#include "cutils/uevent.h"
#include <poll.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <linux/rtc.h>
#include <mtd/mtd-user.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/reboot.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/sysinfo.h>
#include <sys/time.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>
#include <expat.h>
#include <pthread.h>

#define REF_DEBUG

#ifdef REF_DEBUG
#define REF_LOGD ALOGD
#define REF_LOGE ALOGE
#else
#define REF_LOGD(x...)
#define REF_LOGE(x...)
#endif

int main(int argc, char *argv[]) {
  REF_LOGD("start timetest");
  struct timespec ts;
  struct timeval tv;
  int res;
  //ts.tv_sec = 1589731800;
  //ts.tv_nsec = 0;
    tv.tv_sec = 1589731800;
    tv.tv_usec = 0;
  res = settimeofday(&tv, NULL);
  if (res < 0) {
     REF_LOGD("settimeofday() faled:%s\n", strerror(errno));
  }
  
}
```

# Android.mk

```makefile
LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)

LOCAL_SRC_FILES:= \
    timeTest.c

LOCAL_C_INCLUDES += \
    external/expat/lib

 LOCAL_SHARED_LIBRARIES := \
     libhardware_legacy \
     libexpat \
     libc \
     libutils \
     libcutils \
     liblog
 
 LOCAL_MODULE := timetest
 LOCAL_INIT_RC := timetest.rc
 LOCAL_MODULE_TAGS := optional
 LOCAL_PROPRIETARY_MODULE := true
 
 ifeq ($(strip $(LOCAL_PROPRIETARY_MODULE)), true)
     LOCAL_CFLAGS += -DCONFIG_IN_VENDOR
 endif
 
 include $(BUILD_EXECUTABLE)

```

# timetest.rc

```xml
service vendor.timetest /vendor/bin/timetest
    class main
    user root
    group root
```

