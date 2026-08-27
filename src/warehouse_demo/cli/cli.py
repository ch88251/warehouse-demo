import sys
from dataclasses import dataclass


@dataclass
class MenuOption:
  number: int
  label: str


class Cli:

  def __init__(
    self,
    args: list[str] | None = None,
    input_stream=sys.stdin,
    output_stream=sys.stdout,
  ):
    self.args = args or []
    self.in_stream = input_stream
    self.out = output_stream
    self.warehouse = None
    self.main_menu_options: list[MenuOption] = [
      MenuOption(1, "Manage Products"),
      MenuOption(2, "Manage Customers"),
      MenuOption(3, "Manage Orders"),
      MenuOption(5, "Export Reports"),
      MenuOption(4, "Exit")
    ]

    self.product_options: list[MenuOption] = [
      MenuOption(1, "List Products"),
      MenuOption(2, "Add Product"),
      MenuOption(3, "Update Product"),
      MenuOption(4, "Delete Product"),
      MenuOption(5, "Back to Previous Menu")
    ]

    self.customer_options: list[MenuOption] = [
      MenuOption(1, "List Customers"),
      MenuOption(2, "Add Customer"),
      MenuOption(3, "Update Customer"),
      MenuOption(4, "Delete Customer"),
      MenuOption(5, "Back to Previous Menu")
    ]

    self.order_options: list[MenuOption] = [
      MenuOption(1, "List Orders"),
      MenuOption(2, "Add Order"),
      MenuOption(3, "Update Order"),
      MenuOption(4, "Delete Order"),
      MenuOption(5, "Back to Previous Menu")
    ]

  def run(self):
    while True:
      self.display_main_menu()

  def display_main_menu(self):
    self.display_menu(self.main_menu_options, "Main Menu")

  def display_menu(self, options: list[MenuOption], title: str = ""):
    self.out.write(f"\n{title}\n")
    for option in options:
      self.out.write(f"{option.number}. {option.label}\n")
    self.out.write("\n")

  def choose_main_menu_option(self) -> int:
    line = self.in_stream.readline().strip()
    if not line:
      return 0
    
    try:
      value = int(line.strip())
    except ValueError:
      self.out.write("Error: Please enter a valid number\n")
      return 0

    if 1 <= value <= len(self.main_menu_options):
      return value

    self.out.write("Error: Please enter a valid option\n")
    return 0