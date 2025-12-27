Проект представляет собой локальную среду для практики SQL и аналитики данных. Он разворачивает базу данных PostgreSQL, скрипт-генератор синтетических данных и инструмент визуализации Redash.

## Описание компонентов

* **postgres (ecommerce_db):** Основная база данных магазина. Содержит таблицу `orders`.
* **generator:** Python-скрипт, который непрерывно генерирует случайные заказы и записывает их в базу данных в реальном времени. Использует распределения (нормальное и Пуассона) для создания реалистичных данных.
* **redash:** Полный стек сервисов Redash (server, scheduler, worker, redis, internal db) для построения дашбордов и выполнения SQL-запросов.

## Предварительные требования

* Docker
* Docker Compose

## Установка и запуск

### 1. Настройка переменных окружения :((

Так как файл конфигурации находится в `.gitignore`, необходимо создать его вручную.
Создайте файл `.env` в корневой директории проекта и вставьте в него следующее содержимое:

POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=ecommerce_db

PYTHONUNBUFFERED=0
REDASH_LOG_LEVEL=INFO
REDASH_REDIS_URL=redis://redis:6379/0

REDASH_INTERNAL_PASSWORD=secret_redash_pass
REDASH_INTERNAL_DB=redash

REDASH_DATABASE_URL=postgresql://postgres:secret_redash_pass@redash-postgres/redash
REDASH_COOKIE_SECRET=very-secret-key

### 2. Первый запуск:33

При самом первом запуске необходимо создать структуру внутренней базы данных Redash. Выполните команды по очереди:

1. Запустите контейнеры баз данных:
   docker-compose up -d postgres redash-postgres redis

2. Выполните инициализацию базы данных Redash:
   docker-compose run --rm server create_db

3. Запустите остальные сервисы (генератор, сервер Redash, воркеры):
   docker-compose up -d

### 3. Доступ к интерфейсу

После запуска Redash будет доступен по адресу:
http://localhost:5000

При первом входе вам будет предложено создать учетную запись администратора.

## Подключение источника данных в Redash

Чтобы начать работать с данными заказов, выполните следующие шаги в интерфейсе Redash:

1. Перейдите в **Settings** (значок шестеренки) -> **Data Sources**.
2. Нажмите **+ New Data Source** и выберите **PostgreSQL**.
3. Заполните поля подключения, используя данные из `docker-compose.yml`:
   * **Name:** E-commerce Store (или любое другое)
   * **Host:** postgres
   * **Port:** 5432
   * **User:** user
   * **Password:** password
   * **Database Name:** ecommerce_db
4. Нажмите **Test Connection** и **Save**.

## Работа с генератором данных

Контейнер `generator` начинает работу автоматически. Он добавляет примерно 1 заказ в секунду.
Чтобы проверить работу генератора, можно посмотреть логи контейнера:

docker logs -f data_generator

## Остановка проекта

Чтобы остановить все контейнеры:

docker-compose down

Данные сохраняются в Docker volumes (`ecommerce_pg_data` и `redash_pg_data`), поэтому при перезапуске история заказов и настройки дашбордов не пропадут.