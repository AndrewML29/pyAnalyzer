class StreamStatsError(Exception):
    '''Базовый класс для всех исключений нашего пакета streamstats'''
    pass
class UnsupportedFormatError(StreamStatsError):
    '''Вызывается, когда формат входного файла не поддерживается (не CSV и не JSONL)'''
    pass
class InvalidEventError(StreamStatsError):
    '''Вызывается, когда строка файла не соответствует структуре события'''
    pass
class InvalidTimestampError(StreamStatsError):
    '''Вызывается, когда временная метка события имеет неверный формат'''
    pass
class CLIConfigurationError(StreamStatsError):
    '''Вызывается при ошибках в аргументах командной строки'''
    pass