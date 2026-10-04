# database/question_bank.py
import json
import random
from typing import List, Dict, Set, Optional
from models.question import Question


class QuestionBank:
    """通用题库管理类"""
    def __init__(self):
        self.questions: List[Question] = []
        self.categories: Set[str] = set()
        self.subjects: Set[str] = set()  # 支持多科目
    
    def load_from_json(self, filepath: str) -> tuple:
        """从JSON文件加载题库"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.questions = []
            self.categories = set()
            self.subjects = set()
            
            for item in data:
                question = Question.from_dict(item)
                self.questions.append(question)
                if question.category:
                    self.categories.add(question.category)
                if question.subject:
                    self.subjects.add(question.subject)
            
            return True, f"成功加载 {len(self.questions)} 道题目"
        except Exception as e:
            return False, f"加载失败: {str(e)}"
    
    def get_statistics(self) -> Dict:
        """获取题库统计信息"""
        stats = {
            'total': len(self.questions),
            'single': len([q for q in self.questions if q.type == 'single']),
            'multiple': len([q for q in self.questions if q.type == 'multiple']),
            'judge': len([q for q in self.questions if q.type == 'judge']),
            'categories': list(self.categories),
            'subjects': list(self.subjects)
        }
        return stats
    
    def get_random_questions(self, counts: Dict[str, int], category: str = None, 
                            subject: str = None, exclude_ids: set = None) -> List[Question]:
        """随机获取指定数量的题目 - 支持科目筛选"""
        selected = []
        exclude_ids = exclude_ids or set()
        
        for q_type, count in counts.items():
            if count <= 0:
                continue
            
            # 筛选题目
            type_questions = [q for q in self.questions 
                            if q.type == q_type and q.id not in exclude_ids]
            
            # 按分类筛选
            if category and category != '全部':
                type_questions = [q for q in type_questions if q.category == category]
            
            # 按科目筛选（如果有）
            if subject and subject != '全部':
                type_questions = [q for q in type_questions if q.subject == subject]
            
            if type_questions:
                if len(type_questions) >= count:
                    selected.extend(random.sample(type_questions, count))
                else:
                    selected.extend(type_questions)
        
        return selected
    
    def filter_by_subject(self, subject: str) -> List[Question]:
        """按科目筛选题目"""
        if not subject or subject == '全部':
            return self.questions
        return [q for q in self.questions if q.subject == subject]