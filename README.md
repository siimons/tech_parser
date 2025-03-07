# Парсер каталогов запчастей и оборудования

Проект разработан для автоматизированного сбора данных об оборудовании и запчастях из публичных ресурсов. В нём реализованы инструменты для парсинга следующих сайтов:

- [ei.spb.ru](http://ei.spb.ru/brands)
- [dalkos.ru](http://dalkos.ru/manufacturers)
- [pzip.ru](http://pzip.ru/brands)
- [prmth.ru](http://prmth.ru/info/117)

## Структура проекта

```
equipment_parser/
│
├── data/
│   ├── dalkos.csv
│   ├── ei_spb.csv
│   ├── prmth.csv
│   └── pzip.csv
│
├── logs/
│   └── app.log
│
├── src/
│   ├── __init__.py
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── dalkos_parser.py
│   │   ├── ei_spb_parser.py
│   │   ├── prmth_parser.py
│   │   └── pzip_parser.py
│   └── utils/
│       ├── __init__.py
│       ├── data_saver.py
│       ├── http_client.py
│       └── logging.py
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/siimons/equipment_parser
cd equipment_parser

```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv

# Для Linux/MacOS
source venv/bin/activate

# Для Windows
venv\Scripts\activate

```

3. Установите необходимые зависимости:

```bash
pip install -r requirements.txt

```

4. Запустите программу:

```bash
python main.py

```