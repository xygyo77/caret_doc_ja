「初期化トレースポイント」は、主にNode、Executor、CallbackなどのROS構成オブジェクトの作成時に発生するトレースポイントです。
一部のトレースポイントは同じアドレスを共有します (node_handle とコールバック アドレスなど)。
これらのアドレスをバインドすることにより、CARET は各トレース ポイント関係の構造を構築します。

### 各初期化トレース ポイントの関係

単一ノードに関する各トレースポイントの関係は次のようになります。

```mermaid
erDiagram
 rcl_init{
 address context_handle
 }

 caret_init{
 int64_t clock_offset
 string distribution
 }

 rcl_node_init{
 address node_handle
 address rmw_handle
 string node_name
 string node_namespace
 }

 rcl_publisher_init{
 address publisher_handle
 address node_handle
 address rmw_publisher_handle
 string topic_name
 size_t queue_depth
 }

 rcl_subscription_init{
 address subscription_handle
 address node_handle
 address rmw_subscription_handle
 string topic_name
 size_t queue_depth
 }

 rclcpp_subscription_init{
 address subscription_handle
 address subscription
 }

 rclcpp_subscription_callback_added{
 address subscription
 address callback
 }

 rcl_service_init{
 address service_handle
 address node_handle
 address rmw_service_handle
 string service_name
 }

 rclcpp_service_callback_added{
 address service_hadle
 address callback
 }

 rcl_timer_init{
 address timer_handle
 int64_t period
 }

 rclcpp_timer_callback_added{
 address timer_handle
 address callback
 }

 rclcpp_timer_link_node{
 address timer_handle
 address node_handle
 }

 rclcpp_callback_register{
 address callback
 string function_symbol
 }

 rclcpp_buffer_to_ipb{
 address buffer
 address ipb
 }

 rclcpp_ipb_to_subscription{
 address ipb
 address subscription
 }

 rclcpp_construct_ring_buffer{
 address buffer
 uint64_t capacity
 }

 rmw_implementation{
 string rmw_impl
 }

 rcl_client_init{
 address client_handle
 address node_handle
 address rmw_client_handle
 string service_name
 }

 rcl_lifecycle_state_machine_init{
 address node_handle
 address state_machine
 }

    rcl_node_init ||--o{ rcl_publisher_init : node_handle
    rcl_node_init ||--o{ rcl_subscription_init : node_handle
    rcl_node_init ||--o{ rclcpp_timer_link_node : node_handle
    rcl_node_init ||--o{ rcl_service_init : node_handle

    rcl_publisher_init ||--|| PUBLISHER_HANDLE : node_handle
    rcl_subscription_init ||--|| SUBSCRIPTION_HANDLE : node_handle
    rcl_timer_init ||--|| TIMER_HANDLE : node_handle
    rcl_service_init ||--|| SERVICE_HANDLE : node_handle

    rclcpp_subscription_init ||--|| rclcpp_ipb_to_subscription : subscription
    rclcpp_ipb_to_subscription ||--|| rclcpp_buffer_to_ipb : ipb
    rclcpp_buffer_to_ipb ||--|| rclcpp_construct_ring_buffer : buffer

    rcl_subscription_init ||--|| rclcpp_subscription_init : subscription_handle
    rclcpp_subscription_init ||--|| rclcpp_subscription_callback_added : subscription

    rcl_service_init ||--|| rclcpp_service_callback_added : service_handle
    rclcpp_service_callback_added ||--|| rclcpp_callback_register : callback

    rclcpp_timer_callback_added ||--|| rclcpp_callback_register : callback
    rclcpp_subscription_callback_added ||--|| rclcpp_callback_register : callback

    rclcpp_timer_callback_added ||--|| rcl_timer_init : timer_handle
    rclcpp_timer_link_node ||--|| rcl_timer_init: timer_handle

```

### エグゼキュータとコールバック グループの構造を表すトレースポイント

`timer_handle` や `subscription_handle` などのハンドラーがコールバック グループに割り当てられます。コールバック グループはエグゼキュータに属します。

各トレースポイントと実行者との関係は以下のとおりです。

