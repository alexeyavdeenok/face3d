# Архитектурные диаграммы

| Файл | Что показывает | Аудитория |
|---|---|---|
| `c4-l1-context.puml` | Границы продукта и внешние системы | вся команда |
| `c4-l2-container.puml` | Контейнеры, зоны ответственности (клиент / ML) | вся команда + ML |
| `uml-class-domain.puml` | Контракты и DTO домена | ML-разработчик |
| `seq-reconstruct-remote.puml` | Сценарий remote-реконструкции | вся команда |

## Как рендерить

### VS Code
Установить расширение **PlantUML** (jebbs), открыть `.puml` → `Cmd+Shift+P` → `PlantUML: Preview Current Diagram`.

### CLI
```bash
brew install plantuml
plantuml -tsvg docs/architecture/*.puml