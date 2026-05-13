# 古文字库 - 注释功能使用指南

## 📋 概述

本文档说明如何使用古文字库的注释功能。注释功能包括：
- 字头级别的注释管理（【注】部分）
- 注释来源管理（文献、出处等）
- 批量导入注释
- 前端展示

---

## 🗄️ 数据库结构

### 新增表

#### `character_annotations` - 字头注释表
```sql
CREATE TABLE character_annotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNIQUE NOT NULL,  -- 字头 ID
    annotation_text TEXT NOT NULL,         -- 【注】的完整文本
    created_at TIMESTAMP,                  -- 创建时间
    updated_at TIMESTAMP,                  -- 更新时间
    FOREIGN KEY(character_id) REFERENCES characters(id)
);
```

#### `annotation_sources` - 注释来源表
```sql
CREATE TABLE annotation_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    annotation_id INTEGER NOT NULL,        -- 注释 ID
    source_type TEXT NOT NULL,             -- 来源类型（文献、出处等）
    source_text TEXT NOT NULL,             -- 来源文本
    sort_order INTEGER DEFAULT 0,          -- 排序顺序
    created_at TIMESTAMP,                  -- 创建时间
    FOREIGN KEY(annotation_id) REFERENCES character_annotations(id)
);
```

---

## 🔌 API 接口

### 1. 获取字头注释
```
GET /api/char/<char>/annotation
```

**参数:**
- `char`: 单个汉字（支持繁体字）

**响应示例:**
```json
{
  "char": "喜",
  "annotation": {
    "id": 1,
    "text": "【注】从㞢得声，疑'维'之繁文。●雪霄'宋□'夜□人名。",
    "sources": [
      {
        "id": 1,
        "type": "文献",
        "text": "《说文》：'喜，乐也。'",
        "order": 1
      },
      {
        "id": 2,
        "type": "出处",
        "text": "《四十二年逑鼎》...",
        "order": 2
      }
    ],
    "created_at": "2026-05-06T10:13:00",
    "updated_at": "2026-05-06T10:13:00"
  }
}
```

**无注释时的响应:**
```json
{
  "char": "喜",
  "annotation": null
}
```

---

### 2. 创建/更新字头注释
```
POST /api/char/<char>/annotation
```

**参数:**
- `char`: 单个汉字

**请求体:**
```json
{
  "annotation_text": "【注】从㞢得声，疑'维'之繁文。●雪霄'宋□'夜□人名。",
  "sources": [
    {
      "type": "文献",
      "text": "《说文》：'喜，乐也。'",
      "sort_order": 1
    },
    {
      "type": "出处",
      "text": "《四十二年逑鼎》...",
      "sort_order": 2
    }
  ]
}
```

**响应:**
```json
{
  "success": true,
  "annotation_id": 1,
  "message": "注释已保存"
}
```

---

### 3. 批量导入注释
```
POST /api/annotations/batch
```

**请求体:**
```json
{
  "items": [
    {
      "char": "喜",
      "annotation_text": "【注】从㞢得声，疑'维'之繁文。",
      "sources": [
        {
          "type": "文献",
          "text": "《说文》：'喜，乐也。'",
          "sort_order": 1
        }
      ]
    },
    {
      "char": "愙",
      "annotation_text": "【注】从心喜声。",
      "sources": [
        {
          "type": "文献",
          "text": "《说文》：'愙，乐也。'",
          "sort_order": 1
        }
      ]
    }
  ]
}
```

**响应:**
```json
{
  "success": true,
  "imported": 2,
  "failed": 0,
  "errors": null,
  "message": "已导入 2 条注释"
}
```

---

## 🖥️ 前端页面

### 文件位置
`/home/openclaw/.openclaw/workspace/char_detail.html`

### 功能
1. **搜索栏** - 输入单个汉字搜索
2. **字头信息** - 显示字头、拼音分组、字形总数
3. **注释区块** - 显示【注】和来源
4. **字形演变** - 按朝代分组显示字形图片

### 使用方式
1. 启动 Flask 服务：
   ```bash
   cd /home/openclaw/.openclaw/workspace
   python3 app.py
   ```

