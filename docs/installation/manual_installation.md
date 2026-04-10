# 手動インストール

## 必要なパッケージのインストール

### LTTng をインストールします

詳細については、[the official document for LTTng](https://lttng.org/docs/v2.12/#doc-ubuntu-ppa)を参照してください

```bash
sudo apt-add-repository ppa:lttng/stable-2.13
sudo apt-get update
sudo apt-get install lttng-tools liblttng-ust-dev
sudo apt-get install python3-babeltrace python3-lttng
```

### CARET をビルドするパッケージをインストールします

ROS 2 Humble および関連パッケージをインストールします。
[the official document for ROS 2](https://docs.ros.org/en/humble/Installation/Ubuntu-Development-Setup.html) も参照してください。

```bash
sudo apt update && sudo apt install -y \
  build-essential \
  cmake \
  git \
  python3-colcon-common-extensions \
  python3-flake8 \
  python3-pip \
  python3-pytest-cov \
  python3-rosdep \
  python3-setuptools \
  python3-vcstool \
  python3-bt2 \
  wget

python3 -m pip install -U \
  flake8-blind-except \
  flake8-builtins \
  flake8-class-newline \
  flake8-comprehensions \
  flake8-deprecated \
  flake8-docstrings \
  flake8-import-order \
  flake8-quotes \
  pytest-repeat \
  pytest-rerunfailures \
  pytest \
  setuptools \
  colorcet

sudo apt install ros-humble-desktop
```

[`ros2_tracing`](https://github.com/ros2/ros2_tracing) に関連するパッケージをインストールします

```bash
sudo apt install -y \
  ros-humble-ros2trace \
  ros-humble-ros2trace-analysis \
  ros-humble-tracetools \
  ros-humble-tracetools-analysis \
  ros-humble-tracetools-launch \
  ros-humble-tracetools-read \
  ros-humble-tracetools-test \
  ros-humble-tracetools-trace
```

CARET を使用して視覚化用のパッケージをインストールします。

```bash
sudo apt update && sudo apt install -y \
  graphviz \
  graphviz-dev

python3 -m pip install -U \
  pytest-mock \
  pybind11 \
  'pandas>=1.4.0' \
  bokeh \
  pandas-bokeh \
  jupyterlab \
  graphviz

# If you see the message, [ImportError: The Jupyter Server requires tornado >=6.1.0] during installing jupyterlab,
# upgrade tornado with the following command.
# pip install tornado --upgrade
```

## Source build of CARET

```bash
mkdir -p ~/ros2_caret_ws/src
cd ~/ros2_caret_ws

wget https://raw.githubusercontent.com/tier4/caret/main/caret.repos
vcs import src < caret.repos

rosdep install \
  --from-paths src --ignore-src \
  --rosdistro humble -y \
  --skip-keys "console_bridge fastcdr fastrtps rti-connext-dds-5.3.1 urdfdom_headers"

# If you find the error message, [ERROR: the following packages/stacks could not have their rosdep keys resolved],
# execute rosdep initialization and update with the following two commands.
# rosdep init
# rosdep update
source /opt/ros/humble/setup.bash

# Create symbolic link so that the header files, which are provided by the forked packages, should be referred
ln -sf ~/ros2_caret_ws/src/ros-tracing/ros2_tracing/tracetools/include/tracetools ~/ros2_caret_ws/src/ros2/rclcpp/rclcpp/include/
ln -sf ~/ros2_caret_ws/src/ros2/rclcpp/rclcpp_action/include/rclcpp_action ~/ros2_caret_ws/src/ros2/rclcpp/rclcpp/include/
ln -sf ~/ros2_caret_ws/src/ros2/rclcpp/rclcpp_components/include/rclcpp_components/ ~/ros2_caret_ws/src/ros2/rclcpp/rclcpp/include/
ln -sf ~/ros2_caret_ws/src/ros2/rclcpp/rclcpp_lifecycle/include/rclcpp_lifecycle/ ~/ros2_caret_ws/src/ros2/rclcpp/rclcpp/include/

# Build CARET with colcon command
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=off  --symlink-install
```

`ros2_tracing` が利用可能かどうかを確認してください

```bash
$ source ~/ros2_caret_ws/install/local_setup.bash
$ ros2 run tracetools status
Tracing enabled
```
