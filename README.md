# Парсер для сайтов с информацией о бытовой технике

Этот проект предназначен для парсинга данных с различных веб-сайтов, предоставляющих информацию о бытовой технике. В частности, программа собирает данные со следующих ресурсов:

- [ei.spb.ru/brands](http://ei,spb.ru/brands)
- [dalkos.ru/manufacturers](http://dalkos.ru/manufacturers)
- [pzip.ru/brands](http://pzip.ru/brands)
- [prmth.ru/info/117](http://prmth.ru/info/117)

## Структура проекта

```
tech_parser/
├── logs/
│   ├── dalkos_parser.log
│   ├── ei_spb_parser.log
│   ├── prmth_parser.log
│   ├── pzip_parser.log
│   └── parser.log
├── output/
│   ├── dalkos.csv
│   ├── ei_spb.csv
│   ├── prmth.csv
│   └── pzip.csv
├── src/
│   ├── __init__.py
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── dalkos_async_parser.py
│   │   ├── dalkos_parser.py
│   │   ├── ei_spb_parser.py
│   │   ├── prmth_parser.py
│   │   ├── pzip_async_parser.py
│   │   └── pzip_parser.py
│   └── utils/
│       ├── __init__.py
│       ├── file_handling/
│       │   ├── __init__.py
│       │   └── file_saver.py
│       ├── logging/
│       │   ├── __init__.py
│       │   └── logger_setup.py
│       └── requests/
│           ├── __init__.py
│           ├── proxy_picker.py
│           ├── request_handler.py
│           └── user_agent.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Используемые технологии

- **Requests**: Библиотека для выполнения HTTP-запросов к веб-сайтам.
- **BeautifulSoup**: Библиотека для парсинга HTML и извлечения данных из веб-страниц.
- **loguru**: Модуль для логирования событий и ошибок в процессе работы парсера.

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/siimons/tech_parser
cd tech_parser

```

2. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv

source venv/bin/activate      # Для Linux/MacOS
venv\Scripts\activate         # Для Windows

```

3. Установите зависимости:

```bash
pip install -r requirements.txt

```

4. Запустите программу:

```bash
python3 main.py

```