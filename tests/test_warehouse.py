import pytest

from warehouse_demo.warehouse.warehouse import Warehouse


@pytest.mark.parametrize("csv_content,expected", [
    ("1,Product A,10.0\n2,Product B,20.0\n", {
        "1": {"name": "Product A", "price": 10.0},
        "2": {"name": "Product B", "price": 20.0}
    })
])
def test_read_products(tmp_path, csv_content, expected):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(csv_content)
    warehouse = Warehouse()
    warehouse.products_csv_file = str(csv_file)
    warehouse.read_products()
    assert warehouse.products == expected


def test_get_products_reads_products_csv_and_returns_product_models(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text("1,Product A,10.0\n2,Product B,20.0\n")
    warehouse = Warehouse()
    warehouse.products_csv_file = str(csv_file)

    products = warehouse.get_products()

    assert [(product.id, product.name, product.price) for product in products] == [
        ("1", "Product A", 10.0),
        ("2", "Product B", 20.0),
    ]


def test_get_products_supports_pipe_delimited_products_csv(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text("1|Milk|3.49\n2|Bread|2.79\n")
    warehouse = Warehouse()
    warehouse.products_csv_file = str(csv_file)

    products = warehouse.get_products()

    assert [(product.id, product.name, product.price) for product in products] == [
        ("1", "Milk", 3.49),
        ("2", "Bread", 2.79),
    ]

@pytest.mark.parametrize("csv_content,expected", [
    ("1,100\n2,200\n", {"1": 100, "2": 200})
])
def test_read_inventory(tmp_path, csv_content, expected):
    csv_file = tmp_path / "inventory.csv"
    csv_file.write_text(csv_content)
    warehouse = Warehouse()
    warehouse.inventory_csv_file = str(csv_file)
    warehouse.read_inventory()
    assert warehouse.inventory == expected

@pytest.mark.parametrize("csv_content,expected", [
    ("1,Customer A,a@example.com\n2,Customer B,b@example.com\n", {
        "1": {"name": "Customer A", "email": "a@example.com"},
        "2": {"name": "Customer B", "email": "b@example.com"}
    })
])
def test_read_customers(tmp_path, csv_content, expected):
    csv_file = tmp_path / "customers.csv"
    csv_file.write_text(csv_content)
    warehouse = Warehouse()
    warehouse.customers_csv_file = str(csv_file)
    warehouse.read_customers()
    assert warehouse.customers == expected

@pytest.mark.parametrize("csv_content,expected", [
    ("1,1,1,10\n2,2,2,20\n", {
        "1": {"customer_id": "1", "product_id": "1", "quantity": 10},
        "2": {"customer_id": "2", "product_id": "2", "quantity": 20}
    })
])
def test_read_orders(tmp_path, csv_content, expected):
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(csv_content)
    warehouse = Warehouse()
    warehouse.orders_csv_file = str(csv_file)
    warehouse.read_orders()
    assert warehouse.orders == expected