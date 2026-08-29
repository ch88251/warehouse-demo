from typing import TextIO, final

from .report import Report


@final
class Exporter:
    BORDER = "*"
    LEFT_BORDER = BORDER + " "
    RIGHT_BORDER = " " + BORDER
    SEPARATOR = " | "

    def __init__(self, report: Report, out: TextIO) -> None:
        self._report = report
        self._out = out
        self._widths = self._calculate_widths()

        self._total_width = (
            sum(self._widths)
            + len(self.LEFT_BORDER)
            + len(self.SEPARATOR) * (len(self._report.labels) - 1)
            + len(self.RIGHT_BORDER)
        )

    def export(self) -> None:
        self._print_border()
        self._print_strings(self._report.labels)
        self._print_border()

        for record in self._report.records:
            self._print_strings(record)

        self._print_border()

    def _calculate_widths(self) -> list[int]:
        widths = [len(label) for label in self._report.labels]

        for record in self._report.records:
            for index in range(len(widths)):
                widths[index] = max(
                    widths[index],
                    len(record[index]),
                )

        return widths

    def _print_border(self) -> None:
        print(self.BORDER * self._total_width, file=self._out)

    def _print_strings(self, strings: list[str]) -> None:
        formatted_values = (
            f"{value:>{self._widths[index]}}"
            for index, value in enumerate(strings)
        )

        line = (
            self.LEFT_BORDER
            + self.SEPARATOR.join(formatted_values)
            + self.RIGHT_BORDER
        )

        print(line, file=self._out)