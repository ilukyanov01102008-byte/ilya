# ilya
kod 5 
# Currency Converter

**Автор:** Строк Лукьянов Илья  
**Дата:** апрель 2026 г.

## Описание
Графическое приложение для конвертации валют с использованием актуальных курсов из внешнего API (exchangerate-api.com). Поддерживает сохранение истории конвертаций в JSON-файл и её просмотр.

## Как получить API-ключ
1. Зарегистрируйтесь на [exchangerate-api.com](https://app.exchangerate-api.com/sign-up)
2. Скопируйте ключ из панели управления
3. Вставьте его в переменную `API_KEY` в файле `currency_converter.py`

## Установка и запуск
```bash
# Клонировать репозиторий
git clone https://github.com/ваш_username/CurrencyConverter.git
cd CurrencyConverter

# Установить зависимости
pip install requests

# Запустить приложение
python currency_converter.py
