# 🦐 LaCAM 多智能体路径规划框架

一个完整的LaCAM（Lazy Constraints Addition for Multi-agent pathfinding）框架实现，包含可视化工具和用户界面。

## 🎯 项目概述

LaCAM是一个高效的多智能体路径规划（MAPF）算法框架。本项目整合了：
- **LaCAM核心算法** - 基于C++的高效路径规划实现
- **MAPF Visualizer** - 基于openFrameworks的可视化工具
- **图形用户界面** - Python/Tkinter的友好界面
- **工具集** - 地图创建、场景生成等辅助工具

## 📁 项目结构

```
LaCAM/
├── 📄 README.md                 # 本文件
├── 📄 lacam0_README.md          # LaCAM完整使用指南
├── 📄 MAPF_CONTROLLER_README.md # MAPF Visualizer控制器文档
├── 📄 DIRECTORY_STRUCTURE.md    # 目录结构说明
├── 🚀 run_lacam                 # 命令行入口
├── 🎯 run_lacam_unified         # 统一核心脚本
├── 🖥️ run_gui                   # GUI启动脚本
├── 🎮 run_mapf_controller       # MAPF控制器启动
├── 🎨 run_visualizer            # 可视化器启动
├── 📂 tools/                    # 功能性工具
│   ├── 🖥️ lacam_gui.py          # 图形用户界面
│   ├── 🗺️ create_maps.py        # 地图创建工具
│   ├── 🛡️ create_safe_scenario.py # 安全场景创建
│   ├── 🔧 fix_all_isolated_cells.py # 修复孤立单元格
│   ├── 🎮 simple_controller.py  # MAPF Visualizer控制器
│   └── 🧪 test_controller.sh    # 控制器测试脚本
├── 📂 lacam0/                   # LaCAM核心框架（C++）
└── 📂 mapf-visualizer/         # MAPF可视化器（C++/openFrameworks）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3 python3-tk git build-essential cmake
```

### 2. 克隆仓库

```bash
git clone https://github.com/你的用户名/LaCAM.git
cd LaCAM
```

### 3. 编译核心算法

```bash
cd lacam0
make -C build -j4
```

### 4. 编译可视化器（可选）

MAPF Visualizer需要openFrameworks。首先安装依赖：

```bash
# 安装openFrameworks依赖
cd mapf-visualizer
./install_linux.sh

# 下载openFrameworks（约900MB）
# 脚本会自动下载并解压到third_party/openFrameworks/

# 编译可视化器
make -j4
```

注意：openFrameworks文件较大，首次编译需要较长时间。

### 5. 启动使用

```bash
# 图形界面（推荐）
./run_gui

# 命令行模式
./run_lacam

# MAPF Visualizer控制器
./run_mapf_controller
```

## 🔧 核心功能

### 🦐 LaCAM算法
- 高效的冲突解决策略
- 支持大规模智能体规划（1000+智能体）
- 多种启发式算法选择
- 实时进度显示

### 🎨 可视化工具
- 实时路径规划可视化
- 智能体移动动画
- 冲突检测显示
- 多种视图模式

### 🖥️ 用户界面
- 图形化参数配置
- 文件选择器
- 实时状态监控
- 一键运行测试

### 🛠️ 工具集
- 自定义地图创建
- 安全场景生成
- 地图问题修复
- 批量测试支持

## 📊 性能特点

- **高效性**：支持大规模智能体路径规划
- **可视化**：实时显示规划过程和结果
- **易用性**：提供图形界面和命令行两种方式
- **可扩展**：模块化设计，易于添加新功能
- **跨平台**：支持Linux/macOS/Windows（WSL）

## 🧪 测试场景

项目包含多种测试场景：
- 微型测试（5-30智能体）
- 标准测试（100-500智能体）
- 大规模测试（500+智能体）
- 自定义场景支持

## 📖 详细文档

- [LaCAM完整使用指南](lacam0_README.md) - 安装、使用、故障排除
- [MAPF Visualizer控制器文档](MAPF_CONTROLLER_README.md) - 可视化工具使用说明
- [目录结构说明](DIRECTORY_STRUCTURE.md) - 项目文件结构

## 🎮 使用示例

### 基本使用
```bash
# 启动图形界面
./run_gui

# 选择地图和场景文件
# 设置智能体数量
# 点击"运行"开始规划
```

### 命令行高级使用
```bash
# 查看所有选项
./run_lacam --help

# 运行特定测试
./run_lacam -m random-32-32-10.map -s random-32-32-10-random-1.scen -N 400

# 批量测试
./run_lacam --batch-test
```

### 可视化查看
```bash
# 启动MAPF Visualizer控制器
./run_mapf_controller

# 选择地图和解决方案文件
# 点击"启动 MAPF Visualizer"
# 使用控制键交互查看
```

## 🔧 开发指南

### 添加新地图
1. 将`.map`文件放入`lacam0/assets/`
2. 创建对应的场景文件`.scen`
3. 重启GUI或刷新文件列表

### 扩展功能
1. 在`tools/`目录中添加新工具
2. 更新`run_lacam_unified`脚本集成新功能
3. 更新相关文档

### 编译说明
```bash
# 编译LaCAM核心
cd lacam0
make -C build clean
make -C build -j4

# 编译可视化器
cd mapf-visualizer
make clean
make -j4
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！
1. Fork本仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目基于MIT许可证开源。

## 🙏 致谢

- LaCAM算法原作者
- openFrameworks社区
- 所有贡献者和用户

---

**项目状态**：✅ 功能完整 | ✅ 文档齐全 | ✅ 测试通过  
**最后更新**：2026-04-09  
**维护者**：舒悦# LaCAM
