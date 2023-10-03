import json
import time
import requests
from bs4 import BeautifulSoup

def zaka_zaka_games(url_base, num_pages):
    game_data = {}

    for page_number in range(1, num_pages + 1):
        url = f"{url_base}/page{page_number}"
        print(f"Scraping page: {url}")
        
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            tab_items = soup.find_all(class_='game-block')
            
            for item in tab_items:
                if "game-block-more" in item.get("class"):
                    continue
                
                name = item.find(class_="game-block-name").text
                price = float(item.find(class_="game-block-price").text[:-1])
                game_url = item.get('href')
                game_data[name] = {"price": price, "url": game_url}
        
        else:
            print(f'Failed to load page: {response.status_code}')

        time.sleep(1)

    return game_data

if __name__ == '__main__':
    zaka_zaka_url = 'https://zaka-zaka.com/game/new'
    num_pages_to_scrape = 15
    
    scraped_data = zaka_zaka_games(zaka_zaka_url, num_pages_to_scrape)

    with open("zaka.json", "w") as json_file:
        json.dump(scraped_data, json_file, indent=4)