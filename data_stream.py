
from typing import Any

from data_processor import (
    DataProcessor,
    NumericProcessor,
    TextProcessor,
    LogProcessor,
)


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._total_processed: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        if proc not in self._processors:
            self._processors.append(proc)
            self._total_processed[proc] = 0

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            processed = False

            for proc in self._processors:
                if proc.validate(element):
                    try:
                        proc.ingest(element)
                    except Exception as error:
                        print(
                            "DataStream error - "
                            f"Can't process element in stream: "
                            f"{element} ({error})"
                        )
                        processed = True
                        break

                    if isinstance(element, list):
                        count = len(element)
                    else:
                        count = 1

                    self._total_processed[proc] += count
                    processed = True
                    break

            if not processed:
                print(
                    "DataStream error - Can't process "
                    f"element in stream: {element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return

        for proc in self._processors:
            total = self._total_processed[proc]
            remaining = total - proc._rank

            name = (
                proc.__class__.__name__.replace(
                    "Processor", " Processor"
                )
            )

            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")

    data_stream = DataStream()
    data_stream.print_processors_stats()

    numeric = NumericProcessor()
    print("Registering Numeric Processor")
    data_stream.register_processor(numeric)

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]

    print(f"Send first batch of data on stream: {batch}")
    data_stream.process_stream(batch)
    data_stream.print_processors_stats()

    text = TextProcessor()
    logs = LogProcessor()

    print("Registering other data processors")
    data_stream.register_processor(text)
    data_stream.register_processor(logs)

    print("Send the same batch again")
    data_stream.process_stream(batch)
    data_stream.print_processors_stats()

    print(
        "Consume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )

    for _ in range(3):
        numeric.output()

    for _ in range(2):
        text.output()

    for _ in range(1):
        logs.output()

    data_stream.print_processors_stats()


if __name__ == "__main__":
    main()
