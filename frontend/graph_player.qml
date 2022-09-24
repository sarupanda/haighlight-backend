import QtQuick 2.5
import QtQuick.Controls 2.5
import QtMultimedia

ApplicationWindow {
    visible:true
    width:600
    height:400
    title:"Play Video"

    MediaPlayer {
        id:player
        source:"../test_low_res.mp4"
        videoOutput:videoOutput
        audioOutput:audioOutput
    }

    VideoOutput {
        id:videoOutput
        anchors.fill:parent
    }

    AudioOutput {
        id:audioOutput
        volume:volumeSlider.value
    }

    Component.onCompleted: {
        player.play()
    }

    Slider {
        id:volumeSlider
        anchors.top:parent.top
        anchors.right:parent.right
        anchors.margins:20
        orientation:Qt.Vertical
        value:0.5
    }

    Slider {
        id:progressSlider
        width:parent.width
        anchors.bottom:parent.bottom
        enabled:player.seekable
        value:player.duration > 0 ? player.position / player.duration : 0
        
        onMoved:function() {
            player.position = player.duration * progressSlider.position
        }
    }
}