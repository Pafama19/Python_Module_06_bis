
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError("No data available")

        rank = self._rank
        data = self._data.pop(0)
        self._rank += 1

        return rank, data


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if type(data) in (int, float):
            return True

        if isinstance(data, list):
            return all(
                type(item) in (int, float)
                for item in data
            )

        return False

    def ingest(
        self,
        data: int | float | list[int | float],
    ) -> None:  # type: ignore[override]
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if isinstance(data, list):
            converted = [str(item) for item in data]
        else:
            converted = [str(data)]

        self._data.extend(converted)


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)

        return False

    def ingest(self, data: str | list[str]) -> None:
        # type: ignore[override]
        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, list):
            converted = list(data)
        else:
            converted = [data]

        self._data.extend(converted)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(key, str)
                and isinstance(value, str)
                for key, value in data.items()
            )

        if isinstance(data, list):
            return all(
                isinstance(item, dict)
                and all(
                    isinstance(key, str)
                    and isinstance(value, str)
                    for key, value in item.items()
                )
                for item in data
            )

        return False

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]],
    ) -> None:  # type: ignore[override]
        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, dict):
            entries = [data]
        else:
            entries = data

        converted: list[str] = []

        for entry in entries:
            if (
                "log_level" in entry
                and "log_message" in entry
            ):
                message = (
                    f"{entry['log_level']}: "
                    f"{entry['log_message']}"
                )
            else:
                message = str(entry)

            converted.append(message)

        self._data.extend(converted)


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    numeric = NumericProcessor()
    print("Testing Numeric Processor...")
    print(
        f"Trying to validate input '42': "
        f"{numeric.validate(42)}"
    )
    print(
        f"Trying to validate input 'Hello': "
        f"{numeric.validate('Hello')}"
    )

    print(
        "Test invalid ingestion of string "
        "'foo' without prior validation:"
    )
    try:
        numeric.ingest("foo")
    except ValueError as error:
        print(f"Got exception: {error}")

    numbers = [1, 2, 3, 4, 5]
    print(f"Processing data: {numbers}")
    numeric.ingest(numbers)

    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    text = TextProcessor()
    print("Testing Text Processor...")
    print(
        f"Trying to validate input '42': "
        f"{text.validate(42)}"
    )

    words = ["Hello", "Nexus", "World"]
    print(f"Processing data: {words}")
    text.ingest(words)

    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    logs = LogProcessor()
    print("Testing Log Processor...")
    print(
        f"Trying to validate input 'Hello': "
        f"{logs.validate('Hello')}"
    )

    entries = [
        {
            "log_level": "NOTICE",
            "log_message": "Connection to server",
        },
        {
            "log_level": "ERROR",
            "log_message": "Unauthorized access!!",
        },
    ]

    print(f"Processing data: {entries}")
    logs.ingest(entries)

    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = logs.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
