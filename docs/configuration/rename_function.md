# アーキテクチャ オブジェクト内のサブオブジェクトの名前を変更する方法

アーキテクチャ オブジェクトには、コールバック、ノード、パス、エグゼキュータ、トピックなどのいくつかのサブオブジェクトがあります。
CARET は、これらのサブオブジェクトを識別するために名前を割り当てます。これらの名前は、初期化トレースポイントで取得された識別子に由来します。ターゲット アプリケーションは、起動または更新のたびにサブオブジェクトに異なる識別子を割り当てる場合があります。これにより、ユーザーは既存のアーキテクチャ オブジェクトをそのまま再利用できなくなります。アーキテクチャ オブジェクトの再利用性を高めるために、CARET はこれらのサブオブジェクトの名前を変更する API を提供します。

次のコード スニペットはすべて、`Architecture('type', 'file_path')` メソッドがアーキテクチャ オブジェクトをロードした後に実行できます。
サブオブジェクトの名前が変更されたアーキテクチャ オブジェクトは、[the previous page](./load_and_save.md#save) で説明されているようにファイルに保存されます。

## `callback_name` の名前を変更します

`Architecture` クラスの `rename_callback` 関数を使用して、コールバック名を `src` から `dst` に更新できます。

```python
# arch is caret_analyze.architecture.architecture.Architecture-based object

arch.rename_callback('src', 'dst')
```

`src` であるアーキテクチャ オブジェクト内のすべての `callback_name` が `dst` に更新されます。

## `node_name` の名前を変更します

`Architecture` クラスの `rename_node` 関数を使用して、ノード名を `src` から `dst` に更新できます。

```python
# arch is caret_analyze.architecture.architecture.Architecture-based object

arch.rename_node('src', 'dst')
```

`src` であるアーキテクチャ オブジェクト内のすべての `node_name` が `dst` に更新されます。

## `path_name` の名前を変更します

`Architecture` クラスの `rename_path` 関数を使用して、パス名を `src` から `dst` に更新できます。

```python
# arch is caret_analyze.architecture.architecture.Architecture-based object

arch.rename_path('src', 'dst')
```

`src` であるアーキテクチャ オブジェクト内のすべての `path_name` が `dst` に更新されます。

## `executor_name` の名前を変更します

`Architecture` クラスの `rename_executor` 関数を使用して、エグゼキュータ名を `src` から `dst` に更新できます。

```python
# arch is caret_analyze.architecture.architecture.Architecture-based object

arch.rename_executor('src', 'dst')
```

`src` であるアーキテクチャ オブジェクト内のすべての `executor_name` が `dst` に更新されます。

## `topic_name` の名前を変更します

`Architecture` クラスの `rename_topic` 関数を使用して、トピック名を `src` から `dst` に更新できます。

```python
# arch is caret_analyze.architecture.architecture.Architecture-based object

arch.rename_topic('src', 'dst')
```

`src` であるアーキテクチャ オブジェクト内のすべての `topic_name` が `dst` に更新されます。
