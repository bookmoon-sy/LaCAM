#!/usr/bin/env python3
"""
创建各种测试地图文件
"""

import random
import os
from pathlib import Path

# 项目路径
ASSETS_DIR = Path("/home/sy/Homework/LaCAM/lacam0/assets")

def create_random_map(width, height, obstacle_ratio, filename):
    """创建随机地图"""
    map_lines = []
    
    # 地图头部
    map_lines.append("type octile")
    map_lines.append(f"height {height}")
    map_lines.append(f"width {width}")
    map_lines.append("map")
    
    # 生成随机地图
    for y in range(height):
        row = []
        for x in range(width):
            # 边缘保持可通行
            if x == 0 or x == width-1 or y == 0 or y == height-1:
                row.append('.')
            else:
                if random.random() < obstacle_ratio:
                    row.append('@')  # 障碍物
                else:
                    row.append('.')  # 可通行
        map_lines.append(''.join(row))
    
    # 保存文件
    filepath = ASSETS_DIR / filename
    with open(filepath, 'w') as f:
        f.write('\n'.join(map_lines))
    
    print(f"✅ 创建地图: {filename} ({width}x{height}, 障碍物比例: {obstacle_ratio*100:.0f}%)")
    return filepath

def create_narrow_corridor_map(filename="narrow-corridor-16-16.map"):
    """创建狭隘通道地图"""
    width = 16
    height = 16
    
    map_lines = []
    map_lines.append("type octile")
    map_lines.append(f"height {height}")
    map_lines.append(f"width {width}")
    map_lines.append("map")
    
    # 创建狭隘通道
    for y in range(height):
        row = []
        for x in range(width):
            # 创建两条垂直的狭隘通道
            if (x == 3 or x == 12) and (y >= 2 and y <= 13):
                row.append('.')  # 通道
            elif x >= 4 and x <= 11 and (y == 3 or y == 12):
                row.append('.')  # 横向连接
            else:
                row.append('@')  # 障碍物
        map_lines.append(''.join(row))
    
    # 保存文件
    filepath = ASSETS_DIR / filename
    with open(filepath, 'w') as f:
        f.write('\n'.join(map_lines))
    
    print(f"✅ 创建狭隘通道地图: {filename}")
    return filepath

def create_maze_map(filename="maze-24-24.map"):
    """创建迷宫地图"""
    width = 24
    height = 24
    
    # 简单的迷宫模式
    maze_pattern = [
        "@@@@@@@@@@@@@@@@@@@@@@@@",
        "@......................@",
        "@.@@@@.@@@@@@.@@@@@@.@@@",
        "@.@........@.@......@.@",
        "@.@@@@@@.@@.@@.@@@@.@.@",
        "@......@.@....@....@.@",
        "@.@@@@.@.@@@@@@.@@.@.@",
        "@.@....@........@.@.@",
        "@.@.@@@@@@.@@@@.@.@.@",
        "@.@......@.@....@.@.@",
        "@.@@@@.@@.@.@@@@.@.@",
        "@....@.@.@.@....@.@",
        "@.@@.@.@.@.@@@@.@.@",
        "@.@.@.@.@......@.@",
        "@.@.@.@.@@@@@@.@.@",
        "@.@.@.@........@.@",
        "@.@.@.@@@@@@.@@.@.@",
        "@.@.@......@.@.@.@",
        "@.@.@@@@.@@.@.@.@",
        "@.@....@.@.@.@.@",
        "@.@@@@.@.@.@.@.@",
        "@......@.@.@.@",
        "@@@@@@@@@@@@@@@@@@@@@@@@"
    ]
    
    map_lines = []
    map_lines.append("type octile")
    map_lines.append(f"height {height}")
    map_lines.append(f"width {width}")
    map_lines.append("map")
    map_lines.extend(maze_pattern[:height])
    
    # 保存文件
    filepath = ASSETS_DIR / filename
    with open(filepath, 'w') as f:
        f.write('\n'.join(map_lines))
    
    print(f"✅ 创建迷宫地图: {filename}")
    return filepath

def create_large_open_map(filename="open-48-48.map"):
    """创建大型开放地图"""
    width = 48
    height = 48
    
    map_lines = []
    map_lines.append("type octile")
    map_lines.append(f"height {height}")
    map_lines.append(f"width {width}")
    map_lines.append("map")
    
    # 几乎全开放，只有少量障碍物
    for y in range(height):
        row = []
        for x in range(width):
            # 边缘和少量随机障碍物
            if (x == 0 or x == width-1 or y == 0 or y == height-1 or
                (x % 8 == 0 and y % 8 == 0 and random.random() < 0.3)):
                row.append('@')
            else:
                row.append('.')
        map_lines.append(''.join(row))
    
    # 保存文件
    filepath = ASSETS_DIR / filename
    with open(filepath, 'w') as f:
        f.write('\n'.join(map_lines))
    
    print(f"✅ 创建大型开放地图: {filename}")
    return filepath

