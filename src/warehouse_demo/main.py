import sys

from warehouse_demo.cli.cli import Cli


class Main:

    def run(self):
        # display the main menu
        print("Welcome to the Warehouse Management System!")
        Cli().run()


if __name__ == "__main__":
    try:
        Main().run()
    except KeyboardInterrupt:
        print("\nApplication interrupted.", file=sys.stderr)
        raise SystemExit(130)
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}", file=sys.stderr)
        raise SystemExit(1)