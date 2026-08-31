import asyncio
from src.core.manager import AgentManager
from src.agents.content_agent import ContentAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.agents.technical_agent import TechnicalAgent
from src.agents.marketing_agent import MarketingAgent
from src.agents.finance_agent import FinanceAgent
import random
from datetime import datetime


async def generate_random_tasks(manager: AgentManager):
    task_templates = [
        {"type": "blog_posts", "topic": "AI technology", "priority": 1},
        {"type": "social_media", "topic": "digital marketing", "priority": 2},
        {"type": "market_analysis", "subject": "e-commerce", "priority": 1},
        {"type": "automation_script", "requirements": {"target": "data_collection"}, "priority": 3},
        {"type": "seo_optimization", "target_audience": "young professionals", "priority": 2},
        {"type": "budget_planning", "parameters": {"department": "marketing"}, "priority": 1},
        {"type": "data_report", "subject": "customer_behavior", "priority": 2},
        {"type": "web_scraping", "requirements": {"urls": ["competitor1.com", "competitor2.com"]}, "priority": 1},
        {"type": "social_media_campaign", "target_audience": "tech enthusiasts", "budget": 2000, "priority": 3},
        {"type": "investment_report", "parameters": {"portfolio": "growth"}, "priority": 2}
    ]
    
    while True:
        task_data = random.choice(task_templates)
        task_data["type"] = random.choice([
            "writing", "blog_posts", "social_media", "copywriting",
            "data_analysis", "market_research", "reporting", "forecasting",
            "development", "automation", "scripting", "api_integration",
            "social_media", "advertising", "seo", "content_marketing",
            "budgeting", "investment_analysis", "financial_planning", "accounting"
        ])
        
        await manager.create_task(
            description=f"Task: {task_data.get('topic', task_data.get('subject', task_data.get('type', 'general')))}",
            parameters=task_data,
            priority=task_data.get("priority", 1)
        )
        await asyncio.sleep(random.uniform(5, 15))


async def monitor_performance(manager: AgentManager):
    while True:
        stats = manager.get_agent_stats()
        print("\n" + "="*50)
        print(f"Agent Performance Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        total_completed = 0
        total_failed = 0
        
        for agent_name, agent_stats in stats.items():
            completed = agent_stats["completed_tasks"]
            failed = agent_stats["failed_tasks"]
            busy = "Busy" if agent_stats["is_busy"] else "Available"
            
            total_completed += completed
            total_failed += failed
            
            print(f"{agent_name:20} | Completed: {completed:3} | Failed: {failed:3} | Status: {busy}")
        
        print("-"*50)
        print(f"{'Total':20} | Completed: {total_completed:3} | Failed: {total_failed:3}")
        print("="*50)
        
        await asyncio.sleep(30)


async def main():
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
        asyncio.create_task(agent.process_tasks())
    
    print("AI Agent Company initialized!")
    print(f"Registered {len(agents)} agents: {[agent.name for agent in agents]}")
    print("Starting task generation and processing...")
    
    await asyncio.generate(
        manager.process_all_tasks(),
        generate_random_tasks(manager),
        monitor_performance(manager)
    )


if __name__ == "__main__":
    asyncio.run(main())