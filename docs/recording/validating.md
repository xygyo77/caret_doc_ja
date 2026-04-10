# トレースデータの検証

## トレースデータの検証

recording が成功したかどうかは、`ros2 caret check_ctf` コマンドで確認できます。

```sh
ros2 caret check_ctf <path-to-trace-data>
```

<prettier-ignore-start>
!!!info
      長時間の録画データや大規模なアプリケーションの録画データに対して`ros2 caret check_ctf`コマンドを実行すると時間がかかります。
      したがって、長時間の recording を実行する前に、短時間の記録データに対して `ros2 caret check_ctf` コマンドを実行することをお勧めします。
      また、ターゲット アプリケーションを構築するときに、コードを変更して次の警告を回避できるように、トレース データを記録して検証することをお勧めします。
<prettier-ignore-end>

<prettier-ignore-start>
!!!info
      Python やライブラリによって発生する警告は無視できます。
<prettier-ignore-end>

## 間違った手順による警告

### `Failed to find trace point added by caret-rclcpp`

- 原因
  - ターゲット アプリケーションのビルド時に CARET/rclcpp が適用されない
- 解決
  - CARET を使用してアプリケーションをビルドします ([build section](./build_check.md) を参照)

### `Failed to find trace point added by LD_PRELOAD`

- 原因
  - フックされたトレースポイントが見つかりませんでした。`LD_PRELOAD` が見逃される可能性があります
- 解決
  - アプリケーションを実行する前に `LD_PRELOAD` を設定します ([recording section](./recording.md) を参照)

### `Trace data from a package built without caret-rclcpp was detected`

- 原因
  - 一部のパッケージ (例: apt でインストールされたパッケージ) は、caret-rclcpp を使用せずにビルドされています。
- 解決
  - CARET を使用してアプリケーションをビルドします ([build section](./build_check.md) を参照)
  - 上記を確認してもまだこの警告が表示される場合は、
    アプリケーションで使用されるすべてのパッケージをワークスペースに追加し、CARET を使用してビルドします。

### `Tracer discarded`

- 原因
  - トレース データが多すぎるため、recording 中にトレース データの損失が発生しました
  - この警告は、特に CARET を大規模なアプリケーションに適用する場合に発生することがあります。
  - 詳細
    - LTTng セッションは、トレースポイントによって生成されたサンプリング データを収集します。[LTTng documents](https://lttng.org/man/7/lttng-concepts/v2.13/#doc-channel) で説明したように、サンプリングデータはリング バッファに保存されます。リングバッファの一部が占有されると、サンプリングデータは次の空の部分に格納され、占有された部分はファイルにコピーされます。すべてのリングバッファにサンプリングデータを格納する余地がない場合、サンプリングデータは破棄されます。
- 解決
  - トレースフィルターを適用するか、より多くのトピック/ノードを無視するようにトレースフィルター設定を変更します ([trace filtering section](./trace_filtering.md) を参照)
    - 特に頻度の高いノードやトピックのフィルタリングが効果的
    - 頻度の高いノード/トピックは、[summary of trace data](./cli_tool.md#node-summary) をチェックすることで特定できます。
  - ターゲットデバイスに十分なメモリがある場合は [size of ring-buffer in CARET](https://github.com/tier4/ros2_tracing/blob/2cd9d104664b4bf4d7507d01e5553129eefe1c9a/tracetools_trace/tracetools_trace/tools/lttng_impl.py#L109F) を増やします
    - [example](https://github.com/tier4/ros2_tracing/pull/1/files)

## CARET の制限による警告

- CARET は、次のパラメータを使用してコールバック関数を識別します。ノードにパラメータが同一のコールバック関数が複数ある場合、CARET は解析できないため、そのようなノードは無視されます。
  - タイマコールバック関数: タイマ周期
  - サブスクリプションコールバック関数: トピック名

### `Duplicate parameter callback found`

- 原因
  - 同じタイマ周期を持つ複数のタイマコールバック関数がノード内に存在します。
  - 言い換えると、同じタイマ周期を持つ `rclcpp::create_timer()` が複数回呼び出されます。
- 解決策（回避策）
  - 同じタイマ期間の使用を避けるようにコードを変更します (タイマ期間の値をわずかに変更できます)
  - または、ノードを分析する必要がない限り、この警告は無視できます。

### `Failed to identify subscription. Several candidates were found`

- 原因
  ・ノード内に同じトピック名のサブスクリプションコールバック関数が複数存在する
  - つまり、同じトピック名を持つ `rclcpp::create_subscription()` が複数回呼び出されます
- 解決策（回避策）
  - 同じトピック名を持つ複数のサブスクリプションコールバック関数が作成されないようにコードを変更します。

### `Multiple executors using the same callback group were detected`

- 原因
  - コールバックグループが複数のエグゼキュータに追加される
- 解決
  - 現時点では解決策はありません。CARET は、最後のエグゼキュータを使用して分析します。ほとんどの場合、この警告は無視できます。

### `Failed to find callback group`

- 原因
  - CARET はコールバックグループ、コールバック、およびエグゼキュータをバインドできませんでした。それは主に ROS 2 service によるものです。「サービス」は CARET ではサポートされていません
- 解決
  - 現時点では解決策はありません。ほとんどの場合、この警告は無視できます。
