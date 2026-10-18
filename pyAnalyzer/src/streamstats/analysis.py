from datetime import datetime
from typing import Dict, List
from .models import LogEvent

class Stats:
    """
    Класс для агрегации статистики событий лога.
    Поддерживает подсчет общего количества, уровней, источников и временных меток.
    """
    def __init__(self):
        self.total_count: int = 0
        self.level_counts: Dict[str, int] = {}
        self.source_counts: Dict[str, int] = {}
        self.error_sources: Dict[str, int] = {}
        self.first_timestamp: datetime = None
        self.last_timestamp: datetime = None

    def update(self, event: LogEvent):
        """Обновляет счетчики на основе одного события."""
        self.total_count += 1
        self.level_counts[event.level] = self.level_counts.get(event.level, 0) + 1
        self.source_counts[event.source] = self.source_counts.get(event.source, 0) + 1
        
        if event.is_error():
            self.error_sources[event.source] = self.error_sources.get(event.source, 0) + 1
            
        if self.first_timestamp is None or event.timestamp < self.first_timestamp:
            self.first_timestamp = event.timestamp
        if self.last_timestamp is None or event.timestamp > self.last_timestamp:
            self.last_timestamp = event.timestamp

    def get_top_error_sources(self, limit: int = 5) -> Dict[str, int]:
        """
        Возвращает словарь топ-N источников ошибок.
        Ключ — имя источника, значение — количество ошибок.
        """
        # Сортируем и превращаем в словарь
        sorted_errors = sorted(self.error_sources.items(), key=lambda x: x[1], reverse=True)
        # Создаем словарь только для первых N элементов
        return {source: count for source, count in sorted_errors[:limit]}

