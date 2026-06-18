# ui/home_page.py
import customtkinter as ctk
from config import COLORS, APP_NAME, AI_ASSISTANT_NAME
from ui.components import GradientButton, StatCard


class HomePage:
    """通用首页"""
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        # 欢迎区域
        welcome_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        welcome_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            welcome_frame,
            text=f"欢迎使用 {APP_NAME}",
            font=("Arial", 32, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            welcome_frame,
            text="你的全能学习助手，支持多科目学习",
            font=("Arial", 16),
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w")
        
        # 统计卡片网格
        stats = self.app.question_bank.get_statistics()
        wrong_stats = self.app.wrong_bank.get_statistics()
        exam_stats = self.app.exam_records.get_statistics()
        
        cards_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=20)
        cards_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        cards = [
            ("📚 题库总览", f"{stats['total']} 题", 
             f"{stats['single']}单选 · {stats['multiple']}多选 · {stats['judge']}判断"),
            ("❌ 错题本", f"{wrong_stats['total']} 道错题", "需要重点复习"),
            ("📊 学习统计", f"{exam_stats['total']} 次学习", f"平均分 {exam_stats['avg_score']}"),
            ("🤖 小辰助教", "全能AI助教", "随时提问解答")
        ]
        
        for i, (title, main_stat, sub_stat) in enumerate(cards):
            card = StatCard(cards_frame, title, main_stat, sub_stat)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
        
        # 快速行动区域
        quick_frame = ctk.CTkFrame(self.parent, fg_color=COLORS["card_bg"], corner_radius=15)
        quick_frame.pack(fill="x", pady=30)
        
        ctk.CTkLabel(
            quick_frame,
            text="⚡ 快速开始",
            font=("Arial", 20, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=30, pady=(30, 20))
        
        button_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(0, 30))
        button_frame.grid_columnconfigure((0,1,2), weight=1)
        
        GradientButton(
            button_frame,
            text="随机10题",
            icon="📝",
            command=lambda: self.app.quick_exam(10),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            width=200,
            height=45
        ).grid(row=0, column=0, padx=10, sticky="ew")
        
        GradientButton(
            button_frame,
            text="练习错题",
            icon="❌",
            command=self.app.practice_wrong,
            fg_color=COLORS["warning"],
            hover_color="#e67e22",
            width=200,
            height=45
        ).grid(row=0, column=1, padx=10, sticky="ew")
        
        GradientButton(
            button_frame,
            text="问小辰",
            icon="🤖",
            command=self.app.show_ai_assistant,  # 这里调用了 show_ai_assistant 方法
            fg_color=COLORS["info"],
            hover_color="#2980b9",
            width=200,
            height=45
        ).grid(row=0, column=2, padx=10, sticky="ew")
        
        # 最近活动
        if self.app.exam_records.records:
            activity_frame = ctk.CTkFrame(self.parent, fg_color=COLORS["card_bg"], corner_radius=15)
            activity_frame.pack(fill="x", pady=20)
            
            ctk.CTkLabel(
                activity_frame,
                text="📋 最近活动",
                font=("Arial", 20, "bold"),
                text_color=COLORS["text"]
            ).pack(anchor="w", padx=30, pady=(30, 20))
            
            for record in self.app.exam_records.get_records(3):
                record_card = ctk.CTkFrame(activity_frame, fg_color=COLORS["dark"], corner_radius=10)
                record_card.pack(fill="x", padx=30, pady=5)
                
                date = record['date'][:10]
                score_color = COLORS["success"] if record['score'] >= 60 else COLORS["danger"]
                
                ctk.CTkLabel(
                    record_card,
                    text=f"{date} · 得分 {record['score']} · {record['correct']}/{record['total']} 正确",
                    font=("Arial", 13),
                    text_color=COLORS["text"]
                ).pack(side="left", padx=20, pady=15)