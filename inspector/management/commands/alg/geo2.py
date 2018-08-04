import math

def mercator(lon,lat):
    x=lon*20037508.34/180
    y=math.log(math.tan((90+lat)*math.pi/360))/(math.pi/180)
    y=y*20037508.34/180
    return x,y

def un_mercator(x,y):
    x1=x/20037508.34*180
    y1=y/20037508.34*180
    lat=180/math.pi*(2*math.atan(math.exp(y1*math.pi/180))-math.pi/2)
    return x1,lat

def get_factor(cor1,loc1,cor2,loc2):
    corx1,cory1=cor1
    locx1,locy1=loc1
    corx2,cory2=cor2
    locx2,locy2=loc2
    a=(locx1-locx2)/(corx1-corx2)
    c=locx1-a*corx1
    
    b=(locy1-locy2)/(cory1-cory2)
    d=locy1-b* cory1
    return a,b,c,d

def cord2loc(corx,cory):
    lon = a* corx +c
    lat = b * cory +d
    lon,lat=un_mercator(lon,lat)
    return lon,lat


#######################
x1,y1 = -25700,-8758
mx1,my1= 121.202033,31.154141
mx1,my1=mercator(mx1,my1)

x2,y2=-21600,-8988
mx2,my2= 121.245158,31.152109
mx2,my2=mercator(mx2,my2)
############################
a,b,c,d=get_factor((x1,y1),(mx1,my1),(x2,y2),(mx2,my2))

print(cord2loc(x1,y1))