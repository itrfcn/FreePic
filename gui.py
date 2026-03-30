#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import sys
import webbrowser

# 导入上传功能
from free import upload_file_to_oss, COURSE_URL, COOKIE_STRING, COOKIE_STRING as DEFAULT_COOKIE_STRING

class FileUploadGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("免费图床工具 v1.0")
        self.root.geometry("600x550")
        self.root.resizable(False, True)  # 允许垂直调整大小
        
        # 初始化变量
        self.selected_files = []
        self.cookie_var = tk.StringVar(value=COOKIE_STRING)
        self.course_url_var = tk.StringVar(value=COURSE_URL)
        self.status_var = tk.StringVar(value="就绪")
        self.uploaded_files = []  # 存储所有成功上传的文件信息
        
        # 创建主框架（减少顶部内边距）
        self.main_frame = ttk.Frame(root, padding="1 10 10 10")  # 上 右 下 左
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建界面组件
        self.create_widgets()
        
    def create_widgets(self):
        # 创建标签样式
        style = ttk.Style()
        style.configure("TLabel", font=('Arial', 10))
        style.configure("TButton", font=('Arial', 10))
        
        # 0. 顶部区域（使用教程按钮）
        top_frame = ttk.Frame(self.main_frame, padding="0 0 0 10")  # 上 右 下 左
        top_frame.pack(fill=tk.X, pady=0)
        
        # 使用教程按钮（移除内边距，让按钮更靠近顶部）
        ttk.Button(top_frame, text="使用教程", command=self.open_tutorial_web).pack(side=tk.RIGHT, padx=5, pady=0)
        
        # 1. 文件选择区域
        file_frame = ttk.LabelFrame(self.main_frame, text="文件选择", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="选择文件：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        # 创建一个显示区域用于显示选中的文件
        self.file_list_frame = ttk.Frame(file_frame)
        self.file_list_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)
        ttk.Button(file_frame, text="浏览", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)
        
        # 2. 配置区域
        config_frame = ttk.LabelFrame(self.main_frame, text="配置", padding="10")
        config_frame.pack(fill=tk.X, pady=5)
        
        # Cookie输入
        ttk.Label(config_frame, text="Cookie：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        cookie_entry = ttk.Entry(config_frame, textvariable=self.cookie_var, width=50)
        cookie_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(config_frame, text="保存", command=self.save_cookie).grid(row=0, column=2, padx=5, pady=5)
        
        # 课程URL输入
        ttk.Label(config_frame, text="课程URL：").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        url_entry = ttk.Entry(config_frame, textvariable=self.course_url_var, width=50)
        url_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(config_frame, text="保存", command=self.save_course_url).grid(row=1, column=2, padx=5, pady=5)
        
        # 3. 操作区域
        action_frame = ttk.Frame(self.main_frame, padding="10")
        action_frame.pack(fill=tk.X, pady=10)
        
        # 创建自定义按钮样式
        style = ttk.Style()
        style.configure("Large.TButton", 
                       font=('Arial', 12, 'bold'),
                       padding=(20, 10))
        
        # 创建上传按钮并居中显示
        self.upload_btn = ttk.Button(action_frame, text="上传文件", command=self.upload_file, style="Large.TButton")
        self.upload_btn.pack(side=tk.TOP, pady=5, expand=True)
        
        # 4. 文件URL显示区域（用于一键复制）
        url_frame = ttk.LabelFrame(self.main_frame, text="文件URL", padding="10")
        url_frame.pack(fill=tk.X, pady=5)
        
        # 创建一个容器用于显示多个URL项
        self.url_items_container = ttk.Frame(url_frame)
        self.url_items_container.pack(fill=tk.X, pady=5)
        
        # 添加复制所有按钮
        self.copy_all_btn = ttk.Button(url_frame, text="复制所有", command=self.copy_all_urls)
        self.copy_all_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        self.copy_all_btn.config(state="disabled")  # 初始状态禁用
        
        # 初始化URL项存储
        self.url_items = []
        
        # 5. 结果显示区域
        result_frame = ttk.LabelFrame(self.main_frame, text="上传结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建结果文本框
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=10)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(self.result_text, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # 5. 状态区域
        status_frame = ttk.Frame(self.main_frame, padding="10")
        status_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)
        

        

    
    def open_tutorial_web(self):
        """打开使用教程网页"""
        try:
            import webbrowser
            webbrowser.open("https://github.com/itrfcn/FreePic")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开网页：{str(e)}")
    

    
    def copy_all_urls(self):
        """复制所有成功上传的文件URL到剪贴板"""
        if not self.uploaded_files:
            messagebox.showwarning("警告", "没有成功上传的文件！")
            return
            
        try:
            # 收集所有URL
            urls = [file_info['file'] for file_info in self.uploaded_files]
            urls_text = '\n'.join(urls)
            
            # 将URL复制到剪贴板
            self.root.clipboard_clear()
            self.root.clipboard_append(urls_text)
            self.root.update()  # 保持剪贴板内容
            
            messagebox.showinfo("成功", f"已复制 {len(urls)} 个文件URL到剪贴板！")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败：{str(e)}")
    
    def create_url_item(self, file_info, index):
        """为每个成功上传的文件创建URL显示项"""
        # 创建URL项框架
        url_item_frame = ttk.Frame(self.url_items_container)
        url_item_frame.pack(fill=tk.X, pady=3)
        
        # 创建URL标签
        url_label = ttk.Label(url_item_frame, text=f"文件 {index+1}：", anchor=tk.W)
        url_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # 创建URL输入框
        url_var = tk.StringVar(value=file_info['file'])
        url_entry = ttk.Entry(url_item_frame, textvariable=url_var, width=50, state='readonly')
        url_entry.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.X, expand=True)
        
        # 创建复制按钮
        copy_btn = ttk.Button(url_item_frame, text="复制", width=8, 
                            command=lambda u=file_info['file'], f=file_info['name']: self.copy_single_url(u, f))
        copy_btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        # 创建打开按钮
        open_btn = ttk.Button(url_item_frame, text="打开", width=8, 
                            command=lambda u=file_info['file'], f=file_info['name']: self.open_single_url(u, f))
        open_btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        # 保存URL项信息
        return {
            'frame': url_item_frame,
            'url_var': url_var,
            'url_entry': url_entry,
            'copy_btn': copy_btn,
            'open_btn': open_btn
        }
    
    def copy_single_url(self, url, filename):
        """复制单个文件URL到剪贴板"""
        if url:
            try:
                # 将URL复制到剪贴板
                self.root.clipboard_clear()
                self.root.clipboard_append(url)
                self.root.update()  # 保持剪贴板内容
                messagebox.showinfo("成功", f"文件 '{filename}' 的URL已复制到剪贴板！")
            except Exception as e:
                messagebox.showerror("错误", f"复制失败：{str(e)}")
    
    def open_single_url(self, url, filename):
        """在浏览器中打开单个文件URL"""
        if url:
            try:
                webbrowser.open(url)
                messagebox.showinfo("成功", f"文件 '{filename}' 的URL已在浏览器中打开！")
            except Exception as e:
                messagebox.showerror("错误", f"打开失败：{str(e)}")
    
    def clear_url_items(self):
        """清空所有URL显示项"""
        for item in self.url_items:
            item['frame'].destroy()
        self.url_items = []
    
    def browse_file(self):
        """浏览文件"""
        file_paths = filedialog.askopenfilenames(
            title="选择文件",
            filetypes=[
                ("所有支持的文件", "*.png *.jpg *.jpeg *.txt *.doc *.docx *.ppt *.pptx *.xls *.xlsx"),
                ("图片文件", "*.png *.jpg *.jpeg"),
                ("文档文件", "*.txt *.doc *.docx"),
                ("演示文件", "*.ppt *.pptx"),
                ("表格文件", "*.xls *.xlsx"),
            ]
        )
        if file_paths:
            self.selected_files = list(file_paths)
            file_names = [os.path.basename(f) for f in self.selected_files]
            self.status_var.set(f"已选择 {len(self.selected_files)} 个文件：{', '.join(file_names[:3])}{'...' if len(file_names) > 3 else ''}")
            # 更新文件选择显示
            self.update_file_selection_display()
    
    def update_file_selection_display(self):
        """更新文件选择显示区域"""
        # 清空之前的显示
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
        
        if not self.selected_files:
            ttk.Label(self.file_list_frame, text="未选择任何文件", foreground="gray").pack(anchor=tk.W)
            return
        
        # 创建文件列表
        file_list = ttk.Treeview(self.file_list_frame, columns=('filename'), show='headings', height=min(5, len(self.selected_files)))
        file_list.heading('filename', text='文件名')
        file_list.column('filename', width=500)
        
        for file_path in self.selected_files:
            filename = os.path.basename(file_path)
            file_list.insert('', tk.END, values=(filename,))
        
        file_list.pack(fill=tk.X, expand=True)
        
        # 添加删除按钮
        ttk.Button(self.file_list_frame, text="清除选择", command=self.clear_file_selection).pack(side=tk.RIGHT, padx=5, pady=5)
        
        # 自动调整窗口高度
        self.adjust_window_height()
    
    def clear_file_selection(self):
        """清除已选择的文件"""
        self.selected_files = []
        self.status_var.set("就绪")
        self.update_file_selection_display()
        self.adjust_window_height()
    
    def adjust_window_height(self):
        """根据内容自动调整窗口高度"""
        # 计算主框架的总高度
        main_height = self.main_frame.winfo_reqheight()
        
        # 计算窗口需要的总高度（主框架高度 + 窗口标题栏高度）
        window_height = main_height + 50  # 50是窗口标题栏和边框的大概高度
        
        # 设置窗口最小高度为原始高度
        min_height = 550
        
        # 调整窗口高度
        new_height = max(min_height, window_height)
        self.root.geometry(f"600x{new_height}")
    
    def save_cookie(self):
        """保存Cookie到环境变量文件"""
        cookie = self.cookie_var.get().strip()
        if not cookie:
            messagebox.showwarning("警告", "Cookie不能为空！")
            return
            
        try:
            # 创建或更新.env文件
            env_dict = {}
            if os.path.exists(".env"):
                with open(".env", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            key, value = line.split("=", 1)
                            env_dict[key.strip()] = value.strip()
            
            # 更新Cookie配置
            env_dict["COOKIE_STRING"] = cookie
            
            # 写回.env文件
            with open(".env", "w", encoding="utf-8") as f:
                for key, value in env_dict.items():
                    f.write(f"{key}={value}\n")
            
            messagebox.showinfo("成功", "Cookie已保存！")
            self.status_var.set("Cookie已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存Cookie失败：{str(e)}")
            self.status_var.set("保存Cookie失败")
    
    def save_course_url(self):
        """保存课程URL到环境变量文件"""
        url = self.course_url_var.get().strip()
        if not url:
            messagebox.showwarning("警告", "课程URL不能为空！")
            return
            
        try:
            # 创建或更新.env文件
            env_dict = {}
            if os.path.exists(".env"):
                with open(".env", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            key, value = line.split("=", 1)
                            env_dict[key.strip()] = value.strip()
            
            # 更新课程URL配置
            env_dict["COURSE_URL"] = url
            
            # 写回.env文件
            with open(".env", "w", encoding="utf-8") as f:
                for key, value in env_dict.items():
                    f.write(f"{key}={value}\n")
            
            messagebox.showinfo("成功", "课程URL已保存！")
            self.status_var.set("课程URL已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存课程URL失败：{str(e)}")
            self.status_var.set("保存课程URL失败")
    
    def upload_file(self):
        """上传文件"""
        if not self.selected_files:
            messagebox.showwarning("警告", "请先选择要上传的文件！")
            return
            
        # 检查文件是否存在
        for file_path in self.selected_files:
            if not os.path.exists(file_path):
                messagebox.showwarning("警告", f"文件不存在：{os.path.basename(file_path)}")
                return
            
        cookie = self.cookie_var.get().strip()
        if not cookie:
            messagebox.showwarning("警告", "请先输入Cookie！")
            return
            
        # 禁用上传按钮
        self.upload_btn.config(state="disabled")
        
        # 清空URL显示区域
        self.clear_url_items()
        
        # 显示提示信息
        uploading_label = ttk.Label(self.url_items_container, text="正在上传文件...", foreground="gray")
        uploading_label.pack(anchor=tk.W, padx=5, pady=10)
        self.url_items.append({'frame': uploading_label})
        
        self.status_var.set("正在上传文件...")
        self.result_text.delete(1.0, tk.END)
        
        # 在后台线程中执行上传
        self.root.after(100, self._upload_file_thread, self.selected_files, cookie)
    
    def _upload_file_thread(self, file_paths, cookie):
        """上传文件的后台线程"""
        try:
            total_files = len(file_paths)
            success_count = 0
            fail_count = 0
            
            self.result_text.insert(tk.END, f"开始上传 {total_files} 个文件...\n\n")
            self.root.update()
            
            # 清空之前的上传记录
            self.uploaded_files = []
            
            # 循环上传每个文件
            for i, file_path in enumerate(file_paths, 1):
                filename = os.path.basename(file_path)
                self.result_text.insert(tk.END, f"[{i}/{total_files}] 正在上传：{filename}\n")
                self.root.update()
                
                try:
                    file_info = upload_file_to_oss(file_path, cookie, debug=True)
                    
                    if file_info:
                        # 显示上传结果
                        self.result_text.insert(tk.END, f"   ✓ 上传成功！\n")
                        self.result_text.insert(tk.END, f"     文件名：{file_info['name']}\n")
                        self.result_text.insert(tk.END, f"     文件URL：{file_info['file']}\n")
                        self.result_text.insert(tk.END, f"     文件大小：{file_info['size']} 字节\n")
                        self.result_text.insert(tk.END, f"     文件类型：{file_info['type']}\n")
                        
                        success_count += 1
                        self.uploaded_files.append(file_info)
                    else:
                        self.result_text.insert(tk.END, f"   ✗ 上传失败！\n")
                        fail_count += 1
                        
                except Exception as e:
                    self.result_text.insert(tk.END, f"   ✗ 上传出错：{str(e)}\n")
                    fail_count += 1
                
                self.result_text.insert(tk.END, "\n")
                self.root.update()
            
            # 显示上传汇总
            self.result_text.insert(tk.END, "========================================\n")
            self.result_text.insert(tk.END, f"上传完成！共 {total_files} 个文件\n")
            self.result_text.insert(tk.END, f"成功：{success_count} 个\n")
            self.result_text.insert(tk.END, f"失败：{fail_count} 个\n")
            
            # 清空之前的URL显示项
            self.clear_url_items()
            
            if self.uploaded_files:
                # 为每个成功上传的文件创建URL显示项
                for index, file_info in enumerate(self.uploaded_files):
                    url_item = self.create_url_item(file_info, index)
                    self.url_items.append(url_item)
                
                # 启用复制所有按钮
                self.copy_all_btn.config(state="normal")
                
                # 自动调整窗口高度
                self.adjust_window_height()
            else:
                # 没有成功上传的文件，禁用复制所有按钮
                self.copy_all_btn.config(state="disabled")
                
                # 显示提示信息
                no_files_label = ttk.Label(self.url_items_container, text="没有成功上传的文件URL", foreground="gray")
                no_files_label.pack(anchor=tk.W, padx=5, pady=10)
                self.url_items.append({'frame': no_files_label})
                
            # 更新状态
            if fail_count == 0:
                self.status_var.set("全部上传成功")
                messagebox.showinfo("成功", f"全部 {success_count} 个文件上传成功！")
            elif success_count == 0:
                self.status_var.set("全部上传失败")
                messagebox.showerror("错误", f"全部 {fail_count} 个文件上传失败！")
            else:
                self.status_var.set("部分上传成功")
                messagebox.showinfo("提示", f"上传完成！成功 {success_count} 个，失败 {fail_count} 个")
                
        except Exception as e:
            self.result_text.insert(tk.END, f"\n上传过程中出错：{str(e)}\n")
            self.status_var.set("上传失败")
            messagebox.showerror("错误", f"上传过程中出错：{str(e)}")
            
        finally:
            # 启用上传按钮
            self.upload_btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileUploadGUI(root)
    root.mainloop()