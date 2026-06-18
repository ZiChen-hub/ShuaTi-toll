# ui/stats_page.py
import customtkinter as ctk
from config import COLORS
from ui.components import SectionHeader


class StatsPage:
    """学习统计页面"""
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        SectionHeader(
            self.parent,
            "📊 学习统计",
            "你的学习进度"
        ).pack(fill="x", pady=(0, 20))
        
        # 统计卡片网格
        self._create_stats_cards()
        
        # 最近学习记录
        self._create_recent_records()
    
    def _create_stats_cards(self):
        """创建统计卡片"""
        exam_stats = self.app.exam_records.get_statistics()
        wrong_stats = self.app.wrong_bank.get_statistics()
        
        cards_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=20)
        cards_frame.grid_columnconfigure((0,1,2), weight=1)
        
        cards = [
            ("📝 总学习次数", str(exam_stats['total']), "次"),
            ("🎯 平均分", f"{exam_stats['avg_score']}", "分"),
            ("🏆 最高分", str(exam_stats['best_score']), "分"),
            ("⏱️ 总学习时间", f"{exam_stats['total_time']//60}", "分钟"),
            ("❌ 错题总数", str(wrong_stats['total']), "题"),
            ("📈 掌握率", f"{((self.app.question_bank.get_statistics()['total'] - wrong_stats['total'])/self.app.question_bank.get_statistics()['total']*100):.1f}" if self.app.question_bank.get_statistics()['total']>0 else "0", "%")
        ]
        
        for i, (title, value, unit) in enumerate(cards):
            card = ctk.CTkFrame(cards_frame, fg_color=COLORS["card_bg"], corner_radius=15)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 14),
                text_color=COLORS["text_secondary"]
            ).pack(anchor="w", padx=20, pady=(20,5))
            
            value_frame = ctk.CTkFrame(card, fg_color="transparent")
            value_frame.pack(anchor="w", padx=20, pady=(0,20))
            
            ctk.CTkLabel(
                value_frame,
                text=value,
                font=("Arial", 32, "bold"),
                text_color=COLORS["primary"]
            ).pack(side="left")
            
            ctk.CTkLabel(
                value_frame,
                text=unit,
                font=("Arial", 16),
                text_color=COLORS["text_secondary"]
            ).pack(side="left", padx=(5,0))
    
    def _create_recent_records(self):
        """创建最近学习记录"""
        records_frame = ctk.CTkFrame(self.parent, fg_color=COLORS["card_bg"], corner_radius=15)
        records_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(
            records_frame,
            text="📋 最近学习记录",
            font=("Arial", 20, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=20, pady=20)
        
        records = self.app.exam_records.get_records(10)
        if records:
            for record in records:
                self._create_record_card(records_frame, record)
        else:
            ctk.CTkLabel(
                records_frame,
                text="暂无学习记录",
                font=("Arial", 16),
                text_color=COLORS["text_secondary"]
            ).pack(pady=40)
    
    def _create_record_card(self, parent, record):
        """创建记录卡片"""
        record_card = ctk.CTkFrame(parent, fg_color=COLORS["dark"], corner_radius=10)
        record_card.pack(fill="x", padx=20, pady=5)
        
        date = record['date'][:10]
        score_color = COLORS["success"] if record['score'] >= 60 else COLORS["danger"]
        
        ctk.CTkLabel(
            record_card,
            text=date,
            font=("Arial", 13),
            text_color=COLORS["text_secondary"],
            width=100
        ).pack(side="left", padx=15, pady=12)
        
        ctk.CTkLabel(
            record_card,
            text=f"得分 {record['score']}",
            font=("Arial", 14, "bold"),
            text_color=score_color,
            width=100
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            record_card,
            text=f"{record['correct']}/{record['total']} 正确",
            font=("Arial", 13),
            text_color=COLORS["text"],
            width=100
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            record_card,
            text=f"⏱️ {record['time_spent']}秒",
            font=("Arial", 13),
            text_color=COLORS["text_secondary"]
        ).pack(side="right", padx=15)