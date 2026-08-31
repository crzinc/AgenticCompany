#!/bin/bash

echo "🚀 Запуск AgenticCompany..."

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен."
    echo "📥 Скачайте Docker Desktop: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Проверка .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден. Создаю из .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 ОБЯЗАТЕЛЬНО отредактируйте .env файл!"
    echo ""
    echo "Нужно добавить хотя бы один бесплатный API ключ:"
    echo "1. Groq (быстро): https://console.groq.com"
    echo "2. HuggingFace: https://huggingface.co/settings/tokens"
    echo "3. Google Gemini: https://makersuite.google.com/app/apikey"
    echo ""
    echo "После добавления ключа запустите ./start.sh снова"
    exit 1
fi

# Проверка API ключей
source .env
if [ -z "$GROQ_API_KEY" ] && [ -z "$HUGGINGFACE_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ Не найден ни один API ключ в .env файле!"
    echo ""
    echo "Добавьте хотя бы один ключ:"
    echo "1. Groq (рекомендуется, быстро): https://console.groq.com"
    echo "2. HuggingFace: https://huggingface.co/settings/tokens"
    echo "3. Google Gemini: https://makersuite.google.com/app/apikey"
    exit 1
fi

echo "✅ API ключи найдены"

# Запуск services
echo "🐳 Запуск Docker контейнеров..."
docker-compose up -d

echo ""
echo "✅ AgenticCompany запущен!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo ""
echo "📋 Команды:"
echo "   docker-compose down    - остановка"
echo "   docker-compose logs -f - логи"