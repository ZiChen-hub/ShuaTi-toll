# models/question.py
from typing import List, Any


class Question:
    """题目类"""
    def __init__(self, qid: str, content: str, type: str, options: List[str],
                 answer: Any, explanation: str = "", category: str = ""):
        self.id = qid
        self.content = content
        self.type = type  # 'single', 'multiple', 'judge'
        self.options = options
        self.answer = answer
        self.explanation = explanation
        self.category = category
        self.wrong_count = 0
        self.last_wrong_time = None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'type': self.type,
            'options': self.options,
            'answer': self.answer,
            'explanation': self.explanation,
            'category': self.category,
            'wrong_count': self.wrong_count,
            'last_wrong_time': self.last_wrong_time
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建"""
        q = cls(
            qid=data['id'],
            content=data['content'],
            type=data['type'],
            options=data['options'],
            answer=data['answer'],
            explanation=data.get('explanation', ''),
            category=data.get('category', '')
        )
        q.wrong_count = data.get('wrong_count', 0)
        q.last_wrong_time = data.get('last_wrong_time')
        return q