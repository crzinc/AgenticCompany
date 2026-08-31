import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const range = searchParams.get('range') || 'week'
  
  const dailyEarnings = Array.from({ length: 7 }, (_, i) => ({
    date: new Date(Date.now() - (6 - i) * 86400000).toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' }),
    amount: Math.floor(Math.random() * 500) + 100
  }))
  
  const tasksByType = [
    { type: 'Контент', count: 45 },
    { type: 'Аналитика', count: 32 },
    { type: 'Техническая', count: 18 },
    { type: 'Маркетинг', count: 28 },
    { type: 'Финансы', count: 22 }
  ]
  
  const agentPerformance = [
    { agent: 'ContentAgent', tasks: 45, earnings: 2250 },
    { agent: 'AnalyticsAgent', tasks: 32, earnings: 4800 },
    { agent: 'TechnicalAgent', tasks: 18, earnings: 5400 },
    { agent: 'MarketingAgent', tasks: 28, earnings: 8400 },
    { agent: 'FinanceAgent', tasks: 22, earnings: 6600 }
  ]
  
  return NextResponse.json({
    dailyEarnings,
    tasksByType,
    agentPerformance
  })
}