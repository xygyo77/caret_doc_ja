＃ コミュニケーション

通信レイテンシは、トピック メッセージがソース コールバックから次のコールバックまで移動するのにかかる時間を表します。

$$
l_{comm} = t_{sub} - t_{pub}
$$

<prettier-ignore-start>
!!! Info
        この定義では、通信遅延はコールバックのスケジューリングの影響を受け、DDS の通信遅延だけでなく、スケジューリングによる遅延も含まれます。
        たとえば、複数のコールバックが同時にディスパッチされる場合、通信遅延には他のコールバックの実行時間が含まれる可能性があります。
        スケジュールの詳細については、「[Event and latency_definitions | overview](../index.md#detailed-sequence)」を参照してください。
<prettier-ignore-end>

ROSの通信は、プロセス内通信とプロセス間通信をサブスクリプション側で行います。
ROSの通信は多対多の通信が可能なため、1回のパブリッシュでプロセス内通信とプロセス間通信の両方が行われる場合があります。
CARETでは、通信を1:1のペアに分割してレイテンシを計算します。

## プロセス内通信

関連するデータ フローのみに焦点を当てた簡略化されたシーケンス図を以下に示します。

```plantuml
@startuml

participant "UserCode\n(Publisher Side)" as Callback
participant "rclcpp\n (Publisher/Subscription)" as Rclcpp
participant "rclcpp\n (Buffer)" as Buffer
participant rcl
participant LTTng

== Publisher ==

-> Callback
activate Callback

Callback -> Rclcpp : publish
activate Rclcpp
Rclcpp -> LTTng : intra process publish

Rclcpp -> Buffer : enqueue
activate Buffer
Rclcpp -> rcl : notify
deactivate Rclcpp
activate rcl

deactivate Callback

== Subscription ==

rcl -> Rclcpp : dispatch
deactivate rcl
activate Rclcpp

Rclcpp -> Buffer : take
Buffer -> Rclcpp: dequeue
deactivate Buffer
Rclcpp -> LTTng: sample dispatch_intra_subscription_callback
Rclcpp -> LTTng : sample callback_start
Rclcpp -> Callback : callback start

activate Callback
@enduml
```

`to_dataframe` API は、次の列を含むテーブルを返します。

| Column                   | Type        | Description             |
| ------------------------ | ----------- | ----------------------- |
| rclcpp_publish_timestamp | System time | Publish time in rclcpp. |
| callback_start_timestamp | System time | Callback start time     |

こちらも参照

- [Trace points | rclcpp_intra_publish](../trace_points/runtime_trace_points.md#ros2rclcpp_intra_publish)
- [Trace points | dispatch_intra_process_subscription_callback](../trace_points/runtime_trace_points.md#ros2dispatch_intra_process_subscription_callback)
- [Trace points | callback start](../trace_points/runtime_trace_points.md#ros2callback_start)
- [Trace points | message_construct](../trace_points/runtime_trace_points.md#ros2message_construct)
- [RuntimeDataProvider API](https://tier4.github.io/caret_analyze/latest/infra/#caret_analyze.infra.lttng.lttng.Lttng.compose_intra_proc_comm_records)

## プロセス間通信

関連するデータ フローのみに焦点を当てた簡略化されたシーケンス図を以下に示します。

```plantuml
@startuml
title: Definition of major tracepoints

participant UserCode
participant "ROS 2" as ROS2
participant DDS
participant LTTng

== Publisher Side ==


activate ROS2
activate UserCode
UserCode -> ROS2: publish()
activate ROS2
ROS2 -> LTTng: sample rclcpp_publish


ROS2 -> DDS: dds_write()
deactivate ROS2
activate DDS
DDS -> LTTng: sample dds_write
DDS -> LTTng: sample dds_bind_addr_to_stamp

UserCode -> ROS2 : callback_end
deactivate UserCode
deactivate ROS2


== Subscription Side ==


DDS -> ROS2: <notify> on_data_available
activate ROS2

ROS2 -> DDS :  take messages
DDS -> ROS2
deactivate DDS
ROS2 -> LTTng: sample dispatch_subscription_callback
ROS2 -> LTTng: sample [callback_start
ROS2 -> UserCode: callback start
activate UserCode
UserCode -> ROS2: callback end
deactivate UserCode

deactivate ROS2
@enduml
```

`to_dataframe` API は、次の列を含むテーブルを返します。

| Column                   | Type        | Description             |
| ------------------------ | ----------- | ----------------------- |
| rclcpp_publish_timestamp | System time | Publish time in rclcpp. |
| rcl_publish_timestamp    | System time | Publish time in rcl.    |
| dds_write_timestamp      | System time | Publish time in rmw.    |
| callback_start_timestamp | System time | Callback start time.    |

こちらも参照

- [Trace points | message_construct](../trace_points/runtime_trace_points.md#ros2message_construct)
- [Trace points | rclcpp_publish](../trace_points/runtime_trace_points.md#ros2rclcpp_publish)
- [Trace points | rcl_publish](../trace_points/runtime_trace_points.md#ros2rcl_publish)
- [Trace points | dds_write](../trace_points/runtime_trace_points.md#ros2_caretdds_write)
- [Trace points | rclcpp_ring_buffer_enqueue](../trace_points/runtime_trace_points.md#ros2rclcpp_ring_buffer_enqueue)
- [Trace points | rclcpp_ring_buffer_dequeue](../trace_points/runtime_trace_points.md#ros2rclcpp_ring_buffer_dequeue)
- [Trace points | dds_bind_addr_to_addr](../trace_points/runtime_trace_points.md#ros2_caretdds_bind_addr_to_addr)
- [Trace points | dds_bind_addr_to_stamp](../trace_points/runtime_trace_points.md#ros2_caretdds_bind_addr_to_stamp)
- [Trace points | callback start](../trace_points/runtime_trace_points.md#ros2callback_start)
- [Trace points | dispatch_subscription_callback](../trace_points/runtime_trace_points.md#ros2dispatch_subscription_callback)
- [Trace points | rmw_take](../trace_points/runtime_trace_points.md#ros2rmw_take)
- [RuntimeDataProvider API](https://tier4.github.io/caret_analyze/latest/infra/#caret_analyze.infra.lttng.lttng.Lttng.compose_inter_proc_comm_records)
