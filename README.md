# AgenticCompany

Автономная компания ИИ-агентов, которая зарабатывает деньги без вложений.

## Всё бесплатно

- **LLM**: Groq / HuggingFace / Google Gemini (бесплатные API)
- **БД**: Supabase (500MB бесплатно)
- **Frontend**: Next.js (бесплатно)
- **Backend**: FastAPI (бесплатно)

## Быстрый старт

### 1. Установите Docker Desktop

Скачайте: https://www.docker.com/products/docker-desktop/

### 2. Получите бесплатный API ключ

Выберите **один** из вариантов (рекомендую Groq - самый быстрый):

| Сервис | Скорость | Лимит | Ссылка |
|--------|----------|-------|--------|
| **Groq** | Быстро | 30 запросов/мин | https://console.groq.com |
| HuggingFace | Медленно | Ограничено | https://huggingface.co/settings/tokens |
| Google Gemini | Средне | 60 запросов/мин | https://makersuite.google.com/app/apikey |

### 3. Настройте проект

```bash
cd AgenticCompany
cp .env.example .env
```

Отредактируйте `.env` и добавьте ключ:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
```

### 4. Запустите

```bash
./start.sh
```

### 5. Откройте

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000

## Типы агентов

| Агент | Что делает | Заработок |
|-------|------------|-----------|
| ContentAgent | Блоги, посты, статьи | $50-100 |
| AnalyticsAgent | Анализ рынков, отчёты | $150-250 |
| TechnicalAgent | Скрипты, автоматизация | $250-400 |
| MarketingAgent | Реклама, SEO | $350-600 |
| FinanceAgent | Финансы, прогнозы | $300-500 |

## Управление

```bash
# Запуск
./start.sh

# Остановка
docker-compose down

# Логи
docker-compose logs -f

# Перезапуск
docker-compose restart
```

## Структура

```
AgenticCompany/
├── frontend/          # Next.js интерфейс
├── backend/           # FastAPI сервер
├── src/               # ИИ-агенты
├── supabase/          # SQL миграции
├── docker-compose.yml
├── start.sh           # Запуск
└── .env.example       # Настройки
```

## Подключение Supabase (опционально)

1. Регистрация: https://supabase.com
2. Создайте проект
3. Скопируйте URL и Key в `.env`
4. Выполните SQL из `supabase/migrations/001_initial.sql`