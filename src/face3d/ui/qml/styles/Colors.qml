
pragma Singleton
import QtQuick

QtObject {
    // Основная палитра
    readonly property color primary: "#627EFC"
    readonly property color secondary: "#ECEFFE"

    // Ошибки и удаление
    readonly property color danger: "#FE575A"
    readonly property color dangerStrong: "#E42529"
    readonly property color dangerTransparent: "#5EFE575A"

    // Успешные операции
    readonly property color success: "#029727"
    readonly property color successLight: "#B6FFA0"
    readonly property color successTransparent: "#4FB6FFA0"

    // Нейтральные цвета
    readonly property color white: "#FFFFFF"
    readonly property color black: "#000000"

    // Цвета элементов управления
    readonly property color controlInactive: "#D8DEFF"
    readonly property color separator: primary

    // Тень: чёрный, непрозрачность 25%
    readonly property color shadow: "#40000000"
}
