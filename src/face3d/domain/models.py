from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

import numpy as np
from numpy.typing import NDArray
from PIL import Image

from .enums import BackendKind, DepthMode, JobStatus


# --- Тип-алиасы ---------------------------------------------------------
FloatMap = NDArray[np.float32]     # [H, W]
Vertices = NDArray[np.float32]      # [N, 3]
Faces = NDArray[np.int32]           # [M, 3], индексы вершин
Colors = NDArray[np.uint8]          # [N, 3] RGB

# Что можно передать в качестве изображения
ImageInput = str | Path | Image.Image | NDArray[np.uint8]

# Callback для прогресса: (процент 0–100, человекочитаемая стадия)
ProgressFn = Callable[[int, str], None]


# --- Параметры ---------------------------------------------------------
@dataclass(frozen=True)
class ReconstructionConfig:
    """Параметры построения 3D-поверхности."""

    depth_mode: DepthMode = DepthMode.RELATIVE
    mesh_stride: int = 2
    max_depth_jump: float = 0.05
    focal_length_px: Optional[float] = None

    def __post_init__(self) -> None:
        if self.mesh_stride < 1:
            raise ValueError("mesh_stride должен быть >= 1")
        if self.max_depth_jump < 0:
            raise ValueError("max_depth_jump должен быть >= 0")
        if self.focal_length_px is not None and self.focal_length_px <= 0:
            raise ValueError("focal_length_px должен быть > 0")


# --- Результаты инференса -----------------------------------------------
@dataclass
class DepthMap:
    """Результат предсказания глубины."""

    values: FloatMap
    mode: DepthMode
    width: int
    height: int
    inference_time_ms: float = 0.0

    def validate(self) -> None:
        if self.values.ndim != 2:
            raise ValueError("Карта глубины должна иметь форму [H, W]")
        if self.values.shape != (self.height, self.width):
            raise ValueError("Размеры карты глубины не совпадают")
        if not np.isfinite(self.values).all():
            raise ValueError("Карта глубины содержит NaN или Inf")


@dataclass
class FaceMesh:
    """Треугольная 3D-сетка лица."""

    vertices: Vertices
    faces: Faces
    vertex_colors: Optional[Colors] = None
    coordinate_system: str = "camera"
    units: str = "relative"

    def validate(self) -> None:
        if self.vertices.ndim != 2 or self.vertices.shape[1] != 3:
            raise ValueError("vertices должны иметь форму [N, 3]")
        if self.faces.ndim != 2 or self.faces.shape[1] != 3:
            raise ValueError("faces должны иметь форму [M, 3]")
        if not np.isfinite(self.vertices).all():
            raise ValueError("Вершины содержат NaN или Inf")
        if len(self.faces):
            if self.faces.min() < 0:
                raise ValueError("Отрицательный индекс вершины")
            if self.faces.max() >= len(self.vertices):
                raise ValueError("Индекс вершины вне диапазона")
        if self.vertex_colors is not None:
            if self.vertex_colors.shape != self.vertices.shape:
                raise ValueError("Цвет должен быть задан для каждой вершины")


@dataclass
class ModelInfo:
    """Информация о модели/бэкенде для диагностики и UI."""

    name: str
    version: str
    backend: str
    device: str
    input_color_space: str = "RGB"
    task: str = "face_depth_estimation_and_reconstruction"


@dataclass
class ReconstructionResult:
    """Полный результат одного запуска реконструкции."""

    depth_map: DepthMap
    mesh: FaceMesh
    total_time_ms: float
    model_info: ModelInfo
    source_name: Optional[str] = None
    warnings: list[str] = field(default_factory=list)


# --- Доменная сущность для БД -------------------------------------------
@dataclass
class ReconstructionJob:
    """Задание на реконструкцию: то, что сохраняется и читается из БД."""

    id: str
    backend: BackendKind
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    source_names: list[str] = field(default_factory=list)
    error_message: Optional[str] = None
    result: Optional[ReconstructionResult] = None