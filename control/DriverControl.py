#encoding = utf-8
import os, sys, re
import json
reload(sys)
sys.setdefaultencoding('utf8')
cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../lib/')
import logging, logging.config
import traceback
from BaseControl import BaseController
from BaseControl import RT
from table import DriverTable
import file_util
class DriverController(BaseController):
    def __init__(self):
        self.table = DriverTable()

    def addDriver(self, submit_data):
        ret = self.table.unique({'name':submit_data['name']})
        if not ret:
            return RT.ERR, 'driver [%s] exists in the system'
        driver_home = os.path.expanduser('~/.stest/driver/')
        driver_path = os.path.join(driver_home,submit_data['name'])
        file_util.Delete(driver_path)
        file_util.MakeDirs(driver_path)
        #SetUp
        set_up_file = open(os.path.join(driver_path,'setUp.py'), 'w')
        set_up_file.write(submit_data['setuppy'])
        set_up_file.close()
        #TearDown
        tear_down_file = open(os.path.join(driver_path,'tearDown.py'), 'w')
        tear_down_file.write(submit_data['teardownpy'])
        tear_down_file.close()
        #Exec
        exec_file = open(os.path.join(driver_path,'exec.py'), 'w')
        exec_file.write(submit_data['execpy'])
        exec_file.close()
        #param
        param_file = open(os.path.join(driver_path,'param.json'), 'w')
        param_file.write(submit_data['param'])
        ret = self.table.insert(submit_data)
        if not ret[0]==RT.SUCC:
            return RT.ERR, ret[1]
        return RT.SUCC, ''

    def getDriver(self, id):
        ret = self.table.select(id)
        if not ret[0]==0:
            return None
        return ret[1]

    def deleteDriver(self, id):
        ret = self.table.deleteById(id)
        return ret

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
    setuppy = '''def setup(tc):
    pass'''
    submit_data = {'setuppy':setuppy, 'name':'aaaaa'}
    DriverController().addDriver(submit_data)
    pass
