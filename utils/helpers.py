# utils/helpers.py
import hashlib
import json
import os
from datetime import datetime
from typing import Dict, Any


def generate_id(prefix: str = "") -> str:
    """生成唯一ID"""
    timestamp = datetime.now().isoformat()
    return hashlib.md5(f"{prefix}{timestamp}".encode()).hexdigest()[:8]


def safe_json_load(filepath: str, default=None):
    """安全加载JSON文件"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return default or {}


def safe_json_save(filepath: str, data: Any):
    """安全保存JSON文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False


def format_time(seconds: int) -> str:
    """格式化时间"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def truncate_text(text: str, max_length: int = 50) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."