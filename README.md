# Face3D Studio

Десктопное приложение для автоматической реконструкции лица человека по фотографиям
в текстурированную 3D-модель с корректной полигональной топологией.

**Статус:** ранний этап. Домен (контракты и DTO) зафиксирован, остальные слои —
в разработке. См. таблицу [«Что готово»](#что-готово).

---

## Оглавление

- [Зачем это нужно](#зачем-это-нужно)
- [Архитектура](#архитектура)
- [Структура проекта](#структура-проекта)
- [Что готово](#что-готово)
- [Быстрый старт](#быстрый-старт)
- [Как контрибьютить](#как-контрибьютить)
- [Документация](#документация)

---

## Зачем это нужно

Создание 3D-модели лица вручную — это дни работы 3D-художника: восстановление геометрии,
текстурирование, ретопология, удаление аксессуаров (очки, шляпы, маски) и восстановление
скрытых участков кожи. Продукт автоматизирует эти этапы и сокращает время до
**нескольких минут или часов**, возвращая готовую к интеграции в Unreal Engine, Unity
или VFX-конвейер модель.

Подробнее о целях и требованиях — в исходном описании продукта (см. `docs/`).

---

## Архитектура

Проект построен по **слоистой архитектуре** с правилом зависимостей:
`domain` ← `application` ← `infrastructure` / `ui`, плюс `composition` — единственное
место, где известны конкретные реализации.

Ключевая идея — **гибридный инференс**:

- основной режим — **удалённый** (тонкий клиент + ML-сервис в Docker на GPU);
- опциональный — **локальный** (in-process, для offline и приватности);
- выбор реализации — по конфигу, без переписывания UI и бизнес-логики.

Диаграммы (C4 L1–L2, UML классов, UML sequence) — в [`docs/architecture/`](docs/architecture/).

---

## Структура проекта

```
face3d/
├── src/face3d/
│   ├── domain/                    # контракты (ABC/Protocol) и DTO — ЗАФИКСИРОВАНО
│   │   ├── contracts.py
│   │   ├── models.py
│   │   ├── errors.py
│   │   └── enums.py
│   ├── application/               # оркестрация (в разработке)
│   ├── infrastructure/            # адаптеры: бэкенды, репозиторий, вьюеры
│   │   ├── inference/             #   RemoteBackend, LocalBackend (в разработке)
│   │   ├── persistence/           #   JobRepository (в разработке)
│   │   ├── viewing/               #   MeshViewer (в разработке)
│   │   └── export/                #   MeshExporter (в разработке)
│   ├── ui/                        # PySide6 (в разработке)
│   ├── config/                    # pydantic-settings (в разработке)
│   └── composition/               # DI-контейнер и точка входа (в разработке)
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── docs/
    └── architecture/              # диаграммы и README
```

---

## Что готово

| Модуль | Файл | Статус | Что внутри |
|---|---|---|---|
| Домен — перечисления | `domain/enums.py` | ✅ готово | `DepthMode`, `BackendKind`, `JobStatus` |
| Домен — ошибки | `domain/errors.py` | ✅ готово | `Face3DError` и наследники (`InvalidInputError`, `ModelNotLoadedError`, `InferenceError`, `CancelledError`, `PersistenceError`, `ExportError`) |
| Домен — DTO | `domain/models.py` | ✅ готово | `ReconstructionConfig`, `DepthMap`, `FaceMesh`, `ModelInfo`, `ReconstructionResult`, `ReconstructionJob`, тип-алиасы (`ImageInput`, `ProgressFn`, …) |
| Домен — контракты | `domain/contracts.py` | ✅ готово | `FaceReconstructionInterface`, `FaceDepthModelInterface`, `FaceMeshReconstructorInterface`, `JobRepository` (ABC); `MeshViewer`, `MeshExporter` (Protocol) |
| Application — сервисы | `application/*` | ⬜ не начато | `ReconstructionService`, `BackendRouter`, `ImagePreprocessor` |
| Infrastructure — remote-бэкенд | `infrastructure/inference/remote_backend.py` | ⬜ не начато | HTTP-клиент к Inference API |
| Infrastructure — local-бэкенд | `infrastructure/inference/local_backend.py` | ⬜ не начато | Опциональный in-process фасад |
| Infrastructure — репозиторий | `infrastructure/persistence/` | ⬜ не начато | `InMemoryJobRepository`, `SqlAlchemyJobRepository` |
| Infrastructure — вьюеры | `infrastructure/viewing/` | ⬜ не начато | `BrowserMeshViewer`, `QtMeshViewer` |
| UI | `ui/` | ⬜ не начато | PySide6: загрузка фото, прогресс, 3D-вьюер |
| Composition | `composition/` | ⬜ не начато | Сборка зависимостей, точка входа |

---

## Быстрый старт

### Требования

- Python **3.11+**
- [`uv`](https://docs.astral.sh/uv/) (рекомендуется) или `pip` + `venv`

### Установка (после появления `pyproject.toml`)

```bash
git clone git@github.com:alexeyavdeenok/face3d.git
cd face3d
uv venv
uv pip install -e ".[dev]"
```

> **Примечание:** `pyproject.toml` пока не создан. Появится вместе с первым
> рабочим модулем `application/`.

### Проверка домена

На этом этапе проект ещё не запускается как приложение, но контракты можно
импортировать и проверить типы:

```bash
python -c "from face3d.domain.contracts import FaceReconstructionInterface; print('OK')"
```

---

## Как контрибьютить

### Правило зависимостей

- `domain/` **не импортирует** ничего из `application/`, `infrastructure/`, `ui/`, `composition/`.
- `application/` зависит **только** от `domain/`.
- `infrastructure/` реализует контракты из `domain/`.
- `ui/` зависит от `domain/` и `application/`, но **не** от `infrastructure/`.
- `composition/` — единственное место, где известны конкретные классы.

Это правило будет проверяться линтером в CI (`import-linter`), но соблюдать его
нужно уже сейчас.

### Соглашения

- **Импорты:** абсолютные (`from face3d.domain.contracts import …`).
- **Стиль:** `ruff` (line-length 100), `mypy --strict` для `domain/` и `application/`.
- **Коммиты:** [Conventional Commits](https://www.conventionalcommits.org/) —
  `feat:`, `fix:`, `docs:`, `refactor:`, `test:`.
- **Ветки:** `feat/<краткое-имя>`, `fix/<краткое-имя>`.

### Как связаться с ML-разработчиком

Контракты `FaceDepthModelInterface` и `FaceMeshReconstructorInterface` — зона
ML-разработчика. Фасад `FaceReconstructionInterface` реализуется в двух вариантах:
`RemoteBackend` (наш код) и `LocalBackend` (склейка двух нижних контрактов).

Wire-контракт между клиентом и ML-сервисом (OpenAPI) — **пока не написан**.
Это следующий приоритет для коммуникации с ML.

---

## Документация

| Документ | Что внутри |
|---|---|
| [`docs/architecture/`](docs/architecture/) | C4 L1–L2, UML классов, UML sequence, README по рендерингу |
| `docs/architecture/c4-l1-context.puml` | Границы продукта и внешние системы |
| `docs/architecture/c4-l2-container.puml` | Контейнеры и зоны ответственности (клиент / ML) |
| `docs/architecture/uml-class-domain.puml` | Контракты и DTO домена |
| `docs/architecture/seq-reconstruct-remote.puml` | Сценарий remote-реконструкции |

---

## Лицензия

TBD.