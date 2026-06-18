# database/__init__.py
from database.question_bank import QuestionBank
from database.wrong_bank import WrongQuestionBank

__all__ = ['QuestionBank', 'WrongQuestionBank']