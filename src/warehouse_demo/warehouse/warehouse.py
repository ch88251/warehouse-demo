
import csv
from pathlib import Path
from typing import final

from .csv_reader import CsvReader
from .product import Product
from .warehouse_exception import WarehouseException


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

    def add_product(
        self,
        name: str,
        price: float,
    ) -> Product:
        name = name.strip()

        if not name:
            raise WarehouseException("Product name cannot be empty.")

        if not self._products and Path(self.products_csv_file).exists():
            self.read_products()

        product_id = str(self._get_next_product_id())

        delimiter = self._get_csv_delimiter(self.products_csv_file)
        self._ensure_trailing_newline(self.products_csv_file)

        with open(self.products_csv_file, "a", newline="") as output_stream:
            writer = csv.writer(
                output_stream,
                delimiter=delimiter,
                lineterminator="\n",
            )
            writer.writerow([product_id, name, price])

        self._products[product_id] = {
            "name": name,
            "price": price,
        }

        return Product(
            product_id=product_id,
            name=name,
            price=price,
        )

    def _get_next_product_id(self) -> int:
        numeric_ids = [int(product_id) for product_id in self._products]
        return max(numeric_ids, default=0) + 1

    @staticmethod
    def _create_csv_reader(input_stream) -> CsvReader:
        return CsvReader(
            input_stream,
            separator=Warehouse._detect_csv_delimiter(input_stream),
        )

    @staticmethod
    def _detect_csv_delimiter(input_stream) -> str:
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

        return delimiter

    def _get_csv_delimiter(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.exists() or path.stat().st_size == 0:
            return ","

        with path.open("r") as input_stream:
            return self._detect_csv_delimiter(input_stream)

    @staticmethod
    def _ensure_trailing_newline(file_path: str) -> None:
        path = Path(file_path)
        if not path.exists() or path.stat().st_size == 0:
            return

        with path.open("rb+") as output_stream:
            output_stream.seek(-1, 2)
            if output_stream.read(1) != b"\n":
                output_stream.write(b"\n")

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

                if row == ["product", "quantity"]:
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

                if len(row) == 2:
                    customer_id, name = row
                    email = ""
                else:
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

                if row == ["id", "customer_id", "date", "product", "quantity", "pending"]:
                    continue

                if len(row) == 4:
                    order_id, customer_id, product_id, quantity = row
                    order_data = {
                        "customer_id": customer_id,
                        "product_id": product_id,
                        "quantity": int(quantity),
                    }
                else:
                    order_id, customer_id, date, product_name, quantity, pending = row
                    order_data = {
                        "customer_id": customer_id,
                        "product_id": product_name,
                        "quantity": int(quantity),
                        "date": date,
                        "pending": pending.lower() == "true",
                    }

                self._orders[order_id] = order_data

    def load_all(self):
        self.read_products()
        self.read_inventory()
        self.read_customers()
        self.read_orders()
