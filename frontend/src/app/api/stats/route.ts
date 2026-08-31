import { NextResponse } from 'next/server'

export async function GET() {
  const stats = {
    totalAgents: 5,
    activeAgents: 4,
    completedTasks: 145,
    totalEarnings: 27450
  }
  
  return NextResponse.json(stats)
}