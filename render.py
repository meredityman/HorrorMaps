import os
from qgis.core import *
from PyQt5 import *
from PyQt5.QtSvg import *
from PyQt5.Qt import *

app = QgsApplication([], True) 
app.setPrefixPath("/usr/bin/qgis", True) 
app.initQgis() 

project = QgsProject.instance() 
project.read("project.qgz")


# layout = QgsProject.instance().layoutManager().layoutByName("Layout_1")
# exporter = QgsLayoutExporter(layout)

# layers = list(project.mapLayers().values())
# print(layers)

layer_names = [ 
    "incidents_EPSG_31491", 
    "DEU_adm3_EPSG_31491", 
    "DEU_msk_alt_ESPG_31491"
]
layers = [ project.mapLayersByName(name)[0] for name in layer_names]
#layers = list(project.mapLayers().values())

# for layer in layers:
#     layer.setCrs(QgsCoordinateReferenceSystem('EPSG:31491'))


options = QgsMapSettings()

options.setLayers(layers)
options.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:31491'))

print(layers[2].crs())


#options.setDestinationCrs(layers[0].crs())

options.setBackgroundColor(QColor(0, 0, 0))
options.setOutputSize(QSize(1920, 1024))

options.setExtent(layers[0].extent())



print(options.destinationCrs())

render = QgsMapRendererParallelJob(options)
image_location = "renders/render.png"

def finished():
    img = render.renderedImage()
    img.save(image_location, "png")
    print("saved")

render.finished.connect(finished)
render.start()
render.waitForFinished()
