### 基础参数

`-p <packageName1> -p <packageName2> -p <packageName3> ...`

用此参数指定一个或者多个包名，指定包之后，monkey将只启动对应的应用，如果未指定包名，系统将允许monkey启动所有应用。

`-v`

用于指定测试反馈信息级别（信息级别就是日志的详细程度），总共分3个级别，如下：

```
adb shell monkey -p com.android.example -v 100 //仅提供启动、测试完成和最终结果等少量日志。

adb shell monkey -p com.android.example -v -v 100 //提供较详细的日志，包括每个发送到Activity 的事件信息

adb shell monkey -p com.android.example -v -v -v 100 // 包括各个activity的信息
```

`-s <随机数种子>`

用于指定伪随机数生成器的seed 值，如果seed 相同，则两次Monkey测试所产生的事件序列也相同的，示例：

adb shell monkey -p com.android.example -s 10

`--throttle <毫秒>`

用于指定用户操作事件延迟时间。默认不设置，则尽可能的执行。

adb shell monkey -p com.android.example --throttle 3000 10

`-c <main-category>`

如果以这种方式指定一个或多个类别，则Monkey将  仅  允许系统访问使用指定类别之一列出的活动。如果您未指定任何类别，Monkey将选择使用Intent.CATEGORY_LAUNCHER或Intent.CATEGORY_MONKEY类别列出的活动。要指定多个类别，请多次使用-c选项 - 每个类别一个-c选项。

### 事件操作

`--pct-touch <percent>`

用于调整触摸事件占的百分比。

`--pct-motion <percent>`

调整运动事件的百分比 。

`--pct trackball <percent> `

调整轨迹球事件占的百分比

`--pct-nav <percent>`

调整“基本”导航事件的百分比。（导航事件由上/下/左/右组成，作为来自方向输入设备的输入。）

`--pct-majornav <percent>`

调整“主要”导航事件的百分比。（这些导航事件通常会导致UI中的操作，例如5向键盘中的中心按钮，后退键或菜单键。）

`--pct-appswitch <percent> `

调整活动启动的百分比。在随机的时间间隔内，Monkey将发出一个startActivity（）调用，作为最大化包中所有活动的覆盖范围的方法。
