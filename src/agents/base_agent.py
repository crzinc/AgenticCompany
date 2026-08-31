from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import asyncio
from datetime import datetime
import os
import httpx


class Task(BaseModel):
    id: str
    description: str
    parameters: Dict[str, Any]
    priority: int = 1
    status: str = "pending"
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None


class FreeLLMClient:
    def __init__(self):
        self.hf_key = os.getenv("HUGGINGFACE_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.google_key = os.getenv("GOOGLE_API_KEY")
        
    async def generate(self, prompt: str) -> str:
        if self.groq_key:
            return await self._groq_generate(prompt)
        elif self.hf_key:
            return await self._huggingface_generate(prompt)
        elif self.google_key:
            return await self._gemini_generate(prompt)
        else:
            return await self._fallback_generate(prompt)
    
    async def _groq_generate(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1024
                },
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return f"Error: {response.status_code}"
    
    async def _huggingface_generate(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                headers={"Authorization": f"Bearer {self.hf_key}"},
                json={"inputs": prompt},
                timeout=60.0
            )
            if response.status_code == 200:
                return response.json()[0]["generated_text"]
            return f"Error: {response.status_code}"
    
    async def _gemini_generate(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.google_key}",
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return f"Error: {response.status_code}"
    
    async def _fallback_generate(self, prompt: str) -> str:
        return f"Обработка запроса: {prompt[:100]}... [Локальный режим - добавьте API ключ в .env]"


class BaseAgent(ABC):
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.tasks: List[Task] = []
        self.is_busy = False
        self.llm = FreeLLMClient()
        
    @abstractmethod
    async def execute_task(self, task: Task) -> Any:
        pass
    
    @abstractmethod
    def can_handle_task(self, task: Task) -> bool:
        pass
    
    async def generate_with_llm(self, prompt: str) -> str:
        try:
            response = await self.llm.generate(prompt)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def assign_task(self, task: Task) -> bool:
        if self.can_handle_task(task) and not self.is_busy:
            self.tasks.append(task)
            task.status = "assigned"
            return True
        return False
    
    async def process_tasks(self):
        while True:
            pending_tasks = [t for t in self.tasks if t.status == "assigned"]
            if pending_tasks:
                self.is_busy = True
                task = pending_tasks[0]
                task.status = "processing"
                try:
                    result = await self.execute_task(task)
                    task.result = result
                    task.status = "completed"
                    task.completed_at = datetime.now()
                except Exception as e:
                    task.status = "failed"
                    task.result = str(e)
                finally:
                    self.is_busy = False
            await asyncio.sleep(1)