# Recording

## Recording と CARET

CARET は、ターゲット アプリケーションのトレースに LTTng を使用します。
このページでは、トレースの 2 つの異なる方法について説明します。LTTng セッションを手動で開始する方法と、ROS 起動システムを使用して LTTng セッションを開始する方法です。

このページの説明では、CARET が `~/ros2_caret_ws` にインストールされており、チュートリアル セクションで使用されるサンプル アプリケーションが `~/ros2_ws` にあることを前提としています。

## LTTng セッションを手動で開始する

この方法には 2 つの端子が必要です。one for executing a target application, another for starting a LTTng session.

1. ターミナルを開き、対象のアプリケーションを起動します
   - 環境設定は以下の順序で行ってください。ターゲット アプリケーションが CARET/rclcpp を参照しているため、CARET の `local_setup.bash` は ROS 2 の `setup.bash` と一緒に適用する必要があります。

     ```sh
     # Environment settings (keep the order as below)
     source /opt/ros/humble/setup.bash
     source ~/ros2_caret_ws/install/local_setup.bash
     source ~/ros2_ws/install/local_setup.bash
     ```

   - `LD_PRELOAD` を設定して、関数フックによって提供されるトレースポイントを有効にします

     ```sh
     export LD_PRELOAD=$(readlink -f ~/ros2_caret_ws/install/caret_trace/lib/libcaret.so)
     ```

   - (オプション) [trace filtering](./trace_filtering.md) を適用します。トレースフィルタリングの設定により、CARET は不要なノード/トピックを無視できます。この関数は大規模なアプリケーションに役立ちます

     ```sh
     # Apply filter directly
     export CARET_IGNORE_NODES="/rviz*"
     export CARET_IGNORE_TOPICS="/clock:/parameter_events"

     # Apply filter using a setting file
     source ./caret_topic_filter.bash
     ```

   - 対象のアプリケーションを起動します

     ```sh
     ros2 run caret_demos end_to_end_sample
     ```

2. 別の端末を開き、次のコマンドで LTTng セッションを開始します。
   - トレースデータは、パスが`{ROS_TRACE_DIR}/{SESSION_NAME}`で定義されたディレクトリに保存されます。
     - `ROS_TRACE_DIR` は、デフォルト値が `~/.ros/tracing` である環境変数です。
        (オプション) `ROS_TRACE_DIR` 環境変数を設定して、記録されたトレース データが保存される宛先ディレクトリを変更できます。
     - `SESSION_NAME` は、`ros2 caret record` コマンドの `-s` オプションで指定されたセッション名を意味します
   - 「Enter」キーを押してセッションを開始します

   ```sh
   source /opt/ros/humble/setup.bash
   source ~/ros2_caret_ws/install/local_setup.bash

   # (Optional) Set a destination directory
   mkdir -p ~/ros2_ws/evaluate
   export ROS_TRACE_DIR=~/ros2_ws/evaluate

   ros2 caret record -s e2e_sample

   # Start session with pressing Enter key
   ```

3. 「Enter」キーを押して、LTTng セッションが実行されている端末で LTTng セッションを停止します。

4. 対象アプリケーションを停止します

<prettier-ignore-start>
!!!info
      起動後すぐに計測を開始したい場合は、手順1と手順2を逆に行ってください。
      ターゲット アプリケーションを実行する前に、最初に Lttng セッションを開始することもできます。
      ただし、対象アプリケーションの起動中にrecordingが開始されると、録画が失われる可能性があります。
      起動開始前または起動完了後にrecordingを起動してください。
<prettier-ignore-end>

