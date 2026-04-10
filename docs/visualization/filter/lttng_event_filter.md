# LTTng イベントフィルタ

CARET は、数分間記録されたデータを分析できます。CARET を使用して大規模なデータを分析する場合、分析に消費されるメモリと時間の両方が重要な問題になります。

不要なデータをロードしないように、CARETには選択したデータをロード対象から除外する`LTTngEventFilter`が用意されています。

`LTTngEventFilter`には以下のメソッドがあります。

- `init_pass_filter`
- `duration_filter`
- `strip_filter`

## `init_pass_filter`

`init_pass_filter` メソッドでは、ランタイム トレースポイントによって記録されたイベントはメモリにロードされません。

```python
LttngEventFilter.init_pass_filter()
```

## `duration_filter`

`duration_filter`メソッドを使用すると、記録されたデータの時間範囲をターゲットにしてデータをクロップできます。

```python
LttngEventFilter.duration_filter(duration_s: float, offset_s: float)
```

`duration_filter` メソッドには以下の 2 つの引数があります。

- `duration_s` はターゲット時間範囲の継続時間です
- `offset_s` はターゲット時間範囲のポイントです

## `strip_filter`

`strip_filter` メソッドを使用すると、`duration_filter` だけでなく、記録されたデータの時間範囲をターゲットにしてデータをクロップすることができます。`strip_filter` には `duration_filter` とは異なる引数があります。

```python
LttngEventFilter.strip_filter(lsplit_s: Optional[float], rsplit_s: Optional[float])
```

`strip_filter` メソッドには次の 2 つのオプションの引数があります。どちらかまたは両方を省略した場合、オプションの引数にはデフォルト値「0」が与えられます。

- `lstrip_s` はトリミング範囲の開始時刻です。
- `rstrip_s` はトリミング範囲の終点です

## サンプルコード

`duration_filter`を使用したサンプルコードを以下に示します。

```python
from caret_analyze import Lttng, LttngEventFilter

lttng = Lttng('/path/to/ctf', event_filters=[
  LttngEventFilter.duration_filter(10, 5)
]) # Filtering for 10 from 5 seconds
```

別のフィルターを追加する場合は、`event_filters` リストに追加します。
