from __future__ import annotations

from enum import Enum


class DepthMode(str, Enum):
    """Режим карты глубины."""

    RELATIVE = "relative"
    METRIC = "metric"


class BackendKind(str, Enum):
    """Где выполняется инференс."""

    LOCAL = "local"
    REMOTE = "remote"


class JobStatus(str, Enum):
    """Статус задания на реконструкцию (для БД и UI)."""

    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"