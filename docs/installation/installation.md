# インストール

＃＃ 要件

CARET は、次の表に示すプラットフォームでサポートされているバージョンで動作することが確認されています。

|ROS 2 |OS |LTTng |パイソン |ステータス |
|:----- |:----------- |:---------- |:----- |:-------------- |
| Jazzy  | Ubuntu 24.04 | stable-2.13 | 3.12.x | Supported       |
|Humble |Ubuntu 22.04 |安定版-2.13 |3.10.x |サポートあり (LTS) |

ROS 2 ディストリビューションに応じた手順に従ってください。jazzy の場合は、PEP 668 に準拠するためにセットアップ手順でエクスポート コマンドを実行していることを確認してください。

## インストール

Installation using meta repository is the least time-consuming way to install CARET.  
メタリポジトリと Ansible を使用すると、手動インストール (./manual_installation.md) セクション (日本語で書かれています) で説明されている面倒な手動セットアップを省略できます。

Ubuntu 22.04 または 24.04 で次の手順を実行してください。順序が重要であるため、手順を順番に実行する必要があります。

   <details>
   <summary>jazzy</summary>用

Ubuntu 24.04 (Jazzy) ではシステム環境 (PEP 668) への pip インストールが制限されているため、セットアップ スクリプトを実行する前に環境変数 (PIP_BREAK_SYSTEM_PACKAGES) を設定してこれを確認する必要があります。
Jazzy を使用している場合は、必要な環境変数を含む、以下の jazzy タブの手順に従ってください。

   </details>

<prettier-ignore-start>
1. `caret` を複製し、ディレクトリに入ります。
<prettier-ignore-end>

```bash
git clone https://github.com/tier4/caret.git ros2_caret_ws
cd ros2_caret_ws
```

<prettier-ignore-start>
2. src ディレクトリを作成し、その中にリポジトリのクローンを作成します。
<prettier-ignore-end>

CARET は vcstool を使用してワークスペースを構築します。

=== "humble"

    ``` bash
    mkdir src
    vcs import src < caret.repos
    ```

=== "iron"

    ``` bash
    mkdir src
    vcs import src < caret_iron.repos
    ```

=== "jazzy"

    ``` bash
    mkdir src
    vcs import src < caret_jazzy.repos
    ```

<prettier-ignore-start>
3. `setup_caret.sh` を実行します。
<prettier-ignore-end>

=== "humble"

    ``` bash
    ./setup_caret.sh
    ```

=== "iron"

    ``` bash
    ./setup_caret.sh -d iron
    ```

=== "jazzy"

    ``` bash
    export PIP_BREAK_SYSTEM_PACKAGES=1
    ./setup_caret.sh -d jazzy
    ```

<prettier-ignore-start>
4. ワークスペースを構築します。
<prettier-ignore-end>

=== "humble"

    ``` bash
    source /opt/ros/humble/setup.bash
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
    ```

=== "iron"

    ``` bash
    source /opt/ros/iron/setup.bash
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
    ```

=== "jazzy"

    ``` bash
    source /opt/ros/jazzy/setup.bash
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
    ```

<prettier-ignore-start>
5. CARET (ros2-tracing) が有効になっているかどうかを確認します。
<prettier-ignore-end>

CARET は [ros2-tracing](https://gitlab.com/ros-tracing/ros2_tracing) から一部の機能を継承します。

```bash
source ~/ros2_caret_ws/install/local_setup.bash
ros2 run tracetools status # return Tracing enabled
```

`Tracing enabled` が表示された場合は、引き続きアプリケーションに CARET を適用できます。
