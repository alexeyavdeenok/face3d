
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

# Устанавливаем стиль до создания приложения и загрузки QML
QQuickStyle.setStyle("Basic")

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()

qml_path = (
    Path(__file__).parent
    / "src"
    / "face3d"
    / "ui"
    / "qml"
    / "playground"
    / "Playground.qml"
)

engine.load(qml_path.as_uri())

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
