-- Создание таблицы агентов
CREATE TABLE IF NOT EXISTS agents (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  status TEXT DEFAULT 'idle' CHECK (status IN ('active', 'idle', 'error')),
  tasks_completed INTEGER DEFAULT 0,
  earnings DECIMAL(10, 2) DEFAULT 0,
  capabilities JSONB DEFAULT '[]',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Создание таблицы задач
CREATE TABLE IF NOT EXISTS tasks (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  description TEXT NOT NULL,
  type TEXT NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
  agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
  earnings DECIMAL(10, 2) DEFAULT 0,
  result JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  completed_at TIMESTAMP WITH TIME ZONE
);

-- Создание таблицы транзакций
CREATE TABLE IF NOT EXISTS transactions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
  amount DECIMAL(10, 2) NOT NULL,
  description TEXT,
  task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Создание индексов
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_agent_id ON tasks(agent_id);
CREATE INDEX idx_transactions_type ON transactions(type);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);

-- Функция для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Триггер для обновления updated_at
CREATE TRIGGER update_agents_updated_at
  BEFORE UPDATE ON agents
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Вставка тестовых данных
INSERT INTO agents (name, type, status, tasks_completed, earnings, capabilities) VALUES
  ('ContentAgent', 'content', 'active', 45, 2250, '["writing", "blog_posts", "social_media", "copywriting"]'),
  ('AnalyticsAgent', 'analytics', 'active', 32, 4800, '["data_analysis", "market_research", "reporting", "forecasting"]'),
  ('TechnicalAgent', 'technical', 'idle', 18, 5400, '["development", "automation", "scripting", "api_integration"]'),
  ('MarketingAgent', 'marketing', 'active', 28, 8400, '["social_media", "advertising", "seo", "content_marketing"]'),
  ('FinanceAgent', 'finance', 'active', 22, 6600, '["budgeting", "investment_analysis", "financial_planning", "accounting"]');