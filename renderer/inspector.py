from .renderer import *

from qgis.PyQt.QtCore import *
from qgis.core import *
from qgis.gui import *

from horror import send_cue

class MapCanvasInspector(HorrorCanvas):

    max_scale_factor     = 20.0
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

    def wheelEvent (self, event):
        #print(event)
        pass

    def panAction (self, event):
        #print(event)
        pass
             

    def start(self):

        for layer in self.layers:
            if layer.name() == INCIDENTS_LAYER:
                self.incidents_layer = layer
                self.incidents_layer.setLabelsEnabled(False)
                self.mapExtents = self.layers[0].extent()
                break
        self.setExtent(self.mapExtents) 
        self.set_mode("idle")

    def set_mode(self, mode):
        self.last_state_change = time.time()
        self.mode = mode
        send_cue(f"map-{self.mode}")
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
        