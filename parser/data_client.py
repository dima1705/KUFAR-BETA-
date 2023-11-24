from sqlite3 import Error
import psycopg2
from abc import ABC, abstractmethod
import sqlite3
import pandas


class DataClient(ABC):

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def create_meb_table(self, conn):
        pass

    @abstractmethod
    def get_items(self, conn, price_from=0, price_to=100000):
        pass

    @abstractmethod
    def insert(self, conn, link, price, description):
        pass

    def run_test(self):
        conn = self.get_connection()
        self.create_meb_table(conn)
        items = self.get_items(conn, 10, 30)
        for item in items:
            if conn is not None:
                if True:
                    print(item)
                conn.close()
            else:
                print(item)


class PostgresClient(DataClient):
    USER = 'postgres'
    PASSWORD = 'postgres'
    HOST = 'localhost'
    PORT = '5432'

    def get_connection(self):
        try:
            conn = psycopg2.connect(
                user=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT
            )
            return conn
        except Error:
            print(Error)

    def create_meb_table(self, conn):
        cursor_object = conn.cursor()
        cursor_object.execute(
            """
                CREATE TABLE IF NOT EXISTS app_1_meb
                (
                    id serial PRIMARY KEY,
                    link text,
                    price integer,
                    description text
                )
            """
        )
        conn.commit()

    def get_items(self, conn, price_from=0, price_to=100000):
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM app_1_meb WHERE price >= {price_from} and price <= {price_to}')
        return cursor.fetchall()

    def insert(self, conn, link, price, description):
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO app_1_meb (link, price, description) VALUES ('{link}', '{price}', '{description}')")
        conn.commit()


class Sqlite3Client(DataClient):
    DB_NAME = "kufar.db"

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            return conn
        except Error:
            print(Error)

    def create_meb_table(self, conn):
        cursor_object = conn.cursor()
        cursor_object.execute(
            """
                CREATE TABLE IF NOT EXISTS app_1_meb
                (
                    id integer PRIMARY KEY autoincrement, 
                    link text, 
                    price integer, 
                    description text
                )
            """
        )
        conn.commit()

    def get_items(self, conn, price_from=0, price_to=100000):
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM app_1_meb WHERE price >= {price_from} and price <= {price_to}')
        return cursor.fetchall()

    def insert(self, conn, link, price, description):
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO app_1_meb (link, price, description) VALUES ('{link}', '{price}', '{description}')")
        conn.commit()


class CSVClient(DataClient):
    CSVName = 'meb.csv'

    def get_connection(self):
        pass

    def create_meb_table(self, conn):
        pass

    def get_items(self, conn, price_from=0, price_to=100000):
        df = pandas.read_csv(self.CSVName, sep=',', names=['link', 'price', 'description'])
        data = df[(df.price >= price_from) & (df.price <= price_to)]
        data_csv = (data['link'] + ', ' + data['price'].astype(str) + ', ' + data['description']).to_list()
        return data_csv

    def insert(self, conn, link, price, description):
        pandas.DataFrame(
            {
                'link': [link],
                'price': [price],
                'description': [description]
            }
        ).to_csv(
            self.CSVName,
            mode='a',
            index=False,
            header=False
        )


# data_client = PostgresClient()
# data_client = Sqlite3Client()
# data_client = CSVClient()
# data_client.run_test()
