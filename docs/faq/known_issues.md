<!-- cspell:ignore Drclcpp Dtracetools ltracetools -->

# 既知の問題

## インストール

### `setup.py` による警告

- 問題
  - CARET をビルドすると次の警告が発生します

```sh
/usr/local/lib/python3.10/dist-packages/setuptools/command/develop.py:40: EasyInstallDeprecationWarning: easy_install command is deprecated.
!!

        ********************************************************************************
        Please avoid running ``setup.py`` and ``easy_install``.
        Instead, use pypa/build, pypa/installer or other
        standards-based tools.

        See https://github.com/pypa/setuptools/issues/917 for details.
        ********************************************************************************

!!
  easy_install.initialize_options(self)
```

```sh
/usr/local/lib/python3.10/dist-packages/setuptools/_distutils/cmd.py:66: SetuptoolsDeprecationWarning: setup.py install is deprecated.
!!

        ********************************************************************************
        Please avoid running ``setup.py`` directly.
        Instead, use pypa/build, pypa/installer or other
        standards-based tools.

        See https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html for details.
        ********************************************************************************

!!
  self.initialize_options()
```

- 原因
  - Python3 では `setup.py` を使用したビルドは非推奨になります
  - ただし、`setup.py` は、colcon による ROS 2 のビルドに使用されます
- 回避策
  - この警告は CARET の動作を妨げるものではなく、アクションは必要ありません
  - ただし、本当に警告を削除したい場合は、次の手順を実行して警告を抑制できます。

```sh
export PYTHONWARNINGS=ignore:"setup.py install is deprecated.",ignore:"easy_install command is deprecated."
```

## Build

### `libtracetools.so` に対する依存関係の競合

- 問題
  - `pcl_ros` などの特定のパッケージを使用してターゲット アプリケーションをビルドすると、次のエラーが発生します。
    - ``undefined reference to `ros_trace_message_construct'``
    - ``undefined reference to `ros_trace_rclcpp_intra_publish'``
    - ``undefined reference to `ros_trace_dispatch_subscription_callback'``等々
- 原因
  - `~/ros2_caret_ws/install/tracetools/lib/libtracetools.so`をリンクする必要がありますが、一部のパッケージを使用する場合は`/opt/ros/humble/lib/libtracetools.so`が参照されます
  - たとえば、`pcl_ros` パッケージには `/opt/ros/humble/share/pcl_ros/cmake/export_pcl_rosExport.cmake` があり、これにより `/opt/ros/humble/lib/libtracetools.so` が強制的にリンクされます
- 回避策 1
  - 次のビルドオプションを試して、`-Dtracetools_DIR` を明示的に設定して CARET トレースツール ライブラリが使用されるようにしてください。
  - これは、ターゲットアプリケーションが `--merge-install` でビルドされている場合に特に発生する可能性があります。

```sh
colcon build --symlink-install --cmake-args -DBUILD_TESTING=OFF \
  -Drclcpp_DIR="$HOME/ros2_caret_ws/install/rclcpp/share/rclcpp/cmake" \
  -Dtracetools_DIR="$HOME/ros2_caret_ws/install/tracetools/share/tracetools/cmake"

or

colcon build --symlink-install --cmake-args -DBUILD_TESTING=OFF \
  -DCMAKE_SHARED_LINKER_FLAGS="-L$HOME/ros2_caret_ws/install/tracetools/lib -ltracetools" \
  -DCMAKE_EXE_LINKER_FLAGS="-L$HOME/ros2_caret_ws/install/tracetools/lib -ltracetools" \
  -Drclcpp_DIR="$HOME/ros2_caret_ws/install/rclcpp/share/rclcpp/cmake" \
  -Dtracetools_DIR="$HOME/ros2_caret_ws/install/tracetools/share/tracetools/cmake"
```

- 回避策 2
  - `/opt/ros/humble/share/pcl_ros/cmake/export_pcl_rosExport.cmake` から `/opt/ros/humble/lib/libtracetools.so;` を削除します

```sh
sudo cp /opt/ros/humble/share/pcl_ros/cmake/export_pcl_rosExport.cmake /opt/ros/humble/share/pcl_ros/cmake/export_pcl_rosExport.cmake.bak
sudo sed -i -e 's/\/opt\/ros\/humble\/lib\/libtracetools.so;//g' /opt/ros/humble/share/pcl_ros/cmake/export_pcl_rosExport.cmake
```

- 回避策 3
  - 回避策 2 を適用してもエラーが解決しない場合は、すべてのライブラリから`/opt/ros/humble/lib/libtracetools.so;` を削除します

```sh
sudo grep -rl '/opt/ros/humble/lib/libtracetools.so;' /opt/ros/humble/share --include="*.cmake" |
    while read -r f; do
        echo "Delete reference to libtracetools from $f"
        sudo cp "$f" "$f.bak"
        sudo sed -i 's|/opt/ros/humble/lib/libtracetools.so;||g' "$f"
    done
