import sys
import math
import time
import signal

from qgis.PyQt.QtGui import (
    QColor,
)

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

    display0 = MapCanvasA(project)
    display0.setGeometry(0, 0, 1920, 1024)       
    display0.show()


    display1 = MapCanvasB(project)
    display1.setGeometry(0, 0, 1920, 1024)
    display1.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()