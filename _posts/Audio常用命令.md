# Audio常用命令

## Audio底层命令

1.查询声卡设备

```shell
adb shell cat /proc/asound/cards

 0 [sprdphone      ]: sprdphone - sprdphone
                      sprdphone
 1 [alli2s         ]: all-i2s - all-i2s
                      all-i2s
 2 [saudiovoip     ]: saudiovoip - saudiovoip
                      saudiovoip
 3 [saudiolte      ]: saudiolte - saudiolte
                      saudiolte

```



```
执行下如下命令，查看下双mic是否打开

adb root
adb shell
tinymix -D 0

打印出来的信息查看如下内容：

Mic Function                      1
ADCL Mixer MainMICADCL Switch     1

Aux Mic Function                  1
ADCR Mixer AuxMICADCR Switch      1
```