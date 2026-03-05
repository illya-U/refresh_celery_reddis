# Используем официальный Python 3.11 slim образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Отключаем создание pyc файлов и включаем буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем только requirements.txt сначала (для кэширования слоёв)
RUN ls -la

COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь код проекта
COPY . .

# Экспонируем порт для Django
EXPOSE 8000
