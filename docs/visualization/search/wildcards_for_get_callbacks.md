# get_callbacks() のワイルドカード

`get_callbacks()` 関数は、引数として指定された文字列に名前が一致するコールバックのリストを取得します。
一致するコールバックがない場合、この関数はコールバックの候補を通知することがあります。
`get_callbacks()` は、「\*」や「?」などの UNIX ベースのワイルドカードをサポートします。

## 使用法

```python
from caret_analyze import Architecture, Application, Lttng

callback1 = app.get_callbacks('/timer_driven_node/callback_0')
callback2 = app.get_callbacks('/timer_driven_node/callback_?')
callback3 = app.get_callbacks('/timer_driven_node/*')
```
