#!/bin/bash
# test_controller.sh - 测试MAPF Visualizer控制器

echo "🚀 MAPF Visualizer 控制器测试"
echo "=============================="
echo ""

# 检查mapf-visualizer
echo "检查 mapf-visualizer..."
if [ -f "mapf-visualizer/bin/mapf-visualizer" ]; then
    echo "✅ mapf-visualizer 可执行文件存在"
    echo "   路径: mapf-visualizer/bin/mapf-visualizer"
else
    echo "❌ mapf-visualizer 可执行文件不存在"
    echo "   请先编译: cd mapf-visualizer && make"
fi

echo ""

# 检查示例文件
echo "检查示例文件..."
if [ -f "mapf-visualizer/assets/random-32-32-20.map" ]; then
    echo "✅ 示例地图文件存在"
else
    echo "❌ 示例地图文件不存在"
fi

if [ -f "mapf-visualizer/assets/demo_random-32-32-20.txt" ]; then
    echo "✅ 示例解决方案文件存在"
else
    echo "❌ 示例解决方案文件不存在"
fi

echo ""

# 检查Python依赖
echo "检查Python依赖..."
python3 -c "import tkinter" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ tkinter 可用"
else
    echo "❌ tkinter 不可用"
    echo "   安装: sudo apt-get install python3-tk"
fi

echo ""
echo "启动控制器..."
echo ""
echo "控制器功能:"
echo "  1. 选择地图文件和解决方案文件"
echo "  2. 从示例列表快速选择"
echo "  3. 一键运行默认示例"
echo "  4. 显示MAPF Visualizer控制键说明"
echo "  5. 停止正在运行的可视化"
echo ""
echo "MAPF Visualizer 控制键:"
echo "  p: 播放/暂停, l: 循环, r: 重置, v: 显示虚拟线"
echo "  f: 显示ID, g: 显示目标, →←: 前进/后退, ↑↓: 加速/减速"
echo "  ESC: 退出"
echo ""

# 启动控制器
./run_mapf_controller