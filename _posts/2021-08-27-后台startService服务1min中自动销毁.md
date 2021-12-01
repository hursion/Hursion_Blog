

# Log

05-28 17:04:05.852 713-729/system_process W/ActivityManager: Stopping service due to app idle: u0a100 -1m46s220ms com.nexgo.xtms22/com.nexgo.xtms.XTMSService

# analysis

是因为android 8.0之后有了后台 Service 限制，在服务空闲一段时间会被销毁，如果需要保护建议可以换成startForegroundService启动服务并以通知方式处理，谢谢！

# Refs：

https://developer.android.com/about/versions/oreo/background?hl=zh-cn
		https://blog.csdn.net/u011386173/article/details/83615924