2. 打开浏览器访问：
   ```
   http://localhost:5000/char_detail.html
   ```

3. 输入汉字搜索

---

## 📝 使用示例

### Python 示例

#### 获取注释
```python
import requests

response = requests.get('http://localhost:5000/api/char/喜/annotation')
data = response.json()
print(data['annotation']['text'])
```

#### 创建注释
```python
import requests

data = {
    "annotation_text": "【注】从㞢得声，疑'维'之繁文。",
    "sources": [
        {
            "type": "文献",
            "text": "《说文》：'喜，乐也。'"
        }
    ]
}

response = requests.post('http://localhost:5000/api/char/喜/annotation', json=data)
print(response.json())
```

#### 批量导入
```python
import requests
import json

with open('annotations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

response = requests.post('http://localhost:5000/api/annotations/batch', json=data)
print(response.json())
```

### JavaScript 示例

#### 获取注释
```javascript
fetch('/api/char/喜/annotation')
  .then(r => r.json())
  .then(data => {
    console.log(data.annotation.text);
  });
```

#### 创建注释
```javascript
const data = {
  annotation_text: "【注】从㞢得声，疑'维'之繁文。",
  sources: [
    {
      type: "文献",
      text: "《说文》：'喜，乐也。'"
    }
  ]
};

fetch('/api/char/喜/annotation', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 🧪 测试

运行测试脚本：
```bash
cd /home/openclaw/.openclaw/workspace

# 先启动 Flask 服务（另一个终端）
python3 app.py

# 运行测试
python3 test_annotation_api.py
```

---

## 📊 统计信息

获取注释覆盖率：
```bash
curl http://localhost:5000/api/stats
```

响应包含：
- `total_characters`: 总字头数
- `total_forms`: 总字形数
- `annotation_coverage`: 已有注释的字头数

---

## 🔄 迁移脚本

如果需要重新运行迁移：
```bash
cd /home/openclaw/.openclaw/workspace
python3 migrations/run_migration.py
```

---

## ⚠️ 注意事项

1. **字头唯一性** - 每个字头只能有一条注释记录（`character_id` 是 UNIQUE）
2. **繁体字支持** - API 自动转换繁体字（齊→齐、週→周）
3. **来源排序** - 来源按 `sort_order` 排序，从小到大
4. **时间戳** - 所有时间戳使用 ISO 8601 格式

---

## 📁 文件清单

| 文件 | 说明 |
|------|------|
| `app.py` | Flask 应用（已更新，包含注释接口） |
| `char_detail.html` | 前端页面 |
| `API_DOCUMENTATION.md` | API 文档 |
| `migrations/add_annotation_tables.sql` | 数据库迁移脚本 |
| `migrations/run_migration.py` | 迁移执行脚本 |
| `test_annotation_api.py` | 测试脚本 |

---

## 🚀 下一步

1. ✅ 数据库表已创建
2. ✅ API 接口已实现
3. ✅ 前端页面已完成
4. ⏳ 需要导入注释数据

### 导入注释数据

准备 JSON 文件 `annotations.json`：
```json
{
  "items": [
    {
      "char": "喜",
      "annotation_text": "【注】从㞢得声...",
      "sources": [...]
    }
  ]
}
```

然后运行：
```bash
python3 << 'EOF'
import requests
import json

with open('annotations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

response = requests.post('http://localhost:5000/api/annotations/batch', json=data)
print(response.json())
EOF
```

---

## 📞 常见问题

**Q: 如何更新已有的注释？**
A: 使用 POST 接口，系统会自动检测并更新。

**Q: 如何删除注释？**
A: 目前没有删除接口，可以直接操作数据库或联系管理员。

**Q: 注释支持 HTML 吗？**
A: 不支持，所有内容都会被转义为纯文本。

**Q: 如何导出注释？**
A: 可以直接查询数据库或使用 API 逐个获取。

---

## 📞 技术支持

如有问题，请检查：
1. Flask 服务是否正常运行
2. 数据库连接是否正常
3. 迁移脚本是否成功执行
4. 浏览器控制台是否有错误信息
