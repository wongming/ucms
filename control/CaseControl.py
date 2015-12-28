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
from table import CaseTable
class CaseController(BaseController):
    def __init__(self):
        self.table = CaseTable()
        pass

    def get_case(self, id):
        ret = self.table.select(id)
        return ret
        
    def run_case(self, id):

        return ret
if __name__ == '__main__':
    pass