<prettier-ignore-start>
!!!info
      LTTng を 2.13 にアップデートした後、数百のノードを持つ [Autoware](https://github.com/autowarefoundation/autoware) のような大規模なアプリケーションに CARET を適用すると、記録されたデータのサイズが予想よりも奇妙に小さいことに気づく場合があります。この場合、ファイル記述子の最大数が十分ではないことを疑う必要があります。`ulimit -n`コマンドで番号を確認できます。デフォルトの最大数は 1024 ですが、大規模なアプリケーションには十分ではありません。コマンドを実行して最大数を大きくすることで、この問題を回避できます。`ulimit -n 65536`。
<prettier-ignore-end>

<prettier-ignore-start>
!!!info
      マルチホスト システムをトレースするには、トレースするノードを含むホストで次の手順を実行する必要があります。
<prettier-ignore-end>

## ROS 起動による LTTng セッションの開始

ROS 起動システムを使用して LTTng セッションを開始できます。1 つの端末でターゲット アプリケーションを起動した場合は、上で説明したように LTTng セッションを開始するために別の端末を開く必要があります。複数の端末を操作するのはユーザーにとって手間がかかります。CARET を繰り返し適用するには、ROS 起動によるアプリケーションとともに LTTng セッションを開始するのが合理的な方法です。

1. まだ作成していない場合は、ROS の一般的な方法でターゲット アプリケーションの起動ファイルを作成します。

   ```py
   # launch/end_to_end_sample.launch.py
   import launch
   import launch_ros.actions


   def generate_launch_description():
       return launch.LaunchDescription([
           launch_ros.actions.Node(
               package='caret_demos', executable='end_to_end_sample', output='screen'),
       ])
   ```

2. LTTng セッションを開始するための説明を追加します

   ```py
   # launch/end_to_end_sample_with_lttng_session.launch.py
   import launch
   import launch_ros.actions
   from tracetools_launch.action import Trace


   def generate_launch_description():
       return launch.LaunchDescription([
           Trace(
               session_name='e2e_sample',
               events_kernel=[],
               events_ust=['ros2*']
           ),
           launch_ros.actions.Node(
               package='caret_demos', executable='end_to_end_sample', output='screen'),
       ])
   ```

3. 起動ファイルを介してターゲット アプリケーションと LTTng セッションを起動します
   - 環境設定は必要ですが、すべての操作が 1 つの端末だけで実行されます

   ```sh
   source /opt/ros/humble/setup.bash
   source ~/ros2_caret_ws/install/local_setup.bash
   source ~/ros2_ws/install/local_setup.bash

   export LD_PRELOAD=$(readlink -f ~/ros2_caret_ws/install/caret_trace/lib/libcaret.so)

   source ./caret_topic_filter.bash

   ros2 launch caret_demos end_to_end_sample_with_lttng_session.launch.py
   ```

<prettier-ignore-start>
!!!info
      マルチホスト システムをトレースするには、トレースするノードを含むホストで次の手順を実行する必要があります。
<prettier-ignore-end>

## 詳細: 起動ファイルの便利な設定

- 次のスクリプトは、起動ファイルの詳細設定を示しています。
- `caret_session` オプションはセッション名の設定に使用されます。割り当てられていない場合は、日時 (YYYYMMDD-HHMMSS) が使用されます。
- `caret_light` オプションは、別のイベント フィルターを追加するために使用されます。`caret_event` 変数で指定されたイベントのみが記録されます。この例では、`caret_light` が「true」に設定されている場合、ros2:rclcpp レイヤなどの高レベルのイベントが記録されます。この設定は、大規模なアプリケーションを記録する場合に役立ちます。
  - [tracepoint summary](./cli_tool.md#tracepoint-summary) を参照してどのイベントが記録されているかを確認し、必要に応じて `caret_event` を変更してください。

```py
# launch/end_to_end_sample_with_lttng_session.launch.py
import launch
import launch_ros.actions
from tracetools_launch.action import Trace

import sys
import datetime
from distutils.util import strtobool


def generate_launch_description():
  caret_session = ""
  caret_event = ["ros2*"]
  caret_light = True

  for arg in sys.argv:
    if arg.startswith("caret_session:="):
      caret_session = arg.split(":=")[1]
    elif arg.startswith("caret_light:="):
      try:
        caret_light = strtobool(arg.split(":=")[1]) # 0 or 1
      except:
        print("Invalid arguments 'caret_light'.")
        print("Start tracing with 'ros2*'.")

  if caret_light:
    caret_event = [
            "ros2:*callback*",
            "ros2_caret:*callback*",
            "ros2:dispatch*",
            "ros2_caret:dispatch*",
            "ros2:rclcpp*" ,
            "ros2_caret:rclcpp*" ,
            "ros2_caret:rmw*",
            "ros2:rmw_take",
            "*callback_group*",
            "ros2_caret:*executor",
            "ros2_caret:dds_bind*",
            "ros2:rcl_*init",
            "ros2_caret:rcl_*init",
            "ros2_caret:caret_init"]

  if caret_session == "":
    dt_now = datetime.datetime.now()
    caret_session = "autoware_launch_trace_" + dt_now.strftime("%Y%m%d-%H%M%S")

  return launch.LaunchDescription([
    Trace(
      session_name=caret_session,
      events_kernel=[],
      events_ust=caret_event
    ),
    launch_ros.actions.Node(
        package='caret_demos', executable='end_to_end_sample', output='screen'),
  ])
```
