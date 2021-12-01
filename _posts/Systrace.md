ftrace/atrace/systrace的关系

```shell
alias st-start='python /sdk/platform-tools/systrace/systrace.py'  
alias st-start-gfx-trace = ‘st-start -t 8 gfx input view sched freq wm am hwui workq res dalvik sync disk load perf hal rs idle mmc’
```

```shell
adb shell atrace --list_categories
```