'use client'

import { useState, useEffect } from 'react'
import { Activity, DollarSign, CheckCircle, Clock } from 'lucide-react'

interface Stats {
  totalAgents: number
  activeAgents: number
  completedTasks: number
  totalEarnings: number
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats>({
    totalAgents: 0,
    activeAgents: 0,
    completedTasks: 0,
    totalEarnings: 0
  })
  const [recentTasks, setRecentTasks] = useState<any[]>([])

  useEffect(() => {
    fetchStats()
    fetchRecentTasks()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/stats')
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const fetchRecentTasks = async () => {
    try {
      const response = await fetch('/api/tasks/recent')
      if (response.ok) {
        const data = await response.json()
        setRecentTasks(data)
      }
    } catch (error) {
      console.error('Error fetching recent tasks:', error)
    }
  }

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Всего агентов</p>
              <p className="text-3xl font-bold">{stats.totalAgents}</p>
            </div>
            <Activity className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Активных</p>
              <p className="text-3xl font-bold text-green-600">{stats.activeAgents}</p>
            </div>
            <CheckCircle className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Выполнено задач</p>
              <p className="text-3xl font-bold">{stats.completedTasks}</p>
            </div>
            <Clock className="w-8 h-8 text-orange-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Заработано</p>
              <p className="text-3xl font-bold text-green-600">${stats.totalEarnings}</p>
            </div>
            <DollarSign className="w-8 h-8 text-green-500" />
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border">
        <h2 className="text-xl font-semibold mb-4">Последние задачи</h2>
        {recentTasks.length === 0 ? (
          <p className="text-gray-500">Нет выполненных задач</p>
        ) : (
          <div className="space-y-4">
            {recentTasks.map((task, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium">{task.description}</p>
                  <p className="text-sm text-gray-500">{task.agent}</p>
                </div>
                <div className="text-right">
                  <span className={`px-2 py-1 rounded text-xs ${
                    task.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {task.status === 'completed' ? 'Выполнено' : 'В работе'}
                  </span>
                  {task.earnings && (
                    <p className="text-green-600 font-medium mt-1">+${task.earnings}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}