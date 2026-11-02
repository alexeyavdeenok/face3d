from __future__ import annotations


class Face3DError(Exception):
    """Базовое исключение домена. Всё остальное наследуется от него."""


class InvalidInputError(Face3DError):
    """Некорректные входные данные: битый файл, неподдерживаемый формат,
    пустой набор изображений и т.п."""


class ModelNotLoadedError(Face3DError):
    """Бэкенд не готов: веса не загружены, сервис недоступен."""


class InferenceError(Face3DError):
    """Ошибка во время инференса: упал Torch, вернулся битый ответ,
    сервер ответил 5xx и т.п."""


class CancelledError(Face3DError):
    """Операция отменена пользователем (через threading.Event)."""


class PersistenceError(Face3DError):
    """Ошибка сохранения/чтения результата (БД, файловая система)."""


class ExportError(Face3DError):
    """Ошибка экспорта меша в файл (GLB/PLY/…)."""