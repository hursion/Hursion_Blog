1.下载源码[ChkBugReprot](https://github.com/sonyxperiadev/ChkBugReport)，See the [wiki](https://github.com/sonyxperiadev/ChkBugReport/wiki)

2.通过andorid Studio等工具编译

遇到以下错误，可修改编译设置解决。

> File
> -> Settings
> -> Build, Execution, Deployment
> -> Java Compiler option
>
> Change `javac` to `eclipse`, and apply.

```java
Error:Internal error: (java.lang.ClassNotFoundException) com.google.wireless.android.sdk.stats.IntellijIndexingStats$Index
java.lang.ClassNotFoundException: com.google.wireless.android.sdk.stats.IntellijIndexingStats$Index
	at java.net.URLClassLoader.findClass(URLClassLoader.java:382)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:419)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:352)
	at com.intellij.util.indexing.counters.IndexCounters.<clinit>(IndexCounters.java:34)
	at com.intellij.util.indexing.impl.MapReduceIndex.<init>(MapReduceIndex.java:92)
	at com.intellij.util.indexing.impl.MapReduceIndex.<init>(MapReduceIndex.java:108)
	at org.jetbrains.jps.backwardRefs.index.CompilerReferenceIndex$CompilerMapReduceIndex.<init>(CompilerReferenceIndex.java:274)
	at org.jetbrains.jps.backwardRefs.index.CompilerReferenceIndex.<init>(CompilerReferenceIndex.java:110)
	at org.jetbrains.jps.backwardRefs.JavaCompilerBackwardReferenceIndex.<init>(JavaCompilerBackwardReferenceIndex.java:13)
	at org.jetbrains.jps.backwardRefs.JavaBackwardReferenceIndexWriter.initialize(JavaBackwardReferenceIndexWriter.java:80)
	at org.jetbrains.jps.incremental.java.JavaBuilder.buildStarted(JavaBuilder.java:152)
	at org.jetbrains.jps.incremental.IncProjectBuilder.runBuild(IncProjectBuilder.java:361)
	at org.jetbrains.jps.incremental.IncProjectBuilder.build(IncProjectBuilder.java:178)
	at org.jetbrains.jps.cmdline.BuildRunner.runBuild(BuildRunner.java:140)
	at org.jetbrains.jps.cmdline.BuildSession.runBuild(BuildSession.java:297)
	at org.jetbrains.jps.cmdline.BuildSession.run(BuildSession.java:130)
	at org.jetbrains.jps.cmdline.BuildMain$MyMessageHandler.lambda$channelRead0$0(BuildMain.java:232)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)


```

3.生成路径

```
ChkBugReport-master/ChkBugReport-master$ find ./ -name *.jar
./core/build/libs/ChkBugReport.jar
```

4.使用方法

```
java -jar ChkBugReport.jar bugreport-XXX.180610.011-2020-03-20-16-53-20.txt
```

5.根据out中index.html分析问题