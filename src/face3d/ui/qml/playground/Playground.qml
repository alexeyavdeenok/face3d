
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../components"
import "../styles" as Styles

ApplicationWindow {
    visible: true

    width: 900
    height: 650

    title: "Face3D — Settings Playground"
    color: Styles.Colors.secondary

    ScrollView {
        anchors.fill: parent
        anchors.margins: 32

        ColumnLayout {
            width: 600
            spacing: 24

            Text {
                text: "Тестирование ячеек настроек"
                color: Styles.Colors.black
                font.pixelSize: 28
                font.bold: true
            }

            SettingsCell {
                title: "Настройка"
                variant: "switch"
                checked: true
            }

            SettingsCell {
                title: "Настройка"
                variant: "slider"
                sliderValue: 50
            }

            SettingsCell {
                title: "Настройка"
                variant: "combo"

                options: [
                    "Низкое",
                    "Среднее",
                    "Высокое"
                ]

                onOptionSelected: function(index) {
                    console.log("Выбран вариант:", index)
                }
            }
        }
    }
}
