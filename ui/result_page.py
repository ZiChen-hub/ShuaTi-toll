# ui/result_page.py
import customtkinter as ctk
from config import COLORS
from ui.components import GradientButton


class ResultPage:
    """学习结果页面"""
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        result = self.app.exam_result
        
        # 结果头部
        header = ctk.CTkFrame(self.parent, fg_color=COLORS["card_bg"], corner_radius=15, height=120)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        # 返回按钮
        back_btn = ctk.CTkButton(
            header,
            text="← 返回首页",
            command=self.app.main_window.show_home,
            fg_color="transparent",
            text_color=COLORS["text"],
            hover_color=COLORS["dark"],
            width=100,
            height=40,
            font=("Arial", 14)
        )
        back_btn.pack(side="left", padx=20)
        
        # 分数显示
        score_color = COLORS["success"] if result['score'] >= 60 else COLORS["danger"]
        
        score_frame = ctk.CTkFrame(header, fg_color="transparent")
        score_frame.pack(side="right", padx=30)
        
        ctk.CTkLabel(
            score_frame,
            text="最终得分",
            font=("Arial", 16),
            text_color=COLORS["text_secondary"]
        ).pack()
        
        ctk.CTkLabel(
            score_frame,
            text=f"{result['score']}",
            font=("Arial", 48, "bold"),
            text_color=score_color
        ).pack()
        
        # 结果内容
        content = ctk.CTkFrame(self.parent, fg_color="transparent")
        content.pack(fill="both", expand=True)
        
        # 左侧统计
        self._create_stats_panel(content, result)
        
        # 右侧错题详情
        self._create_wrong_panel(content, result)
    
    def _create_stats_panel(self, parent, result):
        """创建左侧统计面板"""
        left_panel = ctk.CTkFrame(parent, fg_color=COLORS["card_bg"], corner_radius=15, width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        left_panel.pack_propagate(False)
        
        ctk.CTkLabel(
            left_panel,
            text="📊 学习统计",
            font=("Arial", 20, "bold"),
            text_color=COLORS["text"]
        ).pack(pady=20)
        
        stats = [
            ("总题数", f"{result['total']} 题"),
            ("正确数", f"{result['correct']} 题"),
            ("错误数", f"{len(result['wrong_questions'])} 题"),
            ("正确率", f"{result['correct']/result['total']*100:.1f}%" if result['total']>0 else "0%"),
            ("用时", f"{result['time_spent']} 秒")
        ]
        
        for label, value in stats:
            stat_frame = ctk.CTkFrame(left_panel, fg_color=COLORS["dark"], corner_radius=10)
            stat_frame.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=("Arial", 13),
                text_color=COLORS["text_secondary"]
            ).pack(side="left", padx=15, pady=10)
            
            ctk.CTkLabel(
                stat_frame,
                text=value,
                font=("Arial", 15, "bold"),
                text_color=COLORS["text"]
            ).pack(side="right", padx=15, pady=10)
        
        # 操作按钮
        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        GradientButton(
            btn_frame,
            text="再次练习",
            icon="🔄",
            command=self.app.retry_exam,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            height=45,
            width=250
        ).pack(fill="x", pady=5)
        
        GradientButton(
            btn_frame,
            text="练习错题",
            icon="❌",
            command=self.app.practice_wrong,
            fg_color=COLORS["warning"],
            hover_color="#e67e22",
            height=45,
            width=250
        ).pack(fill="x", pady=5)
    
    def _create_wrong_panel(self, parent, result):
        """创建右侧错题面板"""
        right_panel = ctk.CTkFrame(parent, fg_color=COLORS["card_bg"], corner_radius=15)
        right_panel.pack(side="right", fill="both", expand=True)
        
        ctk.CTkLabel(
            right_panel,
            text="❌ 错题详情",
            font=("Arial", 20, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=20, pady=20)
        
        if result['wrong_questions']:
            scroll = ctk.CTkScrollableFrame(right_panel, fg_color="transparent")
            scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            for i, q in enumerate(result['wrong_questions'], 1):
                self._create_wrong_card(scroll, i, q, result)
        else:
            ctk.CTkLabel(
                right_panel,
                text="🎉 恭喜！全部正确！",
                font=("Arial", 24, "bold"),
                text_color=COLORS["success"]
            ).pack(expand=True)
    
    def _create_wrong_card(self, parent, index, question, result):
        """创建错题卡片"""
        card = ctk.CTkFrame(parent, fg_color=COLORS["dark"], corner_radius=10)
        card.pack(fill="x", pady=5)
        
        # 题目
        ctk.CTkLabel(
            card,
            text=f"{index}. {question.content}",
            font=("Arial", 13, "bold"),
            text_color=COLORS["text"],
            wraplength=600,
            justify="left"
        ).pack(anchor="w", padx=15, pady=10)
        
        # 答案对比
        answer_frame = ctk.CTkFrame(card, fg_color="transparent")
        answer_frame.pack(fill="x", padx=15, pady=5)
        
        user_answer = result['user_answers'].get(question.id, "")
        if isinstance(user_answer, list):
            user_answer = ','.join(user_answer)
        
        correct_answer = question.answer
        if isinstance(correct_answer, list):
            correct_answer = ','.join(correct_answer)
        
        ctk.CTkLabel(
            answer_frame,
            text=f"您的答案: {user_answer}",
            font=("Arial", 12),
            text_color=COLORS["danger"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            answer_frame,
            text=f"正确答案: {correct_answer}",
            font=("Arial", 12),
            text_color=COLORS["success"]
        ).pack(anchor="w", pady=(2, 5))
        
        # 解析
        if question.explanation:
            ctk.CTkLabel(
                card,
                text=f"📖 解析: {question.explanation}",
                font=("Arial", 12),
                text_color=COLORS["text_secondary"],
                wraplength=580,
                justify="left"
            ).pack(anchor="w", padx=15, pady=(0, 10))