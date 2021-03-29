import sys
import math
import time
import signal

from qgis.PyQt.QtGui import QColor

from qgis.PyQt.QtCore import *
from qgis.core import *
from qgis.gui import *

from renderer import *

def main():

    app = QgsApplication([], True) 
    app.setPrefixPath("/usr/bin/qgis", True) 
    app.initQgis() 

    project = QgsProject.instance() 
    project.read("project.qgz")

    display0 = MapCanvasInspector("display0", project)
    #display0.setGeometry(0, 0, 1920 / 2, 1024 / 2) 
    display0.showFullScreen()
    display0.show()


    display1 = MapCanvasInteractive("display1", project)
    display1.setGeometry(0, 0, 1920, 1024)
    display1.show()
    try:
        display1.windowHandle().setScreen(app.screens()[1])
        display1.showFullScreen()
    except:
        pass


    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()