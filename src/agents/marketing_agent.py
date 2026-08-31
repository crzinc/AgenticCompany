from .base_agent import BaseAgent, Task
from typing import Any, Dict, List
import asyncio
import json


class MarketingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MarketingAgent",
            capabilities=["social_media", "advertising", "seo", "content_marketing"]
        )
        self.rates = {
            "social_media_campaign": 400,
            "seo_optimization": 500,
            "advertising_strategy": 600,
            "content_calendar": 350
        }
        
    def can_handle_task(self, task: Task) -> bool:
        marketing_types = ["social_media", "advertising", "seo", "content_marketing"]
        return any(cap in task.parameters.get("type", "") for cap in marketing_types)
    
    async def execute_task(self, task: Task) -> Any:
        task_type = task.parameters.get("type", "social_media_campaign")
        target_audience = task.parameters.get("target_audience", "general")
        budget = task.parameters.get("budget", 1000)
        
        strategy = await self.create_marketing_strategy(task_type, target_audience, budget)
        
        return {
            "strategy": strategy,
            "type": task_type,
            "estimated_value": self.rates.get(task_type, 400),
            "roi_projection": "150-400%"
        }
    
    async def create_marketing_strategy(self, strategy_type: str, audience: str, budget: int) -> Dict[str, Any]:
        prompts = {
            "social_media_campaign": f"Создай стратегию продвижения в соцсетях для аудитории '{audience}'. Бюджет: ${budget}. Опиши: платформы, контент, частота постов. Формат: JSON.",
            "seo_optimization": f"Разработай SEO-стратегию для сайта на тему '{audience}'. Опиши: ключевые слова, оптимизация, ссылки. Формат: JSON.",
            "advertising_strategy": f"Создай рекламную стратегию для '{audience}'. Бюджет: ${budget}. Опиши: каналы, форматы, KPI. Формат: JSON.",
            "content_calendar": f"Создай контент-календарь на месяц для '{audience}'. Опиши: темы, форматы, расписание. Формат: JSON."
        }
        
        prompt = prompts.get(strategy_type, f"Создай маркетинговую стратегию для {audience}")
        
        response = await self.generate_with_llm(prompt)
        
        try:
            strategy = json.loads(response)
        except:
            strategy = {"description": response}
        
        return strategy