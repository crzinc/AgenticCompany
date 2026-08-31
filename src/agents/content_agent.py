from .base_agent import BaseAgent, Task
from typing import Any, List
import asyncio
import json


class ContentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ContentAgent",
            capabilities=["writing", "blog_posts", "social_media", "copywriting"]
        )
        self.rates = {
            "blog_post": 50,
            "social_media_post": 20,
            "article": 100,
            "copywriting": 75
        }
        
    def can_handle_task(self, task: Task) -> bool:
        content_types = ["writing", "blog_posts", "social_media", "copywriting"]
        return any(cap in task.parameters.get("type", "") for cap in content_types)
    
    async def execute_task(self, task: Task) -> Any:
        task_type = task.parameters.get("type", "blog_post")
        topic = task.parameters.get("topic", "general")
        
        content = await self.generate_content(task_type, topic)
        
        return {
            "content": content,
            "type": task_type,
            "word_count": len(content.split()),
            "estimated_value": self.rates.get(task_type, 50)
        }
    
    async def generate_content(self, content_type: str, topic: str) -> str:
        prompts = {
            "blog_post": f"Напиши блог-пост на тему '{topic}'. Объем 300-500 слов. Стиль: экспертный, но доступный.",
            "social_media_post": f"Создай пост для соцсетей о {topic}'. Объем 50-100 слов. Добавь эмодзи и хэштеги.",
            "article": f"Напиши статью на тему '{topic}'. Объем 800-1000 слов. Структура: введение, основная часть, заключение.",
            "copywriting": f"Создай рекламный текст о {topic}'. Объем 100-200 слов. Стиль: убедительный, с призывом к действию."
        }
        
        prompt = prompts.get(content_type, f"Напиши контент на тему: {topic}")
        
        content = await self.generate_with_llm(prompt)
        
        return content