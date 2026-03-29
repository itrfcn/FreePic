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
        self.root.resizable(False, False)
        
        # 初始化变量
        self.selected_file = tk.StringVar()
        self.cookie_var = tk.StringVar(value=COOKIE_STRING)
        self.course_url_var = tk.StringVar(value=COURSE_URL)
        self.status_var = tk.StringVar(value="就绪")
        
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
        ttk.Entry(file_frame, textvariable=self.selected_file, width=50, state='readonly').grid(row=0, column=1, padx=5, pady=5)
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
        
        # 文件URL标签、复制按钮和浏览器打开按钮
        ttk.Label(url_frame, text="文件地址：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.file_url_var = tk.StringVar()
        self.file_url_entry = ttk.Entry(url_frame, textvariable=self.file_url_var, width=40, state='readonly')
        self.file_url_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.copy_btn = ttk.Button(url_frame, text="复制", command=self.copy_to_clipboard)
        self.copy_btn.grid(row=0, column=2, padx=5, pady=5)
        self.copy_btn.config(state="disabled")  # 初始状态禁用
        
        self.open_btn = ttk.Button(url_frame, text="打开", command=self.open_in_browser)
        self.open_btn.grid(row=0, column=3, padx=5, pady=5)
        self.open_btn.config(state="disabled")  # 初始状态禁用
        
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
    
    def copy_to_clipboard(self):
        """复制文件URL到剪贴板"""
        url = self.file_url_var.get().strip()
        if url:
            try:
                # 将URL复制到剪贴板
                self.root.clipboard_clear()
                self.root.clipboard_append(url)
                self.root.update()  # 保持剪贴板内容
                messagebox.showinfo("成功", "文件URL已复制到剪贴板！")
            except Exception as e:
                messagebox.showerror("错误", f"复制失败：{str(e)}")
    
    def open_in_browser(self):
        """在浏览器中打开文件URL"""
        url = self.file_url_var.get().strip()
        if url:
            try:
                webbrowser.open(url)
                messagebox.showinfo("成功", "文件URL已在浏览器中打开！")
            except Exception as e:
                messagebox.showerror("错误", f"打开失败：{str(e)}")
    
    def browse_file(self):
        """浏览文件"""
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[
                ("所有支持的文件", "*.png *.jpg *.jpeg *.txt *.doc *.docx *.ppt *.pptx *.xls *.xlsx"),
                ("图片文件", "*.png *.jpg *.jpeg"),
                ("文档文件", "*.txt *.doc *.docx"),
                ("演示文件", "*.ppt *.pptx"),
                ("表格文件", "*.xls *.xlsx"),
            ]
        )
        if file_path:
            self.selected_file.set(file_path)
            self.status_var.set(f"已选择文件：{os.path.basename(file_path)}")
    
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
        file_path = self.selected_file.get().strip()
        if not file_path:
            messagebox.showwarning("警告", "请先选择要上传的文件！")
            return
            
        if not os.path.exists(file_path):
            messagebox.showwarning("警告", "选择的文件不存在！")
            return
            
        cookie = self.cookie_var.get().strip()
        if not cookie:
            messagebox.showwarning("警告", "请先输入Cookie！")
            return
            
        # 禁用上传按钮
        self.upload_btn.config(state="disabled")
        
        # 清空文件URL显示并禁用复制和打开按钮
        self.file_url_var.set("")
        self.copy_btn.config(state="disabled")
        self.open_btn.config(state="disabled")
        
        self.status_var.set("正在上传文件...")
        self.result_text.delete(1.0, tk.END)
        
        # 在后台线程中执行上传
        self.root.after(100, self._upload_file_thread, file_path, cookie)
    
    def _upload_file_thread(self, file_path, cookie):
        """上传文件的后台线程"""
        try:
            # 调用上传函数
            self.result_text.insert(tk.END, f"正在上传文件：{os.path.basename(file_path)}\n")
            self.root.update()
            
            file_info = upload_file_to_oss(file_path, cookie, debug=True)
            
            if file_info:
                # 显示上传结果
                self.result_text.insert(tk.END, "\n上传成功！\n")
                self.result_text.insert(tk.END, f"文件名：{file_info['name']}\n")
                self.result_text.insert(tk.END, f"文件URL：{file_info['file']}\n")
                self.result_text.insert(tk.END, f"文件大小：{file_info['size']} 字节\n")
                self.result_text.insert(tk.END, f"文件类型：{file_info['type']}\n")
                
                # 更新文件URL显示并启用复制和打开按钮
                self.file_url_var.set(file_info['file'])
                self.copy_btn.config(state="normal")
                self.open_btn.config(state="normal")
                
                self.status_var.set("上传成功")
                messagebox.showinfo("成功", "文件上传成功！")
            else:
                self.result_text.insert(tk.END, "\n上传失败！\n")
                self.status_var.set("上传失败")
                messagebox.showerror("错误", "文件上传失败！")
                
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