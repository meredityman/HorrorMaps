import time
from math import sin, cos

import random
import numpy as np

from qgis.PyQt.QtCore import *
from qgis.core import *
from qgis.gui import *

INCIDENTS_LAYER = "incidents_EPSG_31491"
ADMIN_LAYER     = "DEU_adm3_EPSG_31491"
ELEVATION_LAYER = "DEU_msk_alt_ESPG_31491"

def getNoiseVector(t):
    return QgsVector(
        0.45348 * sin(t * 1.4831) + 0.74963 * cos(t * 1.02458) + 0.43482 * sin(t * 1.01257), 
        0.34834 * cos(t * 1.8789) + 0.41234 * sin(t * 1.02187) + 0.78545 * sin(t * 1.72785)
    ) 


class HorrorCanvas(QgsMapCanvas):

    def __init__(self, name, project):
        QgsMapCanvas.__init__(self)
        self.t1 = 0
        self.t0 = 0
        self.name = name

        self.project = project

        self.setLayers(name)
        
        self.setMagnificationFactor(1.0)
        self.enableAntiAliasing(True)
        self.setCanvasColor(Qt.black)
        self.setScaleLocked(False)
        self.setParallelRenderingEnabled(True)
        
        self.fullScale = self.scale()

        self.start()
        self.mapCanvasRefreshed.connect(self._update) 

    def setLayers(self, group):

        for child in self.project.layerTreeRoot().children():
            if isinstance(child, QgsLayerTreeGroup):
                if child.name() == group:
                    print(f"Found Layers {group}")
                    self.layers = [c.layer() for c in child.findLayers()]

                    print(self.layers)
                    self.setLayers(self.layers)

                    self.mapExtents = self.layers[0].extent()
                    print(self.mapExtents)
                    self.setExtent(self.mapExtents) 

# QgsMapCanvas.__init__(self)
# self.t1 = 0
# self.t0 = 0
# self.name = name

# self.project = project

# self.incidents_layer = project.mapLayersByName(INCIDENTS_LAYER)[0]
# self.incidents_layer.setLabelsEnabled(False)

# self.admin_layer     = project.mapLayersByName(ADMIN_LAYER)[0]
# self.elevation_layer = project.mapLayersByName(ELEVATION_LAYER)[0]

# self.setMagnificationFactor(1.3)

# self.enableAntiAliasing(True)
# self.setCanvasColor(Qt.black)
# self.setScaleLocked(False)
# self.setParallelRenderingEnabled(False)

# self.setLayers([
#     self.incidents_layer,
#     # self.admin_layer,     
#     self.elevation_layer 
# ])

# 


# self.setExtent(self.mapExtents) 
# self.fullScale = self.scale()

# self.start()
# self.mapCanvasRefreshed.connect(self._update) 


    def start(self):
        pass


    def _update(self):
        self.t0 = time.time()

        self.dtime = min(1.0, self.t0 - self.t1)
        self.framerate = 1.0 / max(self.dtime, 0.000001)
        self.setWindowTitle(f"[{self.name}] | FPS: {self.framerate:04f}")

        if(self.update()):
            self.refresh()

        self.t1 = time.time()

    def update(self):
        raise NotImplementedError()
