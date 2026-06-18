# ui/exam_config_page.py
import tkinter as tk
import customtkinter as ctk
from config import COLORS
from ui.components import GradientButton, SectionHeader


class ExamConfigPage:
    """学习配置页面"""
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        """创建界面"""
        if not self.app.question_bank.questions:
            self._show_empty_state()
            return
        
        self._show_config_form()
    
    def _show_empty_state(self):
        """显示空状态"""
        error_frame = ctk.CTkFrame(self.parent, fg_color=COLORS["card_bg"], corner_radius=15)
        error_frame.pack(pady=50, padx=50, fill="both", expand=True)
        
        ctk.CTkLabel(
            error_frame,
            text="⚠️ 暂无题库",
            font=("Arial", 32, "bold"),
            text_color=COLORS["danger"]
        ).pack(pady=50)
        
        ctk.CTkLabel(
            error_frame,
            text="请先上传题库文件",
            font=("Arial", 16),
            text_color=COLORS["text_secondary"]
        ).pack()
        
        GradientButton(
            error_frame,
            text="上传题库",
            icon="📁",
            command=self.app.upload_file,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            width=200,
            height=50
        ).pack(pady=30)

    
    def _show_config_form(self):
        """显示配置表单"""
        # 清空现有内容
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        SectionHeader(
            self.parent,
            "📝 学习配置",
            "自定义你的学习计划"
        ).pack(fill="x", pady=(0, 20))
        
        # 配置卡片
        config_card = ctk.CTkFrame(self.parent, fg_color=COLORS["card_bg"], corner_radius=15)
        config_card.pack(pady=20, padx=50, fill="both", expand=True)
        
        stats = self.app.question_bank.get_statistics()
        
        # 分类选择
        category_frame = ctk.CTkFrame(config_card, fg_color="transparent")
        category_frame.pack(fill="x", padx=40, pady=30)
        
        ctk.CTkLabel(
            category_frame,
            text="选择专题",
            font=("Arial", 16),
            text_color=COLORS["text"]
        ).pack(anchor="w")
        
        # 确保 exam_category_var 存在
        if not hasattr(self.app, 'exam_category_var'):
            self.app.exam_category_var = tk.StringVar(value="全部")
        else:
            self.app.exam_category_var.set("全部")
        
        categories = ["全部"] + stats['categories']
        category_combo = ctk.CTkComboBox(
            category_frame,
            values=categories,
            variable=self.app.exam_category_var,
            width=400,
            height=40,
            font=("Arial", 14),
            dropdown_font=("Arial", 14)
        )
        category_combo.pack(anchor="w", pady=10)
        
        # 题型数量配置
        counts_frame = ctk.CTkFrame(config_card, fg_color="transparent")
        counts_frame.pack(fill="x", padx=40, pady=20)
        counts_frame.grid_columnconfigure((0,1,2), weight=1)
        
        count_configs = [
            ("单选题", "single_count", "5", stats['single']),
            ("多选题", "multiple_count", "3", stats['multiple']),
            ("判断题", "judge_count", "2", stats['judge'])
        ]
        
        # 确保 exam_counts 存在
        if not hasattr(self.app, 'exam_counts'):
            self.app.exam_counts = {}
        
        for i, (label, key, default, max_val) in enumerate(count_configs):
            frame = ctk.CTkFrame(counts_frame, fg_color="transparent")
            frame.grid(row=0, column=i, padx=10, sticky="nsew")
            
            ctk.CTkLabel(
                frame,
                text=label,
                font=("Arial", 14),
                text_color=COLORS["text"]
            ).pack(anchor="w")
            
            # 使用现有变量或创建新变量
            if key not in self.app.exam_counts:
                self.app.exam_counts[key] = tk.StringVar(value=default)
            else:
                self.app.exam_counts[key].set(default)
            
            entry = ctk.CTkEntry(
                frame,
                textvariable=self.app.exam_counts[key],
                width=120,
                height=40,
                font=("Arial", 14),
                placeholder_text=f"最多{max_val}"
            )
            entry.pack(anchor="w", pady=5)
            
            ctk.CTkLabel(
                frame,
                text=f"最多 {max_val} 题",
                font=("Arial", 11),
                text_color=COLORS["text_secondary"]
            ).pack(anchor="w")
        
        # 学习时间
        time_frame = ctk.CTkFrame(config_card, fg_color="transparent")
        time_frame.pack(fill="x", padx=40, pady=30)
        
        ctk.CTkLabel(
            time_frame,
            text="学习时间",
            font=("Arial", 16),
            text_color=COLORS["text"]
        ).pack(anchor="w")
        
        time_input_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        time_input_frame.pack(anchor="w", pady=10)
        
        if not hasattr(self.app, 'exam_duration_var'):
            self.app.exam_duration_var = tk.StringVar(value="30")
        else:
            self.app.exam_duration_var.set("30")
        
        time_entry = ctk.CTkEntry(
            time_input_frame,
            textvariable=self.app.exam_duration_var,
            width=120,
            height=40,
            font=("Arial", 14)
        )
        time_entry.pack(side="left")
        
        ctk.CTkLabel(
            time_input_frame,
            text="分钟",
            font=("Arial", 14),
            text_color=COLORS["text_secondary"]
        ).pack(side="left", padx=10)
        
        # 开始学习按钮
        button_frame = ctk.CTkFrame(config_card, fg_color="transparent")
        button_frame.pack(pady=40)
        
        GradientButton(
            button_frame,
            text="开始学习",
            icon="🚀",
            command=self.app.start_exam,
            fg_color=COLORS["success"],
            hover_color=COLORS["primary_dark"],
            width=300,
            height=60,
            font=("Arial", 18, "bold")
        ).pack()
    
    def refresh(self):
        """手动刷新页面"""
        self._show_config_form()