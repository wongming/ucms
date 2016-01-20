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

    def addDriver(self, submit_data):
        ret = self.table.insert(submit_data)
        return ret

    def getDriver(self, id):
        ret = self.table.select(id)
        if not ret[0]==0:
            return None
        return ret[1]

    def getDriverByName(self, name):
        ret = self.table.selectByName(name)
        if not ret[0]==RT.SUCC:
            return None
        return ret[1]

    def getDrivers(self, start, limit):
        ret = self.table.selects(start, limit)
        return ret

    def getAllDrivers(self):
        ret = self.table.selectAll()
        return ret[1]

    def getAllDriversMap(self):
        ret = self.table.selectAll()
        driver_map = {}
        for driver in ret[1]:
            driver_map[driver['name']] = driver
        return driver_map

    def count(self,cond_dict={}):
        ret = self.table.count(cond_dict)
        if not ret[0]==0:
            return 0
        return ret[1]

if __name__ == '__main__':
    pass
