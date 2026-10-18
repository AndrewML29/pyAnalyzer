import json
from .analysis import Stats

def generate_json_report(stats: Stats) -> str:
    """
    Формирует итоговый отчет в формате JSON на основе объекта статистики.
    """
    report = {
        "summary": {
            "total_events": stats.total_count,
            "first_seen": stats.first_timestamp.isoformat() if stats.first_timestamp else None,
            "last_seen": stats.last_timestamp.isoformat() if stats.last_timestamp else None,
        },
        "levels": stats.level_counts,
        "top_error_sources": stats.get_top_error_sources()
    }
    return json.dumps(report, indent=4)
