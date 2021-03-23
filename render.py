import sys
import math
import time
import signal

from qgis.PyQt.QtGui import (
    QColor,
)

from qgis.PyQt.QtCore import Qt, QRectF, QTimer

from qgis.core import (
    QgsVectorLayer,
    QgsPoint,
    QgsPointXY,
    QgsProject,
    QgsGeometry,
    QgsMapRendererJob,
    QgsApplication
)

from qgis.gui import (
    QgsMapCanvas,
    QgsVertexMarker,
    QgsMapCanvasItem,
    QgsRubberBand,
    QgsMapToolIdentifyFeature
)


INCIDENTS_LAYER = "incidents_EPSG_31491"
ADMIN_LAYER     = "DEU_adm3_EPSG_31491"
ELEVATION_LAYER = "DEU_msk_alt_ESPG_31491"

app = QgsApplication([], True) 
app.setPrefixPath("/usr/bin/qgis", True) 
app.initQgis() 

project = QgsProject.instance() 
project.read("project.qgz")

incidents_layer = project.mapLayersByName(INCIDENTS_LAYER)[0]
admin_layer     = project.mapLayersByName(ADMIN_LAYER)[0]
elevation_layer = project.mapLayersByName(ELEVATION_LAYER)[0]

canvases = {
    "display0" : QgsMapCanvas(), 
    "display1" : QgsMapCanvas()
}
canvases_rev = {v: k for k, v in canvases.items()}

def tick(canvas):
    name = canvases_rev[canvas]

    if name == "display0":
        mag = 1.2 + 0.2 * math.sin(time.time())
    elif name == "display1":
        mag = 4.0 + 0.2 * math.sin(time.time())
    else:
        mag = 1.0


    canvas.setMagnificationFactor(mag)
    canvas.refresh()


for name, canvas in canvases.items():
    canvas.setGeometry(0, 0, 1920, 1024)
    canvas.setCanvasColor(Qt.black)
    canvas.enableAntiAliasing(True)

    canvas.setLayers([
        incidents_layer,
        admin_layer,     
        elevation_layer 
    ])

    canvas.setExtent(incidents_layer.extent())    

    canvas.mapCanvasRefreshed.connect(lambda canvas=canvas: tick(canvas))  
    canvas.show()


signal.signal(signal.SIGINT, signal.SIG_DFL)
# timer = QTimer()
# timer.timeout.connect(tick)
# timer.start(1/12)

# while(True):


sys.exit(app.exec_())
