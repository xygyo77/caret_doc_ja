# アーキテクチャファイル

アーキテクチャ ファイルは、ターゲット アプリケーションの構造を記述する YAML ベースのファイルです。
以下の情報が含まれます。

- 測定するデータパスの定義
・測定対象となるソフトウェアの構造に関する情報
  - 執行者情報
  - ノード情報 (例: ノードのレイテンシー定義)

## ファイル形式

アーキテクチャファイルのサンプルは以下の通りです。

|キー |タイプ |必須？|自動生成しますか？<br> (設定方法) |注記 / 説明 |
|----------------------------------------------- |------------ |------------------------------------------ |------------------------------------------ |-------------------------------------------------- |
|named_paths |List |はい |はい |評価するパス定義。|
|&emsp;path_name |String |はい |いいえ (Python-API 経由で編集) ||
|&emsp;node_chain |List |はい |いいえ (Python-API 経由で編集) ||
|&emsp;&emsp;node_name |String |はい |いいえ (Python-API 経由で編集) ||
|&emsp;&emsp;publish_topic_name |String |ノードがパスの終端ではない場合は必須です。|いいえ (Python-API 経由で編集) ||
|&emsp;&emsp;subscribe_topic_name |String |ノードがパスの始点ではない場合は必須です。|いいえ (Python-API 経由で編集) ||
|&emsp;&emsp;publisher_construction_order |int |いいえ |いいえ (Python-API 経由で編集) |存在しない場合は、デフォルト値としてゼロが使用されます。|
|&emsp;&emsp;subscription_construction_order |int |いいえ |いいえ (Python-API 経由で編集) |存在しない場合は、デフォルト値としてゼロが使用されます。|
|executors |List |はい |はい ||
|&emsp;node_chain |String |はい |はい |シングルスレッドエグゼキュータ / マルチスレッドエグゼキュータ |
|&emsp;executor_name |String |はい |はい ||
|&emsp;callback_group_names |List(String) |はい |はい ||
|nodes |List |はい |はい ||
|&emsp;node_name |String |はい |はい ||
|&emsp;callback_groups |List |はい |はい ||
|&emsp;&emsp;callback_group_type |String |はい |はい |相互排他的 / 再入可能 |
|&emsp;&emsp;callback_group_name |String |はい |はい ||
|&emsp;callbacks |List |はい |はい ||
|&emsp;&emsp;callback_type |String |はい |はい |タイマーコールバック / サブスクリプションコールバック |
|&emsp;&emsp;symbol |String |はい |はい |コールバック関数のシンボル。|
|&emsp;&emsp;period_ns |int |timer_callback の場合にのみ必要です。|はい ||
|&emsp;&emsp;topic_name |String |subscription_callback の場合にのみ必須です。|はい ||
|&emsp;&emsp;construction_order |int |いいえ |はい |存在しない場合は、デフォルト値としてゼロが使用されます。|
|&emsp;variable_passings |List |いいえ |はい ||
|&emsp;&emsp;callback_name_write |String |いいえ |いいえ (アーキテクチャ ファイルを編集) |デフォルト値 = 未定義 |
|&emsp;&emsp;callback_name_read |String |いいえ |いいえ (アーキテクチャ ファイルを編集) |デフォルト値 = 未定義 |
|&emsp;publishes |List |いいえ |はい ||
|&emsp;&emsp;topic_name |String |いいえ |はい ||
|&emsp;&emsp;callback_names                  |List(String) |いいえ |いいえ (アーキテクチャ ファイルを編集) |callbacks which publish the topic.|
|&emsp;&emsp;construction_order |int |いいえ |はい |存在しない場合は、デフォルト値としてゼロが使用されます。|
|&emsp;subscribes |List |いいえ |はい ||
|&emsp;&emsp;topic_name |String |いいえ |はい ||
|&emsp;&emsp;callback_name |String |いいえ |はい ||
|&emsp;&emsp;construction_order |int |いいえ |はい |存在しない場合は、デフォルト値としてゼロが使用されます。|
|&emsp;message_contexts |List |いいえ |はい |ノードのレイテンシを定義するフィールド |
|&emsp;&emsp;context_type |String |いいえ |いいえ (アーキテクチャ ファイルを編集) |デフォルト値 = 未定義 |
|&emsp;&emsp;subscription_topic_name |String |いいえ |はい ||
|&emsp;&emsp;publisher_topic_name |String |いいえ |はい ||
|&emsp;&emsp;publisher_construction_order |int |いいえ |はい |存在しない場合は、デフォルト値としてゼロが使用されます。|
|&emsp;&emsp;subscription_construction_order |int |いいえ |はい |存在しない場合は、デフォルト値としてゼロが使用されます。|

## サンプル

アーキテクチャファイルのサンプルは以下の通りです。

```yaml
named_paths:
  - path_name: target_path
    node_chain:
      - node_name: /ping_node
        publish_topic_name: /chatter
        subscribe_topic_name: UNDEFINED
      - node_name: /pong_node
        publish_topic_name: UNDEFINED
        subscribe_topic_name: /chatter
        subscription_construction_order: 1
executors:
  - executor_type: single_threaded_executor
    executor_name: executor_0
    callback_group_names:
      - /ping_node/callback_group_0
      - /pong_node/callback_group_0
nodes:
  - node_name: /ping_node
    callback_groups:
      - callback_group_type: mutually_exclusive
        callback_group_name: /ping_node/callback_group_0
        callback_names:
          - /ping_node/callback_0
    callbacks:
      - callback_name: subscription_callback_0
        type: subscription_callback
        topic_name: /topic3
        symbol: Node::{lambda()}
      - callback_name: timer_callback_0
        type: timer_callback
        period_ns: 100000000
        symbol: Node::{lambda()}
      - callback_name: timer_callback_0
        type: timer_callback
        period_ns: 100000000
        symbol: Node::{lambda()}
        construction_order: 1
    variable_passings:
      - callback_name_write: subscription_callback_0
        callback_name_read: timer_callback_0
    publishes:
      - topic_name: /ping
        callback_names:
          - timer_callback_0
    subscribes:
      - topic_name: /pong
        callback_name: timer_callback_0
    message_contexts:
      - context_type: use_latest_message
        subscription_topic_name: /pong
        publisher_topic_name: /ping
```

## コールバック識別

ユーザーがコールバック関数を識別できるように名前を付けると便利です。ただし、ROS 2 のコンテキストでは、アドレスのみがコールバックに与えられます。

アドレスはアプリケーションを起動するたびに変わります。
このため、コールバックのパフォーマンスを評価する際に、アドレスごとにコールバックを処理することが困難になります。
たとえば、起動ごとに特定のコールバックの実行時間を比較したい場合は、アドレスを見つけてターゲット コールバックを選択する必要があります。

CARET はユーザーがコールバックに名前を付けるのに役立ちますが、上で説明した理由により、そのアドレスには直接関連付けられません。

この問題を解決するために、CARET は、以下のデータの組み合わせを使用して、名前とコールバックのアドレスを関連付けます。

- `node_name`
- `callback_type`
- `period_ns` / `topic_name`
- `symbol`
- `construction_order`

この情報を使用して `callback_name` とコールバック アドレスを照合することで、
各 `callback_name` は、コールバック アドレスを意識せずに、常に同一のコールバックを参照します。
