
from typing import Any, Protocol

from data_processor import (
    DataProcessor,
    NumericProcessor,
    TextProcessor,
    LogProcessor,
)


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values: list[str] = []

        for _, value in data:
            if any(char in value for char in ',\"\n\r'):
                value = '"' + value.replace('"', '""') + '"'
            values.append(value)

        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        entries: list[str] = []

        for rank, value in data:
            escaped = self._escape_string(value)
            entries.append(f'"item_{rank}": "{escaped}"')

        print("JSON Output:")
        print("{" + ", ".join(entries) + "}")

    @staticmethod
    def _escape_string(value: str) -> str:
        escaped = value.replace("\\", "\\\\")
        escaped = escaped.replace('"', '\\"')
        escaped = escaped.replace("\n", "\\n")
        escaped = escaped.replace("\r", "\\r")
        escaped = escaped.replace("\t", "\\t")

        result: list[str] = []
        for char in escaped:
            if ord(char) < 32:
                result.append(f"\\u{ord(char):04x}")
            else:
                result.append(char)

        return "".join(result)


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._total_processed: dict[DataProcessor, int] = {}
        self._pending: dict[DataProcessor, list[tuple[int, str]]] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        if proc not in self._processors:
            self._processors.append(proc)
            self._total_processed[proc] = 0
            self._pending[proc] = []

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            processed = False

            for proc in self._processors:
                if not proc.validate(element):
                    continue

                try:
                    proc.ingest(element)
                except (TypeError, ValueError) as error:
                    print(f"DataStream error: {error}")
                    processed = True
                    break

                count = len(element) if isinstance(element, list) else 1
                start_rank = self._total_processed[proc]

                new_values = proc._data[-count:] if count else []

                for offset, value in enumerate(new_values):
                    self._pending[proc].append(
                        (start_rank + offset, value)
                    )

                self._total_processed[proc] += count
                processed = True
                break

            if not processed:
                print(f"DataStream error: no processor for {element!r}")

    def output_pipeline(
        self,
        nb: int,
        plugin: ExportPlugin,
    ) -> None:
        if nb <= 0:
            return

        for proc in self._processors:
            output_data: list[tuple[int, str]] = []
            pending = self._pending[proc]
            count = min(nb, len(pending))

            for _ in range(count):
                rank, value = pending.pop(0)
                proc.output()
                output_data.append((rank, value))

            if output_data:
                plugin.process_output(output_data)

    def print_processors_stats(self) -> None:
        if not self._processors:
            print("No processor found, no data")
            return

        print("== DataStream statistics ==")

        for proc in self._processors:
            name = proc.__class__.__name__.replace(
                "Processor", " Processor"
            )
            total = self._total_processed[proc]
            remaining = len(self._pending[proc])

            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")

    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    first_batch: list[Any] = [
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

    print(f"Send first batch of data on stream: {first_batch}")
    stream.process_stream(first_batch)
    stream.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin:")
    csv_plugin = CSVExportPlugin()
    stream.output_pipeline(3, csv_plugin)
    stream.print_processors_stats()

    second_batch: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash",
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]

    print(f"Send another batch of data: {second_batch}")
    stream.process_stream(second_batch)
    stream.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    json_plugin = JSONExportPlugin()
    stream.output_pipeline(5, json_plugin)
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
