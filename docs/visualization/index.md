# 概要

この章では、トレースデータを期待どおりに視覚化する方法について説明します。[Gallery](../gallery.md) セクションでは、CARET でサポートされているビジュアライゼーションのタイプを示します。CARET は、このようなグラフを作成するための均一な視覚化 API を提供します。

## 統一された API 設計

CARET は、トレースデータを視覚化するために `Plot` クラスを提供します。次のサンプルコードは、`Plot` の基本的な使用方法を示しています。

```python
from caret_analyze import Application, Architecture, Lttng
from caret_analyze.plot import Plot
from bokeh.plotting import output_notebook, figure, show
output_notebook()

# Load recorded data
lttng = Lttng('/path/to/trace_data')
# Load an Architecture object
arch = Architecture('yaml', '/path/to/architecture_file')
# Map the architecture object to the recorded data
app = Application(arch, lttng)

# Focus on a target callback
callback = app.get_callback('/target/callback/name')

# Get plot object for visualizing callback frequency
# Plot.create_[Metrics]_[GraphType]_plot(data)
# is format to get a target data set to visualize
plot = Plot.create_frequency_timeseries_plot(callback)

# Assign a table to callback_df object
callback_df = plot.to_dataframe()

# Create a graph for frequency of callback execution
plot.show()
```

`plot` オブジェクトは `Plot.create_[Metrics]_[GraphType]_plot(data)` から取得されます。`data` の引数は、たとえば、`CallbackBase` ベースのオブジェクトまたは `Communication` ベースのオブジェクトです。後述するように、`CallbackBase` または `Communication` のリストも使用できます。
`latency`、`frequency`、または `period` などのパフォーマンスメトリックは、`Metrics` として指定されます。`GraphType` は、時系列やヒストグラムなどのグラフの種類を選択するために提供されます。

`plot` オブジェクトには次の 4 つのメソッドがあります。`to_dataframe()`、`show()`、`save()`、`figure()`。

- `to_dataframe()` メソッドは、指定されたメトリクスの時系列データを含むテーブルを返します。別の種類のグラフを手動で作成したい場合は、`to_dataframe()` メソッドでテーブルを取得し、期待するグラフに変換します。
- `show()`メソッドは時系列グラフの図を作成します。つまり、`show()` メソッドは時系列データを可視化します。
- `save()`メソッドは、任意のパスに図形を保存します。
- `figure()` メソッドは、対応する Figure ハンドラーを返します。この方法を使用すると、Figure を表示する前に追加のカスタマイズが可能になります。

マルチホストシステムの記録データを視覚化するには、記録データのリストを LTTng オブジェクトに渡すことができます。

```python
lttng = Lttng(['/path/to/host0/trace_data', '/path/to/host1/trace_data'])
```

## 視覚化 API

このセクションでは、いくつかのメトリクスを視覚化する方法をリストします。リンクにアクセスすると、メトリクスに対応するサンプル図が表示されます。
一部のメソッドは統一された API 設計に従って設計されていないため、例外となります。

### Callback

- [`create_frequency_timeseries_plot(callbacks: Collection[CallbackBase])`](./frequency/index.md#callback)
- [`create_period_timeseries_plot(callbacks: Collection[CallbackBase])`](./period/index.md#callback)
- [`create_latency_timeseries_plot(callbacks: Collection[CallbackBase])`](./latency/index.md#callback)
- [`create_callback_scheduling_plot`](./scheduling/callback.md)
  - コールバックのスケジューリングを視覚化する

### コミュニケーション

- [`create_frequency_timeseries_plot(communications: Collection[Communication])`](./frequency/index.md#communication)
- [`create_period_timeseries_plot(data: [Communication])`](./period/index.md#communication)
- [`create_latency_timeseries_plot(data: [Communication])`](./latency/index.md#communication)

ここで、CARET は、メッセージの送信と受信の両方が失われずに正常に実行された場合の通信を考慮しています。
詳細については、[Premise of communication](./premise_of_communication.md) を参照してください。興味のない方はこのページは読み飛ばしてください。

＃＃＃ パス

- [`create_message_flow_plot`](./path/message_flow.md)
  - ターゲットパスのメッセージフローを可視化
- [`create_response_time_histogram_plot`](./path/response_time.md)
- [`chain_latency`](./path/chain_latency.md)

## ヘルパー API

CARET は、ユーザーがそれぞれの興味に集中できるようにする API をいくつか提供します。

- [`LTTngEventFilter()`](./filter/lttng_event_filter.md)
- [Wildcards for `get_callbacks()`](./search/wildcards_for_get_callbacks.md)

<prettier-ignore-start>
!!!info
    [CARET analyze API document](https://tier4.github.io/caret_analyze/) では、API のパラメーターと戻り値について説明します。
<prettier-ignore-end>
