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
        self.admin_layer     = project.mapLayersByName(ADMIN_LAYER)[0]
        self.elevation_layer = project.mapLayersByName(ELEVATION_LAYER)[0]


        self.enableAntiAliasing(True)
        self.setCanvasColor(Qt.black)
        self.setScaleLocked(False)

        self.setLayers([
            self.incidents_layer,
            self.admin_layer,     
            self.elevation_layer 
        ])

        self.mapExtents = self.incidents_layer.extent()


        self.setExtent(self.mapExtents) 
        self.fullScale = self.scale()

        self.start()
        self.mapCanvasRefreshed.connect(self._update) 


    def start(self):
        pass


    def _update(self):
        self.t0 = time.time()

        self.dtime = min(1.0, self.t0 - self.t1)
        self.framerate = 1.0 / max(self.dtime, 0.000001)
        self.setWindowTitle(f"[{self.name}] | FPS: {self.framerate:04f}")

        self.update()
        self.refresh()
        self.t1 = time.time()

    def update(self):
        raise NotImplementedError()

class MapCanvasInspector(HorrorCanvas):

    max_scale_factor = 20.0

    idle_time            = 1.0
    focus_idle_time      = 7.0

    moving_to_point_target_scale = 800000000

    scale_step = 0.000
    pan_step   = 3000

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


    def scale_up(self, target_scale):
        curScale = self.scale()
        print(curScale, target_scale, curScale  > target_scale)
        if(curScale  > target_scale ):
            fac = 1.0 + (self.scale_step * self.dtime)
            print(fac)
            self.setScale(fac)
            return False
        else: 
            #self.zoomScale(target_scale, ignoreScaleLock = True )
            return True

    def scale_down(self, target_scale):
        curScale = self.scale()
        print(curScale, target_scale, curScale  < target_scale)
        if(curScale  < target_scale ):
            fac = 1.0 - (self.scale_step * self.dtime)
            print(fac)
            #self.zoomByFactor(fac)	
            return False
        else: 
            #self.zoomScale(target_scale, ignoreScaleLock = True)
            return True

    def update(self):
        t = time.time()
        mode = self.mode

        if mode == "idle":
            center = self.center()

            print(self.dtime)
            center += getNoiseVector(t) * (self.pan_step * self.dtime)
            self.setCenter(center)

            if(t - self.last_state_change >= self.idle_time):
                print("Idle timed out...")
                self.get_random_poi()

        elif mode == "moving-to-point":
            p = self.pan_to(self.pio)
            s = self.scale_up(self.fullScale / 10)
            if p and s:
                self.set_mode("fit-data")


        elif mode == "fit-data":
            self.set_mode("focus-idle")
        elif mode == "focus-idle":
            if(t - self.last_state_change < self.focus_idle_time):
                pass
            else:
                self.set_mode("moving-to-idle")

        elif mode == "moving-to-idle":
            p = self.pan_to(self.mapExtents.center())
            s = self.scale_down(self.fullScale)
            if p and s:
                self.setExtent(self.mapExtents) 
                self.set_mode("fit-data")

        else:
            print(f"Mode not recognized {mode}")
            pass
        