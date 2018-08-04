import math

a,b,c,d = 1.17052262339854, 0.004886539695803549, 13522234.538214915, 3663178.0482749026

def un_mercator(x,y):
    x1=x/20037508.34*180
    y1=y/20037508.34*180
    lat=180/math.pi*(2*math.atan(math.exp(y1*math.pi/180))-math.pi/2)
    return x1,lat

def cord2loc(x,y):
    o_x=a*x+b*y+c
    o_y=b*x-a*y+d
    lon=o_x
    lat=o_y
    #lon,lat = XYmiller(o_x,o_y)
    lon,lat = un_mercator(o_x,o_y)
    #return geo.wgs84_to_gcj02( lon,lat )
    return lon,lat