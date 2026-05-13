# 古文字库 - 在线部署指南

## 📋 部署前准备

你的项目已经准备好上线。这是一个 Flask + SQLite 的完整系统，包含：

- ✅ 后端 API（Flask）
- ✅ 前端页面（HTML5）
- ✅ 数据库（SQLite）
- ✅ 图片资源（45MB）
- ✅ 部署配置文件

---

## 🚀 推荐部署方案

### 方案 A：Render（最简单，推荐）

**优点：** 免费额度、自动部署、无需配置、支持 Python

**步骤：**

1. **创建 GitHub 仓库**
   ```bash
   # 在 GitHub 上创建新仓库：ancient-characters-db
   # 然后本地推送
   git remote add origin https://github.com/YOUR_USERNAME/ancient-characters-db.git
   git branch -M main
   git push -u origin main
   ```

2. **连接 Render**
   - 访问 https://render.com
   - 用 GitHub 账号登录
   - 点击 "New +" → "Web Service"
   - 选择你的仓库
   - 配置：
     - **Name:** ancient-characters-db
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python app.py`
   - 点击 "Create Web Service"

3. **等待部署完成**
   - Render 会自动构建和启动
   - 你会获得一个公网 URL，比如：`https://ancient-characters-db.onrender.com`

4. **测试**
   - 访问 `https://ancient-characters-db.onrender.com`
   - 应该看到项目展示页
   - 点击"立即体验"进入应用

**注意：** 免费版本可能会在 15 分钟无活动后休眠，首次访问需要等待启动。

---

### 方案 B：Railway（备选，也很简单）

**优点：** 免费额度充足、启动快、支持自动部署

**步骤：**

1. 访问 https://railway.app
2. 用 GitHub 登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. Railway 会自动检测 Python 项目并部署
6. 获得公网 URL

---

### 方案 C：Vercel（如果改成纯前端）

**注意：** Vercel 主要用于前端，你的项目有 Flask 后端，所以不太适合。

---

## 🔧 部署前检查清单

在推送到 GitHub 前，确保：

- [ ] `.gitignore` 已配置（已完成 ✅）
- [ ] `requirements.txt` 包含所有依赖（已完成 ✅）
- [ ] `Procfile` 已创建（已完成 ✅）
- [ ] `render.yaml` 已创建（已完成 ✅）
- [ ] 数据库文件 `ancient_characters.db` 在仓库中（已完成 ✅）
- [ ] 图片目录 `extracted_final/` 在仓库中（已完成 ✅）

---

## 📦 项目文件结构

```
ancient-characters-db/
├── app.py                    # Flask 后端
├── index.html                # 项目展示首页
├── char_detail.html          # 应用主页面
├── ancient_characters.db     # SQLite 数据库
├── extracted_final/          # 字形图片（45MB）
├── requirements.txt          # Python 依赖
├── Procfile                  # Heroku/Render 配置
├── render.yaml               # Render 配置
├── .env.example              # 环境变量示例
├── .gitignore                # Git 忽略文件
├── README.md                 # 项目说明
├── PROJECT_SHOWCASE.md       # 项目展示文档
└── API_DOCUMENTATION.md      # API 文档
```

---

## 🌐 部署后的 URL 结构

部署完成后，你的网站会有这样的结构：

```
https://your-domain.com/                    # 项目展示首页
https://your-domain.com/char_detail.html    # 应用主页面
https://your-domain.com/api/search?q=喜     # API 接口
```

---

## 💡 给 HR 看的最佳方式

部署完成后，给 HR 发这个链接：

```
https://your-domain.com/
```

这个首页会展示：
- 项目名称和简介
- 核心数据（839 个字头、5661 个字形）
- 技术栈
- 项目亮点
- "立即体验"按钮

HR 点击"立即体验"就能直接进入应用，无需任何配置。

---

## 🔗 绑定自定义域名（可选）

如果你想用自己的域名，比如 `yourname-portfolio.com`：

1. 在域名注册商（GoDaddy、阿里云等）购买域名
2. 在 Render/Railway 的设置中添加自定义域名
3. 按照指引配置 DNS 记录
4. 等待 DNS 生效（通常 24 小时内）

---

## 📊 部署后的监控

部署完成后，你可以：

- 在 Render/Railway 的仪表板查看日志
- 监控应用性能
- 查看错误信息
- 手动重启应用

---

## ⚠️ 常见问题

### Q: 图片无法加载怎么办？
A: 确保 `extracted_final/` 目录已上传到 GitHub，并且路径配置正确。

### Q: 数据库连接失败？
A: 检查 `ancient_characters.db` 是否在仓库中，以及环境变量 `DB_PATH` 是否正确。

### Q: 应用启动很慢？
A: 免费版本可能会休眠，首次访问需要等待。升级到付费版本可以避免这个问题。

### Q: 如何更新代码？
A: 本地修改代码后，推送到 GitHub：
```bash
git add .
git commit -m "Update message"
git push
```
Render/Railway 会自动检测并重新部署。

---

## 🎯 下一步

1. **创建 GitHub 仓库** - 如果还没有
2. **推送代码** - `git push -u origin main`
3. **连接 Render** - 按照上面的步骤
4. **等待部署** - 通常 5-10 分钟
5. **测试应用** - 访问生成的 URL
6. **分享给 HR** - 发送项目展示页的链接

---

## 📞 需要帮助？

如果部署过程中遇到问题，检查：

1. GitHub 仓库是否公开
2. `requirements.txt` 是否完整
3. Render/Railway 的构建日志
4. 环境变量是否正确配置

---

**准备好了吗？开始部署吧！** 🚀
