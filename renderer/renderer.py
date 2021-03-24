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

        self.incidents_layer = project.mapLayersByName(INCIDENTS_LAYER)[0]
        self.incidents_layer.setLabelsEnabled(False)
        
        self.admin_layer     = project.mapLayersByName(ADMIN_LAYER)[0]
        self.elevation_layer = project.mapLayersByName(ELEVATION_LAYER)[0]

        self.setMagnificationFactor(1.3)

        self.enableAntiAliasing(True)
        self.setCanvasColor(Qt.black)
        self.setScaleLocked(False)
        self.setParallelRenderingEnabled(False)

        self.setLayers([
            self.incidents_layer,
            # self.admin_layer,     
            self.elevation_layer 
        ])

        self.mapExtents = self.incidents_layer.extent()


        self.setExtent(self.mapExtents) 
        self.fullScale = self.scale()

        self.start()
        self.mapCanvasRefreshed.connect(self._update) 


    def start(self):
        pass

    def panAction (self, event):
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

class MapCanvasInspector(HorrorCanvas):

    max_scale_factor = 20.0

    idle_time            = 15.0
    focus_idle_time      = 7.0
    fit_data_time        = 3.0

    moving_to_point_target_scale = 800000000

    scale_step = 0.000
    pan_step   = 30000

    modes = [
        "idle",
        "moving-to-point",
        "fit-data",
        "focus-idle",
        "moving-to-idle"

    ]

    def start(self):
        self.set_mode("idle")

    def set_mode(self, mode):
        self.last_state_change = time.time()
        self.mode = mode
        print(f"Changed mode to {self.mode}")

    def set_pio(self, point):
        mode = self.mode
        if mode != "idle":
            print(f"Can only set point in idle mode. Mode is {mode}")
            return

        self.pio = point
        self.set_mode("moving-to-point")

    def get_random_poi(self):
        index = random.randint(0, self.incidents_layer.featureCount())
        for i, feature in enumerate(self.incidents_layer.getFeatures()):
            if( i == index):
                break

        point = QgsPointXY(QgsGeometry.asPoint(feature.geometry()))

        self.set_pio(point)


    def pan_to(self, point):
        vec = (point - self.center())
        if(vec.length() > self.pan_step ):
            vec = vec.normalized() * self.pan_step
            center = self.center() + vec
            self.setCenter(center)

            return False
        else:
            self.setCenter(point)
            return True


    def update(self):
        t = time.time()
        mode = self.mode

        if mode == "idle":
            center = self.center()


            center += getNoiseVector(t) * (self.pan_step * self.dtime)
            self.setCenter(center)

            if(t - self.last_state_change >= self.idle_time):
                print("Idle timed out...")
                self.get_random_poi()

            return True
        elif mode == "moving-to-point":
            self.setMagnificationFactor(1.5)
            if self.pan_to(self.pio):
                self.set_mode("fit-data")

            return True

        elif mode == "fit-data":
            if(self.magnificationFactor()  != 10.5):
                self.setMagnificationFactor(10.5)
                self.incidents_layer.setLabelsEnabled(True)
            else:
                if(t - self.last_state_change >= self.fit_data_time):
                    self.set_mode("focus-idle")
            
            return True

        elif mode == "focus-idle":
            if(t - self.last_state_change < self.focus_idle_time):
                if(self.magnificationFactor()  != 300.5):
                    self.setMagnificationFactor(300.5)
                    self.incidents_layer.setLabelsEnabled(True)
                    return True
                else:
                    return False
            else:
                self.set_mode("moving-to-idle")
                return True


        elif mode == "moving-to-idle":
            self.incidents_layer.setLabelsEnabled(False)
            self.setMagnificationFactor(2.5)

            if self.pan_to(self.mapExtents.center()):
                self.setExtent(self.mapExtents) 
                self.set_mode("idle")

            return True
        else:
            print(f"Mode not recognized {mode}")
            return False
        