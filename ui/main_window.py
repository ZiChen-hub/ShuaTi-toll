# ui/main_window.py
import tkinter as tk
import customtkinter as ctk
from config import COLORS, APP_NAME, APP_VERSION
from ui.home_page import HomePage
from ui.exam_config_page import ExamConfigPage
from ui.wrong_bank_page import WrongBankPage
from ui.stats_page import StatsPage


class MainWindow:
    """主窗口"""
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.current_view = "home"
        self.show_requirements = False  # 格式要求显示状态
        
        self._create_widgets()
    
    def _create_widgets(self):
        """创建界面组件"""
        # 主容器
        self.main_container = ctk.CTkFrame(self.root, fg_color=COLORS["darker"])
        self.main_container.pack(fill="both", expand=True)
        
        # 侧边栏
        self._create_sidebar()
        
        # 内容区域
        self.content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=COLORS["darker"],
            corner_radius=0
        )
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # 初始显示首页
        self.show_home()
    
    def _create_sidebar(self):
        """创建侧边栏"""
        self.sidebar = ctk.CTkFrame(
            self.main_container,
            width=280,
            fg_color=COLORS["dark"],
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # 侧边栏头部
        sidebar_header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        sidebar_header.pack(fill="x", padx=20, pady=30)
        
        ctk.CTkLabel(
            sidebar_header,
            text=APP_NAME,
            font=("Arial", 24, "bold"),
            text_color=COLORS["primary"]
        ).pack()
        
        ctk.CTkLabel(
            sidebar_header,
            text="你的全能学习伴侣",
            font=("Arial", 16),
            text_color=COLORS["text_secondary"]
        ).pack()
        
        # 上传题库按钮
        upload_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        upload_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.upload_btn = ctk.CTkButton(
            upload_frame,
            text="📤 上传题库",
            command=self.app.upload_file,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            height=45,
            font=("Arial", 14, "bold")
        )
        self.upload_btn.pack(fill="x")
        
        # 题库格式要求提示（可折叠）
        self.requirements_btn = ctk.CTkButton(
            upload_frame,
            text="📋 格式要求 ▼",
            command=self._toggle_requirements,
            fg_color="transparent",
            text_color=COLORS["text_secondary"],
            hover_color=COLORS["card_bg"],
            height=30,
            font=("Arial", 11)
        )
        self.requirements_btn.pack(pady=(5, 0))
        
        # 格式要求详情框架（初始不显示）
        self.requirements_frame = ctk.CTkFrame(self.sidebar, fg_color=COLORS["card_bg"], corner_radius=8)
        
        # 用户信息卡片
        self.user_card = ctk.CTkFrame(
            self.sidebar,
            fg_color=COLORS["card_bg"],
            corner_radius=15
        )
        self.user_card.pack(fill="x", padx=20, pady=10)
        
        stats = self.app.question_bank.get_statistics()
        ctk.CTkLabel(
            self.user_card,
            text="📊 题库统计",
            font=("Arial", 14, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.stats_text = ctk.CTkLabel(
            self.user_card,
            text=f"总题数: {stats['total']}\n单选题: {stats['single']}\n多选题: {stats['multiple']}\n判断题: {stats['judge']}",
            font=("Arial", 12),
            text_color=COLORS["text_secondary"],
            justify="left"
        )
        self.stats_text.pack(anchor="w", padx=15, pady=(0, 15))
        
        # 导航菜单
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=15, pady=20)
        
        nav_items = [
            ("🏠 首页", self.show_home),
            ("📝 开始学习", self.show_exam_config),
            ("❌ 错题本", self.show_wrong_bank),
            ("📊 学习记录", self.show_stats),
            ("🤖 小辰助教", self.show_ai)
        ]
        
        for text, command in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=command,
                fg_color="transparent",
                text_color=COLORS["text"],
                hover_color=COLORS["card_bg"],
                anchor="w",
                height=45,
                corner_radius=10,
                font=("Arial", 14)
            )
            btn.pack(fill="x", pady=2)
        
        # 底部信息
        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            footer,
            text=f"{APP_NAME} v{APP_VERSION}",
            font=("Arial", 11),
            text_color=COLORS["text_secondary"]
        ).pack()
    
    def _toggle_requirements(self):
        """切换格式要求显示/隐藏"""
        self.show_requirements = not self.show_requirements
        
        if self.show_requirements:
            self.requirements_btn.configure(text="📋 格式要求 ▲")
            self._show_requirements()
        else:
            self.requirements_btn.configure(text="📋 格式要求 ▼")
            self.requirements_frame.pack_forget()
    
    def _show_requirements(self):
        """显示格式要求详情"""
        # 清空之前的内容
        for widget in self.requirements_frame.winfo_children():
            widget.destroy()
        
        # 创建滚动文本框显示要求
        textbox = ctk.CTkTextbox(
            self.requirements_frame,
            height=280,
            wrap="word",
            font=("Consolas", 11),
            fg_color=COLORS["dark"],
            text_color=COLORS["text"]
        )
        textbox.pack(fill="both", expand=True, padx=2, pady=2)
        
        requirements_text = """
📌 JSON 文件格式要求：

{
  "id": "唯一标识符",
  "content": "题目内容",
  "type": "题型",
  "options": ["A. 选项1", "B. 选项2", ...],
  "answer": "A" 或 ["A", "B"],
  "explanation": "解析（可选）",
  "category": "专题分类（可选）",
  "subject": "科目（可选）"
}

📌 题型说明：
• single   - 单选题
• multiple - 多选题
• judge    - 判断题

📌 单选题示例：
{
  "id": "q001",
  "content": "Python中哪个关键字用于定义函数？",
  "type": "single",
  "options": ["A. def", "B. func", "C. function", "D. define"],
  "answer": "A",
  "explanation": "def是Python中定义函数的关键字",
  "category": "Python基础"
}

📌 多选题示例：
{
  "id": "q002",
  "content": "以下哪些是Python的数据类型？",
  "type": "multiple",
  "options": ["A. int", "B. float", "C. string", "D. array"],
  "answer": ["A", "B", "C"],
  "explanation": "int、float、string都是Python的数据类型"
}

📌 判断题示例：
{
  "id": "q003",
  "content": "Python是解释型语言。",
  "type": "judge",
  "options": ["A. 正确", "B. 错误"],
  "answer": "A"
}

💡 注意事项：
• 文件必须是UTF-8编码的.json格式
• 选项建议使用"A. 内容"的格式
• 多选题答案可以是数组
• 所有字段都区分大小写
        """
        
        textbox.insert("1.0", requirements_text)
        textbox.configure(state="disabled")  # 设置为只读
        
        # 将格式要求框架插入到用户卡片之前
        # 先隐藏用户卡片
        self.user_card.pack_forget()
        
        # 重新打包格式要求和用户卡片
        self.requirements_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.user_card.pack(fill="x", padx=20, pady=10)
    
    def update_statistics(self):
        """更新统计信息"""
        try:
            stats = self.app.question_bank.get_statistics()
            self.stats_text.configure(
                text=f"总题数: {stats['total']}\n单选题: {stats['single']}\n多选题: {stats['multiple']}\n判断题: {stats['judge']}"
            )
        except:
            pass
    
    def notify_upload_complete(self):
        """通知上传完成"""
        # 更新侧边栏统计
        self.update_statistics()
        
        # 如果当前在考试配置页面，自动刷新
        if self.current_view == 'exam_config':
            self.show_exam_config()
        
        # 如果当前在AI页面，更新科目列表
        if self.current_view == 'ai' and hasattr(self, 'current_page'):
            if hasattr(self.current_page, 'refresh_status'):
                self.current_page.refresh_status()
    
    def clear_content(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """显示首页"""
        self.clear_content()
        self.current_view = "home"
        HomePage(self.content_frame, self.app)
    
    def show_exam_config(self):
        """显示学习配置页"""
        self.clear_content()
        self.current_view = "exam_config"
        ExamConfigPage(self.content_frame, self.app)
    
    def show_exam(self):
        """显示学习页"""
        self.clear_content()
        self.current_view = "exam"
        from ui.exam_page import ExamPage
        ExamPage(self.content_frame, self.app)
    
    def show_result(self):
        """显示结果页"""
        self.clear_content()
        self.current_view = "result"
        from ui.result_page import ResultPage
        ResultPage(self.content_frame, self.app)
    
    def show_wrong_bank(self):
        """显示错题本页"""
        self.clear_content()
        self.current_view = "wrong"
        WrongBankPage(self.content_frame, self.app)
    
    def show_stats(self):
        """显示学习记录页"""
        self.clear_content()
        self.current_view = "stats"
        StatsPage(self.content_frame, self.app)
    
    def show_ai(self):
        """显示小辰助教页"""
        self.clear_content()
        self.current_view = "ai"
        # 在这里导入 AIPage，避免循环导入
        from ui.ai_page import AIPage
        ai_page = AIPage(self.content_frame, self.app)
        self.current_page = ai_page