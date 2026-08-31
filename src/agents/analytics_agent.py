from .base_agent import BaseAgent, Task
from typing import Any, Dict, List
import asyncio
import json


class AnalyticsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="AnalyticsAgent",
            capabilities=["data_analysis", "market_research", "reporting", "forecasting"]
        )
        self.rates = {
            "market_analysis": 150,
            "data_report": 200,
            "forecast": 250,
            "competitor_analysis": 180
        }
        
    def can_handle_task(self, task: Task) -> bool:
        analytics_types = ["data_analysis", "market_research", "reporting", "forecasting"]
        return any(cap in task.parameters.get("type", "") for cap in analytics_types)
    
    async def execute_task(self, task: Task) -> Any:
        task_type = task.parameters.get("type", "market_analysis")
        subject = task.parameters.get("subject", "market")
        
        report = await self.generate_analysis(task_type, subject)
        
        return {
            "report": report,
            "type": task_type,
            "subject": subject,
            "estimated_value": self.rates.get(task_type, 150)
        }
    
    async def generate_analysis(self, analysis_type: str, subject: str) -> Dict[str, Any]:
        prompts = {
            "market_analysis": f"Проведи анализ рынка '{subject}'. Опиши: размер рынка, тенденции, возможности, рекомендации. Формат: JSON.",
            "data_report": f"Создай аналитический отчёт по данным '{subject}'. Включи: ключевые метрики, инсайты, визуализации. Формат: JSON.",
            "forecast": f"Сделай прогноз по '{subject}' на следующий квартал. Включи: прогноз дохода, рост, уровень риска. Формат: JSON.",
            "competitor_analysis": f"Проведи анализ конкурентов в сфере '{subject}'. Опиши: сильные/слабые стороны, позиция на рынке. Формат: JSON."
        }
        
        prompt = prompts.get(analysis_type, f"Проанализируй: {subject}")
        
        response = await self.generate_with_llm(prompt)
        
        try:
            report = json.loads(response)
        except:
            report = {"analysis": response}
        
        return report