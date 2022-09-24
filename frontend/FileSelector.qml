// main.qml
import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: window
    visible: true

    CustomButton {
        text: "Button"
        anchors.centerIn: parent
    }
}