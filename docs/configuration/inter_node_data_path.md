# ノード間のデータパスを定義する方法

アーキテクチャ オブジェクトが CTF ベースの記録データのセットからロードされた直後は、レイテンシー定義セクションは空です。ターゲット パス上のデータ フローを観察したい場合は、ターゲット パスをアーキテクチャ オブジェクトに追加する必要があります。パスは複数のノードとトピックの組み合わせであるため、それらの名前をリストするのは面倒な場合があります。このような負担を軽減するために、CARET は目的のパスを検索する機能を提供します。ターゲットのパスは、Python API を介してアーキテクチャ オブジェクトに追加されます。

## ターゲットパスを検索して追加するための基本的な使用法

ノードとトピックを名前でリストするのは面倒です。CARET は、観察したい候補を検索するための便利なメソッド `arch.search_paths` を提供します。

以下のサンプルコードは、`arch.search_paths` メソッドの使用方法を示しています。

```python
# Architecture object is loaded to variable of arch

paths = arch.search_paths('source_node',
                          'destination_node')

type(paths) # list of multiple paths
paths[0].summary.pprint() # shows nodes and topics in paths[0]
```

サンプルでは、​​`paths` は、`source_node` と `destination_node` の間のすべての可能なパスを含むリストであり、タイプは `PathStructValue` です。`paths[0].summary.pprint()` の出力に満足している場合は、以下のように `paths[0]` を `arch` オブジェクトに追加する必要があります。

```python
arch.add_path('target_path', paths[0])

arch.export('new_architecture_with_path.yaml')
```

上記のサンプルでは、​​`paths[0]` は `target_path` という名前で `arch` オブジェクトに登録されています。`arch` オブジェクトは、再利用するために新しいアーキテクチャ ファイルにエクスポートされます。

`paths[0]` オブジェクトを `new_architecture_with_path.yaml` ファイルで復元したい場合は、`arch.get_path()` メソッドが役に立ちます。

```python
arch = Architecture('yaml', 'new_architecture_with_path.yaml')

path = arch.get_path('target_path') # path object is same as paths[0] in the previous sample
```

### 効率的なターゲットパス検索

上で説明したように、`Architecture.search_paths()` は複数のパスのリストを返します。
アプリケーションに多数のノードがあり、ソース ノードと宛先ノード間の距離が長い場合、リスト サイズが大きすぎてターゲット パスを見つけることができません。最悪の場合、`Architecture.search_paths()` は検索を続け、数時間が経過しても `paths` 変数を返しません。

`Architecture.search_paths()` メソッドは、以下に示すように、可能なパスを絞り込むための 4 つのオプションを提供します。

1. 可変長引数としての **追加ノード**
2. `max_node_depth` を使用して特定のノード間の **最大ノード数を制限**
3. 特定のノードを含むパスを除外する **ノード フィルター**
4. 特定のトピックを含むパスを除外する **コミュニケーション フィルター**

つまり、`Architecture.search_paths` は次のように定義されます。

```python
search_paths(
    *node_names: 'str',
    max_node_depth: 'Optional[int]' = None,
    node_filter: 'Optional[Callable[[str], bool]]' = None,
    communication_filter: 'Optional[Callable[[str], bool]]' = None
) -> 'List[PathStructValue]'
```

