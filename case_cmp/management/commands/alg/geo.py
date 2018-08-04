import math

#a,b,c,d=1.6558230947769061, 0.65501128231426264, 13540711.169806115, 3653775.1671717167
a,b,c,d =0.27754975426000783, 0.24002047717772257, 13503924.727609258, 3654480.9400234558

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