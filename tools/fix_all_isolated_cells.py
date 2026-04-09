#!/usr/bin/env python3
"""
修复所有场景文件中的孤立单元格问题
"""

import random
import os
from pathlib import Path

ASSETS_DIR = Path("/home/sy/Homework/LaCAM/lacam0/assets")

def find_isolated_cells(map_file):
    """找出地图中的所有孤立单元格"""
    map_path = ASSETS_DIR / map_file
    if not map_path.exists():
        return set()
    
    with open(map_path, 'r') as f:
        lines = f.readlines()
    
    height = int(lines[1].split()[1])
    width = int(lines[2].split()[1])
    map_data = [list(line.strip()) for line in lines[4:4+height]]
    
    isolated_cells = set()
    for y in range(height):
        for x in range(width):
            if map_data[y][x] == '.':
                # 检查是否孤立（四周都是障碍物）
                isolated = True
                for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if map_data[ny][nx] == '.':
                            isolated = False
                            break
                
                if isolated:
                    isolated_cells.add((x, y))
    
    return isolated_cells, width, height, map_data

def get_passable_non_isolated(map_data, isolated_cells):
    """获取所有非孤立的可通行位置"""
    height = len(map_data)
    width = len(map_data[0]) if height > 0 else 0
    
    passable_cells = []
    for y in range(height):
        for x in range(width):
            if map_data[y][x] == '.' and (x, y) not in isolated_cells:
                passable_cells.append((x, y))
    
    return passable_cells

def fix_scenario_file(scen_file, map_file):
    """修复场景文件中的孤立单元格问题"""
    scen_path = ASSETS_DIR / scen_file
    if not scen_path.exists():
        print(f"  ❌ 场景文件不存在: {scen_file}")
        return False
    
    # 获取孤立单元格信息
    isolated_cells, width, height, map_data = find_isolated_cells(map_file)
    if not isolated_cells:
        print(f"  ✅ 地图没有孤立单元格")
        return True
    
    print(f"  地图孤立单元格: {len(isolated_cells)} 个")
    
    # 获取非孤立可通行位置
    passable_cells = get_passable_non_isolated(map_data, isolated_cells)
    if len(passable_cells) < 2:
        print(f"  ❌ 非孤立可通行位置不足")
        return False
    
    # 读取场景文件
    with open(scen_path, 'r') as f:
        scen_lines = f.readlines()
    
    # 检查需要修复的行
    lines_to_fix = []
    for i, line in enumerate(scen_lines[1:], 1):
        parts = line.strip().split('\t')
        if len(parts) >= 8:
            start_x, start_y = int(parts[4]), int(parts[5])
            goal_x, goal_y = int(parts[6]), int(parts[7])
            
            if (start_x, start_y) in isolated_cells or (goal_x, goal_y) in isolated_cells:
                lines_to_fix.append(i)
    
    if not lines_to_fix:
        print(f"  ✅ 场景文件没有使用孤立单元格")
        return True
    
    print(f"  需要修复的行数: {len(lines_to_fix)}")
    
    # 创建修复后的文件
    random.seed(42)
    fixed_lines = [scen_lines[0]]  # 保留version行
    
    for i, line in enumerate(scen_lines[1:], 1):
        if i in lines_to_fix:
            # 替换为新的非孤立位置
            start_idx = random.randint(0, len(passable_cells)-1)
            goal_idx = random.randint(0, len(passable_cells)-1)
            
            start_x, start_y = passable_cells[start_idx]
            goal_x, goal_y = passable_cells[goal_idx]
            
            distance = abs(goal_x - start_x) + abs(goal_y - start_y)
            if distance == 0:
                distance = 1.0
            
            fixed_line = f"{i}\t{map_file}\t{width}\t{height}\t{start_x}\t{start_y}\t{goal_x}\t{goal_y}\t{distance:.1f}"
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    
    # 备份原始文件
    backup_path = ASSETS_DIR / (scen_file + '.bak')
    import shutil
    shutil.copy2(scen_path, backup_path)
    
    # 保存修复后的文件
    with open(scen_path, 'w') as f:
        f.writelines(fixed_lines)
    
    print(f"  ✅ 修复完成，原始文件备份为: {backup_path.name}")
    return True

def main():
    """主函数"""
    print("🛠️ 修复所有场景文件的孤立单元格问题")
    print("=" * 60)
    
    # 需要检查的文件列表
    files_to_check = [
        ("random-48-48-20-200.scen", "random-48-48-20.map"),
        ("random-48-48-20-1000.scen", "random-48-48-20.map"),
        ("random-64-64-15-500.scen", "random-64-64-15.map"),
        ("random-64-64-15-2000.scen", "random-64-64-15.map"),
        ("open-48-48-300.scen", "open-48-48.map"),
        ("open-48-48-1500.scen", "open-48-48.map"),
        ("random-16-16-10-30.scen", "random-16-16-10.map"),
        ("random-16-16-10-100.scen", "random-16-16-10.map"),
        ("narrow-corridor-16-16-5.scen", "narrow-corridor-16-16.map"),
        ("narrow-corridor-16-16-10.scen", "narrow-corridor-16-16.map"),
        ("empty-8-8-test.scen", "empty-8-8.map"),
    ]
    
    fixed_count = 0
    for scen_file, map_file in files_to_check:
        print(f"\n📄 检查: {scen_file} → {map_file}")
        print("-" * 40)
        
        if fix_scenario_file(scen_file, map_file):
            fixed_count += 1
    
    print("\n" + "=" * 60)
    print(f"🎉 修复完成! 检查了 {len(files_to_check)} 个文件")
    print(f"✅ 修复了 {fixed_count} 个文件的孤立单元格问题")
    
    # 测试修复后的文件
    print("\n🧪 快速测试修复效果...")
    test_files = [
        ("random-48-48-20-200.scen", "random-48-48-20.map", 158),
        ("random-48-48-20-1000.scen", "random-48-48-20.map", 200),
    ]
    
    import subprocess
    for scen_file, map_file, n in test_files:
        print(f"\n测试 {scen_file} (N={n}): ", end='', flush=True)
        try:
            result = subprocess.run(
                ['./run_lacam', '-s', scen_file, '-m', map_file, '-N', str(n), '-v', '0', '-t', '3'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if '✅ LaCAM 运行完成!' in result.stdout:
                print('✅ 成功')
            elif '段错误' in result.stdout:
                print('❌ 段错误')
            else:
                print(f'❓ 其他')
        except:
            print('⏱️  超时')

if __name__ == "__main__":
    main()