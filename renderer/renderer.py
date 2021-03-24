import time
import math

from qgis.PyQt.QtCore import *
from qgis.core import *
from qgis.gui import *

INCIDENTS_LAYER = "incidents_EPSG_31491"
ADMIN_LAYER     = "DEU_adm3_EPSG_31491"
ELEVATION_LAYER = "DEU_msk_alt_ESPG_31491"

class HorrorCanvas(QgsMapCanvas):

    def __init__(self, project):
        QgsMapCanvas.__init__(self)
        self.t1 = 0
        self.t0 = 0


        self.project = project

        incidents_layer = project.mapLayersByName(INCIDENTS_LAYER)[0]
        admin_layer     = project.mapLayersByName(ADMIN_LAYER)[0]
        elevation_layer = project.mapLayersByName(ELEVATION_LAYER)[0]



        self.enableAntiAliasing(True)
        self.setCanvasColor(Qt.black)

        self.setLayers([
            incidents_layer,
            admin_layer,     
            elevation_layer 
        ])

        self.setExtent(incidents_layer.extent())    
        self.mapCanvasRefreshed.connect(self._update) 


    def _update(self):
        self.t0 = time.time()



        self.dtime = self.t0 - self.t1
        self.framerate = 1.0 / max(self.dtime, 0.000001)
        self.setWindowTitle(f"dtime: {self.dtime:04f} | FPS: {self.framerate:04f}")


        self.update()
        self.refresh()
        self.t1 = time.time()

    def update(self):
        raise NotImplementedError()

class MapCanvasA(HorrorCanvas):

    def __init__(self, project):
        super(MapCanvasA, self).__init__(project)

    def update(self):
        mag = 1.2 + 0.2 * math.sin(time.time())
        self.setMagnificationFactor(mag)



class MapCanvasB(HorrorCanvas):

    def __init__(self, project):
        super(MapCanvasB, self).__init__(project)

    def update(self):
        mag = 4.0 + 0.2 * math.sin(time.time())
        self.setMagnificationFactor(mag)

