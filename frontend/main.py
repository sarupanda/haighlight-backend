from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QWidget
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)
app.setStyle("Material")

engine = QQmlApplicationEngine()

window = Window()

engine.rootContext().setContextProperty('window', window)
engine.load('FileSelector.qml')

# Start the event loop.
sys.exit(app.exec())