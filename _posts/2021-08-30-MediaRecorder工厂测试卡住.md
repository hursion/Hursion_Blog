工厂生产中时常出现整机测试过程中卡在麦克风测试的问题
分析总结：
1. MediaRecorder API(8.1)调用方法无问题，native setOutputFile调用存在耗时；
2. setOutputFile 在MediaRecorder.java中仅有传参作用，并未使用jni调用native setOutputFile ；
3. setOutputFile 实际在prepare阶段调用，解释了setOutputFile 和setAudioEncoder在log打印顺序上的问题；
4. RandomAccessFile(mFile, “rws”)，s表示sync，从添加的log和trace推断系统在做fsync时耗时较久；
5. 客户分别修改为rw和在测试逻辑上加上mpath是否存在文件，如存在先删除，两种方案验证可以解决该问题。
6. sprdroid10_trunk_19c上代码已经是rw，猜测为google在新版本修复类似问题。

![image-20210901194517901](C:\Users\hursion.zhang\AppData\Roaming\Typora\typora-user-images\image-20210901194517901.png)

Debug使用的一些方法：
获取Native调用栈信息，

```c++
#include <utils/CallStack.h>
CallStack stack;
stack.update();
stack.log("log_tag");
```

Java层trace：
adb shell kill -3 PID，执行完后会在手机data/anr目录下有相应的trace文件生成

抓kernel态的栈：
echo 'l' > /proc/sysrq-trigger 
echo 'w' > /proc/sysrq-trigger
strace  -f -p pid -o /data/anr/strace.txt -t -tt -T -y