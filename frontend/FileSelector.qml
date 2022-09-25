// main.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Dialogs

ApplicationWindow {
    id: fileSelectorWindow
    width: 800
    height: 400
    visible: true

    TextField {
        id: fileLocation
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: 15
        placeholderText: qsTr("Hello, World!")
        width: 600
    }

    Button {
        id: openDialogButton
        text: "Confirm"
        anchors.centerIn: parent

        onClicked:function() {
            foo.set_file_name(fileLocation.text)
            foo.trigger_analysis(fileLocation.text, 5)
            fileSelectorWindow.visible = false
        }
    }

    Button {
        id: submitButton
        text: "Select File"
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 15

        onClicked:function() {
            fileDialog.open();
        }
    }

    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        nameFilters: ["Video Files (*.mp4 *.mpeg *.avi *.xvid)"]
        onAccepted:function() {
            fileLocation.text = Qt.resolvedUrl(fileDialog.selectedFile)
            fileDialog.close()
        }
    }
}