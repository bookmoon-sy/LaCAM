#!/usr/bin/env python3
"""
MAPF Visualizer 控制器 - 最简单版
确保每个中文字符都能完整显示
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
import sys
import threading

class MAPFVisualizerController:
    def __init__(self, root):
        self.root = root
        self.root.title("MAPF Visualizer 控制器")
        
        # 设置窗口尺寸 - 更大一些确保每个字都能完整显示
        self.root.geometry("800x900")
        self.root.minsize(750, 850)
        
        # 当前运行的进程
        self.current_process = None
        
        # 创建界面
        self.create_widgets()
        
        # 检查mapf-visualizer是否存在
        self.check_visualizer()
        
    def check_visualizer(self):
        """检查mapf-visualizer程序"""
        visualizer_path = os.path.join("mapf-visualizer", "bin", "mapf-visualizer")
        
        if os.path.exists(visualizer_path):
            self.status_var.set(f"✅ MAPF Visualizer 可用")
            self.visualizer_available = True
            self.visualizer_path = visualizer_path
        else:
            self.status_var.set("❌ 错误: 找不到 mapf-visualizer 可执行文件")
            self.visualizer_available = False
            self.run_button.config(state='disabled')
            self.run_example_button.config(state='disabled')
    
    def create_widgets(self):
        """创建界面组件"""
        
        # 创建主容器
        main_container = ttk.Frame(self.root, padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_container, text="MAPF Visualizer 控制器", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # 文件选择框架
        file_frame = ttk.LabelFrame(main_container, text="文件选择", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 12))
        
        # 地图文件
        map_frame = ttk.Frame(file_frame)
        map_frame.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(map_frame, text="地图文件 (.map):", width=14).pack(side=tk.LEFT, padx=(0, 8))
        self.map_file_var = tk.StringVar()
        map_entry = ttk.Entry(map_frame, textvariable=self.map_file_var)
        map_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        ttk.Button(map_frame, text="浏览...", command=self.browse_map_file, width=10).pack(side=tk.LEFT)
        
        # 解决方案文件
        solution_frame = ttk.Frame(file_frame)
        solution_frame.pack(fill=tk.X)
        
        ttk.Label(solution_frame, text="解决方案文件 (.txt):", width=14).pack(side=tk.LEFT, padx=(0, 8))
        self.solution_file_var = tk.StringVar()
        solution_entry = ttk.Entry(solution_frame, textvariable=self.solution_file_var)
        solution_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        ttk.Button(solution_frame, text="浏览...", command=self.browse_solution_file, width=10).pack(side=tk.LEFT)
        
        # 快速示例框架
        example_frame = ttk.LabelFrame(main_container, text="快速示例", padding=10)
        example_frame.pack(fill=tk.X, pady=(0, 12))
        
        example_inner_frame = ttk.Frame(example_frame)
        example_inner_frame.pack(fill=tk.X)
        
        # 示例文件列表
        self.example_var = tk.StringVar()
        example_combo = ttk.Combobox(example_inner_frame, textvariable=self.example_var, 
                                    state="readonly")
        example_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        # 加载示例文件
        self.load_examples()
        example_combo['values'] = list(self.examples.keys())
        if self.examples:
            example_combo.current(0)
            self.example_var.set(list(self.examples.keys())[0])
        
        ttk.Button(example_inner_frame, text="使用此示例", 
                  command=self.use_selected_example, width=12).pack(side=tk.LEFT)
        
        # 控制按钮框架
        control_frame = ttk.Frame(main_container)
        control_frame.pack(pady=(0, 15))
        
        # 第一行按钮
        button_row1 = ttk.Frame(control_frame)
        button_row1.pack(pady=(0, 8))
        
        self.run_button = ttk.Button(button_row1, text="🚀 启动 MAPF Visualizer", 
                                    command=self.run_visualizer, width=24)
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.run_example_button = ttk.Button(button_row1, text="📁 运行默认示例", 
                                           command=self.run_default_example, width=24)
        self.run_example_button.pack(side=tk.LEFT)
        
        # 第二行按钮
        button_row2 = ttk.Frame(control_frame)
        button_row2.pack()
        
        self.stop_button = ttk.Button(button_row2, text="⏹️ 停止可视化", 
                                     command=self.stop_visualizer, width=50, state='disabled')
        self.stop_button.pack()
        
        # 控制键说明框架 - 使用更大的宽度和字体
        keys_frame = ttk.LabelFrame(main_container, text="MAPF Visualizer 控制键说明", padding=12)
        keys_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        
        # 创建Text组件 - 使用更大的宽度和字体
        keys_text = """═══════════════════════════════════════════════════════════════════
