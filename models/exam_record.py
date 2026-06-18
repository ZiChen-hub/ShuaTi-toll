# models/exam_record.py
import json
import hashlib
import os
from datetime import datetime
from typing import List, Dict
from config import EXAM_RECORDS_FILE


class ExamRecord:
    """考试记录类"""
    def __init__(self):
        self.records = []
        self.load_records()
    
    def add_record(self, record: Dict):
        """添加考试记录"""
        record['id'] = hashlib.md5(f"{record['date']}{record['score']}".encode()).hexdigest()[:8]
        self.records.append(record)
        self.save_records()
    
    def get_records(self, limit: int = 20) -> List[Dict]:
        """获取最近的考试记录"""
        return sorted(self.records, key=lambda x: x['date'], reverse=True)[:limit]
    
    def get_statistics(self) -> Dict:
        """获取考试统计"""
        if not self.records:
            return {'total': 0, 'avg_score': 0, 'best_score': 0, 'total_time': 0}
        
        total = len(self.records)
        avg_score = sum(r['score'] for r in self.records) / total
        best_score = max(r['score'] for r in self.records)
        total_time = sum(r['time_spent'] for r in self.records)
        
        return {
            'total': total,
            'avg_score': round(avg_score, 2),
            'best_score': best_score,
            'total_time': total_time
        }
    
    def save_records(self):
        """保存记录到文件"""
        try:
            with open(EXAM_RECORDS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def load_records(self):
        """从文件加载记录"""
        try:
            if os.path.exists(EXAM_RECORDS_FILE):
                with open(EXAM_RECORDS_FILE, 'r', encoding='utf-8') as f:
                    self.records = json.load(f)
        except:
            self.records = []