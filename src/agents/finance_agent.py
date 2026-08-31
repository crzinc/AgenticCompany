from .base_agent import BaseAgent, Task
from typing import Any, Dict, List
from datetime import datetime, timedelta
import asyncio
import json


class FinanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="FinanceAgent",
            capabilities=["budgeting", "investment_analysis", "financial_planning", "accounting"]
        )
        self.rates = {
            "budget_planning": 300,
            "investment_report": 450,
            "financial_forecast": 500,
            "expense_analysis": 350
        }
        
    def can_handle_task(self, task: Task) -> bool:
        finance_types = ["budgeting", "investment_analysis", "financial_planning", "accounting"]
        return any(cap in task.parameters.get("type", "") for cap in finance_types)
    
    async def execute_task(self, task: Task) -> Any:
        task_type = task.parameters.get("type", "budget_planning")
        parameters = task.parameters.get("parameters", {})
        
        financial_data = await self.process_financial_data(task_type, parameters)
        
        return {
            "financial_data": financial_data,
            "type": task_type,
            "estimated_value": self.rates.get(task_type, 300),
            "next_review": (datetime.now() + timedelta(days=30)).isoformat()
        }
    
    async def process_financial_data(self, data_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        prompts = {
            "budget_planning": f"Составь бюджет на основе данных: {json.dumps(parameters)}. Опиши: категории, фонды, оптимизация. Формат: JSON.",
            "investment_report": f"Создай отчёт об инвестициях: {json.dumps(parameters)}. Опиши: портфель, доходность, рекомендации. Формат: JSON.",
            "financial_forecast": f"Сделай финансовый прогноз: {json.dumps(parameters)}. Опиши: прогноз доходов/расходов, сценарии. Формат: JSON.",
            "expense_analysis": f"Проанализируй расходы: {json.dumps(parameters)}. Опиши: статьи, оптимизация, экономия. Формат: JSON."
        }
        
        prompt = prompts.get(data_type, f"Обработай финансовые данные: {json.dumps(parameters)}")
        
        response = await self.generate_with_llm(prompt)
        
        try:
            data = json.loads(response)
        except:
            data = {"analysis": response}
        
        return data