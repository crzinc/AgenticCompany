from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.core.manager import AgentManager
from src.agents.content_agent import ContentAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.agents.technical_agent import TechnicalAgent
from src.agents.marketing_agent import MarketingAgent
from src.agents.finance_agent import FinanceAgent

load_dotenv()

app = FastAPI(title="AgenticCompany API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = AgentManager()

agents = [
    ContentAgent(),
    AnalyticsAgent(),
    TechnicalAgent(),
    MarketingAgent(),
    FinanceAgent()
]

for agent in agents:
    manager.register_agent(agent)


@app.get("/health")
async def health_check():
    return {"status": "ok", "agents": len(agents)}


@app.get("/api/stats")
async def get_stats():
    stats = manager.get_agent_stats()
    total_completed = sum(s["completed_tasks"] for s in stats.values())
    total_failed = sum(s["failed_tasks"] for s in stats.values())
    active_agents = sum(1 for s in stats.values() if s["is_busy"])
    
    return {
        "totalAgents": len(agents),
        "activeAgents": active_agents,
        "completedTasks": total_completed,
        "totalEarnings": total_completed * 100
    }


@app.get("/api/agents")
async def get_agents():
    stats = manager.get_agent_stats()
    agents_data = []
    for agent in agents:
        agent_stats = stats.get(agent.name, {})
        agents_data.append({
            "id": agent.name.lower(),
            "name": agent.name,
            "type": agent.name.replace("Agent", "").lower(),
            "status": "active" if agent_stats.get("is_busy") else "idle",
            "tasksCompleted": agent_stats.get("completed_tasks", 0),
            "earnings": agent_stats.get("completed_tasks", 0) * 100,
            "capabilities": agent.capabilities
        })
    return agents_data


@app.get("/api/tasks")
async def get_tasks():
    tasks_data = []
    for agent in agents:
        for task in agent.tasks:
            tasks_data.append({
                "id": task.id,
                "description": task.description,
                "type": task.parameters.get("type", "general"),
                "status": task.status,
                "agent": agent.name,
                "earnings": 100 if task.status == "completed" else 0,
                "createdAt": task.created_at.isoformat()
            })
    return tasks_data


@app.post("/api/tasks")
async def create_task(task_data: dict):
    task = await manager.create_task(
        description=task_data.get("description", ""),
        parameters=task_data.get("parameters", {}),
        priority=task_data.get("priority", 1)
    )
    return {"id": task.id, "status": "created"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)