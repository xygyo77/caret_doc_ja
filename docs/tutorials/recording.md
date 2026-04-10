# Recording と CARET

このページでは、CARETの使用方法をサンプルアプリケーションで説明します。
サンプル アプリケーションは [caret_demos](https://github.com/tier4/caret_demos.git) リポジトリにあります。

詳細については、[Recording](../recording/index.md) を参照してください。

## CARET を使用してアプリケーションを構築する

ターゲット アプリケーションをトレースするには、CARET/rclcpp を使用してターゲットをビルドする必要があります。CARET/rclcpp を使用せずにターゲットをすでにビルドしている場合は、CARET/rclcpp を使用してターゲットを再度ビルドする必要があります。CARET/rclcpp を使用してアプリケーションをビルドするには、以下に示すように、CARET の `local_setup.bash` を ROS 2 の `setup.bash` とともに適用する必要があります。

=== "humble"

    ``` bash
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws

    git clone https://github.com/tier4/caret_demos.git src/caret_demos

    source /opt/ros/humble/setup.bash
    source ~/ros2_caret_ws/install/local_setup.bash # please keep the order after 'source /opt/ros/humble/setup.bash'

    colcon build --symlink-install --packages-up-to caret_demos --cmake-args -DBUILD_TESTING=OFF
    ```

=== "iron"

    ``` bash
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws

    git clone https://github.com/tier4/caret_demos.git src/caret_demos

    source /opt/ros/iron/setup.bash

    colcon build --symlink-install --packages-up-to caret_demos --cmake-args -DBUILD_TESTING=OFF
    ```

=== "jazzy"

    ``` bash
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws

    git clone https://github.com/tier4/caret_demos.git src/caret_demos

    source /opt/ros/jazzy/setup.bash

    colcon build --symlink-install --packages-up-to caret_demos --cmake-args -DBUILD_TESTING=OFF
    ```

次のコマンドを実行すると、各パッケージに CARET/rclcpp が適用されているかどうかを確認できます。
記録するパッケージに caret/rclcpp が適用されていない場合は、ターゲットおよびワークスペースの環境変数にどの rclcpp が使用されているかを確認してください。

```bash
ros2 caret check_caret_rclcpp ~/ros2_ws/

# Expected output. CARET/rclcpp is applied to all packages
INFO    : 2022-06-12 12:26:49 | All packages are built using caret-rclcpp.

# In case there are packages to which CARET/rclcpp is not applied
# The following message will be outputted
WARNING : 2022-06-12 12:25:26 | The following packages have not been built using caret-rclcpp:
   demo_nodes_cpp
   caret_demos
   intra_process_demo
```

<details>
<summary>iron</summary>以降

次のコマンドを実行する必要はありません。

```bash
ros2 caret check_caret_rclcpp ~/ros2_ws/
```

CARET では、iron 以降の ROS 2 ディストリビューションで caret-rclcpp を使用したビルドは必要ありません。

</details>

## CARET を使用してサンプル アプリケーションをトレースする

### 対象アプリケーションの起動

以下に示すようにターゲットを実行します。

=== "humble"

    ``` bash
    # Environment settings (keep the order as below)
    source /opt/ros/humble/setup.bash
    source ~/ros2_caret_ws/install/local_setup.bash
    source ~/ros2_ws/install/local_setup.bash

    # Enable tracepoints which are defined hooked functions.
    export LD_PRELOAD=$(readlink -f ~/ros2_caret_ws/install/caret_trace/lib/libcaret.so)

    # (Optional) Exclude nodes and topics which you are not concerned with
    export CARET_IGNORE_NODES="/rviz*"
    export CARET_IGNORE_TOPICS="/clock:/parameter_events"

    # Launch the target application, demos_end_to_end_sample
    ros2 launch caret_demos end_to_end_sample.launch.py
    ```

=== "iron"

    ``` bash
    # Environment settings (keep the order as below)
    source /opt/ros/iron/setup.bash
    source ~/ros2_caret_ws/install/local_setup.bash
    source ~/ros2_ws/install/local_setup.bash

    # Enable tracepoints which are defined hooked functions.
    export LD_PRELOAD=$(readlink -f ~/ros2_caret_ws/install/caret_trace/lib/libcaret.so)

    # (Optional) Exclude nodes and topics which you are not concerned with
    export CARET_IGNORE_NODES="/rviz*"
    export CARET_IGNORE_TOPICS="/clock:/parameter_events"

    # Launch the target application, demos_end_to_end_sample
    ros2 launch caret_demos end_to_end_sample.launch.py
    ```

=== "jazzy"

    ``` bash
    # Environment settings (keep the order as below)
    source /opt/ros/jazzy/setup.bash
    source ~/ros2_caret_ws/install/local_setup.bash
    source ~/ros2_ws/install/local_setup.bash

    # Enable tracepoints which are defined hooked functions.
    export LD_PRELOAD=$(readlink -f ~/ros2_caret_ws/install/caret_trace/lib/libcaret.so)

    # (Optional) Exclude nodes and topics which you are not concerned with
    export CARET_IGNORE_NODES="/rviz*"
    export CARET_IGNORE_TOPICS="/clock:/parameter_events"

    # Launch the target application, demos_end_to_end_sample
    ros2 launch caret_demos end_to_end_sample.launch.py
    ```

### recording を開始します

新しいターミナルを開き、パフォーマンス データを記録します。

=== "humble"

    ``` bash
    source /opt/ros/humble/setup.bash
    source ~/ros2_caret_ws/install/local_setup.bash

    # set a destination directory. ~/.ros/tracing is default.
    mkdir -p ~/ros2_ws/evaluate
    export ROS_TRACE_DIR=~/ros2_ws/evaluate

    ros2 caret record -s e2e_sample

    # Start recording with pressing Enter key
    # > All process tarted recording.
    # > press enter to stop...
    ```

=== "iron"

    ``` bash
    source /opt/ros/iron/setup.bash
    source ~/ros2_caret_ws/install/local_setup.bash

    # set a destination directory. ~/.ros/tracing is default.
    mkdir -p ~/ros2_ws/evaluate
    export ROS_TRACE_DIR=~/ros2_ws/evaluate

    ros2 caret record -s e2e_sample

    # Start recording with pressing Enter key
    # > All process tarted recording.
    # > press enter to stop...
    ```

=== "jazzy"

    ``` bash
    source /opt/ros/jazzy/setup.bash
    source ~/ros2_caret_ws/install/local_setup.bash

    # set a destination directory. ~/.ros/tracing is default.
    mkdir -p ~/ros2_ws/evaluate
    export ROS_TRACE_DIR=~/ros2_ws/evaluate

    ros2 caret record -s e2e_sample

    # Start recording with pressing Enter key
    # > All process tarted recording.
    # > press enter to stop...
    ```

## 記録されたデータを簡単に検証する

記録データを可視化する前に、`ros2 caret check_ctf`コマンドでトレースが成功したかどうかを確認できます。

```bash
ros2 caret check_ctf ~/ros2_ws/evaluate/e2e_sample/

# If there are problems with the recorded data, warning messages will be displayed.
```
