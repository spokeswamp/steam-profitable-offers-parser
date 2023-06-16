from prettytable import PrettyTable
from config import config
from modules import steam_market_parser

items = []


def draw_table():
    """
    Draw table with items dataset
    """
    items_table = PrettyTable(reversesort=True)
    items_table.field_names = ["Name", "Price", "List. count", "Weight"]
    items_table.add_rows(items)
    items_table.sortby = "Weight"

    print(items_table)


if __name__ == '__main__':
    if config['debug']:
        print("[INFO] App in debug mode")
    items = steam_market_parser.fill_items_data()
    draw_table()
