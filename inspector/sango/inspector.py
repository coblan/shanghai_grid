# encoding:utf-8
"""
这个代码不用了，现在用manage.py case 命令定时去三高获取数据
"""
from __future__ import unicode_literals

import requests
from django.conf import settings
from ..models import InspectorCase
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

class InspectorCaseConnecter(object):
    def __init__(self,start,end,code):
        self.start=start
        self.end=end
        self.code=code
        self.proxies = getattr(settings,'DATA_PROXY',{})
        self.content=None
    
    def update(self):
        self._req_first()
        self._req_second()
        InspectorCase.objects.update_or_create(code=self.code,defaults={'page': self.content})
        
    def _req_first(self):
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
            'Origin':'http://10.231.18.25',
            'X-Requested-With':'XMLHttpRequest',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Content-Type':'application/x-www-form-urlencoded',
            'Referer':'http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchConditionFlat.aspx',
            # 'Cookie':'ASP.NET_SessionId=0jomini1le3yjhfozaby3bcj; ScreenWidth=2560; ScreenHeight=1440; .ASPXAUTH=454EEB8DB6AF0C3D7375D4D1E09490A8B5ED8422477F833EECEC9EE94869BA75353A463969A74E2CF5F7FC8F4B0A699A1C295F719DF0ABE22C16711430D602AAD0486E6F73E533169B997BC46BEEB09FE070075148A082EA248474001926859D11A3770DCD26BE6F29185B66F06B4D7E4F5184390539BFFBB0845986D315B5A58E53BD811246C649643BD3CFDE29B08E'
            'Cookie':'ASP.NET_SessionId=0jomini1le3yjhfozaby3bcj; ScreenWidth=2560; ScreenHeight=1440;'
           
        }
        
        
        var_dict={
            #'inspector':'31189242',
            #'start':'2017121400',
            #'end':'2017121500',
            'dept':'20601', # 赵项代码
        }
        
        #body="""arrstring:{"startDate":"2018-02-01","endDate":"2018-02-01","btnTime":"","hidSelectedTime":"","startHour":"00:00","endHour":"23:59","MainExeDept":"","SubExeDept":"","RbStatus":true,"RbSolvingStatus":false,"hidStatusID":"","hidStatusName":"","mainStatus_0":false,"mainStatus_1":false,"mainStatus_2":false,"mainStatus_3":false,"mainStatus_4":false,"mainStatus_5":false,"mainStatus_6":false,"mainStatus_7":false,"mainStatus_8":false,"mainStatus_9":false,"mainStatus_10":false,"mainStatus_11":false,"mainStatus_12":false,"mainStatus_13":false,"mainStatus_14":false,"mainStatus_15":false,"mainStatus_16":false,"mainStatus_17":false,"mainStatus_18":false,"hidSolStatus":"","hidSolStatusName":"","SolvingStatus_0":false,"SolvingStatus_1":false,"SolvingStatus_2":false,"SolvingStatus_3":false,"SolvingStatus_4":false,"SolvingStatus_5":false,"SolvingStatus_6":false,"SolvingStatus_7":false,"SolvingStatus_8":false,"SolvingStatus_9":false,"SolvingStatus_10":false,"SolvingStatus_11":false,"mainTxt":"31189633","txtAddress":"","TakeCaseInTimeValue":"","TakeCaseInTimeText":"","TakeCaseInTime_0":false,"TakeCaseInTime_1":false,"SovlingtimeTypeValue":"","SovlingtimeTypeText":"","SovlingtimeType_0":false,"SovlingtimeType_1":false,"SovlingtimeType_2":false,"SovlingtimeType_3":false,"BackCaseInTimeValue":"","BackCaseInTimeText":"","BackCaseInTime_0":false,"BackCaseInTime_1":false,"AlltimeTypeValue":"","AlltimeTypeText":"","AlltimeType_0":false,"AlltimeType_1":false,"AlltimeType_2":false,"AlltimeType_3":false,"MainCollDept":"","SubCollDept":"","TxtstrPriorityArea":"","txtHeshiCount":"","txtHechaCount":"","discoverStartTime":"","discoverEndTime":"","preCreateStartTime":"","preCreateEndTime":"","dispatchStartTime":"","dispatchEndTime":"","CreateStartTime":"","CreateEndTime":"","solvingStartTime":"","solvingEndTime":"","endStartTime":"","endEndTime":"","TxtSimilarCase":"","btnsetcolumn":"显示查询列","btnSelecExelist":"下载列表","btnSaveModule":"保存模板","btnSearchs":"查  询","hdnFlag":"1","hdnTabCount":"3","hidTab":"0","Hidcount":"","hidUseItemID":"","hidDept":"","hidOwnerName":"","hidCaseBelongLevel":"","hidStreetCode":"","hidStreetName":"","hidCommunityCode":"","hidCommunityName":"","hidgridCode":"","hidgridName":"","hidgridtype":"","hidgridtypeName":"","hidnewworkCode":"","hidnewworkName":"","hidnewgridCode":"","hidnewgridkName":"","hidSourceID":"","hidSourceName":"","HidCurDeptLv":"","HidCurStreetCode":"","HidHeChaDeptCode":"","HidHeChaDeptName":"","HidBeforeCollDept":"","HidBeforeCollDeptName":"","HidMainCollDept":"","HidMainCollDeptName":"","HidSubCollDept":"","HidSubCollDeptName":"","HidMainDeptCode":"","HidMainDeptName":"","hidSubDeptCode":"","hidSubDeptName":"","HidDifferentID":"","HidType":"","HidTypename":"","HidMEBClass":"","HidMEBClassName":"","HidMESClass":"","HidMESClassName":"","HidSonClass":"","HidSonClassName":"","HidATClass":"","HidATClassName":"","HidTypeDifferent":"","HidRelationCase":"","HidA0383":"","selectedTime":"01","ddl_IsMainCase":"10","ddl_Casebelonging":"-1","ddlKeyList":"5","ddlSort":"-1","ddlDesAsc":"desc","select_new_street":null,"select_gridtype":null,"select_new_workgrid":null,"select_new_grid":null,"select_community":"-1","select_grid":"-1","InputArea":null,"ddlMEBClass":"-1","ddlMESClass":"-1","ddlSonClass":"-1","ddlAtClass":"-1","ddlApproach":"-1","ddlUrgentdegree":"-1","ddl_ServiceType":"-1","ddlIsThreatened":"-1","ddlIndustry":null,"ddlIsWeiXian":"-1","ddlisPriorityArea":"-1","ddlRiskLevel":"-1","ddl_WorkTypes":"-1","DDLCompareHeshi":"-1","DDLCompare":"-1","ddlOverTimeCheck":"-1","dllCaseValuation":"-1","ddl_IsFeedBack":"-1","hcMyd":"-1","ddlIsFirstContract":"-1","hfMyd":"-1","ddlIsWaiValue":"-1","ddlWaiManYiDu":"-1","ddlWaiFuWu":"-1","ddlHasLead":"-1","ddlLEADERHANDTYPE":"-1","ddlHasTenType":"-1","ddlIsCaseEnd":"-1","ddlIsTypical":"-1","ddlIsStubborn":"-1","ddlIsSimilar":"-1","ddl_IsNew":"-1","ddl_IsBackBill":"-1"}"""
        # body ='arrstring=%7B%22startDate%22%3A%222018-02-01%22%2C%22endDate%22%3A%222018-02-01%22%2C%22btnTime%22%3A%22%22%2C%22hidSelectedTime%22%3A%22%22%2C%22startHour%22%3A%2200%3A00%22%2C%22endHour%22%3A%2223%3A59%22%2C%22MainExeDept%22%3A%22%22%2C%22SubExeDept%22%3A%22%22%2C%22RbStatus%22%3Atrue%2C%22RbSolvingStatus%22%3Afalse%2C%22hidStatusID%22%3A%22%22%2C%22hidStatusName%22%3A%22%22%2C%22mainStatus_0%22%3Afalse%2C%22mainStatus_1%22%3Afalse%2C%22mainStatus_2%22%3Afalse%2C%22mainStatus_3%22%3Afalse%2C%22mainStatus_4%22%3Afalse%2C%22mainStatus_5%22%3Afalse%2C%22mainStatus_6%22%3Afalse%2C%22mainStatus_7%22%3Afalse%2C%22mainStatus_8%22%3Afalse%2C%22mainStatus_9%22%3Afalse%2C%22mainStatus_10%22%3Afalse%2C%22mainStatus_11%22%3Afalse%2C%22mainStatus_12%22%3Afalse%2C%22mainStatus_13%22%3Afalse%2C%22mainStatus_14%22%3Afalse%2C%22mainStatus_15%22%3Afalse%2C%22mainStatus_16%22%3Afalse%2C%22mainStatus_17%22%3Afalse%2C%22mainStatus_18%22%3Afalse%2C%22hidSolStatus%22%3A%22%22%2C%22hidSolStatusName%22%3A%22%22%2C%22SolvingStatus_0%22%3Afalse%2C%22SolvingStatus_1%22%3Afalse%2C%22SolvingStatus_2%22%3Afalse%2C%22SolvingStatus_3%22%3Afalse%2C%22SolvingStatus_4%22%3Afalse%2C%22SolvingStatus_5%22%3Afalse%2C%22SolvingStatus_6%22%3Afalse%2C%22SolvingStatus_7%22%3Afalse%2C%22SolvingStatus_8%22%3Afalse%2C%22SolvingStatus_9%22%3Afalse%2C%22SolvingStatus_10%22%3Afalse%2C%22SolvingStatus_11%22%3Afalse%2C%22mainTxt%22%3A%2231189633%22%2C%22txtAddress%22%3A%22%22%2C%22TakeCaseInTimeValue%22%3A%22%22%2C%22TakeCaseInTimeText%22%3A%22%22%2C%22TakeCaseInTime_0%22%3Afalse%2C%22TakeCaseInTime_1%22%3Afalse%2C%22SovlingtimeTypeValue%22%3A%22%22%2C%22SovlingtimeTypeText%22%3A%22%22%2C%22SovlingtimeType_0%22%3Afalse%2C%22SovlingtimeType_1%22%3Afalse%2C%22SovlingtimeType_2%22%3Afalse%2C%22SovlingtimeType_3%22%3Afalse%2C%22BackCaseInTimeValue%22%3A%22%22%2C%22BackCaseInTimeText%22%3A%22%22%2C%22BackCaseInTime_0%22%3Afalse%2C%22BackCaseInTime_1%22%3Afalse%2C%22AlltimeTypeValue%22%3A%22%22%2C%22AlltimeTypeText%22%3A%22%22%2C%22AlltimeType_0%22%3Afalse%2C%22AlltimeType_1%22%3Afalse%2C%22AlltimeType_2%22%3Afalse%2C%22AlltimeType_3%22%3Afalse%2C%22MainCollDept%22%3A%22%22%2C%22SubCollDept%22%3A%22%22%2C%22TxtstrPriorityArea%22%3A%22%22%2C%22txtHeshiCount%22%3A%22%22%2C%22txtHechaCount%22%3A%22%22%2C%22discoverStartTime%22%3A%22%22%2C%22discoverEndTime%22%3A%22%22%2C%22preCreateStartTime%22%3A%22%22%2C%22preCreateEndTime%22%3A%22%22%2C%22dispatchStartTime%22%3A%22%22%2C%22dispatchEndTime%22%3A%22%22%2C%22CreateStartTime%22%3A%22%22%2C%22CreateEndTime%22%3A%22%22%2C%22solvingStartTime%22%3A%22%22%2C%22solvingEndTime%22%3A%22%22%2C%22endStartTime%22%3A%22%22%2C%22endEndTime%22%3A%22%22%2C%22TxtSimilarCase%22%3A%22%22%2C%22btnsetcolumn%22%3A%22%E6%98%BE%E7%A4%BA%E6%9F%A5%E8%AF%A2%E5%88%97%22%2C%22btnSelecExelist%22%3A%22%E4%B8%8B%E8%BD%BD%E5%88%97%E8%A1%A8%22%2C%22btnSaveModule%22%3A%22%E4%BF%9D%E5%AD%98%E6%A8%A1%E6%9D%BF%22%2C%22btnSearchs%22%3A%22%E6%9F%A5++%E8%AF%A2%22%2C%22hdnFlag%22%3A%221%22%2C%22hdnTabCount%22%3A%223%22%2C%22hidTab%22%3A%220%22%2C%22Hidcount%22%3A%22%22%2C%22hidUseItemID%22%3A%22%22%2C%22hidDept%22%3A%22%22%2C%22hidOwnerName%22%3A%22%22%2C%22hidCaseBelongLevel%22%3A%22%22%2C%22hidStreetCode%22%3A%22%22%2C%22hidStreetName%22%3A%22%22%2C%22hidCommunityCode%22%3A%22%22%2C%22hidCommunityName%22%3A%22%22%2C%22hidgridCode%22%3A%22%22%2C%22hidgridName%22%3A%22%22%2C%22hidgridtype%22%3A%22%22%2C%22hidgridtypeName%22%3A%22%22%2C%22hidnewworkCode%22%3A%22%22%2C%22hidnewworkName%22%3A%22%22%2C%22hidnewgridCode%22%3A%22%22%2C%22hidnewgridkName%22%3A%22%22%2C%22hidSourceID%22%3A%22%22%2C%22hidSourceName%22%3A%22%22%2C%22HidCurDeptLv%22%3A%22%22%2C%22HidCurStreetCode%22%3A%22%22%2C%22HidHeChaDeptCode%22%3A%22%22%2C%22HidHeChaDeptName%22%3A%22%22%2C%22HidBeforeCollDept%22%3A%22%22%2C%22HidBeforeCollDeptName%22%3A%22%22%2C%22HidMainCollDept%22%3A%22%22%2C%22HidMainCollDeptName%22%3A%22%22%2C%22HidSubCollDept%22%3A%22%22%2C%22HidSubCollDeptName%22%3A%22%22%2C%22HidMainDeptCode%22%3A%22%22%2C%22HidMainDeptName%22%3A%22%22%2C%22hidSubDeptCode%22%3A%22%22%2C%22hidSubDeptName%22%3A%22%22%2C%22HidDifferentID%22%3A%22%22%2C%22HidType%22%3A%22%22%2C%22HidTypename%22%3A%22%22%2C%22HidMEBClass%22%3A%22%22%2C%22HidMEBClassName%22%3A%22%22%2C%22HidMESClass%22%3A%22%22%2C%22HidMESClassName%22%3A%22%22%2C%22HidSonClass%22%3A%22%22%2C%22HidSonClassName%22%3A%22%22%2C%22HidATClass%22%3A%22%22%2C%22HidATClassName%22%3A%22%22%2C%22HidTypeDifferent%22%3A%22%22%2C%22HidRelationCase%22%3A%22%22%2C%22HidA0383%22%3A%22%22%2C%22selectedTime%22%3A%2201%22%2C%22ddl_IsMainCase%22%3A%2210%22%2C%22ddl_Casebelonging%22%3A%22-1%22%2C%22ddlKeyList%22%3A%225%22%2C%22ddlSort%22%3A%22-1%22%2C%22ddlDesAsc%22%3A%22desc%22%2C%22select_new_street%22%3Anull%2C%22select_gridtype%22%3Anull%2C%22select_new_workgrid%22%3Anull%2C%22select_new_grid%22%3Anull%2C%22select_community%22%3A%22-1%22%2C%22select_grid%22%3A%22-1%22%2C%22InputArea%22%3Anull%2C%22ddlMEBClass%22%3A%22-1%22%2C%22ddlMESClass%22%3A%22-1%22%2C%22ddlSonClass%22%3A%22-1%22%2C%22ddlAtClass%22%3A%22-1%22%2C%22ddlApproach%22%3A%22-1%22%2C%22ddlUrgentdegree%22%3A%22-1%22%2C%22ddl_ServiceType%22%3A%22-1%22%2C%22ddlIsThreatened%22%3A%22-1%22%2C%22ddlIndustry%22%3Anull%2C%22ddlIsWeiXian%22%3A%22-1%22%2C%22ddlisPriorityArea%22%3A%22-1%22%2C%22ddlRiskLevel%22%3A%22-1%22%2C%22ddl_WorkTypes%22%3A%22-1%22%2C%22DDLCompareHeshi%22%3A%22-1%22%2C%22DDLCompare%22%3A%22-1%22%2C%22ddlOverTimeCheck%22%3A%22-1%22%2C%22dllCaseValuation%22%3A%22-1%22%2C%22ddl_IsFeedBack%22%3A%22-1%22%2C%22hcMyd%22%3A%22-1%22%2C%22ddlIsFirstContract%22%3A%22-1%22%2C%22hfMyd%22%3A%22-1%22%2C%22ddlIsWaiValue%22%3A%22-1%22%2C%22ddlWaiManYiDu%22%3A%22-1%22%2C%22ddlWaiFuWu%22%3A%22-1%22%2C%22ddlHasLead%22%3A%22-1%22%2C%22ddlLEADERHANDTYPE%22%3A%22-1%22%2C%22ddlHasTenType%22%3A%22-1%22%2C%22ddlIsCaseEnd%22%3A%22-1%22%2C%22ddlIsTypical%22%3A%22-1%22%2C%22ddlIsStubborn%22%3A%22-1%22%2C%22ddlIsSimilar%22%3A%22-1%22%2C%22ddl_IsNew%22%3A%22-1%22%2C%22ddl_IsBackBill%22%3A%22-1%22%7D'
    
        body ='arrstring=%7B%22startDate%22%3A%22{start}%22%2C%22endDate%22%3A%22{end}%22%2C%22btnTime%22%3A%22%22%2C%22hidSelectedTime%22%3A%22%22%2C%22startHour%22%3A%2200%3A00%22%2C%22endHour%22%3A%2223%3A59%22%2C%22MainExeDept%22%3A%22%22%2C%22SubExeDept%22%3A%22%22%2C%22RbStatus%22%3Atrue%2C%22RbSolvingStatus%22%3Afalse%2C%22hidStatusID%22%3A%22%22%2C%22hidStatusName%22%3A%22%22%2C%22mainStatus_0%22%3Afalse%2C%22mainStatus_1%22%3Afalse%2C%22mainStatus_2%22%3Afalse%2C%22mainStatus_3%22%3Afalse%2C%22mainStatus_4%22%3Afalse%2C%22mainStatus_5%22%3Afalse%2C%22mainStatus_6%22%3Afalse%2C%22mainStatus_7%22%3Afalse%2C%22mainStatus_8%22%3Afalse%2C%22mainStatus_9%22%3Afalse%2C%22mainStatus_10%22%3Afalse%2C%22mainStatus_11%22%3Afalse%2C%22mainStatus_12%22%3Afalse%2C%22mainStatus_13%22%3Afalse%2C%22mainStatus_14%22%3Afalse%2C%22mainStatus_15%22%3Afalse%2C%22mainStatus_16%22%3Afalse%2C%22mainStatus_17%22%3Afalse%2C%22mainStatus_18%22%3Afalse%2C%22hidSolStatus%22%3A%22%22%2C%22hidSolStatusName%22%3A%22%22%2C%22SolvingStatus_0%22%3Afalse%2C%22SolvingStatus_1%22%3Afalse%2C%22SolvingStatus_2%22%3Afalse%2C%22SolvingStatus_3%22%3Afalse%2C%22SolvingStatus_4%22%3Afalse%2C%22SolvingStatus_5%22%3Afalse%2C%22SolvingStatus_6%22%3Afalse%2C%22SolvingStatus_7%22%3Afalse%2C%22SolvingStatus_8%22%3Afalse%2C%22SolvingStatus_9%22%3Afalse%2C%22SolvingStatus_10%22%3Afalse%2C%22SolvingStatus_11%22%3Afalse%2C%22mainTxt%22%3A%22{code}%22%2C%22txtAddress%22%3A%22%22%2C%22TakeCaseInTimeValue%22%3A%22%22%2C%22TakeCaseInTimeText%22%3A%22%22%2C%22TakeCaseInTime_0%22%3Afalse%2C%22TakeCaseInTime_1%22%3Afalse%2C%22SovlingtimeTypeValue%22%3A%22%22%2C%22SovlingtimeTypeText%22%3A%22%22%2C%22SovlingtimeType_0%22%3Afalse%2C%22SovlingtimeType_1%22%3Afalse%2C%22SovlingtimeType_2%22%3Afalse%2C%22SovlingtimeType_3%22%3Afalse%2C%22BackCaseInTimeValue%22%3A%22%22%2C%22BackCaseInTimeText%22%3A%22%22%2C%22BackCaseInTime_0%22%3Afalse%2C%22BackCaseInTime_1%22%3Afalse%2C%22AlltimeTypeValue%22%3A%22%22%2C%22AlltimeTypeText%22%3A%22%22%2C%22AlltimeType_0%22%3Afalse%2C%22AlltimeType_1%22%3Afalse%2C%22AlltimeType_2%22%3Afalse%2C%22AlltimeType_3%22%3Afalse%2C%22MainCollDept%22%3A%22%22%2C%22SubCollDept%22%3A%22%22%2C%22TxtstrPriorityArea%22%3A%22%22%2C%22txtHeshiCount%22%3A%22%22%2C%22txtHechaCount%22%3A%22%22%2C%22discoverStartTime%22%3A%22%22%2C%22discoverEndTime%22%3A%22%22%2C%22preCreateStartTime%22%3A%22%22%2C%22preCreateEndTime%22%3A%22%22%2C%22dispatchStartTime%22%3A%22%22%2C%22dispatchEndTime%22%3A%22%22%2C%22CreateStartTime%22%3A%22%22%2C%22CreateEndTime%22%3A%22%22%2C%22solvingStartTime%22%3A%22%22%2C%22solvingEndTime%22%3A%22%22%2C%22endStartTime%22%3A%22%22%2C%22endEndTime%22%3A%22%22%2C%22TxtSimilarCase%22%3A%22%22%2C%22btnsetcolumn%22%3A%22%E6%98%BE%E7%A4%BA%E6%9F%A5%E8%AF%A2%E5%88%97%22%2C%22btnSelecExelist%22%3A%22%E4%B8%8B%E8%BD%BD%E5%88%97%E8%A1%A8%22%2C%22btnSaveModule%22%3A%22%E4%BF%9D%E5%AD%98%E6%A8%A1%E6%9D%BF%22%2C%22btnSearchs%22%3A%22%E6%9F%A5++%E8%AF%A2%22%2C%22hdnFlag%22%3A%221%22%2C%22hdnTabCount%22%3A%223%22%2C%22hidTab%22%3A%220%22%2C%22Hidcount%22%3A%22%22%2C%22hidUseItemID%22%3A%22%22%2C%22hidDept%22%3A%22%22%2C%22hidOwnerName%22%3A%22%22%2C%22hidCaseBelongLevel%22%3A%22%22%2C%22hidStreetCode%22%3A%22%22%2C%22hidStreetName%22%3A%22%22%2C%22hidCommunityCode%22%3A%22%22%2C%22hidCommunityName%22%3A%22%22%2C%22hidgridCode%22%3A%22%22%2C%22hidgridName%22%3A%22%22%2C%22hidgridtype%22%3A%22%22%2C%22hidgridtypeName%22%3A%22%22%2C%22hidnewworkCode%22%3A%22%22%2C%22hidnewworkName%22%3A%22%22%2C%22hidnewgridCode%22%3A%22%22%2C%22hidnewgridkName%22%3A%22%22%2C%22hidSourceID%22%3A%22%22%2C%22hidSourceName%22%3A%22%22%2C%22HidCurDeptLv%22%3A%22%22%2C%22HidCurStreetCode%22%3A%22%22%2C%22HidHeChaDeptCode%22%3A%22%22%2C%22HidHeChaDeptName%22%3A%22%22%2C%22HidBeforeCollDept%22%3A%22%22%2C%22HidBeforeCollDeptName%22%3A%22%22%2C%22HidMainCollDept%22%3A%22%22%2C%22HidMainCollDeptName%22%3A%22%22%2C%22HidSubCollDept%22%3A%22%22%2C%22HidSubCollDeptName%22%3A%22%22%2C%22HidMainDeptCode%22%3A%22%22%2C%22HidMainDeptName%22%3A%22%22%2C%22hidSubDeptCode%22%3A%22%22%2C%22hidSubDeptName%22%3A%22%22%2C%22HidDifferentID%22%3A%22%22%2C%22HidType%22%3A%22%22%2C%22HidTypename%22%3A%22%22%2C%22HidMEBClass%22%3A%22%22%2C%22HidMEBClassName%22%3A%22%22%2C%22HidMESClass%22%3A%22%22%2C%22HidMESClassName%22%3A%22%22%2C%22HidSonClass%22%3A%22%22%2C%22HidSonClassName%22%3A%22%22%2C%22HidATClass%22%3A%22%22%2C%22HidATClassName%22%3A%22%22%2C%22HidTypeDifferent%22%3A%22%22%2C%22HidRelationCase%22%3A%22%22%2C%22HidA0383%22%3A%22%22%2C%22selectedTime%22%3A%2201%22%2C%22ddl_IsMainCase%22%3A%2210%22%2C%22ddl_Casebelonging%22%3A%22-1%22%2C%22ddlKeyList%22%3A%225%22%2C%22ddlSort%22%3A%22-1%22%2C%22ddlDesAsc%22%3A%22desc%22%2C%22select_new_street%22%3Anull%2C%22select_gridtype%22%3Anull%2C%22select_new_workgrid%22%3Anull%2C%22select_new_grid%22%3Anull%2C%22select_community%22%3A%22-1%22%2C%22select_grid%22%3A%22-1%22%2C%22InputArea%22%3Anull%2C%22ddlMEBClass%22%3A%22-1%22%2C%22ddlMESClass%22%3A%22-1%22%2C%22ddlSonClass%22%3A%22-1%22%2C%22ddlAtClass%22%3A%22-1%22%2C%22ddlApproach%22%3A%22-1%22%2C%22ddlUrgentdegree%22%3A%22-1%22%2C%22ddl_ServiceType%22%3A%22-1%22%2C%22ddlIsThreatened%22%3A%22-1%22%2C%22ddlIndustry%22%3Anull%2C%22ddlIsWeiXian%22%3A%22-1%22%2C%22ddlisPriorityArea%22%3A%22-1%22%2C%22ddlRiskLevel%22%3A%22-1%22%2C%22ddl_WorkTypes%22%3A%22-1%22%2C%22DDLCompareHeshi%22%3A%22-1%22%2C%22DDLCompare%22%3A%22-1%22%2C%22ddlOverTimeCheck%22%3A%22-1%22%2C%22dllCaseValuation%22%3A%22-1%22%2C%22ddl_IsFeedBack%22%3A%22-1%22%2C%22hcMyd%22%3A%22-1%22%2C%22ddlIsFirstContract%22%3A%22-1%22%2C%22hfMyd%22%3A%22-1%22%2C%22ddlIsWaiValue%22%3A%22-1%22%2C%22ddlWaiManYiDu%22%3A%22-1%22%2C%22ddlWaiFuWu%22%3A%22-1%22%2C%22ddlHasLead%22%3A%22-1%22%2C%22ddlLEADERHANDTYPE%22%3A%22-1%22%2C%22ddlHasTenType%22%3A%22-1%22%2C%22ddlIsCaseEnd%22%3A%22-1%22%2C%22ddlIsTypical%22%3A%22-1%22%2C%22ddlIsStubborn%22%3A%22-1%22%2C%22ddlIsSimilar%22%3A%22-1%22%2C%22ddl_IsNew%22%3A%22-1%22%2C%22ddl_IsBackBill%22%3A%22-1%22%7D'
        body=body.format(start=self.start,end=self.end,code=self.code)
        
        url="http://10.231.18.25/CITYGRID.QUERY/XinZeng/GetCondition"
        
        rt=requests.post(url,headers=headers,data=body,proxies=self.proxies) 
    
    def _req_second(self):
        url2= 'http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchResultAllFlat.aspx?IsQuery=1'

        header2={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
            'Origin':'http://10.231.18.25',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Referer':'http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchConditionFlat.aspx',
            # 'Cookie':'ASP.NET_SessionId=0jomini1le3yjhfozaby3bcj; ScreenWidth=2560; ScreenHeight=1440; .ASPXAUTH=454EEB8DB6AF0C3D7375D4D1E09490A8B5ED8422477F833EECEC9EE94869BA75353A463969A74E2CF5F7FC8F4B0A699A1C295F719DF0ABE22C16711430D602AAD0486E6F73E533169B997BC46BEEB09FE070075148A082EA248474001926859D11A3770DCD26BE6F29185B66F06B4D7E4F5184390539BFFBB0845986D315B5A58E53BD811246C649643BD3CFDE29B08E'
            'Cookie':'ASP.NET_SessionId=0jomini1le3yjhfozaby3bcj; ScreenWidth=2560; ScreenHeight=1440;'
        }
            
        rt2 = requests.get(url2,headers=header2,proxies=self.proxies)
        self.content =  rt2.content
    
    def get_page(self):
        content = ""
        try:
            record  = InspectorCase.objects.get(code = self.code)
            content =  record.page
        except InspectorCase.DoseNotExist:
            self.update()
            content =  self.content
        
        soup = BeautifulSoup(content)
        host = 'http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchResultFlat.aspx?IsQuery=1'
        for script in soup.select('script'):
            if script.get('src'):
                script.attrs['src']=urljoin(host,script.attrs['src'])
        for link in soup.select('link'):
            if link.get('href'):
                link.attrs['href'] = urljoin(host,link.attrs['href'])
        return  unicode(soup)
        
    
    def get_number(self):
        if not self.content:
            self.update()
        number = self._parse(self.content)
        return number
    
    def _parse(self,content):
        mt = re.search(r"Pagination.Refresh\(parseInt\('(\d+)'",content)
        if mt:
            return mt.group(1)
        else:
            return 0
    
    
    