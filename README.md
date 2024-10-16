# Парсер для сайтов с информацией о бытовой технике

Этот проект предназначен для парсинга данных с различных веб-сайтов, предоставляющих информацию о бытовой технике. В частности, программа собирает данные с следующих ресурсов:

- [ei.spb.ru/brands](http://ei,spb.ru/brands)
- [dalkos.ru/manufacturers](http://dalkos.ru/manufacturers)
- [pzip.ru/brands](http://pzip.ru/brands)
- [prmth.ru/info/117](http://prmth.ru/info/117)

## Структура проекта

```
parse_appliances/
├── logs/
│   ├── dalkos_parser.log
│   ├── ei_spb_parser.log
│   ├── prmth_parser.log
│   ├── pzip_parser.log
│   └── parser.log
├── output/
│   ├── dalkos.txt
│   ├── ei_spb.txt
│   ├── prmth.txt
│   └── pzip.txt
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
│       ├── file_utils.py
│       ├── logger_setup.py
│       ├── proxy_picker.py
│       └── user_agent.py
├── main.py
├── README.md
└── requirements.txt
```

## Используемые технологии

- **Requests**: Библиотека для выполнения HTTP-запросов к веб-сайтам.
- **BeautifulSoup**: Библиотека для парсинга HTML и извлечения данных из веб-страниц.
- **asyncio**: Модуль для работы с асинхронным программированием, используется в некоторых парсерах для повышения производительности.
- **loguru**: Модуль для логирования событий и ошибок в процессе работы парсера.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <URL_репозитория>
   cd parse_appliances

   ```
2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
 
    ```
3. Запустите программу:
    ```bash
    python3 main.py

    ```