```

### SYSTEM の rclcpp が参照されています

- 問題
  - 対象アプリケーションのビルド時に以下のエラーが発生する

```sh
/opt/ros/humble/include/rclcpp/rclcpp/publisher.hpp: In member function ‘void rclcpp::Publisher<MessageT, AllocatorT>::do_inter_process_publish(const ROSMessageType&)’:
/opt/ros/humble/include/rclcpp/rclcpp/publisher.hpp:452:5: error: too few arguments to function ‘void ros_trace_rclcpp_publish(const void*, const void*, uint64_t)’
  452 |     TRACEPOINT(rclcpp_publish, nullptr, static_cast<const void *>(&msg));
```

- 原因
  - CARET、caret/rclcppを使用してビルドする必要があります。ただし、何らかの理由で SYSTEM ( `/opt/ros/humble` ) の rclcpp が使用されている場合、ビルドは失敗します。
  - `pcl_ros` を例にとると、`/opt/ros/humble/share/pcl_ros/cmake/export_pcl_rosExport.cmake` は `/opt/ros/humble/include/rclcpp` の参照を強制します。そのため、caret/rclcpp は使用されず、`pcl_ros` に依存するパッケージのビルドは失敗します。
- 回避策 1
  - `/opt/ros/humble/share/pcl_ros/cmake/export_pcl_rosExport.cmake` から `/opt/ros/humble/include/rclcpp;` を削除します

```sh
sudo cp /opt/ros/humble/share/pcl_ros/cmake/export_pcl_rosExport.cmake /opt/ros/humble/share/pcl_ros/cmake/export_pcl_rosExport.cmake.bak2
sudo sed -i -e 's/\/opt\/ros\/humble\/include\/rclcpp;//g' /opt/ros/humble/share/pcl_ros/cmake/export_pcl_rosExport.cmake
```

- 回避策 2
  - 回避策 1 を適用してもエラーが解決しない場合は、すべてのライブラリを変更します。

```sh
sudo grep -rl '/opt/ros/humble/include/rclcpp;' /opt/ros/humble/share --include="*.cmake" |
    while read -r f; do
        echo "Delete reference to rclcpp from $f"
        sudo cp "$f" "$f.bak"
        sudo sed -i 's|/opt/ros/humble/include/rclcpp;||g' "$f"
    done
```

- 回避策 3
  - 回避策 1 と 2 を適用してもエラーが解決しない場合は、`-Drclcpp_DIR` を明示的に設定して CARET rclcpp が使用されていることを確認してください。
  - これは、ターゲットアプリケーションが `--merge-install` でビルドされている場合に特に発生する可能性があります。

```sh
--cmake-args -Drclcpp_DIR="$HOME/ros2_caret_ws/install/rclcpp/share/rclcpp/cmake"
```

### ament_cmake を使用してビルドする

- 問題
  - ament_cmakeを使用してターゲットアプリケーションをビルドすると、次のエラーが発生します
    - `error: too few arguments to function ‘void ros_trace_rclcpp_publish`
- 原因
  - `SYSTEM` は、[this PR](https://github.com/ament/ament_cmake/commit/799183ab9bcfd9b66df0de9b644abaf8c9b78e84) によって ament_cmake_auto に依存関係として追加されます。その結果、一部のパッケージでは CARET/rclcpp ではなく ros2/rclcpp が使用されます。
- 回避策
  - ament_cmake_auto の依存関係から `SYSTEM` を削除します

```sh
cd /opt/ros/humble/share/ament_cmake_auto/cmake/
sudo cp ament_auto_add_executable.cmake ament_auto_add_executable.cmake.bak
sudo cp ament_auto_add_library.cmake ament_auto_add_library.cmake.bak
sudo sed -i -e 's/SYSTEM//g' ament_auto_add_executable.cmake
sudo sed -i -e 's/SYSTEM//g' ament_auto_add_library.cmake
```

## Recording

### メタデータのみが記録されます

- 問題
  - メタデータファイル(`~/.ros/tracing/ooo/ust/uid/1000/64-bit/metadata`)のみが作成され、トレースデータのサイズは常に約28KByteになります
- 原因
  - LTTng バッファのサイズが一部の環境では大きすぎます
  - 特に次のような場合に起こります。
    - Docker 上の Recording
    - CPU の数が多い (例: 24 コア)
- 回避策
  - LTTngバッファサイズの数値を小さくします
    - [lttng_impl.py](https://github.com/tier4/ros2_tracing/blob/64545052077d38c770b0c6e73fad221bcaba0583/tracetools_trace/tracetools_trace/tools/lttng_impl.py#L157)
      - 変更後のリビルドは不要です
    - バッファ サイズを小さくすると、トレーサが破棄される可能性があることに注意してください
