# アーキテクチャオブジェクトをロードおよび保存する方法

構成の最初のステップは、CTF ベースの記録データのセットからアーキテクチャ オブジェクトをメモリにロードすることです。次のセクションで説明するように、アーキテクチャ オブジェクトを更新できます。更新が完了したら、「アーキテクチャ ファイル」と呼ばれる yaml ベースのファイルに保存して、更新されたオブジェクトを再利用できます。

アーキテクチャ ファイルには、対象となるアプリケーションの構造が含まれます。[`dear_ros_node_viewer`](https://github.com/takeshi-iwanari/dear_ros_node_viewer) は、アーキテクチャ ファイルを使用してアプリケーションの構造を理解するのに役立ちます。

## Python API

CARET は、アーキテクチャ オブジェクトの読み込みと保存を行うための Python ベースの API を提供します。

次のコード スニペットはすべて、`source /path/to/ros2_caret_ws/install/setup.bash` で環境変数をロードした後に実行できます。

### CTF ベースの記録データのセットからロード

`Architecture` コンストラクターを使用してアーキテクチャ オブジェクトをロードできます。

```python
from caret_analyze import Architecture

arch = Architecture('lttng', '/path/to/ctf-based_recorded_data')
```

「`arch`」という名前の `caret_analyze.architecture.Architecture` ベースのオブジェクトが見つかります。

マルチホストシステムの記録データをロードするには、記録データのリストを Architecture オブジェクトに渡すことができます。

```python
arch = Architecture('lttng', ['/path/to/host0/data', '/path/to/host1/data'])
```

CTF ベースの記録データからアーキテクチャ オブジェクトを読み込むのは、時間のかかる作業になりがちです。

### YAML ベースのアーキテクチャ ファイルからロードする

前述したように、CARET は、再利用可能にするために、アーキテクチャ オブジェクトを YAML ベースのアーキテクチャ ファイルに保存する機能を果たします。ロード時間を節約し、オブジェクトの更新を保持できます。`Architecture` コンストラクターの第一引数の '`lttng`' を '`yaml`' に置き換えるだけで、YAML ベースのファイルからロードできます。

```python
from caret_analyze import Architecture

arch = Architecture('yaml', '/path/to/architecture.yaml')
```

対象となるアプリケーションの構造が変更されない限り、再利用性を考慮して YAML ベースのファイルを使用することをお勧めします。

### 保存

CARET は、次のようにアーキテクチャ オブジェクトを保存するための `Architecture.export` メソッドを提供します。

```python
# arch is caret_analyze.architecture.architecture.Architecture-based object


arch.export('/path/to/destination/architecture.yaml')

! readlink -f /path/to/destination//architecture.yaml
# /path/to/destination/architecture.yaml

```

`arch.export()`の引数は文字列型で、`arch`オブジェクトを格納するファイルパスを意味します。このサンプルでは、​​宛先パスが書き込み可能であるか、同じ名前の別のファイルが存在する場合、`architecture.yaml` が `/path/to/destination` ディレクトリに作成されます。

`arch.export()` には 2 番目の引数 `force` があり、`arch` オブジェクトを既存のファイルに上書きできます。以下のサンプルは上書きする方法を示しています。

```python

arch.export('/path/to/destination/architecture.yaml', force=True)

! readlink -f /path/to/destination//architecture.yaml
# /path/to/destination/architecture.yaml
```

`force=True` オプションは、既存のアーキテクチャ オブジェクトを消去します。

## CLI

### CLI 経由でアーキテクチャ ファイルを作成する

上記で紹介した機能を利用すると、アーキテクチャオブジェクトを含むYAMLベースのファイルを作成できます。CARET は、CLI を使用して作成することもできます。`create_architecture_file` コマンドがその役割を果たします。

以下のサンプルコードは、`create_architecture_file` コマンドの使用方法を示しています。

```bash
source /path/to/ros2_caret_ws/install/setup.bash

ros2 caret create_architecture_file /path/to/ctf-based_recorded_data -o /path/to/destination/architecture.yaml

readlink -f /path/to/destination/architecture.yaml
# /path/to/destination/architecture.yaml
```

マルチホストシステムのYAMLベースのファイルを作成するには、記録されたデータのリストを`create_architecture_file`コマンドに渡すことができます。

```bash
ros2 caret create_architecture_file /path/to/host0/data /path/to/host1/data -o /path/to/destination/architecture.yaml
```
