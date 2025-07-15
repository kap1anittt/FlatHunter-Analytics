import requests
import pandas as pd
from datetime import datetime
import time
import random
from bs4 import BeautifulSoup

def get_cian_api_data(page: int = 1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    json_data = {
        "jsonQuery": {
            "_type": "flatrent",
            "region": {"type": "terms", "value": [1]},
            "room": {"type": "terms", "value": [1, 2, 3, 4]},
            "for_day": {"type": "term", "value": "!1"},
            "page": {"type": "term", "value": page}
        }
    }

    try:
        response = requests.post(
            'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
            headers=headers,
            json=json_data,
            timeout=15
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return None

def parse_seller_info(offer: dict) -> tuple:
    """Извлекаем детальную информацию о продавце"""
    user = offer.get('user', {})
    phones = user.get('phones', [{}])
    
    # Парсим HTML с описанием продавца
    seller_html = user.get('description', '')
    try:
        soup = BeautifulSoup(seller_html, 'html.parser')
        seller_type = soup.find('span', class_=lambda x: x and 'color_gray60_100' in x)
        seller_name = soup.find('span', class_=lambda x: x and 'color_current_color' in x)
        
        seller_type_text = seller_type.get_text(strip=True) if seller_type else user.get('userType', '')
        seller_name_text = seller_name.get_text(strip=True) if seller_name else user.get('name', '')
        
        # Форматируем ID продавца
        seller_id = f"ID {user['id']}" if user.get('id') else ''
    except:
        seller_type_text = user.get('userType', '')
        seller_name_text = user.get('name', '')
        seller_id = ''
    
    return {
        'author': f"{seller_id} {seller_name_text}".strip(),
        'author_type': seller_type_text,
        'phone': phones[0].get('number', '') if phones else '',
        'agent_name': user.get('agentName', '')
    }

def parse_offer(offer: dict) -> dict:
    building = offer.get('building', {})
    geo = offer.get('geo', {})
    
    # Получаем информацию о продавце
    seller_info = parse_seller_info(offer)
    
    # Обработка даты
    creation_date = ''
    if offer.get('creationDate'):
        try:
            if isinstance(offer['creationDate'], int):
                creation_date = datetime.fromtimestamp(offer['creationDate']).strftime('%Y-%m-%d')
            elif isinstance(offer['creationDate'], str) and offer['creationDate'].isdigit():
                creation_date = datetime.fromtimestamp(int(offer['creationDate'])).strftime('%Y-%m-%d')
            else:
                creation_date = offer['creationDate'][:10] if offer['creationDate'] else ''
        except:
            creation_date = ''

    return {
        'author': seller_info['author'],
        'author_type': seller_info['author_type'],
        'agent_name': seller_info['agent_name'],
        'url': f"https://www.cian.ru/rent/flat/{offer.get('id', '')}/",
        'location': 'Москва',
        'deal_type': 'rent_long',
        'accommodation_type': 'flat',
        'price': offer.get('bargainTerms', {}).get('price', ''),
        'year_of_construction': building.get('buildYear', ''),
        'house_material_type': building.get('materialType', ''),
        'heating_type': building.get('heatingType', ''),
        'gas_type': building.get('gasType', ''),
        'water_supply_type': building.get('waterSupplyType', ''),
        'sewage_system': building.get('sewerageType', ''),
        'bathroom': offer.get('bathroom', ''),
        'living_meters': offer.get('livingArea', ''),
        'floors_count': building.get('floorsCount', ''),
        'phone': seller_info['phone'],
        'district': geo.get('districtName', ''),
        'underground': ', '.join([s['name'] for s in geo.get('undergrounds', [])]),
        'street': geo.get('streetName', ''),
        'house_number': geo.get('houseNumber', ''),
        'creation_date': creation_date
    }

def main():
    data = []
    for page in range(1, 100):
        print(f"Парсинг страницы {page}...")
        result = get_cian_api_data(page)
        if result and result.get('data'):
            try:
                offers = result['data'].get('offersSerialized', [])
                data.extend([parse_offer(o) for o in offers])
            except Exception as e:
                print(f"Ошибка обработки страницы {page}: {e}")
        time.sleep(random.uniform(1, 3))
    
    if data:
        df = pd.DataFrame(data)
        filename = f'cian_rent_{datetime.now().strftime("%Y%m%d")}.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\nСохранено {len(data)} объявлений в {filename}")
        print("Пример данных о продавцах:")
        print(df[['author', 'author_type', 'agent_name', 'phone']].head())
    else:
        print("Не удалось получить данные")

if __name__ == "__main__":
    main()