# トレースポイントのフィルタリング

多数のノードで構成される Autoware などのターゲット アプリケーションを測定する場合、トレースからのデータ量が非常に大きくなる可能性があります。

LTTng はシステムへの影響を最小限に抑えるための廃棄モードであるため、大量の recording の間にトレース データの廃棄が発生します。

CARET は、特定のトピックまたはノードに関連付けられたトレース ポイントを無効にする機能を提供します。
これにより、rviz ノードまたは tf トピックに関連するトレース データのみを recording から除外できるようになり、大規模システムでも CARET の測定が可能になります。

このフィルタリング関数は、インスタンス アドレス (コールバックやパブリッシャなど) を調べて、それらがフィルタに含まれているかどうかを確認します。
このチェックは std::unowned_map を使用するため、O1 順序で行われます。

```cpp
void ros_trace_callback_start(const void * callback, bool is_intra_process) {
  // Record trace data only if current callback is allowed to record
  if (controller.is_allowed_callback(callback)) {
    tracepoint(callback, is_intra_process); // LTTng tracepoint
  }
}
```

こちらも参照

- [caret_trace](../software_architecture/caret_trace.md)
- [Tracepoint](../trace_points/index.md)
- [Recording | trace filtering](../../recording/trace_filtering.md)

## DDS レイヤーのトレースポイント フィルタリング

トレースポイントをフィルタリングするには、ノードとトピックに関する情報を含む `callback` や `publisher` などのオブジェクトが必要です。DDS レイヤーでは、そのようなオブジェクトは利用できません。つまり、ROS 2 レイヤーのトレースポイントと同じ方法で [`dds_write`](../trace_points/runtime_trace_points.md#ros2_caretdds_write) と [`dds_bind_addr_to_stamp`](../trace_points/runtime_trace_points.md#ros2_caretdds_bind_addr_to_stamp) をフィルターすることはできません。

これらのトレースポイントをフィルタリングするには、[`rcl_publish`](../trace_points/runtime_trace_points.md#ros2rcl_publish)、`dds_write`、および `dds_bind_addr_to_stamp` が常に同じスレッドに連続して記録されるという事実を利用します。`rcl_publish` がフィルターで除外されると、同じスレッド内の後続の `dds_write` および `dds_bind_addr_to_stamp` もフィルターで除外されます。`rcl_publish` がフィルターで除外されない場合、同じスレッド内の後続の `dds_write` および `dds_bind_addr_to_stamp` もフィルターで除外できません。

`rcl_publish` が記録されているかどうかを送信するためにスレッドローカル ストレージを利用します。

```c++
thread_local bool trace_filter_is_rcl_publish_recorded;

void ros_trace_rcl_publish(const void * publisher_handle, const void * message)
{
  ...

  if (controller.is_allowed_publisher_handle(publisher_handle) &&
    context.is_recording_allowed())
  {
    ((functionT) orig_func)(publisher_handle, message);
    trace_filter_is_rcl_publish_recorded = true;
  } else {
    trace_filter_is_rcl_publish_recorded = false;
  }
}

void ros_trace_rmw_publish(const void * message)
{
  if (trace_filter_is_rcl_publish_recorded) {
    tracepoint(TRACEPOINT_PROVIDER, dds_write, message);
  }
}

int dds_write_impl(void * wr, void * data, long tstamp, int action)
{
  ...

  if (context.is_recording_allowed() && trace_filter_is_rcl_publish_recorded) {
    tracepoint(TRACEPOINT_PROVIDER, dds_bind_addr_to_stamp, data, tstamp);
  }

  ...
}
```
