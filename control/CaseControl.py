# -*- coding: utf-8 -*
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
from table import CaseTable,CaseResultTable
import stest

class CaseController(BaseController):
    def __init__(self):
        self.caseTable = CaseTable()
        self.caseResultTable = CaseResultTable()

    def runCase(self, id):
        cs = self.getCase(id)
        case_result = {}
        case_result['case'] = cs['name']
        case_result['status'] = 'new'
        ret = self.caseResultTable.insert(case_result)
        if not ret[0]==RT.SUCC:
            return False, 'insert case result in db failed and case name is [%s]' % cs['name']
        return True, ''

    def addCase(self, submit_data):
        ret = self.caseTable.insert(submit_data)
        return ret

    def getCase(self, id):
        ret = self.caseTable.select(id)
        if not ret[0]==0:
            return None
        return ret[1]

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

    def getCaseResults(self, start, limit, cond_dict={}):
        ret = self.caseResultTable.selects(start, limit, cond_dict)
        return ret

    def countCaseResult(self,cond_dict={}):
        ret = self.caseResultTable.count(cond_dict)
        if not ret[0]==0:
            return 0
        return ret[1]

if __name__ == '__main__':
    pass
