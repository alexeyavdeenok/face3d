from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol, runtime_checkable

from .models import (
    DepthMap,
    FaceMesh,
    ImageInput,
    ModelInfo,
    ProgressFn,
    ReconstructionConfig,
    ReconstructionJob,
    ReconstructionResult,
)


# =======================================================================
# Порты инференса
# =======================================================================
class FaceDepthModelInterface(ABC):
    """Контракт модели оценки глубины лица.

    Реализация может быть локальной (Torch в процессе) или удалённой
    (обёртка над HTTP). Домен об этом не знает.
    """

    @abstractmethod
    def load_weights(self, path: str | Path) -> None:
        """Загрузить обученные веса."""

    @abstractmethod
    def predict_depth(
        self,
        image: ImageInput,
        *,
        cancel: threading.Event | None = None,
    ) -> DepthMap:
        """Предсказать карту глубины для одного изображения."""

    @abstractmethod
    def is_ready(self) -> bool:
        """Загружены ли веса и готов ли бэкенд к работе."""

    @abstractmethod
    def unload(self) -> None:
        """Освободить ресурсы (VRAM, RAM, соединения)."""

    @abstractmethod
    def get_info(self) -> ModelInfo:
        """Метаданные модели: имя, версия, устройство, backend."""


class FaceMeshReconstructorInterface(ABC):
    """Контракт алгоритма построения 3D-сетки по карте глубины."""

    @abstractmethod
    def reconstruct(
        self,
        image: ImageInput,
        depth_map: DepthMap,
        config: ReconstructionConfig,
        *,
        cancel: threading.Event | None = None,
    ) -> FaceMesh:
        """Построить треугольную сетку лица."""

    @abstractmethod
    def export_mesh(
        self,
        mesh: FaceMesh,
        path: str | Path,
    ) -> Path:
        """Экспортировать сетку в файл (GLB, PLY, …)."""


class FaceReconstructionInterface(ABC):
    """Единый порт инференса: local и remote реализации взаимозаменяемы.

    Именно с этим интерфейсом работает ``ReconstructionService``
    в слое ``application/``. UI и ``application/`` не знают,
    какая реализация стоит за портом.
    """

    @abstractmethod
    def load_weights(self, path: str | Path) -> None:
        """Загрузить веса (для локального бэкенда — с диска,
        для удалённого — например, проверить доступность сервера
        и его версию модели)."""

    @abstractmethod
    def reconstruct(
        self,
        image: ImageInput,
        config: ReconstructionConfig | None = None,
        *,
        progress: ProgressFn | None = None,
        cancel: threading.Event | None = None,
    ) -> ReconstructionResult:
        """Полный пайплайн: изображение → depth → mesh → результат.

        ``progress`` вызывается по стадиям (0–100, текст стадии).
        ``cancel`` проверяется между стадиями; при установке флага
        реализация обязана бросить ``domain.errors.CancelledError``.
        """

    @abstractmethod
    def is_ready(self) -> bool:
        """Готов ли бэкенд принимать запросы."""

    @abstractmethod
    def unload(self) -> None:
        """Освободить ресурсы."""

    @abstractmethod
    def get_info(self) -> ModelInfo:
        """Информация о модели/бэкенде для UI и логов."""


# =======================================================================
# Порт персистентности (для БД)
# =======================================================================
class JobRepository(ABC):
    """Хранилище заданий на реконструкцию.

    Реализация может быть in-memory, SQLite, PostgreSQL — сервису
    в ``application/`` это безразлично.
    """

    @abstractmethod
    def save(self, job: ReconstructionJob) -> None:
        """Создать или обновить задание (upsert по ``job.id``)."""

    @abstractmethod
    def get(self, job_id: str) -> ReconstructionJob | None:
        """Вернуть задание по id или ``None``, если его нет."""

    @abstractmethod
    def list_recent(self, limit: int = 20) -> list[ReconstructionJob]:
        """Последние задания — для панели истории в UI."""

    @abstractmethod
    def delete(self, job_id: str) -> None:
        """Удалить задание (например, вместе с тяжёлым результатом)."""


# =======================================================================
# Периферийные порты (Protocol — адаптер не обязан наследоваться)
# =======================================================================
@runtime_checkable
class MeshViewer(Protocol):
    """Показ 3D-меша в UI.

    ``BrowserMeshViewer`` и ``QtMeshViewer`` реализуют этот протокол
    структурно. UI вызывает ``show`` / ``update`` / ``close``
    и не знает, какая именно реализация активна.
    """

    def show(self, mesh: FaceMesh, *, title: str = "") -> None: ...

    def update(self, mesh: FaceMesh) -> None: ...

    def close(self) -> None: ...


class MeshExporter(Protocol):
    """Экспорт меша в файл (GLB, PLY, …)."""

    def export_mesh(self, mesh: FaceMesh, path: str | Path) -> Path: ...