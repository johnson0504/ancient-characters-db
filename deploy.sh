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
