# database/wrong_bank.py
import json
import os
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Optional
from models.question import Question
from config import WRONG_QUESTIONS_FILE


class WrongQuestionBank:
    """错题库类"""
    def __init__(self):
        self.wrong_questions: Dict[str, Question] = {}
        self.wrong_stats = defaultdict(int)
        self.load_wrong_questions()
    
    def add_wrong(self, question: Question):
        """添加错题"""
        if question.id not in self.wrong_questions:
            self.wrong_questions[question.id] = question
            question.wrong_count = 1
        else:
            self.wrong_questions[question.id].wrong_count += 1
        
        self.wrong_stats[question.type] += 1
        self.wrong_stats['total'] += 1
        question.last_wrong_time = datetime.now().isoformat()
        self.save_wrong_questions()
    
    def remove_correct(self, question: Question):
        """移除已掌握的错题"""
        if question.id in self.wrong_questions:
            del self.wrong_questions[question.id]
            self.wrong_stats[question.type] -= 1
            self.wrong_stats['total'] -= 1
            self.save_wrong_questions()
    
    def get_wrong_questions(self, category: str = None, q_type: str = None) -> List[Question]:
        """获取错题"""
        questions = list(self.wrong_questions.values())
        
        if category and category != '全部':
            questions = [q for q in questions if q.category == category]
        
        if q_type and q_type != '全部':
            questions = [q for q in questions if q.type == q_type]
        
        return questions
    
    def get_statistics(self) -> Dict:
        """获取错题统计"""
        categories = defaultdict(int)
        for q in self.wrong_questions.values():
            categories[q.category] += 1
        
        return {
            'total': len(self.wrong_questions),
            'by_type': dict(self.wrong_stats),
            'by_category': dict(categories)
        }
    
    def save_wrong_questions(self):
        """保存错题到文件"""
        try:
            data = [q.to_dict() for q in self.wrong_questions.values()]
            with open(WRONG_QUESTIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def load_wrong_questions(self):
        """从文件加载错题"""
        try:
            if os.path.exists(WRONG_QUESTIONS_FILE):
                with open(WRONG_QUESTIONS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item in data:
                    q = Question.from_dict(item)
                    self.wrong_questions[q.id] = q
                    self.wrong_stats[q.type] = self.wrong_stats.get(q.type, 0) + 1
                    self.wrong_stats['total'] = self.wrong_stats.get('total', 0) + 1
        except:
            pass