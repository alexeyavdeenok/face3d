
import QtQuick
import QtQuick.Controls
import QtQuick.Effects

import "../styles" as Styles

Item {
    id: root

    // Основные свойства
    property string title: "Настройка"
    property string variant: "switch"

    // Переключатель
    property bool checked: true

    // Слайдер
    property real sliderValue: 85
    property real sliderFrom: 0
    property real sliderTo: 100

    // Выпадающий список
    property var options: ["Первый", "Второй", "Третий"]
    property int selectedIndex: 0

    // События
    signal optionSelected(int index)

    // Размеры
    implicitWidth: 280

    implicitHeight: variant === "slider" ? 140 : 120

    // Фон карточки
    Rectangle {
        anchors.fill: parent

        radius: 16
        color: Styles.Colors.white

        layer.enabled: true

        layer.effect: MultiEffect {
            shadowEnabled: true
            shadowColor: Styles.Colors.shadow
            shadowHorizontalOffset: 2
            shadowVerticalOffset: 4
            shadowBlur: 0.25
            shadowOpacity: 1.0
        }
    }

    // Заголовок
    Text {
        id: titleText

        text: root.title
        color: Styles.Colors.black

        font.pixelSize: 20

        anchors.verticalCenter:
            root.variant === "slider"
            ? undefined
            : parent.verticalCenter

        anchors.top:
            root.variant === "slider"
            ? parent.top
            : undefined

        anchors.topMargin: 28

        anchors.horizontalCenter:
            root.variant === "slider"
            ? parent.horizontalCenter
            : undefined

        anchors.left:
            root.variant !== "slider"
            ? parent.left
            : undefined

        anchors.leftMargin: 24
    }

    // Переключатель
    Item {
        id: switchControl

        visible: root.variant === "switch"

        width: 56
        height: 32

        anchors.right: parent.right
        anchors.rightMargin: 24
        anchors.verticalCenter: parent.verticalCenter

        Rectangle {
            anchors.fill: parent

            radius: height / 2

            color: root.checked
                   ? Styles.Colors.primary
                   : Styles.Colors.controlInactive

            Behavior on color {
                ColorAnimation {
                    duration: 150
                }
            }

            Rectangle {
                width: 26
                height: 26

                radius: width / 2
                color: Styles.Colors.white

                anchors.verticalCenter: parent.verticalCenter

                x: root.checked
                   ? parent.width - width - 3
                   : 3

                Behavior on x {
                    NumberAnimation {
                        duration: 150
                        easing.type: Easing.OutCubic
                    }
                }
            }
        }

        MouseArea {
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor

            onClicked: root.checked = !root.checked
        }
    }

    // Слайдер
    Slider {
        id: sliderControl

        visible: root.variant === "slider"

        from: root.sliderFrom
        to: root.sliderTo
        value: root.sliderValue

        padding: 0

        anchors.left: parent.left
        anchors.right: parent.right

        anchors.leftMargin: 24
        anchors.rightMargin: 24

        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: 30

        height: 24

        background: Rectangle {
            x: 0
            y: (sliderControl.height - height) / 2

            width: sliderControl.width
            height: 5

            radius: height / 2

            color: Styles.Colors.controlInactive

            Rectangle {
                width: sliderControl.visualPosition * parent.width
                height: parent.height

                radius: parent.radius

                color: Styles.Colors.primary
            }
        }

        handle: Rectangle {
            x: sliderControl.visualPosition
               * (sliderControl.width - width)

            y: (sliderControl.height - height) / 2

            width: 20
            height: 20

            radius: width / 2

            color: Styles.Colors.primary
        }

        onMoved: root.sliderValue = value
    }

    // Выпадающий список
    ComboBox {
        id: comboControl

        visible: root.variant === "combo"

        model: root.options
        currentIndex: root.selectedIndex

        width: 110
        height: 40

        anchors.right: parent.right
        anchors.rightMargin: 24
        anchors.verticalCenter: parent.verticalCenter

        background: Rectangle {
            color: Styles.Colors.secondary
            radius: 10
        }

        contentItem: Text {
            text: comboControl.displayText

            color: Styles.Colors.primary
            font.pixelSize: 12

            verticalAlignment: Text.AlignVCenter
            leftPadding: 10

            elide: Text.ElideRight
        }

        onActivated: function(index) {
            root.selectedIndex = index
            root.optionSelected(index)
        }
    }
}
