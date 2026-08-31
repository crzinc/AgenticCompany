import { NextResponse } from 'next/server'

const mockAgents = [
  {
    id: '1',
    name: 'ContentAgent',
    type: 'content',
    status: 'active',
    tasksCompleted: 45,
    earnings: 2250,
    capabilities: ['writing', 'blog_posts', 'social_media', 'copywriting']
  },
  {
    id: '2',
    name: 'AnalyticsAgent',
    type: 'analytics',
    status: 'active',
    tasksCompleted: 32,
    earnings: 4800,
    capabilities: ['data_analysis', 'market_research', 'reporting', 'forecasting']
  },
  {
    id: '3',
    name: 'TechnicalAgent',
    type: 'technical',
    status: 'idle',
    tasksCompleted: 18,
    earnings: 5400,
    capabilities: ['development', 'automation', 'scripting', 'api_integration']
  },
  {
    id: '4',
    name: 'MarketingAgent',
    type: 'marketing',
    status: 'active',
    tasksCompleted: 28,
    earnings: 8400,
    capabilities: ['social_media', 'advertising', 'seo', 'content_marketing']
  },
  {
    id: '5',
    name: 'FinanceAgent',
    type: 'finance',
    status: 'active',
    tasksCompleted: 22,
    earnings: 6600,
    capabilities: ['budgeting', 'investment_analysis', 'financial_planning', 'accounting']
  }
]

export async function GET() {
  return NextResponse.json(mockAgents)
}

export async function POST(request: Request) {
  const body = await request.json()
  
  const newAgent = {
    id: String(mockAgents.length + 1),
    name: body.name,
    type: body.type,
    status: 'idle',
    tasksCompleted: 0,
    earnings: 0,
    capabilities: body.capabilities || []
  }
  
  mockAgents.push(newAgent)
  
  return NextResponse.json(newAgent, { status: 201 })
}