# -*- coding: utf-8 -*
import os, sys, re
import json
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../common/')
import logging, logging.config
import traceback
from BaseControl import BaseController
from BaseControl import RT
from table import CaseTable,CaseResultTable
import stest
case_workbench = cur_dir+'/../workbench/case/'
class CaseController(BaseController):
    def __init__(self):
        self.caseTable = CaseTable()
        self.caseResultTable = CaseResultTable()

    def runCase(self, id):
        cs = self.getCase(id)
        case_result = {}
        case_result['case_name'] = cs['name']
        case_result['status'] = 'new'
        case_result['create_time'] = datetime.datetime.now()
        ret = self.caseResultTable.insert(case_result)
        if not ret[0]==RT.SUCC:
            return RT.ERR, 'insert case result to db failed and case name is [%s]' % cs['name']
        return RT.SUCC, ''

    def addCase(self, submit_data):
        case_info = {}
        case_info['name'] = submit_data['name']
        case_info['driver'] = submit_data['driver']
        case_info['data'] = json.loads(submit_data['param'])
        case_name = submit_data['name']
        case_home_path = cur_dir+'/../workbench/case/'
        case_path = os.path.join(case_home_path,'tc_'+case_name)
        case_file = open(case_path, 'w')
        case_file.write(json.dumps(case_info, indent=4))
        case_file.close()
        ret = self.caseTable.insert(submit_data)
        if not ret[0]==RT.SUCC:
            return RT.ERR, 'insert case to db failed and case name is [%s]' % case_name
        return RT.SUCC, ''

    def getCase(self, id):
        ret = self.caseTable.select(id)
        if not ret[0]==0:
            return None
        return ret[1]

    def deleteCase(self, id):
        ret = self.caseTable.deleteById(id)
        return ret
        
    def getCaseByName(self, name):
        ret = self.caseTable.selectByName(name)
        if not ret[0]==RT.SUCC:
            return None
        return ret[1]

    def getCases(self, start, limit, cond_dict={}):
        ret = self.caseTable.selects(start, limit, cond_dict)
        return ret


    def count(self,cond_dict={}):
        ret = self.caseTable.count(cond_dict)
        if not ret[0]==0:
            return 0
        return ret[1]

    def getCaseResults(self, start, limit, cond_dict={}, order_dict={}):
        ret = self.caseResultTable.selects(start, limit, cond_dict, order_dict)
        return ret

    def countCaseResult(self,cond_dict={}):
        ret = self.caseResultTable.count(cond_dict)
        if not ret[0]==0:
            return 0
        return ret[1]

if __name__ == '__main__':
    pass
