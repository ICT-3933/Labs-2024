import geopandas as gpd
from shapely.geometry import Polygon
from math import cos, sin, pi
import numpy as np

# This method returns a grid teselation shape based on:
## xmin: left x border to fulfill with grid (UTM coordinate)
## xmax: right x border to fulfill with grid (UTM coordinate)
## ymin: bottom y border to fulfill with grid (UTM coordinate)
## ymax: top y border to fulfill with grid (UTM coordinate)
## width: width of specific cell in grid teselation (meters)
## heigth: heigth of specific cell in grid teselation (meters)
## epsg: projection used in the input coordinates (UTM)
def grid_teselation(xmin, xmax, ymin, ymax, width, height, epsg):
    w = width
    h = height
    
    rows = int(np.ceil((ymax-ymin) / height))
    cols = int(np.ceil((xmax-xmin) / width))
    
    xCol = xmin
    yCol = ymax
    
    cells = []
    polygons = []
    c = 1
    for _ in range(cols):
        x = xCol
        y = yCol
        xCol += w
        for _ in range(rows):
            cells.append(c)
            polygons.append(Polygon([(x,y), (x+w,y), (x+w,y-h), (x,y-h)])) 
            y -= h
            c+=1

    grid = gpd.GeoDataFrame({'cell': cells, 'geometry':polygons})
    grid.crs = epsg
    grid['area'] = grid.area
    return grid

# This method returns a hexagon teselation shape based on:
## xmin: left x border to fulfill with grid (UTM coordinate)
## xmax: right x border to fulfill with grid (UTM coordinate)
## ymin: bottom y border to fulfill with grid (UTM coordinate)
## ymax: top y border to fulfill with grid (UTM coordinate)
## side: hexagon radious or side (meters)
## epsg: projection used in the input coordinates (UTM)
def hexagon_teselation(xmin, xmax, ymin, ymax, side, epsg):
    s = side
    a = s*cos(pi/6)
    b = s*sin(pi/6)
    
    rows = int(np.ceil((ymax-ymin) / (2*a)))
    cols = int(np.ceil((xmax-xmin) / (b+s)))
    
    xEvenCol = xmin
    yEvenCol = ymax
    xOddCol = xmin + s + b
    yOddCol = ymax + a
    
    cells = []
    polygons = []
    
    c = 1
    for i in range(cols+1):
        if i%2 == 0:
            x = xEvenCol
            y = yEvenCol
            xEvenCol += 2*(b+s) 
        else:
            x = xOddCol
            y = yOddCol
            xOddCol += 2*(b+s)
        for _ in range(rows+1):
            cells.append(c)
            polygons.append(Polygon([(x, y), (x+s,y), (x+s+b,y-a), (x+s,y-2*a),(x,y-2*a),(x-b,y-a)])) 
            y -= 2*a
            c+=1 
    hexagon = gpd.GeoDataFrame({'cell': cells, 'geometry':polygons})
    hexagon.crs = epsg
    hexagon['area'] = hexagon.area
    return hexagon