# ai/ai_config.py
import json
import os
from config import AI_CONFIG_FILE, MODEL_CONFIGS


class AIConfig:
    """AI配置类"""
    def __init__(self):
        self.provider = "openai"
        self.api_key = ""
        self.api_url = ""
        self.model = ""
        self.enabled = False
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists(AI_CONFIG_FILE):
                with open(AI_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.provider = data.get('provider', 'openai')
                    self.api_key = data.get('api_key', '')
                    self.api_url = data.get('api_url', '')
                    self.model = data.get('model', '')
                    self.enabled = data.get('enabled', False)
        except:
            pass
    
    def save_config(self):
        """保存配置"""
        try:
            data = {
                'provider': self.provider,
                'api_key': self.api_key,
                'api_url': self.api_url,
                'model': self.model,
                'enabled': self.enabled
            }
            with open(AI_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def get_model_config(self):
        """获取模型配置"""
        return MODEL_CONFIGS.get(self.provider, MODEL_CONFIGS["自定义"])