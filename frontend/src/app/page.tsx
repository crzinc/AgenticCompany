'use client'

import { useState, useEffect } from 'react'
import Dashboard from '@/components/Dashboard'
import AgentList from '@/components/AgentList'
import TaskManager from '@/components/TaskManager'
import Stats from '@/components/Stats'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'agents' | 'tasks' | 'stats'>('dashboard')
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    checkConnection()
  }, [])

  const checkConnection = async () => {
    try {
      const response = await fetch('/api/health')
      setIsConnected(response.ok)
    } catch {
      setIsConnected(false)
    }
  }

  return (
    <main className="min-h-screen p-8">
      <header className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold">AgenticCompany</h1>
            <p className="text-gray-600 mt-2">Автономная компания ИИ-агентов</p>
          </div>
          <div className="flex items-center gap-4">
            <div className={`px-3 py-1 rounded-full text-sm ${isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
              {isConnected ? 'Подключено' : 'Не подключено'}
            </div>
          </div>
        </div>
      </header>

      <nav className="flex gap-4 mb-8 border-b pb-4">
        {(['dashboard', 'agents', 'tasks', 'stats'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-lg transition-colors ${
              activeTab === tab
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 hover:bg-gray-200'
            }`}
          >
            {tab === 'dashboard' && 'Главная'}
            {tab === 'agents' && 'Агенты'}
            {tab === 'tasks' && 'Задачи'}
            {tab === 'stats' && 'Статистика'}
          </button>
        ))}
      </nav>

      <section>
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'agents' && <AgentList />}
        {activeTab === 'tasks' && <TaskManager />}
        {activeTab === 'stats' && <Stats />}
      </section>
    </main>
  )
}