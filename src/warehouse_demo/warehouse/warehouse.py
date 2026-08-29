
from typing import final


@final
class Warehouse:

    def __init__(self):
        self.products_csv_file = "products.csv"
        self.inventory_csv_file = "inventory.csv"
        self.customers_csv_file = "customers.csv"
        self.orders_csv_file = "orders.csv"

        self._products: dict[str, dict[str, float | str]] = {}
        self._inventory: dict[str, int] = {}
        self._customers: dict[str, dict[str, str]] = {}
        self._orders: dict[str, dict[str, int | str]] = {}

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

    def read_products(self):
        self._products = {}
        with open(self.products_csv_file, "r") as f:
            for line in f:
                product_id, name, price = line.strip().split(",")
                self._products[product_id] = {"name": name, "price": float(price)}

    def read_inventory(self):
        self._inventory = {}
        with open(self.inventory_csv_file, "r") as f:
            for line in f:
                product_id, quantity = line.strip().split(",")
                self._inventory[product_id] = int(quantity)

    def read_customers(self):
        self._customers = {}
        with open(self.customers_csv_file, "r") as f:
            for line in f:
                customer_id, name, email = line.strip().split(",")
                self._customers[customer_id] = {"name": name, "email": email}

    def read_orders(self):
        self._orders = {}
        with open(self.orders_csv_file, "r") as f:
            for line in f:
                order_id, customer_id, product_id, quantity = line.strip().split(",")
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
