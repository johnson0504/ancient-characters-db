#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# 支持环境变量配置路径
DB_PATH = os.getenv('DB_PATH', "/home/openclaw/.openclaw/workspace/ancient_characters.db")
DATA_DIR = os.getenv('DATA_DIR', "/home/openclaw/.openclaw/workspace/extracted_final_v7")
GLYPH_DIR = os.path.join(DATA_DIR, "字形图片")

# 获取端口
PORT = int(os.getenv('PORT', 5000))

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """主页"""
    return send_file('index.html')

# 朝代标记映射（图片形式）
DYNASTY_MARKERS = {
    'rId30': '商', 
    'rId35': '楚', 
    'rId46': '燕',
    'rId52': '晋', 
    'rId57': '秦', 
    'rId70': '周',
}

# 朝代名称映射（文字形式，包括繁体）
DYNASTY_NAMES = {
    '商': '商',
    '周': '周',
    '晋': '晋',
    '晉': '晋',  # 繁体
    '楚': '楚',
    '燕': '燕',
    '秦': '秦',
    '齐': '齐',
    '齊': '齐',  # 繁体
}

TRADITIONAL_TO_SIMPLIFIED = {
    '齊': '齐',
    '晉': '晋',
    '週': '周',
}

@app.route('/api/search', methods=['GET'])
def search():
    """搜索字头，返回所有朝代的字形"""
    char = request.args.get('q', '').strip()
    
    if not char or len(char) != 1:
        return jsonify({'error': '请输入单个字符'}), 400
    
    char = TRADITIONAL_TO_SIMPLIFIED.get(char, char)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, simplified_char, phonetic_group
    FROM characters
    WHERE simplified_char = ?
    """, (char,))
    
    char_row = cursor.fetchone()
    if not char_row:
        conn.close()
        return jsonify({'error': '未找到该字'}), 404
    
    char_id = char_row['id']
    
    # 查询所有朝代的字形
    cursor.execute("""
    SELECT 
        d.dynasty_name,
        d.dynasty_order,
        cf.id,
        cf.source_code,
        cf.variant_index,
        cf.filename,
        cf.image_path,
        cf.annotation
    FROM character_forms cf
    JOIN dynasties d ON cf.dynasty_id = d.id
    WHERE cf.character_id = ?
    ORDER BY d.dynasty_order, cf.source_code, cf.variant_index
    """, (char_id,))
    
    forms = cursor.fetchall()
    conn.close()
    
    if not forms:
        return jsonify({'error': '未找到字形'}), 404
    
    # 按朝代分组
    dynasties_dict = {}
    for form in forms:
        dynasty = form['dynasty_name']
        if dynasty not in dynasties_dict:
            dynasties_dict[dynasty] = {
                'order': form['dynasty_order'],
                'glyphs': []
            }
        
        glyph = {
            'id': form['id'],
            'source_code': form['source_code'],
            'variant_index': form['variant_index'],
            'filename': form['filename'],
            'image_path': form['image_path'],
            'annotation': form['annotation']
        }
        dynasties_dict[dynasty]['glyphs'].append(glyph)
    
    # 按朝代顺序排序（修复：确保朝代顺序正确）
    dynasty_order = ['商', '周', '晋', '楚', '燕', '秦', '齐']
    dynasties = []
    for dynasty_name in dynasty_order:
        if dynasty_name in dynasties_dict:
            dynasties.append({
                'name': dynasty_name,
                'glyphs': dynasties_dict[dynasty_name]['glyphs']
            })
    
    return jsonify({
        'char': char_row['simplified_char'],
        'phonetic_group': char_row['phonetic_group'],
        'dynasties': dynasties
    })

@app.route('/api/glyph/<int:glyph_id>', methods=['GET'])
def get_glyph(glyph_id):
    """获取单个字形的详细信息"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 
        c.simplified_char,
        d.dynasty_name,
        cf.source_code,
        cf.variant_index,
        cf.filename,
        cf.image_path,
        cf.annotation
    FROM character_forms cf
    JOIN characters c ON cf.character_id = c.id
    JOIN dynasties d ON cf.dynasty_id = d.id
    WHERE cf.id = ?
    """, (glyph_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({'error': '未找到字形'}), 404
    
    return jsonify({
        'char': row['simplified_char'],
        'dynasty': row['dynasty_name'],
        'source_code': row['source_code'],
        'variant_index': row['variant_index'],
        'filename': row['filename'],
        'image_path': row['image_path'],
        'annotation': row['annotation']
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """获取统计信息"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM characters")
    char_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM dynasties")
    dynasty_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM character_forms")
    form_count = cursor.fetchone()[0]
    
    cursor.execute("""
    SELECT d.dynasty_name, COUNT(*) as count
    FROM character_forms cf
    JOIN dynasties d ON cf.dynasty_id = d.id
    GROUP BY d.dynasty_name
    ORDER BY d.dynasty_order
    """)
    
    dynasty_stats = {row[0]: row[1] for row in cursor.fetchall()}
    
    # 统计注释覆盖率
    cursor.execute("SELECT COUNT(*) FROM character_annotations")
    annotation_count = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_characters': char_count,
        'total_dynasties': dynasty_count,
        'total_forms': form_count,
        'forms_by_dynasty': dynasty_stats,
        'annotation_coverage': annotation_count
    })

