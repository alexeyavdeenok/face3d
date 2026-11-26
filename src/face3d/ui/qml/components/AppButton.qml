
import QtQuick
import QtQuick.Controls
import QtQuick.Effects

import "../styles" as Styles

Button {
    id: root

    // Варианты оформления
    property string variant: "primary"

    // Цветовая палитра
    readonly property color backgroundColor:
        variant === "primary"
            ? Styles.Colors.primary
            : Styles.Colors.secondary

    readonly property color foregroundColor:
        variant === "primary"
            ? Styles.Colors.secondary
            : Styles.Colors.primary

    // Размеры
    implicitWidth: 280
    implicitHeight: 72

    // Типографика
    font.pixelSize: 14
    font.weight: Font.DemiBold

    // Фон кнопки
    background: Rectangle {
        id: buttonBackground

        radius: 16
        color: root.backgroundColor

        layer.enabled: true

        layer.effect: MultiEffect {
            shadowEnabled: true
            shadowColor: "#40000000"
            shadowHorizontalOffset: 2
            shadowVerticalOffset: 4
            shadowBlur: 0.25
            shadowOpacity: 1.0
        }

        Behavior on color {
            ColorAnimation {
                duration: 120
            }
        }
    }

    // Текст кнопки
    contentItem: Text {
        text: root.text
        color: root.foregroundColor

        font: root.font

        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    // Состояние доступности
    opacity: enabled ? 1.0 : 0.5
}
