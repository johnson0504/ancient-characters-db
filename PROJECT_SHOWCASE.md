# 古文字库 - 项目展示站

这是一个完整的古文字数据库系统，包含 839 个字头、5661 个字形，支持 7 个朝代的字形演变查询。

## 🎯 项目亮点

### 核心功能
- **字头搜索** - 支持繁体字自动转换，快速查询任意字头
- **字形演变** - 按朝代分组展示字形演变过程（商、周、晋、楚、燕、秦、齐）
- **注释系统** - 完整的字头注释和来源管理
- **API 接口** - RESTful API 支持批量查询和数据导入

### 技术栈
- **后端** - Flask + SQLite3
- **前端** - HTML5 + CSS3 + JavaScript
- **数据库** - SQLite（2MB 核心数据 + 45MB 图片资源）
- **部署** - Python 3.8+

### 数据规模
- 字头总数：839 个
- 字形总数：5661 个
- 注释覆盖率：27.41%（230 条注释）
- 朝代覆盖：7 个历史朝代

## 📊 项目成果

### 已实现功能
✅ 完整的字头数据库（839 个字头）  
✅ 多朝代字形展示（7 个朝代）  
✅ 智能搜索和繁体转换  
✅ 注释管理系统（字头级注释 + 来源追踪）  
✅ RESTful API 接口  
✅ 批量数据导入功能  
✅ 响应式前端界面  

### 核心 API
```
GET  /api/search?q=<字符>              # 搜索字头
GET  /api/char/<char>/annotation       # 获取注释
POST /api/char/<char>/annotation       # 创建/更新注释
POST /api/annotations/batch            # 批量导入注释
GET  /health                           # 健康检查
```

## 🚀 快速开始

### 本地运行
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 访问
http://localhost:5000/char_detail.html
```

### 在线体验
访问部署后的在线链接即可直接使用，无需本地配置。

## 📁 项目结构
```
ancient-characters-db/
├── app.py                    # Flask 后端应用
├── char_detail.html          # 前端页面
├── ancient_characters.db     # SQLite 数据库
├── extracted_final/          # 字形图片资源
├── requirements.txt          # Python 依赖
├── API_DOCUMENTATION.md      # API 文档
├── ANNOTATION_GUIDE.md       # 注释使用指南
└── README.md                 # 项目说明
```

## 💡 技术亮点

### 1. 数据库设计
- 规范化的 SQLite 数据库结构
- 支持字头、字形、朝代、注释的完整关系
- 高效的查询性能

### 2. 前端交互
- 实时搜索和结果展示
- 按朝代分组的字形展示
- 注释的动态加载和编辑

### 3. API 设计
- RESTful 风格的接口设计
- 支持 CORS 跨域请求
- 完整的错误处理和验证

### 4. 数据处理
- 繁体字自动转换
- 特殊字符文件名处理
- 批量数据导入支持

## 📝 使用场景

- 古文字研究和学习
- 字形演变分析
- 历史文献查阅
- 教学和演示

## 🔗 相关链接

- [API 文档](API_DOCUMENTATION.md)
- [注释指南](ANNOTATION_GUIDE.md)
- [部署指南](DEPLOYMENT_GUIDE.md)
- [GitHub 仓库](https://github.com/YOUR_USERNAME/ancient-characters-db)

---

**项目状态** - 生产就绪 ✅  
**最后更新** - 2026-05-06  
**版本** - 1.0
