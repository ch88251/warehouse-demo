import builtins

from warehouse_demo.cli.cli import Cli
from warehouse_demo.warehouse.warehouse import Warehouse


def test_do_product_action_adds_product_to_products_csv(tmp_path, capsys, monkeypatch) -> None:
    csv_file = tmp_path / "products.csv"
    csv_file.write_text("1|Milk|3.49\n")

    warehouse = Warehouse()
    warehouse.products_csv_file = str(csv_file)
    warehouse.read_products()

    cli = Cli()
    cli._warehouse = warehouse

    answers = iter(["Bread", "2.79"])
    monkeypatch.setattr(builtins, "input", lambda _: next(answers))

    cli._do_product_action(2)

    captured = capsys.readouterr()

    assert "Added product 2: Bread (2.79)" in captured.out
    assert csv_file.read_text().splitlines() == [
        "1|Milk|3.49",
        "2|Bread|2.79",
    ]
