# バイナリのインストール

一部の caret パッケージは Debian パッケージとして利用できます。
次の表に、バイナリ インストールを使用してインストールできるパッケージを示します。

|パッケージ名 |パッケージの説明 |バイナリのインストール |
|---------------------------------------------------------------------- |---------------------------------------------------------------------------- |:-----------: |
|[caret_trace](https://github.com/tier4/caret_trace/tree/main/CARET_trace) |関数フックによって追加されたトレースポイントを定義する |× |
|[caret_msgs](https://github.com/tier4/caret_trace/tree/main/caret_msgs) |caret | で定義されるメッセージ タイプ○ |
|[caret_analyze](https://github.com/tier4/caret_analyze) |データを分析および視覚化するためのスクリプトのライブラリ |○ |
|[caret_analyze_cpp_impl](https://github.com/tier4/caret_analyze_cpp_impl) |C++ で記述されたトレース データを分析するための効率的なヘルパー関数 |○ |
|[ros2caret](https://github.com/tier4/ros2caret.git) |`ros2 caret` のような CLI コマンド |○ |
|[rclcpp](https://github.com/tier4/rclcpp/tree/v0.3.0) |CARET 専用のトレースポイントを含む、フォークされた rclcpp× |
|[ros2_tracing](https://github.com/tier4/ros2_tracing/tree/v0.3.0) |CARET 専用のトレースポイントの定義を含む、フォークされた `ros2_tracing`× |

<prettier-ignore-start>
!!! Note
    バイナリインストールでインストールできるのは、トレースデータ解析用のパッケージのみです。
    バイナリには、recording トレース データのパッケージは含まれていません。
<prettier-ignore-end>

＃＃ 要件

CARET は、次の表に示すプラットフォームでサポートされているバージョンで動作することが確認されています。

|依存プラットフォーム |サポートされているバージョン |
|------------------ |----------------- |
|ロス |Humble |
|Ubuntu |4月22日 |
|LTTng |安定版-2.13 |
|Linux カーネル |5.15.x |
|Python3 |3.10.x |

## 必要なパッケージのインストール

apt リポジトリのキャッシュを更新します。

```bash
sudo apt update
```

CARET バイナリ パッケージには次のパッケージが必要です。
これらの依存関係は、バイナリ インストールでは自動的にインストールされません。

```bash
sudo apt install python3-bt2
python3 -m pip install -U \
  pandas>=2.1.1 \
  bokeh>=3 \
  jupyterlab \
  multimethod
```

## CARET パッケージをインストールする

ROS ビルド ファームでリリースされた caret パッケージをインストールします。
ここでインストールされるパッケージはトレースデータ解析に関連するパッケージのみです。

```bash
sudo apt install -y \
  ros-humble-caret-analyze \
  ros-humble-caret-analyze-cpp-impl \
  ros-humble-ros2caret \
  ros-humble-caret-msgs
```

以下のコマンドでインストールが成功したことを確認できます。

```bash
source /opt/ros/humble/setup.bash
ros2 pkg list | grep caret
# caret_analyze
# caret_analyze_cpp_impl
# caret_msgs
# ros2caret
```

このセクションにインストールされている CARET は、事前に測定されたトレース データを分析する機能を提供します。
解析手順は[tutorial](../tutorials/visualization.md)をご覧ください。
