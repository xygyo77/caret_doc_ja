# オリジナルのROSとの違い

<prettier-ignore-start>
!!! note
    このセクションでは、CARET の v0.2 実装と ROS 2 Gaoptic の実装の違いについて説明します。実装の観点からは最新の説明ではありませんが、設計の観点からの違いを理解するには十分です。
<prettier-ignore-end>

## CARET v0.2 vs ROS2 Galactic

[caret.repos](https://github.com/tier4/caret/blob/main/caret.repos) には次のリポジトリが含まれています

- <https://github.com/ros2/rcl.git>
- <https://github.com/tier4/rclcpp/tree/galactic_tracepoint_added>
- <https://github.com/tier4/ros2_tracing/tree/galactic_tracepoint_added>

これらはそれぞれ、元の ROS 2 リポジトリからクローン化されます。オリジナルとの相違点について説明します。

### rcl

ソースコードは変更されていません。
組み込みトレース ポイントを有効にするために再構築が必要なため、このパッケージは複製されます。

### rclcpp

このクローン作成は、LD_PRELOAD による関数フックでは追加できないトレースポイントを追加するためのものです。

こちらも参照

- [Tracepoints](./index.md)

ros2_tracingのインクルードディレクトリを追加する必要があります。

<prettier-ignore-start>
!!! info
    ros2_tracing のインクルード ファイルを rclcpp に追加する理由。
    LD_PRELOAD を使用すると、実行開始直後にカスタム共有ライブラリを優先的にロードできます。
    一方、上記のようにヘッダーにトレースポイントを追加するには、ビルド時のヘッダー検索中に、トレースポイントが追加されたバージョンのヘッダーを最初にロードする必要があります。
    この優先順位が期待どおりであることを確認するために、インクルード ファイルが追加されます。
    トレースポイントを ros2 メインフレームにマージする場合、ros2_tracing インクルード ファイルを rclcpp に追加する必要はありません。
<prettier-ignore-end>

### ros2_トレーシング

このクローン作成は、rclcpp に追加されたトレースポイントを定義するためのものです。

## v0.3 対 Humble

v0.3 では、Galactic版 CARET で使用されていたトレース ポイントが移植されました。
いくつかのトレースポイントが Humble に追加されましたが、現在 CARET では使用されていません。
これらのトレースポイントは将来のバージョンでサポートされる予定です。
