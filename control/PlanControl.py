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
