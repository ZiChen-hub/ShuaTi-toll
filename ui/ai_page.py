# ui/ai_page.py
import tkinter as tk
import customtkinter as ctk
import threading
from tkinter import messagebox
from config import COLORS, AI_ASSISTANT_NAME, APP_NAME
from ui.components import GradientButton, SectionHeader


class AIPage:
    """AI助手页面 - 小辰助教（带记忆功能）"""
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        SectionHeader(
            self.parent,
            f"🤖 {AI_ASSISTANT_NAME}",
            f"{APP_NAME}的全能AI助教"
        ).pack(fill="x", pady=(0, 20))
        
        # 主容器
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # 左侧对话区域
        chat_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["card_bg"], corner_radius=15)
        chat_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # 对话历史
        self.ai_history = ctk.CTkTextbox(
            chat_frame,
            wrap="word",
            font=("Arial", 14),
            fg_color=COLORS["dark"],
            text_color=COLORS["text"]
        )
        self.ai_history.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 输入区域
        input_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.ai_input = ctk.CTkEntry(
            input_frame,
            placeholder_text=f"向{AI_ASSISTANT_NAME}提问...",
            height=50,
            font=("Arial", 14),
            fg_color=COLORS["dark"],
            border_color=COLORS["primary"]
        )
        self.ai_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.ai_send_btn = ctk.CTkButton(
            input_frame,
            text="发送",
            command=self.send_to_ai,
            width=100,
            height=50,
            font=("Arial", 14, "bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"]
        )
        self.ai_send_btn.pack(side="right")
        
        # 右侧配置面板 - 使用可滚动框架
        self._create_scrollable_config_panel(main_frame)
        
        # 显示欢迎信息
        self._show_welcome_message()
        
        # 绑定回车键
        self.ai_input.bind("<Return>", lambda e: self.send_to_ai())
    
    def _create_scrollable_config_panel(self, parent):
        """创建可滚动的配置面板"""
        # 创建一个容器框架来容纳滚动条和内容
        config_container = ctk.CTkFrame(parent, fg_color="transparent", width=320)
        config_container.pack(side="right", fill="y")
        config_container.pack_propagate(False)
        
        # 创建可滚动的配置面板
        self.config_scroll = ctk.CTkScrollableFrame(
            config_container,
            fg_color=COLORS["card_bg"],
            corner_radius=15,
            width=300
        )
        self.config_scroll.pack(fill="both", expand=True)
        
        # 标题
        ctk.CTkLabel(
            self.config_scroll,
            text=f"🤖 {AI_ASSISTANT_NAME}",
            font=("Arial", 20, "bold"),
            text_color=COLORS["text"]
        ).pack(pady=(20, 10))
        
        # 新建对话按钮
        new_chat_btn = ctk.CTkButton(
            self.config_scroll,
            text="➕ 新建对话",
            command=self._new_conversation,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            height=35,
            font=("Arial", 13)
        )
        new_chat_btn.pack(fill="x", padx=20, pady=5)
        
        # 对话历史列表
        history_label = ctk.CTkLabel(
            self.config_scroll,
            text="📋 对话历史",
            font=("Arial", 14, "bold"),
            text_color=COLORS["text"]
        )
        history_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.history_frame = ctk.CTkFrame(
            self.config_scroll,
            fg_color=COLORS["dark"],
            corner_radius=8
        )
        self.history_frame.pack(fill="x", padx=20, pady=5)
        
        self._refresh_history_list()
        
        # 状态卡片
        status_card = ctk.CTkFrame(self.config_scroll, fg_color=COLORS["dark"], corner_radius=10)
        status_card.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            status_card,
            text="当前状态",
            font=("Arial", 12),
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", padx=15, pady=(15,5))
        
        self.ai_status_label = ctk.CTkLabel(
            status_card,
            text=self._get_status_text(),
            font=("Arial", 16, "bold"),
            text_color=self._get_status_color()
        )
        self.ai_status_label.pack(anchor="w", padx=15, pady=(0,15))
        
        # 模型信息
        model_card = ctk.CTkFrame(self.config_scroll, fg_color=COLORS["dark"], corner_radius=10)
        model_card.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            model_card,
            text="当前模型",
            font=("Arial", 12),
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", padx=15, pady=(15,5))
        
        self.provider_label = ctk.CTkLabel(
            model_card,
            text=f"{self.app.ai_config.provider}",
            font=("Arial", 14, "bold"),
            text_color=COLORS["text"]
        )
        self.provider_label.pack(anchor="w", padx=15)
        
        self.model_label = ctk.CTkLabel(
            model_card,
            text=f"{self.app.ai_config.model or '未配置'}",
            font=("Arial", 12),
            text_color=COLORS["text_secondary"]
        )
        self.model_label.pack(anchor="w", padx=15, pady=(0,15))
        
        # 简洁模式开关
        concise_card = ctk.CTkFrame(self.config_scroll, fg_color=COLORS["dark"], corner_radius=10)
        concise_card.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            concise_card,
            text="回答风格",
            font=("Arial", 12),
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", padx=15, pady=(15,5))
        
        self.concise_var = tk.BooleanVar(value=True)
        concise_switch = ctk.CTkSwitch(
            concise_card,
            text="简洁模式（推荐）",
            variable=self.concise_var,
            onvalue=True,
            offvalue=False,
            font=("Arial", 12),
            progress_color=COLORS["primary"]
        )
        concise_switch.pack(anchor="w", padx=15, pady=(0,15))
        
        # 科目选择
        subject_card = ctk.CTkFrame(self.config_scroll, fg_color=COLORS["dark"], corner_radius=10)
        subject_card.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            subject_card,
            text="当前科目",
            font=("Arial", 12),
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", padx=15, pady=(15,5))
        
        self.subject_var = tk.StringVar(value="通用")
        subjects = ["通用"] + self.app.question_bank.get_statistics().get('subjects', [])
        subject_combo = ctk.CTkComboBox(
            subject_card,
            values=subjects,
            variable=self.subject_var,
            width=250,
            height=35,
            font=("Arial", 12)
        )
        subject_combo.pack(anchor="w", padx=15, pady=(0,15))
        
        # 配置按钮
        GradientButton(
            self.config_scroll,
            text=f"⚙️ 配置{AI_ASSISTANT_NAME}",
            command=self.app.configure_ai,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            height=40,
            width=250
        ).pack(fill="x", padx=20, pady=10)
        
        # 清空历史按钮
        ctk.CTkButton(
            self.config_scroll,
            text="🗑️ 清空所有对话",
            command=self._clear_all_conversations,
            fg_color="transparent",
            text_color=COLORS["danger"],
            hover_color=COLORS["dark"],
            height=30,
            font=("Arial", 11)
        ).pack(pady=5)
        
        # 底部留一些空白空间
        ctk.CTkLabel(self.config_scroll, text="").pack(pady=10)
    
    def _refresh_history_list(self):
        """刷新对话历史列表"""
        # 清空现有列表
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # 获取所有对话
        conversations = self.app.ai_assistant.get_conversations()
        
        if not conversations:
            ctk.CTkLabel(
                self.history_frame,
                text="暂无历史对话",
                font=("Arial", 11),
                text_color=COLORS["text_secondary"]
            ).pack(pady=10)
            return
        
        # 显示每个对话
        for conv in conversations[:10]:  # 只显示最近10个
            conv_frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
            conv_frame.pack(fill="x", pady=2)
            
            # 对话标题和切换按钮
            btn = ctk.CTkButton(
                conv_frame,
                text=f"{conv['title']}",
                command=lambda sid=conv['id']: self._switch_conversation(sid),
                fg_color=COLORS["darker"] if conv['id'] == self.app.ai_assistant.memory.current_session_id else "transparent",
                text_color=COLORS["text"],
                hover_color=COLORS["card_bg"],
                anchor="w",
                height=30,
                font=("Arial", 11)
            )
            btn.pack(side="left", fill="x", expand=True)
            
            # 删除按钮
            del_btn = ctk.CTkButton(
                conv_frame,
                text="✕",
                width=25,
                height=25,
                command=lambda sid=conv['id']: self._delete_conversation(sid),
                fg_color="transparent",
                text_color=COLORS["danger"],
                hover_color=COLORS["dark"]
            )
            del_btn.pack(side="right")
    
    def _new_conversation(self):
        """新建对话"""
        welcome = self.app.ai_assistant.new_conversation()
        self.ai_history.insert("end", f"\n\n系统: {welcome}\n")
        self._refresh_history_list()
    
    def _switch_conversation(self, session_id: str):
        """切换对话"""
        if self.app.ai_assistant.switch_conversation(session_id):
            # 清空并重新加载历史
            self.ai_history.delete("1.0", "end")
            
            # 加载该对话的历史消息
            session = self.app.ai_assistant.memory.get_current_session()
            for msg in session.messages:
                role_display = "您" if msg.role == 'user' else AI_ASSISTANT_NAME
                self.ai_history.insert("end", f"\n{role_display}: {msg.content}\n")
            
            self._refresh_history_list()
    
    def _delete_conversation(self, session_id: str):
        """删除对话"""
        if messagebox.askyesno("确认", "确定要删除这个对话吗？"):
            self.app.ai_assistant.delete_conversation(session_id)
            self._refresh_history_list()
            
            # 如果删除的是当前对话，清空显示
            if session_id == self.app.ai_assistant.memory.current_session_id:
                self.ai_history.delete("1.0", "end")
                self._show_welcome_message()
    
    def _clear_all_conversations(self):
        """清空所有对话"""
        if messagebox.askyesno("确认", "确定要清空所有对话历史吗？"):
            self.app.ai_assistant.memory.clear_all_sessions()
            self.app.ai_assistant.new_conversation()
            self.ai_history.delete("1.0", "end")
            self._show_welcome_message()
            self._refresh_history_list()
    
    def _get_status_text(self):
        """获取状态文本"""
        if not self.app.ai_config.enabled:
            return "未启用"
        if self.app.ai_config.api_key:
            return "已启用 ✓"
        return "配置不完整"
    
    def _get_status_color(self):
        """获取状态颜色"""
        if not self.app.ai_config.enabled:
            return COLORS["text_secondary"]
        if self.app.ai_config.api_key:
            return COLORS["success"]
        return COLORS["warning"]
    
    def _show_welcome_message(self):
        """显示欢迎信息"""
        welcome_msg = f"👋 你好！我是{AI_ASSISTANT_NAME}，你的全能学习助教\n\n"
        welcome_msg += "💡 我可以帮你解答任何学科的问题：\n"
        welcome_msg += "• 📐 数学、物理、化学\n"
        welcome_msg += "• 📖 语文、历史、哲学\n"
        welcome_msg += "• 💻 编程、计算机科学\n"
        welcome_msg += "• 🌍 地理、生物、医学\n"
        welcome_msg += "• 🎨 艺术、音乐、设计\n\n"
        
        if self.app.ai_config.enabled and self.app.ai_config.api_key:
            welcome_msg += f"✅ {AI_ASSISTANT_NAME}已启用，可以开始提问！"
        else:
            welcome_msg += f"⚙️ 请点击右侧配置按钮启用{AI_ASSISTANT_NAME}"
        
        self.ai_history.insert("end", welcome_msg)
    
    def refresh_status(self):
        """刷新状态显示"""
        self.ai_status_label.configure(
            text=self._get_status_text(),
            text_color=self._get_status_color()
        )
        self.provider_label.configure(text=self.app.ai_config.provider)
        self.model_label.configure(text=self.app.ai_config.model or '未配置')
        self._refresh_history_list()
    
    def send_to_ai(self):
        """发送消息到AI"""
        question = self.ai_input.get().strip()
        if not question:
            return
        
        # 显示用户消息
        self.ai_history.insert("end", f"\n\n您: {question}\n")
        self.ai_history.see("end")
        self.ai_input.delete(0, "end")
        
        # 禁用发送按钮
        self.ai_send_btn.configure(state="disabled", text="小辰思考中...")
        
        # 获取当前设置
        subject = self.subject_var.get() if self.subject_var.get() != "通用" else ""
        concise = self.concise_var.get()
        
        # 在新线程中请求AI
        thread = threading.Thread(
            target=self._ai_request_thread,
            args=(question, subject, concise)
        )
        thread.daemon = True
        thread.start()
    
    def _ai_request_thread(self, question: str, subject: str, concise: bool):
        """在线程中请求AI"""
        context = ""
        response = self.app.ai_assistant.ask(question, context, subject, concise)
        self.app.root.after(0, lambda: self._update_ai_response(response))
    
    def _update_ai_response(self, response: str):
        """更新AI响应"""
        self.ai_history.insert("end", f"\n{AI_ASSISTANT_NAME}: {response}\n")
        self.ai_history.see("end")
        self.ai_send_btn.configure(state="normal", text="发送")