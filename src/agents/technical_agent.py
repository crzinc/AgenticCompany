from .base_agent import BaseAgent, Task
from typing import Any, Dict, List
import asyncio
import json


class TechnicalAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TechnicalAgent",
            capabilities=["development", "automation", "scripting", "api_integration"]
        )
        self.rates = {
            "automation_script": 300,
            "api_integration": 400,
            "web_scraping": 250,
            "data_processing": 350
        }
        
    def can_handle_task(self, task: Task) -> bool:
        tech_types = ["development", "automation", "scripting", "api_integration"]
        return any(cap in task.parameters.get("type", "") for cap in tech_types)
    
    async def execute_task(self, task: Task) -> Any:
        task_type = task.parameters.get("type", "automation_script")
        requirements = task.parameters.get("requirements", {})
        
        solution = await self.develop_solution(task_type, requirements)
        
        return {
            "solution": solution,
            "type": task_type,
            "estimated_value": self.rates.get(task_type, 300),
            "delivery_time": "1-7 days"
        }
    
    async def develop_solution(self, solution_type: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        prompts = {
            "automation_script": f"Разработай скрипт автоматизации для: {json.dumps(requirements)}. Опиши: название, функции, сложность. Формат: JSON.",
            "api_integration": f"Спроектируй интеграцию API для: {json.dumps(requirements)}. Опиши: тип, эндпоинты, аутентификация. Формат: JSON.",
            "web_scraping": f"Создай веб-скрапер для: {json.dumps(requirements)}. Опиши: сайты, данные, форматы вывода. Формат: JSON.",
            "data_processing": f"Спроектируй пайплайн обработки данных для: {json.dumps(requirements)}. Опиши: шаги, объём, время. Формат: JSON."
        }
        
        prompt = prompts.get(solution_type, f"Разработай решение: {json.dumps(requirements)}")
        
        response = await self.generate_with_llm(prompt)
        
        try:
            solution = json.loads(response)
        except:
            solution = {"description": response}
        
        return solution