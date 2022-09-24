// CustomButton.qml
import QtQuick
import QtQuick.Controls

Button {
    id: control

    background: Rectangle {
        radius: width / 2
        implicitWidth: 36
        implicitHeight: 36
        color: control.pressed ? "#ccc" : "#eee"
    }
}