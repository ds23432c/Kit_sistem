# EduAsset — Система мониторинга IT-оборудования

## Стек
Django 4.2 + MySQL (Railway) + Gunicorn + WhiteNoise

## Быстрый деплой на Railway (5 шагов)

### 1. Запушить в GitHub
```bash
cd Kit_sistem
git remote set-url origin https://github.com/ds23432c/Kit_sistem.git
# Создайте токен: GitHub → Settings → Developer settings → Personal access tokens
git push origin main
```

### 2. Создать сервис на Railway
- Открыть https://railway.app
- New Project → Deploy from GitHub repo → выбрать Kit_sistem

### 3. Добавить переменные окружения в Railway
В Railway → ваш сервис → Variables → добавить:
```
SECRET_KEY=сгенерируйте-любую-длинную-строку-50-символов
DEBUG=False
ALLOWED_HOSTS=*
```

Переменные MySQL Railway добавит **автоматически** при добавлении MySQL-сервиса.
Если MySQL уже есть — добавьте Variable Reference из него.

### 4. Railway сам выполнит:
```
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py load_fixtures   # загрузка тестовых данных
gunicorn config.wsgi --workers 2
```

### 5. Готово! Логины для входа:

| Логин    | Пароль   | Роль               |
|----------|----------|--------------------|
| admin    | admin123 | Администратор      |
| ahc      | admin123 | Зам. по АХЧ        |
| keeper1  | admin123 | Заведующий каб.    |
| keeper2  | admin123 | Заведующий каб.    |
| keeper3  | admin123 | Заведующий каб.    |
| tech1    | admin123 | Техник             |
| tech2    | admin123 | Техник             |
| buh1     | admin123 | Бухгалтерия        |

## Тестовые данные (загружаются автоматически)
- 1 здание → 3 этажа → 10 кабинетов
- 12 видов оборудования
- 25 единиц оборудования (реальные марки и модели)
- 10 заявок на ремонт (разные статусы)
- 3 запроса на изменение
- Логи изменений и уведомления

## Структура URL
```
/login/              → Вход
/dashboard/          → Дашборд
/map/                → Интерактивная карта
/map/editor/         → Редактор карты (только admin)
/equipment/          → Список оборудования
/equipment/<id>/     → Карточка оборудования
/equipment/import/   → Импорт Excel
/equipment/export/   → Экспорт Excel
/requests/           → Заявки на ремонт
/accounting/         → Бухгалтерия
/admin/users/        → Пользователи (только admin)
/changelog/          → Лог изменений
```

## Локальная разработка
```bash
# Создайте .env из примера
cp .env.example .env
# Отредактируйте данные БД (или используйте SQLite для теста)

# Установите зависимости
pip install -r requirements.txt

# Миграции и данные
python manage.py migrate
python manage.py load_fixtures

# Запуск
python manage.py runserver
```
