import requests
from bs4 import BeautifulSoup
import data_client


class Parser:
    links_to_parse = [
        'https://www.kufar.by/l/mebel',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6Mn0%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30%3D'
    ]

    data_client_imp = data_client.PostgresClient()

    @staticmethod
    def get_meb_by_link(link):
        response = requests.get(link)
        meb_data = response.text

        meb_items = []

        to_parse = BeautifulSoup(meb_data, 'html.parser')
        for el in to_parse.find_all('a', class_='styles_wrapper__yaLfq'):
            try:
                price, description = el.text.split('р.')
                meb_items.append((
                    el['href'],
                    int(price.replace(' ', '')),
                    description
                ))
            except:
                print(f'Цена не была указана. {el.text}')

        return meb_items

    def save_to_postgres(self, meb_items):
        connection = self.data_client_imp.get_connection()
        self.data_client_imp.create_meb_table(connection)
        for item in meb_items:
            self.data_client_imp.insert(connection, item[0], int(item[1]), item[2])

    def run(self):
        meb_items = []
        for link in Parser.links_to_parse:
            meb_items.extend(self.get_meb_by_link(link))
        self.save_to_postgres(meb_items)


Parser().run()