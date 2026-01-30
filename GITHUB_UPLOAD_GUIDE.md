# GitHub 上传指南 - PubMed Search Tool for OpenWebUI

## 项目文件清单

### 核心文件（必须上传）
```
pubmed-openwebui-tool/
├── pubmed_search_tool.py      # 主插件文件（从 results/ 复制）
├── test_pubmed_tool.py        # 测试文件（从 workflow/ 复制）
├── README.md                  # 项目说明文档
├── .gitignore                 # Git 忽略配置
├── pyproject.toml             # Python 项目配置
└── LICENSE                    # 许可证（建议添加）
```

---

## 详细上传步骤

### 前提条件

1. **安装 Git**（如未安装）
   ```bash
   # Windows: 下载 https://git-scm.com/download/win
   # macOS:
   brew install git
   # Linux (Ubuntu/Debian):
   sudo apt-get install git
   ```

2. **配置 Git 用户信息**（首次使用需要）
   ```bash
   git config --global user.name "你的用户名"
   git config --global user.email "你的邮箱@example.com"
   ```

3. **有 GitHub 账号**
   - 注册地址: https://github.com/signup

---

### 步骤 1: 在 GitHub 创建新仓库

1. 登录 GitHub: https://github.com
2. 点击右上角 **+** 号 → **New repository**
3. 填写仓库信息:
   - **Repository name**: `pubmed-openwebui-tool` (或您喜欢的名字)
   - **Description**: `PubMed Literature Search Tool for OpenWebUI`
   - **Visibility**: 选择 Public（公开）或 Private（私有）
   - **⚠️ 不要勾选** "Add a README file"（我们已有）
   - **⚠️ 不要勾选** "Add .gitignore"（我们已有）
4. 点击 **Create repository**

---

### 步骤 2: 准备本地项目文件夹

在您的电脑上创建一个干净的项目文件夹，并复制必要文件：

```bash
# 1. 创建项目文件夹
mkdir pubmed-openwebui-tool
cd pubmed-openwebui-tool

# 2. 从原始位置复制文件（假设原文件在 ~/Downloads/ 或其他位置）
# 请根据您的实际文件位置修改路径

# 复制主插件文件
cp /path/to/results/pubmed_search_tool.py ./

# 复制测试文件
cp /path/to/workflow/test_pubmed_tool.py ./

# 复制 README
cp /path/to/README.md ./

# 复制 .gitignore
cp /path/to/.gitignore ./

# 复制项目配置
cp /path/to/pyproject.toml ./
```

---

### 步骤 3: 初始化 Git 仓库并推送

在项目文件夹中执行以下命令：

```bash
# 1. 初始化 Git 仓库
git init

# 2. 添加所有文件到暂存区
git add .

# 3. 查看将要提交的文件（可选，用于确认）
git status

# 4. 创建首次提交
git commit -m "Initial commit: PubMed Search Tool for OpenWebUI"

# 5. 设置主分支名称
git branch -M main

# 6. 添加远程仓库地址（替换为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/pubmed-openwebui-tool.git

# 7. 推送到 GitHub
git push -u origin main
```

---

### 步骤 4: 验证上传

1. 打开浏览器，访问您的仓库: `https://github.com/YOUR_USERNAME/pubmed-openwebui-tool`
2. 确认所有文件都已上传
3. README.md 应该自动显示在仓库首页

---

## 常见问题解决

### Q: 提示需要登录认证

**使用 HTTPS 方式（推荐）**:
```bash
# Git 2.x 以上版本会自动弹出浏览器登录
# 或者使用 Personal Access Token (PAT)
```

**创建 Personal Access Token**:
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制 token
5. 推送时用 token 代替密码

### Q: 提示 "remote origin already exists"

```bash
# 删除旧的远程地址
git remote remove origin

# 重新添加
git remote add origin https://github.com/YOUR_USERNAME/pubmed-openwebui-tool.git
```

### Q: 想要更新已上传的文件

```bash
# 1. 修改文件后
git add .
git commit -m "Update: 描述您的修改"
git push
```

---

## 推荐的额外步骤

### 添加 LICENSE 文件

创建 `LICENSE` 文件，推荐使用 MIT 许可证：

```text
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 添加 GitHub Topics/Tags

上传后，在仓库页面:
1. 点击 ⚙️ Settings 旁边的齿轮图标
2. 添加 Topics: `openwebui`, `pubmed`, `llm-tool`, `python`, `biomedical`

---

## 快速命令汇总

```bash
# 一次性执行（在准备好文件的文件夹中）
git init && \
git add . && \
git commit -m "Initial commit: PubMed Search Tool for OpenWebUI" && \
git branch -M main && \
git remote add origin https://github.com/YOUR_USERNAME/pubmed-openwebui-tool.git && \
git push -u origin main
```

**记得将 `YOUR_USERNAME` 替换为您的 GitHub 用户名！**

---

## 项目结构说明

| 文件 | 用途 |
|------|------|
| `pubmed_search_tool.py` | OpenWebUI 插件主文件，包含完整的 PubMed 搜索功能 |
| `test_pubmed_tool.py` | 测试脚本，验证插件功能 |
| `README.md` | 项目说明、安装指南、使用示例 |
| `.gitignore` | 告诉 Git 忽略哪些文件（缓存、日志等） |
| `pyproject.toml` | Python 项目配置，包含依赖信息 |

---

如有问题，请参考 GitHub 官方文档: https://docs.github.com/cn/get-started
