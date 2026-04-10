# 実践的な構成例

前のセクションでは、構成で何を行うかを説明しました。このセクションでは、設定の流れを理解するために実際の例を説明します。

このセクションでは、Jupyter Notebook で `caret_demos` のアーキテクチャ ファイルを作成する方法を示します。ノード間およびノー​​ド内のデータ パスの定義についても説明します。以下の 3 つのステップについて説明します。

1. Jupyter Notebook に Architecture オブジェクトをロードする
2. ノード間のデータ パスを定義する
3. ノード内のデータ パスを定義する

この例で作成されるアーキテクチャ ファイルは [here](https://raw.githubusercontent.com/tier4/caret_demos/main/samples/end_to_end_sample/architecture.yaml) で提供されます。

## Jupyter Notebook に Architecture オブジェクトをロードする

[Load and save](./load_and_save.md) のセクションで説明されているように、記録されたデータからアーキテクチャ オブジェクトをロードします。

1. Jupyter Notebook (Jupyter Lab) を起動します。

   ```bash
   mkdir -p ~/ros2_ws/evaluate && cd ~/ros2_ws/evaluate

   source ~/ros2_caret_ws/install/setup.bash
   jupyter-lab
   ```

2. 以下のように記録データからアーキテクチャファイルを生成します

   ```python
   from caret_analyze import Architecture

   # Read description of application's architecture from recorded data
   #
   arch = Architecture('lttng', './e2e_sample')

   # Save description as an architecture file
   arch.export('architecture.yaml')

   # Check if the architecture file is created
   ! readlink -f ./architecture.yaml
   # /home/user/ros2_caret_ws/eval/architecture.yaml
   ```

## ノード間のデータ パスを定義する

[Define inter-node data path](./inter_node_data_path.md) のセクションで説明されているように、ロードされたアーキテクチャ オブジェクト上でノード間データ パスを定義します。

1. 以下のように yaml ベースのアーキテクチャ ファイルをロードします

   ```python
   from caret_analyze import Architecture, check_procedure
   arch = Architecture('yaml', './architecture.yaml')
   ```

2. パス内の送信元ノードと宛先ノードを選択します

   `arch.search_paths` パスの候補をすべて抽出します

   ```python
   paths = arch.search_paths(
   '/sensor_dummy_node', # source node
   '/actuator_dummy_node') # destination node
   ```

   対象のアプリケーションが大きく複雑な場合、`arch.search_paths` メソッドでは 1 分以上の時間がかかる場合があります。
   消費時間を短縮するには、ノードとトピックを無視し、検索の深さを指定します。詳細については、[Define inter-node data path](../configuration/inter_node_data_path.md)を参照してください。

3. 期待どおりのパスを確認します

   複数のパスの候補が表示されます。どの候補者がターゲットとして期待されているかを確認できます。次のコードは、ユーザーが確認する例です。

   ```python
   path = paths[0]
   path.summary.pprint()

   ---Output text as below---

   path:
     - message_context: null # for definition of node latency
       node: /sensor_dummy_node
     - topic: /topic1
     - message_context:
         publisher_topic_name: /topic2
         subscription_topic_name: /topic1
         type: callback_chain
       node: /filter_node
     - topic: /topic2
     - message_context: null
       node: /message_driven_node
     - topic: /topic3
     - message_context: null
       node: /timer_driven_node
     - topic: /topic4
     - message_context: null
       node: /actuator_dummy_node
   ```

4. 選択したパスに名前を付け、アーキテクチャ ファイルを更新します

   ```python
   arch.add_path('target', path)
   arch.export('./architecture.yaml', force=True)
   ```

   更新されたアーキテクチャ ファイルには、`target_path` という名前のパスが記述されています。

   ```yaml
   named_paths:
     - path_name: target_path
       node_chain:
         - node_name: /sensor_dummy_node
           publish_topic_name: /topic1
           subscribe_topic_name: UNDEFINED
         - node_name: /filter_node
           publish_topic_name: /topic2
           subscribe_topic_name: /topic1
         - node_name: /message_driven_node
           publish_topic_name: /topic3
           subscribe_topic_name: /topic2
         - node_name: /timer_driven_node
           publish_topic_name: /topic4
           subscribe_topic_name: /topic3
         - node_name: /actuator_dummy_node
           publish_topic_name: UNDEFINED
           subscribe_topic_name: /topic4
   ```

## ノード内のデータ パスを定義する

[Define intra-node data path](./intra_node_data_path.md) のセクションで説明されているように、ロードされたアーキテクチャ オブジェクトにノード内データ パスを定義します。

1. どのノードのレイテンシを設定する必要があるかを確認します

   `path.verify()` メソッドは、次の例に示すように、どのノードのレイテンシーを定義する必要があるかを示します。

   ```python
   from caret_analyze import Architecture

   arch = Architecture('yaml', './architecture.yaml')
   path = arch.get_path('target_path')
   path.verify()

   ---Output text as below---
   WARNING : 2021-12-20 19:14:03 | Detected "message_contest is None". Correct these node_path definitions.
   To see node definition and procedure,execute :
   >> check_procedure('yaml', '/path/to/yaml', arch, '/message_driven_node')
   message_context: null
   node: /message_driven_node
   publish_topic_name: /topic3
   subscribe_topic_name: /topic2

   WARNING : 2021-12-20 19:14:03 | Detected "message_contest is None". Correct these node_path definitions.
   To see node definition and procedure,execute :
   >> check_procedure('yaml', '/path/to/yaml', arch, '/timer_driven_node')
   message_context: null
   node: /timer_driven_node
   publish_topic_name: /topic4
   subscribe_topic_name: /topic3
   ```

   この例では、`path.verify()` は 2 つのノードの入力と出力の関係が未定義であることを示しています。
   - 入力 `/topic2` とノード `/message_driven_node` の出力 `/topic3`
   - 入力 `/topic3` とノード `/timer_driven_node` の出力 `/topic4`

   それらの関係は、アーキテクチャ ファイル内の対応する message_context 項目と明示的に示す必要があります。

2. 入力と出力の関係を定義する

   サンプルでは、​​message_contexts の項目を以下のように変更する必要があります。

   ```yaml
   # in /message_driven_node
   message_contexts:
     - context_type: use_latest_message # changed from 'UNDEFINED' to 'use_latest_message'
       subscription_topic_name: /topic2
       publisher_topic_name: /topic3
   ```

   ```yaml
   # in /timer_driven_node
     message_contexts:　
     - context_type: use_latest_message # changed from 'UNDEFINED' to 'use_latest_message'
       subscription_topic_name: /topic3
       publisher_topic_name: /topic4

   ```

3. ノード遅延が定義されているかどうかを確認します

   `path.verify()` は、パス内に未定義のノード遅延がないことを示します。

   ```python
   from caret_analyze import Architecture

   arch = Architecture('yaml', './architecture.yaml')
   path = arch.get_path('target_path')
   path.verify()
   ```

   `path.verify()` が `True` を返す場合、CARET はパスのレイテンシを計算できます。それ以外の場合、レイテンシを計算するための定義が不足しています。
