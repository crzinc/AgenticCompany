import asyncio
import pytest
from src.core.manager import AgentManager
from src.agents.content_agent import ContentAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.agents.technical_agent import TechnicalAgent
from src.agents.marketing_agent import MarketingAgent
from src.agents.finance_agent import FinanceAgent


@pytest.mark.asyncio
async def test_agent_registration():
    manager = AgentManager()
    agent = ContentAgent()
    
    manager.register_agent(agent)
    
    assert len(manager.agents) == 1
    assert manager.agents[0].name == "ContentAgent"


@pytest.mark.asyncio
async def test_task_creation():
    manager = AgentManager()
    
    task = await manager.create_task(
        description="Test task",
        parameters={"type": "blog_posts", "topic": "AI"},
        priority=1
    )
    
    assert task.status == "pending"
    assert task.description == "Test task"
    assert len(manager.tasks) == 1


@pytest.mark.asyncio
async def test_agent_task_assignment():
    manager = AgentManager()
    agent = ContentAgent()
    manager.register_agent(agent)
    
    task = await manager.create_task(
        description="Write blog post",
        parameters={"type": "blog_posts", "topic": "technology"},
        priority=1
    )
    
    success = await manager.assign_task_to_agent(task)
    
    assert success is True
    assert task.status == "assigned"


@pytest.mark.asyncio
async def test_agent_task_execution():
    agent = ContentAgent()
    
    from src.agents.base_agent import Task
    from datetime import datetime
    
    task = Task(
        id="test-1",
        description="Test content creation",
        parameters={"type": "blog_posts", "topic": "AI"},
        priority=1,
        created_at=datetime.now()
    )
    
    result = await agent.execute_task(task)
    
    assert "content" in result
    assert "type" in result
    assert "estimated_value" in result


@pytest.mark.asyncio
async def test_multiple_agents():
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
    
    assert len(manager.agents) == 5
    
    task = await manager.create_task(
        description="Complex task",
        parameters={"type": "market_analysis", "subject": "technology"},
        priority=1
    )
    
    success = await manager.assign_task_to_agent(task)
    assert success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])