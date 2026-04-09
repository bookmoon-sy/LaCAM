#!/usr/bin/env python3
"""
LaCAM 图形化界面程序
功能：在窗口中修改参数，点击启动后运行仿真并显示结果
"""

import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path

# 项目路径
PROJECT_DIR = Path("/home/sy/Homework/LaCAM")
LACAM_DIR = PROJECT_DIR / "lacam0"

class LaCAMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LaCAM 可视化控制面板")
        self.root.geometry("900x700")
        
        # 设置图标和样式
        self.root.configure(bg="#f0f0f0")
        
        # 创建主框架
        self.create_widgets()
        
        # 当前运行状态
        self.running = False
        self.process = None
        
        # 初始化时刷新文件列表
        self.root.after(100, self.refresh_file_lists)
        
    def create_widgets(self):
        """创建所有界面组件"""
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # ========== 标题 ==========
        title_label = ttk.Label(
            main_frame,
            text="LaCAM 多智能体路径规划仿真",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # ========== 参数设置区域 ==========
        params_frame = ttk.LabelFrame(main_frame, text="参数设置", padding="10")
        params_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        params_frame.columnconfigure(1, weight=1)
        
        # 行计数器
        row = 0
        
        # 场景文件选择
        ttk.Label(params_frame, text="场景文件:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.scenario_var = tk.StringVar(value="random-32-32-10-random-1.scen")
        self.scenario_combo = ttk.Combobox(
            params_frame,
            textvariable=self.scenario_var,
            width=45,  # 增加宽度以显示完整文件名
            state="readonly"
        )
        self.scenario_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        # 绑定选择事件，自动匹配地图
        self.scenario_combo.bind("<<ComboboxSelected>>", self.on_scenario_selected)
        row += 1
        
        # 地图文件选择
        ttk.Label(params_frame, text="地图文件:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.map_var = tk.StringVar(value="random-32-32-10.map")
        self.map_combo = ttk.Combobox(
            params_frame,
            textvariable=self.map_var,
            width=40,
            state="readonly"
        )
        self.map_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        row += 1
        
        # 智能体数量
        ttk.Label(params_frame, text="智能体数量:").grid(row=row, column=0, sticky=tk.W, pady=5)
        agents_frame = ttk.Frame(params_frame)
        agents_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        self.agents_var = tk.IntVar(value=400)
        self.agents_scale = ttk.Scale(
            agents_frame,
            from_=1,
            to=461,
            variable=self.agents_var,
            orient=tk.HORIZONTAL,
            length=300
        )
        self.agents_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.agents_label = ttk.Label(agents_frame, text="400", width=5)
        self.agents_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 绑定滑块事件
        self.agents_scale.configure(command=self.update_agents_label)
        row += 1
        
        # 详细程度
        ttk.Label(params_frame, text="详细程度:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.verbose_var = tk.IntVar(value=1)
        verbose_frame = ttk.Frame(params_frame)
        verbose_frame.grid(row=row, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        for i in range(4):
            rb = ttk.Radiobutton(
                verbose_frame,
                text=f"等级 {i}",
                variable=self.verbose_var,
                value=i
            )
            rb.pack(side=tk.LEFT, padx=(0, 10))
        row += 1
        
        # 随机种子
        ttk.Label(params_frame, text="随机种子:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.seed_var = tk.StringVar(value="0")
        ttk.Entry(
            params_frame,
            textvariable=self.seed_var,
            width=20
        ).grid(row=row, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        row += 1
        
        # 时间限制
        ttk.Label(params_frame, text="时间限制(秒):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.time_limit_var = tk.StringVar(value="3")
        ttk.Entry(
            params_frame,
            textvariable=self.time_limit_var,
            width=20
        ).grid(row=row, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        row += 1
        
        # 高级选项框架
        advanced_frame = ttk.LabelFrame(params_frame, text="高级选项", padding="10")
        advanced_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        advanced_frame.columnconfigure(1, weight=1)
        
        adv_row = 0
        
        # 实时优化
        self.anytime_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            advanced_frame,
            text="启用实时优化（树重连）",
            variable=self.anytime_var
        ).grid(row=adv_row, column=0, columnspan=2, sticky=tk.W, pady=2)
        adv_row += 1
        
        # 禁用PIBT交换
        self.no_swap_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            advanced_frame,
            text="禁用PIBT交换",
            variable=self.no_swap_var
        ).grid(row=adv_row, column=0, columnspan=2, sticky=tk.W, pady=2)
        adv_row += 1
        
        # 禁用PIBT阻碍
        self.no_hindrance_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            advanced_frame,
            text="禁用PIBT阻碍",
            variable=self.no_hindrance_var
        ).grid(row=adv_row, column=0, columnspan=2, sticky=tk.W, pady=2)
        adv_row += 1
        
        # ========== 控制按钮区域 ==========
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=3, pady=(10, 10))
        
        # 刷新文件列表按钮
        ttk.Button(
            buttons_frame,
            text="刷新文件列表",
            command=self.refresh_file_lists,
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 显示命令按钮
        ttk.Button(
            buttons_frame,
            text="显示命令",
            command=self.show_command,
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 启动按钮
        self.start_button = ttk.Button(
            buttons_frame,
            text="▶ 启动仿真",
            command=self.start_simulation,
            width=15,
            style="Accent.TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 停止按钮
        self.stop_button = ttk.Button(
            buttons_frame,
            text="■ 停止",
            command=self.stop_simulation,
            width=15,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 帮助按钮
        ttk.Button(
            buttons_frame,
            text="❓ 帮助",
            command=self.show_help,
            width=15
        ).pack(side=tk.LEFT)
        
        # ========== 输出显示区域 ==========
        output_frame = ttk.LabelFrame(main_frame, text="仿真输出", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # 输出文本框（修复中文显示问题）
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            width=80,
            height=15,
            font=("WenQuanYi Micro Hei Mono", 11),  # 使用支持中文的等宽字体
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="white",
            relief=tk.FLAT,
            borderwidth=2,
            padx=5,
            pady=5
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置主框架行权重
        main_frame.rowconfigure(3, weight=1)
        
        # ========== 状态栏 ==========
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(
            status_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2)
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 初始化文件列表
        self.refresh_file_lists()
        
    def update_agents_label(self, value):
        """更新智能体数量标签"""
        agents = int(float(value))
        self.agents_label.config(text=str(agents))
        
    def refresh_file_lists(self):
        """刷新场景和地图文件列表"""
        try:
            assets_dir = LACAM_DIR / "assets"
            
            # 获取场景文件
            scen_files = sorted([f.name for f in assets_dir.glob("*.scen")])
            if scen_files:
                self.scenario_combo['values'] = scen_files
                if self.scenario_var.get() not in scen_files:
                    self.scenario_var.set(scen_files[0])
                    # 自动匹配地图
                    self.auto_match_map(scen_files[0])
                    # 更新智能体限制
                    self.update_agents_limit(scen_files[0])
            
            # 获取地图文件
            map_files = sorted([f.name for f in assets_dir.glob("*.map")])
            if map_files:
                self.map_combo['values'] = map_files
                if self.map_var.get() not in map_files:
                    self.map_var.set(map_files[0])
                    
            self.status_var.set(f"文件列表已刷新: {len(scen_files)}个场景, {len(map_files)}个地图")
            
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件列表: {str(e)}")
            
    def on_scenario_selected(self, event):
        """场景文件选择事件"""
        selected_scen = self.scenario_var.get()
        self.auto_match_map(selected_scen)
        # 更新智能体数量限制
        self.update_agents_limit(selected_scen)
        
    def auto_match_map(self, scenario_file):
        """自动匹配地图文件"""
        matched_map = None
        
        # 首先尝试从场景文件内容读取地图名
        try:
            scen_path = LACAM_DIR / "assets" / scenario_file
            with open(scen_path, 'r') as f:
                first_line = f.readline()
                if first_line.startswith("version"):
                    second_line = f.readline()
                    if second_line:
                        parts = second_line.split("\t")
                        if len(parts) >= 2:
                            matched_map = parts[1]
        except:
            pass  # 如果无法读取，使用文件名匹配
        
        # 如果从内容无法获取，使用文件名匹配
        if not matched_map:
            # 常见地图文件名模式匹配
            if "empty-8-8" in scenario_file:
                matched_map = "empty-8-8.map"
            elif "random-16-16-10" in scenario_file:
                matched_map = "random-16-16-10.map"
            elif "random-32-32-10" in scenario_file:
                matched_map = "random-32-32-10.map"
            elif "random-48-48-20" in scenario_file:
                matched_map = "random-48-48-20.map"
            elif "random-64-64-15" in scenario_file:
                matched_map = "random-64-64-15.map"
            elif "narrow-corridor-16-16" in scenario_file:
                matched_map = "narrow-corridor-16-16.map"
            elif "maze-24-24" in scenario_file:
                matched_map = "maze-24-24.map"
            elif "open-48-48" in scenario_file:
                matched_map = "open-48-48.map"
            else:
                # 尝试通用匹配：提取地图名前缀
                for map_file in self.map_combo['values']:
                    if map_file.replace('.map', '') in scenario_file:
                        matched_map = map_file
                        break
        
        # 检查地图文件是否存在
        if matched_map:
            map_path = LACAM_DIR / "assets" / matched_map
            if map_path.exists() and matched_map in self.map_combo['values']:
                self.map_var.set(matched_map)
                self.status_var.set(f"已自动匹配: {scenario_file} → {matched_map}")
                return True
        
        # 如果无法匹配，使用第一个可用地图
        if self.map_combo['values']:
            self.map_var.set(self.map_combo['values'][0])
            self.status_var.set(f"⚠️ 无法自动匹配地图，使用: {self.map_combo['values'][0]}")
        
        return False
            
    def update_agents_limit(self, scenario_file):
        """根据场景文件更新智能体数量限制"""
        try:
            scen_path = LACAM_DIR / "assets" / scenario_file
            with open(scen_path, 'r') as f:
                lines = f.readlines()
                
            # 场景文件格式: 第一行是"version 1"，后面每行一个智能体
            max_agents = len(lines) - 1  # 减去version行
            
            if max_agents > 0:
                # 更新滑块范围
                self.agents_scale.configure(to=max_agents)
                
                # 如果当前值超过限制，调整为最大值
                current_value = self.agents_var.get()
                if current_value > max_agents:
                    self.agents_var.set(max_agents)
                    self.agents_label.config(text=str(max_agents))
                
                # 更新状态提示（显示文件名和智能体数量）
                self.status_var.set(f"{scenario_file}: 最多 {max_agents} 个智能体")
                
                return max_agents
            else:
                self.status_var.set(f"{scenario_file}: 文件格式错误")
                return 0
            
        except Exception as e:
            # 如果无法读取，使用默认值461
            self.agents_scale.configure(to=461)
            self.status_var.set(f"无法读取 {scenario_file}，使用默认限制: 461")
            return 461
            
    def show_command(self):
        """显示将要运行的命令"""
        cmd = self.build_command()
        messagebox.showinfo("运行命令", f"将要运行的命令:\n\n{cmd}")
        
    def build_command(self):
        """构建运行命令"""
        cmd_parts = [
            str(PROJECT_DIR / "run_lacam"),
            "-s", self.scenario_var.get(),
            "-m", self.map_var.get(),
            "-N", str(self.agents_var.get()),
            "-v", str(self.verbose_var.get()),
            "--seed", self.seed_var.get(),
            "-t", self.time_limit_var.get()
        ]
        
        if self.anytime_var.get():
            cmd_parts.append("--anytime")
        if self.no_swap_var.get():
            cmd_parts.append("--no-pibt-swap")
        if self.no_hindrance_var.get():
            cmd_parts.append("--no-pibt-hindrance")
            
        return " ".join(cmd_parts)
        
    def start_simulation(self):
        """启动仿真"""
        if self.running:
            messagebox.showwarning("警告", "仿真已经在运行中")
            return
            
        # 检查程序是否存在
        if not (LACAM_DIR / "build" / "main").exists():
            messagebox.showerror("错误", "找不到LaCAM可执行文件\n请先编译: cd lacam0 && make -C build -j4")
            return
            
        # 更新界面状态
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set("仿真运行中...")
        
        # 清空输出并显示简洁信息
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "🚀 LaCAM 仿真开始\n")
        self.output_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # 构建命令
        cmd = self.build_command()
        self.output_text.insert(tk.END, f"📝 运行命令: {cmd}\n\n")
        self.output_text.insert(tk.END, "⏳ 正在运行，请稍候...\n")
        self.output_text.insert(tk.END, "=" * 40 + "\n\n")
        self.output_text.see(tk.END)
        
        # 在新线程中运行仿真
        self.simulation_thread = threading.Thread(target=self.run_simulation, args=(cmd,))
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
        
    def run_simulation(self, cmd):
        """运行仿真（在后台线程中）"""
        try:
            # 运行命令
            self.process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # 实时读取输出
            for line in iter(self.process.stdout.readline, ''):
                if not line:
                    break
                    
                # 在主线程中更新输出
                self.root.after(0, self.append_output, line)
                
            # 等待进程结束
            self.process.wait()
            
            # 在主线程中更新状态
            self.root.after(0, self.simulation_finished, self.process.returncode)
            
        except Exception as e:
            self.root.after(0, self.append_output, f"\n错误: {str(e)}\n")
            self.root.after(0, self.simulation_finished, 1)
            
    def append_output(self, text):
        """添加输出到文本框"""
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        
    def simulation_finished(self, returncode):
        """仿真完成"""
        self.running = False
        self.process = None
        
        # 更新界面状态
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        if returncode == 0:
            self.status_var.set("仿真完成 ✓")
            
            # 显示简洁的结果
            self.append_output("\n" + "=" * 60 + "\n")
            self.append_output("✅ 仿真成功完成\n")
            
            # 只显示结果文件保存路径
            result_file = LACAM_DIR / "build" / "result.txt"
            if result_file.exists():
                result_path = str(result_file.absolute())
                self.append_output(f"📁 结果文件已保存至:\n")
                self.append_output(f"{result_path}\n\n")
                
                # 可选：显示文件大小
                file_size = result_file.stat().st_size
                self.append_output(f"📄 文件大小: {file_size} 字节\n")
                
                # 显示关键指标（可选，简洁版）
                try:
                    with open(result_file, 'r') as f:
                        first_line = f.readline().strip()
                        if first_line:
                            # 提取关键信息
                            if "耗时:" in first_line:
                                parts = first_line.split("\t")
                                time_info = parts[0] if parts else first_line
                                self.append_output(f"⏱️  {time_info}\n")
                except:
                    pass
            else:
                self.append_output("⚠️ 未找到结果文件\n")
        else:
            self.status_var.set(f"仿真失败 (代码: {returncode})")
            self.append_output(f"\n仿真失败，返回代码: {returncode}\n")
            
    def stop_simulation(self):
        """停止仿真"""
        if self.running and self.process:
            self.process.terminate()
            self.append_output("\n仿真已被用户终止\n")
            self.status_var.set("仿真已终止")
            
    def show_help(self):
        """显示帮助信息"""
        help_window = tk.Toplevel(self.root)
        help_window.title("LaCAM 使用帮助")
        help_window.geometry("800x600")
        help_window.configure(bg="#f0f0f0")
        
        # 创建主框架
        main_frame = ttk.Frame(help_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建带滚动条的文本框
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text = scrolledtext.ScrolledText(
            text_frame,
            width=80,
            height=25,
            font=("WenQuanYi Micro Hei", 11),
            bg="white",
            fg="black",
            wrap=tk.WORD
        )
        help_text.pack(fill=tk.BOTH, expand=True)
        
        # 帮助内容
        help_content = """🎯 LaCAM 使用帮助
========================================

📋 参数说明

1. 场景文件 (Scenario File) 🆚 地图文件 (Map File)

   🔹 地图文件 (.map):
   • 定义环境的静态结构
   • 包含: 地图尺寸、障碍物位置、可通行区域
   • 特点: 一个地图可以被多个场景使用
   • 示例: random-32-32-10.map (32×32, 10%障碍物)

   🔹 场景文件 (.scen):
   • 定义具体任务
   • 包含: 智能体起始位置、目标位置、智能体数量
   • 特点: 一个场景对应一个特定地图
   • 示例: random-32-32-10-random-1.scen

   🔗 匹配关系:
   • empty-8-8-test.scen → empty-8-8.map
   • random-32-32-10-random-*.scen → random-32-32-10.map

   💡 使用提示:
   • GUI会自动匹配场景对应的地图
   • 也可以手动选择不同的地图（但必须匹配）
   • 不匹配会导致仿真失败

3. 智能体数量 (Agents)
   • 要规划的智能体数量
   • 范围: 1-N（N由场景文件决定）
   • 自动限制: GUI会根据场景文件自动调整最大值
   • 场景文件容量:
     - random-32-32-10-random-*.scen: 461个智能体
     - empty-8-8-test.scen: 10个智能体
   • 错误提示: 如果超过限制会显示 "invalid N, check instance"

4. 详细程度 (Verbose Level)
   • 0: 最少输出，只显示最终结果
   • 1: 基本输出，显示关键步骤（默认）
   • 2: 更多细节，显示规划过程
   • 3: 最详细输出，包含实时进度

5. 随机种子 (Random Seed)
   • 用于确保结果可复现
   • 相同种子 + 相同参数 = 相同结果
   • 默认: 0

6. 时间限制 (Time Limit)
   • 规划的时间限制（秒）
   • 默认: 3秒
   • 建议: 简单场景1-3秒，复杂场景5-10秒

7. 高级选项
   • 实时优化 (Anytime): 在规划过程中持续优化结果
   • 禁用PIBT交换: 禁用智能体之间的交换操作
   • 禁用PIBT阻碍: 禁用阻碍处理算法

📊 输出结果解读

仿真完成后，结果保存在:
   lacam0/build/result.txt

结果文件包含以下关键指标:

1. 耗时 (Elapsed Time)
   • 总运行时间（包括I/O）
   • 示例: 耗时: 25ms

2. 计算时间 (Computation Time)
   • 纯计算时间（不包括I/O）
   • 示例: 计算时间(毫秒): 14

3. 最大步数 (Makespan)
   • 所有智能体完成所需的最大步数
   • 示例: 最大步数: 58
   • 下界/上界: 理论最优值和当前解的质量比

4. 总成本 (Sum of Costs, SOC)
   • 所有智能体移动的总成本
   • 示例: 总成本: 16993
   • 下界: 理论最优成本 (SOC_LB)
   • 上界: 当前解与最优解的比率

5. 总损失 (Sum of Loss)
   • 与最优解的差距
   • 示例: 总损失: 14829
   • 下界: 理论最小损失

6. 已解决 (Solved)
   • 1: 成功找到解
   • 0: 未找到解（超时或失败）

7. 随机种子 (Seed)
   • 使用的随机种子值

8. 起始位置 (Starts)
   • 所有智能体的起始坐标列表

🚀 使用建议

1. 首次使用
   • 使用默认参数运行测试
   • 查看结果文件了解输出格式

2. 参数调试
   • 从少量智能体开始（如50）
   • 逐步增加数量测试性能
   • 使用固定种子确保可复现

3. 性能优化
   • 批量测试时使用详细程度0
   • 复杂场景增加时间限制
   • 内存不足时减少智能体数量

4. 结果分析
   • 对比不同参数的结果
   • 关注总成本和最大步数
   • 检查是否成功解决（solved=1）

🔧 故障排除

1. 找不到可执行文件
   • 运行: cd lacam0 && make -C build -j4

2. 智能体数量超限
   • 错误: invalid N, check instance
   • 解决: 减少智能体数量（最大461）

3. 内存不足
   • 错误: 段错误 (核心已转储)
   • 解决: 减少智能体数量

4. 运行时间太长
   • 解决: 减少时间限制或智能体数量

📞 更多帮助

• 命令行帮助: ./run_lacam --help
• 参数解释: ./run_lacam --explain
• 文件列表: ./run_lacam --list-files
• 查看本帮助: 点击"❓ 帮助"按钮
"""
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)  # 设置为只读
        
        # 关闭按钮
        close_button = ttk.Button(
            main_frame,
            text="关闭帮助",
            command=help_window.destroy
        )
        close_button.pack(pady=(10, 0))
        
        # 让帮助窗口获得焦点
        help_window.focus_set()
        help_window.grab_set()
            
def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置样式
    style = ttk.Style()
    style.theme_use('clam')
    
    # 创建主窗口
    app = LaCAMGUI(root)
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()