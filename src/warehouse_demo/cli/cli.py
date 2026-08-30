import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TextIO, final

from warehouse_demo.warehouse.exporter import Exporter
from warehouse_demo.warehouse.report import Report
from warehouse_demo.warehouse.warehouse import Warehouse
from warehouse_demo.warehouse.warehouse_exception import WarehouseException


class UnsupportedOperationError(Exception):
    """Raised when a menu operation has not been implemented."""


@final
class Cli:

    @dataclass(frozen=True)
    class MenuOption:
        number: int
        label: str

    MAIN_MENU_OPTIONS = (
        MenuOption(1, "Manage products"),
        MenuOption(2, "Manage customers"),
        MenuOption(3, "Manage orders"),
        MenuOption(4, "Export reports"),
        MenuOption(5, "Exit program"),
    )

    PRODUCT_OPTIONS = (
        MenuOption(1, "List products"),
        MenuOption(2, "Add product"),
        MenuOption(3, "Update product"),
        MenuOption(4, "Delete product"),
        MenuOption(5, "Go back to previous menu"),
    )

    CUSTOMER_OPTIONS = (
        MenuOption(1, "List customers"),
        MenuOption(2, "Add customer"),
        MenuOption(3, "Update customer"),
        MenuOption(4, "Delete customer"),
        MenuOption(5, "Go back to previous menu"),
    )

    ORDER_OPTIONS = (
        MenuOption(1, "List orders"),
        MenuOption(2, "Add order"),
        MenuOption(3, "Update order"),
        MenuOption(4, "Delete order"),
        MenuOption(5, "Go back to previous menu"),
    )

    REPORT_OPTIONS = (
        MenuOption(1, "Daily revenue report"),
        MenuOption(2, "Go back to previous menu"),
    )

    SUB_MENU_OPTIONS = {  # noqa: RUF012
        1: PRODUCT_OPTIONS,
        2: CUSTOMER_OPTIONS,
        3: ORDER_OPTIONS,
        4: REPORT_OPTIONS,
    }

    EXPORT_OPTIONS = (
        MenuOption(1, "Export to TXT"),
        MenuOption(2, "Go back to previous menu"),
    )

    def __init__(self) -> None:
        self._warehouse: Warehouse | None = None

    def run(self) -> None:
        try:
            self._warehouse = Warehouse()
            self._warehouse.load_all()
        except FileNotFoundError as error:
            print(
                "Please ensure the required CSV files are present: "
                f"{error}",
                file=sys.stderr,
            )
            raise SystemExit(1) from error
        except WarehouseException as error:
            print(
                f"Failed to initialize the warehouse: {error}",
                file=sys.stderr,
            )
            raise SystemExit(2) from error

        while True:
            self._display_main_menu()

            try:
                main_menu_choice = self._choose_main_menu_option()

                if main_menu_choice == -1:
                    break

                while True:
                    self._display_sub_menu(main_menu_choice)

                    try:
                        sub_menu_choice = self._choose_sub_menu_option(
                            main_menu_choice
                        )

                        if sub_menu_choice == -1:
                            break

                        self._do_menu_action(
                            main_menu_choice,
                            sub_menu_choice,
                        )
                    except ValueError as error:
                        print(error, file=sys.stderr)
                    except WarehouseException as error:
                        print(error, file=sys.stderr)
                    except UnsupportedOperationError as error:
                        print(error, file=sys.stderr)

            except ValueError as error:
                print(error, file=sys.stderr)
            except WarehouseException as error:
                print(error, file=sys.stderr)
            except UnsupportedOperationError as error:
                print(error, file=sys.stderr)

    def _display_main_menu(self) -> None:
        self._display_menu(self.MAIN_MENU_OPTIONS)

    def _display_sub_menu(self, main_menu_choice: int) -> None:
        options = self.SUB_MENU_OPTIONS[main_menu_choice]
        self._display_menu(options)

    @staticmethod
    def _display_menu(
        options: Sequence[MenuOption],
    ) -> None:
        for option in options:
            print(f"{option.number}.\t{option.label}")

    def _choose_main_menu_option(self) -> int:
        return self._choose_menu_option(self.MAIN_MENU_OPTIONS)

    def _choose_sub_menu_option(
        self,
        main_menu_choice: int,
    ) -> int:
        options = self.SUB_MENU_OPTIONS[main_menu_choice]
        return self._choose_menu_option(options)

    @staticmethod
    def _choose_menu_option(
        options: Sequence[MenuOption],
    ) -> int:
        raw_choice = input("Enter a menu option and press RETURN: ")

        try:
            choice = int(raw_choice)
        except ValueError:
            raise ValueError(
                "Invalid input. Enter a number."
            ) from None

        first_option = options[0]
        last_option = options[-1]

        if not first_option.number <= choice <= last_option.number:
            raise ValueError(
                "Invalid menu choice. Available options are "
                f"{first_option.number} to {last_option.number}."
            )

        # The last option is always Exit or Go Back.
        if choice == last_option.number:
            return -1

        return choice

    def _do_menu_action(
        self,
        main_menu_choice: int,
        sub_menu_choice: int,
    ) -> None:
        if main_menu_choice == 1:
            self._do_product_action(sub_menu_choice)
        elif main_menu_choice == 2:
            self._do_customer_action(sub_menu_choice)
        elif main_menu_choice == 3:
            self._do_order_action(sub_menu_choice)
        elif main_menu_choice == 4:
            self._do_report_action(sub_menu_choice)
        else:
            raise RuntimeError(
                "There are only four main menu options; "
                "this cannot happen."
            )

    def _do_product_action(
        self,
        sub_menu_choice: int,
    ) -> None:
        if sub_menu_choice == 1:
            self._do_product_list()
        elif sub_menu_choice == 2:
            self._do_product_add()
        elif sub_menu_choice == 3:
            raise UnsupportedOperationError(
                "Updating products not yet implemented."
            )
        elif sub_menu_choice == 4:
            raise UnsupportedOperationError(
                "Deleting products not yet implemented."
            )
        else:
            raise RuntimeError(
                "There are only four product actions; "
                "this cannot happen."
            )

    def _do_product_add(self) -> None:
        name = input("Enter product name and press RETURN: ").strip()
        if not name:
            raise ValueError("Product name cannot be empty.")

        raw_price = input("Enter product price and press RETURN: ").strip()
        try:
            price = float(raw_price)
        except ValueError:
            raise ValueError("Invalid input. Enter a valid price.") from None

        product = self._get_warehouse().add_product(
            name,
            price,
        )
        print(f"Added product {product.id}: {product.name} ({product.price})")

    def _do_customer_action(
        self,
        sub_menu_choice: int,
    ) -> None:
        if sub_menu_choice == 1:
            self._do_customer_list()
        elif sub_menu_choice == 2:
            raise UnsupportedOperationError(
                "Adding customers not yet implemented."
            )
        elif sub_menu_choice == 3:
            raise UnsupportedOperationError(
                "Updating customers not yet implemented."
            )
        elif sub_menu_choice == 4:
            raise UnsupportedOperationError(
                "Deleting customers not yet implemented."
            )
        else:
            raise RuntimeError(
                "There are only four customer actions; "
                "this cannot happen."
            )

    def _do_order_action(
        self,
        sub_menu_choice: int,
    ) -> None:
        if sub_menu_choice == 1:
            self._do_order_list()
        elif sub_menu_choice == 2:
            raise UnsupportedOperationError(
                "Adding orders not yet implemented."
            )
        elif sub_menu_choice == 3:
            raise UnsupportedOperationError(
                "Updating orders not yet implemented."
            )
        elif sub_menu_choice == 4:
            raise UnsupportedOperationError(
                "Deleting orders not yet implemented."
            )
        else:
            raise RuntimeError(
                "There are only four order actions; "
                "this cannot happen."
            )

    def _do_report_action(
        self,
        sub_menu_choice: int,
    ) -> None:
        warehouse = self._get_warehouse()

        if sub_menu_choice == 1:
            report = warehouse.generate_daily_revenue_report(
                Report.Type.DAILY_REVENUE
            )
        else:
            raise RuntimeError(
                "There is only one report action; "
                "this cannot happen."
            )

        self._do_report_export(report, sys.stdout)

    def _do_report_export(
        self,
        report: Report,
        out: TextIO,
    ) -> None:
        self._display_menu(self.EXPORT_OPTIONS)

        export_menu_choice = self._choose_menu_option(
            self.EXPORT_OPTIONS
        )

        if export_menu_choice == -1:
            return

        exporter = Exporter(report, out)
        exporter.export()

    def _do_product_list(self) -> None:
        products = list(self._get_warehouse().get_products())

        max_id_width = max(
            (len(str(product.id)) for product in products),
            default=0,
        )
        max_name_width = max(
            (len(product.name) for product in products),
            default=0,
        )
        max_price_width = max(
            (len(str(product.price)) for product in products),
            default=0,
        )

        for product in products:
            print(
                f"\t{product.id:>{max_id_width}}"
                f"\t\t{product.name:>{max_name_width}}"
                f"\t\t{product.price:>{max_price_width}}"
            )

    def _do_customer_list(self) -> None:
        customers = list(
            self._get_warehouse().get_customers()
        )

        max_id_width = max(
            (len(str(customer.id)) for customer in customers),
            default=0,
        )
        max_name_width = max(
            (len(customer.name) for customer in customers),
            default=0,
        )

        for customer in customers:
            print(
                f"\t{customer.id:>{max_id_width}}"
                f"\t\t{customer.name:>{max_name_width}}"
            )

    def _do_order_list(self) -> None:
        orders = list(self._get_warehouse().get_orders())

        max_id_width = max(
            (len(str(order.id)) for order in orders),
            default=0,
        )
        max_customer_name_width = max(
            (len(order.customer.name) for order in orders),
            default=0,
        )
        max_customer_id_width = max(
            (len(str(order.customer.id)) for order in orders),
            default=0,
        )
        max_total_price_width = max(
            (len(str(order.get_total_price())) for order in orders),
            default=0,
        )

        for order in orders:
            status = "pending" if order.pending else "fulfilled"
            total_price = order.get_total_price()

            print(
                f"\t{order.id:>{max_id_width}} {order.date}"
                f"\t\t"
                f"{order.customer.name:>{max_customer_name_width}} "
                f"({order.customer.id:>{max_customer_id_width}})"
                f"\t\t"
                f"{total_price:>{max_total_price_width}} "
                f"[{status}]"
            )

    def _get_warehouse(self) -> Warehouse:
        if self._warehouse is None:
            raise RuntimeError(
                "The warehouse has not been initialized."
            )

        return self._warehouse