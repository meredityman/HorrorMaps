from .renderer import *

from qgis.PyQt.QtCore import *
from qgis.core import *
from qgis.gui import *

class MapCanvasInteractive(HorrorCanvas):

    def start(self):
        self.incidents_layer = self.project.mapLayersByName(INCIDENTS_LAYER)[0]
        self.incidents_layer.setLabelsEnabled(False)
        self.mapExtents = self.layers[0].extent()
        self.setExtent(self.mapExtents) 

    def update(self):
        pass
        