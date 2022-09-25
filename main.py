from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QObject, Slot
from PySide6.QtGui import QFont
from backend.luminosity_detection import extract_luminosity_data
from backend.audio_lufs import extractLufsFromVideo
import pandas as pd
import sys
from PySide6.QtCharts import QChart, QBarSeries, QLineSeries, QBarSet, QBarCategoryAxis, QValueAxis

class Window(QWidget):
    def __init__(self):
        super().__init__()

class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None

class Foo(QObject):
    @Slot(str)
    def set_file_name(self, file_name):
        self.file_name = file_name
        print(self.file_name)
    
    @Slot(result=str)
    def get_file_name(self):
        return self.file_name

    @Slot(str, int)
    def trigger_analysis(self, file_name, interval_seconds):
        luminosity = extract_luminosity_data(file_name, interval_seconds)
        lufs = extractLufsFromVideo(file_name, interval_seconds)
        luminosity['lufs'] = lufs['lufs']
        luminosity = luminosity.dropna()
        self.graph_data = PandasModel(luminosity)
        engine.rootContext().setContextProperty('myModel', self.graph_data)
        self.load_graph_player()
    
    def load_graph_player(self):
        engine.load('frontend/GraphPlayer.qml')

    @Slot(str, result=list)
    def add_series(self, name):
        self.series = QLineSeries()
        self.series.setName(name)

        # Filling QLineSeries
        for i in range(self.graph_data.rowCount()):
            x = int(self.graph_data._dataframe.index[i])
            y = float(self.graph_data.index(i, 0).data())
            self.series.append(x, y)

        return self.series.points()

    @Slot()
    def plot_graph(self):
        seconds = self.graph_data.index
        luminosity = self.graph_data['luminosity']
        lufs = self.graph_data['lufs']

        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeBlueIcy)

        font = QFont()
        font.setPixelSize(20)
        chart.setTitleFont(font)
        chart.setTitle("blah")

        cases_max = []
        i = 0
        series = QBarSeries()
        curr_set = "set" + str(i)
        curr_set = QBarSet(str(year[0]))
        curr_set << int(year[1])
        series.append(curr_set)
        series.setLabelsVisible(True)
        series.labelsPosition()
        chart.addSeries(series)
        cases_max.append(int(year[1]))
        # print(self.graph_data.index)
        # get the data
        # years = []
        # reports = []
        # for year in year_list:
        #     years.append(year[0])
        #     reports.append(year[1])

        # # create the chart
        
        # # set font for chart title
        

        # #data to series and put to chart
        

        #     i += 1

        # #create axis
        # axisX = QBarCategoryAxis()
        # axisX.setLabelsVisible(True)
        # axisX.append(years)

        # axisY = QValueAxis()
        # axisY.setLabelsVisible(True)
        # axisY.setMin(0)
        # axisY.setMax(max(reports))
        # axisY.setLabelFormat("%.0f")
        # axisY.setTitleText("Reports")

        # # bild the chart
        # chart.createDefaultAxes()
        # chart.legend().hide()
        # chart.setAxisX(axisX)
        # chart.setAxisY(axisY)

        # # create view
        # chartview = QChartView(chart)
        # vbox = QVBoxLayout()
        # vbox.addWidget(chartview)

        # # put view to qt grid layout
        # self.ui.gridLayout.addWidget(chartview,0,0)

app = QApplication(sys.argv)
app.setStyle("Windows")

engine = QQmlApplicationEngine()

window = Window()
foo = Foo()

engine.load('frontend/FileSelector.qml')

engine.rootContext().setContextProperty('window', window)
engine.rootContext().setContextProperty("foo", foo)

# Start the event loop.
sys.exit(app.exec())