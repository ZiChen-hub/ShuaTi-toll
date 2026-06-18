# models/exam_paper.py
from datetime import datetime
from typing import List, Dict, Any, Optional
from models.question import Question


class ExamPaper:
    """试卷类"""
    def __init__(self, questions: List[Question]):
        self.questions = questions
        self.user_answers = {}
        self.start_time = datetime.now()
        self.end_time = None
        self.wrong_questions = []
    
    def submit_answer(self, qid: str, answer: Any):
        """提交答案"""
        self.user_answers[qid] = answer
    
    def grade(self) -> Dict[str, Any]:
        """批改试卷"""
        self.end_time = datetime.now()
        total = len(self.questions)
        correct = 0
        self.wrong_questions = []
        
        for q in self.questions:
            user_answer = self.user_answers.get(q.id, "")
            if self._check_answer(q, user_answer):
                correct += 1
            else:
                self.wrong_questions.append(q)
                self.user_answers[q.id] = user_answer
        
        score = (correct / total) * 100 if total > 0 else 0
        
        return {
            'total': total,
            'correct': correct,
            'score': round(score, 2),
            'wrong_questions': self.wrong_questions,
            'user_answers': self.user_answers,
            'time_spent': (self.end_time - self.start_time).seconds
        }
    
    def _check_answer(self, question: Question, user_answer: Any) -> bool:
        """检查单个答案是否正确"""
        if question.type == 'single':
            return str(user_answer).strip().upper() == str(question.answer).strip().upper()
        elif question.type == 'multiple':
            if isinstance(user_answer, list):
                user_set = set(str(a).strip().upper() for a in user_answer if a)
            else:
                user_set = set()
            correct_set = set(str(a).strip().upper() for a in question.answer)
            return user_set == correct_set
        elif question.type == 'judge':
            return str(user_answer).strip().upper() == str(question.answer).strip().upper()
        return False