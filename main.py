import sys
import math
import time
import signal

from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QFrame
from qgis.PyQt.QtCore import *
from qgis.core import *
from qgis.gui import *

from renderer import *

def main():

    app = QgsApplication([], True) 
    app.setPrefixPath("/usr/bin/qgis", True) 
    app.initQgis() 

    screens = app.screens()

    project = QgsProject.instance() 
    project.read("project.qgz")

    display0 = MapCanvasInspector("display0", project)
    display0.setGeometry(screens[0].geometry().x(), screens[0].geometry().y(), 1920, 1024)
    display0.setFrameShape(QFrame.NoFrame)
    display0.showFullScreen()
    display0.show()


    display1 = MapCanvasInteractive("display1", project)
    display1.show()
    display1.setGeometry(screens[1].geometry().x(), screens[1].geometry().y(), 1920, 1024)
    display1.setFrameShape(QFrame.NoFrame)
    display1.showFullScreen()


    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()