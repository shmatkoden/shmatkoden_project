# Використовуємо офіційний образ Python 3.8-slim-bullseye
FROM python:3.8-slim-bullseye

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл з залежностями
COPY requirements.txt .

# Встановлюємо залежності
RUN python -m pip install -r requirements.txt

# Копіюємо всі файли проєкту до контейнера
COPY . /app

# Команда для запуску Flask-застосунку
CMD ["flask", "--app", "app", "run", "-h", "0.0.0.0", "-p", "5000"]