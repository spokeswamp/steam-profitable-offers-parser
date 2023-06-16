import json
import time
import httpx

from config import config


def get_items_by_api(start=0):
    """
    Retrieving items from steam market API
    :param start:
    :return:
    """
    url = "https://steamcommunity.com/market/search/render/" \
          "?category_730_Type[]=tag_CSGO_Type_WeaponCase" \
          "&sort_column=default" \
          "&appid=730" \
          "&norender=1" \
          "&count=100" \
          "&start={}".format(start)
    return httpx.get(url, cookies=config['cookies']).json()


def get_items_from_file():
    """
    Retrieving items from a file, for debugging (because steam has a rate limits)
    :return:
    """
    with open('items.json', 'r', encoding='utf8') as f:
        return json.load(f)


def get_items_page(start=0):
    """
    For debug and if you want to use a different API
    :param start:
    :return:
    """
    print("[INFO] Retrieving items with start = {}".format(start))
    if config['debug']:
        return get_items_from_file()
    else:
        return get_items_by_api(start)


def get_item_price(price):
    """
    If the item is not on sale, the price may be 0.
    Multiplication for simplified work with currencies other than dollars
    Dividing by 100 is necessary to get the correct price, because Steam returns it multiplied to 100
        (for correct floating-point operation, I think)
    :param price: :return:
    """
    if price == 0:
        return 0
    return round(price * config['usd_to_custom'] / 100, 4)


def get_item_weight(price, listings):
    """
    Price to listings weight to get profitable offers
    :param price:
    :param listings:
    :return:
    """
    if price == 0 or listings == 0:
        return 0
    return round(price / listings, 4)


def fill_items_data():
    """
    Gets the cases, then puts them into the resulting array with these indexes:
    0 - name,
    1 - price,
    2 - listings count
    3 - weight

    time.sleep() because rate limiting
    :return:
    """
    all_items = []
    start = 0
    total_count = 100

    while start < total_count:
        items_json = get_items_page(start)
        total_count = items_json['total_count']
        start += 100

        for item in items_json['results']:
            all_items.append([
                item['asset_description']['market_hash_name'],
                get_item_price(item['sell_price']),
                item['sell_listings'],
                get_item_weight(get_item_price(item['sell_price']), item['sell_listings'])
            ])

        time.sleep(config['cooldown_time'])

    return all_items
