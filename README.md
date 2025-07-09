# Микросервис Clinic appointments

## Стек
### Основной стек
| Категория       | Технологии               | Версии      | Назначение                                                                 |
|----------------|--------------------------|------------|----------------------------------------------------------------------------|
| Фреймворк      | FastAPI                  | 0.115.14   | Асинхронный Бэкенд-сервис с автодокументацией OpenAPI                                 |
| Сервер         | Uvicorn (для дальнейшего проксирования NGINX)         | 0.35.0 | ASGI-сервер для FastAPI (высокая производительность)                      |
| ORM            | SQLAlchemy               | 2.0.41     | Работа с БД (PostgreSQL)                                                  |
| Миграции       | Alembic                  | 1.16.2     | Управление изменениями схемы БД                                           |
| Валидация      | Pydantic + Pydantic-Settings | 2.11.7, 2.10.1 | Валидация запросов/ответов и конфигурация через `.env`                   |

### Стек тестирования и качества кода
| Категория      | Технологии               | Версии    | Назначение                                                                |
|---------------|--------------------------|----------|---------------------------------------------------------------------------|
| Тесты         | pytest + pytest-asyncio  | 8.4.1, 1.0.0 | Юнит- и интеграционные тесты (асинхронная поддержка)                     |
| Покрытие кода | coverage + pytest-cov    | 7.9.2, 6.2.1 | Отслеживание покрытия тестами                                           |
| Линтеры       | flake8 + black + isort   | -        | Проверка стиля (PEP 8) и форматирование (Длина строки выбрана 79)                                  |

При провектировании микросервиса было решено использовать ORM SQLAlchemy для работы с Python объектами и легкой миграции на другие БД в случае такой необходимости. Также для миграций был выбран Alembic как инструмент для управления изменениями схемы базы данных.


## Структура проекта
### Архитектурная схема
![Архитектурная схема](https://i.ibb.co/67xfLZnW/image.png)
### Дерево папок проекта
```bash
├── .github/
│   └── workflows/
│       └── ci.yml # Настройка CI проекта
├── Dockerfile # Docker файл
├── Makefile # Команды make
├── app/
│   ├── API/
│   │   ├── Appointments/ # Логика модуля проекта: DAO, Роутер
│   │   ├── FastAPIService.py # Инициализация приложения FastAPI
│   ├── ClinicAppointments.py # Настройка приложений проекта
│   ├── Core/ # Для настройки проекта
│   ├── DataBase/
│   │   ├── Base.py # Объект Base SQLAlchemy
│   │   └── models/ # Модели базы данных
│   │   │   └── __init__.py # Файл для инициализации моделей для видимости Alembic
│   │   └── migrations/ # Миграции alembic
│   ├── Logger.py # Логирование проекта
├── docker-compose.yaml # Запуск стека Docker Compose
├── main.py # Точка входа в приложение
├── requirements.txt # Зависимости
└── tests/ # Папка с тестами
    ├── integration/ # Интеграционные тесты
    └── unit/ # Юнит тесты
```

### Проектирование базы данных
Это проект — микросервис, поэтому тут было решено создать 1 модель базы данных: Appointment без использования вспомогательных таблиц и вторичных ключей. Сделаем предположение, что id пациента и доктора будут приходить из других сервисов или в дальнейшем будут заменены на вторичные ключи других таблиц.
#### ER-Диаграмма
![ER-Диаграмма](https://i.ibb.co/ynxrKynR/ERD.png)

#### SQL запрос для создания таблицы
```sql
CREATE TABLE "Appointment"(
    "id" BIGINT NOT NULL,
    "doctor_id" BIGINT NOT NULL,
    "client_id" BIGINT NOT NULL,
    "start_time" TIMESTAMP(0) WITH TIME ZONE NOT NULL,
    "end_time" TIMESTAMP(0) WITH TIME ZONE NULL,
    "note" VARCHAR(255) NULL
);
ALTER TABLE
    "Appointment" ADD PRIMARY KEY("id");
ALTER TABLE
    "Appointment" ADD CONSTRAINT "appointment_doctor_id_unique" UNIQUE("doctor_id");
ALTER TABLE
    "Appointment" ADD CONSTRAINT "appointment_start_time_unique" UNIQUE("start_time");
```

### Activity-Диаграмма
![Activity-Диаграмма](https://i.ibb.co/BV0dLSx8/Activity.png)

# Запуск проекта

## Быстрый Запуск (prod)
```bash
git clone https://github.com/AlexeyGrushev/clinic_appointments.git

cp .env.example .env # Можно задать свои значения окружения

make up # Или: docker compose --env-file .env up -d --build
```

## Запуск Development Версии
```bash
# Use python 3.12
git clone https://github.com/AlexeyGrushev/clinic_appointments.git

cd clinic_appointments

cp .env.example .env # Задаем переменные окружения базы данных

python3 -m venv venv

source venv/bin/activate

make req-dev

python3 main.py
```

# Команды Make
В проекте доступны команды Makefile. Их запуск и значение:

## Управление сервисами

### `make up`
Запускает все Docker-сервисы в фоновом режиме с пересборкой контейнеров

### `make down`
Останавливает и удаляет все Docker-сервисы

## Проверка кода

### `make lint`
Проверяет код на соответствие стилю и форматированию

### `make format`
Автоматически форматирует код согласно стандартам

## Тестирование

### `make test`
Запускает тесты с выводом информации о покрытии кода

## Работа с базой данных

### `make makemigrations msg="описание"`
Создает новые миграции для базы данных (требует указания сообщения)

### `make migrate`
Применяет все ожидающие миграции базы данных

## Обслуживание

### `make healthcheck`
Проверяет работоспособность сервиса

### `make clean`
Удаляет временные файлы и кэш Python

## Управление зависимостями

### `make req`
Устанавливает основные зависимости проекта

### `make req-dev`
Устанавливает зависимости для разработки

### `make req-del`
Удаляет зависимости для разработки

---

*Проект является технической демонстрацией, не используется в реальном Production и распространяется по лицензии GNU GPL v3*