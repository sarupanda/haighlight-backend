import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtCharts
import QtMultimedia

ApplicationWindow {
    visible: true
    width: 600
    height: 400
    title: "Play Video"

    MediaPlayer {
        id:player
        videoOutput:videoOutput
        audioOutput:audioOutput
    }

    VideoOutput {
        id:videoOutput
        anchors.fill:parent
    }

    ChartView {
        id: chart
        anchors.fill: parent
        clip: true
        opacity: 0.5
        axes: [
            ValueAxis{
                id: xAxis
                min: 50.0
                max: 2500.0
            },
            ValueAxis{
                id: yAxis
                min: 1.0
                max: 255.0
            }
        ]
    }

    // TableView {
    //     id: myTableView
    //     anchors.fill: parent
    //     columnSpacing: 1
    //     rowSpacing: 1
    //     clip: true
    //     opacity: 0.5

    //     // model: TableModel {}

    //     delegate: Rectangle {
    //         implicitWidth: 100
    //         implicitHeight: 50
    //         Text {
    //             text: display
    //         }
    //     }
    // }

    AudioOutput {
        id:audioOutput
        volume:volumeSlider.value
    }

    Component.onCompleted: {
        player.source = foo.get_file_name()
        player.play()
        // myTableView.model = myModel
        var all_points = foo.add_series(qsTr("blah"))

        var series = chart.createSeries(ChartView.SeriesTypeLine, "line", xAxis, yAxis);
        series.pointsVisible = true;
        series.pointsVisible = true;
        series.color = Qt.rgba(Math.random(),Math.random(),Math.random(),1);
        series.hovered.connect(function(point, state){ console.log(point); }); // connect onHovered signal to a function
        var maxX = 2
        var minY = 6000
        var maxY = -6000
        for (var i = 0; i < all_points.length; i++)  {
            series.append(all_points[i].x, all_points[i].y)
            if (all_points[i].x > maxX) {
                maxX = all_points[i].x
            }
            if (all_points[i].y < minY) {
                minY = all_points[i].y 
            }
            else if (all_points[i].y > maxY) {
                maxY = all_points[i].y
            }
        }
        xAxis.max = maxX
        yAxis.min = minY
        yAxis.max = maxY
        // foo.plot_graph()
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