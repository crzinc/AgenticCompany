'use client'

import { useState, useEffect } from 'react'
import { Bot, Play, Pause, Settings } from 'lucide-react'

interface Agent {
  id: string
  name: string
  type: string
  status: 'active' | 'idle' | 'error'
  tasksCompleted: number
  earnings: number
  capabilities: string[]
}

export default function AgentList() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAgents()
  }, [])

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents')
      if (response.ok) {
        const data = await response.json()
        setAgents(data)
      }
    } catch (error) {
      console.error('Error fetching agents:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleAgent = async (agentId: string, currentStatus: string) => {
    const newStatus = currentStatus === 'active' ? 'pause' : 'start'
    try {
      await fetch(`/api/agents/${agentId}/${newStatus}`, { method: 'POST' })
      fetchAgents()
    } catch (error) {
      console.error('Error toggling agent:', error)
    }
  }

  const getAgentIcon = (type: string) => {
    const icons: Record<string, string> = {
      content: '✍️',
      analytics: '📊',
      technical: '⚙️',
      marketing: '📢',
      finance: '💰'
    }
    return icons[type] || '🤖'
  }

  if (loading) {
    return <div className="text-center py-8">Загрузка...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">ИИ-агенты</h2>
        <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
          Добавить агента
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <div key={agent.id} className="bg-white p-6 rounded-xl shadow-sm border">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{getAgentIcon(agent.type)}</span>
                <div>
                  <h3 className="font-semibold">{agent.name}</h3>
                  <p className="text-sm text-gray-500 capitalize">{agent.type}</p>
                </div>
              </div>
              <span className={`px-2 py-1 rounded-full text-xs ${
                agent.status === 'active' ? 'bg-green-100 text-green-800' :
                agent.status === 'idle' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {agent.status === 'active' ? 'Активен' :
                 agent.status === 'idle' ? 'Ожидание' : 'Ошибка'}
              </span>
            </div>

            <div className="space-y-3 mb-4">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Выполнено задач:</span>
                <span className="font-medium">{agent.tasksCompleted}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Заработано:</span>
                <span className="font-medium text-green-600">${agent.earnings}</span>
              </div>
            </div>

            <div className="mb-4">
              <p className="text-xs text-gray-500 mb-2">Возможности:</p>
              <div className="flex flex-wrap gap-1">
                {agent.capabilities.map((cap, index) => (
                  <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                    {cap}
                  </span>
                ))}
              </div>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => toggleAgent(agent.id, agent.status)}
                className={`flex-1 flex items-center justify-center gap-2 py-2 rounded-lg ${
                  agent.status === 'active'
                    ? 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'
                    : 'bg-green-100 text-green-700 hover:bg-green-200'
                }`}
              >
                {agent.status === 'active' ? (
                  <>
                    <Pause className="w-4 h-4" />
                    Пауза
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" />
                    Запустить
                  </>
                )}
              </button>
              <button className="p-2 bg-gray-100 rounded-lg hover:bg-gray-200">
                <Settings className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}