
import csv
from typing import final

from .csv_reader import CsvReader
from .product import Product


@final
class Warehouse:

    def __init__(self):
        self._products = {}
        self._inventory = {}
        self._customers = {}
        self._orders = {}

        self.products_csv_file = "products.csv"
        self.inventory_csv_file = "inventory.csv"
        self.customers_csv_file = "customers.csv"
        self.orders_csv_file = "orders.csv"

    @property
    def products(self):
        return self._products

    @property
    def inventory(self):
        return self._inventory

    @property
    def customers(self):
        return self._customers

    @property
    def orders(self):
        return self._orders

    def get_products(self) -> list[Product]:
        if not self._products:
            self.read_products()

        return [
            Product(
                product_id=product_id,
                name=product_data["name"],
                price=product_data["price"],
            )
            for product_id, product_data in self._products.items()
        ]

    def get_inventory(self) -> dict[str, int]:
        if not self._inventory:
            self.read_inventory()
        return self._inventory

    @staticmethod
    def _create_csv_reader(input_stream) -> CsvReader:
        sample = input_stream.read(1024)
        input_stream.seek(0)

        delimiter = ","
        if sample:
            try:
                delimiter = csv.Sniffer().sniff(
                    sample,
                    delimiters=",|",
                ).delimiter
            except csv.Error:
                pass

        return CsvReader(input_stream, separator=delimiter)

    def read_products(self):
        self._products = {}
        with open(self.products_csv_file, "r") as f:
            reader = self._create_csv_reader(f)

            while reader.has_next_row():
                row = reader.next_row()
                if not row:
                    continue

                product_id, name, price = row
                self._products[product_id] = {"name": name, "price": float(price)}

    def read_inventory(self):
        self._inventory = {}
        with open(self.inventory_csv_file, "r") as f:
            reader = self._create_csv_reader(f)

            while reader.has_next_row():
                row = reader.next_row()
                if not row:
                    continue

                product_id, quantity = row
                self._inventory[product_id] = int(quantity)

    def read_customers(self):
        self._customers = {}
        with open(self.customers_csv_file, "r") as f:
            reader = self._create_csv_reader(f)

            while reader.has_next_row():
                row = reader.next_row()
                if not row:
                    continue

                customer_id, name, email = row
                self._customers[customer_id] = {"name": name, "email": email}

    def read_orders(self):
        self._orders = {}
        with open(self.orders_csv_file, "r") as f:
            reader = self._create_csv_reader(f)

            while reader.has_next_row():
                row = reader.next_row()
                if not row:
                    continue

                order_id, customer_id, product_id, quantity = row
                self._orders[order_id] = {
                    "customer_id": customer_id,
                    "product_id": product_id,
                    "quantity": int(quantity)
                }

    def load_all(self):
        self.read_products()
        self.read_inventory()
        self.read_customers()
        self.read_orders()
