使用ps -A看看mediaserver是否启动了，如果mediaserver启动了，是可以支持rtsp协议的；

```shell
root@S2:/ # ps | grep media
media_rw  186   1     3524   288   00000000 b6edb1d0 S /system/bin/sdcard
media     215   1     32084  1744  00000000 b6eaa494 S /system/bin/mediaserver
u0_a17    986   210   226856 15396 00000000 40100644 S android.process.media
```

如果非Android平台，没有启动mediaserver进程，则rtsp协议是无法直接解析的，目前rtsp流媒体播放是运行在mediaserver进程的。

