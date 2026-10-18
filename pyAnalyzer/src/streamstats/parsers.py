import json
import csv
from datetime import datetime
from typing import Generator
from .models import LogEvent
from .errors import InvalidEventError, InvalidTimestampError

def parse_jsonl(file_path: str) -> Generator[LogEvent, None, None]:
    """
    Потоково читает файл в формате JSONL.
    Каждая строка должна быть валидным JSON-объектом.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
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

def parse_csv(file_path: str) -> Generator[LogEvent, None, None]:
    """
    Потоково читает файл в формате CSV с заголовками.
    Ожидает колонки: timestamp, level, source, message.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
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
