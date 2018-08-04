
from inspector.models import Inspector,InspectorWorkGroup
from django.utils.timezone import datetime, timedelta
from dianzi_weilan.models import OutBlockWarning
from helpers.director.kv import get_value

def removeInvalidPos(keeper, posList): 
    """
    移除非工作时间的数据
    """
    worktimes = inspectorWorkTime(keeper)
    leftPos = [x for x in posList if isInWorktime( x.get('tracktime'), worktimes )]
    return leftPos

def noPosCheck(keeper,posList, checkDay):
    """
    检查工作时间内，没有数据的点
    """
    worktimes = inspectorWorkTime(keeper)
    for worktime in worktimes:
        working = True
        lastWarning = None
        for timePoint in splitTime(worktime, checkDay):
            if working != hasTrackNearTime(timePoint, posList):
                if working:
                    lastWarning = OutBlockWarning.objects.create(inspector= keeper,reason= '没有坐标点', start_time = timePoint)
                    working = False
                else:
                    lastWarning.end_time = timePoint
                    lastWarning.save()
                    working = True
        if lastWarning and not lastWarning.end_time:
            lastWarning.end_time = timePoint 
            lastWarning.save()
        
            

def outBoxCheck(keeper,posList):
    """
    @posList:
    """
    working = True
    weilanBox =  inspectorWeilan(keeper)
    for posdc in posList:
        # 不在围栏内，需要报警
        #x,y=cordToloc(pos.get('coordx'),pos.get('coordy'))
        #pos = Point(float(x),float(y))
        pos = posdc.get('pos')
        timePoint = posdc.get('tracktime')
        if working != in_the_block(pos, weilanBox):
            if working:
                lastWarning = OutBlockWarning.objects.create(inspector= keeper,reason= '跑出围栏', start_time = timePoint)
                working = False
            else:
                lastWarning.end_time = timePoint
                lastWarning.save()
                working = True          


def isInWorktime(tracktime, worktimes): 
    for worktime in worktimes:
        lt, gt = [todayTime(x, tracktime) for x in worktime.split('-')]
        if lt <= tracktime <= gt:
            return True
    return False

def inspectorWorkTime(keeper):
    ls=[]
    for workgroup in keeper.inspectorworkgroup_set.all():
        ls.extend(workgroup.work_time.split(';'))
    if not ls:
        ls.extend( get_value('work_time','8:30-12:30;14:00-18:00').split(';') )
    return ls

def in_the_block(pos,weilanBox):
    out_blocks=[]
    #for group in inspector.inspectorgrop_set.filter(kind = 1):
        #for rel in group.inspectorgroupandweilanrel_set.all():
            #polygon = rel.block.bounding
    for polygon in  weilanBox:
            # 经纬度坐标之distance*100大致等于公里数。因为不准确性的存在，warning_distance是按照公里数来判断的。
            if pos.distance(polygon)*100< float( get_value('warning_distance','0.3') ):
                return True
            else:
                out_blocks.append(polygon)
    # 某些监督员没有指定区域，尽管没有被框在某个block里面，但是被认为没有 出界
    if not out_blocks:
        return True
    else:
        return False

def inspectorWeilan(inspector): 
    ls = []
    for group in inspector.inspectorgrop_set.filter(kind = 1):
        for rel in group.inspectorgroupandweilanrel_set.all():
            polygon = rel.block.bounding
            ls.append(polygon)
    return ls
            ## 经纬度坐标之distance*100大致等于公里数。因为不准确性的存在，warning_distance是按照公里数来判断的。
            #if pos.distance(polygon)*100< float( get_value('warning_distance','0.3') ):
                #return True
            #else:
                #out_blocks.append(polygon)

def splitTime(timeSpan, mainTime = None): 
    """
    @timeSpan:8:30-12:30
    """
    mainTime = mainTime or datetime.now()
    start, end = [todayTime(x, mainTime) for x in timeSpan.split('-')]
    
    start += timedelta(minutes = 15)
    while start < end:
        yield start
        start += timedelta(minutes = 15)
    

def todayTime(timeStr, mainTime = None): 
    if not mainTime:
        mainTime =  datetime.now()
    nn = datetime.strptime(timeStr, '%H:%M')
    tm = mainTime.replace(hour = nn.hour, minute = nn.minute)
    return tm

def hasTrackNearTime(timePoint, posList): 
    lt = timePoint + timedelta(minutes = 10)
    gt = timePoint - timedelta(minutes = 10)
    for posdc in posList:
        if gt <= posdc.get('tracktime') <= lt:
            return True
    return False

