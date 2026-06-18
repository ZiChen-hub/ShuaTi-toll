# ai/ai_assistant.py
import requests
import json
from ai.ai_config import AIConfig
from ai.chat_memory import ChatMemory
from config import MODEL_CONFIGS, AI_SYSTEM_PROMPT, AI_ASSISTANT_NAME


class AIAssistant:
    """AI助手类 - 小辰助教（带记忆功能）"""
    
    def __init__(self, config: AIConfig):
        self.config = config
        self.name = AI_ASSISTANT_NAME
        self.memory = ChatMemory()  # 记忆管理器
    
    def ask(self, question: str, context: str = "", subject: str = "", concise: bool = True) -> str:
        """向AI提问，带记忆功能"""
        if not self.config.enabled or not self.config.api_key:
            return f"请先在设置中配置并启用{self.name}"
        
        # 保存用户问题到记忆
        full_question = f"[{subject}] {question}" if subject else question
        if context:
            full_question = f"题目：{context}\n问题：{full_question}"
        self.memory.add_message('user', full_question)
        
        model_config = self.config.get_model_config()
        
        headers = model_config.get("headers", {}).copy()
        auth_type = model_config.get("auth_type", "Authorization")
        headers[auth_type] = f"Bearer {self.config.api_key}"
        
        # 构建系统提示词
        system_prompt = AI_SYSTEM_PROMPT
        if concise:
            system_prompt += "\n\n【重要】请保持回答简洁，50字内能说清就不要用100字。"
        
        if subject:
            system_prompt += f"\n\n当前学生正在学习【{subject}】科目。"
        
        # 添加对话历史提示
        system_prompt += "\n\n【注意】请记住我们之前的对话内容，保持上下文连贯。"
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加对话历史（最近10条）
        history = self.memory.get_conversation_history()
        messages.extend(history)
        
        provider = model_config.get("provider", "openai")
        
        # 参数设置
        temperature = 0.3 if concise else 0.7
        max_tokens = 800 if concise else 2000
        
        if provider == "dashscope":
            data = {
                "model": self.config.model or model_config.get("model", "qwen-turbo"),
                "input": {"messages": messages},
                "parameters": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "top_p": 0.8,
                    "repetition_penalty": 1.1
                }
            }
        elif provider == "zhipu":
            data = {
                "model": self.config.model or model_config.get("model", "glm-4-flash"),
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.8,
                "do_sample": False
            }
        elif provider == "wenxin":
            data = {
                "messages": messages,
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": 0.8,
                "penalty_score": 1.1
            }
        else:
            data = {
                "model": self.config.model or model_config.get("model", "gpt-3.5-turbo"),
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.8,
                "frequency_penalty": 0.5
            }
        
        response = self._call_api(self.config.api_url or model_config["api_url"], headers, data, provider)
        
        # 保存AI回答到记忆
        self.memory.add_message('assistant', response)
        
        return response
    
    def _call_api(self, url, headers, data, provider):
        """调用API"""
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return self._parse_response(result, provider)
        except requests.exceptions.RequestException as e:
            return f"{self.name}请求失败: {str(e)}"
        except Exception as e:
            return f"{self.name}请求失败: {str(e)}"
    
    def _parse_response(self, result, provider):
        """解析响应"""
        try:
            if provider == "dashscope":
                if "output" in result and "text" in result["output"]:
                    return result["output"]["text"]
                elif "output" in result and "choices" in result["output"]:
                    return result["output"]["choices"][0]["message"]["content"]
            elif provider in ["zhipu", "openai", "custom", "deepseek"]:
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
            elif provider == "wenxin":
                if "result" in result:
                    return result["result"]
            return str(result)
        except:
            return str(result)
    
    def new_conversation(self):
        """开启新对话"""
        self.memory.new_session()
        return "已开启新的对话，让我们重新开始吧！"
    
    def get_conversations(self):
        """获取所有对话列表"""
        return self.memory.get_all_sessions()
    
    def switch_conversation(self, session_id: str):
        """切换对话"""
        return self.memory.switch_session(session_id)
    
    def delete_conversation(self, session_id: str):
        """删除对话"""
        self.memory.delete_session(session_id)