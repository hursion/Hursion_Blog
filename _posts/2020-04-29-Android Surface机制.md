# 如何理解surface

1.app与surface如何交互；

2.surface和surfaceFlinger的关系。

![image](https://wiki.jikexueyuan.com/project/deep-android-v1/images/chapter8/image001.png)



* 不论是使用Skia绘制二维图像，还是用OpenGL绘制三维图像，最终Application都要和Surface交互。Surface就像是UI的画布，而App则像是在Surface上作画。
* Surface和SurfaceFlinger的关系，很像Audio系统中AudioTrack和AudioFlinger的关系。Surface向SurfaceFlinger提供数据，而SurfaceFlinger则混合数据。



# 显示一个Activity

## activity的创建

​			Zygote在响应请求后会fork一个子进程，这个子进程是App对应的进程，它的入口函数是ActivityThread类的main函数。ActivityThread类中有一个handleLaunchActivity函数，它就是创建Activity的地方。

[-->[ActivityThread.java](http://10.0.1.79:8081/xref/sprdroid10_trunk_19c/frameworks/base/core/java/android/app/ActivityThread.java)]

```java
3443      /**
3444       * Extended implementation of activity launch. Used when server requests a launch or relaunch.
3445       */
3446      @Override
3447      public Activity handleLaunchActivity(ActivityClientRecord r,
3448              PendingTransactionActions pendingActions, Intent customIntent) {
...
3475          final Activity a = performLaunchActivity(r, customIntent);
3476  
3477          if (a != null) {
3478              r.createdConfig = new Configuration(mConfiguration);
3479              reportSizeConfigurations(r);
3480              if (!r.activity.mFinished && pendingActions != null) {
3481                  pendingActions.setOldState(r.state);
3482                  pendingActions.setRestoreInstanceState(true);
3483                  pendingActions.setCallOnPostCreate(true);
3484              }
...
3497      }
```

### 创建activity

1. final Activity a = performLaunchActivity(r, customIntent);//返回APP中的Activity

   [-->[ActivityThread.java](http://10.0.1.79:8081/xref/sprdroid10_trunk_19c/frameworks/base/core/java/android/app/ActivityThread.java)]
   
   ```java
   3186      /**  Core implementation of activity launch. */
   3187      private Activity performLaunchActivity(ActivityClientRecord r, Intent customIntent) {
   ...
   3209          Activity activity = null;
   3210          try {
   3211              java.lang.ClassLoader cl = appContext.getClassLoader();
   3212              long startTime = CheckTime.getTime();
       //后面跟踪
   3213              activity = mInstrumentation.newActivity(
   3214                      cl, component.getClassName(), r.intent);
   3215              CheckTime.checkTime(startTime, "instantiate activity");
   3216              StrictMode.incrementExpectedActivityCount(activity.getClass());
   3217              r.intent.setExtrasClassLoader(cl);
   3218              r.intent.prepareToEnterProcess();
   3219              if (r.state != null) {
   3220                  r.state.setClassLoader(cl);
   3221              }
   3222          } catch (Exception e) {
   3223              if (!mInstrumentation.onException(activity, e)) {
   3224                  throw new RuntimeException(
   3225                      "Unable to instantiate activity " + component
   3226                      + ": " + e.toString(), e);
   3227              }
   3228          }
   3229  
   ... 
   3243              if (activity != null) {
   ...
   3291                  if (r.isPersistable()) {
   3292                      mInstrumentation.callActivityOnCreate(activity, r.state, r.persistentState);
   3293                  } else {
   3294                      mInstrumentation.callActivityOnCreate(activity, r.state);
   3295                  }
   ...
   3331  
   3332          return activity;
   3333      }
   3334  
   ```

* 根据类名利用java反射机制创建一个Activity(mInstrumentation.newActivity)
* mInstrumentation.callActivityOnCreate来调用app生命周期中的onCreate()方法，在onCreate()方法中，和UI相关的重要工作就是调用setContentView来设置UI的外观。

#### handleResumeActivity

​				android P之前该方法是在handleLaunchActivity中直接执行，android P及之后改成通过ResumeActivityItem.execute来调用。

[-->[ActivityThread.java](http://10.0.1.79:8081/xref/sprdroid10_trunk_19c/frameworks/base/core/java/android/app/ActivityThread.java)]

```java
4310      @Override
4311      public void handleResumeActivity(IBinder token, boolean finalStateRequest, boolean isForward,
4312              String reason) {
...
4354          if (r.window == null && !a.mFinished && willBeVisible) {
4355              r.window = r.activity.getWindow();
    //1.获得decodeView对象
4356              View decor = r.window.getDecorView();
4357              decor.setVisibility(View.INVISIBLE);
    //2.获得ViewManager对象
4358              ViewManager wm = a.getWindowManager();
4359              WindowManager.LayoutParams l = r.window.getAttributes();
4360              a.mDecor = decor;
4361              l.type = WindowManager.LayoutParams.TYPE_BASE_APPLICATION;
4362              l.softInputMode |= forwardBit;
...
4378              if (a.mVisibleFromClient) {
4379                  if (!a.mWindowAdded) {
4380                      a.mWindowAdded = true;
    //3.把刚才的decor对象加入到ViewManager
4381                      wm.addView(decor, l);
4382                      DecorView.setAddedToWindow(a.mDecor);
...
4445      }
```

以上三个关键点已经开始和UI（window、view）联系起来，再来看看Activity中加载UI的部分setContentView；



### setContentView

setContentView的同名方法有好几个，以传参layoutResID为例

[-->[Activity.java](http://10.0.1.79:8081/xref/sprdroid10_trunk_19c/frameworks/base/core/java/android/app/Activity.java)]

```java
3371      public void setContentView(@LayoutRes int layoutResID) {
3372          getWindow().setContentView(layoutResID);
3373          initWindowDecorActionBar();
3374      }
```

```java
1022      public Window getWindow() {
1023          return mWindow;
1024      }
```



​		上面出现了两个和UI有关系的类：View和Window[①]。来看SDK文档是怎么描述这两个类的。这里先给出原文描述，然后进行对应翻译：

· Window：abstract base class for a top-levelwindow look and behavior policy. An instance of this class should be used asthe top-level view added to the window manager. It provides standard UIpolicies such as a background, title area, default key processing, etc.

中文的意思是：Window是一个抽象基类，用于控制顶层窗口的外观和行为。做为顶层窗口它有什么特殊的职能呢？即绘制背景和标题栏、默认的按键处理等。

这里面有一句比较关键的话：它将做为一个顶层的view加入到Window Manager中。

· View：This class represents the basicbuilding block for user interface components. A View occupies a rectangulararea on the screen and is responsible for drawing and event handling.

View的概念就比较简单了，它是一个基本的UI单元，占据屏幕的一块矩形区域，可用于绘制，并能处理事件。

从上面的View和Window的描述，再加上setContentView的代码，我们能想象一下这三者的关系，如图所示：

![image](https://wiki.jikexueyuan.com/project/deep-android-v1/images/chapter8/image002.png)

两个疑问：

* Window是一个抽象类，它实际的对象到底是什么类型？

  ```
  mWindow = new PhoneWindow(this, window, activityConfigCallback);
  ```

* Window Manager究竟是什么？



#### （1）Activity的Window -todo

​		据上文讲解可知，Window是一个抽象类。它实际的对象到底属于什么类型？先回到Activity创建的地方去看看。下面正是创建Activity时的代码，可当时没有深入地分析。

[-->[ActivityThread.java](http://10.0.1.79:8081/xref/sprdroid10_trunk_19c/frameworks/base/core/java/android/app/ActivityThread.java)-->[performLaunchActivity](http://10.0.1.79:8081/xref/sprdroid10_trunk_19c/frameworks/base/core/java/android/app/ActivityThread.java#3187)]

```java
3213              activity = mInstrumentation.newActivity(
3214                      cl, component.getClassName(), r.intent);
```



[-->[Instrumentation.java](http://10.0.1.79:8081/xref/sprdroid10_trunk_19c/frameworks/base/core/java/android/app/Instrumentation.java)]

```java
1244      public Activity newActivity(ClassLoader cl, String className,
1245              Intent intent)
1246              throws InstantiationException, IllegalAccessException,
1247              ClassNotFoundException {
1248          String pkg = intent != null && intent.getComponent() != null
1249                  ? intent.getComponent().getPackageName() : null;
1250          return getFactory(pkg).instantiateActivity(cl, className, intent);
1251      }
```



```java
1253      private AppComponentFactory getFactory(String pkg) {
1254          if (pkg == null) {
1255              Log.e(TAG, "No pkg specified, disabling AppComponentFactory");
1256              return AppComponentFactory.DEFAULT;
1257          }
1258          if (mThread == null) {
1259              Log.e(TAG, "Uninitialized ActivityThread, likely app-created Instrumentation,"
1260                      + " disabling AppComponentFactory", new Throwable());
1261              return AppComponentFactory.DEFAULT;
1262          }
1263          LoadedApk apk = mThread.peekPackageInfo(pkg, true);
1264          // This is in the case of starting up "android".
1265          if (apk == null) apk = mThread.getSystemContext().mPackageInfo;
1266          return apk.getAppFactory();
1267      }
1268  
```

[-->[LoadedApk.java](http://10.0.1.79:8081/xref/sprdroid10_trunk_19c/frameworks/base/core/java/android/app/LoadedApk.java)]

```java
269      public AppComponentFactory getAppFactory() {
270          return mAppComponentFactory;
271      }
```



```java
162      Application getApplication() {
163          return mApplication;
164      }
```



```java
1202      public Application makeApplication(boolean forceDefaultAppClass,
...
1226              app = mActivityThread.mInstrumentation.newApplication(
1227                      cl, appClass, appContext);
1228              appContext.setOuterContext(app);
1229          } catch (Exception e) {
1230              if (!mActivityThread.mInstrumentation.onException(app, e)) {
1231                  Trace.traceEnd(Trace.TRACE_TAG_ACTIVITY_MANAGER);
1232                  throw new RuntimeException(
1233                      "Unable to instantiate application " + appClass
1234                      + ": " + e.toString(), e);
1235              }
1236          }
1237          mActivityThread.mAllApplications.add(app);
1238          mApplication = app;
1239 
1240          if (instrumentation != null) {
1241              try {
1242                  instrumentation.callApplicationOnCreate(app);
1243              }
...
1266  
1267          return app;
1268      }
```



[-->[Instrumentation.java](http://10.0.1.79:8081/xref/sprdroid10_trunk_19c/frameworks/base/core/java/android/app/Instrumentation.java)]

```
1151      public Application newApplication(ClassLoader cl, String className, Context context)
1152              throws InstantiationException, IllegalAccessException,
1153              ClassNotFoundException {
1154          Application app = getFactory(context.getPackageName())
1155                  .instantiateApplication(cl, className);
1156          app.attach(context);
1157          return app;
1158      }
```



[-->[Application.java](http://10.0.1.79:8081/xref/sprdroid10_trunk_19c/frameworks/base/core/java/android/app/Application.java)]

```
350      /* package */ final void attach(Context context) {
351          attachBaseContext(context);
352          mLoadedApk = ContextImpl.getImpl(context).mPackageInfo;
353      }
```