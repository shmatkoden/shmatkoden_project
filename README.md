# Shmatkoden Project

##Варіант
29%3=2
2. Користувацькі категорії витрат

## Опис
Це Flask-додаток, запущений у Docker-контейнері з використанням Docker Compose.

## Вимоги
- Docker
- Docker Compose

## Запуск проекту локально

1. **Клонування репозиторію:**
   ```bash
   git clone https://github.com/shmatkoden/shmatkoden_project.git
   
2.Перехід у директорію проекту:
 "cd shmatkoden_project"

3.Запуск контейнера за допомогою Docker Compose:
 "docker-compose build"

4. Запуск контейнера за допомогою Docker Compose:
  "docker-compose up"

## Міграція
1.flask db migrate -m "Initial migration."
2.flask db upgrade
3.flask run 