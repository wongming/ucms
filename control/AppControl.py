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
from ReleaseTask import ReleaseTask
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
            template_path = os.path.normpath(cur_dir+'/../workbench/release/template/'+app_type+'Template.xml')
            xml_path = os.path.normpath(cur_dir+'/../workbench/release/'+app_name+'.xml')
            file_util.Copy(template_path, xml_path)
            process.run("sed -ig 's#PPProjectName#%s#' %s" %(app_name, xml_path))
            process.run("sed -ig 's#WWWorkspace#%s#' %s" %(workspace, xml_path))
        ret = self.table.insert(submit_data)
        return ret

    def getApp(self, id):
        ret = self.table.select(id)
        if not ret[0]==RT.SUCC:
            return None
        if isAccessedUrl(ret[1]['access_url']):
            self.updateApp(id, {'status': 'Running'})
        else:
            self.updateApp(id, {'status': 'Down'})
        ret = self.table.select(id)
        if not ret[0]==RT.SUCC:
            return None
        return ret[1]

    def updateApp(self, id, value_map):
        ret = self.table.update({'id': id}, value_map)
        return ret

    def getAppByName(self, name):
        ret = self.table.selectByName(name)
        if not ret[0]==RT.SUCC:
            return None
        return ret[1]

    def getAllApps(self):
        ret = self.table.selectAll()
        return ret[1]

    def releaseApp(self, id):
        if not self.getApp(id):
            return RT.SUCC, 'app of id=[] not exist'
        self.table.update({'id': id}, {'status': 'ToRelease'})
        task = ReleaseTask(id)
        task.start()
        return RT.SUCC, 'task to release app has started'

def isAccessedUrl(url):
    try:
        reqst = urllib2.Request(url)
        reps = urllib2.urlopen(reqst)
        reps_code = reps.code
        print reps_code
        if reps_code=='200':
            print 'reponse code is not 200'
            return False
        return True
    except Exception,e:
        err = traceback.format_exc()
        print err
        return False

if __name__ == '__main__':
    pass
