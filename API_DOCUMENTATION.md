# 古文字数据库 API 文档

## 概述
- **数据库**: 796 个字头，7163 个字形
- **朝代**: 商、周、晋、楚、燕、秦、齐
- **更新时间**: 2026-04-27
- **繁体字支持**: 齊(齐)、週(周)

## API 端点

### 1. 搜索字头（所有朝代）
**GET** `/api/search?q=<字符>`

返回指定字头的所有朝代字形。支持繁体字。

**参数:**
- `q` (必需): 单个汉字（支持繁体字：齊→齐、週→周）

**响应示例:**
```json
{
  "char": "喜",
  "phonetic_group": "曉紐喜聲",
  "dynasties": [
    {
      "name": "商",
      "glyphs": [
        {
          "id": 1,
          "source_code": "合390臼",
          "variant_index": 0,
          "filename": "合390臼.png",
          "image_path": "/path/to/image",
          "annotation": null
        }
      ]
    }
  ]
}
```

### 2. 按朝代搜索
**GET** `/api/search-by-dynasty?q=<字符>&dynasty=<朝代>`

返回指定字头在特定朝代的字形。

**参数:**
- `q` (必需): 单个汉字
- `dynasty` (可选): 朝代名称（商、周、晋、楚、燕、秦、齐）

**响应示例:**
```json
{
  "char": "喜",
  "phonetic_group": "曉紐喜聲",
  "glyphs": [
    {
      "id": 1,
      "dynasty": "商",
      "source_code": "合390臼",
      "variant_index": 0,
      "filename": "合390臼.png",
      "image_path": "/path/to/image"
    }
  ]
}
```

### 3. 获取字形详情
**GET** `/api/glyph/<glyph_id>`

获取单个字形的详细信息。

**响应示例:**
```json
{
  "char": "喜",
  "dynasty": "商",
  "source_code": "合390臼",
  "variant_index": 0,
  "filename": "合390臼.png",
  "image_path": "/path/to/image",
  "annotation": null
}
```

### 4. 获取朝代列表
**GET** `/api/dynasties`

获取所有朝代信息。

**响应示例:**
```json
{
  "dynasties": [
    {"id": 1, "name": "商", "order": 1},
    {"id": 2, "name": "周", "order": 2},
    {"id": 3, "name": "晋", "order": 3},
    {"id": 4, "name": "楚", "order": 4},
    {"id": 5, "name": "燕", "order": 5},
    {"id": 6, "name": "秦", "order": 6},
    {"id": 7, "name": "齐", "order": 7}
  ]
}
```

### 5. 获取统计信息
**GET** `/api/stats`

获取数据库统计信息。

**响应示例:**
```json
{
  "total_characters": 796,
  "total_dynasties": 7,
  "total_forms": 7163,
  "forms_by_dynasty": {
    "商": 2741,
    "周": 0,
    "晋": 494,
    "楚": 1666,
    "燕": 140,
    "秦": 646,
    "齐": 0
  }
}
```

### 6. 列出所有字头
**GET** `/api/characters`

获取所有字头列表。

**响应示例:**
```json
{
  "characters": [
    {"char": "㘽", "phonetic": "未分类"},
    {"char": "㚦", "phonetic": "未分类"},
    {"char": "喜", "phonetic": "曉紐喜聲"}
  ]
}
```

### 7. 获取字形图片
**GET** `/images/<filename>`

获取字形图片文件。

**参数:**
- `filename`: 图片文件名（如 `合390臼.png`）

### 8. 获取字头注释
**GET** `/api/char/<char>/annotation`

获取指定字头的注释和来源。

**参数:**
- `char` (必需): 单个汉字

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
    ]
  }
}
```

### 9. 创建/更新字头注释
**POST** `/api/char/<char>/annotation`

创建或更新字头的注释。

**参数:**
- `char` (必需): 单个汉字

**请求体:**
```json
{
  "annotation_text": "【注】从㞢得声...",
  "sources": [
    {
      "type": "文献",
      "text": "《说文》：'喜，乐也。'",
      "sort_order": 1
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

### 10. 批量导入注释
**POST** `/api/annotations/batch`

批量导入多个字头的注释。

**请求体:**
```json
{
  "items": [
    {
      "char": "喜",
      "annotation_text": "【注】从㞢得声...",
      "sources": [
        {
          "type": "文献",
          "text": "《说文》：'喜，乐也。'",
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
  "imported": 1,
  "failed": 0,
  "message": "已导入 1 条注释"
}
```

### 11. 健康检查
**GET** `/health`

检查 API 服务状态。

**响应:**
```json
{"status": "ok"}
```

## 错误响应

所有错误响应都返回 JSON 格式：

```json
{"error": "错误描述"}
```

常见错误码：
- `400`: 请求参数错误
- `404`: 资源不存在
- `500`: 服务器错误

## 使用示例

### Python
```python
import requests

# 搜索字头
response = requests.get('http://localhost:5000/api/search?q=喜')
data = response.json()
print(f"字头: {data['char']}")
print(f"朝代数: {len(data['dynasties'])}")

# 按朝代搜索
response = requests.get('http://localhost:5000/api/search-by-dynasty?q=喜&dynasty=商')
glyphs = response.json()['glyphs']
print(f"商朝字形数: {len(glyphs)}")
```

### JavaScript
```javascript
// 搜索字头
fetch('/api/search?q=喜')
  .then(r => r.json())
  .then(data => {
    console.log(`字头: ${data.char}`);
    console.log(`朝代数: ${data.dynasties.length}`);
  });

// 获取统计信息
fetch('/api/stats')
  .then(r => r.json())
  .then(data => {
    console.log(`总字头: ${data.total_characters}`);
    console.log(`总字形: ${data.total_forms}`);
  });
```

## 启动服务

```bash
cd /home/openclaw/.openclaw/workspace
python3 app.py
```

服务将在 `http://localhost:5000` 启动。

## 数据库表结构

### characters（字头表）
- `id`: 主键
- `simplified_char`: 简化字
- `phonetic_group`: 拼音分组

### character_forms（字形表）
- `id`: 主键
- `character_id`: 字头 ID
- `dynasty_id`: 朝代 ID
- `source_code`: 出处编码（如 "合390臼"）
- `variant_index`: 变体索引
- `filename`: 图片文件名
- `image_path`: 图片路径
- `annotation`: 字形级别的注释（可选）

### character_annotations（字头注释表）
- `id`: 主键
- `character_id`: 字头 ID（唯一）
- `annotation_text`: 注释文本（【注】部分）
- `created_at`: 创建时间
- `updated_at`: 更新时间

### annotation_sources（注释来源表）
- `id`: 主键
- `annotation_id`: 注释 ID
- `source_type`: 来源类型（文献、出处、引用等）
- `source_text`: 来源文本
- `sort_order`: 排序顺序
- `created_at`: 创建时间

## 数据更新

数据库已更新至最新版本：
- 新增字头: 113 个
- 更新字头: 333 个
- 总字头: 796 个
- 总字形: 7163 个
- 注释覆盖率: 0%（待导入）
