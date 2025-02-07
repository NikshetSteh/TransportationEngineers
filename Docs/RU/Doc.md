# Архитектура сервера

```mermaid
graph TD
linkStyle default interpolate linear

NGINX[NGINX]

LOADBALANCER[Load Balancer]

BaseServer[Base Server]
StoreServer[Store Server]
FaceServer[Face Server]
FrontendServer[Frontend Server]

BaseDB[Base Server Database]
StoreDB[Store Server Database]
Redis[Redis]

Accounting[Accounting or CRM]

VectorDB[Vector Database]

NGINX --> LOADBALANCER

LOADBALANCER --> FrontendServer
LOADBALANCER --> BaseServer
LOADBALANCER --> StoreServer
LOADBALANCER --> FaceServer

BaseServer --> BaseDB
StoreServer --> StoreDB
BaseServer --> Redis

StoreServer -.-> Accounting

FaceServer --> VectorDB

classDef dottedNode stroke-dasharray: 5 5;
class Accounting dottedNode
```

Главной технической частью проекта является сервер.
Он состоит из нескольких модулей которые представлены в диаграмме выше.

## Высокоуровневая архитектура

Backend состоит из 4 основных модулей:

- Основной сервис
- Сервис магазинов
- Сервис биометрии
- Frontend
  Так же есть несколько дополнительных модулей:
- DebugConsole (для отладки, временно заменяет админ панель)
- DebugData (набор тестовых данных)

Входным шлюзом служит Nginx и его встроенный балансировщик нагрузок.

Каждому модулю так же соответствует база данных (за исключением frontend).

## Запуск сервера

Сервер запускается посредством Docker Compose. В корне проекта находится файл конфигурации `compose.yml`.

```bash
docker-compose up -d --build
```

## Nginx

Конфигурации nginx находятся в корне проекта (файл `nginx.conf`).
Она автоматически монтируется в образ Docker.

Монтируются следующие пути:

- `/static` - статический контент
- `/keycloak` - доступ к keycloak
- `/base_api` - основной сервис
- `/store_api` - сервис магазинов

# Общее описание модулей

Все модули имеют определенный шаблон:

```
/module_name
├── app
├──── main.py
├──── config.py
├── pyproject.toml
├── poetry.toml
└── Dockerfile
```

