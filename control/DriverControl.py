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
from table import DriverTable

class DriverController(BaseController):
    def __init__(self):
        self.table = DriverTable()

    def getDriver(self, id):
        ret = self.table.select(id)
        if not ret[0]==0:
            return None
        return ret[1]

    def getDrivers(self, start, limit):
        ret = self.table.selects(start, limit)
        return ret

    def count(self,cond_dict={}):
        ret = self.table.count(cond_dict)
        if not ret[0]==0:
            return 0
        return ret[1]

if __name__ == '__main__':
    pass
