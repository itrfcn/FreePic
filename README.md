# 免费图床工具 v1.0

一款利用班级魔方的OSS存储服务开发的免费图床工具，支持上传图片、文档、演示文件等格式的文件。

- 核心亮点，利用了班级魔方的接口，实现了免费使用国内高速的OSS存储。
- 无需自己购买OSS存储以及域名，直接使用班级魔方的OSS存储服务和域名。
- 实现0成本，使用国内高速的OSS存储服务。

想直接使用，点击这里：[免费图床工具](https://github.com/itrfcn/Freepic/releases/latest)

### 支持的文件格式
- **图片**：.png, .jpg, .jpeg
- **文档**：.txt, .doc, .docx
- **演示文件**：.ppt, .pptx
- **表格文件**：.xls, .xlsx


## 安装要求

### 系统要求
- Windows, macOS, Linux
- Python 3.12+

### 依赖库
```
requests
python-dotenv
```

## 安装步骤

1. 克隆或下载项目
2. 安装依赖库：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

### 1. GUI模式（推荐）

运行GUI程序：
```bash
python gui.py
```
#### 参数获取

- 需要微信扫码注册班级魔方教师账号和学生账号，一个微信就可以同时注册学生账号和教师账号。
- 教师账号创建班级，学生账号加入班级。
- 教师账号发布一个 填报/问卷 添加文件上传项，学生账号加入填报/问卷。
- 问卷的链接就是 COURSE_URL 参数。
- COOKIE_STRING是学生账号的Cookie信息的remember_student部分，s=部分会自动获取。
- Cookie有效期为5年放心使用。

#### 使用步骤
1. **配置设置**：
   - 输入Cookie信息并点击保存
   - 可选择修改课程URL（默认已配置）

2. **文件上传**：
   - 点击"浏览"按钮选择要上传的文件
   - 点击居中的"上传文件"按钮开始上传

3. **上传结果**：
   - 上传成功后，文件URL会显示在"文件URL"区域
   - 点击"复制"按钮将URL复制到剪贴板
   - 点击"打开"按钮在浏览器中打开文件
   - 详细结果显示在"上传结果"区域


### 2. 命令行模式

```bash
python free.py -i <文件路径> [-c <cookie>] [--debug]
```

#### 参数说明
- `-i, --image`：要上传的文件路径（必填）
- `-c, --cookie`：Cookie信息（可选，默认从.env或环境变量获取）
- `--debug`：启用调试模式（可选）

#### 示例
```bash
python free.py -i "C:\Users\User\Desktop\example.png" -c "remember_student=xxx"
```

## 配置说明

### 环境变量

可以通过环境变量配置：
- `COURSE_URL`：课程页面URL
- `COOKIE_STRING`：Cookie信息


### .env文件

创建.env文件并添加配置：
```
COURSE_URL=https://k8n.cn/student/profile/course/11111/11111
COOKIE_STRING=remember_student=xxx
```

## 相关项目

网页版本：[PicUp](https://github.com/itrfcn/PicUp)

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题或建议，请通过GitHub Issue反馈。