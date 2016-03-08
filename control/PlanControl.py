#encoding = utf-8
import os, sys, re
import json
reload(sys)
sys.setdefaultencoding('utf8')
cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../common/')
import logging, logging.config
import traceback
from BaseControl import BaseController
from BaseControl import RT
from table import PlanTable, PlanResultTable

class PlanController(BaseController):
    def __init__(self):
        self.planTable = PlanTable()
        self.planResultTable = PlanResultTable()

    def runPlan(self, id):
        plan = self.getPlan(id)
        plan_result = {}
        plan_result['plan_name'] = plan['name']
        plan_result['status'] = 'new'
        ret = self.planResultTable.insert(plan_result)
        if not ret[0]==RT.SUCC:
            return RT.ERR, 'insert plan result in db failed and plan name is [%s]' % plan['name']
        return RT.SUCC, ''

    def addPlan(self, submit_data):
        plan_info = {}
        '''
        {
          "Plan Name":"plan_demo",
          "Case List":"tc_case_demo_1",
          "Email List":"byonecry@qq.com",
          "Log":"Warn"
        }
        '''
        plan_info['Plan Name'] = submit_data['name']
        case_list = submit_data['case_list'].split(",")
        case_list_str = ''
        for case_name in case_list:
            if case_list_str=='':
                case_list_str = 'tc_' + case_name
            else:
                case_list_str = case_list_str + ',tc_' + case_name
        plan_info['Case List'] = case_list_str
        plan_info['Email List'] = submit_data['people']
        plan_home_path = cur_dir+'/../workbench/case/'
        plan_path = os.path.join(plan_home_path, submit_data['name']+'.json')
        plan_file = open(plan_path, 'w')
        plan_file.write(json.dumps(plan_info, indent=4))
        plan_file.close()
        ret = self.planTable.insert(submit_data)
        return ret

    def getPlan(self, id):
        ret = self.planTable.select(id)
        if not ret[0]==0:
            return None
        return ret[1]

    def getPlanByName(self, name):
        ret = self.planTable.selectByName(name)
        if not ret[0]==RT.SUCC:
            return None
        return ret[1]

    def getPlans(self, start, limit, cond_dict={}):
        ret = self.planTable.selects(start, limit, cond_dict)
        return ret

    def count(self, cond_dict={}):
        ret = self.planTable.count(cond_dict)
        if not ret[0]==0:
            return 0
        return ret[1]

    def getPlanResults(self, start, limit, cond_dict={}, order_dict={}):
        ret = self.planResultTable.selects(start, limit, cond_dict, order_dict)
        return ret

    def countPlanResult(self, cond_dict={}):
        ret = self.planResultTable.count(cond_dict)
        if not ret[0]==0:
            return 0
        return ret[1]

if __name__ == '__main__':
    pass
