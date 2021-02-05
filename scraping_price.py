import re
from bs4 import BeautifulSoup
import urllib.request

results = []
PATH = 'https://www.olx.ua/uk/elektronika/telefony-i-aksesuary/q-google-pixel-3/?page='


def get_content(page=0, number_of_pages=1):
    """Scraping our site"""
    
    while page != number_of_pages:        # number of pages
        try:
            r = urllib.request.urlopen(f'{PATH}{page}')
            html = r.read()
            page += 1
            soup = BeautifulSoup(html, 'html.parser')
            new = soup.find_all('div', class_='offer-wrapper')
            select_content(new)
        except StopIteration:
            break


def select_price(price):
    """Filter by price"""
    
    return True if 2000 < int(re.sub('[ ,грн.]', '', price)) < 5000 else False



def select_content(new):
    """Getting specific content, filter and sort it"""

    for item in new:
        price = item.find("p", class_="price").get_text(strip=True)
        title = item.find("strong").get_text(strip=True)
        href = item.a.get("href")
        print(price)
        if select_price(price):
            results.append([title, price, href])
    result = sorted(results, key=lambda x: x[1], reverse=True)
    write_down(result)


def write_down(result):
    """write down result in txt file"""

    with open("price.txt", "w", encoding="utf-8") as file:
        for i in result:
            file.write(f'Title : {i[0]}\nPrice : {i[1]}\nLink : {i[2]}\n\n')


if __name__ == '__main__':
    get_content(0, 2)
