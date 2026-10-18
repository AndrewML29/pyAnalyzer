import sys
from .parsers import parse_jsonl, parse_csv
from .analysis import Stats
from .report import generate_json_report

def main():
    if len(sys.argv) < 5:
        print("Использование: python -m streamstats analyze <INPUT> --format <csv|jsonl>")
        sys.exit(1)

    input_file = sys.argv[2]
    format_arg = ""
    for i, arg in enumerate(sys.argv):
        if arg == "--format" and i + 1 < len(sys.argv):
            format_arg = sys.argv[i+1]
            break

    if format_arg == "jsonl":
        parser = parse_jsonl
    elif format_arg == "csv":
        parser = parse_csv
    else:
        print("Ошибка: Поддерживаются только форматы csv и jsonl")
        sys.exit(1)

    stats = Stats()
    try:
        events = parser(input_file)
        for event in events:
            stats.update(event)
            
        print(generate_json_report(stats))

    except Exception as e:
        print(f"Критическая ошибка при обработке: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
