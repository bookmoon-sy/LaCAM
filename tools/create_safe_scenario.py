#!/usr/bin/env python3
"""
创建安全的场景文件，确保：
1. 起始位置唯一
2. 位置在可通行区域
3. 坐标在地图范围内
"""

import random
import os
from pathlib import Path

ASSETS_DIR = Path("/home/sy/Homework/LaCAM/lacam0/assets")

def get_passable_positions(map_file):
    """获取地图中所有可通行位置"""
    map_path = ASSETS_DIR / map_file
    if not map_path.exists():
        raise FileNotFoundError(f"地图文件不存在: {map_file}")
    
    with open(map_path, 'r') as f:
        lines = f.readlines()
    
    # 解析地图尺寸
    height = int(lines[1].split()[1])
    width = int(lines[2].split()[1])
    
    # 获取地图数据
    map_data = lines[4:4+height]
    
    # 收集所有可通行位置
    passable_positions = []
    for y in range(height):
        row = map_data[y].strip()
        if len(row) != width:
            print(f"警告: 第{y+4}行长度({len(row)}) != 宽度({width})")
            continue
            
        for x in range(width):
            if row[x] == '.':  # 可通行
                passable_positions.append((x, y))
    
    print(f"地图 {map_file}: {width}x{height}, 可通行位置: {len(passable_positions)}")
    return passable_positions, width, height

def create_safe_scenario(map_file, num_agents, output_file):
    """创建安全的场景文件"""
    
    # 获取可通行位置
    passable_positions, width, height = get_passable_positions(map_file)
    
    if len(passable_positions) < num_agents * 2:
        print(f"警告: 可通行位置不足，需要{num_agents*2}，实际{len(passable_positions)}")
        num_agents = min(num_agents, len(passable_positions) // 2)
        print(f"调整为: {num_agents} 个智能体")
    
    # 随机选择起始和目标位置
    random.seed(42)  # 固定种子确保可复现
    selected_indices = random.sample(range(len(passable_positions)), num_agents * 2)
    
    # 生成场景文件
    scenario_lines = ["version 1"]
    
    for i in range(num_agents):
        start_idx = selected_indices[i * 2]
        goal_idx = selected_indices[i * 2 + 1]
        
        start_x, start_y = passable_positions[start_idx]
        goal_x, goal_y = passable_positions[goal_idx]
        
        # 计算曼哈顿距离
        distance = abs(goal_x - start_x) + abs(goal_y - start_y)
        if distance == 0:
            distance = 1.0
        
        scenario_lines.append(
            f"{i+1}\t{map_file}\t{width}\t{height}\t"
            f"{start_x}\t{start_y}\t{goal_x}\t{goal_y}\t{distance:.1f}"
        )
    
    # 保存文件
    output_path = ASSETS_DIR / output_file
    with open(output_path, 'w') as f:
        f.write('\n'.join(scenario_lines))
    
    print(f"✅ 创建安全场景文件: {output_file} ({num_agents}个智能体)")
    
    # 验证文件
    verify_scenario(output_file, map_file)
    
    return output_path

def verify_scenario(scen_file, map_file):
    """验证场景文件"""
    scen_path = ASSETS_DIR / scen_file
    map_path = ASSETS_DIR / map_file
    
    with open(scen_path, 'r') as f:
        lines = f.readlines()
    
    print(f"\n🔍 验证 {scen_file}:")
    print(f"  总行数: {len(lines)}")
    print(f"  智能体数量: {len(lines) - 1}")
    
    # 检查起始位置唯一性
    start_positions = set()
    duplicate_count = 0
    
    for i, line in enumerate(lines[1:], 1):
        parts = line.strip().split('\t')
        if len(parts) >= 6:
            try:
                start_x, start_y = int(parts[4]), int(parts[5])
                pos = (start_x, start_y)
                if pos in start_positions:
                    duplicate_count += 1
                else:
                    start_positions.add(pos)
            except:
                pass
    
    print(f"  唯一起始位置: {len(start_positions)}")
    if duplicate_count > 0:
        print(f"  ❌ 重复起始位置: {duplicate_count}")
    else:
        print(f"  ✅ 起始位置唯一")
    
    # 检查坐标范围
    with open(map_path, 'r') as f:
        map_lines = f.readlines()
    
    map_height = int(map_lines[1].split()[1])
    map_width = int(map_lines[2].split()[1])
    
    out_of_bounds = 0
    for i, line in enumerate(lines[1:], 1):
        parts = line.strip().split('\t')
        if len(parts) >= 8:
            try:
                start_x, start_y = int(parts[4]), int(parts[5])
                goal_x, goal_y = int(parts[6]), int(parts[7])
                
                if (start_x < 0 or start_x >= map_width or 
                    start_y < 0 or start_y >= map_height):
                    out_of_bounds += 1
                
                if (goal_x < 0 or goal_x >= map_width or 
                    goal_y < 0 or goal_y >= map_height):
                    out_of_bounds += 1
            except:
                pass
    
    print(f"  超出边界坐标: {out_of_bounds}")
    if out_of_bounds > 0:
        print(f"  ❌ 有坐标超出地图边界")
    else:
        print(f"  ✅ 所有坐标在地图范围内")

def main():
    """主函数"""
    print("🛡️ 创建安全的场景文件")
    print("=" * 50)
    
    # 修复有问题的文件
    problems = [
        ("maze-24-24.map", 50, "maze-24-24-50.scen"),
        ("random-48-48-20.map", 1000, "random-48-48-20-1000.scen"),
    ]
    
    for map_file, agents, scen_file in problems:
        print(f"\n🔄 修复: {scen_file}")
        print("-" * 30)
        
        # 删除旧文件
        old_path = ASSETS_DIR / scen_file
        if old_path.exists():
            os.remove(old_path)
            print(f"已删除旧文件: {scen_file}")
        
        # 创建新文件
        create_safe_scenario(map_file, agents, scen_file)
    
    print("\n" + "=" * 50)
    print("🎉 安全场景文件创建完成!")
    print("\n🚀 现在可以安全使用这些文件了")

if __name__ == "__main__":
    main()