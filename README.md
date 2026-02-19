# WinterPractik

<<<<<<< HEAD
Небольшое Python-приложение. Краткое описание проекта и инструкции по запуску.
=======
Python-приложение по управлению файловой системой компьютера через браузер.
>>>>>>> e73b98e8f3f530283c4b87c9d554ab879362f7aa

## Требования
- Python 3.10+ (рекомендуется)
- зависимости в `requirements.txt`

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

## Пояснения
- Внешние зависимости: `Flask`, `psycopg2-binary` (указаны в `requirements.txt`).
- Стандартные библиотеки (`os`, `datetime`, `time`, `shutil`, `json`) не требуют установки.