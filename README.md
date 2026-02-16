# WinterPractik

Небольшое Python-приложение. Краткое описание проекта и инструкции по запуску.

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

## Отправка на GitHub
1. Создать репозиторий на GitHub (через веб-интерфейс или `gh` CLI).
2. Привязать удалённый репозиторий и запушить:
```powershell
git remote add origin https://github.com/<USERNAME>/<REPO>.git
git branch -M main
git push -u origin main
```

Или с помощью GitHub CLI (если установлен и настроен):
```powershell
gh repo create <REPO> --public --source=. --remote=origin --push
```

Если хотите, могу создать репозиторий через `gh` и запушить (потребуется ваша авторизация `gh`).