```mermaid
erDiagram
 construct_executor{
 address executor_addr
 string executor_type_name
 }

 construct_static_executor{
 address executor_addr
 address entities_collector_addr
 string executor_type_name
 }

 add_callback_group{
 address executor_addr
 address callback_group_addr
 string group_type_name
 }

 callback_group_to_executor_entity_collector{
 address entities_collector_addr
 address callback_group_addr
 address group_type_name
 }
 executor_entity_collector_to_executor{
 address executor_addr
 address entities_collector_addr
 }

 add_callback_group_static_executor{
 address entities_collector_addr
 address callback_group_addr
 string group_type_name
 }

 callback_group_add_timer{
 address callback_group_addr
 address timer_handle
 }

 callback_group_add_subscription{
 address callback_group_addr
 address subscription_handle
 }

 callback_group_add_service{
 address callback_group_addr
 address service_handle
 }

 callback_group_add_client{
 address callback_group_addr
 address client_handle
 }


 construct_executor ||--o{ add_callback_group : executor_addr
 construct_static_executor ||--o{ add_callback_group_static_executor : entities_collector_addr

    add_callback_group_static_executor ||--o{ callback_group_add_timer : callback_group_addr
    add_callback_group_static_executor ||--o{ callback_group_add_subscription : callback_group_addr
    add_callback_group_static_executor ||--o{ callback_group_add_service : callback_group_addr
    add_callback_group_static_executor ||--o{ callback_group_add_client : callback_group_addr
    callback_group_to_executor_entity_collector ||--|| executor_entity_collector_to_executor: entities_collector_addr
    executor_entity_collector_to_executor ||--|| construct_executor: executor_addr
    executor_entity_collector_to_executor ||--|| construct_static_executor: executor_addr
    add_callback_group ||--o{ callback_group_add_timer : callback_group_addr
    add_callback_group ||--o{ callback_group_add_subscription : callback_group_addr
    add_callback_group ||--o{ callback_group_add_service : callback_group_addr
    add_callback_group ||--o{ callback_group_add_client : callback_group_addr

    callback_group_to_executor_entity_collector ||--o{ callback_group_add_timer : callback_group_addr
    callback_group_to_executor_entity_collector ||--o{ callback_group_add_subscription : callback_group_addr
    callback_group_to_executor_entity_collector ||--o{ callback_group_add_service : callback_group_addr
    callback_group_to_executor_entity_collector ||--o{ callback_group_add_client : callback_group_addr
    callback_group_add_timer ||--|| TIMER_HANDLE : callback_group_addr
    callback_group_add_subscription ||--|| SUBSCRIPTION_HANDLE : callback_group_addr
    callback_group_add_service ||--|| SERVICE_HANDLE : callback_group_addr
    callback_group_add_client ||--|| CLIENT_HANDLE : callback_group_addr


```

### トレースポイントの定義

トレースポイントの定義を以下に示します。
`timer_handle` や `subscription_handle` などのハンドラーがコールバック グループに割り当てられます。コールバック グループはエグゼキュータに属します。

