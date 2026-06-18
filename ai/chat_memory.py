# ai/chat_memory.py
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from collections import deque


class ChatMessage:
    """对话消息"""
    def __init__(self, role: str, content: str, timestamp: float = None):
        self.role = role  # 'user' 或 'assistant'
        self.content = content
        self.timestamp = timestamp or datetime.now().timestamp()
    
    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['role'], data['content'], data['timestamp'])


class ChatSession:
    """对话会话"""
    def __init__(self, session_id: str = None):
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.messages: List[ChatMessage] = []
        self.created_at = datetime.now().timestamp()
        self.updated_at = self.created_at
        self.title = "新对话"
        self.context = {}  # 额外上下文信息
    
    def add_message(self, role: str, content: str):
        """添加消息"""
        message = ChatMessage(role, content)
        self.messages.append(message)
        self.updated_at = datetime.now().timestamp()
        
        # 如果是第一条用户消息，用它作为对话标题
        if len(self.messages) == 1 and role == 'user':
            self.title = content[:20] + "..." if len(content) > 20 else content
    
    def get_recent_messages(self, count: int = 10) -> List[ChatMessage]:
        """获取最近的消息"""
        return self.messages[-count:]
    
    def get_messages_for_api(self, max_tokens: int = 2000) -> List[Dict]:
        """获取适合API调用的消息格式"""
        messages = []
        total_chars = 0
        
        # 从最新的消息开始往前取，直到达到token限制
        for msg in reversed(self.messages):
            msg_chars = len(msg.content)
            if total_chars + msg_chars > max_tokens * 4:  # 粗略估计：1 token ≈ 4字符
                break
            messages.insert(0, {"role": msg.role, "content": msg.content})
            total_chars += msg_chars
        
        return messages
    
    def clear_history(self):
        """清空历史"""
        self.messages = []
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'session_id': self.session_id,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'messages': [msg.to_dict() for msg in self.messages],
            'context': self.context
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """从字典创建"""
        session = cls(data['session_id'])
        session.title = data.get('title', '新对话')
        session.created_at = data.get('created_at', session.created_at)
        session.updated_at = data.get('updated_at', session.updated_at)
        session.messages = [ChatMessage.from_dict(m) for m in data.get('messages', [])]
        session.context = data.get('context', {})
        return session


class ChatMemory:
    """对话记忆管理器"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.sessions: Dict[str, ChatSession] = {}
        self.current_session_id: str = None
        self.memory_file = "chat_memory.json"
        self.max_sessions = 50  # 最多保存50个会话
        self.load_memory()
    
    def new_session(self) -> ChatSession:
        """创建新会话"""
        session = ChatSession()
        self.sessions[session.session_id] = session
        self.current_session_id = session.session_id
        self._trim_sessions()
        self.save_memory()
        return session
    
    def get_current_session(self) -> ChatSession:
        """获取当前会话"""
        if not self.current_session_id or self.current_session_id not in self.sessions:
            return self.new_session()
        return self.sessions[self.current_session_id]
    
    def switch_session(self, session_id: str) -> bool:
        """切换会话"""
        if session_id in self.sessions:
            self.current_session_id = session_id
            return True
        return False
    
    def add_message(self, role: str, content: str):
        """添加消息到当前会话"""
        session = self.get_current_session()
        session.add_message(role, content)
        self.save_memory()
    
    def get_conversation_history(self, max_messages: int = 10) -> List[Dict]:
        """获取对话历史"""
        session = self.get_current_session()
        return session.get_messages_for_api(max_tokens=2000)
    
    def get_all_sessions(self) -> List[Dict]:
        """获取所有会话列表"""
        sessions = []
        for session in self.sessions.values():
            sessions.append({
                'id': session.session_id,
                'title': session.title,
                'created_at': session.created_at,
                'updated_at': session.updated_at,
                'message_count': len(session.messages)
            })
        # 按更新时间排序
        return sorted(sessions, key=lambda x: x['updated_at'], reverse=True)
    
    def delete_session(self, session_id: str):
        """删除会话"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            if self.current_session_id == session_id:
                self.current_session_id = None
            self.save_memory()
    
    def clear_all_sessions(self):
        """清空所有会话"""
        self.sessions = {}
        self.current_session_id = None
        self.save_memory()
    
    def _trim_sessions(self):
        """限制会话数量"""
        if len(self.sessions) > self.max_sessions:
            # 按更新时间排序，保留最新的
            sorted_sessions = sorted(
                self.sessions.values(),
                key=lambda x: x.updated_at,
                reverse=True
            )
            keep_sessions = sorted_sessions[:self.max_sessions]
            self.sessions = {s.session_id: s for s in keep_sessions}
    
    def save_memory(self):
        """保存记忆到文件"""
        try:
            data = {
                'current_session_id': self.current_session_id,
                'sessions': {sid: session.to_dict() for sid, session in self.sessions.items()}
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存记忆失败: {e}")
    
    def load_memory(self):
        """从文件加载记忆"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.current_session_id = data.get('current_session_id')
                self.sessions = {}
                for sid, session_data in data.get('sessions', {}).items():
                    self.sessions[sid] = ChatSession.from_dict(session_data)
        except Exception as e:
            print(f"加载记忆失败: {e}")
            self.sessions = {}
            self.current_session_id = None