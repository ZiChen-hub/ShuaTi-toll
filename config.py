# config.py
import os

# 应用信息
APP_NAME = "小辰伴学"
APP_VERSION = "1.0.0"
AI_ASSISTANT_NAME = "小辰助教"

# 颜色方案
COLORS = {
    "primary": "#2ecc71",      # 翡翠绿
    "primary_dark": "#27ae60",  # 深绿
    "secondary": "#3498db",     # 蓝色
    "success": "#2ecc71",       # 成功绿
    "warning": "#f39c12",       # 橙色
    "danger": "#e74c3c",        # 红色
    "info": "#3498db",          # 信息蓝
    "dark": "#2c3e50",          # 深蓝灰
    "darker": "#1a2632",        # 更深色
    "light": "#ecf0f1",          # 浅灰
    "card_bg": "#2d3e50",        # 卡片背景
    "text": "#ffffff",           # 文字颜色
    "text_secondary": "#b0bec5"  # 次要文字
}

# 文件路径
DEFAULT_QUESTION_FILE = "题库.json"  # 改为通用名称
EXAM_RECORDS_FILE = "exam_records.json"
WRONG_QUESTIONS_FILE = "wrong_questions.json"
AI_CONFIG_FILE = "ai_config.json"
SUBJECTS_FILE = "subjects.json"  # 科目配置文件

# 模型提供商配置
MODEL_CONFIGS = {
    "通义千问": {
        "provider": "dashscope",
        "api_url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "model": "qwen-turbo",
        "headers": {"Content-Type": "application/json"},
        "auth_type": "Authorization"
    },
    "智谱AI": {
        "provider": "zhipu",
        "api_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "model": "glm-4",
        "headers": {"Content-Type": "application/json"},
        "auth_type": "Authorization"
    },
    "文心一言": {
        "provider": "wenxin",
        "api_url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions",
        "model": "ernie-3.5-8k",
        "headers": {"Content-Type": "application/json"},
        "auth_type": "Authorization"
    },
    "DeepSeek": {
        "provider": "deepseek",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "headers": {"Content-Type": "application/json"},
        "auth_type": "Authorization"
    },
    "OpenAI": {
        "provider": "openai",
        "api_url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-3.5-turbo",
        "headers": {"Content-Type": "application/json"},
        "auth_type": "Authorization"
    },
    "自定义": {
        "provider": "custom",
        "api_url": "",
        "model": "",
        "headers": {"Content-Type": "application/json"},
        "auth_type": "Authorization"
    }
}

# AI助教系统提示词 - 通用版本
AI_SYSTEM_PROMPT = """你的名字叫小辰，是一位全能学习助教。请遵循以下原则：

🎯 回答风格：
1. 简洁明了：用最少的字数说清楚问题，避免啰嗦
2. 直击要点：直接回答问题核心，不要绕弯子
3. 结构清晰：适当使用列表、分段，但不要太长
4. 态度友好：保持亲切但不啰嗦

📚 知识范围：
- 理工科：数学、物理、化学、生物、计算机
- 文史哲：语文、历史、哲学、艺术
- 社会科学：政治、经济、法律
- 专业技能：编程、设计、工程

💡 回答示例：
❌ 错误示例（太啰嗦）：
"关于这个问题，首先我们要从历史的角度来看，追溯到古希腊时期...经过漫长的发展...综上所述..."

✅ 正确示例（简洁）：
"答案是X。因为Y（一句话解释）。如果需要详细讲解，请告诉我。"

记住：简洁是智慧的灵魂！"""