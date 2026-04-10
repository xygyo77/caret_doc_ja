# ROS 時間 (sim_time) のサポート

## 導入

CARET は、デフォルトでシステム時間を使用してトレース データを分析します。特にrosbagで記録されたトレースデータを扱う場合には不便な場合があります。以下に例を示します。

- `[-r RATE]`オプションでrosbagを再生した場合、解析結果(時系列グラフなど)の時間の流れがROSとは異なります。たとえば、rosbag が `[-r 0.2]` で再生された場合、10 Hz は 2 Hz になりますが、分析にはシステム時間が使用されます
- 同じrosbagファイルを使用してもrecordingごとに時間が異なるため、実験結果の比較が困難

このページではsim_timeの使い方を説明します。

## Recording `/clock` トピック

`/clock` トピックをトレース データに記録する必要があります。`/clock` トピは、トレース データに `ros2_caret:sim_time` イベントとして記録されます。

`ros2 caret record` コマンドに `--record-clock` オプションを追加します。

<prettier-ignore-start>
!!!info
      ターゲット アプリケーションを起動するときに、各ノードに `use_sim_time=true` を設定することを忘れないでください。
      rosbag をプレイするときは、`--clock` オプションを忘れずに追加してください
<prettier-ignore-end>

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_caret_ws/install/local_setup.bash

ros2 caret record --record-clock
```

`/clock`が正常に記録されたかどうかは、以下のコマンドで確認できます。

```bash
babeltrace <path-to-trace-data> | cut -d' ' -f 4 | sort -u | grep sim_time
```

```bash
---Expected output text as below---

ros2_caret:sim_time:
```

## sim_time を使用した視覚化

`xaxis_type='sim_time'` を設定すると、Plot オブジェクト内の以下の API でシステム時間の代わりに sim_time が使用されます。

```python
def to_dataframe(
   self,
   xaxis_type: str
) -> pd.DataFrame:

def figure(
   self,
   xaxis_type: Optional[str],
   ywheel_zoom: Optional[bool],
   full_legends: Optional[bool]
) -> Figure:

def show(
    self,
    xaxis_type: str = 'system_time',
    ywheel_zoom: bool = True,
    full_legends: bool = False,
) -> None:

def save(
    self,
    export_path: str,
    title: str = '',
    xaxis_type: Optional[str] = None,
    ywheel_zoom: Optional[bool] = None,
    full_legends: Optional[bool] = None
) -> None:
```

`/clock`トピックがトレースデータに記録されていない場合、以下のエラーが発生します。

```python
InvalidArgumentError: Failed to load sim_time. Please measure again with clock_recorder running.
```

<prettier-ignore-start>
!!!warning
    タイマコールバックがターゲットパスの途中に存在する場合、ROSBAG の再生レートはパスの動作に大きく影響します。そのため、`xaxis_type`が`'sim_time'`であっても、ROSBAG再生レートが1.0以外のトレースデータについては、パスの[response time](../visualization/path/response_time.md)を正しく計算できません。
<prettier-ignore-end>

## sim_time を使用するサンプル

以下の説明は、CARET が `~/ros2_caret_ws` にインストールされており、チュートリアル セクションで使用されるサンプル アプリケーションが `~/ros2_ws` にあることを前提としています。

### rosbag を記録する

次の手順は、CARET を使用しても使用しなくても実行できます。CARET を使用せずにターゲット アプリケーションをビルドした場合は、CARET および LD_PRELOAD の環境を設定する必要はありません。

1. ターミナルを開いてターゲットアプリケーションを実行し、rosbag を記録します

   ```sh
   source /opt/ros/humble/setup.bash
   source ~/ros2_caret_ws/install/local_setup.bash
   source ~/ros2_ws/install/local_setup.bash
   export LD_PRELOAD=$(readlink -f ~/ros2_caret_ws/install/caret_trace/lib/libcaret.so)

   ros2 run caret_demos end_to_end_sample
   ```

2.別の端末を開いて rosbag を記録します

   ```sh
   source /opt/ros/humble/setup.bash
   source ~/ros2_caret_ws/install/local_setup.bash
   source ~/ros2_ws/install/local_setup.bash

   ros2 bag record /topic1 /drive
   ```

   ここで、`/topic1` と `/drive` はサンプル アプリケーションのソース トピックです。
   rosbag が正常に記録されたかどうかを確認できます。

   ```bash
   ros2 bag info rosbag2_2022_09_30-10_57_06

   Files:             rosbag2_2022_09_30-10_57_06_0.db3
   Bag size:          29.3 KiB
   Storage id:        sqlite3
   Duration:          9.601s
   Start:             Sep 30 2022 10:57:08.952 (1664503028.952)
   End:               Sep 30 2022 10:57:18.554 (1664503038.554)
   Messages:          194
   Topic information: Topic: /drive | Type: sensor_msgs/msg/Image | Count: 97 | Serialization Format: cdr
                   Topic: /topic1 | Type: sensor_msgs/msg/Image | Count: 97 | Serialization Format: cdr
   ```

### トレースデータを記録する

1. ターミナルを開いてターゲット アプリケーションを実行し、CARET でトレース データを記録します。

   起動ファイルでは、`use_sim_time` が true に設定され、ソース ノードが無効になります。

   ```sh
    source /opt/ros/humble/setup.bash
    source ~/ros2_caret_ws/install/local_setup.bash
    source ~/ros2_ws/install/local_setup.bash
    export LD_PRELOAD=$(readlink -f ~/ros2_caret_ws/install/caret_trace/lib/libcaret.so)

    ros2 launch caret_demos end_to_end_sample.launch.py use_sim_time:=true use_rosbag:=true
   ```

2. 別の端末を開いて、`/clock` トピックを使用してパフォーマンス データを記録します。

   ```sh
    source /opt/ros/humble/setup.bash
    source ~/ros2_caret_ws/install/local_setup.bash
    source ~/ros2_ws/install/local_setup.bash

    ros2 caret record -s e2e_sample --record-clock
   ```

3. 別の端末を開いて rosbag を再生します

   ```sh
    source /opt/ros/humble/setup.bash
    source ~/ros2_caret_ws/install/local_setup.bash
    source ~/ros2_ws/install/local_setup.bash

    ros2 bag play rosbag2_2022_09_30-10_57_06 --clock -r 0.2
   ```

4. アプリケーションと rosbag を停止します。

5. `/clock` トピックがトレース データに `sim_time` として記録されているかどうかを確認します

   ```bash
   babeltrace ~/ros2_ws/evaluate/e2e_sample | cut -d' ' -f 4 | sort -u | grep sim_time
   ros2_caret:sim_time:
   ```

### sim_time を使用して結果を視覚化する

1. `~/ros2_ws/evaluate` で Jupyter Notebook を起動し、次のスクリプトを実行します。
   - 参照: [the tutorial](../tutorials/visualization.md)

```python
from bokeh.plotting import output_notebook
output_notebook()
from caret_analyze import Architecture, Application, Lttng
from caret_analyze.plot import Plot, message_flow

# Read trace data
arch = Architecture('lttng', './e2e_sample')
lttng = Lttng('./e2e_sample')

# Search and add path
paths = arch.search_paths(
    '/filter_node',
    '/message_driven_node')
arch.add_path('target_path', paths[0])
app = Application(arch, lttng)

# Draw message_flow
path = app.get_path('target_path')
plot = Plot.create_message_flow_plot(path)
plot.show(xaxis_type='sim_time')

# Draw node info
node = app.get_node('/filter_node')
plot = Plot.create_period_timeseries_plot(node.callbacks)
plot.show(xaxis_type='sim_time')
```