- `app` (или `src`) - содержит исходный код модуля
- `pyproject.toml` - Зависимости
- `poetry.toml` - конфигурация poetry
- `Dockerfile` - конфигурация docker (при необходимости)
- `config.py` - конфигурация приложение (
  используется [pydantic-settings](https://pydantic-docs.helpmanual.io/usage/settings/))

Все модули (работающие на python) используют [poetry](https://python-poetry.org) для управления зависимостями.

Стандартная конфигурация poetry (`poetry.toml`)

```toml
[virtualenvs]
in-project = true # Создавать виртуальное окружение внутри проекта
```

## Серверные модули

- Основной фреймворк - [FastAPI](https://fastapi.tiangolo.com)
- Реляциональная база данных - [Postgres](https://www.postgresql.org/)
- Кэш - [Redis](https://redis.io/)
- Векторная база данных - [ChromaDB](https://github.com/duckdblabs/chroma)
- Миграция базы данных - [alembic](https://alembic.sqlalchemy.org/en/latest/)

Базовая структура:

```
app
├── alembic
├── models
├── some_submodule
├──── schemes
├──── router
├──── service
├──── depencies
├── main.py
├── alembic.ini
├── depencies
└── schemes
```

- `main.py` содержит root router. Все другие модули подключаются к нему из `some_submodule/router.py`.
- `service.py` содержит бизнес логику.
- `router` роутеры отдельных submodules.
- `depencies`, `schenes`, `exceptions`, ... - зависимости, схемы, исключения... Могу быть глобальные и привязанные к
  отельным
  submodules
- `alembic.ini` - конфигурация alembic
- `models` - модели базы данных
- `alembic` - система миграции баз данных. Стандартный `env.py` был переписан

# Base Server

Основной сервер. Отвечает почти за все взаимодействие с роботом, на время тестов эмулирует логику основного сервера ЖД
компании

## Submodules

- `admin` - отвечает за отладку, заменяет основной сервис ЖД компании. Отвечает за создание билетов, регистрацию
  инженеров
  и так далее. Исключительно на время разработки, использование на проде не предусмотренно
- `auth` - отвечает за авторизацию. Предоставляет Dependencies для авторизации пользователя
- `robot` - отвечает за работу с роботом. Реализует такие функции как проверка билетов, авторизация пользователей и т.
  д.
- `users` - отвечает за работу с пользователями. В основном предоставление информации для робота
- `face_api` - внешняя зависимость сервиса биометрии
- `store_api` - внешняя зависимость сервиса магазинов
- `redis_async` - небольшая обертка для работы с redis через асинхронный контекстный менеджер

## База данных

```mermaid
classDiagram
    direction LR
    class active_stores {
        varchar(500) public_key
        timestamp with time zone created_at
        uuid id
    }
    class alembic_version {
        varchar(32) version_num
    }
    class attractions {
        varchar(256) name
        varchar(1024) description
        varchar(256) logo_url
        varchar(256) destination_id
        timestamp with time zone created_at
        uuid id
    }
    class auth_cards {
        uuid engineer_id
        varchar(256) key
        timestamp with time zone created_at
        uuid id
    }
    class engineers {
        varchar(60) login
        varchar(60) password
        integer privileges
        timestamp with time zone created_at
        uuid id
    }
    class hotels {
        varchar(256) name
        varchar(1024) description
        varchar(256) logo_url
        varchar(256) destination_id
        timestamp with time zone created_at
        uuid id
    }
    class keycloak_users {
        uuid user_id
        uuid id
    }
    class robots {
        varchar(60) robot_model_id
        varchar(60) robot_model_name
        varchar(500) public_key
        timestamp with time zone created_at
        uuid id
    }
    class tickets {
        uuid user_id
        integer train_number
        integer wagon_number
        integer place_number
        timestamp with time zone date
        varchar(60) station_id
        varchar(60) destination_id
        timestamp with time zone start_date
        varchar(128) code
        boolean used
        uuid id
    }
    class train_stores {
        uuid store_id
        integer train_number
        timestamp with time zone train_date
        uuid id
    }
    class users {
        varchar(60) name
        timestamp with time zone created_at
        uuid id
    }

    auth_cards --> engineers: engineer_id&#58id
    keycloak_users --> users: user_id&#58id
    tickets --> users: user_id&#58id
```

## Endpoints

### 1. User Management

#### Add User

**Endpoint:** `POST /admin/user`

**Description:** Adds a new user.

**Request Body:**

```json
{
  "name": "string",
  "face": "string (optional)"
}
```

**Response:**

```json
{
  "id": "string",
  "name": "string"
}
```

**Errors:**

- `422 Validation Error`

#### Update User Face

**Endpoint:** `PATCH /admin/user/{user_id}/face`

**Description:** Updates the face data of a user.

**Parameters:**

- `user_id` (string, required): The ID of the user.

**Request Body:**

```json
{
  "face": "string"
}
```

**Response:**

```json
{
  "status": "OK"
}
```

**Errors:**

- `422 Validation Error`

#### Delete User Face

**Endpoint:** `DELETE /admin/user/face`

**Description:** Deletes a user's face data.

**Parameters:**

- `user_id` (query, required, string): The ID of the user.

**Response:**

```json
{
  "status": "OK"
}
```

**Errors:**

- `422 Validation Error`

#### Get Users

**Endpoint:** `GET /admin/users`

**Description:** Retrieves a paginated list of users.

**Parameters:**

- `page` (query, optional, integer, default: 1): Page number.
- `size` (query, optional, integer, default: 50, max: 100): Page size.

**Response:**

```json
{
  "items": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "total": 100,
  "page": 1,
  "size": 50
}
```

**Errors:**

- `422 Validation Error`

#### Delete User

**Endpoint:** `DELETE /admin/users/{user_id}`

**Description:** Deletes a specific user.

**Parameters:**

- `user_id` (path, required, string): The ID of the user.

**Response:**

```json
{
  "status": "OK"
}
```

**Errors:**

- `422 Validation Error`

### 2. Engineer Management

#### Create Engineer

**Endpoint:** `POST /admin/engineer`

**Description:** Creates a new engineer.

**Request Body:**

```json
{
  "login": "string",
  "password": "string"
}
```

**Response:**

```json
{
  "id": "string",
  "login": "string"
}
```

**Errors:**

- `422 Validation Error`

#### Delete Engineer

**Endpoint:** `DELETE /admin/engineers/{engineer_id}`

**Description:** Deletes an engineer.

**Parameters:**

- `engineer_id` (path, required, string): The ID of the engineer.

**Response:**

```json
{
  "status": "OK"
}
```

**Errors:**

- `422 Validation Error`

#### Get Engineers

**Endpoint:** `GET /admin/engineers`

**Description:** Retrieves a paginated list of engineers.

**Parameters:**

- `page` (query, optional, integer, default: 1): Page number.
- `size` (query, optional, integer, default: 50, max: 100): Page size.

**Response:**

```json
{
  "items": [
    {
      "id": "string",
      "login": "string"
    }
  ],
  "total": 100,
  "page": 1,
  "size": 50
}
```

**Errors:**

- `422 Validation Error`

#### Update Engineer Privileges

**Endpoint:** `PUT /admin/engineer_privileges`

**Description:** Updates the privileges of an engineer.

**Request Body:**

```json
{
  "id": "string",
  "privileges": [
    "ROBOT_LOGIN",
    "STORE_LOGIN"
  ]
}
```

**Response:**

```json
{
  "status": "OK"
}
```

**Errors:**

- `422 Validation Error`

### 3. Store Management

#### Add Store to Training

**Endpoint:** `POST /admin/store/{store_id}/train`

**Description:** Adds a store to training data.

**Parameters:**

- `store_id` (path, required, string): The ID of the store.

**Request Body:**

```json
{
  "train_number": 123,
  "train_date": "2025-02-01T00:00:00Z"
}
```

**Response:**

```json
{
  "status": "OK"
}
```

**Errors:**

- `422 Validation Error`

#### Remove Store from Training

**Endpoint:** `DELETE /admin/store/{store_id}/train/unbind`

**Description:** Removes a store from training data.

**Parameters:**

- `store_id` (path, required, string): The ID of the store.

**Request Body:**

```json
{
  "train_number": 123,
  "train_date": "2025-02-01T00:00:00Z"
}
```

**Response:**

```json
{
  "status": "OK"
}
```

**Errors:**

- `422 Validation Error`

### 4. Ticket Management

#### Create Ticket

**Endpoint:** `POST /admin/ticket`

**Description:** Creates a new ticket.

**Request Body:**

```json
{
  "user_id": "string",
  "train_number": 123,
  "wagon_number": 5,
  "place_number": 12,
  "station_id": "string",
  "destination": "string",
  "date": "2025-02-01T00:00:00Z",
  "start_date": "2025-02-01T00:00:00Z"
}
```

**Response:**

```json
{
  "id": "string",
  "train_number": 123,
  "wagon_number": 5,
  "place_number": 12,
  "destination": "string"
}
```

**Errors:**

- `422 Validation Error`

#### Delete Ticket

**Endpoint:** `DELETE /admin/ticket/{ticket_id}`

**Description:** Deletes a ticket.

**Parameters:**

- `ticket_id` (path, required, string): The ID of the ticket.

**Response:**

```json
{
  "status": "OK"
}
```

**Errors:**

- `422 Validation Error`

This document covers the main API endpoints. Let me know if you need additional formatting or more endpoints!

# Store Server

Отвечает за работу магазинов

## Submodules

- `admin` - отвечает за отладку, заменяет основной сервис ЖД компании. Отвечает за создание билетов, регистрацию
  инженеров
  и так далее. Исключительно на время разработки, использование на проде не предусмотренно
- `redis_async` - небольшая обертка для работы с redis через асинхронный контекстный менеджер
- `robot` - взаимодействие с роботом
- `store` - взаимодействие с магазинами

## База данных

```mermaid
---
config:
    flowchart:
        defaultRenderer: elk
---
classDiagram
    direction BT
    class alembic_version {
        varchar(32) version_num
    }
    class purchase_items {
        uuid purchase_id
        uuid store_item_id
        integer count
        uuid id
    }
    class purchases {
        uuid store_id
        uuid user_id
        timestamp with time zone created_at
        uuid id
    }
    class store_items {
        uuid store_id
        varchar(100) name
        varchar(255) description
        varchar(255) logo_url
        integer balance
        integer price_penny
        varchar(100) category
        timestamp with time zone created_at
        uuid id
    }
    class stores {
        varchar(100) name
        varchar(255) description
        varchar(255) logo_url
        store_type_enum store_type
        timestamp with time zone created_at
        uuid id
    }
    class tasks {
        uuid store_id
        uuid user_id
        uuid purchase_id
        boolean is_ready
        json additional_data
        timestamp with time zone created_at
        uuid id
    }

    purchase_items --> purchases: purchase_id&#58id
    purchase_items --> store_items: store_item_id&#58id
    purchases --> stores: store_id&#58id
    store_items --> stores: store_id&#58id
    tasks --> purchases: purchase_id&#58id
    tasks --> stores: store_id&#58id
```

## Endpoints

### 1. Store Management

#### Create Store

**Endpoint:** `POST /admin/store`

**Description:** Creates a new store.

**Request Body:**

```json
{
  "name": "string",
  "description": "string",
  "logo_url": "string",
  "store_type": "SHOP | RESTAURANT"
}
```

**Response:**

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "logo_url": "string",
  "store_type": "SHOP | RESTAURANT"
}
```

**Errors:**

- `422 Validation Error`

#### Get Stores

**Endpoint:** `GET /admin/stores`

**Description:** Retrieves a list of stores.

**Query Parameters:**

- `page` (integer, default: 1) - Page number
- `size` (integer, default: 50, max: 100) - Number of results per page

**Response:**

```json
{
  "items": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "logo_url": "string",
      "store_type": "SHOP | RESTAURANT"
    }
  ],
  "total": 100,
  "page": 1,
  "size": 50
}
```

**Errors:**

- `422 Validation Error`

#### Get Store

**Endpoint:** `GET /admin/store/{store_id}`

**Description:** Retrieves details of a specific store.

**Path Parameters:**

- `store_id` (string) - Unique identifier of the store

**Response:**

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "logo_url": "string",
  "store_type": "SHOP | RESTAURANT"
}
```

**Errors:**

- `422 Validation Error`

#### Delete Store

**Endpoint:** `DELETE /admin/store/{store_id}`

**Description:** Deletes a store.

**Path Parameters:**

- `store_id` (string) - Unique identifier of the store

**Response:**

```json
{
  "status": "OK"
}
```

**Errors:**

- `422 Validation Error`

### 2. Store Items Management

#### Get Items

**Endpoint:** `GET /store/items`

**Description:** Retrieves a list of store items.

**Query Parameters:**

- `page` (integer, default: 1) - Page number
- `size` (integer, default: 50, max: 100) - Number of results per page

**Response:**

```json
{
  "items": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "price_penny": 1000
    }
  ],
  "total": 100,
  "page": 1,
  "size": 50
}
```

**Errors:**

- `422 Validation Error`

#### Get Item

**Endpoint:** `GET /store/item/{item_id}`

**Description:** Retrieves details of a specific item.

**Path Parameters:**

- `item_id` (string) - Unique identifier of the item

**Response:**

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price_penny": 1000
}
```

**Errors:**

- `422 Validation Error`

#### Add Item

**Endpoint:** `POST /store/item`

**Description:** Adds a new item to the store.

**Request Body:**

```json
{
  "name": "string",
  "description": "string",
  "price_penny": 1000
}
```

**Response:**

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price_penny": 1000
}
```

**Errors:**

- `422 Validation Error`

### Update Item

**Endpoint:** `PUT /store/item`

**Description:** Updates an existing item.

**Request Body:**

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price_penny": 1000
}
```

**Response:**

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price_penny": 1000
}
```

**Errors:**

- `422 Validation Error`

#### Remove Item

**Endpoint:** `DELETE /store/item/{item_id}`

**Description:** Removes an item from the store.

**Path Parameters:**

- `item_id` (string) - Unique identifier of the item

**Response:**

```json
{
  "status": "OK"
}
```

**Errors:**

- `422 Validation Error`

### 3. Purchase Management

#### Make Purchase

**Endpoint:** `POST /store/purchase`

**Description:** Creates a new purchase.

**Request Body:**

```json
{
  "user_id": "string",
  "items": [
    {
      "item_id": "string",
      "count": 1
    }
  ],
  "is_default_ready": true
}
```

**Response:**

```json
{
  "id": "string",
  "store_id": "string",
  "user_id": "string",
  "items": [
    {
      "item_id": "string",
      "count": 1
    }
  ],
  "date": "2024-01-01T12:00:00Z"
}
```

**Errors:**

- `422 Validation Error`

# Robot

Данный модуль агрегирует в себе все компоненты для физических устройств экосистемы.
В нем есть реализация всех методов API серверов необходимых для функционирования компонентов системы.
В основе разработки, как и в остальных модулях лежит асинхронный подход.
Для пользовательского интерфейса был выбран PySide6.
Так как он основывается на синхронном PyQT, был использован дополнительный пакет `qasync`:

```python
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop
import sys
import asyncio


async def main(app_loop):
    while True:
        pass


# Запуск PySide приложение параллельно с асинхронным кастомным event-loop
application = QApplication(sys.argv)
loop = QEventLoop(application)
asyncio.set_event_loop(loop)
loop.run_until_complete(main(loop))
```

## Submodule

- `auth`. Реализует API авторизации, а так же содержит методы для работы с ключами авторизации
- `deviatn`. Реализует распознавания девиантного поведения
- `fsm`. Реализация finite-state-machine
- `hardware`. Модуль для работы с низкоуровневыми устройствами
- `info_service`. Модуль для работы с информационными сервисами (получениие данных о местоположении)
- `states`. Состояния для fsm
- `store`. Модуль для работы с магазинами
- `tickets`. Модуль для работы с билетами
- `ui`. Реализация пользовательского интерфейса
- `users`. Модуль для работы с пользователями
- `video`. Небольшая обертка для асинхронного использования камеры

## Особенности

Ввиду отсутствия интерфейса конфигурации, настройка осуществляется через консоль.
Так как она может быть динамической, то она доступна во время всей работы приложения.
Из-за синхронности стандартного `input`, он запускается в асинхронном режиме:

```python
import asyncio


async def async_input(
        title: str = "> "
):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, title)
```

Был обнаружен баг на стороне python, из-за которого при использовании данного подхода блокируется создание новых
потоков,
а разблокировка возможна только при завершении выполнения текущего `await input()`.

Для временного исправления данного бага была введена функция `Stop config`, которая прекращает работу с консолью.
Много поточность использует система распознавания девиантного поведения, так что перед её запуском следует
воспользоваться данной функцией

## Распознавание девиантного поведения

На текущий момент алгоритм выглядит следующим образом:

```mermaid
sequenceDiagram
NOTE over Robot: Запуск системы в фоновом режиме
NOTE over Robot: Обнаружение девиантного поведения
Robot ->> Server: Сигнал о девиантном поведении
```

Алгоритм работы модели:

```mermaid
flowchart
    loadModel[Загрузка модели]
    getCam[Получение N кадров с камеры]
    createThread[Создание потока]
    runModel[Работа модели]
    sendResult[Отправка результата]
    loadModel --> getCam
    getCam --> createThread
    createThread --> runModel
    runModel --> sendResult
    sendResult --> getCam
```

Планируется расширение функционала до:

1. Обнаружение девиантного поведения

```mermaid
sequenceDiagram
    Terminal ->> Server: Конфигурация мониторинга
NOTE over Robot: Настройка информации о камере (местоположение, название)
NOTE over Robot: Запуск системы в фоновом режиме
NOTE over Robot: Обнаружение девиантного поведения
loop
Robot ->> Server: Сигнал о девиантном поведении
Server ->> Terminal: Сигнал о девиантном поведении
Server ->> Terminal: Информация об участниках
end
```

2. Обнаружение нежелательных лиц

```mermaid
sequenceDiagram
NOTE over Robot: Настройка информации о камере (местоположение, название)
NOTE over Robot: Запуск системы в фоновом режиме
NOTE over Robot: Обнаружение девиантного поведения
loop
NOTE over Robot: Обнаружение нового лица
Robot ->> Server: Запрос на распознавание
NOTE over Server: Проверка биометрии по базе
Server ->> Terminal: Информация об угрозе
end
```

Алгоритм работы модели:

```mermaid
sequenceDiagram
NOTE over ModelThread: Загрузка модели
MainThread ->> ModelThread: единичный батч данных
NOTE over ModelThread: Работа модели
ModelThread ->> MainThread: Результат
NOTE over MainThread: Отправка отчета 
```

Как основная модель был выбран [Data-efficient-video-transformer](https://github.com/NikshetSteh/Data-efficient-video-transformer)
- Модель основана на архитектуре [ViT](https://arxiv.org/abs/2010.11929), поэтому может работать с изображениями произвольного размера.
- Shape входного батча: `[BATCH_SIZE, FRAME_COUNT, CHANNEL, HEIGHT, WIDTH]`
- Выход модели: `[BATCH_SIZE, 1]`

Проект был разработан более 4 лет назад, так что была проведена работа над переводом его на новые версии библиотек, а
так же восстановлены веса pre-trained модели (были удалены авторам, из-за чего сейчас оригинальный пакет не работает).
Обновленная версия представлена на [GitHub](https://github.com/NikshetSteh/Data-efficient-video-transformer)


# Алгоритмы работы системы 
## Авторизация компонентов системы 
Авторизация компонентов системы построена на основе RSA ключей 
(планируется переход на более быстрые эллиптические кривые).

Первая аутентификация компонентов системы происходит на основе данных
инженера с соответствующими правами

```mermaid
sequenceDiagram
    NOTE over Robot: генерация RSA ключей
    Robot ->> Server: public_key, engineer credentials, robot data
    NOTE over Server: Проверка прав доступа
    Server ->> DB: Сохранения публичного ключа 
    Server ->> Robot: Robot id
```

Повторная аутентификация происходит на основе RSA ключей:

```mermaid
sequenceDiagram
    Robot ->> Server: Запрос на авторизацию
    Server ->> Robot: Зашифрованный публичным ключом код
    Robot ->> Server: Расшифрованный код
    NOTE over Server: Валидация кода
    NOTE over Server: Генерация случайного токена
    Server ->> Redis: Сохранения данных новой сессии 
    Server ->> Robot: Токе доступа 
```


Для доступа к требующим авторизациям endpoint\`s используется схема `Bearer` (заголовок `Authorization: Bearer <token>`)
