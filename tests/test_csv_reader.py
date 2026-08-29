from io import StringIO

import pytest

from warehouse_demo.warehouse.csv_reader import CsvReader


def test_has_next_row_true_when_row_available_and_not_consumed() -> None:
    reader = CsvReader(StringIO("a,b\n"))

    assert reader.has_next_row() is True
    assert reader.has_next_row() is True


def test_next_row_consumes_cached_row_and_reads_following_rows() -> None:
    reader = CsvReader(StringIO("1,2\n3,4\n"))

    assert reader.has_next_row() is True
    assert reader.next_row() == ["1", "2"]
    assert reader.next_row() == ["3", "4"]


def test_next_row_raises_stop_iteration_at_end_of_file() -> None:
    reader = CsvReader(StringIO(""))

    assert reader.has_next_row() is False
    with pytest.raises(StopIteration, match="No more CSV rows"):
        reader.next_row()


def test_next_row_strips_crlf_newline_only() -> None:
    reader = CsvReader(StringIO("  x , y  \r\n"))

    assert reader.next_row() == ["  x ", " y  "]


def test_next_row_returns_empty_list_for_blank_line() -> None:
    reader = CsvReader(StringIO("   \n"))

    assert reader.next_row() == []


def test_next_row_uses_custom_separator() -> None:
    reader = CsvReader(StringIO("alpha|beta|gamma\n"), separator="|")

    assert reader.next_row() == ["alpha", "beta", "gamma"]