@app.route('/api/characters', methods=['GET'])
def list_characters():
    """列出所有字头"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT simplified_char, phonetic_group
    FROM characters
    ORDER BY simplified_char
    """)
    
    chars = [{'char': row[0], 'phonetic': row[1]} for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'characters': chars})

@app.route('/api/dynasties', methods=['GET'])
def get_dynasties():
    """获取所有朝代列表"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, dynasty_name, dynasty_order
    FROM dynasties
    ORDER BY dynasty_order
    """)
    
    dynasties = [{'id': row[0], 'name': row[1], 'order': row[2]} for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'dynasties': dynasties})

@app.route('/api/search-by-dynasty', methods=['GET'])
def search_by_dynasty():
    """按朝代搜索字形"""
    char = request.args.get('q', '').strip()
    dynasty = request.args.get('dynasty', '').strip()
    
    if not char or len(char) != 1:
        return jsonify({'error': '请输入单个字符'}), 400
    
    char = TRADITIONAL_TO_SIMPLIFIED.get(char, char)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, simplified_char, phonetic_group
    FROM characters
    WHERE simplified_char = ?
    """, (char,))
    
    char_row = cursor.fetchone()
    if not char_row:
        conn.close()
        return jsonify({'error': '未找到该字'}), 404
    
    char_id = char_row['id']
    
    # 查询指定朝代的字形
    if dynasty:
        cursor.execute("""
        SELECT 
            d.dynasty_name,
            cf.id,
            cf.source_code,
            cf.variant_index,
            cf.filename,
            cf.image_path
        FROM character_forms cf
        JOIN dynasties d ON cf.dynasty_id = d.id
        WHERE cf.character_id = ? AND d.dynasty_name = ?
        ORDER BY cf.variant_index
        """, (char_id, dynasty))
    else:
        cursor.execute("""
        SELECT 
            d.dynasty_name,
            cf.id,
            cf.source_code,
            cf.variant_index,
            cf.filename,
            cf.image_path
        FROM character_forms cf
        JOIN dynasties d ON cf.dynasty_id = d.id
        WHERE cf.character_id = ?
        ORDER BY d.dynasty_order, cf.variant_index
        """, (char_id,))
    
    forms = cursor.fetchall()
    conn.close()
    
    if not forms:
        return jsonify({'error': '未找到字形'}), 404
    
    glyphs = [{
        'id': form[1],
        'dynasty': form[0],
        'source_code': form[2],
        'variant_index': form[3],
        'filename': form[4],
        'image_path': form[5]
    } for form in forms]
    
    return jsonify({
        'char': char_row['simplified_char'],
        'phonetic_group': char_row['phonetic_group'],
        'glyphs': glyphs
    })

# ============ 注释相关接口 ============

@app.route('/api/char/<char>/annotation', methods=['GET'])
def get_annotation(char):
    """获取字头注释"""
    char = TRADITIONAL_TO_SIMPLIFIED.get(char, char)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 查询字头
    cursor.execute("SELECT id FROM characters WHERE simplified_char = ?", (char,))
    char_row = cursor.fetchone()
    
    if not char_row:
        conn.close()
        return jsonify({'error': '未找到该字'}), 404
    
    char_id = char_row[0]
    
    # 查询注释
    cursor.execute("""
    SELECT id, annotation_text, created_at, updated_at
    FROM character_annotations
    WHERE character_id = ?
    """, (char_id,))
    
    annotation_row = cursor.fetchone()
    
    if not annotation_row:
        conn.close()
        return jsonify({
            'char': char,
            'annotation': None
        })
    
    annotation_id = annotation_row[0]
    
    # 查询注释来源
    cursor.execute("""
    SELECT id, source_type, source_text, sort_order
    FROM annotation_sources
    WHERE annotation_id = ?
    ORDER BY sort_order
    """, (annotation_id,))
    
    sources = [{
        'id': row[0],
        'type': row[1],
        'text': row[2],
        'order': row[3]
    } for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'char': char,
        'annotation': {
            'id': annotation_row[0],
            'text': annotation_row[1],
            'sources': sources,
            'created_at': annotation_row[2],
            'updated_at': annotation_row[3]
        }
    })

@app.route('/api/char/<char>/annotation', methods=['POST'])
def create_or_update_annotation(char):
    """创建或更新字头注释"""
    char = TRADITIONAL_TO_SIMPLIFIED.get(char, char)
    data = request.get_json()
    
    if not data or 'annotation_text' not in data:
        return jsonify({'error': '缺少 annotation_text 字段'}), 400
    
    annotation_text = data['annotation_text'].strip()
    sources = data.get('sources', [])
    
    if not annotation_text:
        return jsonify({'error': 'annotation_text 不能为空'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # 查询字头
        cursor.execute("SELECT id FROM characters WHERE simplified_char = ?", (char,))
        char_row = cursor.fetchone()
        
        if not char_row:
            conn.close()
            return jsonify({'error': '未找到该字'}), 404
        
        char_id = char_row[0]
        
        # 检查是否已存在注释
        cursor.execute("SELECT id FROM character_annotations WHERE character_id = ?", (char_id,))
        existing = cursor.fetchone()
        
        if existing:
            # 更新
            annotation_id = existing[0]
            cursor.execute("""
            UPDATE character_annotations
            SET annotation_text = ?, updated_at = ?
            WHERE id = ?
            """, (annotation_text, datetime.now().isoformat(), annotation_id))
            
            # 删除旧的来源
            cursor.execute("DELETE FROM annotation_sources WHERE annotation_id = ?", (annotation_id,))
        else:
            # 创建新注释
            cursor.execute("""
            INSERT INTO character_annotations (character_id, annotation_text, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """, (char_id, annotation_text, datetime.now().isoformat(), datetime.now().isoformat()))
            
            annotation_id = cursor.lastrowid
        
        # 插入来源
        for idx, source in enumerate(sources):
            cursor.execute("""
            INSERT INTO annotation_sources (annotation_id, source_type, source_text, sort_order)
            VALUES (?, ?, ?, ?)
            """, (annotation_id, source.get('type', ''), source.get('text', ''), idx + 1))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'annotation_id': annotation_id,
            'message': '注释已保存'
        })
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/annotations/batch', methods=['POST'])
def batch_import_annotations():
    """批量导入注释"""
    data = request.get_json()
    
    if not data or 'items' not in data:
        return jsonify({'error': '缺少 items 字段'}), 400
    
    items = data['items']
    imported = 0
    failed = 0
    errors = []
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        for item in items:
            char = item.get('char', '').strip()
            annotation_text = item.get('annotation_text', '').strip()
            sources = item.get('sources', [])
            
            if not char or not annotation_text:
                failed += 1
                errors.append(f"字 '{char}' 缺少必要字段")
                continue
            
            char = TRADITIONAL_TO_SIMPLIFIED.get(char, char)
            
            try:
                # 查询字头
                cursor.execute("SELECT id FROM characters WHERE simplified_char = ?", (char,))
                char_row = cursor.fetchone()
                
                if not char_row:
                    failed += 1
                    errors.append(f"字 '{char}' 不存在")
                    continue
                
                char_id = char_row[0]
                
                # 检查是否已存在
                cursor.execute("SELECT id FROM character_annotations WHERE character_id = ?", (char_id,))
                existing = cursor.fetchone()
                
                if existing:
                    annotation_id = existing[0]
                    cursor.execute("""
                    UPDATE character_annotations
                    SET annotation_text = ?, updated_at = ?
                    WHERE id = ?
                    """, (annotation_text, datetime.now().isoformat(), annotation_id))
                    
                    cursor.execute("DELETE FROM annotation_sources WHERE annotation_id = ?", (annotation_id,))
                else:
                    cursor.execute("""
                    INSERT INTO character_annotations (character_id, annotation_text, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """, (char_id, annotation_text, datetime.now().isoformat(), datetime.now().isoformat()))
                    
                    annotation_id = cursor.lastrowid
                
                # 插入来源
                for idx, source in enumerate(sources):
                    cursor.execute("""
                    INSERT INTO annotation_sources (annotation_id, source_type, source_text, sort_order)
                    VALUES (?, ?, ?, ?)
                    """, (annotation_id, source.get('type', ''), source.get('text', ''), idx + 1))
                
                imported += 1
            
            except Exception as e:
                failed += 1
                errors.append(f"字 '{char}' 导入失败: {str(e)}")
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'imported': imported,
            'failed': failed,
            'errors': errors if errors else None,
            'message': f'已导入 {imported} 条注释'
        })
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/images/<path:filepath>', methods=['GET'])
def serve_image(filepath):
    """提供字形图片"""
    # 方案 1: 直接从 GLYPH_DIR 查找
    full_path = os.path.join(GLYPH_DIR, filepath)
    if os.path.exists(full_path):
        return send_file(full_path)
    
    # 方案 2: 从数据库查询完整路径（处理特殊字符文件名）
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT image_path FROM character_forms WHERE filename = ? LIMIT 1", (filepath,))
    row = cursor.fetchone()
    conn.close()
    
    if row and row[0] and os.path.exists(row[0]):
        return send_file(row[0])
    
    return jsonify({'error': '图片不存在'}), 404

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=PORT)
