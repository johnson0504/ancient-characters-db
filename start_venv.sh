#!/bin/bash
# 快速启动脚本 - 使用虚拟环境

set -e

WORKSPACE="/home/openclaw/.openclaw/workspace"
VENV_PATH="$WORKSPACE/venv_ancient"
DB_PATH="$WORKSPACE/ancient_characters.db"

echo "🚀 古文字库 - 快速启动"
echo "========================"

# 检查数据库
if [ ! -f "$DB_PATH" ]; then
    echo "❌ 数据库不存在: $DB_PATH"
    exit 1
fi

echo "✅ 数据库已找到"

# 创建虚拟环境（如果不存在）
if [ ! -d "$VENV_PATH" ]; then
    echo ""
    echo "📦 创建虚拟环境..."
    python3 -m venv "$VENV_PATH"
    echo "✅ 虚拟环境已创建"
fi

# 激活虚拟环境
echo ""
echo "🔧 激活虚拟环境..."
source "$VENV_PATH/bin/activate"

# 安装依赖
echo ""
echo "📚 检查依赖..."
pip install -q flask flask-cors 2>/dev/null && echo "✅ 依赖已安装" || {
    echo "⚠️  安装依赖..."
    pip install flask flask-cors
    echo "✅ 依赖已安装"
}

# 检查迁移
echo ""
echo "检查数据库表..."
python3 << 'EOF'
import sqlite3

db_path = "/home/openclaw/.openclaw/workspace/ancient_characters.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查表是否存在
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('character_annotations', 'annotation_sources')")
tables = cursor.fetchall()

if len(tables) == 2:
    print("✅ 注释表已存在")
else:
    print("⚠️  注释表不存在，正在创建...")
    
    # 执行迁移
    with open('/home/openclaw/.openclaw/workspace/migrations/add_annotation_tables.sql', 'r', encoding='utf-8') as f:
        migration_sql = f.read()
    
    cursor.executescript(migration_sql)
    conn.commit()
    print("✅ 注释表已创建")

conn.close()
EOF

# 启动服务
echo ""
echo "========================"
echo "🌐 启动 Flask 服务..."
echo "📍 访问地址: http://localhost:5000"
echo "📄 详情页面: http://localhost:5000/char_detail.html"
echo "📚 API 文档: http://localhost:5000/api/stats"
echo "========================"
echo ""

cd "$WORKSPACE"
python3 app.py
