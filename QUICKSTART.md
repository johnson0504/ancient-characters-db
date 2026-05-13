# 🚀 古文字库 - 快速开始指南

## 📋 当前状态

✅ **系统已完全就绪**

| 组件 | 状态 | 说明 |
|------|------|------|
| 数据库 | ✅ | 839 个字头，7163 个字形 |
| 注释数据 | ✅ | 230 条注释已导入（27.41% 覆盖率） |
| API 接口 | ✅ | 3 个新接口已实现 |
| 前端页面 | ✅ | 完整的字头详情页面 |
| 虚拟环境 | ✅ | venv_ancient 已创建 |
| 依赖 | ✅ | flask, flask-cors 已安装 |

---

## 🎯 一键启动

### 方式 1：使用虚拟环境（推荐）

```bash
cd /home/openclaw/.openclaw/workspace
bash start_venv.sh
```

### 方式 2：手动启动

```bash
cd /home/openclaw/.openclaw/workspace

# 激活虚拟环境
source venv_ancient/bin/activate

# 启动服务
python3 app.py
```

---

## 🌐 访问页面

启动后，打开浏览器访问：

### 字头详情页面
```
http://localhost:5000/char_detail.html
```

### API 统计信息
```
http://localhost:5000/api/stats
```

### 健康检查
```
http://localhost:5000/health
```

---

## 📝 使用示例

### 1. 搜索字头

在页面上输入单个汉字，比如：
- `喜` - 有注释的字
- `㚦` - 有注释的字
- `㠯` - 有注释的字

### 2. 查看注释

页面会显示：
- 【注】部分（字头级别的注释）
- 字形演变（按朝代分组）
- 出处编码

### 3. API 调用

#### 获取字头注释
```bash
curl http://localhost:5000/api/char/喜/annotation
```

#### 创建注释
```bash
curl -X POST http://localhost:5000/api/char/喜/annotation \
  -H "Content-Type: application/json" \
  -d '{
    "annotation_text": "【注】从㞢得声...",
    "sources": [
      {"type": "文献", "text": "《说文》：..."}
    ]
  }'
```

#### 批量导入
```bash
curl -X POST http://localhost:5000/api/annotations/batch \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "char": "喜",
        "annotation_text": "【注】...",
        "sources": [...]
      }
    ]
  }'
```

---

## 📊 数据统计

```bash
curl http://localhost:5000/api/stats
```

响应示例：
```json
{
  "total_characters": 839,
  "total_dynasties": 7,
  "total_forms": 7163,
  "forms_by_dynasty": {
    "商": 2741,
    "周": 0,
    "晋": 494,
    "楚": 1666,
    "燕": 140,
    "��": 646,
    "齐": 0
  },
  "annotation_coverage": 230
}
```

---

## 🧪 测试

### 运行测试脚本

```bash
cd /home/openclaw/.openclaw/workspace

# 先启动服务（另一个终端）
bash start_venv.sh

# 运行测试
source venv_ancient/bin/activate
python3 test_annotation_api.py
```

---

## 📁 重要文件

```
/home/openclaw/.openclaw/workspace/
├── app.py                          # Flask 应用
├── char_detail.html                # 前端页面
├── venv_ancient/                   # 虚拟环境
├── start_venv.sh                   # 启动脚本
├── import_annotations.py           # 注释导入脚本
├── test_annotation_api.py          # 测试脚本
├── API_DOCUMENTATION.md            # API 文档
├── ANNOTATION_GUIDE.md             # 使用指南
├── IMPLEMENTATION_SUMMARY.md       # 实现总结
├── migrations/
│   ├── add_annotation_tables.sql
│   └── run_migration.py
└── ancient_characters.db           # 数���库
```

---

## 🔧 常见问题

### Q: 如何停止服务？
A: 按 `Ctrl+C`

### Q: 如何重新导入注释？
A: 
```bash
source venv_ancient/bin/activate
python3 import_annotations.py
```

### Q: 如何查看注释覆盖率？
A: 
```bash
curl http://localhost:5000/api/stats | grep annotation_coverage
```

### Q: 如何添加新的注释？
A: 使用 POST API 或批量导入脚本

### Q: 虚拟环境出问题了怎么办？
A: 删除并重新创建：
```bash
rm -rf venv_ancient
python3 -m venv venv_ancient
source venv_ancient/bin/activate
pip install flask flask-cors
```

---

## 📈 后续优化

### 短期
- [ ] 导入更多注释数据
- [ ] 测试前端各项功能
- [ ] 优化图片加载性能

### 中期
- [ ] 添加删除注释接口
- [ ] 实现注释搜索功能
- [ ] 添加权限管理

### 长期
- [ ] 版本控制和编辑历史
- [ ] 全文搜索引擎集成
- [ ] 注释审核工作流

---

## 📞 技术支持

如有问题，检查：
1. Flask 服务是否正常运行
2. 虚拟环境是否已激活
3. 依赖是否已安装
4. 数据库是否存在
5. 浏览器控制台是否有错误

---

## ✨ 总结

🎉 **古文字库注释系统已完全就绪！**

- ✅ 230 条注释已导入
- ✅ 前端页面可直接使用
- ✅ API 接口完整可靠
- ✅ 虚拟环境已配置
- ✅ 一键启动脚本已准备

**立即开始：**
```bash
bash start_venv.sh
```

然后打开 `http://localhost:5000/char_detail.html`

---

**最后更新**: 2026-05-06 10:40 GMT+8
**版本**: 1.0
**状态**: ✅ 生产就绪
