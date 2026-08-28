class Warehouse:

    def __init__(self):
        self.products_csv_file = "products.csv"
        self.inventory_csv_file = "inventory.csv"
        self.customers_csv_file = "customers.csv"
        self.orders_csv_file = "orders.csv"

        self.products = {}
        self.inventory = {}
        self.customers = {}
        self.orders = {}

    def read_products(self):
        with open(self.products_csv_file, "r") as f:
            for line in f:
                product_id, name, price = line.strip().split(",")
                self.products[product_id] = {"name": name, "price": float(price)}

    def read_inventory(self):
        with open(self.inventory_csv_file, "r") as f:
            for line in f:
                product_id, quantity = line.strip().split(",")
                self.inventory[product_id] = int(quantity)

    def read_customers(self):
        with open(self.customers_csv_file, "r") as f:
            for line in f:
                customer_id, name, email = line.strip().split(",")
                self.customers[customer_id] = {"name": name, "email": email}

    def read_orders(self):
        with open(self.orders_csv_file, "r") as f:
            for line in f:
                order_id, customer_id, product_id, quantity = line.strip().split(",")
                self.orders[order_id] = {
                    "customer_id": customer_id,
                    "product_id": product_id,
                    "quantity": int(quantity)
                }
