# Техническая часть

## Архитектура

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

Система представляет из себя модульную конструкцию базирующуюся на
нескольких сервисах:

- Base Server. 
  Совмещает в себе эмуляцию сервисов самой ЖД компании,
  а также взаимодействие с аппаратными комплексом
- Store Server.
  Предоставляет API для работы различных магазинов и
  ресторанов интегрированных в систему
- Face Server.
  Отвечает за работу с биометрией
- Frontend Server.
  Предоставляет сайт для взаимодействия с
  пользователями

Планируется добавление систем сбора данных о состоянии системы и логов

### Базы данных

Для основных задач была выбрана СУБД PostgresSQL, для хранения биометрии ChromaDB и для
хранения сессий Redis

#### ChromaDB

Одна коллекция, один тип записей в формате: вектор + метаданные (user_id)

#### Redis

Две коллекции:

- Сессии в формате: session_token: user_id, session_id
- Запросы на авторизацию: user_id: request_id

#### Базовый сервер

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

#### Сервис магазинов

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

### Компонент системы

При разработке базы для всех компонентов системы был использован асинхронный-функциональный подход.
Графическим фреймворком послужил `PySide`. Так как PySide построен на основе синхронной архитектуры,
для асинхронной обработки использовались дополнительные пакеты, такие как `qasync`, а так же
встраивание кастомного event-loop в основную логику приложения:

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

### Особенности системы

Система не обладает какими-то особыми алгоритмами и структурами данных,
в основном только массивы и словари.
Временная сложность у всех endpoints можно считать константой или линейной
от количества пользователей в системе.

## Алгоритмы

### Авторизация и Аутентификация компонентов системы

Первая аутентификация компонентов системы происходит на основе данных
инженера с соответствующими правами

```mermaid
sequenceDiagram
NOTE over Robot: генерация RSA ключей
Robot ->> Server: public_key, engineer credentials, robot data
Server ->> Robot: Robot id
```

Повторная аутентификация происходит на основе RSA ключей:

```mermaid
sequenceDiagram
    Robot ->> Server: Запрос на авторизацию
    Server ->> Robot: Зашифрованный публичным ключом код
    Robot ->> Server: Расшифрованный код
    Server ->> Robot: Токены доступа 
```

Для авторизации соответственно используются токены доступа полученные при аунтентификации
через заголовок `Authorization: Bearer <token>`

### Рекомендательный алгоритм

Для систем рекомендации временно используется упрощенный алгоритм. В момента запроса
формируется несколько списков популярных товаров:

- Личные предпочтения пользователя
- Товары популярные в магазине

А так же список последних покупок товаров. На их основе определяется рекомендованный список
товаров

### Проверка доступа к админ-панели робота

```mermaid
sequenceDiagram
    Engineer ->> Robot: NFC карта доступа
    Robot ->> Server: Проверка прав доступа
    Server ->> Robot: Результат
```

### Система интеллектуального видеонаблюдения

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

### Проверка билетов

```mermaid
flowchart
    getCam[Получение данных с камеры]
    qrCheck{Проверка наличие QR-кода в кадре}
    timeoutCheck[Проверка таймаута]
    faceCheck[Проверка биометрии]
    codeCheck[Проверка кода]
    results["Отображение результата"]
    getCam --> qrCheck
    qrCheck -- Да --> codeCheck
    qrCheck -- Нет --> timeoutCheck
    timeoutCheck -- Да --> faceCheck
    timeoutCheck -- Нет --> getCam
    faceCheck --> results
    codeCheck --> results
```

### Отладка 
Для отладки системы был создан отдельный модуль DebugConsole, который 
заменял админ панель и реальную интеграцию с системами ЖД

## Используемые технологии

- Основной язык программирования - Python 3.12
- Контроль версий - [Git](https://git-scm.com/)
- Конфигурации системы - pydantic-settings
- Миграции базы данных - alembic
- Работа с базой данных - sqlalchemy
- Драйвер подключения к базе данных - asyncpg
- Построение API - fastapi + pydantic
- Работа с Redis - redis
- Интерфейс - PySide + qasync
- Бекенд для моделей - pytorch
- Распознавание лиц - insightface
- Работа с камерой и QR кодами - OpenCV
- Драйвер базы данных для alembic - psycopg2  
- Асинхронное взаимодействие с низкоуровневым железом - pyserial-asyncio
- Менеджер пакетов - [poetry](https://python-poetry.org/)
- Контейнеризация и оркестрация - Docker и Docker Compose

Список всех используемых сторонних библиотек с ссылками на них:
- [PySide](https://pypi.org/project/PySide6/)
- [FastAPI](https://pypi.org/project/fastapi/)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [pydantic-settings](https://pypi.org/project/pydantic-settings/)
- [fastapi-pagination](https://pypi.org/project/fastapi-pagination/)
- [insightface](https://pypi.org/project/insightface/)
- [chromadb](https://pypi.org/project/chromadb/)
- [asyncpg](https://pypi.org/project/asyncpg/)
- [asyncpg](https://pypi.org/project/asyncpg/)
- [redis](https://pypi.org/project/redis/)
- [cryptography](https://pypi.org/project/cryptography/)
- [aiohttp](https://pypi.org/project/aiohttp/)
- [alembic](https://pypi.org/project/alembic/)
- [uvicorn](https://pypi.org/project/uvicorn/)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- [isort](https://pypi.org/project/isort/)
- [qasync](https://pypi.org/project/qasync/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- menovideo [оригинал](https://pypi.org/project/menovideo) и 
[исправленная нами версия](https://github.com/NikshetSteh/Data-efficient-video-transformer.git)
- [timm](https://pypi.org/project/timm/)
- [scikit-image](https://pypi.org/project/scikit-image/)
- [numpy](https://pypi.org/project/numpy/)
- [pyserial-asyncio](https://pypi.org/project/pyserial-asyncio/)
- [shiboken6](https://pypi.org/project/shiboken6/)
- [jinja2](https://pypi.org/project/jinja2/)
- [insightface](https://pypi.org/project/insightface/)
- [chromadb](https://pypi.org/project/chromadb/)
- [requests](https://pypi.org/project/requests/)


### Нейронные сети
#### [Data-efficient-video-transformer](https://github.com/NikshetSteh/Data-efficient-video-transformer)
Модель основана на архитектуре [ViT](https://arxiv.org/abs/2010.11929)
поэтому может работать с изображениями произвольного размера.
Shape входного батча: `[BATCH_SIZE, FRAME_COUNT, CHANNEL, HEIGHT, WIDTH]`
Выход модели: `[BATCH_SIZE, 1]`


#### [InsightFace](https://github.com/deepinsight/insightface)
На вход модели поступает изображение произвольного размера, далее 
во внутреннем алгоритме оно приводится к размеру `640*640*3`.
На выходе модели есть несколько параметров, включающих BBOXs для каждого
обнаруженного лица, а так же эмбеддинги (размерность `512`) для них.



## Исходный код
Весь код, модели, схемы и исходники самой этой технической документации
(в формате markdown и схемы в формате mermaid)
представлены на [github](https://github.com/NikshetSteh/TransportationEngineers/)  
https://github.com/NikshetSteh/TransportationEngineers/