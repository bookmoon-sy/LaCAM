# 📁 LaCAM 项目目录结构（整理后）

## 🎯 核心文件（根目录）

### 1. **启动脚本**
- `run_lacam` - 🚀 命令行主入口（用户使用）
- `run_lacam_unified` - 🎯 统一核心脚本（所有功能集成）
- `run_gui` - 🖥️ 图形界面启动脚本
- `run_mapf_controller` - 🎮 MAPF Visualizer控制器启动
- `run_visualizer` - 🎨 可视化器启动

### 2. **文档**
- `lacam0_README.md` - 📖 LaCAM完整使用指南
- `MAPF_CONTROLLER_README.md` - 🎮 MAPF Visualizer控制器文档
- `DIRECTORY_STRUCTURE.md` - 📁 目录结构说明

### 3. **功能性工具目录**
- `tools/` - 🔧 所有功能性工具

### 4. **子项目**
- `lacam0/` - 🦐 LaCAM核心框架（C++）
- `mapf-visualizer/` - 🎨 MAPF可视化器（C++/openFrameworks）

## 📂 详细结构

```
LaCAM/
├── 📄 lacam0_README.md          # 主文档
├── 📄 MAPF_CONTROLLER_README.md # 控制器文档
├── 📄 DIRECTORY_STRUCTURE.md    # 目录结构
├── 🚀 run_lacam                 # 命令行入口
├── 🎯 run_lacam_unified         # 统一核心脚本
├── 🖥️ run_gui                   # GUI启动
├── 🎮 run_mapf_controller       # MAPF控制器启动
├── 🎨 run_visualizer            # 可视化器启动
├── 📂 tools/                    # 功能性工具
│   ├── 🖥️ lacam_gui.py          # 图形界面
│   ├── 🗺️ create_maps.py        # 地图创建
│   ├── 🛡️ create_safe_scenario.py # 安全场景
│   ├── 🔧 fix_all_isolated_cells.py # 修复工具
│   ├── 🎮 simple_controller.py  # MAPF控制器
│   └── 🧪 test_controller.sh    # 测试脚本
├── 📂 lacam0/                   # LaCAM核心框架
│   ├── 📄 README.md
│   ├── 📄 RUN_HELP.md
│   ├── 🚀 run_lacam.py
│   ├── 📂 src/                 # 源代码
│   ├── 📂 include/             # 头文件
│   ├── 📂 assets/              # 示例数据
│   ├── 📂 tests/               # 测试文件
│   └── 📂 build/               # 编译输出
└── 📂 mapf-visualizer/         # MAPF可视化器
    ├── 📄 README.md
    ├── 📄 install_linux.sh
    ├── 📂 src/                 # 源代码
    ├── 📂 include/             # 头文件
    ├── 📂 assets/              # 示例数据
    ├── 📂 bin/                 # 可执行文件
    └── 📂 third_party/         # 第三方依赖
```

## 🚀 快速启动指南

### 1. **命令行模式**
```bash
./run_lacam
```

### 2. **图形界面模式**
```bash
./run_gui
```

### 3. **MAPF Visualizer控制器**
```bash
./run_mapf_controller
```

### 4. **直接运行可视化器**
```bash
./run_visualizer
```

## 🔧 工具使用

所有功能性工具都位于 `tools/` 目录中：

### 地图创建工具
```bash
cd tools/
python3 create_maps.py
```

### 安全场景创建
```bash
cd tools/
python3 create_safe_scenario.py
```

### 修复孤立单元格
```bash
cd tools/
python3 fix_all_isolated_cells.py
```

### MAPF控制器
```bash
cd tools/
python3 simple_controller.py
```

### 控制器测试
```bash
cd tools/
./test_controller.sh
```

## 📖 详细文档

- **LaCAM框架**：阅读 `lacam0_README.md`
- **MAPF控制器**：阅读 `MAPF_CONTROLLER_README.md`
- **目录结构**：阅读本文件

## 🧹 整理说明

### ✅ 已完成整理
1. **清理多余文件**：删除所有旧的控制器版本和测试文件
2. **统一工具目录**：所有功能性工具移动到 `tools/` 目录
3. **更新启动脚本**：所有启动脚本指向正确的工具位置
4. **保持根目录整洁**：根目录只保留启动脚本和文档

### 📁 工具目录内容
```
tools/
├── 🖥️ lacam_gui.py          # 图形用户界面
├── 🗺️ create_maps.py        # 地图创建工具
├── 🛡️ create_safe_scenario.py # 安全场景创建工具
├── 🔧 fix_all_isolated_cells.py # 修复孤立单元格工具
├── 🎮 simple_controller.py  # MAPF Visualizer控制器
└── 🧪 test_controller.sh    # 控制器测试脚本
```

### 🚀 启动脚本对应关系
- `run_gui` → `tools/lacam_gui.py`
- `run_mapf_controller` → `tools/simple_controller.py`
- `run_visualizer` → `mapf-visualizer/bin/mapf-visualizer`

## 🎉 项目状态
- ✅ 目录结构：清晰整洁
- ✅ 功能性工具：统一管理
- ✅ 启动脚本：全部更新
- ✅ 文档：完整更新

**整理时间**：2026-04-09 20:25  
**整理内容**：清理多余文件，统一工具目录，更新启动脚本