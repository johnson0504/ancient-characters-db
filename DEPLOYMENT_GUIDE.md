# 📦 古文字库系统 - 交付部署指南

## 🎯 交付清单

### 必需文件

#### 1. 核心应用文件
```
app.py                          # Flask 应用主程序
char_detail.html                # 前端页面
ancient_characters.db           # 数据库文件（重要！）
```

#### 2. 虚拟环境和依赖
```
venv_ancient/                   # Python 虚拟环境（整个目录）
requirements.txt                # Python 依赖列表（需要创建）
```

#### 3. 启动脚本
```
start_venv.sh                   # 启动脚本
```

#### 4. 数据文件
```
extracted_final/字形图片/       # 字形图片目录（整个目录，约 1.4GB）
```

#### 5. 文档文件
```
API_DOCUMENTATION.md            # API 文档
ANNOTATION_GUIDE.md             # 注释使用指南
QUICKSTART.md                   # 快速开始指南
DELIVERY_REPORT.md              # 交付报告
```

---

## 📋 完整的文件清单

### 需要复制的目录结构

```
ancient-characters-db/
├── app.py                              # ✅ 必需
├── char_detail.html                    # ✅ 必需
├── ancient_characters.db               # ✅ 必需（数据库）
├── venv_ancient/                       # ✅ 必需（虚拟环境）
│   ├── bin/
│   ├── lib/
│   └── ...
├── extracted_final/字形图片/           # ✅ 必需（图片数据，约 1.4GB）
│   ├── hai/
│   ├── kai/
│   └── ...
├── requirements.txt                    # ✅ 必需（依赖列表）
├── start_venv.sh                       # ✅ 必需（启动脚本）
├── README.md                           # ✅ 推荐（部署说明）
├── API_DOCUMENTATION.md                # ✅ 推荐（API 文档）
├── QUICKSTART.md                       # ✅ 推荐（快速开始）
└── DELIVERY_REPORT.md                  # ✅ 推荐（交付报告）
```

---

## 🔧 准备工作

### 第一步：创建 requirements.txt

在项目根目录创建 `requirements.txt` 文件：

```bash
cat > requirements.txt << 'EOF'
Flask==2.3.3
Flask-CORS==4.0.0
Werkzeug==2.3.7
EOF
```

### 第二步：验证虚拟环境

```bash
# 检查虚拟环境是否完整
ls -la venv_ancient/bin/python3
ls -la venv_ancient/lib/python3.12/site-packages/flask
```

### 第三步：验证数据库

```bash
# 检查数据库文件大小
ls -lh ancient_characters.db

# 验证数据库完整性
sqlite3 ancient_characters.db "SELECT COUNT(*) FROM characters;"
```

### 第四步：验证图片数据

```bash
# 检查图片目录大小
du -sh extracted_final/字形图片/

# 检查图片数量
find extracted_final/字形图片 -type f | wc -l
```

---

## 📦 打包方式

### 方式 1：使用 tar 压缩（推荐）

```bash
# 创建压缩包（包含虚拟环境）
tar -czf ancient-characters-db-full.tar.gz \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  app.py \
  char_detail.html \
  ancient_characters.db \
  venv_ancient/ \
  extracted_final/字形图片/ \
  requirements.txt \
  start_venv.sh \
  README.md \
  API_DOCUMENTATION.md \
  QUICKSTART.md \
  DELIVERY_REPORT.md

# 查看压缩包大小
ls -lh ancient-characters-db-full.tar.gz
```

### 方式 2：分离虚拟环境（更小的包）

```bash
# 创建不含虚拟环境的压缩包
tar -czf ancient-characters-db-lite.tar.gz \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  app.py \
  char_detail.html \
  ancient_characters.db \
  extracted_final/字形图片/ \
  requirements.txt \
  start_venv.sh \
  README.md \
  API_DOCUMENTATION.md \
  QUICKSTART.md \
  DELIVERY_REPORT.md

# 客户端需要自己创建虚拟环境
```

### 方式 3：分卷压缩（用于网络传输）

```bash
# 分卷压缩（每卷 500MB）
tar -czf - \
  app.py \
  char_detail.html \
  ancient_characters.db \
  venv_ancient/ \
  extracted_final/字形图片/ \
  requirements.txt \
  start_venv.sh \
  README.md \
  API_DOCUMENTATION.md \
  QUICKSTART.md \
  DELIVERY_REPORT.md | split -b 500m - ancient-characters-db.tar.gz.

# 合并分卷
cat ancient-characters-db.tar.gz.* | tar -xzf -
```

---

## 📥 客户端部署步骤

### 步骤 1：解压文件

```bash
# 如果是完整包
tar -xzf ancient-characters-db-full.tar.gz

# 如果是分卷
cat ancient-characters-db.tar.gz.* | tar -xzf -
```

### 步骤 2：创建虚拟环境（仅限 lite 版本）

```bash
cd ancient-characters-db
python3 -m venv venv_ancient
source venv_ancient/bin/activate
pip install -r requirements.txt
```

### 步骤 3：启动服务

```bash
bash start_venv.sh
```

### 步骤 4：访问系统

```
http://localhost:5000/char_detail.html
```

---

## 📊 文件大小估计