次のサブセクションでは、それらの役割と使用法について詳しく説明します。Autoware のパス検索でこれらのオプションを使用する例は、[add_path_to_architecture.py](https://github.com/tier4/caret_report/blob/main/report/analyze_path/add_path_to_architecture.py) にあります。

#### 追加のノード

前の例では、`Architecture.search_paths()` には 2 つの引数 `source_node` と `destination_node` がありました。ただし、`Architecture.search_paths()` に与えられるノードの数は可変であり、常に 2 つであるとは限りません。以下のように `Architecture.search_paths()` に他のノードを追加すると、指定されたすべてのノードを通過する複数のパスを含むリストが取得されます。

```python
# Architecture object is loaded to variable of arch

paths = arch.search_paths('source_node',
                          'intermediate_node_1',
                          'intermediate_node_2',
                          'destination_node')
```

`paths`は、`source_node`、`intermediate_node_1`、`intermediate_node_2`、および `destination_node` を渡す複数のパスを含むリストです。別のノードを通過することは許可されていますが、選択されたすべてのノードが順番に通過されます。

#### 最大ノード数の制限

`max_node_depth` 引数を指定しない場合、`Architecture.search_paths()` は可能な限りすべてのパスをスキャンします。`max_node_depth` は、指定されたノード間の最大数を意味します。この引数により候補パスの数が抑制されます。

この引数は、`Architecture.search_paths()` に多くの時間を浪費する場合に役立ちます。

使い方は以下の通りです。これは、候補をフィルタリングするための別のアプローチと併用できます。

```python
# Architecture object is loaded to variable of arch

paths = arch.search_paths('source_node',
                          'intermediate_node_1',
                          'destination_node',
                          max_node_depth=10)

```

`max_node_depth` は、送信元と宛先の間の最大ノード数を常に制限するとは限りません。上記のように `arch.search_paths` に 3 つのノードを与える場合、`max_node_depth` は `source_node` と `destination_node` の間の最大ノード数を制限しません。この例では、`max_node_depth` は、`source_node` と `intermediate_node_1` の間のノード数と、`intermediate_node_1` と `destination_node` の間のノード数を制限します。

#### ノードとトピックのフィルター

ノードフィルタは通信フィルタと似ているため、ここではまとめて説明します。

ノード フィルターと通信フィルターを使用すると、`Architecture.search_paths()` は、選択したノードまたはトピックを含むパスを除外します。正規表現をサポートしています。

次のサンプルコードは使用方法を示しています。

```python
import re

# name list of nodes to be excluded
node_filters = [
    re.compile(r'/_ros2cli_/*'),
    re.compile(r'/launch_ros_*'),
]

# name list of topics to be excluded
comm_filters = [
    re.compile(r'/tf/*'),
]
def comm_filter(topic_name: str) -> bool:
    can_pass = True
    for comm_filter in comm_filters:
        can_pass &= not bool(comm_filter.search(topic_name))
    return can_pass

def node_filter(node_name: str) -> bool:
    can_pass = True
    for node_filter in node_filters:
        can_pass &= not bool(node_filter.search(node_name))
    return can_pass

paths = arch.search_paths(
    '/start_node',
    '/intermediate_node'
    '/end_node',
    max_node_depth=30,
    node_filter = node_filter,
    communication_filter = comm_filter)
```

### パスの結合

`Architecture.combine_path()` は、`Architecture.search_paths()` で見つかった 2 つのパスを結合します。
短いパスを探索して組み合わせを繰り返すことで、目的のパスを得ることができます。「分割統治」方法に従って長いパスを直接検索するよりも効率的な場合があります。

`Architecture.combine_path()`の使い方は以下の通りです。

```python
paths_1 = arch.search_paths('source_node',
                            'intermediate_node')
paths_2 = arch.search_paths('intermediate_node',
                            'destination_node')
target_path = arch.combine_path(paths_1[0], paths_2[0])

arch.add_path('combined_path_name', target_path)
arch.export('new_architecture.yaml')
```

結合できないペアの場合は例外が発生します。

### 最初/最後のコールバックを考慮する

CARET では、パスは `[node_name]-[topic_name]-... -[topic_name]-[node_name]` (for more information in [Path](../design/event_and_latency_definitions/path.md#Path)) として定義されます。
デフォルト構成では、パス分析には、上記のパスの最初のノードまたは最後のノードでのコールバック処理時間は含まれません。次の 2 つの処理時間は、デフォルトではパス分析に含まれません。

- 最初のノードでの処理時間。`callback_start` から `rclcpp_publish` または `rclcpp_intra_publish` まで
- 最後のノードでの処理時間。`callback_start` から `callback_end` まで

これらの処理時間は、次のオプションを使用して評価されます。

- `Path.include_first_callback`
  - デフォルト: `False`
  - `True`の場合、最初のノードでの処理時間もパス解析の対象となります。最初のノードの callback_start は、タイムスタンプがパブリッシュに最も近く、スレッド ID (tid) がパブリッシュと同じであるトレース データのコールバックスタートです。ノードに複数のコールバックがあり、それらのいずれかがパブリッシュ前に実行される場合、最初のノードの callback_start のコールバック オブジェクトは異なる可能性があることに注意してください。
- `Path.include_last_callback`
  - デフォルト: `False`
  - `True`の場合、最終ノードでの処理時間もパス解析の対象となります。

`Path.include_first_callback/include_last_callback`の使い方は以下の通りです。

```python
app = Application(arch, lttng)

path_name = 'target_path'
target_path = app.get_path(path_name)

target_path.include_first_callback = True     # Include first callback in path analysis.
target_path.include_last_callback = True      # Include last callback in path analysis.
```
