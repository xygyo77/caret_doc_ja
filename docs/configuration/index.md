＃ 構成

＃＃ 導入

構成は、ユーザーが視覚化の対象となるデータ パスを CARET に指示するフェーズです。

CARET は、大規模なアプリケーションが実行されている場合でも、recording の膨大な数のイベントを処理できます。大規模なアプリケーションには多数のデータ パスがある可能性がありますが、ほとんどのユーザーはすべてのデータ パスを観察することを望んでいないはずです。CARET がすべての可能なデータ パスの分析結果を親切に表示すると、ユーザーは大量の結果を処理するのに圧倒されて疲れ果ててしまうでしょう。

効率的な分析を実現するために、CARET はオンデマンドで分析結果を表示するように設計されています。CARET は、ユーザーの関心を満たすターゲット データ パスを選択するユーザー機能を提供します。

CARET は、ターゲット パスの定義に加えて、ユーザーが視覚化を使用してアプリケーションを分析する前にノード レイテンシを定義するように求めます。

この章の残りの部分では、次の 2 種類のセクションについて説明します。

- 構成の詳細な背景
- 必要な構成を準備するための基本的な手順

詳細については、以下のセクションに記載されています。

- [**Background of configuration**](./background.md) セクションでは、構成フェーズの詳細な背景について説明します
- [**How to load and save**](./load_and_save.md) セクションでは、設定をロードおよび保存する方法について説明します。
- [**How to define inter-node data path**](./inter_node_data_path.md) セクションでは、`architecture.search_paths()` の使用方法について説明します。
- [**How to define intra-node data path**](./intra_node_data_path.md) は `message_context` が何であるかを教えてくれます。これは他のトピックよりも高度なトピックです
- [**How to rename sub-objects**](./rename_function.md) セクションでは、`rename_XXX()` の使用方法について説明します。
- [**How to get difference of two architectures**](./architecture_diff_func.md) は `diff_XXX_YYY()` 関数の使用方法を説明します
- [**Practical example with caret_demos**](./practical_example.md) では、[`caret_demos`](https://github.com/tier4/caret_demos) の構成プロセスをデモンストレーションします
  **アプリケーション構造の視覚化**は、アーキテクチャ オブジェクトの別の使用法を示す付録として用意されます。CARET は、パフォーマンス分析ツールでありながら、対象のアプリケーションの構造を表示できます。この付録も近々公開される予定です。
