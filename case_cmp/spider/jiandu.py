# encoding:utf-8
from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import re
from django.conf import settings

class JianDuSpider(object):
    """获取监督员case"""
    def __init__(self,start,end=None):
        """
        @start:2018-03-04
        @end:
        """
        self.proxies = getattr(settings,'DATA_PROXY',{})
        self.start=start
        self.end= end or start
        self.headers={
            'Cache-Control': 'max-age=0',
            'Origin': 'http://10.231.18.25',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://10.231.18.25/INSGRID/caseoperate_flat/ALLCASELIST.ASPX?STATUSID=3&CATEGORYID=120',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie':'ASP.NET_SessionId=n3p0p0urmin3rzc5xvmpwaaa',
        }
        
    def get_data(self):
        """
        rt = [
        u'1', #序号
        u'\u5f85\u53d7\u7406', #案件状态
        u'1803I8111682', #任务号
        u'\u76d1\u7763\u5458\u4e0a\u62a5', #案件来源
        u'2018-03-19 13:26', #发现时间
        u'\u4e8b\u4ef6', #案件属性
        u'\u73af\u536b\u5e02\u5bb9', #案件大类
        u'\u4e71\u6d82\u5199\u3001\u4e71\u5f20\u8d34...', #案件小类
        u'', #案件子类
        u'\u8d75\u5df7\u9547',  #街镇
        u'\u8d75\u534e\u8def512\u5f041\u53f7 ',#发生地址
        u'', #重点区域
        u'',#派遣时间
        u'', #在派遣中间派遣时间
        u'\u8d75\u5df7\u9547', #主责部门
        u'\u8d75\u5df7\u9547', #三级主责部门	
        u'', #结案时间
        u'-26463.84,-9090.60' #坐标
        ]

        """
        self.send_query_condition()
        crt_index = 0
        while True:
            content = self.get_page(crt_index)
            rows,total = self.parse_page(content)
            rows = self.filter_has(rows)
            for row in rows:
                row.append( self.get_coord(row[2]))
                yield row
            
            print('total=%s;crt_page_index=%s'%(total,crt_index))
            if (crt_index+1) *10 <total:
                crt_index +=1
            else:
                break            
    
    def send_query_condition(self):
        #body = 'arrstring=%7B%22startDate%22%3A%222018-01-01%22%2C%22endDate%22%3A%222018-03-31%22%2C%22btnTime%22%3A%22%22%2C%22hidSelectedTime%22%3A%22%22%2C%22startHour%22%3A%2200%3A00%22%2C%22endHour%22%3A%2223%3A59%22%2C%22MainExeDept%22%3A%22%22%2C%22SubExeDept%22%3A%22%22%2C%22RbStatus%22%3Atrue%2C%22RbSolvingStatus%22%3Afalse%2C%22hidStatusID%22%3A%220%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C100%2C101%2C102%22%2C%22hidStatusName%22%3A%22%E5%BE%85%E5%8F%97%E7%90%86%2C%E5%BE%85%E6%A0%B8%E5%AE%9E%2C%E5%B7%B2%E4%B8%8A%E6%8A%A5%E6%A0%B8%E5%AE%9E%2C%E5%BE%85%E7%AB%8B%E6%A1%88%2C%E5%BE%85%E6%B4%BE%E9%81%A3%2C%E5%BE%85%E5%82%AC%E5%8A%9E%2C%E5%BE%85%E4%B8%8B%E5%8F%91%E6%A0%B8%E6%9F%A5%2C%E5%B7%B2%E4%B8%8B%E5%8F%91%E6%A0%B8%E6%9F%A5%2C%E5%BE%85%E7%BB%93%E6%A1%88%2C%E5%B7%B2%E7%BB%93%E6%A1%88%2C%E5%B7%B2%E5%8F%97%E7%90%86%2C%E5%B7%B2%E7%AB%8B%E6%A1%88%2C%E5%B7%B2%E6%B4%BE%E9%81%A3%22%2C%22mainStatus_0%22%3Atrue%2C%22mainStatus_1%22%3Atrue%2C%22mainStatus_2%22%3Atrue%2C%22mainStatus_3%22%3Atrue%2C%22mainStatus_4%22%3Atrue%2C%22mainStatus_5%22%3Atrue%2C%22mainStatus_6%22%3Atrue%2C%22mainStatus_7%22%3Atrue%2C%22mainStatus_8%22%3Atrue%2C%22mainStatus_9%22%3Atrue%2C%22mainStatus_10%22%3Afalse%2C%22mainStatus_11%22%3Afalse%2C%22mainStatus_12%22%3Afalse%2C%22mainStatus_13%22%3Afalse%2C%22mainStatus_14%22%3Afalse%2C%22mainStatus_15%22%3Afalse%2C%22mainStatus_16%22%3Atrue%2C%22mainStatus_17%22%3Atrue%2C%22mainStatus_18%22%3Atrue%2C%22hidSolStatus%22%3A%22%22%2C%22hidSolStatusName%22%3A%22%22%2C%22SolvingStatus_0%22%3Afalse%2C%22SolvingStatus_1%22%3Afalse%2C%22SolvingStatus_2%22%3Afalse%2C%22SolvingStatus_3%22%3Afalse%2C%22SolvingStatus_4%22%3Afalse%2C%22SolvingStatus_5%22%3Afalse%2C%22SolvingStatus_6%22%3Afalse%2C%22SolvingStatus_7%22%3Afalse%2C%22SolvingStatus_8%22%3Afalse%2C%22SolvingStatus_9%22%3Afalse%2C%22SolvingStatus_10%22%3Afalse%2C%22SolvingStatus_11%22%3Afalse%2C%22mainTxt%22%3A%22%22%2C%22txtAddress%22%3A%22%22%2C%22TakeCaseInTimeValue%22%3A%22%22%2C%22TakeCaseInTimeText%22%3A%22%22%2C%22TakeCaseInTime_0%22%3Afalse%2C%22TakeCaseInTime_1%22%3Afalse%2C%22SovlingtimeTypeValue%22%3A%22%22%2C%22SovlingtimeTypeText%22%3A%22%22%2C%22SovlingtimeType_0%22%3Afalse%2C%22SovlingtimeType_1%22%3Afalse%2C%22SovlingtimeType_2%22%3Afalse%2C%22SovlingtimeType_3%22%3Afalse%2C%22BackCaseInTimeValue%22%3A%22%22%2C%22BackCaseInTimeText%22%3A%22%22%2C%22BackCaseInTime_0%22%3Afalse%2C%22BackCaseInTime_1%22%3Afalse%2C%22AlltimeTypeValue%22%3A%22%22%2C%22AlltimeTypeText%22%3A%22%22%2C%22AlltimeType_0%22%3Afalse%2C%22AlltimeType_1%22%3Afalse%2C%22AlltimeType_2%22%3Afalse%2C%22AlltimeType_3%22%3Afalse%2C%22MainCollDept%22%3A%22%22%2C%22SubCollDept%22%3A%22%22%2C%22TxtstrPriorityArea%22%3A%22%22%2C%22txtHeshiCount%22%3A%22%22%2C%22txtHechaCount%22%3A%22%22%2C%22discoverStartTime%22%3A%22%22%2C%22discoverEndTime%22%3A%22%22%2C%22preCreateStartTime%22%3A%22%22%2C%22preCreateEndTime%22%3A%22%22%2C%22dispatchStartTime%22%3A%22%22%2C%22dispatchEndTime%22%3A%22%22%2C%22CreateStartTime%22%3A%22%22%2C%22CreateEndTime%22%3A%22%22%2C%22solvingStartTime%22%3A%22%22%2C%22solvingEndTime%22%3A%22%22%2C%22endStartTime%22%3A%22%22%2C%22endEndTime%22%3A%22%22%2C%22TxtSimilarCase%22%3A%22%22%2C%22TxtSimilarNum%22%3A%22%22%2C%22TxtDispatchNum%22%3A%22%22%2C%22TxtEndUser%22%3A%22%22%2C%22btnsetcolumn%22%3A%22%E6%98%BE%E7%A4%BA%E6%9F%A5%E8%AF%A2%E5%88%97%22%2C%22btnSelecExelist%22%3A%22%E4%B8%8B%E8%BD%BD%E5%88%97%E8%A1%A8%22%2C%22btnSaveModule%22%3A%22%E4%BF%9D%E5%AD%98%E6%A8%A1%E6%9D%BF%22%2C%22btnSearchs%22%3A%22%E6%9F%A5++%E8%AF%A2%22%2C%22hdnFlag%22%3A%221%22%2C%22hdnTabCount%22%3A%223%22%2C%22hidTab%22%3A%220%22%2C%22Hidcount%22%3A%22%22%2C%22hidUseItemID%22%3A%22%22%2C%22hidDept%22%3A%22%22%2C%22hidOwnerName%22%3A%22%22%2C%22hidCaseBelongLevel%22%3A%22%22%2C%22hidStreetCode%22%3A%22%22%2C%22hidStreetName%22%3A%22%22%2C%22hidCommunityCode%22%3A%22%22%2C%22hidCommunityName%22%3A%22%22%2C%22hidgridCode%22%3A%22%22%2C%22hidgridName%22%3A%22%22%2C%22hidgridtype%22%3A%22%22%2C%22hidgridtypeName%22%3A%22%22%2C%22hidnewworkCode%22%3A%22%22%2C%22hidnewworkName%22%3A%22%22%2C%22hidnewgridCode%22%3A%22%22%2C%22hidnewgridkName%22%3A%22%22%2C%22hidSourceID%22%3A%22%22%2C%22hidSourceName%22%3A%22%22%2C%22HidCurDeptLv%22%3A%22%22%2C%22HidCurStreetCode%22%3A%22%22%2C%22HidHeChaDeptCode%22%3A%22%22%2C%22HidHeChaDeptName%22%3A%22%22%2C%22HidBeforeCollDept%22%3A%2220601%22%2C%22HidBeforeCollDeptName%22%3A%22%E8%B5%B5%E5%B7%B7%E9%95%87%22%2C%22HidMainCollDept%22%3A%22%22%2C%22HidMainCollDeptName%22%3A%22%22%2C%22HidSubCollDept%22%3A%22%22%2C%22HidSubCollDeptName%22%3A%22%22%2C%22HidMainDeptCode%22%3A%2220601%22%2C%22HidMainDeptName%22%3A%22%E8%B5%B5%E5%B7%B7%E9%95%87%22%2C%22hidSubDeptCode%22%3A%22%22%2C%22hidSubDeptName%22%3A%22%22%2C%22HidDifferentID%22%3A%22%22%2C%22HidType%22%3A%22%22%2C%22HidTypename%22%3A%22%22%2C%22HidMEBClass%22%3A%22%22%2C%22HidMEBClassName%22%3A%22%22%2C%22HidMESClass%22%3A%22%22%2C%22HidMESClassName%22%3A%22%22%2C%22HidSonClass%22%3A%22%22%2C%22HidSonClassName%22%3A%22%22%2C%22HidATClass%22%3A%22%22%2C%22HidATClassName%22%3A%22%22%2C%22HidTypeDifferent%22%3A%22%22%2C%22HidRelationCase%22%3A%22%22%2C%22HidA0383%22%3A%22%22%2C%22selectedTime%22%3A%2201%22%2C%22ddl_IsMainCase%22%3A%2210%22%2C%22ddl_Casebelonging%22%3A%22-1%22%2C%22ddlKeyList%22%3A%22-1%22%2C%22ddlSort%22%3A%22discovertime%22%2C%22ddlDesAsc%22%3A%22desc%22%2C%22select_new_street%22%3Anull%2C%22select_gridtype%22%3Anull%2C%22select_new_workgrid%22%3Anull%2C%22select_new_grid%22%3Anull%2C%22select_community%22%3A%22-1%22%2C%22select_grid%22%3A%22-1%22%2C%22InputArea%22%3Anull%2C%22ddlMEBClass%22%3A%22-1%22%2C%22ddlMESClass%22%3A%22-1%22%2C%22ddlSonClass%22%3A%22-1%22%2C%22ddlAtClass%22%3A%22-1%22%2C%22ddlApproach%22%3A%22-1%22%2C%22ddlUrgentdegree%22%3A%22-1%22%2C%22ddl_ServiceType%22%3A%22-1%22%2C%22ddlIsThreatened%22%3A%22-1%22%2C%22ddlIndustry%22%3Anull%2C%22ddlIsWeiXian%22%3A%22-1%22%2C%22ddlisPriorityArea%22%3A%22-1%22%2C%22ddlRiskLevel%22%3A%22-1%22%2C%22ddl_WorkTypes%22%3A%22-1%22%2C%22ddlWGCallBack%22%3A%22-1%22%2C%22DDLCompareHeshi%22%3A%22-1%22%2C%22DDLCompare%22%3A%22-1%22%2C%22ddlOverTimeCheck%22%3A%22-1%22%2C%22ddlIsWaiValue%22%3A%22-1%22%2C%22ddlWaiManYiDu%22%3A%22-1%22%2C%22ddlWaiFuWu%22%3A%22-1%22%2C%22dllCaseValuation%22%3A%22-1%22%2C%22ddl_IsFeedBack%22%3A%22-1%22%2C%22hcMyd%22%3A%22-1%22%2C%22ddlTelask%22%3A%22-1%22%2C%22ddlIsFirstContract%22%3A%22-1%22%2C%22ddlOverType%22%3A%22-1%22%2C%22ddlIsReply%22%3A%22-1%22%2C%22hfMyd%22%3A%22-1%22%2C%22ddlTaiDuManYi%22%3A%22-1%22%2C%22ddlHTelask%22%3A%22-1%22%2C%22ddlHIsFirstContact%22%3A%22-1%22%2C%22ddlHOverType%22%3A%22-1%22%2C%22ddlIsOver%22%3A%22-1%22%2C%22ddlAllManyi%22%3A%22-1%22%2C%22ddlGuoChenManyi%22%3A%22-1%22%2C%22ddlHResultType%22%3A%22-1%22%2C%22ddlHasLead%22%3A%22-1%22%2C%22ddlLEADERHANDTYPE%22%3A%22-1%22%2C%22ddlHasTenType%22%3A%22-1%22%2C%22ddlShijiHasTenType%22%3A%22-1%22%2C%22ddlFirstContact%22%3A%22-1%22%2C%22ddlSatisfied%22%3A%22-1%22%2C%22ddlFactType%22%3A%22-1%22%2C%22ddlViewInfo%22%3A%22-1%22%2C%22ddlAppealType%22%3A%22-1%22%2C%22ddlReplyType%22%3A%22-1%22%2C%22ddlIsPublic%22%3A%22-1%22%2C%22ddlBanliResult%22%3A%22-1%22%2C%22ddlIsCaseEnd%22%3A%22-1%22%2C%22ddlIsTypical%22%3A%22-1%22%2C%22ddlIsStubborn%22%3A%22-1%22%2C%22ddlIsSimilar%22%3A%22-1%22%2C%22ddlSimilarNum%22%3A%22-1%22%2C%22ddl_IsNew%22%3A%22-1%22%2C%22ddl_IsBackBill%22%3A%22-1%22%2C%22ddlIsTimeEnd%22%3A%22-1%22%2C%22ddlDispatchNum%22%3A%22-1%22%2C%22ddlIsStand%22%3A%22-1%22%2C%22ddlIsFast%22%3A%22-1%22%2C%22ddlIsSimplify%22%3A%22-1%22%2C%22ddlIsImage%22%3A%22-1%22%2C%22ddlCheckImage%22%3A%22-1%22%7D'
        
        body = 'arrstring=%7B%22startDate%22%3A%22{start}%22%2C%22endDate%22%3A%22{end}%22%2C%22btnTime%22%3A%22%22%2C%22hidSelectedTime%22%3A%22%22%2C%22startHour%22%3A%2200%3A00%22%2C%22endHour%22%3A%2223%3A59%22%2C%22MainExeDept%22%3A%22%22%2C%22SubExeDept%22%3A%22%22%2C%22RbStatus%22%3Atrue%2C%22RbSolvingStatus%22%3Afalse%2C%22hidStatusID%22%3A%220%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C100%2C101%2C102%22%2C%22hidStatusName%22%3A%22%E5%BE%85%E5%8F%97%E7%90%86%2C%E5%BE%85%E6%A0%B8%E5%AE%9E%2C%E5%B7%B2%E4%B8%8A%E6%8A%A5%E6%A0%B8%E5%AE%9E%2C%E5%BE%85%E7%AB%8B%E6%A1%88%2C%E5%BE%85%E6%B4%BE%E9%81%A3%2C%E5%BE%85%E5%82%AC%E5%8A%9E%2C%E5%BE%85%E4%B8%8B%E5%8F%91%E6%A0%B8%E6%9F%A5%2C%E5%B7%B2%E4%B8%8B%E5%8F%91%E6%A0%B8%E6%9F%A5%2C%E5%BE%85%E7%BB%93%E6%A1%88%2C%E5%B7%B2%E7%BB%93%E6%A1%88%2C%E5%B7%B2%E5%8F%97%E7%90%86%2C%E5%B7%B2%E7%AB%8B%E6%A1%88%2C%E5%B7%B2%E6%B4%BE%E9%81%A3%22%2C%22mainStatus_0%22%3Atrue%2C%22mainStatus_1%22%3Atrue%2C%22mainStatus_2%22%3Atrue%2C%22mainStatus_3%22%3Atrue%2C%22mainStatus_4%22%3Atrue%2C%22mainStatus_5%22%3Atrue%2C%22mainStatus_6%22%3Atrue%2C%22mainStatus_7%22%3Atrue%2C%22mainStatus_8%22%3Atrue%2C%22mainStatus_9%22%3Atrue%2C%22mainStatus_10%22%3Afalse%2C%22mainStatus_11%22%3Afalse%2C%22mainStatus_12%22%3Afalse%2C%22mainStatus_13%22%3Afalse%2C%22mainStatus_14%22%3Afalse%2C%22mainStatus_15%22%3Afalse%2C%22mainStatus_16%22%3Atrue%2C%22mainStatus_17%22%3Atrue%2C%22mainStatus_18%22%3Atrue%2C%22hidSolStatus%22%3A%22%22%2C%22hidSolStatusName%22%3A%22%22%2C%22SolvingStatus_0%22%3Afalse%2C%22SolvingStatus_1%22%3Afalse%2C%22SolvingStatus_2%22%3Afalse%2C%22SolvingStatus_3%22%3Afalse%2C%22SolvingStatus_4%22%3Afalse%2C%22SolvingStatus_5%22%3Afalse%2C%22SolvingStatus_6%22%3Afalse%2C%22SolvingStatus_7%22%3Afalse%2C%22SolvingStatus_8%22%3Afalse%2C%22SolvingStatus_9%22%3Afalse%2C%22SolvingStatus_10%22%3Afalse%2C%22SolvingStatus_11%22%3Afalse%2C%22mainTxt%22%3A%22%22%2C%22txtAddress%22%3A%22%22%2C%22TakeCaseInTimeValue%22%3A%22%22%2C%22TakeCaseInTimeText%22%3A%22%22%2C%22TakeCaseInTime_0%22%3Afalse%2C%22TakeCaseInTime_1%22%3Afalse%2C%22SovlingtimeTypeValue%22%3A%22%22%2C%22SovlingtimeTypeText%22%3A%22%22%2C%22SovlingtimeType_0%22%3Afalse%2C%22SovlingtimeType_1%22%3Afalse%2C%22SovlingtimeType_2%22%3Afalse%2C%22SovlingtimeType_3%22%3Afalse%2C%22BackCaseInTimeValue%22%3A%22%22%2C%22BackCaseInTimeText%22%3A%22%22%2C%22BackCaseInTime_0%22%3Afalse%2C%22BackCaseInTime_1%22%3Afalse%2C%22AlltimeTypeValue%22%3A%22%22%2C%22AlltimeTypeText%22%3A%22%22%2C%22AlltimeType_0%22%3Afalse%2C%22AlltimeType_1%22%3Afalse%2C%22AlltimeType_2%22%3Afalse%2C%22AlltimeType_3%22%3Afalse%2C%22MainCollDept%22%3A%22%22%2C%22SubCollDept%22%3A%22%22%2C%22TxtstrPriorityArea%22%3A%22%22%2C%22txtHeshiCount%22%3A%22%22%2C%22txtHechaCount%22%3A%22%22%2C%22discoverStartTime%22%3A%22%22%2C%22discoverEndTime%22%3A%22%22%2C%22preCreateStartTime%22%3A%22%22%2C%22preCreateEndTime%22%3A%22%22%2C%22dispatchStartTime%22%3A%22%22%2C%22dispatchEndTime%22%3A%22%22%2C%22CreateStartTime%22%3A%22%22%2C%22CreateEndTime%22%3A%22%22%2C%22solvingStartTime%22%3A%22%22%2C%22solvingEndTime%22%3A%22%22%2C%22endStartTime%22%3A%22%22%2C%22endEndTime%22%3A%22%22%2C%22TxtSimilarCase%22%3A%22%22%2C%22TxtSimilarNum%22%3A%22%22%2C%22TxtDispatchNum%22%3A%22%22%2C%22TxtEndUser%22%3A%22%22%2C%22btnsetcolumn%22%3A%22%E6%98%BE%E7%A4%BA%E6%9F%A5%E8%AF%A2%E5%88%97%22%2C%22btnSelecExelist%22%3A%22%E4%B8%8B%E8%BD%BD%E5%88%97%E8%A1%A8%22%2C%22btnSaveModule%22%3A%22%E4%BF%9D%E5%AD%98%E6%A8%A1%E6%9D%BF%22%2C%22btnSearchs%22%3A%22%E6%9F%A5++%E8%AF%A2%22%2C%22hdnFlag%22%3A%221%22%2C%22hdnTabCount%22%3A%223%22%2C%22hidTab%22%3A%220%22%2C%22Hidcount%22%3A%22%22%2C%22hidUseItemID%22%3A%22%22%2C%22hidDept%22%3A%22%22%2C%22hidOwnerName%22%3A%22%22%2C%22hidCaseBelongLevel%22%3A%22%22%2C%22hidStreetCode%22%3A%22%22%2C%22hidStreetName%22%3A%22%22%2C%22hidCommunityCode%22%3A%22%22%2C%22hidCommunityName%22%3A%22%22%2C%22hidgridCode%22%3A%22%22%2C%22hidgridName%22%3A%22%22%2C%22hidgridtype%22%3A%22%22%2C%22hidgridtypeName%22%3A%22%22%2C%22hidnewworkCode%22%3A%22%22%2C%22hidnewworkName%22%3A%22%22%2C%22hidnewgridCode%22%3A%22%22%2C%22hidnewgridkName%22%3A%22%22%2C%22hidSourceID%22%3A%22%22%2C%22hidSourceName%22%3A%22%22%2C%22HidCurDeptLv%22%3A%22%22%2C%22HidCurStreetCode%22%3A%22%22%2C%22HidHeChaDeptCode%22%3A%22%22%2C%22HidHeChaDeptName%22%3A%22%22%2C%22HidBeforeCollDept%22%3A%2220601%22%2C%22HidBeforeCollDeptName%22%3A%22%E8%B5%B5%E5%B7%B7%E9%95%87%22%2C%22HidMainCollDept%22%3A%22%22%2C%22HidMainCollDeptName%22%3A%22%22%2C%22HidSubCollDept%22%3A%22%22%2C%22HidSubCollDeptName%22%3A%22%22%2C%22HidMainDeptCode%22%3A%2220601%22%2C%22HidMainDeptName%22%3A%22%E8%B5%B5%E5%B7%B7%E9%95%87%22%2C%22hidSubDeptCode%22%3A%22%22%2C%22hidSubDeptName%22%3A%22%22%2C%22HidDifferentID%22%3A%22%22%2C%22HidType%22%3A%22%22%2C%22HidTypename%22%3A%22%22%2C%22HidMEBClass%22%3A%22%22%2C%22HidMEBClassName%22%3A%22%22%2C%22HidMESClass%22%3A%22%22%2C%22HidMESClassName%22%3A%22%22%2C%22HidSonClass%22%3A%22%22%2C%22HidSonClassName%22%3A%22%22%2C%22HidATClass%22%3A%22%22%2C%22HidATClassName%22%3A%22%22%2C%22HidTypeDifferent%22%3A%22%22%2C%22HidRelationCase%22%3A%22%22%2C%22HidA0383%22%3A%22%22%2C%22selectedTime%22%3A%2201%22%2C%22ddl_IsMainCase%22%3A%2210%22%2C%22ddl_Casebelonging%22%3A%22-1%22%2C%22ddlKeyList%22%3A%22-1%22%2C%22ddlSort%22%3A%22discovertime%22%2C%22ddlDesAsc%22%3A%22desc%22%2C%22select_new_street%22%3Anull%2C%22select_gridtype%22%3Anull%2C%22select_new_workgrid%22%3Anull%2C%22select_new_grid%22%3Anull%2C%22select_community%22%3A%22-1%22%2C%22select_grid%22%3A%22-1%22%2C%22InputArea%22%3Anull%2C%22ddlMEBClass%22%3A%22-1%22%2C%22ddlMESClass%22%3A%22-1%22%2C%22ddlSonClass%22%3A%22-1%22%2C%22ddlAtClass%22%3A%22-1%22%2C%22ddlApproach%22%3A%22-1%22%2C%22ddlUrgentdegree%22%3A%22-1%22%2C%22ddl_ServiceType%22%3A%22-1%22%2C%22ddlIsThreatened%22%3A%22-1%22%2C%22ddlIndustry%22%3Anull%2C%22ddlIsWeiXian%22%3A%22-1%22%2C%22ddlisPriorityArea%22%3A%22-1%22%2C%22ddlRiskLevel%22%3A%22-1%22%2C%22ddl_WorkTypes%22%3A%22-1%22%2C%22ddlWGCallBack%22%3A%22-1%22%2C%22DDLCompareHeshi%22%3A%22-1%22%2C%22DDLCompare%22%3A%22-1%22%2C%22ddlOverTimeCheck%22%3A%22-1%22%2C%22ddlIsWaiValue%22%3A%22-1%22%2C%22ddlWaiManYiDu%22%3A%22-1%22%2C%22ddlWaiFuWu%22%3A%22-1%22%2C%22dllCaseValuation%22%3A%22-1%22%2C%22ddl_IsFeedBack%22%3A%22-1%22%2C%22hcMyd%22%3A%22-1%22%2C%22ddlTelask%22%3A%22-1%22%2C%22ddlIsFirstContract%22%3A%22-1%22%2C%22ddlOverType%22%3A%22-1%22%2C%22ddlIsReply%22%3A%22-1%22%2C%22hfMyd%22%3A%22-1%22%2C%22ddlTaiDuManYi%22%3A%22-1%22%2C%22ddlHTelask%22%3A%22-1%22%2C%22ddlHIsFirstContact%22%3A%22-1%22%2C%22ddlHOverType%22%3A%22-1%22%2C%22ddlIsOver%22%3A%22-1%22%2C%22ddlAllManyi%22%3A%22-1%22%2C%22ddlGuoChenManyi%22%3A%22-1%22%2C%22ddlHResultType%22%3A%22-1%22%2C%22ddlHasLead%22%3A%22-1%22%2C%22ddlLEADERHANDTYPE%22%3A%22-1%22%2C%22ddlHasTenType%22%3A%22-1%22%2C%22ddlShijiHasTenType%22%3A%22-1%22%2C%22ddlFirstContact%22%3A%22-1%22%2C%22ddlSatisfied%22%3A%22-1%22%2C%22ddlFactType%22%3A%22-1%22%2C%22ddlViewInfo%22%3A%22-1%22%2C%22ddlAppealType%22%3A%22-1%22%2C%22ddlReplyType%22%3A%22-1%22%2C%22ddlIsPublic%22%3A%22-1%22%2C%22ddlBanliResult%22%3A%22-1%22%2C%22ddlIsCaseEnd%22%3A%22-1%22%2C%22ddlIsTypical%22%3A%22-1%22%2C%22ddlIsStubborn%22%3A%22-1%22%2C%22ddlIsSimilar%22%3A%22-1%22%2C%22ddlSimilarNum%22%3A%22-1%22%2C%22ddl_IsNew%22%3A%22-1%22%2C%22ddl_IsBackBill%22%3A%22-1%22%2C%22ddlIsTimeEnd%22%3A%22-1%22%2C%22ddlDispatchNum%22%3A%22-1%22%2C%22ddlIsStand%22%3A%22-1%22%2C%22ddlIsFast%22%3A%22-1%22%2C%22ddlIsSimplify%22%3A%22-1%22%2C%22ddlIsImage%22%3A%22-1%22%2C%22ddlCheckImage%22%3A%22-1%22%7D'
        body = body.format(start=self.start,end=self.end)
        #print(body)
        url = 'http://10.231.18.25/CITYGRID.QUERY/XinZeng/GetCondition'
        requests.post(url,headers=self.headers,data=body,proxies=self.proxies)

    def get_page(self,pageindex):
        body ='__VIEWSTATE=%2FwEPDwUKLTI3NzQ5NDQyOA8WAh4KaVBhZ2VDb3VudAKt8woWAgIDD2QWAgIBD2QWAmYPDxYCHgdWaXNpYmxlZ2RkZDrrWBDk%2BI%2BxV9iFwgY7Chlm%2BgEeQ6%2BHcDpSOuvX%2FHJ9&__EVENTVALIDATION=%2FwEWBwLiyLGMDAKDxqfyBwLxkIDFDgLRtveLBwKln%2FPuCgK3%2B56LBAKFt7SHCQLqYFykqOjbdpSYLK3lXULw0RUuysj%2BX4UbjKGJQ%2FG6&pageindex={pageindex}&hdn_excelfile=OutputExcel.aspx%3Fpage%3DInfoMSearchConfigurableNew%26&Hidden_Index=&btnSearch=&txtSQL=SELECT+STATUSNAME+%E6%A1%88%E4%BB%B6%E7%8A%B6%E6%80%81%2CTASKID+%E4%BB%BB%E5%8A%A1%E5%8F%B7%2CINFOSOURCENAME+%E6%A1%88%E4%BB%B6%E6%9D%A5%E6%BA%90%2CTO_CHAR+%28DISCOVERTIME%2C+%27yyyy-mm-dd+hh24%3Ami%27%29+%E5%8F%91%E7%8E%B0%E6%97%B6%E9%97%B4%2CINFOTYPENAME+%E6%A1%88%E4%BB%B6%E5%B1%9E%E6%80%A7%2CINFOBCNAME+%E6%A1%88%E4%BB%B6%E5%A4%A7%E7%B1%BB%2CINFOSCNAME+%E6%A1%88%E4%BB%B6%E5%B0%8F%E7%B1%BB%2CINFOZCNAME+%E6%A1%88%E4%BB%B6%E5%AD%90%E7%B1%BB%2CSTREETNAME+%E8%A1%97%E9%95%87%2CAddress+%E5%8F%91%E7%94%9F%E5%9C%B0%E5%9D%80%2CCITYGRID.FN_GET_PRIORITYAREANAME%28PRIORITYAREA%29+%E9%87%8D%E7%82%B9%E5%8C%BA%E5%9F%9F%2CTO_CHAR+%28DISPATCHTIME%2C+%27yyyy-mm-dd+hh24%3Ami%27%29+%E6%B4%BE%E9%81%A3%E6%97%B6%E9%97%B4%2CTO_CHAR+%28MIDDISPATCHTIME%2C+%27yyyy-mm-dd+hh24%3Ami%27%29+%E5%86%8D%E6%B4%BE%E9%81%A3%E4%B8%AD%E9%97%B4%E6%B4%BE%E9%81%A3%E6%97%B6%E9%97%B4%2CCITYGRID.F_REC_MAINDEPTNAME%28EXECUTEDEPTCODE%2CDEPTCODE%2CTASKID%29+%E4%B8%BB%E8%B4%A3%E9%83%A8%E9%97%A8%2CCITYGRID.F_REC_THREEDEPTNAME%28EXECUTEDEPTCODE%2CDEPTCODE%2CTASKID%29+%E4%B8%89%E7%BA%A7%E4%B8%BB%E8%B4%A3%E9%83%A8%E9%97%A8%2CTO_CHAR+%28ENDTIME%2C+%27yyyy-mm-dd+hh24%3Ami%27%29+%E7%BB%93%E6%A1%88%E6%97%B6%E9%97%B4++FROM+%28SELECT+tt.*%2C+ROWNUM+AS+rowno++FROM+%28SELECT+*+FROM+CITYGRID.T_TASKINFO+main++WHERE+1%3D1+%29tt++WHERE+ROWNUM+%3C%3D+20%29+table_alias+WHERE+table_alias.rowno+%3E10'
        
        body=body.format(pageindex=pageindex)
        
        url="http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchResultAllFlat.aspx?IsQuery=1"
        rt=requests.post(url,data=body,headers=self.headers,proxies=self.proxies) 
        return rt.content

    def parse_page(self,content):
        soup = BeautifulSoup(content)
        rows=[]
        for tr in soup.select('#userlist tr')[1:]:
            ls = tr.select('td')
            ls = [x.text for x in ls]
            rows.append(ls)
        mt = re.search('Pagination.Refresh\(parseInt\(\'(\d+)\'\)',content)
        if mt:
            total = int(mt.group(1))
        #else:
            #print(content)
        return rows,total    

    def filter_has(self,rows):
        return rows

    def get_coord(self,taskid):
        """
        @
        http://10.231.18.25/CityGrid/CaseOperate_flat/ParticularDisplayInfo.aspx?taskid=1803G6099867
        """
        url = 'http://10.231.18.25/CityGrid/CaseOperate_flat/ParticularDisplayInfo.aspx?taskid=%s'%taskid
        rt  = requests.get(url,proxies=self.proxies)
        soup = BeautifulSoup(rt.content)
        return soup.select('#lbl_xy')[0].text

    



