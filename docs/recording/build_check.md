<!-- cspell:ignore Drclcpp Dtracetools ltracetools -->

# CARET でビルドする

## CARET を使用してターゲットアプリケーションをビルドします

トレースデータを記録するには、ターゲットアプリケーションを CARET/rclcpp でビルドする必要があります。CARET/rclcpp を使用せずにアプリケーションをすでにビルドしている場合は、CARET/rclcpp を使用してアプリケーションを再度ビルドする必要があります。

CARET/rclcpp を使用してアプリケーションをビルドするには、以下に示すように、CARET の `local_setup.bash` を ROS 2 の `setup.bash` とともに適用する必要があります。また、ビルドオプションには`-DBUILD_TESTING=OFF`を与える必要があります。

```sh
cd <path-to-workspace>

source /opt/ros/humble/setup.bash
source ~/ros2_caret_ws/install/local_setup.bash  # please keep the order after ROS 2's setup.bash

colcon build --symlink-install --cmake-args -DBUILD_TESTING=OFF
```

<prettier-ignore-start>
!!!info "How to fix build errors and caret-rclcpp check errors"
      ビルドエラーが発生したり、`check_caret_rclcpp`(後述)で警告が表示される場合は、以下のビルドオプションをお試しください。特定のエラー メッセージとその原因の詳細については、[Known Issues - Build](../faq/known_issues.md#build) を参照してください。

      ```sh
      colcon build --symlink-install --cmake-args -DBUILD_TESTING=OFF \
        -Drclcpp_DIR="$HOME/ros2_caret_ws/install/rclcpp/share/rclcpp/cmake" \
        -Dtracetools_DIR="$HOME/ros2_caret_ws/install/tracetools/share/tracetools/cmake"
      ```

      または

      ```sh
      colcon build --symlink-install --cmake-args -DBUILD_TESTING=OFF \
        -DCMAKE_SHARED_LINKER_FLAGS="-L$HOME/ros2_caret_ws/install/tracetools/lib -ltracetools" \
        -DCMAKE_EXE_LINKER_FLAGS="-L$HOME/ros2_caret_ws/install/tracetools/lib -ltracetools" \
        -Drclcpp_DIR="$HOME/ros2_caret_ws/install/rclcpp/share/rclcpp/cmake" \
        -Dtracetools_DIR="$HOME/ros2_caret_ws/install/tracetools/share/tracetools/cmake"
      ```

<prettier-ignore-end>

<prettier-ignore-start>
!!!info "Reason for building a target application with CARET/rclcpp"
      CARET/rclcpp は [ROS 2-based rclcpp](https://github.com/ros2/rclcpp) のフォークであり、CARET によって定義された追加のトレースポイントがいくつかあります。
      CARET がターゲット アプリケーションを記録するには、rclcpp ヘッダー ファイルによって参照されるテンプレート実装にいくつかのトレースポイントを追加する必要があります。
      追加のトレースポイントを持つ rclcpp を適用するには、アプリケーションを CARET/rclcpp で再度ビルドする必要があります。
      したがって、CARET は、`demo_nodes_cpp` などの Ubuntu の aptitude によって提供されるアプリケーションをトレースできません。
      このようなビルド前のパッケージをトレースしたい場合は、ソース コードから再度ビルドしてください。
<prettier-ignore-end>

<prettier-ignore-start>
!!!info "Reason for giving `-DBUILD_TESTING=OFF`"
      CARET を使用するには、CARET/rclcpp などのフォークされた共有ライブラリとヘッダを使用する必要があります。
      テストコードでは、ヘッダの読み込み優先順位の問題により、CARET/rclcpp は使用できません。
      CARET のバージョンによっては、共有ライブラリ間で競合が発生する可能性があります。
      ros-rclcpp と CARET/rclcpp のヘッダーにより、コンパイル エラーが発生します。
      したがって、テストコードはビルドから除外する必要があります。
<prettier-ignore-end>

## 各パッケージにCARET/rclcppが適用されているか確認する

`ros2 caret check_caret_rclcpp` コマンドを使用して、CARET/rclcpp で対象のアプリケーションが正常にビルドされたかどうかを確認できます。

```sh
ros2 caret check_caret_rclcpp <path-to-workspace>
```

|出力メッセージ |説明 |
|-------------------------------------------------------------- |---------------------------------------------------------------------------------------------- |
|`All packages are built using caret-rclcpp` |問題ありません |
|`The following packages have not been built using caret-rclcpp` |CARET/rclcpp は、リストされているパッケージ <br> に適用されていません (修正するには次のセクションをお読みください)。

## 修正方法

分析したいパッケージに CARET/rclcpp が適用されていない場合は、修正する必要があります。考えられる原因と解決策を以下に示します。

- ケース 1: すべてのパッケージが CARET/rclcpp としてリストされ、適用されません
  - ROS 2 の `setup.bash` の後に CARET の `local_setup.bash` を適用していることを確認してください (順序を維持してください)
- ケース 2: すべてではなく、一部のパッケージが CARET/rclcpp が適用されていないとしてリストされます
  - リストされたパッケージの `package.xml` に次の行があることを確認してください。
    - `<depend>rclcpp</depend>`

<prettier-ignore-start>
!!!info
      CARET/rclcpp でビルドされた他のパッケージは適切にトレースされますが、リストされたパッケージはトレースされません。したがって、リストされたパッケージをトレース/分析する必要がない場合は、このメッセージを無視してかまいません。
<prettier-ignore-end>
