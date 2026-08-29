from io import TextIOBase
from typing import final


@final
class CsvReader:
    DEFAULT_SEPARATOR = ","

    def __init__(
        self,
        input_stream: TextIOBase,
        separator: str = DEFAULT_SEPARATOR,
    ) -> None:
        self._input_stream = input_stream
        self._separator = separator
        self._next_line: str | None = None
        self._end_of_file = False

    def has_next_row(self) -> bool:
        if self._next_line is not None:
            return True

        if self._end_of_file:
            return False

        line = self._input_stream.readline()

        if line == "":
            self._end_of_file = True
            return False

        self._next_line = line
        return True

    def next_row(self) -> list[str]:
        if not self.has_next_row():
            raise StopIteration("No more CSV rows")

        line = self._next_line
        self._next_line = None

        # Remove the newline without removing other whitespace.
        line = line.rstrip("\r\n")

        if not line.strip():
            return []

        return line.split(self._separator)