| 文件/目录 | 大小 | 说明 |
|----------|------|------|
| app.py | ~16 KB | Flask 应用 |
| char_detail.html | ~12 KB | 前端页面 |
| ancient_characters.db | ~2 MB | 数据库 |
| venv_ancient/ | ~500 MB | 虚拟环境 |
| extracted_final/字形图片/ | ~1.4 GB | 字形图片 |
| 文档文件 | ~50 KB | 各种文档 |
| **总计（完整包）** | **~1.9 GB** | 包含虚拟环境 |
| **总计（lite 包）** | **~1.4 GB** | 不含虚拟环境 |

---

## 🔍 系统要求

### 客户端要求

#### 最低配置
- **操作系统：** Linux (Ubuntu 20.04+) / macOS / Windows (WSL2)
- **Python：** 3.8+
- **磁盘空间：** 2 GB（完整包）或 1.5 GB（lite 包）
- **内存：** 2 GB
- **网络：** 无特殊要求

#### 推荐配置
- **操作系统：** Linux (Ubuntu 22.04+)
- **Python：** 3.10+
- **磁盘空间：** 3 GB
- **内存：** 4 GB
- **CPU：** 2 核+

### 依赖软件

#### 必需
- Python 3.8+
- pip（Python 包管理器）

#### 可选
- SQLite3（用于数据库查询）
- curl 或 wget（用于测试 API）

---

## 🚀 快速部署脚本

创建 `deploy.sh` 脚本供客户使用：

```bash
#!/bin/bash

echo "🚀 古文字库系统 - 部署脚本"
echo "================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"

# 检查虚拟环境
if [ ! -d "venv_ancient" ]; then
    echo ""
    echo "📦 创建虚拟环境..."
    python3 -m venv venv_ancient
    source venv_ancient/bin/activate
    pip install -r requirements.txt
    echo "✅ 虚拟环境已创建"
else
    echo "✅ 虚拟环境已存在"
    source venv_ancient/bin/activate
fi

# 检查数据库
if [ ! -f "ancient_characters.db" ]; then
    echo "❌ 错误：未找到数据库文件"
    exit 1
fi

echo "✅ 数据库文件已找到"

# 检查图片目录
if [ ! -d "extracted_final/字形图片" ]; then
    echo "❌ 错误：未找到图片目录"
    exit 1
fi

echo "✅ 图片目录已找到"

# 启动服务
echo ""
echo "🌐 启动 Flask 服务..."
echo "📍 访问地址: http://localhost:5000"
echo "📄 详情页面: http://localhost:5000/char_detail.html"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python3 app.py
```

---

## 📝 创建 README.md

```markdown
# 古文字库系统

## 快速开始

### 方式 1：使用启动脚本（推荐）

\`\`\`bash
bash start_venv.sh
\`\`\`

### 方式 2：手动启动

\`\`\`bash
source venv_ancient/bin/activate
python3 app.py
\`\`\`

### 方式 3：使用部署脚本

\`\`\`bash
bash deploy.sh
\`\`\`

## 访问系统

打开浏览器访问：
\`\`\`
http://localhost:5000/char_detail.html
\`\`\`

## 系统要求

- Python 3.8+
- 2 GB 磁盘空间
- 2 GB 内存

## 文档

- [API 文档](API_DOCUMENTATION.md)
- [使用指南](ANNOTATION_GUIDE.md)
- [快速开始](QUICKSTART.md)
- [交付报告](DELIVERY_REPORT.md)

## 支持

如有问题，请参考文档或联系技术支持。
```

---

## ✅ 交付检查清单

在交付前，请确认以下项目：

- [ ] `app.py` 已复制
- [ ] `char_detail.html` 已复制
- [ ] `ancient_characters.db` 已复制（验证大小 ~2 MB）
- [ ] `venv_ancient/` 已复制（或 requirements.txt 已创建）
- [ ] `extracted_final/字形图片/` 已复制（验证大小 ~1.4 GB）
- [ ] `start_venv.sh` 已复制
- [ ] `requirements.txt` 已创建
- [ ] `README.md` 已创建
- [ ] `deploy.sh` 已创建
- [ ] 所有文档已复制
- [ ] 压缩包已创建并验证
- [ ] 在测试环境中验证部署流程

---

## 🎯 推荐交付方式

### 对于本地交付
```bash
# 使用完整包（包含虚拟环境）
tar -czf ancient-characters-db-full.tar.gz \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  app.py char_detail.html ancient_characters.db \
  venv_ancient/ extracted_final/字形图片/ \
  requirements.txt start_venv.sh deploy.sh \
  README.md API_DOCUMENTATION.md QUICKSTART.md DELIVERY_REPORT.md
```

### 对于网络传输
```bash
# 使用 lite 包（不含虚拟环境，更小）
tar -czf ancient-characters-db-lite.tar.gz \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  app.py char_detail.html ancient_characters.db \
  extracted_final/字形图片/ \
  requirements.txt start_venv.sh deploy.sh \
  README.md API_DOCUMENTATION.md QUICKSTART.md DELIVERY_REPORT.md
```

---

## 📞 客户支持

### 常见问题

**Q: 如何启动系统？**  
A: 运行 `bash start_venv.sh` 或 `bash deploy.sh`

**Q: 系统无法启动？**  
A: 检查 Python 版本、虚拟环境、数据库文件

**Q: 如何停止系统？**  
A: 按 Ctrl+C

**Q: 如何修改端口？**  
A: 编辑 `app.py` 最后一行，改为 `app.run(port=8000)`

---

**交付日期：** 2026-05-06  
**版本：** 1.0  
**状态：** 生产就绪
