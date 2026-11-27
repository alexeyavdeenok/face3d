
import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: window

    visible: true

    width: 900
    height: 750

    minimumWidth: 600
    minimumHeight: 500

    title: "Face3D — Photo Preview Playground"

    PhotoPreviewPlayground {
        anchors.fill: parent
    }
}