`(caret_trace added)` を持つトレース ポイントは、caret_trace によってフックされ、init_timestamp が追加されます。
詳細については、[Runtime recording](../runtime_processing/runtime_recording.md#tracepoint) を参照してください。

#### ros2:rcl_init

[内蔵トレースポイント]

サンプル品

- void \* context_handle
- int64_t init_timestamp (caret_trace追加)

---

#### ros2:rcl_node_init

[内蔵トレースポイント]

サンプル品

- void \* node_handle
- void \* rmw_handle
- char \* node_name
- char \* node_namespace
- int64_t init_timestamp (caret_trace追加)

---

#### ros2:rcl_publisher_init

[内蔵トレースポイント]

サンプル品

- void \* Publisher_handle
- void \* node_handle
- void \* rmw_publisher_handle
- char \* topic_name
- size_t queue_depth
- int64_t init_timestamp (caret_trace追加)

---

#### ros2:rcl_subscription_init

[内蔵トレースポイント]

サンプル品

- void \* subscription_handle
- void \* node_handle
- void \* rmw_subscription_handle
- char \* topic_name
- size_t queue_depth
- int64_t init_timestamp (caret_trace追加)

---

#### ros2:rclcpp_subscription_init

[内蔵トレースポイント]

サンプル品

- void \* subscription_handle
- void \* subscription
- int64_t init_timestamp (caret_trace追加)

---

#### ros2:rclcpp_subscription_callback_added

[内蔵トレースポイント]

サンプル品

- void \* subscription
- void \* callback
- int64_t init_timestamp (caret_trace 追加)

---

#### ros2:rcl_service_init

[内蔵トレースポイント]

サンプル品

- void \* service_handle
- void \* node_handle
- void \* rmw_service_handle
- char \* service_name

---

#### ros2:rclcpp_service_callback_added

[内蔵トレースポイント]

サンプル品

- void \* service_handle
- void \* callback

---

#### ros2:rcl_timer_init

[内蔵トレースポイント]

サンプル品

- void \* timer_handle
- int64_t period
- int64_t init_timestamp (caret_trace追加)

---

#### ros2:rclcpp_timer_callback_added

[内蔵トレースポイント]

サンプル品

- void \* timer_handle
- void \* callback
- int64_t init_timestamp (caret_trace追加)

---

#### ros2:rclcpp_timer_link_node

[内蔵トレースポイント]

サンプル品

- void \* timer_handle
- void \* node_handle
- int64_t init_timestamp (caret_trace追加)

---

#### ros2:rclcpp_callback_register

[内蔵トレースポイント]

サンプル品

- void \* callback
- char \* function_symbol
- int64_t init_timestamp (caret_trace追加)

---

#### ros2:rclcpp_ipb_to_subscription

[内蔵トレースポイント]

サンプル品

- void \* ipb
- void \* subscription
- int64_t init_timestamp (caret_trace 追加)

<prettier-ignore-start>
!!!Note
    iron以降およびイントラ通信のみ。
<prettier-ignore-end>

---

#### ros2:rclcpp_buffer_to_ipb

[内蔵トレースポイント]

サンプル品

- void \* buffer
- void \* ipb
- int64_t init_timestamp (caret_trace 追加)

<prettier-ignore-start>
!!!Note
    iron以降およびイントラ通信のみ。
<prettier-ignore-end>

---

#### ros2:rclcpp_construct_ring_buffer

[内蔵トレースポイント]

サンプル品

- void \* buffer
- uint64_t capacity
- int64_t init_timestamp (caret_trace追加)

<prettier-ignore-start>
!!!Note
    iron以降およびイントラ通信のみ。
<prettier-ignore-end>

---

#### ros2_caret:caret_init

[フックされたトレースポイント]

サンプル品

- int64_t clock_offset
- char \* distribution

---

#### ros2_caret:rmw_implementation

[フックされたトレースポイント]

サンプル品

- char \* rmw_impl
- int64_t init_timestamp

---

#### ros2:rcl_client_init

[内蔵トレースポイント]

サンプル品

- void \* client_handle
- void \* node_handle
- void \* rmw_client_handle
- char \* service_name

---

#### ros2:rcl_lifecycle_state_machine_init

[内蔵トレースポイント]

サンプル品

- void \* node_handle
- void \* state_machine

---

#### ros2_caret:callback_group_to_executor_entity_collector

サンプル品

- void \* entities_collector_addr
- void \* callback_group_addr
- void \* group_type_name
- int64_t init_timestamp

<prettier-ignore-start>
!!!Note
    このトレース ポイントは jazzy 以降で使用できます。
<prettier-ignore-end>

---

#### ros2_caret:executor_entity_collector_to_executor

サンプル品

- void \* executor_addr
- void \* entities_collector_addr
- int64_t init_timestamp

<prettier-ignore-start>
!!!Note
    このトレース ポイントは jazzy 以降で使用できます。
<prettier-ignore-end>

---

#### ros2_caret:construct_executor

[フックされたトレースポイント]

サンプル品

- void \* executor_addr
- char \* executor_type_name
- int64_t init_timestamp

---

#### ros2_caret:construct_static_executor

[フックされたトレースポイント]

サンプル品

- void \* executor_addr
- void \* entities_collector_addr
- char \* executor_type_name
- int64_t init_timestamp

---

#### ros2_caret:add_callback_group

[フックされたトレースポイント]

サンプル品

- void \* executor_addr
- void \* callback_group_addr
- char \* group_type_name
- int64_t init_timestamp

<prettier-ignore-start>
!!!Note
    このトレース ポイントは jazzy 以降は使用できません。
<prettier-ignore-end>

---

#### ros2_caret:add_callback_group_static_executor

[フックされたトレースポイント]

サンプル品

- void \* entities_collector_addr
- void \* callback_group_addr
- char \* group_type_name
- int64_t init_timestamp

<prettier-ignore-start>
!!!Note
    このトレース ポイントは jazzy 以降は使用できません。
<prettier-ignore-end>

---

#### ros2_caret:callback_group_add_timer

[フックされたトレースポイント]

サンプル品

- void \* callback_group_addr
- void \* timer_handle
- int64_t init_timestamp

---

#### ros2_caret:callback_group_add_subscription

[フックされたトレースポイント]

サンプル品

- void \* callback_group_addr
- void \* subscription_handle
- int64_t init_timestamp

---

#### ros2_caret:callback_group_add_service

[フックされたトレースポイント]

サンプル品

- void \* callback_group_addr
- void \* service_handle
- int64_t init_timestamp

---

#### ros2_caret:callback_group_add_client

[フックされたトレースポイント]

サンプル品

- void \* callback_group_addr
- void \* client_handle
- int64_t init_timestamp