def create_scenario_for_map(map_file, num_agents, filename):
    """为地图创建场景文件"""
    # 读取地图尺寸
    map_path = ASSETS_DIR / map_file
    with open(map_path, 'r') as f:
        lines = f.readlines()
    
    # 解析地图尺寸
    height = int(lines[1].split()[1])
    width = int(lines[2].split()[1])
    
    # 读取地图数据，找出所有可通行位置
    map_data = lines[4:]  # 跳过前4行头部
    passable_positions = []
    
    for y in range(height):
        row = map_data[y].strip()
        for x in range(width):
            if row[x] == '.':  # 可通行位置
                passable_positions.append((x, y))
    
    if len(passable_positions) < num_agents * 2:
        print(f"⚠️  警告: 地图 {map_file} 可通行位置不足，减少智能体数量")
        num_agents = min(num_agents, len(passable_positions) // 2)
    
    # 生成场景文件
    scenario_lines = ["version 1"]
    
    # 随机选择起始和目标位置
    import random
    random.seed(42)  # 固定种子确保可复现
    
    selected_positions = random.sample(passable_positions, num_agents * 2)
    
    for i in range(num_agents):
        start_x, start_y = selected_positions[i * 2]
        goal_x, goal_y = selected_positions[i * 2 + 1]
        
        # 计算曼哈顿距离作为最优距离估计
        distance = abs(goal_x - start_x) + abs(goal_y - start_y)
        if distance == 0:
            distance = 1.0  # 避免零距离
        
        scenario_lines.append(f"{i+1}\t{map_file}\t{width}\t{height}\t{start_x}\t{start_y}\t{goal_x}\t{goal_y}\t{distance:.1f}")
    
    # 保存文件
    filepath = ASSETS_DIR / filename
    with open(filepath, 'w') as f:
        f.write('\n'.join(scenario_lines))
    
    print(f"✅ 创建场景文件: {filename} ({num_agents}个智能体)")
    return filepath

def main():
    """主函数"""
    print("🗺️ 开始创建地图和场景文件...")
    print("=" * 50)
    
    # 确保目录存在
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. 大型地图（支持几千智能体）
    print("\n📏 创建大型地图:")
    large_map = create_random_map(64, 64, 0.15, "random-64-64-15.map")
    create_scenario_for_map("random-64-64-15.map", 2000, "random-64-64-15-2000.scen")
    create_scenario_for_map("random-64-64-15.map", 500, "random-64-64-15-500.scen")
    
    # 2. 中型地图
    print("\n📏 创建中型地图:")
    medium_map = create_random_map(48, 48, 0.20, "random-48-48-20.map")
    create_scenario_for_map("random-48-48-20.map", 1000, "random-48-48-20-1000.scen")
    create_scenario_for_map("random-48-48-20.map", 200, "random-48-48-20-200.scen")
    
    # 3. 狭隘通道地图
    print("\n🚧 创建狭隘通道地图:")
    narrow_map = create_narrow_corridor_map()
    create_scenario_for_map("narrow-corridor-16-16.map", 10, "narrow-corridor-16-16-10.scen")
    create_scenario_for_map("narrow-corridor-16-16.map", 5, "narrow-corridor-16-16-5.scen")
    
    # 4. 迷宫地图
    print("\n🌀 创建迷宫地图:")
    maze_map = create_maze_map()
    create_scenario_for_map("maze-24-24.map", 50, "maze-24-24-50.scen")
    create_scenario_for_map("maze-24-24.map", 20, "maze-24-24-20.scen")
    
    # 5. 大型开放地图
    print("\n🌄 创建大型开放地图:")
    open_map = create_large_open_map()
    create_scenario_for_map("open-48-48.map", 1500, "open-48-48-1500.scen")
    create_scenario_for_map("open-48-48.map", 300, "open-48-48-300.scen")
    
    # 6. 小型测试地图
    print("\n🔬 创建小型测试地图:")
    small_map = create_random_map(16, 16, 0.10, "random-16-16-10.map")
    create_scenario_for_map("random-16-16-10.map", 100, "random-16-16-10-100.scen")
    create_scenario_for_map("random-16-16-10.map", 30, "random-16-16-10-30.scen")
    
    print("\n" + "=" * 50)
    print("🎉 地图和场景文件创建完成！")
    print("\n📁 创建的文件:")
    
    # 列出创建的文件
    import glob
    new_maps = sorted(glob.glob(str(ASSETS_DIR / "*.map")))
    new_scens = sorted(glob.glob(str(ASSETS_DIR / "*.scen")))
    
    print(f"\n🗺️ 地图文件 ({len(new_maps)}个):")
    for m in new_maps[-10:]:  # 显示最近创建的
        print(f"  {Path(m).name}")
    
    print(f"\n🎯 场景文件 ({len(new_scens)}个):")
    for s in new_scens[-10:]:  # 显示最近创建的
        scene_name = Path(s).name
        # 提取智能体数量信息
        if "-2000.scen" in scene_name:
            print(f"  {scene_name} (2000个智能体)")
        elif "-1000.scen" in scene_name:
            print(f"  {scene_name} (1000个智能体)")
        elif "-500.scen" in scene_name:
            print(f"  {scene_name} (500个智能体)")
        elif "-10.scen" in scene_name:
            print(f"  {scene_name} (10个智能体)")
        elif "-5.scen" in scene_name:
            print(f"  {scene_name} (5个智能体)")
        else:
            print(f"  {scene_name}")

if __name__ == "__main__":
    main()