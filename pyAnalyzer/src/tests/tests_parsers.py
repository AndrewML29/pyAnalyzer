import pytest
from src.streamstats.parsers import parse_jsonl, parse_csv
from src.streamstats.models import LogEvent

def test_parse_jsonl_valid():
    """Проверка парсинга валидной строки JSONL."""
    test_data = [
        '{"timestamp": "2023-10-15T10:00:00", "level": "INFO", "source": "test-src", "message": "test-msg"}'
    ]
    events = list(parse_jsonl(test_data))
    
    assert len(events) == 1
    assert isinstance(events[0], LogEvent)
    assert events[0].level == "INFO"
    assert events[0].source == "test-src"
    assert events[0].timestamp.year == 2023

def test_parse_jsonl_invalid_format():
    """Проверка, что битый JSON не вызывает падение программы."""
    test_data = ['{битая_строка_без_кавычек}']
    # Функция должна просто напечатать ошибку и вернуть пустой генератор
    events = list(parse_jsonl(test_data))
    assert len(events) == 0

def test_parse_csv_valid():
    """Проверка парсинга валидной строки CSV."""
    test_data = [
        "timestamp,level,source,message\n2023-10-16T09:00:00,DEBUG,worker-1,msg"
    ]
    events = list(parse_csv(test_data))
    
    assert len(events) == 1
    assert isinstance(events[0], LogEvent)
    assert events[0].level == "DEBUG"
    assert events[0].source == "worker-1"

def test_parse_csv_missing_column():
    """Проверка, что отсутствие колонки не роняет парсер."""
    test_data = [
        "timestamp,level\n2023-10-16T09:00:00,DEBUG" # нет колонки source
    ]
    # В нашем коде мы просто выводим ошибку KeyError, поэтому генератор будет пуст
    events = list(parse_csv(test_data))
    assert len(events) == 0
