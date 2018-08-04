from geoinfo.polygon import dict2poly
from django.contrib.gis.geos import Polygon
import math
def polygon2circle(polygon):
    center =  polygon.centroid.coords
    radius =  math.sqrt( polygon.area)*50000
    return {
        'center':center,
        'radius':radius
    }
