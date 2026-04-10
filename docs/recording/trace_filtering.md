# トレースフィルタリング

## トレースのフィルタリング

CARET は、特定のノードとトピックを除外するトレース フィルター機能を提供します。Autoware のような大規模なアプリケーションを recording する場合、記録すべきデータが多すぎるためにトレース データが破棄される可能性があり、記録されたトレース データを検証/分析するときに警告が表示されます ([validating](./validating.md#tracer-discarded) を参照)。トレースフィルターを適用すると、`/tf` などの無関係なイベントが無視され、記録されるデータのサイズが減少します。

## トレースフィルター設定

- トレースフィルタの設定は、以下の環境変数を設定することで実行されます。
  - `CARET_SELECT_NODES` : 記録するノード名
  - `CARET_IGNORE_NODES` : 無視するノード名
  - `CARET_SELECT_TOPICS` : 記録するトピック名
  - `CARET_IGNORE_TOPICS` : 無視するトピック名
- 両方が使用されている場合、「SELECT」設定は「IGNORE」設定をオーバーライドします
- コロン「`:`」は、複数のノード/トピックを設定するために使用されます
- 正規表現がサポートされています
- これらの変数は、実行中のターゲット アプリケーションと同じ端末で設定する必要があります。
- ほとんどの場合、`/rviz`、`/clock` トピック、および `/parameter_events` トピックに関連するノードはアプリケーションの分析には不要です。これらのノード/トピックは無視することをお勧めします

以下に設定例を示します

```sh
export CARET_IGNORE_NODES="/rviz*"
export CARET_IGNORE_TOPICS="/clock:/parameter_events"
```

## トレースフィルタ設定ファイル

以下のようなトレースフィルタ設定ファイルを用意しておくと便利です。

```sh
# caret_topic_filter.bash
#!/bin/bash

export CARET_IGNORE_NODES=\
"\
/rviz*:\
/caret_trace_*:\
"

export CARET_IGNORE_TOPICS=\
"\
/clock:\
/parameter_events:\
"

# if you want to select nodes or topics,
# please remove comment out of the followings.
# export CARET_SELECT_NODES=\
# "\
# /rviz*:\
# /caret_trace_*:\
# "

# export CARET_SELECT_TOPICS=\
# "\
# /clock:\
# /parameter_events:\
# "
```

<prettier-ignore-start>
!!! Info
        トレースポイント情報からノードが特定できない場合は、フィルタを適用せずにトレースを収集します。
<prettier-ignore-end>
