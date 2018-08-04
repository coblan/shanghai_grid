# encoding:utf-8
from django.core.management.base import BaseCommand
import requests
import xmltodict
from inspector.models import Inspector
from django.conf import settings
from helpers.director.kv import set_value
from bs4 import BeautifulSoup
import json
from django.utils.timezone import datetime
# import wingdbstub
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.proxies = getattr(settings,'DATA_PROXY',{})
        
        self.sess = requests.Session()
        
        self._req_first()
        self._req_second()
        content = self._req_table()
        table_data= self.parse_rt(content)
        json_str = json.dumps(table_data)
        self.save_json_str(json_str)
    
    def _req_first(self):
        today = datetime.now().date()
        today_str = unicode(today)
        
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
            'Origin':'http://10.231.18.25',
            'X-Requested-With':'XMLHttpRequest',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Content-Type':'application/x-www-form-urlencoded',
            'Referer':'http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchConditionFlat.aspx',
            # 'Cookie':'ASP.NET_SessionId=0jomini1le3yjhfozaby3bcj; ScreenWidth=2560; ScreenHeight=1440; .ASPXAUTH=454EEB8DB6AF0C3D7375D4D1E09490A8B5ED8422477F833EECEC9EE94869BA75353A463969A74E2CF5F7FC8F4B0A699A1C295F719DF0ABE22C16711430D602AAD0486E6F73E533169B997BC46BEEB09FE070075148A082EA248474001926859D11A3770DCD26BE6F29185B66F06B4D7E4F5184390539BFFBB0845986D315B5A58E53BD811246C649643BD3CFDE29B08E'
            'Cookie':'ASP.NET_SessionId=mlv4zdrstxjfcpn0n032q3qh; ScreenWidth=1920; ScreenHeight=1080; SearchColumn=CITYGRID.F_MAIN_STATUS(status)%26TASKID%26TO_CHAR+(DISCOVERTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)%26CITYGRID.F_REC_ISC_NAME_NEW(INFOBCCODE%2cINFOSCCODE%2cINFOTYPEID)%26CITYGRID.F_REC_STREETNAME(STREETCODE)%26Address%26KeeperSN%26TO_CHAR+(DISPATCHTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)%26TO_CHAR+(ENDTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)'
        }
        # body = """arrstring=%7B%22startDate%22%3A%222018-02-05%22%2C%22endDate%22%3A%222018-02-05%22%2C%22btnTime%22%3A%22%22%2C%22hidSelectedTime%22%3A%22%22%2C%22startHour%22%3A%2200%3A00%22%2C%22endHour%22%3A%2223%3A59%22%2C%22MainExeDept%22%3A%22%22%2C%22SubExeDept%22%3A%22%22%2C%22RbStatus%22%3Atrue%2C%22RbSolvingStatus%22%3Afalse%2C%22hidStatusID%22%3A%22%22%2C%22hidStatusName%22%3A%22%22%2C%22mainStatus_0%22%3Afalse%2C%22mainStatus_1%22%3Afalse%2C%22mainStatus_2%22%3Afalse%2C%22mainStatus_3%22%3Afalse%2C%22mainStatus_4%22%3Afalse%2C%22mainStatus_5%22%3Afalse%2C%22mainStatus_6%22%3Afalse%2C%22mainStatus_7%22%3Afalse%2C%22mainStatus_8%22%3Afalse%2C%22mainStatus_9%22%3Afalse%2C%22mainStatus_10%22%3Afalse%2C%22mainStatus_11%22%3Afalse%2C%22mainStatus_12%22%3Afalse%2C%22mainStatus_13%22%3Afalse%2C%22mainStatus_14%22%3Afalse%2C%22mainStatus_15%22%3Afalse%2C%22mainStatus_16%22%3Afalse%2C%22mainStatus_17%22%3Afalse%2C%22mainStatus_18%22%3Afalse%2C%22hidSolStatus%22%3A%22%22%2C%22hidSolStatusName%22%3A%22%22%2C%22SolvingStatus_0%22%3Afalse%2C%22SolvingStatus_1%22%3Afalse%2C%22SolvingStatus_2%22%3Afalse%2C%22SolvingStatus_3%22%3Afalse%2C%22SolvingStatus_4%22%3Afalse%2C%22SolvingStatus_5%22%3Afalse%2C%22SolvingStatus_6%22%3Afalse%2C%22SolvingStatus_7%22%3Afalse%2C%22SolvingStatus_8%22%3Afalse%2C%22SolvingStatus_9%22%3Afalse%2C%22SolvingStatus_10%22%3Afalse%2C%22SolvingStatus_11%22%3Afalse%2C%22mainTxt%22%3A%22%22%2C%22txtAddress%22%3A%22%22%2C%22TakeCaseInTimeValue%22%3A%22%22%2C%22TakeCaseInTimeText%22%3A%22%22%2C%22TakeCaseInTime_0%22%3Afalse%2C%22TakeCaseInTime_1%22%3Afalse%2C%22SovlingtimeTypeValue%22%3A%22%22%2C%22SovlingtimeTypeText%22%3A%22%22%2C%22SovlingtimeType_0%22%3Afalse%2C%22SovlingtimeType_1%22%3Afalse%2C%22SovlingtimeType_2%22%3Afalse%2C%22SovlingtimeType_3%22%3Afalse%2C%22BackCaseInTimeValue%22%3A%22%22%2C%22BackCaseInTimeText%22%3A%22%22%2C%22BackCaseInTime_0%22%3Afalse%2C%22BackCaseInTime_1%22%3Afalse%2C%22AlltimeTypeValue%22%3A%22%22%2C%22AlltimeTypeText%22%3A%22%22%2C%22AlltimeType_0%22%3Afalse%2C%22AlltimeType_1%22%3Afalse%2C%22AlltimeType_2%22%3Afalse%2C%22AlltimeType_3%22%3Afalse%2C%22MainCollDept%22%3A%22%22%2C%22SubCollDept%22%3A%22%22%2C%22TxtstrPriorityArea%22%3A%22%22%2C%22txtHeshiCount%22%3A%22%22%2C%22txtHechaCount%22%3A%22%22%2C%22discoverStartTime%22%3A%22%22%2C%22discoverEndTime%22%3A%22%22%2C%22preCreateStartTime%22%3A%22%22%2C%22preCreateEndTime%22%3A%22%22%2C%22dispatchStartTime%22%3A%22%22%2C%22dispatchEndTime%22%3A%22%22%2C%22CreateStartTime%22%3A%22%22%2C%22CreateEndTime%22%3A%22%22%2C%22solvingStartTime%22%3A%22%22%2C%22solvingEndTime%22%3A%22%22%2C%22endStartTime%22%3A%22%22%2C%22endEndTime%22%3A%22%22%2C%22TxtSimilarCase%22%3A%22%22%2C%22btnsetcolumn%22%3A%22%E6%98%BE%E7%A4%BA%E6%9F%A5%E8%AF%A2%E5%88%97%22%2C%22btnSelecExelist%22%3A%22%E4%B8%8B%E8%BD%BD%E5%88%97%E8%A1%A8%22%2C%22btnSaveModule%22%3A%22%E4%BF%9D%E5%AD%98%E6%A8%A1%E6%9D%BF%22%2C%22btnSearchs%22%3A%22%E6%9F%A5++%E8%AF%A2%22%2C%22hdnFlag%22%3A%221%22%2C%22hdnTabCount%22%3A%223%22%2C%22hidTab%22%3A%220%22%2C%22Hidcount%22%3A%22%22%2C%22hidUseItemID%22%3A%22%22%2C%22hidDept%22%3A%22%22%2C%22hidOwnerName%22%3A%22%22%2C%22hidCaseBelongLevel%22%3A%22%22%2C%22hidStreetCode%22%3A%221806%22%2C%22hidStreetName%22%3A%22%E8%B5%B5%E5%B7%B7%E9%95%87%22%2C%22hidCommunityCode%22%3A%22%22%2C%22hidCommunityName%22%3A%22%22%2C%22hidgridCode%22%3A%22%22%2C%22hidgridName%22%3A%22%22%2C%22hidgridtype%22%3A%22%22%2C%22hidgridtypeName%22%3A%22%22%2C%22hidnewworkCode%22%3A%22%22%2C%22hidnewworkName%22%3A%22%22%2C%22hidnewgridCode%22%3A%22%22%2C%22hidnewgridkName%22%3A%22%22%2C%22hidSourceID%22%3A%22%22%2C%22hidSourceName%22%3A%22%22%2C%22HidCurDeptLv%22%3A%22%22%2C%22HidCurStreetCode%22%3A%22%22%2C%22HidHeChaDeptCode%22%3A%22%22%2C%22HidHeChaDeptName%22%3A%22%22%2C%22HidBeforeCollDept%22%3A%22%22%2C%22HidBeforeCollDeptName%22%3A%22%22%2C%22HidMainCollDept%22%3A%22%22%2C%22HidMainCollDeptName%22%3A%22%22%2C%22HidSubCollDept%22%3A%22%22%2C%22HidSubCollDeptName%22%3A%22%22%2C%22HidMainDeptCode%22%3A%22%22%2C%22HidMainDeptName%22%3A%22%22%2C%22hidSubDeptCode%22%3A%22%22%2C%22hidSubDeptName%22%3A%22%22%2C%22HidDifferentID%22%3A%22%22%2C%22HidType%22%3A%22%22%2C%22HidTypename%22%3A%22%22%2C%22HidMEBClass%22%3A%22%22%2C%22HidMEBClassName%22%3A%22%22%2C%22HidMESClass%22%3A%22%22%2C%22HidMESClassName%22%3A%22%22%2C%22HidSonClass%22%3A%22%22%2C%22HidSonClassName%22%3A%22%22%2C%22HidATClass%22%3A%22%22%2C%22HidATClassName%22%3A%22%22%2C%22HidTypeDifferent%22%3A%22%22%2C%22HidRelationCase%22%3A%22%22%2C%22HidA0383%22%3A%22%22%2C%22selectedTime%22%3A%2201%22%2C%22ddl_IsMainCase%22%3A%2210%22%2C%22ddl_Casebelonging%22%3A%22-1%22%2C%22ddlKeyList%22%3A%22-1%22%2C%22ddlSort%22%3A%22-1%22%2C%22ddlDesAsc%22%3A%22desc%22%2C%22select_new_street%22%3Anull%2C%22select_gridtype%22%3Anull%2C%22select_new_workgrid%22%3Anull%2C%22select_new_grid%22%3Anull%2C%22select_community%22%3A%22-1%22%2C%22select_grid%22%3A%22-1%22%2C%22InputArea%22%3Anull%2C%22ddlMEBClass%22%3A%22-1%22%2C%22ddlMESClass%22%3A%22-1%22%2C%22ddlSonClass%22%3A%22-1%22%2C%22ddlAtClass%22%3A%22-1%22%2C%22ddlApproach%22%3A%22-1%22%2C%22ddlUrgentdegree%22%3A%22-1%22%2C%22ddl_ServiceType%22%3A%22-1%22%2C%22ddlIsThreatened%22%3A%22-1%22%2C%22ddlIndustry%22%3Anull%2C%22ddlIsWeiXian%22%3A%22-1%22%2C%22ddlisPriorityArea%22%3A%22-1%22%2C%22ddlRiskLevel%22%3A%22-1%22%2C%22ddl_WorkTypes%22%3A%22-1%22%2C%22DDLCompareHeshi%22%3A%22-1%22%2C%22DDLCompare%22%3A%22-1%22%2C%22ddlOverTimeCheck%22%3A%22-1%22%2C%22dllCaseValuation%22%3A%22-1%22%2C%22ddl_IsFeedBack%22%3A%22-1%22%2C%22hcMyd%22%3A%22-1%22%2C%22ddlIsFirstContract%22%3A%22-1%22%2C%22hfMyd%22%3A%22-1%22%2C%22ddlIsWaiValue%22%3A%22-1%22%2C%22ddlWaiManYiDu%22%3A%22-1%22%2C%22ddlWaiFuWu%22%3A%22-1%22%2C%22ddlHasLead%22%3A%22-1%22%2C%22ddlLEADERHANDTYPE%22%3A%22-1%22%2C%22ddlHasTenType%22%3A%22-1%22%2C%22ddlIsCaseEnd%22%3A%22-1%22%2C%22ddlIsTypical%22%3A%22-1%22%2C%22ddlIsStubborn%22%3A%22-1%22%2C%22ddlIsSimilar%22%3A%22-1%22%2C%22ddl_IsNew%22%3A%22-1%22%2C%22ddl_IsBackBill%22%3A%22-1%22%7D"""
        body = """arrstring=%7B%22startDate%22%3A%22{start}%22%2C%22endDate%22%3A%22{end}%22%2C%22btnTime%22%3A%22%22%2C%22hidSelectedTime%22%3A%22%22%2C%22startHour%22%3A%2200%3A00%22%2C%22endHour%22%3A%2223%3A59%22%2C%22MainExeDept%22%3A%22%22%2C%22SubExeDept%22%3A%22%22%2C%22RbStatus%22%3Atrue%2C%22RbSolvingStatus%22%3Afalse%2C%22hidStatusID%22%3A%22%22%2C%22hidStatusName%22%3A%22%22%2C%22mainStatus_0%22%3Afalse%2C%22mainStatus_1%22%3Afalse%2C%22mainStatus_2%22%3Afalse%2C%22mainStatus_3%22%3Afalse%2C%22mainStatus_4%22%3Afalse%2C%22mainStatus_5%22%3Afalse%2C%22mainStatus_6%22%3Afalse%2C%22mainStatus_7%22%3Afalse%2C%22mainStatus_8%22%3Afalse%2C%22mainStatus_9%22%3Afalse%2C%22mainStatus_10%22%3Afalse%2C%22mainStatus_11%22%3Afalse%2C%22mainStatus_12%22%3Afalse%2C%22mainStatus_13%22%3Afalse%2C%22mainStatus_14%22%3Afalse%2C%22mainStatus_15%22%3Afalse%2C%22mainStatus_16%22%3Afalse%2C%22mainStatus_17%22%3Afalse%2C%22mainStatus_18%22%3Afalse%2C%22hidSolStatus%22%3A%22%22%2C%22hidSolStatusName%22%3A%22%22%2C%22SolvingStatus_0%22%3Afalse%2C%22SolvingStatus_1%22%3Afalse%2C%22SolvingStatus_2%22%3Afalse%2C%22SolvingStatus_3%22%3Afalse%2C%22SolvingStatus_4%22%3Afalse%2C%22SolvingStatus_5%22%3Afalse%2C%22SolvingStatus_6%22%3Afalse%2C%22SolvingStatus_7%22%3Afalse%2C%22SolvingStatus_8%22%3Afalse%2C%22SolvingStatus_9%22%3Afalse%2C%22SolvingStatus_10%22%3Afalse%2C%22SolvingStatus_11%22%3Afalse%2C%22mainTxt%22%3A%22%22%2C%22txtAddress%22%3A%22%22%2C%22TakeCaseInTimeValue%22%3A%22%22%2C%22TakeCaseInTimeText%22%3A%22%22%2C%22TakeCaseInTime_0%22%3Afalse%2C%22TakeCaseInTime_1%22%3Afalse%2C%22SovlingtimeTypeValue%22%3A%22%22%2C%22SovlingtimeTypeText%22%3A%22%22%2C%22SovlingtimeType_0%22%3Afalse%2C%22SovlingtimeType_1%22%3Afalse%2C%22SovlingtimeType_2%22%3Afalse%2C%22SovlingtimeType_3%22%3Afalse%2C%22BackCaseInTimeValue%22%3A%22%22%2C%22BackCaseInTimeText%22%3A%22%22%2C%22BackCaseInTime_0%22%3Afalse%2C%22BackCaseInTime_1%22%3Afalse%2C%22AlltimeTypeValue%22%3A%22%22%2C%22AlltimeTypeText%22%3A%22%22%2C%22AlltimeType_0%22%3Afalse%2C%22AlltimeType_1%22%3Afalse%2C%22AlltimeType_2%22%3Afalse%2C%22AlltimeType_3%22%3Afalse%2C%22MainCollDept%22%3A%22%22%2C%22SubCollDept%22%3A%22%22%2C%22TxtstrPriorityArea%22%3A%22%22%2C%22txtHeshiCount%22%3A%22%22%2C%22txtHechaCount%22%3A%22%22%2C%22discoverStartTime%22%3A%22%22%2C%22discoverEndTime%22%3A%22%22%2C%22preCreateStartTime%22%3A%22%22%2C%22preCreateEndTime%22%3A%22%22%2C%22dispatchStartTime%22%3A%22%22%2C%22dispatchEndTime%22%3A%22%22%2C%22CreateStartTime%22%3A%22%22%2C%22CreateEndTime%22%3A%22%22%2C%22solvingStartTime%22%3A%22%22%2C%22solvingEndTime%22%3A%22%22%2C%22endStartTime%22%3A%22%22%2C%22endEndTime%22%3A%22%22%2C%22TxtSimilarCase%22%3A%22%22%2C%22btnsetcolumn%22%3A%22%E6%98%BE%E7%A4%BA%E6%9F%A5%E8%AF%A2%E5%88%97%22%2C%22btnSelecExelist%22%3A%22%E4%B8%8B%E8%BD%BD%E5%88%97%E8%A1%A8%22%2C%22btnSaveModule%22%3A%22%E4%BF%9D%E5%AD%98%E6%A8%A1%E6%9D%BF%22%2C%22btnSearchs%22%3A%22%E6%9F%A5++%E8%AF%A2%22%2C%22hdnFlag%22%3A%221%22%2C%22hdnTabCount%22%3A%223%22%2C%22hidTab%22%3A%220%22%2C%22Hidcount%22%3A%22%22%2C%22hidUseItemID%22%3A%22%22%2C%22hidDept%22%3A%22%22%2C%22hidOwnerName%22%3A%22%22%2C%22hidCaseBelongLevel%22%3A%22%22%2C%22hidStreetCode%22%3A%221806%22%2C%22hidStreetName%22%3A%22%E8%B5%B5%E5%B7%B7%E9%95%87%22%2C%22hidCommunityCode%22%3A%22%22%2C%22hidCommunityName%22%3A%22%22%2C%22hidgridCode%22%3A%22%22%2C%22hidgridName%22%3A%22%22%2C%22hidgridtype%22%3A%22%22%2C%22hidgridtypeName%22%3A%22%22%2C%22hidnewworkCode%22%3A%22%22%2C%22hidnewworkName%22%3A%22%22%2C%22hidnewgridCode%22%3A%22%22%2C%22hidnewgridkName%22%3A%22%22%2C%22hidSourceID%22%3A%22%22%2C%22hidSourceName%22%3A%22%22%2C%22HidCurDeptLv%22%3A%22%22%2C%22HidCurStreetCode%22%3A%22%22%2C%22HidHeChaDeptCode%22%3A%22%22%2C%22HidHeChaDeptName%22%3A%22%22%2C%22HidBeforeCollDept%22%3A%22%22%2C%22HidBeforeCollDeptName%22%3A%22%22%2C%22HidMainCollDept%22%3A%22%22%2C%22HidMainCollDeptName%22%3A%22%22%2C%22HidSubCollDept%22%3A%22%22%2C%22HidSubCollDeptName%22%3A%22%22%2C%22HidMainDeptCode%22%3A%22%22%2C%22HidMainDeptName%22%3A%22%22%2C%22hidSubDeptCode%22%3A%22%22%2C%22hidSubDeptName%22%3A%22%22%2C%22HidDifferentID%22%3A%22%22%2C%22HidType%22%3A%22%22%2C%22HidTypename%22%3A%22%22%2C%22HidMEBClass%22%3A%22%22%2C%22HidMEBClassName%22%3A%22%22%2C%22HidMESClass%22%3A%22%22%2C%22HidMESClassName%22%3A%22%22%2C%22HidSonClass%22%3A%22%22%2C%22HidSonClassName%22%3A%22%22%2C%22HidATClass%22%3A%22%22%2C%22HidATClassName%22%3A%22%22%2C%22HidTypeDifferent%22%3A%22%22%2C%22HidRelationCase%22%3A%22%22%2C%22HidA0383%22%3A%22%22%2C%22selectedTime%22%3A%2201%22%2C%22ddl_IsMainCase%22%3A%2210%22%2C%22ddl_Casebelonging%22%3A%22-1%22%2C%22ddlKeyList%22%3A%22-1%22%2C%22ddlSort%22%3A%22-1%22%2C%22ddlDesAsc%22%3A%22desc%22%2C%22select_new_street%22%3Anull%2C%22select_gridtype%22%3Anull%2C%22select_new_workgrid%22%3Anull%2C%22select_new_grid%22%3Anull%2C%22select_community%22%3A%22-1%22%2C%22select_grid%22%3A%22-1%22%2C%22InputArea%22%3Anull%2C%22ddlMEBClass%22%3A%22-1%22%2C%22ddlMESClass%22%3A%22-1%22%2C%22ddlSonClass%22%3A%22-1%22%2C%22ddlAtClass%22%3A%22-1%22%2C%22ddlApproach%22%3A%22-1%22%2C%22ddlUrgentdegree%22%3A%22-1%22%2C%22ddl_ServiceType%22%3A%22-1%22%2C%22ddlIsThreatened%22%3A%22-1%22%2C%22ddlIndustry%22%3Anull%2C%22ddlIsWeiXian%22%3A%22-1%22%2C%22ddlisPriorityArea%22%3A%22-1%22%2C%22ddlRiskLevel%22%3A%22-1%22%2C%22ddl_WorkTypes%22%3A%22-1%22%2C%22DDLCompareHeshi%22%3A%22-1%22%2C%22DDLCompare%22%3A%22-1%22%2C%22ddlOverTimeCheck%22%3A%22-1%22%2C%22dllCaseValuation%22%3A%22-1%22%2C%22ddl_IsFeedBack%22%3A%22-1%22%2C%22hcMyd%22%3A%22-1%22%2C%22ddlIsFirstContract%22%3A%22-1%22%2C%22hfMyd%22%3A%22-1%22%2C%22ddlIsWaiValue%22%3A%22-1%22%2C%22ddlWaiManYiDu%22%3A%22-1%22%2C%22ddlWaiFuWu%22%3A%22-1%22%2C%22ddlHasLead%22%3A%22-1%22%2C%22ddlLEADERHANDTYPE%22%3A%22-1%22%2C%22ddlHasTenType%22%3A%22-1%22%2C%22ddlIsCaseEnd%22%3A%22-1%22%2C%22ddlIsTypical%22%3A%22-1%22%2C%22ddlIsStubborn%22%3A%22-1%22%2C%22ddlIsSimilar%22%3A%22-1%22%2C%22ddl_IsNew%22%3A%22-1%22%2C%22ddl_IsBackBill%22%3A%22-1%22%7D"""
        body=body.format(start=today_str,end=today_str)
        self.sess.headers.update(headers)
        
        url="http://10.231.18.25/CITYGRID.QUERY/XinZeng/GetCondition"
        
        rt=self.sess.post(url,data=body,proxies=self.proxies) 
    

    def _req_second(self):
        # url2= 'http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchResultAllFlat.aspx?IsQuery=1'
        url2='http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchResultFlat.aspx?IsQuery=1'

        # header2={
            # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
            # 'Origin':'http://10.231.18.25',
            # 'Accept':'application/json, text/javascript, */*; q=0.01',
            # 'Referer':'http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchConditionFlat.aspx',
            # # 'Cookie':'ASP.NET_SessionId=0jomini1le3yjhfozaby3bcj; ScreenWidth=2560; ScreenHeight=1440; .ASPXAUTH=454EEB8DB6AF0C3D7375D4D1E09490A8B5ED8422477F833EECEC9EE94869BA75353A463969A74E2CF5F7FC8F4B0A699A1C295F719DF0ABE22C16711430D602AAD0486E6F73E533169B997BC46BEEB09FE070075148A082EA248474001926859D11A3770DCD26BE6F29185B66F06B4D7E4F5184390539BFFBB0845986D315B5A58E53BD811246C649643BD3CFDE29B08E'
            # 'Cookie':'ASP.NET_SessionId=mlv4zdrstxjfcpn0n032q3qh; ScreenWidth=1920; ScreenHeight=1080; .ASPXAUTH=B566BD0E6F3F0FD3D2FA1ABB8EE70F417C25CD5BB92ED40866B20EB80CEAD2825520F1A073D49CD7B6E04863D60882D08D9EC417F539431931DEDE002E5A00BADD34CA9920F6068A717590FD211D5C68B24B7AE319655A9031336D7464E169F117037D30BA7E2C29E7EFFB416F6A61F8476A3167030DB53120AC994F20AF816EEC91F49BD6984938E5F10D528E277B02; SearchColumn=CITYGRID.F_MAIN_STATUS(status)%26TASKID%26CITYGRID.F_REC_INFOSOURCENAME(INFOSOURCEID)%26TO_CHAR+(DISCOVERTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)%26CITYGRID.F_REC_INFOTYPENAME_NEW(INFOTYPEID)%26CITYGRID.F_REC_IBC_NAME_NEW(INFOBCCODE%2cINFOTYPEID)%26CITYGRID.F_REC_ISC_NAME_NEW(INFOBCCODE%2cINFOSCCODE%2cINFOTYPEID)%26CITYGRID.F_REC_IZC_NAME(INFOBCCODE%2cINFOSCCODE%2cINFOZCCODE%2cINFOTYPEID)%26CITYGRID.F_REC_STREETNAME(STREETCODE)%26Address%26KeeperSN%26TO_CHAR+(DISPATCHTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)%26CITYGRID.F_REC_MAINDEPTNAME+(EXECUTEDEPTCODE%2c+DEPTCODE%2c+TASKID)%26CITYGRID.F_REC_THREEDEPTNAME(EXECUTEDEPTCODE%2cDEPTCODE%2cTASKID)%26TO_CHAR+(ENDTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)'
           
        # }
        # header2={
            # 'Accept-Language':'zh-CN,zh;q=0.9',
            # 'Host':'10.231.18.25',
            # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            # 'Upgrade-Insecure-Requests':'1',
            # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Cookie':'ASP.NET_SessionId=mlv4zdrstxjfcpn0n032q3qh; ScreenWidth=1920; ScreenHeight=1080; SearchColumn=CITYGRID.F_MAIN_STATUS(status)%26TASKID%26CITYGRID.F_REC_INFOSOURCENAME(INFOSOURCEID)%26TO_CHAR+(DISCOVERTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)%26CITYGRID.F_REC_INFOTYPENAME_NEW(INFOTYPEID)%26CITYGRID.F_REC_IBC_NAME_NEW(INFOBCCODE%2cINFOTYPEID)%26CITYGRID.F_REC_ISC_NAME_NEW(INFOBCCODE%2cINFOSCCODE%2cINFOTYPEID)%26CITYGRID.F_REC_IZC_NAME(INFOBCCODE%2cINFOSCCODE%2cINFOZCCODE%2cINFOTYPEID)%26CITYGRID.F_REC_STREETNAME(STREETCODE)%26GRIDCODE%26Address%26KeeperSN%26TO_CHAR+(DISPATCHTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)%26CITYGRID.F_REC_MAINDEPTNAME+(EXECUTEDEPTCODE%2c+DEPTCODE%2c+TASKID)%26CITYGRID.F_REC_THREEDEPTNAME(EXECUTEDEPTCODE%2cDEPTCODE%2cTASKID)%26TO_CHAR+(ENDTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)'
        # }
        # self.sess.headers.update(header2)
        
        rt2 = self.sess.get(url2,proxies=self.proxies)
        self.content =  rt2.content
        
    
    def _req_table(self):
        # header2={
            # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
            # 'Origin':'http://10.231.18.25',
            # # 'Accept':'application/json, text/javascript, */*; q=0.01',
            # 'Referer':'http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/SearchConditionFlat.aspx',
            # # 'Cookie':'ASP.NET_SessionId=0jomini1le3yjhfozaby3bcj; ScreenWidth=2560; ScreenHeight=1440; .ASPXAUTH=454EEB8DB6AF0C3D7375D4D1E09490A8B5ED8422477F833EECEC9EE94869BA75353A463969A74E2CF5F7FC8F4B0A699A1C295F719DF0ABE22C16711430D602AAD0486E6F73E533169B997BC46BEEB09FE070075148A082EA248474001926859D11A3770DCD26BE6F29185B66F06B4D7E4F5184390539BFFBB0845986D315B5A58E53BD811246C649643BD3CFDE29B08E'
            # 'Cookie':'ASP.NET_SessionId=mlv4zdrstxjfcpn0n032q3qh; ScreenWidth=1920; ScreenHeight=1080; .ASPXAUTH=B566BD0E6F3F0FD3D2FA1ABB8EE70F417C25CD5BB92ED40866B20EB80CEAD2825520F1A073D49CD7B6E04863D60882D08D9EC417F539431931DEDE002E5A00BADD34CA9920F6068A717590FD211D5C68B24B7AE319655A9031336D7464E169F117037D30BA7E2C29E7EFFB416F6A61F8476A3167030DB53120AC994F20AF816EEC91F49BD6984938E5F10D528E277B02; SearchColumn=CITYGRID.F_MAIN_STATUS(status)%26TASKID%26CITYGRID.F_REC_INFOSOURCENAME(INFOSOURCEID)%26TO_CHAR+(DISCOVERTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)%26CITYGRID.F_REC_INFOTYPENAME_NEW(INFOTYPEID)%26CITYGRID.F_REC_IBC_NAME_NEW(INFOBCCODE%2cINFOTYPEID)%26CITYGRID.F_REC_ISC_NAME_NEW(INFOBCCODE%2cINFOSCCODE%2cINFOTYPEID)%26CITYGRID.F_REC_IZC_NAME(INFOBCCODE%2cINFOSCCODE%2cINFOZCCODE%2cINFOTYPEID)%26CITYGRID.F_REC_STREETNAME(STREETCODE)%26Address%26KeeperSN%26TO_CHAR+(DISPATCHTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)%26CITYGRID.F_REC_MAINDEPTNAME+(EXECUTEDEPTCODE%2c+DEPTCODE%2c+TASKID)%26CITYGRID.F_REC_THREEDEPTNAME(EXECUTEDEPTCODE%2cDEPTCODE%2cTASKID)%26TO_CHAR+(ENDTIME%2c+%27yyyy-mm-dd+hh24%3ami%27)'
           
        # }
        
        url3='http://10.231.18.25/CITYGRID.QUERY/archivesinfo_flat/OutputExcel.aspx?page=InfoMSearchConfigurableNew&'
        rt3 = self.sess.get(url3,proxies=self.proxies)
        return rt3.content
    
    def parse_rt(self,content):
        soup=BeautifulSoup(content,"html.parser")
        total=[]
        for i in soup.select('td tr'):
            ls=[]
            for k in i.select('td'):
                ls.append(k.text)
            total.append(ls)   
        return total

    def save_json_str(self,json_str):
        set_value('inspector_case',json_str)
    


