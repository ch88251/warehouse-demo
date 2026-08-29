from dataclasses import dataclass, field
from enum import Enum, auto
from typing import final


@final
@dataclass
class Report:
    class Type(Enum):
        DAILY_REVENUE = auto()

    labels: list[str] = field(default_factory=list)
    records: list[list[str]] = field(default_factory=list)

    def add_label(self, label: str) -> None:
        self.labels.append(label)

    def add_record(self, record: list[object]) -> None:
        self.records.append([str(value) for value in record])