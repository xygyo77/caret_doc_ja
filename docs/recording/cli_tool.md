# recording 用の CLI ツール

CARET は、recording プロセスで利用できる CLI ツールを提供します。

<prettier-ignore-start>
!!!info
      これらのCLIツールを使用するには、以下のコマンドでCARETの環境設定を行う必要があります。

      ```bash
      source /opt/ros/humble/setup.bash
      source ~/ros2_caret_ws/install/local_setup.bash
      ```

<prettier-ignore-end>

## ビルド結果の検証

このコマンドは、ターゲット アプリケーションが CARET/rclcpp で正常にビルドされたかどうかを確認します。([See details](./build_check.md#check-whether-caretrclcpp-is-applied-to-each-package))

```bash
ros2 caret check_caret_rclcpp <path-to-workspace>
```

```bash
---Output text as below---

INFO    : 2022-09-29 20:18:43 | All packages are built using caret-rclcpp.
```

## Recording

このコマンドは、LTTng セッションと recording シーケンスを開始します。([See details](./recording.md))

`All process started recording`が表示された後、Recordingが始まります。

```bash
ros2 caret record --session-name <session_name> --recording-frequency <recording_frequency> --verbose
```

<!-- Please refer to [name of page](path) for detail of `<recording_frequency>`. -->

`<recording_frequency>` の値を増やすと、recording の開始に必要な時間が短縮されます。
ただし、`<recording_frequency>`に大きな値を与えると、recordingが`Tracer discarded`を引き起こす可能性が高くなります。
`-f` は `--recording-frequency` の短いオプションです
【TODO】詳細の参考としてデザインページへのリンクを追加します。

`--verbose` オプションを使用すると、recording シーケンスのステータスを詳細に確認できます。
`-v` は `--verbose` の短いオプションです

## トレースデータの検証

このコマンドは、recording が成功したかどうかを確認します。([See details](./validating.md#validating-trace-data))

記録データに問題がある場合は警告メッセージが表示されます

```bash
ros2 caret check_ctf <path-to-trace-data>
```

## ノードの概要

このコマンドは、ノードごとのイベント数を表示します。

```bash
ros2 caret node_summary <path-to-trace-data>
```

```bash
---Output text as below---

=============================================
Trace creation datetime | 2022-07-16 17:34:07
Trace range             | 17:34:07 ~ 17:35:08
Trace duration          | 0:01:00
=============================================

 node_name            |   number_of_trace_points
----------------------+--------------------------
 /message_driven_node |                     4207
 /timer_driven_node   |                     3630
 /filter_node         |                     2680
 /drive_node          |                     2146
 /sensor_dummy_node   |                     2144
 /actuator_dummy_node |                     1609
```

## トピックの概要

このコマンドは、トピックごとのイベント数を表示します。

```bash
ros2 caret topic_summary <path-to-trace-data>
```

```bash
---Output text as below---

=============================================
Trace creation datetime | 2022-07-16 17:34:07
Trace range             | 17:34:07 ~ 17:35:08
Trace duration          | 0:01:00
=============================================

 topic_name        |   number_of_trace_points
-------------------+--------------------------
 /drive            |                     2668
 /topic1           |                     2668
 /topic2           |                     2668
 /topic4           |                     2658
 /topic3           |                     2478
 /parameter_events |                       66
 /rosout           |                        6
```

<prettier-ignore-start>
!!!info
      イベントの数が多すぎて処理できない場合は、出力結果に基づいて不要なノード/トピックを除外する [trace filtering](./trace_filtering.md) が合理的な選択です。
<prettier-ignore-end>

## トレースポイントの概要

このコマンドは、トレース データに含まれるすべてのトレースポイントと、トレースポイントによって収集されたイベントの数を表示します。

```bash
ros2 caret trace_point_summary <path-to-trace-data>
```

```bash
---Output text as below---

=============================================
Trace creation datetime | 2022-07-16 17:34:07
Trace range             | 17:34:07 ~ 17:35:08
Trace duration          | 0:01:00
=============================================

 trace_point                                       |   number_of_trace_points
---------------------------------------------------+--------------------------
 ros2:callback_end                                 |                     4216
 ros2:callback_start                               |                     4216
 ros2_caret:dds_write                              |                     2790
 ros2_caret:dds_bind_addr_to_stamp                 |                     2790
 ros2:rcl_publish                                  |                     2650
 ros2:rclcpp_publish                               |                     2650
 ros2:dispatch_subscription_callback               |                     2620
 ros2:rclcpp_subscription_callback_added           |                       44
 ros2:rclcpp_service_callback_added                |                       44
 ros2:rclcpp_callback_register                     |                       44
 ros2:rclcpp_timer_callback_added                  |                       44
 ros2_caret:callback_group_add_service             |                       36
 ros2:rcl_service_init                             |                       36
 ros2:rcl_publisher_init                           |                       17
 ros2_caret:callback_group_add_subscription        |                       11
 ros2:rcl_node_init                                |                        6
 ros2_caret:add_callback_group                     |                        6
 ros2:rcl_subscription_init                        |                        5
 ros2:rclcpp_subscription_init                     |                        5
 ros2:rcl_timer_init                               |                        3
 ros2:rclcpp_timer_link_node                       |                        3
 ros2_caret:callback_group_add_timer               |                        3
 ros2_caret:construct_executor                     |                        1
 ros2_caret:rmw_implementation                     |                        1
 ros2:rcl_init                                     |                        1
 ros2:rcl_client_init                              |                        0
 ros2:dispatch_intra_process_subscription_callback |                        0
 ros2_caret:tilde_subscribe_added                  |                        0
 ros2_caret:tilde_subscribe                        |                        0
 ros2_caret:tilde_publisher_init                   |                        0
 ros2_caret:tilde_publish                          |                        0
 ros2_caret:sim_time                               |                        0
 ros2_caret:on_data_available                      |                        0
 ros2:message_construct                            |                        0
 ros2_caret:dds_bind_addr_to_addr                  |                        0
 ros2_caret:construct_static_executor              |                        0
 ros2:rclcpp_intra_publish                         |                        0
 ros2:rcl_lifecycle_transition                     |                        0
 ros2:rcl_lifecycle_state_machine_init             |                        0
 ros2_caret:callback_group_add_client              |                        0
 ros2_caret:add_callback_group_static_executor     |                        0
 ros2_caret:tilde_subscription_init                |                        0
```

## サマリーコマンドのフィルタリング

膨大なトレースデータ (10 分以上など) のサマリーコマンドを実行するには時間がかかります。
次の 2 つのオプションを使用すると、サマリー出力に使用されるトレース データの負荷範囲をフィルタリングできます。
どちらのオプションでも、引数の型は float で、時間の単位は秒です。

```bash
ros2 caret trace_point_summary <path-to-trace-data> --duration_filter <DURATION> <OFFSET>
ros2 caret trace_point_summary <path-to-trace-data> --strip_filter <LSTRIP> <RSTRIP>
```

- `--duration_filter [DURATION] [OFFSET]`
  - [OFFSET]からこの[DURATION]のみを読み込みます。
- `--strip_filter [LSTRIP] [RSTRIP]`
  - 開始/終了から指定秒間のトレース データを無視します。

```bash
---Output text as below---

=============================================
Trace creation datetime | 2022-07-16 17:34:07
Trace range             | 17:34:07 ~ 17:35:08
Trace duration          | 0:01:00
Filtered trace range    | 17:34:15 ~ 17:34:45
Filtered trace duration | 0:00:29
=============================================

 trace_point                                       |   number_of_trace_points
---------------------------------------------------+--------------------------
 ros2:callback_end                                 |                     2385
 ros2:callback_start                               |                     2385
 ros2:dispatch_subscription_callback               |                     1485
 ros2:rcl_publish                                  |                     1484
 ros2_caret:dds_write                              |                     1484
 ros2_caret:dds_bind_addr_to_stamp                 |                     1484
 ros2:rclcpp_publish                               |                     1484
 ros2:rclcpp_subscription_callback_added           |                       44
 ros2:rclcpp_service_callback_added                |                       44
 ros2:rclcpp_callback_register                     |                       44
 ros2:rclcpp_timer_callback_added                  |                       44
 ros2_caret:callback_group_add_service             |                       36
 ros2:rcl_service_init                             |                       36
 ros2:rcl_publisher_init                           |                       17
 ros2_caret:callback_group_add_subscription        |                       11
 ros2:rcl_node_init                                |                        6
 ros2_caret:add_callback_group                     |                        6
 ros2:rcl_subscription_init                        |                        5
 ros2:rclcpp_subscription_init                     |                        5
 ros2:rcl_timer_init                               |                        3
 ros2:rclcpp_timer_link_node                       |                        3
 ros2_caret:callback_group_add_timer               |                        3
 ros2_caret:construct_executor                     |                        1
 ros2_caret:rmw_implementation                     |                        1
 ros2:rcl_init                                     |                        1
 ros2:rcl_client_init                              |                        0
 ros2:dispatch_intra_process_subscription_callback |                        0
 ros2_caret:tilde_subscribe_added                  |                        0
 ros2_caret:tilde_subscribe                        |                        0
 ros2_caret:tilde_publisher_init                   |                        0
 ros2_caret:tilde_publish                          |                        0
 ros2_caret:sim_time                               |                        0
 ros2_caret:on_data_available                      |                        0
 ros2:message_construct                            |                        0
 ros2_caret:dds_bind_addr_to_addr                  |                        0
 ros2_caret:construct_static_executor              |                        0
 ros2:rclcpp_intra_publish                         |                        0
 ros2:rcl_lifecycle_transition                     |                        0
 ros2:rcl_lifecycle_state_machine_init             |                        0
 ros2_caret:callback_group_add_client              |                        0
 ros2_caret:add_callback_group_static_executor     |                        0
 ros2_caret:tilde_subscription_init                |                        0
```
