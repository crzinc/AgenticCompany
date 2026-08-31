import { NextResponse } from 'next/server'

const mockTasks = [
  {
    id: '1',
    description: 'Написать блог-пост о AI',
    type: 'content',
    status: 'completed',
    agent: 'ContentAgent',
    earnings: 50,
    createdAt: new Date(Date.now() - 86400000).toISOString()
  },
  {
    id: '2',
    description: 'Анализ рынка e-commerce',
    type: 'analytics',
    status: 'completed',
    agent: 'AnalyticsAgent',
    earnings: 150,
    createdAt: new Date(Date.now() - 172800000).toISOString()
  },
  {
    id: '3',
    description: 'Скрипт автоматизации сбора данных',
    type: 'technical',
    status: 'processing',
    agent: 'TechnicalAgent',
    createdAt: new Date(Date.now() - 3600000).toISOString()
  },
  {
    id: '4',
    description: 'SEO-стратегия для сайта',
    type: 'marketing',
    status: 'pending',
    createdAt: new Date().toISOString()
  },
  {
    id: '5',
    description: 'Финансовый прогноз на квартал',
    type: 'finance',
    status: 'completed',
    agent: 'FinanceAgent',
    earnings: 200,
    createdAt: new Date(Date.now() - 259200000).toISOString()
  }
]

export async function GET() {
  return NextResponse.json(mockTasks)
}

export async function POST(request: Request) {
  const body = await request.json()
  
  const newTask = {
    id: String(mockTasks.length + 1),
    description: body.description,
    type: body.type,
    status: 'pending',
    createdAt: new Date().toISOString()
  }
  
  mockTasks.push(newTask)
  
  return NextResponse.json(newTask, { status: 201 })
}