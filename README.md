# File repository

Python-приложение по управлению файловой системой компьютера через браузер.

## Ключевые возможности
- Загрузка файлов на диск и регистрация метаданных в PostgreSQL
- Получение списка файлов и метаданных в формате JSON
- Поиск по шаблону пути
- Скачивание, обновление и удаление файлов

## Технологии
- Python 3.10+
- Flask 2.3.x
- PostgreSQL (psycopg2-binary)

## Установка (Windows PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Запуск
```powershell
python main.py
```

## API — основные эндпоинты

Все ответы возвращаются в JSON (миметип `application/json`). Ниже примеры с `curl`.

- GET `/all` — получить все файлы

```bash
curl http://127.0.0.1:5000/all
```

- POST `/file` — получить файл по точному пути (форма или x-www-form-urlencoded)

```bash
curl -X POST -F "path=C:/storage/file.txt" http://127.0.0.1:5000/file
```

- POST `/add` — загрузить файл (multipart/form-data)

```bash
curl -F "file=@myfile.txt" -F "path=C:/storage/" http://127.0.0.1:5000/add
```

- POST `/delete` — удалить файл

```bash
curl -X POST -F "path=C:/storage/myfile.txt" http://127.0.0.1:5000/delete
```

- POST `/search` — поиск по шаблону пути

```bash
curl -X POST -F "path=/root-folder/" http://127.0.0.1:5000/search
```

- POST `/download` — скачать файл

```bash
curl -X POST -F "path=C:/storage/myfile.txt" http://127.0.0.1:5000/download --output myfile.txt
```

- POST `/update` + `/update_confirm` — обновление метаданных и перемещение файла

