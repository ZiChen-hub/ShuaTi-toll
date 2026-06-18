# main.py
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import threading
from datetime import datetime

from config import COLORS, DEFAULT_QUESTION_FILE, APP_NAME, AI_ASSISTANT_NAME
from models.question import Question
from models.exam_paper import ExamPaper
from models.exam_record import ExamRecord
from database.question_bank import QuestionBank
from database.wrong_bank import WrongQuestionBank
from ai.ai_config import AIConfig
from ai.ai_assistant import AIAssistant
from ui.main_window import MainWindow
from config import MODEL_CONFIGS


class ExamApp:
    """主应用程序 - 小辰伴学"""
    def __init__(self):
        # 设置主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        self.root = ctk.CTk()
        self.root.title(f"{APP_NAME} - 你的全能学习伴侣")
        self.root.geometry("1400x800")
        
        # 初始化组件
        self.question_bank = QuestionBank()
        self.exam_records = ExamRecord()
        self.wrong_bank = WrongQuestionBank()
        self.ai_config = AIConfig()
        self.ai_assistant = AIAssistant(self.ai_config)
        self.ExamPaper = ExamPaper  # 添加类引用
        
        self.current_paper = None
        self.exam_submitted = False
        self.timer_id = None
        self.exam_duration = 0
        self.exam_start_time = None
        self.exam_result = None
        self.timer_label = None  # 添加计时器标签引用
        self.submit_btn = None   # 添加提交按钮引用
        
        # 创建主窗口
        self.main_window = MainWindow(self.root, self)
        
        # 加载默认题库
        self.load_default_bank()
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_default_bank(self):
        """加载默认题库"""
        if os.path.exists(DEFAULT_QUESTION_FILE):
            success, msg = self.question_bank.load_from_json(DEFAULT_QUESTION_FILE)
            if success:
                self.root.after(100, self.main_window.update_statistics)
    
    def quick_exam(self, count):
        """快速学习"""
        stats = self.question_bank.get_statistics()
        total = stats['total']
        
        if total == 0:
            messagebox.showwarning("提示", "请先上传题库")
            return
        
        # 按比例分配题目
        single = min(int(count * stats['single'] / total) if total > 0 else 0, stats['single'])
        multiple = min(int(count * stats['multiple'] / total) if total > 0 else 0, stats['multiple'])
        judge = min(int(count * stats['judge'] / total) if total > 0 else 0, stats['judge'])
        
        while single + multiple + judge < count:
            if single < stats['single']:
                single += 1
            elif multiple < stats['multiple']:
                multiple += 1
            elif judge < stats['judge']:
                judge += 1
            else:
                break
        
        self.exam_counts = {
            'single_count': tk.StringVar(value=str(single)),
            'multiple_count': tk.StringVar(value=str(multiple)),
            'judge_count': tk.StringVar(value=str(judge))
        }
        self.exam_duration_var = tk.StringVar(value="30")
        self.exam_category_var = tk.StringVar(value="全部")
        
        self.start_exam()
    
    def start_exam(self):
        """开始学习"""
        try:
            single = int(self.exam_counts['single_count'].get() or "0")
            multiple = int(self.exam_counts['multiple_count'].get() or "0")
            judge = int(self.exam_counts['judge_count'].get() or "0")
            
            counts = {'single': single, 'multiple': multiple, 'judge': judge}
            
            if sum(counts.values()) == 0:
                messagebox.showwarning("提示", "请至少选择一道题目")
                return
            
            duration = int(self.exam_duration_var.get() or "30")
            if duration <= 0:
                messagebox.showwarning("提示", "请输入有效的学习时间")
                return
            self.exam_duration = duration * 60
            
            category = self.exam_category_var.get()
            if category == "全部":
                category = None
            
            questions = self.question_bank.get_random_questions(counts, category)
            
            if not questions:
                messagebox.showwarning("提示", "没有找到符合条件的题目")
                return
            
            self.current_paper = ExamPaper(questions)
            self.exam_submitted = False
            
            self.main_window.show_exam()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"开始学习失败: {str(e)}")
    
    def practice_wrong(self):
        """练习错题"""
        wrong_questions = self.wrong_bank.get_wrong_questions()
        if not wrong_questions:
            messagebox.showinfo("提示", "暂无错题")
            return
        
        self.current_paper = ExamPaper(wrong_questions)
        self.exam_submitted = False
        self.exam_duration = 60 * 60
        self.main_window.show_exam()
    
    def start_timer(self):
        """开始计时"""
        self.exam_start_time = datetime.now()
        self.update_timer()
    
    def update_timer(self):
        """更新计时器"""
        if not self.current_paper or not self.exam_start_time or self.exam_submitted:
            return
        
        elapsed = (datetime.now() - self.exam_start_time).seconds
        remaining = max(0, self.exam_duration - elapsed)
        
        minutes = remaining // 60
        seconds = remaining % 60
        if self.timer_label:
            self.timer_label.configure(text=f"⏱️ {minutes:02d}:{seconds:02d}")
        
        if remaining <= 0:
            self.timeout()
        else:
            self.timer_id = self.root.after(1000, self.update_timer)
    
    def stop_timer(self):
        """停止计时器"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def timeout(self):
        """时间到自动提交"""
        self.stop_timer()
        
        if self.current_paper and not self.exam_submitted:
            messagebox.showinfo("时间到", "学习时间结束，系统将自动提交")
            self.submit_exam()
    
    def submit_exam(self):
        """提交学习结果"""
        if not self.current_paper or self.exam_submitted:
            return
        
        self.exam_submitted = True
        self.stop_timer()
        
        # 收集答案
        for q in self.current_paper.questions:
            if hasattr(q, 'answer_var'):
                answer = q.answer_var.get()
                self.current_paper.submit_answer(q.id, answer)
            elif hasattr(q, 'answer_vars'):
                selected = [letter for letter, var in q.answer_vars if var.get()]
                self.current_paper.submit_answer(q.id, selected)
        
        # 批改
        result = self.current_paper.grade()
        self.exam_result = result
        
        # 添加到错题库
        for q in result['wrong_questions']:
            self.wrong_bank.add_wrong(q)
        
        # 添加学习记录
        record = {
            'date': datetime.now().isoformat()[:19],
            'score': result['score'],
            'correct': result['correct'],
            'total': result['total'],
            'time_spent': result['time_spent']
        }
        self.exam_records.add_record(record)
        
        # 显示结果
        self.main_window.show_result()
    
    def retry_exam(self):
        """再次练习相同的题目"""
        if hasattr(self, 'current_paper') and self.current_paper:
            questions = [q for q in self.current_paper.questions]
            self.current_paper = ExamPaper(questions)
            self.exam_submitted = False
            self.main_window.show_exam()
    
    def show_ai_assistant(self):
        """显示AI助手页面"""
        self.main_window.show_ai()
    
    def configure_ai(self):
        """配置小辰助教"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(f"配置{AI_ASSISTANT_NAME}")
        dialog.geometry("550x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.configure(fg_color=COLORS["darker"])
        
        main_frame = ctk.CTkFrame(dialog, fg_color=COLORS["card_bg"], corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text=f"🤖 {AI_ASSISTANT_NAME}配置",
            font=("Arial", 24, "bold"),
            text_color=COLORS["text"]
        ).pack(pady=20)
        
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30)
        
        # 启用开关
        enable_var = tk.BooleanVar(value=self.ai_config.enabled)
        enable_switch = ctk.CTkSwitch(
            form_frame,
            text=f"启用{AI_ASSISTANT_NAME}",
            variable=enable_var,
            font=("Arial", 14),
            progress_color=COLORS["primary"]
        )
        enable_switch.pack(anchor="w", pady=10)
        
        # 模型提供商
        ctk.CTkLabel(
            form_frame,
            text="模型提供商",
            font=("Arial", 14),
            text_color=COLORS["text"]
        ).pack(anchor="w", pady=(20,5))
        
        provider_var = tk.StringVar(value=self.ai_config.provider)
        providers = list(MODEL_CONFIGS.keys())
        provider_combo = ctk.CTkComboBox(
            form_frame,
            values=providers,
            variable=provider_var,
            width=400,
            height=40,
            font=("Arial", 13),
            command=lambda x: self._update_ai_config_fields(x, api_url_entry, model_entry)
        )
        provider_combo.pack(pady=(0,10))
        
        # API密钥
        ctk.CTkLabel(
            form_frame,
            text="API密钥",
            font=("Arial", 14),
            text_color=COLORS["text"]
        ).pack(anchor="w", pady=(10,5))
        
        api_key_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            height=40,
            font=("Arial", 13),
            placeholder_text="输入你的API密钥"
        )
        api_key_entry.insert(0, self.ai_config.api_key)
        api_key_entry.pack(pady=(0,10))
        
        # API地址
        ctk.CTkLabel(
            form_frame,
            text="API地址",
            font=("Arial", 14),
            text_color=COLORS["text"]
        ).pack(anchor="w", pady=(10,5))
        
        api_url_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            height=40,
            font=("Arial", 13)
        )
        api_url_entry.insert(0, self.ai_config.api_url)
        api_url_entry.pack(pady=(0,10))
        
        # 模型名称
        ctk.CTkLabel(
            form_frame,
            text="模型名称",
            font=("Arial", 14),
            text_color=COLORS["text"]
        ).pack(anchor="w", pady=(10,5))
        
        model_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            height=40,
            font=("Arial", 13)
        )
        model_entry.insert(0, self.ai_config.model)
        model_entry.pack(pady=(0,20))
        
        # 保存按钮
        from ui.components import GradientButton
        GradientButton(
            form_frame,
            text="保存配置",
            icon="💾",
            command=lambda: self._save_ai_config(enable_var.get(), provider_var.get(), 
                                               api_key_entry.get(), api_url_entry.get(), 
                                               model_entry.get(), dialog),
            fg_color=COLORS["success"],
            hover_color=COLORS["primary_dark"],
            height=45,
            width=200
        ).pack(pady=20)
    
    def _update_ai_config_fields(self, provider, url_entry, model_entry):
        """更新AI配置字段"""
        config = MODEL_CONFIGS.get(provider, MODEL_CONFIGS["自定义"])
        url_entry.delete(0, "end")
        url_entry.insert(0, config.get("api_url", ""))
        model_entry.delete(0, "end")
        model_entry.insert(0, config.get("model", ""))
    
    def _save_ai_config(self, enabled, provider, api_key, api_url, model, dialog):
        """保存AI配置"""
        self.ai_config.enabled = enabled
        self.ai_config.provider = provider
        self.ai_config.api_key = api_key
        self.ai_config.api_url = api_url
        self.ai_config.model = model
        self.ai_config.save_config()
        
        self.ai_assistant = AIAssistant(self.ai_config)
        
        # 关闭配置对话框
        dialog.destroy()
        
        # 自动刷新AI助手页面的状态
        self._refresh_ai_page_status()
        
        messagebox.showinfo("成功", f"{AI_ASSISTANT_NAME}配置已保存")
    
    def _refresh_ai_page_status(self):
        """自动刷新AI助手页面的状态"""
        # 如果当前在AI助手页面，自动刷新状态
        if hasattr(self.main_window, 'current_view') and self.main_window.current_view == 'ai':
            # 重新加载AI助手页面
            self.main_window.show_ai()
    
    def upload_file(self):
        """上传题库文件"""
        file_path = filedialog.askopenfilename(
            title="选择题库文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            success, msg = self.question_bank.load_from_json(file_path)
            
            if success:
                # 通知主窗口上传完成
                self.main_window.notify_upload_complete()
                messagebox.showinfo("成功", msg)
            else:
                messagebox.showerror("错误", msg)
            
        except Exception as e:
            messagebox.showerror("错误", f"加载失败: {str(e)}")
    
    def on_closing(self):
        """窗口关闭事件"""
        self.stop_timer()
        self.root.destroy()
    
    def run(self):
        """运行应用"""
        self.root.mainloop()


def main():
    """主函数"""
    
    app = ExamApp()
    app.run()


if __name__ == "__main__":
    main()