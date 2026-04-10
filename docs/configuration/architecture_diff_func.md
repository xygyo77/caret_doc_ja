# アーキテクチャの違いを取得する方法

アーキテクチャオブジェクトは、ターゲットアプリケーションの構造を持ちます。構造を調べたいときに便利です。場合によっては、対象アプリケーションの現在のバージョンと以前のバージョンとの違いを確認したいことがあります。違いにより、どのエグゼキューター、ノード、コールバック、またはトピックが更新されたかがわかります。CARET は、2 つのアーキテクチャ オブジェクト間の差異を取得する機能を果たします。以下、この関数を`diff`関数と呼びます。

`diff` 関数を使用すると、2 つのアーキテクチャ オブジェクト間の違いを見つけることができます。具体的には、`diff` 関数は、ノード、公開トピック、サブスクライブされたトピックなど、いずれかのアーキテクチャにのみ存在するデータを検索できます。
いくつかの `diff` 関数があり、アーキテクチャ全体を比較する関数とアーキテクチャ内のノードを比較する関数に分けることができます。

`diff` 関数については、次のセクションで説明します。`diff` 関数を使用する前に、次のスクリプトに示すように、2 つのアーキテクチャ オブジェクトが事前にメモリにロードされます。

```python
from caret_analyze import Architecture
left_arch = Architecture('yaml', 'old_architecture.yaml')
right_arch = Architecture('yaml', 'new_architecture.yaml')

```

## アーキテクチャを比較する方法

関数 `diff_node_names()` および `diff_topic_names()` は、2 つのオブジェクトの一方にのみ存在するノード名とトピック名をそれぞれ検索することにより、2 つのアーキテクチャ オブジェクトを比較します。
`diff_node_names()` は、ターゲット アプリケーションの新しいバージョンで追加または削除されたノードを示します。`diff_topic_names()` には、追加または削除されたトピックが表示されます。

### diff_node_names()

`diff_node_names()` 関数は、指定された 2 つのアーキテクチャ オブジェクトのうちの 1 つにのみ名前が表示されるノードの名前を返します。

```python
# sample_1

# get node names that are only in left_arch and right_arch respectively
left_only_node_names, right_only_node_names = Architecture.diff_node_names(left_arch, right_arch)

# display differences
print(left_only_node_names)
print(right_only_node_names)

```

`diff_node_names()` には 2 つのアーキテクチャが与えられています。異なるノードがある場合は、ノード名を含む 2 つのタプルが返されます。それらが同じノードを持っている場合、`diff_node_names()` は 2 つの空のタプルを返します。

### diff_topic_names()

`diff_topic_names()` 関数は、指定された 2 つのアーキテクチャ オブジェクトのうちの 1 つにのみ名前が表示されるトピックの名前を返します。

```python
# sample_2

# get topic names that are only in left_arch and right_arch respectively
left_only_topics, right_only_topics = Architecture.diff_topic_names(left_arch, right_arch)

# display differences
print(left_only_topics)
print(right_only_topics)

```

`diff_topic_names()` には 2 つのアーキテクチャが与えられています。異なるトピックがある場合は、トピック名を含む 2 つのタプルが返されます。それらが同じトピックを持っている場合、`diff_topic_names()` は 2 つの空のタプルを返します。

<prettier-ignore-start>
!!!info
      アーキテクチャ オブジェクトには、Executor や Callback などの他の要素があります。ただし、Executor や Callback の差分を取得する関数はまだ実装されていません。必要に応じて開発者にお問い合わせください。
<prettier-ignore-end>

## アーキテクチャ内のノードを比較する方法

`diff_node_pubs()` 関数と `diff_node_subs()` 関数は、2 つのノードのうちの 1 つにのみ存在する公開トピックと購読トピックをそれぞれ検索します。
`diff_node_pubs()` は、ターゲット ノードの新しいバージョンで追加または削除された公開トピックを示します。`diff_node_subs()` には、サブスクライブされたトピックが追加または削除されたことが表示されます。

### diff_node_pubs()

`diff_node_pubs()` 関数は、2 つのノードの一方にのみ名前が表示される公開トピックの名前を返します。

```python
# sample_3

left_node = left_arch.get_node('node1')
right_node = right_arch.get_node('node1')

# get publish topic names that are only in left_node and right_node respectively
left_only_pub_topics, right_only_pub_topics = Architecture.diff_node_pubs(left_node, right_node)

# display differences
print(left_only_pub_topics)
print(right_only_pub_topics)

```

タイプが `NodeStructValue` である 2 つのノードが `diff_node_pubs()` に割り当てられます。異なる公開トピックがある場合は、トピック名を含む 2 つのタプルが返されます。それらが同じトピックを持っている場合、`diff_node_pubs()` は 2 つの空のタプルを返します。

### diff_node_subs()

`diff_node_subs()` 関数は、2 つのノードのうちの 1 つにのみ名前が表示されるサブスクライブされたトピックの名前を返します。

```python
# sample_4

left_node = left_arch.get_node('node1')
right_node = right_arch.get_node('node1')

# get subscribe topic names that are only in left_node and right_node respectively
left_only_sub_topics, right_only_sub_topics = Architecture.diff_node_subs(left_node, right_node)

# display differences
print(left_only_sub_topics)
print(right_only_sub_topics)

```

タイプが `NodeStructValue` である 2 つのノードが `diff_node_subs()` に割り当てられます。サブスクライブされたトピックが異なる場合は、トピック名を含む 2 つのタプルが返されます。それらが同じトピックを持っている場合、`diff_node_subs()` は 2 つの空のタプルを返します。
