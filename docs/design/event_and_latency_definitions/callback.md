＃ Callback

コールバック レイテンシーは、コールバック実行の開始から終了までの時間として定義されます。
これらのイベントは、それぞれ `callback_start` および `callback_end` として表されます。

$$
l_{\rm{コールバック}} = t_{\rm{コールバック\ 終了}} - t_{\rm{コールバック\ 開始}}
$$

シーケンス図は、CARET rclcpp が 2 つのイベントをどのように取得するかを示しています。callback_start と callback_end。

```plantuml


participant "UserCode \n Callback" as Callback
participant "rclcpp" as Rclcpp
participant LTTng

activate Rclcpp

Rclcpp -> LTTng : sample callback_start
Rclcpp -> Callback : execute callback

activate Callback
Callback -> Rclcpp
deactivate Callback
Rclcpp -> LTTng : sample callback_end
```

`to_dataframe` API は、次の列を含むテーブルを返します。

| Column         | Type        | Description         |
| -------------- | ----------- | ------------------- |
| callback_start | System time | Callback start time |
| callback_end   | System time | Callback end time   |

こちらも参照

- [Trace points | Callback Start](../trace_points/runtime_trace_points.md#ros2callback_start)
- [Trace points | Callback End](../trace_points/runtime_trace_points.md#ros2callback_end)
- [RuntimeDataProvider API](https://tier4.github.io/caret_analyze/latest/infra/#caret_analyze.infra.lttng.lttng.Lttng.compose_callback_records)