基本控制:
  p         播放/暂停
  l         循环/不循环
  r         重置
  ESC       退出

显示控制:
  v         显示到目标的虚拟线
  f         显示智能体 & 节点ID
  g         显示目标
  G         显示/隐藏网格

导航控制:
  →         前进一个时间步
  ←         后退一个时间步
  ↑         加速动画
  ↓         减速动画

视图控制:
  i         放大
  o         缩小
  空格       截图（保存到桌面）

其他功能:
  鼠标拖动   平移视图
  鼠标滚轮   缩放视图
═══════════════════════════════════════════════════════════════════"""
        
        # 创建Frame来包装Text组件
        text_frame = ttk.Frame(keys_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建Text组件 - 使用更大的宽度和字体
        keys_display = tk.Text(text_frame, wrap=tk.NONE,  # 不自动换行
                              font=('Courier', 12),  # 更大的字体
                              bg='white', relief=tk.FLAT,
                              padx=15, pady=15,  # 更大的内边距
                              height=18,  # 更多行
                              width=70)   # 更大的宽度，确保每个字都能完整显示
        
        keys_display.insert(tk.END, keys_text)
        keys_display.config(state=tk.DISABLED)  # 设置为只读
        
        # 添加水平滚动条
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=keys_display.xview)
        keys_display.configure(xscrollcommand=h_scrollbar.set)
        
        # 布局
        keys_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_container, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, padding=(10, 5))
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # 添加一些提示文本
        tip_label = ttk.Label(main_container, 
                             text="提示: 选择文件后点击'启动 MAPF Visualizer'，控制键在可视化窗口中有效",
                             font=('Arial', 10), foreground='gray')
        tip_label.pack(pady=(5, 0))
    
    def load_examples(self):
        """加载示例文件"""
        self.examples = {}
        
        # 检查mapf-visualizer的assets目录
        assets_dir = os.path.join("mapf-visualizer", "assets")
        
        if os.path.exists(assets_dir):
            # 查找.map文件
            for file in os.listdir(assets_dir):
                if file.endswith('.map'):
                    map_file = os.path.join(assets_dir, file)
                    # 查找对应的解决方案文件
                    base_name = file[:-4]  # 去掉.map扩展名
                    solution_file = os.path.join(assets_dir, f"demo_{base_name}.txt")
                    
                    if os.path.exists(solution_file):
                        # 读取地图信息
                        try:
                            with open(map_file, 'r') as f:
                                lines = f.readlines()
                            
                            width = 0
                            height = 0
                            for line in lines:
                                if line.startswith('width'):
                                    width = int(line.split()[1])
                                elif line.startswith('height'):
                                    height = int(line.split()[1])
                            
                            display_name = f"{base_name} ({width}x{height})"
                            self.examples[display_name] = (map_file, solution_file)
                        except:
                            self.examples[base_name] = (map_file, solution_file)
        
        # 如果没有找到示例，添加默认示例
        if not self.examples:
            default_map = os.path.join("mapf-visualizer", "assets", "random-32-32-20.map")
            default_solution = os.path.join("mapf-visualizer", "assets", "demo_random-32-32-20.txt")
            
            if os.path.exists(default_map) and os.path.exists(default_solution):
                self.examples["random-32-32-20 (32x32)"] = (default_map, default_solution)
    
    def browse_map_file(self):
        """浏览地图文件"""
        initial_dir = os.path.join("mapf-visualizer", "assets") if os.path.exists(os.path.join("mapf-visualizer", "assets")) else "."
        
        filename = filedialog.askopenfilename(
            title="选择地图文件",
            initialdir=initial_dir,
            filetypes=[("MAP files", "*.map"), ("All files", "*.*")]
        )
        if filename:
            self.map_file_var.set(filename)
    
    def browse_solution_file(self):
        """浏览解决方案文件"""
        initial_dir = os.path.join("mapf-visualizer", "assets") if os.path.exists(os.path.join("mapf-visualizer", "assets")) else "."
        
        filename = filedialog.askopenfilename(
            title="选择解决方案文件",
            initialdir=initial_dir,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.solution_file_var.set(filename)
    
    def use_selected_example(self):
        """使用选中的示例"""
        selected = self.example_var.get()
        if selected in self.examples:
            map_file, solution_file = self.examples[selected]
            self.map_file_var.set(map_file)
            self.solution_file_var.set(solution_file)
            self.status_var.set(f"已选择示例: {selected}")
    
    def run_default_example(self):
        """运行默认示例"""
        if not self.visualizer_available:
            messagebox.showerror("错误", "MAPF Visualizer 不可用")
            return
        
        # 使用默认示例文件
        default_map = os.path.join("mapf-visualizer", "assets", "random-32-32-20.map")
        default_solution = os.path.join("mapf-visualizer", "assets", "demo_random-32-32-20.txt")
        
        if not os.path.exists(default_map):
            messagebox.showerror("错误", f"默认地图文件不存在: {default_map}")
            return
        
        if not os.path.exists(default_solution):
            messagebox.showerror("错误", f"默认解决方案文件不存在: {default_solution}")
            return
        
        self.map_file_var.set(default_map)
        self.solution_file_var.set(default_solution)
        
        # 运行可视化器
        self.run_visualizer()
    
    def run_visualizer(self):
        """运行MAPF Visualizer"""
        if not self.visualizer_available:
            messagebox.showerror("错误", "MAPF Visualizer 不可用")
            return
        
        map_file = self.map_file_var.get()
        solution_file = self.solution_file_var.get()
        
        if not map_file:
            messagebox.showwarning("警告", "请选择地图文件")
            return
        
        if not solution_file:
            messagebox.showwarning("警告", "请选择解决方案文件")
            return
        
        if not os.path.exists(map_file):
            messagebox.showerror("错误", f"地图文件不存在: {map_file}")
            return
        
        if not os.path.exists(solution_file):
            messagebox.showerror("错误", f"解决方案文件不存在: {solution_file}")
            return
        
        # 更新UI状态
        self.run_button.config(state='disabled')
        self.run_example_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_var.set("正在启动 MAPF Visualizer...")
        
        # 在后台线程中运行
        thread = threading.Thread(target=self._run_visualizer_thread, 
                                 args=(map_file, solution_file))
        thread.daemon = True
        thread.start()
    
    def _run_visualizer_thread(self, map_file, solution_file):
        """运行MAPF Visualizer的后台线程"""
        try:
            # 构建命令
            cmd = [self.visualizer_path, map_file, solution_file]
            
            self.root.after(0, lambda: self.status_var.set(f"运行: {os.path.basename(map_file)}"))
            
            # 运行进程
            self.current_process = subprocess.Popen(cmd, 
                                                  stdout=subprocess.PIPE, 
                                                  stderr=subprocess.PIPE)
            
            # 等待进程结束
            stdout, stderr = self.current_process.communicate()
            
            # 检查返回码
            if self.current_process.returncode == 0:
                self.root.after(0, lambda: self.status_var.set("MAPF Visualizer 已退出"))
            elif self.current_process.returncode == -11:  # 段错误
                self.root.after(0, lambda: messagebox.showwarning("警告", 
                    "MAPF Visualizer 段错误。这可能是由于图形驱动或兼容性问题。"))
                self.root.after(0, lambda: self.status_var.set("段错误"))
            else:
                error_msg = stderr.decode('utf-8', errors='ignore') if stderr else "未知错误"
                self.root.after(0, lambda: messagebox.showwarning("警告", 
                    f"MAPF Visualizer 异常退出:\n{error_msg}"))
                self.root.after(0, lambda: self.status_var.set("异常退出"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"运行失败: {str(e)}"))
            self.root.after(0, lambda: self.status_var.set("运行失败"))
        finally:
            self.current_process = None
            self.root.after(0, self.reset_ui)
    
    def stop_visualizer(self):
        """停止MAPF Visualizer"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.status_var.set("正在停止 MAPF Visualizer...")
                
                # 等待进程结束
                def wait_for_stop():
                    try:
                        self.current_process.wait(timeout=2)
                    except:
                        self.current_process.kill()
                    finally:
                        self.current_process = None
                        self.root.after(0, self.reset_ui)
                        self.root.after(0, lambda: self.status_var.set("已停止"))
                
                thread = threading.Thread(target=wait_for_stop)
                thread.daemon = True
                thread.start()
                
            except Exception as e:
                messagebox.showerror("错误", f"停止失败: {str(e)}")
                self.reset_ui()
    
    def reset_ui(self):
        """重置UI状态"""
        self.run_button.config(state='normal')
        self.run_example_button.config(state='normal')
        self.stop_button.config(state='disabled')
        
        if not self.current_process:
            self.status_var.set("就绪")

def main():
    """主函数"""
    root = tk.Tk()
    controller = MAPFVisualizerController(root)
    root.mainloop()

if __name__ == "__main__":
    main()