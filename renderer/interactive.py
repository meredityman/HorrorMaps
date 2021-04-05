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

        w = QgsFieldValuesLineEdit()
        w.setLayer(self.incidents_layer)
        w.setAttributeIndex(0) # or 1, 2,.. depending on which field you want to show
        w.show()

    def update(self):
        pass
        