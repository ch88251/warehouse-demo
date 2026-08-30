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


def test_add_product_appends_to_products_csv_and_updates_cache(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text("1|Milk|3.49\n")
    warehouse = Warehouse()
    warehouse.products_csv_file = str(csv_file)

    product = warehouse.add_product("Bread", 2.79)

    assert (product.id, product.name, product.price) == ("2", "Bread", 2.79)
    assert warehouse.products == {
        "1": {"name": "Milk", "price": 3.49},
        "2": {"name": "Bread", "price": 2.79},
    }
    assert csv_file.read_text().splitlines() == [
        "1|Milk|3.49",
        "2|Bread|2.79",
    ]


def test_add_product_uses_next_highest_numeric_id(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text("1,Milk,3.49\n10,Bread,2.79\n")
    warehouse = Warehouse()
    warehouse.products_csv_file = str(csv_file)

    product = warehouse.add_product("Eggs", 4.29)

    assert product.id == "11"
    assert csv_file.read_text().splitlines() == [
        "1,Milk,3.49",
        "10,Bread,2.79",
        "11,Eggs,4.29",
    ]


def test_add_product_adds_newline_before_appending_to_last_row(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text("1|Milk|3.49")
    warehouse = Warehouse()
    warehouse.products_csv_file = str(csv_file)

    product = warehouse.add_product("Bread", 2.79)

    assert product.id == "2"
    assert "\r" not in csv_file.read_text()
    assert csv_file.read_text().splitlines() == [
        "1|Milk|3.49",
        "2|Bread|2.79",
    ]


def test_read_inventory_skips_runtime_header_row(tmp_path):
    csv_file = tmp_path / "inventory.csv"
    csv_file.write_text("product|quantity\nMilk|50\nBread|40\n")
    warehouse = Warehouse()
    warehouse.inventory_csv_file = str(csv_file)

    warehouse.read_inventory()

    assert warehouse.inventory == {"Milk": 50, "Bread": 40}

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


def test_read_customers_supports_rows_without_email(tmp_path):
    csv_file = tmp_path / "customers.csv"
    csv_file.write_text("1|John Smith\n2|Jane Doe\n")
    warehouse = Warehouse()
    warehouse.customers_csv_file = str(csv_file)

    warehouse.read_customers()

    assert warehouse.customers == {
        "1": {"name": "John Smith", "email": ""},
        "2": {"name": "Jane Doe", "email": ""},
    }

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


def test_read_orders_supports_runtime_header_and_extended_columns(tmp_path):
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(
        "id|customer_id|date|product|quantity|pending\n"
        "1|1|2024-06-01|Milk|2|true\n"
    )
    warehouse = Warehouse()
    warehouse.orders_csv_file = str(csv_file)

    warehouse.read_orders()

    assert warehouse.orders == {
        "1": {
            "customer_id": "1",
            "product_id": "Milk",
            "quantity": 2,
            "date": "2024-06-01",
            "pending": True,
        }
    }