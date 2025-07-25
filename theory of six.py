import requests
from bs4 import BeautifulSoup
import time

def extract_links(url):
    """Извлекаем все ссылки из статьи Википедии."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Найдем все ссылки в основном блоке и блоке References
    links = set()
    # Основной блок
    for a in soup.select('#bodyContent a[href^="/wiki/"]'):
        link = a.get('href')
        if link and not link.startswith('#'):
            links.add('https://en.wikipedia.org' + link)

    # Блок References
    for ref in soup.select('#References a[href^="/wiki/"]'):
        link = ref.get('href')
        if link and not link.startswith('#'):
            links.add('https://en.wikipedia.org' + link)

    return links

def find_path(nachal_url, final_url, limit):
    """Находим путь между двумя ссылками"""
       # Создается очередь, где значение ссылки хранится совместно со значением пути к ней (в списке)
    queue = [(nachal_url, [nachal_url])]
    visited = set()
    true_limit = 0

    while queue:
            # Выбираем текущую ссылку и путь к ней, после чего их удаляем из очереди проверки 
        true_url, path = queue.pop()
            # Проверка завершения поиска
        if true_url == final_url:
            return path
            # Проверка числа переходов
        depth = len(path)        
        if depth >= 5:
            #print(f"Переходов между ссылками больше 5") 
            continue         
              # Добавляем текущую страницу в очередь, если она еще не проверялась, и получаем ссылки с текущей страницы
        if true_url not in visited:
            visited.add(true_url)
            links = extract_links(true_url)
            true_limit = true_limit + 1
              # Проверка rate-limit
            if true_limit >= limit:
                time.sleep(1)  
                true_limit = 0  
            for link in links:
                if link not in visited:
              # Добавление ссылки, если она не проверялась, с текущей страницы в очередь
                    queue.append((link, path + [link]))
                        
    return None

def main(url10, url20, limit1):
    rez1 = find_path(url10, url20, limit1)
    rez2 = find_path(url20, url10, limit1)
    if rez1:
        print(f'Путь между ссылками от url1 к url2   {rez1}')
    else:
        print('Не удалось найти путь между ссылками url1 и url2')
    if rez2:
        print(f'Путь между ссылками от url2 к url1   {rez2}')
    else:
        print('Не удалось найти путь между ссылками url2 и url1')

# Основная программа
if __name__ == "__main__":
    print('Программа выполняет поиск переходов между двумя ссылками (не более пяти переходов)')
    print('Первая ссылка url1 = https://en.wikipedia.org/wiki/Six_degrees_of_separation')
    print('Вторая ссылка url2 = https://en.wikipedia.org/wiki/American_Broadcasting_Company')
    url1 = "https://en.wikipedia.org/wiki/Six_degrees_of_separation"
    url2 = "https://en.wikipedia.org/wiki/American_Broadcasting_Company"
    rate_limit = 10  
    main(url1, url2, rate_limit)