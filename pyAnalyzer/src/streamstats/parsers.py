import json
import csv
import io
from datetime import datetime
from typing import Generator, Union
from .models import LogEvent
from .errors import InvalidEventError, InvalidTimestampError

def parse_jsonl(lines: Union[str, list[str]]) -> Generator[LogEvent, None, None]:
    """
    Потоково обрабатывает строки JSONL.
    Может принимать как путь к файлу (str), так и список строк (list[str]).
    """
    if isinstance(lines, str):
        # Мы открываем файл и выполняем цикл ВНУТРИ блока with
        with open(lines, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    data = json.loads(line)
                    ts = datetime.fromisoformat(data['timestamp'])
                    yield LogEvent(
                        timestamp=ts,
                        level=data['level'],
                        source=data['source'],
                        message=data['message']
                    )
                except json.JSONDecodeError:
                    print(f"Ошибка: Строка не является валидным JSON: {line}")
                except KeyError as e:
                    print(f"Ошибка: В строке не хватает ключа {e}")
                except ValueError as e:
                    print(f"Ошибка формата даты: {e}")
    else:
        # Если это список строк, используем виртуальный файл
        data_stream = io.StringIO("\n".join(lines))
        for line in data_stream:
            line = line.strip()
            if not line: continue
            try:
                data = json.loads(line)
                ts = datetime.fromisoformat(data['timestamp'])
                yield LogEvent(
                    timestamp=ts,
                    level=data['level'],
                    source=data['source'],
                    message=data['message']
                )
            except json.JSONDecodeError:
                print(f"Ошибка: Строка не является валидным JSON: {line}")
            except KeyError as e:
                print(f"Ошибка: В строке не хватает ключа {e}")
            except ValueError as e:
                print(f"Ошибка формата даты: {e}")

def parse_csv(lines: Union[str, list[str]]) -> Generator[LogEvent, None, None]:
    """
    Потоково обрабатывает строки CSV.
    Может принимать как путь к файлу (str), так и список строк (list[str]).
    """
    if isinstance(lines, str):
        with open(lines, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    ts = datetime.fromisoformat(row['timestamp'])
                    yield LogEvent(
                        timestamp=ts,
                        level=row['level'],
                        source=row['source'],
                        message=row['message']
                    )
                except KeyError as e:
                    print(f"Ошибка: В файле отсутствует обязательная колонка: {e}")
                except ValueError as e:
                    print(f"Ошибка формата даты: {e}")
    else:
        data_stream = io.StringIO("\n".join(lines))
        reader = csv.DictReader(data_stream)
        for row in reader:
            try:
                ts = datetime.fromisoformat(row['timestamp'])
                yield LogEvent(
                    timestamp=ts,
                    level=row['level'],
                    source=row['source'],
                    message=row['message']
                )
            except KeyError as e:
                print(f"Ошибка: В файле отсутствует обязательная колонка: {e}")
            except ValueError as e:
                print(f"Ошибка формата даты: {e}")
