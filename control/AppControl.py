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
import file_util
import process
from table import AppTable

class AppController(BaseController):
    def __init__(self):
        self.table = AppTable()

    def addApp(self, submit_data):
        app_name = submit_data['name']
        app_type = submit_data['type']
        workspace = os.path.normpath(cur_dir+'/../workbench/release/project')
        #ant xml
        if app_type =='JavaWeb' or app_type =='JavaWeb-Maven':
            submit_data.pop('script')
            template_path = os.path.normpath(cur_dir+'/../workbench/release/'+app_type+'Template.xml')
            xml_path = os.path.normpath(cur_dir+'/../workbench/release/'+app_name+'.xml')
            file_util.Copy(template_path, xml_path)
            process.run("sed -ig 's/$ProjectName/%s/' %s" %(app_name, xml_path)
            process.run("sed -ig 's/$Workspace/%s/' %s" %(workspace, xml_path)
        #cp project code source
        #https://192.168.88.210/repos/csdc/amss/trunk
        #svn co https://192.168.88.210/repos/csdc/amss/trunk --username=wangming --password=wangming
        repository_type = submit_data['repository_type']
        repository_path = submit_data['repository_path']
        if repository_type=='SVN':
            cmd = 'svn co %s --username=wangming --password=wangming'%(repository_path)

        ret = self.table.insert(submit_data)
        return ret

    def getApp(self, id):
        ret = self.table.select(id)
        if not ret[0]==0:
            return None
        return ret[1]

    def getAppByName(self, name):
        ret = self.table.selectByName(name)
        if not ret[0]==RT.SUCC:
            return None
        return ret[1]

    def getAllApps(self):
        ret = self.table.selectAll()
        return ret[1]

    def releaseApp(id):

        return

if __name__ == '__main__':
    pass
