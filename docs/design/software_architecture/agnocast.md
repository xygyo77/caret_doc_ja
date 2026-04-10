# Agnocast のサポート

[Agnocast](https://github.com/tier4/agnocast) は、rclcpp と互換性のある真のゼロコピー IPC ミドルウェアです。CARET は、DDS の代わりに Agnocast を使用するアプリケーションをサポートするように拡張され、CARET の既存の [runtime recording](../runtime_processing/runtime_recording.md)、[tracepoint filtering](../runtime_processing/tracepoint_filtering.md)、および Agnocast ベースのシステムでの分析機能の使用が可能になりました。Agnocast ベースのアプリケーションを使用する場合、CARET の使用法は変更されません。

実装については次の PR を参照してください。

- [tier4/caret_trace#316](https://github.com/tier4/caret_trace/pull/316) - Agnocast のランタイム recording
- [tier4/caret_trace#318](https://github.com/tier4/caret_trace/pull/318) - Agnocast のトレース フィルタリング
- [tier4/caret_analyze#577](https://github.com/tier4/caret_analyze/pull/577) - Agnocast データの処理と分析
- [tier4/caret_trace#326](https://github.com/tier4/caret_trace/pull/326) - ランタイム recording および Agnocast ノード トレースポイントのトレース フィルタリング
- [tier4/caret_analyze#587](https://github.com/tier4/caret_analyze/pull/587) - Agnocast ノード トレースポイント データの処理と分析

＃＃ 詳細

トレースポイント定義の詳細については、次のドキュメントを参照してください。

- [Agnocast Initialization Tracepoints](../trace_points/agnocast_initialization_tracepoints.md)
- [Agnocast Runtime Tracepoints](../trace_points/agnocast_runtime_tracepoints.md)

## バージョンの互換性

CARET は、[2.3.1](https://github.com/autowarefoundation/agnocast/releases/tag/2.3.1) 以降の Agnocast バージョンのみをサポートします。
