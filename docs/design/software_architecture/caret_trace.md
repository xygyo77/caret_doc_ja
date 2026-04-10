# caret_trace

`caret_trace` は、記録時に以下の機能を提供するパッケージです。

1. 関数フックを介して、CARET専用のトレースポイントを定義する
2. トレースフィルタリングおよび実行時記録のための関数フックを介して、トレースポイントの状態管理を追加する
3. `sim_time` を使用した記録機能を追加する

- [Tracepoints](../trace_points/index.md)
- [Hook](../runtime_processing/hook.md)
- [Runtime recording](../runtime_processing/runtime_recording.md)

## クラス構造

```plantuml

class Context {
    -- public --
    + get_trace_controller(): TracingController
    + get_node(): TraceNode
    + is_recording_enabled(): bool
    + ...
}
note left of Context : A class that manages instances; Singleton.

class HashableKeys<T1, T2, ...> {
    -- public --
    .. read only ..
    + hash(): size_t
    + equal_to(...) : bool
    -- private --
    - key: T1;
    - ...
}
note left of HashableKeys : Tuple-like class that can calculate and compare hash values

class KeysSet<T> {
    -- public --
    + insert(value: T): void
    .. read only..
    + first(): T
    + ...
    -- private --
    - keys_: set<HashableKeys<T>>
}
note left of KeysSet : Class that stores HashableKeys as a set.

class RecordableData<KeyT> {
    -- public [writer lock] --
    + assign(function: FuncT): void
    + store(tracepoint args): bool
    + record_next_one(): bool
    + start(): void
    + reset(): void
    + ...

    -- private --
    - func_: FuncT
    - pending_set_ : KeysSet<KeyT>
    - set_ : KeysSet<KeyT>
}
note left of RecordableData : Data storage class that has a record function\nData are stored as pending during recording, and are merged after the record is completed. Thread safe.

class LttngSession {
    + is_session_running(): bool
}
note left of LttngSession : Class for manipulating LTTng sessions.

class Clock {
    + now(): int64_t
}
note left of Clock : Class for LTTng clock

class TracingController {
    -- public [writer lock] --
    + add_node(address: void *): void
    + ...

    .. read only..
    + is_allowed_node(address: void *) : bool
    + ...
}
note left of TracingController : Class for tracepoint filtering.

class DataContainer{
    -- public --
    + record(loop_count: uint64_t): bool

    + store_rcl_init(tracepoint_args) bool
    + ...

    + assign_rcl_init(recording_function): void
    + ...
    -- private --
    - rcl_init_: shared_ptr<RecordableData>
    - ...
}
note left of DataContainer : Class that stores RecordableData for all tracepoints.

class DataRecorder {
    -- public --
    + start(): void
    + reset(): void
    + record_next(): bool
    .. read only ..
    + finished(): bool
    + ...
}
note left of DataRecorder : Class for handling RecordableData for all trace points

class TraceNode {
    + start_callback(caret_msgs::Start)
    + end_callback(caret_msgs::End)
    + timer_callback()
}
note left of TraceNode : Class for controlling recording state.

DataContainer "1" --> "1" DataRecorder : use
DataRecorder "1" --> "0..*" RecordableData: use
RecordableData "1" o-- "1"  KeysSet
Context "1" o-- "1"  DataContainer
Context "1" o-- "1" TraceNode
Context "1" o-- "1" TracingController
Context "1" o--- "1" Clock
Context "1" o---- "1" LttngSession
TraceNode "1" --> "1" DataContainer : use
DataContainer "1" o- "0..*"  RecordableData
KeysSet "1" o-- "0..*" HashableKeys



```

## 関数フックを使用したトレースポイントの実装

CARET は、主に新しいトレース ポイントを追加するために関数フックを採用しています。一方、CARET にはトレースポイントの状態を管理する関数が追加されているため、ROS 2 に組み込まれている既存のトレースポイントも関数フックによって再定義されます。

以下はフック関数の疑似コードです。

```C++
void ros_trace_callback_start(TRACEPOINT_ARGS) {
  // Record trace data only if current callback is allowed to record
  if (controller.is_allowed(TRACEPOINT_ARGS)) {
    tracepoint(TRACEPOINT_ARGS); // LTTng tracepoint
  }
}

void ros_trace_XXX_init(TRACEPOINT_ARGS)
{
  // Wrapper function for tracepoint.
  // This function is executed with delay.
  // This function is executed either from the record at the end of this function
  // or from TraceNode's timer callback.
  // Duplicate data are resolved with caret_analyze.
  static auto record = [](TRACEPOINT_ARGS, now) {
    // Record trace data only if current callback is allowed to record
    if (controller.is_allowed(TRACEPOINT_ARGS)) {
      tracepoint(TRACEPOINT_ARGS, now); // LTTng tracepoint
    }
  };

  auto now = clock.now(); // Measure immediately after function call

  if (!data_container.is_assigned_XXX()) {
    data_container.assign_XXX(record);
  }

  // Store TRACEPOINT_ARGS in memory.
  data_container.store_XXX(TRACEPOINT_ARGS, now);

  record(TRACEPOINT_ARGS, now);
}

```

`ros_trace_callback_start` は、コールバックの開始をトレースするフック関数の例です。アプリケーションに関連するイベントを収集するためのトレース ポイントの一種です。
の動作、いわゆるランタイム トレース ポイント。

`ros_trace_XXX_init` は、アプリケーションのコンポーネントの ID を取得するフック関数の例です。アプリケーションの起動時および初期化時に呼び出されることが期待されます。トレースポイントは初期化トレースポイントに分類されます。

コールバック アドレスやノード名などの一連の識別情報は `TRACEPOINT_ARGS` として与えられます。
数種類の初期化トレース ポイントが提供され、それぞれが異なる種類のコンポーネントにアタッチされます。たとえば、1 つはノードの ID を収集するために呼び出され、もう 1 つはパブリッシャーの ID を収集するために呼び出されます。

さまざまなトレース ポイントから収集された ID は、要素として同じアドレスまたは名前を共有します。このような ID を同じアドレスまたは名前で結び付けることで、CARET はアプリケーションの構造を見つけるのに役立ちます。

詳細については、[Initialization trace points](../trace_points/initialization_trace_points.md) を参照してください。

## クロックレコーダー

CARET は、視覚化のために `sim_time` として表されるシミュレーション時間を選択できます。
`sim_time` は、`clock_recorder` ノードを実行することで記録できます。これにより、`sim_time` 記録のトレース ポイントが追加されます。

```bash
ros2 caret trace --record-clock
```

`ClockRecorder` ノードは 1 秒ごとに起動し、`sim_time` とシステム時刻のペアを記録します。
このペアは、システム時間をシミュレーション時間に変換するために使用されます。
