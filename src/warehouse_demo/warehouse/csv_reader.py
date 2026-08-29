import csv
from io import TextIOBase
from typing import final


@final
class CsvReader:
    def __init__(
        self,
        input_stream: TextIOBase,
        separator: str = ",",
    ) -> None:
        self._reader = csv.reader(input_stream, delimiter=separator)
        self._rows = iter(self._reader)
        self._next_row: list[str] | None = None
        self._end_of_file = False

    def has_next_row(self) -> bool:
        if self._next_row is not None:
            return True

        if self._end_of_file:
            return False

        try:
            self._next_row = next(self._rows)
            return True
        except StopIteration:
            self._end_of_file = True
            return False

    def next_row(self) -> list[str]:
        if not self.has_next_row():
            raise StopIteration("No more CSV rows")

        row = self._next_row
        self._next_row = None

        # Preserve historical behavior: whitespace-only lines are treated as empty rows.
        if row is not None and len(row) == 1 and row[0].strip() == "":
            return []

        return row