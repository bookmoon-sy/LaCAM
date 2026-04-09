# 🎮 MAPF Visualizer 控制器

## 📋 概述

这是一个图形用户界面(GUI)控制器，用于控制 **mapf-visualizer** 程序。通过这个界面，你可以：
- 选择地图文件和解决方案文件
- 从示例列表快速选择
- 一键运行默认示例
- 控制mapf-visualizer的启动和停止
- 查看所有控制键说明

## 🚀 快速开始

### 启动控制器
```bash
cd /home/sy/Homework/LaCAM

# 方法1: 使用测试脚本（推荐）
./test_controller.sh

# 方法2: 直接启动
./run_mapf_controller

# 方法3: 直接运行Python脚本
python3 mapf_visualizer_controller.py
```

### 直接运行mapf-visualizer（命令行）
```bash
# 运行默认示例
cd mapf-visualizer
./bin/mapf-visualizer assets/random-32-32-20.map assets/demo_random-32-32-20.txt

# 或使用包装脚本
cd /home/sy/Homework/LaCAM
./run_visualizer
```

## 🎯 控制器功能

### 1. 文件选择
- **浏览地图文件**：选择 `.map` 格式的地图文件
- **浏览解决方案文件**：选择 `.txt` 格式的解决方案文件
- **自动定位**：默认从 `mapf-visualizer/assets/` 目录开始浏览

### 2. 快速示例
- **示例列表**：自动扫描并列出所有可用的示例文件
- **一键选择**：点击"使用此示例"自动填充文件路径
- **示例信息**：显示地图尺寸信息（如 "random-32-32-20 (32x32)"）

### 3. 控制按钮
- **🚀 启动 MAPF Visualizer**：使用当前选择的文件运行可视化
- **📁 运行默认示例**：一键运行 `random-32-32-20.map` 示例
- **⏹️ 停止**：停止正在运行的可视化器

### 4. 控制键说明
显示所有MAPF Visualizer的键盘控制键，包括：
- 播放/暂停、循环、重置
- 显示虚拟线、ID、目标
- 前进/后退、加速/减速
- 放大/缩小、网格显示、截图
- 退出

## 📁 文件说明

### 核心文件
- `mapf_visualizer_controller.py` - 主控制器程序
- `run_mapf_controller` - 控制器启动脚本
- `test_controller.sh` - 测试脚本

### 依赖文件
- `mapf-visualizer/bin/mapf-visualizer` - MAPF Visualizer可执行文件
- `mapf-visualizer/assets/` - 示例地图和解决方案文件
- `run_visualizer` - 原始运行脚本（保留）

## 🔧 系统要求

### 必需组件
1. **mapf-visualizer 程序**
   ```bash
   # 如果未编译，需要先编译
   cd mapf-visualizer
   make clean
   make -j4
   ```

2. **Python3 和 Tkinter**
   ```bash
   # 安装Python3
   sudo apt-get install python3
   
   # 安装Tkinter（GUI库）
   sudo apt-get install python3-tk
   ```

### 检查安装
```bash
# 检查mapf-visualizer
ls -la mapf-visualizer/bin/mapf-visualizer

# 检查Python依赖
python3 -c "import tkinter; print('Tkinter可用')"
```

## 🎮 使用方法

### 步骤1: 选择文件
1. 点击"浏览..."按钮选择地图文件（`.map`格式）
2. 点击"浏览..."按钮选择解决方案文件（`.txt`格式）
3. 或从示例下拉列表中选择并点击"使用此示例"

### 步骤2: 运行可视化
1. 点击"🚀 启动 MAPF Visualizer"按钮
2. MAPF Visualizer窗口将打开
3. 使用键盘控制键操作可视化

### 步骤3: 控制操作
- **暂停/继续**：在可视化窗口按 `p` 键
- **停止可视化**：在控制器点击"⏹️ 停止"按钮
- **退出可视化**：在可视化窗口按 `ESC` 键

## 🎯 MAPF Visualizer 控制键

### 基本控制
| 按键 | 功能 |
|------|------|
| `p` | 播放/暂停 |
| `l` | 循环/不循环 |
| `r` | 重置 |
| `ESC` | 退出 |

### 显示控制
| 按键 | 功能 |
|------|------|
| `v` | 显示到目标的虚拟线 |
| `f` | 显示智能体 & 节点ID |
| `g` | 显示目标 |
| `G` | 显示/隐藏网格 |

### 导航控制
| 按键 | 功能 |
|------|------|
| `→` | 前进一个时间步 |
| `←` | 后退一个时间步 |
| `↑` | 加速动画 |
| `↓` | 减速动画 |

### 视图控制
| 按键 | 功能 |
|------|------|
| `i` | 放大 |
| `o` | 缩小 |
| `空格` | 截图（保存到桌面） |

## 🛠️ 故障排除

### 问题1: "找不到 mapf-visualizer 可执行文件"
```bash
# 编译mapf-visualizer
cd mapf-visualizer
make clean
make -j4

# 检查是否编译成功
ls -la bin/mapf-visualizer
```

### 问题2: "tkinter未安装"
```bash
# 安装Tkinter
sudo apt-get install python3-tk

# 验证安装
python3 -c "import tkinter; print('安装成功')"
```

### 问题3: MAPF Visualizer 段错误
如果出现段错误（segmentation fault）：
1. 可能是图形驱动问题
2. 尝试在终端直接运行检查错误信息
3. 控制器会检测到段错误并显示警告

### 问题4: 示例文件不存在
```bash
# 检查示例文件
ls -la mapf-visualizer/assets/

# 如果目录为空，可能需要重新下载或解压
```

## 📊 示例文件

控制器自动扫描的示例文件位于：
```
mapf-visualizer/assets/
├── random-32-32-20.map          # 32x32地图，20%障碍物
├── demo_random-32-32-20.txt     # 对应解决方案
├── ost003d.map                  # 标准测试地图
├── demo_ost003d.txt             # 对应解决方案
├── 2x2.map                      # 小型测试地图
├── demo_2x2.txt                 # 对应解决方案
└── ...                          # 其他示例文件
```

## 🎉 开始使用

### 最简单的开始方式
```bash
cd /home/sy/Homework/LaCAM
./test_controller.sh
```

### 直接运行默认示例
在控制器中点击"📁 运行默认示例"按钮。

### 手动选择文件
1. 点击"浏览..."选择 `mapf-visualizer/assets/random-32-32-20.map`
2. 点击"浏览..."选择 `mapf-visualizer/assets/demo_random-32-32-20.txt`
3. 点击"🚀 启动 MAPF Visualizer"

## 📝 注意事项

1. **mapf-visualizer 必须已编译**：控制器需要可执行的 `mapf-visualizer` 程序
2. **图形环境**：需要在图形桌面环境中运行
3. **控制键**：控制键在MAPF Visualizer窗口中有效，不是在控制器窗口中
4. **段错误处理**：控制器会检测并报告段错误，但无法修复底层问题
5. **进程管理**：使用"⏹️ 停止"按钮可以强制停止卡住的可视化器

## 🤝 与原始工具集成

### 使用原始运行脚本
```bash
# 原始运行方式仍然可用
./run_visualizer

# 或直接运行
cd mapf-visualizer
./bin/mapf-visualizer 地图文件.map 解决方案文件.txt
```

### 控制器优势
- 图形化文件选择
- 示例文件管理
- 进程控制（启动/停止）
- 控制键参考
- 错误检测和报告

现在你可以通过图形界面轻松控制MAPF Visualizer了！