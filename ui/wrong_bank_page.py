# ui/wrong_bank_page.py
import tkinter as tk
import customtkinter as ctk
from config import COLORS
from ui.components import GradientButton, SectionHeader


class WrongBankPage:
    """错题库页面"""
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        SectionHeader(
            self.parent,
            "❌ 错题本",
            "复习你的错题"
        ).pack(fill="x", pady=(0, 20))
        
        stats = self.app.wrong_bank.get_statistics()
        
        # 统计卡片
        stats_frame = ctk.CTkFrame(self.parent, fg_color=COLORS["card_bg"], corner_radius=15)
        stats_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"总错题: {stats['total']} 题",
            font=("Arial", 18, "bold"),
            text_color=COLORS["text"]
        ).pack(side="left", padx=30, pady=20)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"单选: {stats['by_type'].get('single', 0)} · 多选: {stats['by_type'].get('multiple', 0)} · 判断: {stats['by_type'].get('judge', 0)}",
            font=("Arial", 14),
            text_color=COLORS["text_secondary"]
        ).pack(side="left", padx=20)
        
        # 筛选器
        filter_frame = ctk.CTkFrame(self.parent, fg_color=COLORS["card_bg"], corner_radius=15)
        filter_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            filter_frame,
            text="🔍 筛选",
            font=("Arial", 16, "bold"),
            text_color=COLORS["text"]
        ).pack(side="left", padx=20)
        
        self.wrong_category_var = tk.StringVar(value="全部")
        category_combo = ctk.CTkComboBox(
            filter_frame,
            values=["全部"] + list(self.app.question_bank.categories),
            variable=self.wrong_category_var,
            width=200,
            height=35,
            font=("Arial", 12),
            command=lambda x: self._refresh_display()
        )
        category_combo.pack(side="left", padx=10)
        
        self.wrong_type_var = tk.StringVar(value="全部")
        type_combo = ctk.CTkComboBox(
            filter_frame,
            values=["全部", "single", "multiple", "judge"],
            variable=self.wrong_type_var,
            width=120,
            height=35,
            font=("Arial", 12),
            command=lambda x: self._refresh_display()
        )
        type_combo.pack(side="left", padx=10)
        
        GradientButton(
            filter_frame,
            text="练习筛选的错题",
            icon="▶",
            command=self._practice_filtered,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            width=180,
            height=35
        ).pack(side="right", padx=20)
        
        # 错题列表
        list_frame = ctk.CTkFrame(self.parent, fg_color=COLORS["card_bg"], corner_radius=15)
        list_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            list_frame,
            text="📋 错题列表",
            font=("Arial", 18, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=20, pady=20)
        
        self.wrong_scroll = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.wrong_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self._refresh_display()
    
    def _refresh_display(self):
        """刷新错题显示"""
        if not hasattr(self, 'wrong_scroll'):
            return
        
        for widget in self.wrong_scroll.winfo_children():
            widget.destroy()
        
        category = self.wrong_category_var.get()
        q_type = self.wrong_type_var.get()
        if q_type == "全部":
            q_type = None
        
        wrong_questions = self.app.wrong_bank.get_wrong_questions(category, q_type)
        
        if not wrong_questions:
            ctk.CTkLabel(
                self.wrong_scroll,
                text="✨ 暂无错题，继续加油！",
                font=("Arial", 18),
                text_color=COLORS["text_secondary"]
            ).pack(pady=50)
            return
        
        for i, q in enumerate(wrong_questions, 1):
            self._create_wrong_card(i, q)
    
    def _create_wrong_card(self, index, question):
        """创建错题卡片"""
        card = ctk.CTkFrame(self.wrong_scroll, fg_color=COLORS["dark"], corner_radius=10)
        card.pack(fill="x", pady=5)
        
        # 头部
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=10)
        
        type_names = {'single': '单选', 'multiple': '多选', 'judge': '判断'}
        type_text = type_names.get(question.type, question.type)
        
        ctk.CTkLabel(
            header,
            text=f"{index}. [{type_text}] {question.category}",
            font=("Arial", 14, "bold"),
            text_color=COLORS["text"]
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text=f"❌ {question.wrong_count}次",
            font=("Arial", 12),
            text_color=COLORS["danger"]
        ).pack(side="right")
        
        # 题目
        ctk.CTkLabel(
            card,
            text=question.content,
            font=("Arial", 13),
            text_color=COLORS["text"],
            wraplength=800,
            justify="left"
        ).pack(anchor="w", padx=15, pady=5)
        
        # 答案
        answer = question.answer
        if isinstance(answer, list):
            answer = ','.join(answer)
        
        ctk.CTkLabel(
            card,
            text=f"正确答案: {answer}",
            font=("Arial", 12),
            text_color=COLORS["success"]
        ).pack(anchor="w", padx=15, pady=2)
        
        # 解析
        if question.explanation:
            ctk.CTkLabel(
                card,
                text=f"解析: {question.explanation}",
                font=("Arial", 12),
                text_color=COLORS["text_secondary"],
                wraplength=780,
                justify="left"
            ).pack(anchor="w", padx=15, pady=5)
        
        # 操作按钮
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="练习此题",
            command=lambda q=question: self._practice_single(q),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            width=100,
            height=30
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="标记已掌握",
            command=lambda q=question: self._mark_mastered(q),
            fg_color=COLORS["success"],
            hover_color=COLORS["primary_dark"],
            width=100,
            height=30
        ).pack(side="left", padx=5)
    
    def _practice_filtered(self):
        """练习筛选后的错题"""
        category = self.wrong_category_var.get()
        q_type = self.wrong_type_var.get()
        if q_type == "全部":
            q_type = None
        
        wrong_questions = self.app.wrong_bank.get_wrong_questions(category, q_type)
        if not wrong_questions:
            from tkinter import messagebox
            messagebox.showinfo("提示", "没有符合条件的错题")
            return
        
        self.app.current_paper = self.app.ExamPaper(wrong_questions)
        self.app.exam_submitted = False
        self.app.exam_duration = 60 * 60
        self.app.main_window.show_exam()
    
    def _practice_single(self, question):
        """练习单道错题"""
        self.app.current_paper = self.app.ExamPaper([question])
        self.app.exam_submitted = False
        self.app.exam_duration = 60 * 60
        self.app.main_window.show_exam()
    
    def _mark_mastered(self, question):
        """标记错题为已掌握"""
        self.app.wrong_bank.remove_correct(question)
        self._refresh_display()
        from tkinter import messagebox
        messagebox.showinfo("成功", "已从错题库中移除")