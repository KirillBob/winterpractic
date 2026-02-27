# WinterPractik — Менеджер файлов 

REST API для управления метаданными файлов и хранением файлов на сервере. 
Все ответы возвращаются в формате JSON. Работает с PostgreSQL и использует SQLAlchemy ORM.

## Быстрый старт с Docker

### Запуск через Docker Compose

```bash
docker-compose up -d
```

Приложение будет доступно по адресу: `http://localhost:5000`  
PostgreSQL: `localhost:5432`

Остановка:
```bash
docker-compose down
```

Просмотр логов:
```bash
docker-compose logs -f app
```

## Архитектура

- **`main.py`** — точка входа, Flask приложение с RESTful эндпоинтами.
- **`backend/config.py`** — конфигурация и переменные окружения.
- **`backend/db.py`** — инициализация SQLAlchemy engine и session.
- **`backend/models.py`** — ORM модель `File` для таблицы БД.
- **`backend/schemas.py`** — `FileUpdate` модель для автоматической трансформации JSON в объекты.
- **`backend/manager.py`** — бизнес-логика (`FileManager`): CRUD операции, управление файлами и БД транзакции.

## Установка и запуск

### 1. Подготовка окружения (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Подключение к БД

Убедитесь, что PostgreSQL запущен. По умолчанию приложение ожидает:
```
postgresql+psycopg2://postgres:kirill@localhost:5432/WinterPractic
```

### 3. Запуск приложения

```powershell
python main.py
```

Приложение будет доступно по адресу: `http://127.0.0.1:5000`

## Конфигурация

Основные параметры находятся в `backend/config.py`. Переопределить можно через переменные окружения:

| Переменная | Значение по умолчанию | Описание |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg2://postgres:kirill@localhost:5432/WinterPractic` | Строка подключения к PostgreSQL |
| `STORAGE_PATH` | Текущая папка | Путь к корневой директории для хранения файлов |
| `DEBUG` | `True` | Режим отладки Flask |

Пример установки переменной окружения в PowerShell:
```powershell
$Env:DATABASE_URL = "postgresql+psycopg2://user:pass@host:5432/dbname"
$Env:STORAGE_PATH = "C:/MyStorage"
```

## REST API Эндпоинты

Все ответы — JSON. Коды ошибок: 400 (неверные данные), 404 (не найдено), 500 (ошибка сервера).

### GET `/`
Проверка здоровья приложения.
```bash
curl http://127.0.0.1:5000/
```
Ответ:
```json
{"status": "ok"}
```

### GET `/files`
Получить список всех файлов. Можно фильтровать по подстроке в пути: `?q=substring`.
```bash
curl http://127.0.0.1:5000/files
curl http://127.0.0.1:5000/files?q=txt
```
Ответ:
```json
[
  {
    "id": 1,
    "name": "document",
    "extension": "pdf",
    "size": 2048,
    "path": "C:/storage/document.pdf",
    "created_at": "2026-02-19T10:30:00",
    "updated_at": "2026-02-19T10:30:00",
    "comment": "Important doc"
  }
]
```

### POST `/files`
Зарегистрировать файл в БД (файл должен существовать на диске).
```bash
curl -X POST http://127.0.0.1:5000/files \
  -H "Content-Type: application/json" \
  -d '{"dirpath": "C:/storage", "filename": "document.pdf"}'
```
Ответ (201 Created):
```json
{
  "id": 1,
  "name": "document",
  "extension": "pdf",
  ...
}
```

### GET `/files/{id}`
Получить информацию о конкретном файле.
```bash
curl http://127.0.0.1:5000/files/1
```
Ответ:
```json
{
  "id": 1,
  "name": "document",
  "extension": "pdf",
  ...
}
```

### PATCH `/files/{id}`
Обновить метаданные файла (название, путь, комментарий).
В запросе можно передать любые поля, они будут автоматически
конвертированы в модель `FileUpdate` на сервисе.
```bash
curl -X PATCH http://127.0.0.1:5000/files/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "document_v2", "comment": "Updated version"}'
```
Ответ:
```json
{
  "id": 1,
  "name": "document_v2",
  ...
}
```

### DELETE `/files/{id}`
Удалить файл из БД и с диска.
```bash
curl -X DELETE http://127.0.0.1:5000/files/1
```
Ответ:
```json
{"status": "deleted"}
```

### GET `/files/{id}/download`
Скачать файл на локальный компьютер.
```bash
curl -O http://127.0.0.1:5000/files/1/download
```

## Структура БД

Таблица `files` создаётся автоматически при запуске. Столбцы:

| Столбец | Тип | Описание |
|---|---|---|
| `id` | SERIAL PRIMARY KEY | Уникальный идентификатор |
| `name` | VARCHAR(256) | Имя файла без расширения |
| `extension` | VARCHAR(64) | Расширение файла |
| `size` | INTEGER | Размер файла в байтах |
| `path` | VARCHAR(1024) | Полный путь к файлу на диске |
| `created_at` | TIMESTAMP | Дата/время создания в БД |
| `updated_at` | TIMESTAMP | Дата/время последнего обновления |
| `comment` | VARCHAR(1024) | Произвольный комментарий |

## Development

### Структура проекта
```
WinterPractik/
├── main.py                 # Flask приложение и маршруты
├── backend/
│   ├── __init__.py
│   ├── config.py           # Конфигурация
│   ├── db.py               # SQLAlchemy engine и session
│   ├── models.py           # ORM модели
│   ├── schemas.py          # Модели данных для API (FileUpdate)
│   └── manager.py          # Бизнес-логика (FileManager)
├── requirements.txt        # Зависимости Python
└── README.md               # Этот файл
```

### Использование FileManager

`FileManager` в `backend/manager.py` обеспечивает:
- `list_files(search=None)` — получить список файлов (опционально фильтровать).
- `get(file_id)` — получить информацию о файле.
- `create_from_path(dirpath, filename)` — зарегистрировать существующий файл.
- `update(file_id, update_data)` — обновить метаданные, где `update_data` — dict или `FileUpdate` модель. JSON трансформируется в модель прямо в сервисе.
- `delete(file_id, remove_file=True)` — удалить запись в БД и файл с диска.

Все операции выполняются в транзакциях SQLAlchemy.


