from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEvent:
    """
    Модель одного события лога.
    Хранит основные данные о событии: время, уровень, источник и сообщение.
    """
    timestamp: datetime
    level: str
    source: str
    message: str

    def is_error(self) -> bool:
        """Проверяет, является ли уровень лога критическим (ERROR или CRITICAL)."""
        return self.level in ("ERROR", "CRITICAL")
