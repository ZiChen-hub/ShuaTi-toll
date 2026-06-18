# ui/exam_page.py
import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from config import COLORS


class ExamPage:
    """学习页面"""
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.question_frames = []
        self.question_buttons = []
        self._create_widgets()
    
    def _create_widgets(self):
        # 学习头部
        header = ctk.CTkFrame(self.parent, fg_color=COLORS["card_bg"], corner_radius=15, height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        # 返回按钮
        back_btn = ctk.CTkButton(
            header,
            text="← 返回",
            command=self._confirm_back,
            fg_color="transparent",
            text_color=COLORS["text"],
            hover_color=COLORS["dark"],
            width=80,
            height=40,
            font=("Arial", 14)
        )
        back_btn.pack(side="left", padx=20)
        
        # 学习信息
        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.pack(side="left", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=f"📝 共 {len(self.app.current_paper.questions)} 题",
            font=("Arial", 18, "bold"),
            text_color=COLORS["text"]
        ).pack(side="left", padx=20)
        
        # 计时器
        self.app.timer_label = ctk.CTkLabel(
            info_frame,
            text="⏱️ 00:00",
            font=("Arial", 24, "bold"),
            text_color=COLORS["warning"]
        )
        self.app.timer_label.pack(side="left", padx=20)
        
        # 提交按钮
        self.app.submit_btn = ctk.CTkButton(
            header,
            text="提交结果",
            command=self._confirm_submit,
            fg_color=COLORS["danger"],
            hover_color="#c0392b",
            width=120,
            height=45,
            font=("Arial", 14, "bold")
        )
        self.app.submit_btn.pack(side="right", padx=20)
        
        # 创建左右分栏
        paned = ctk.CTkFrame(self.parent, fg_color="transparent")
        paned.pack(fill="both", expand=True)
        
        # 左侧题目导航
        self._create_navigation(paned)
        
        # 右侧题目区域
        self._create_question_area(paned)
        
        # 显示题目
        self._display_paper()
        
        # 开始计时
        self.app.start_timer()
    
    def _create_navigation(self, parent):
        """创建左侧导航"""
        left_panel = ctk.CTkFrame(parent, fg_color=COLORS["card_bg"], corner_radius=15, width=250)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        left_panel.pack_propagate(False)
        
        ctk.CTkLabel(
            left_panel,
            text="📋 题目导航",
            font=("Arial", 18, "bold"),
            text_color=COLORS["text"]
        ).pack(pady=20)
        
        nav_frame = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, padx=10)
        
        for i in range(len(self.app.current_paper.questions)):
            btn_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
            btn_frame.pack(fill="x", pady=2)
            
            btn = ctk.CTkButton(
                btn_frame,
                text=f"第 {i+1} 题",
                command=lambda idx=i: self._scroll_to_question(idx),
                fg_color=COLORS["dark"],
                hover_color=COLORS["primary"],
                height=35,
                font=("Arial", 13)
            )
            btn.pack(side="left", fill="x", expand=True)
            
            status = ctk.CTkLabel(
                btn_frame,
                text="○",
                font=("Arial", 16),
                text_color=COLORS["text_secondary"],
                width=30
            )
            status.pack(side="right")
            
            self.question_buttons.append({'button': btn, 'status': status, 'answered': False})
    
    def _create_question_area(self, parent):
        """创建右侧题目区域"""
        right_panel = ctk.CTkFrame(parent, fg_color=COLORS["card_bg"], corner_radius=15)
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.app.exam_canvas = ctk.CTkScrollableFrame(right_panel, fg_color="transparent")
        self.app.exam_canvas.pack(fill="both", expand=True, padx=20, pady=20)
    
    def _display_paper(self):
        """显示所有题目"""
        for i, q in enumerate(self.app.current_paper.questions):
            frame = self._create_question_frame(self.app.exam_canvas, i, q)
            frame.pack(fill="x", padx=10, pady=5)
            self.question_frames.append(frame)
    
    def _create_question_frame(self, parent, index, question):
        """创建单个题目框架"""
        frame = ctk.CTkFrame(parent, fg_color=COLORS["dark"], corner_radius=10)
        
        # 头部
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=10)
        
        type_names = {'single': '单选题', 'multiple': '多选题', 'judge': '判断题'}
        type_text = type_names.get(question.type, question.type)
        
        ctk.CTkLabel(
            header,
            text=f"{index+1}. {type_text}",
            font=("Arial", 14, "bold"),
            text_color=COLORS["primary"]
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text=question.category,
            font=("Arial", 12),
            text_color=COLORS["text_secondary"]
        ).pack(side="right")
        
        # 题目内容
        ctk.CTkLabel(
            frame,
            text=question.content,
            font=("Arial", 13),
            text_color=COLORS["text"],
            wraplength=700,
            justify="left"
        ).pack(anchor="w", padx=15, pady=5)
        
        # 选项
        if question.type == 'single':
            self._create_single_choice(frame, question)
        elif question.type == 'multiple':
            self._create_multiple_choice(frame, question)
        elif question.type == 'judge':
            self._create_judge_question(frame, question)
        
        return frame
    
    def _create_single_choice(self, parent, question):
        """创建单选题"""
        var = tk.StringVar(value="")
        question.answer_var = var
        
        for opt in question.options:
            opt_letter = opt[0].lower() if opt else ''
            rb = ctk.CTkRadioButton(
                parent,
                text=opt,
                variable=var,
                value=opt_letter,
                font=("Arial", 12),
                text_color=COLORS["text"],
                fg_color=COLORS["primary"],
                command=lambda q=question, v=var: self._on_answer_selected(q, v.get())
            )
            rb.pack(anchor="w", padx=35, pady=2)
    
    def _create_multiple_choice(self, parent, question):
        """创建多选题"""
        vars = []
        for opt in question.options:
            var = tk.BooleanVar(value=False)
            opt_letter = opt[0].lower() if opt else ''
            vars.append((opt_letter, var))
            cb = ctk.CTkCheckBox(
                parent,
                text=opt,
                variable=var,
                font=("Arial", 12),
                text_color=COLORS["text"],
                fg_color=COLORS["primary"],
                command=lambda q=question, v=vars: self._on_multiple_selected(q, v)
            )
            cb.pack(anchor="w", padx=35, pady=2)
        question.answer_vars = vars
    
    def _create_judge_question(self, parent, question):
        """创建判断题"""
        var = tk.StringVar(value="")
        question.answer_var = var
        
        rb_true = ctk.CTkRadioButton(
            parent,
            text="A. 正确",
            variable=var,
            value="A",
            font=("Arial", 12),
            text_color=COLORS["text"],
            fg_color=COLORS["primary"],
            command=lambda q=question, v=var: self._on_answer_selected(q, v.get())
        )
        rb_true.pack(anchor="w", padx=35, pady=2)
        
        rb_false = ctk.CTkRadioButton(
            parent,
            text="B. 错误",
            variable=var,
            value="B",
            font=("Arial", 12),
            text_color=COLORS["text"],
            fg_color=COLORS["primary"],
            command=lambda q=question, v=var: self._on_answer_selected(q, v.get())
        )
        rb_false.pack(anchor="w", padx=35, pady=2)
    
    def _on_answer_selected(self, question, answer):
        """单选题答案选择回调"""
        if self.app.current_paper:
            self.app.current_paper.submit_answer(question.id, answer)
            self._update_question_status(question.id, True)
    
    def _on_multiple_selected(self, question, vars):
        """多选题答案选择回调"""
        if self.app.current_paper:
            selected = [letter for letter, var in vars if var.get()]
            self.app.current_paper.submit_answer(question.id, selected)
            self._update_question_status(question.id, bool(selected))
    
    def _update_question_status(self, qid, answered):
        """更新题目状态"""
        for i, q in enumerate(self.app.current_paper.questions):
            if q.id == qid and i < len(self.question_buttons):
                self.question_buttons[i]['answered'] = answered
                self.question_buttons[i]['status'].configure(
                    text="●" if answered else "○",
                    text_color=COLORS["success"] if answered else COLORS["text_secondary"]
                )
    
    def _scroll_to_question(self, index):
        """滚动到指定题目"""
        if index < len(self.question_frames):
            frame = self.question_frames[index]
            y_position = frame.winfo_y()
            self.app.exam_canvas._parent_canvas.yview_moveto(y_position / self.app.exam_canvas.winfo_height())
    
    def _confirm_back(self):
        """确认返回"""
        from tkinter import messagebox
        result = messagebox.askyesno("确认", "学习正在进行，确定要返回首页吗？")
        if result:
            self.app.stop_timer()
            self.app.main_window.show_home()
    
    def _confirm_submit(self):
        """确认提交"""
        from tkinter import messagebox
        result = messagebox.askyesno("确认", "确定要提交学习结果吗？")
        if result:
            self.app.submit_exam()