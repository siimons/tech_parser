import random as rnd

proxies = [
    "http://123.45.67.89:8080",
    "http://98.76.54.32:3128",
    "http://111.222.333.444:8888",
    "https://123.456.789.012:443",
    "http://12.34.56.78:9090",
]

def get_random_proxy():
    """Возвращает случайный прокси из списка."""
    return rnd.choice(proxies)