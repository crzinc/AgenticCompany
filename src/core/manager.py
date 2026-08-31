from typing import List, Dict, Any
from ..agents.base_agent import BaseAgent, Task
import asyncio
from datetime import datetime
import uuid


class AgentManager:
    def __init__(self):
        self.agents: List[BaseAgent] = []
        self.tasks: List[Task] = []
        self.task_queue: asyncio.Queue = asyncio.Queue()
        
    def register_agent(self, agent: BaseAgent):
        self.agents.append(agent)
        
    async def create_task(self, description: str, parameters: Dict[str, Any], priority: int = 1) -> Task:
        task = Task(
            id=str(uuid.uuid4()),
            description=description,
            parameters=parameters,
            priority=priority,
            created_at=datetime.now()
        )
        self.tasks.append(task)
        await self.task_queue.put(task)
        return task
    
    async def assign_task_to_agent(self, task: Task) -> bool:
        for agent in self.agents:
            if await agent.assign_task(task):
                return True
        return False
    
    async def process_all_tasks(self):
        while True:
            if not self.task_queue.empty():
                task = await self.task_queue.get()
                if not await self.assign_task_to_agent(task):
                    await self.task_queue.put(task)
            await asyncio.sleep(0.1)
    
    def get_agent_stats(self) -> Dict[str, Any]:
        stats = {}
        for agent in self.agents:
            completed = len([t for t in agent.tasks if t.status == "completed"])
            failed = len([t for t in agent.tasks if t.status == "failed"])
            stats[agent.name] = {
                "completed_tasks": completed,
                "failed_tasks": failed,
                "is_busy": agent.is_busy
            }
        return stats