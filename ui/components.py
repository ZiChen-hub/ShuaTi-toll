# ui/components.py
import customtkinter as ctk
from config import COLORS


class GradientButton(ctk.CTkButton):
    """渐变按钮"""
    def __init__(self, master, text="", command=None, icon="", **kwargs):
        # 提取可能冲突的参数
        button_kwargs = {}
        
        # 处理字体
        if 'font' in kwargs:
            button_kwargs['font'] = kwargs.pop('font')
        else:
            button_kwargs['font'] = ("Arial", 13, "bold")
        
        # 处理高度
        if 'height' in kwargs:
            button_kwargs['height'] = kwargs.pop('height')
        else:
            button_kwargs['height'] = 40
        
        # 处理宽度
        if 'width' in kwargs:
            button_kwargs['width'] = kwargs.pop('width')
        else:
            button_kwargs['width'] = 140
        
        # 添加图标到文本
        display_text = f"{icon} {text}" if icon else text
        
        # 调用父类初始化
        super().__init__(
            master,
            text=display_text,
            command=command,
            corner_radius=10,
            **button_kwargs,
            **kwargs
        )


class StatCard(ctk.CTkFrame):
    """统计卡片"""
    def __init__(self, master, title="", main_value="", sub_text="", **kwargs):
        super().__init__(master, fg_color=COLORS["card_bg"], corner_radius=15, **kwargs)
        
        ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 14),
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(
            self,
            text=main_value,
            font=("Arial", 28, "bold"),
            text_color=COLORS["primary"]
        ).pack(anchor="w", padx=15)
        
        ctk.CTkLabel(
            self,
            text=sub_text,
            font=("Arial", 11),
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", padx=15, pady=(5, 15))


class SectionHeader(ctk.CTkFrame):
    """章节标题"""
    def __init__(self, master, title="", subtitle=""):
        super().__init__(master, fg_color="transparent")
        
        ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 28, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w")
        
        if subtitle:
            ctk.CTkLabel(
                self,
                text=subtitle,
                font=("Arial", 14),
                text_color=COLORS["text_secondary"]
            ).pack(anchor="w")