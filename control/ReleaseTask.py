import os,sys
import threading
import time,datetime
import urllib
import urllib2
import traceback

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../db/')
sys.path.append(cur_dir+'/../control/')
sys.path.append(cur_dir+'/../lib/')

from table import AppTable
from BaseControl import RT
import logging, logging.config
import ant_util,file_util,process

logging.config.fileConfig(cur_dir+'/../conf/log.conf')
logger = logging.getLogger('releasetask')
class ReleaseTask(threading.Thread):
    def __init__(self, id):
        self.app_id = id
        self.now = getCurrentTimeStr()
        self.appTable = AppTable()
        self.app = self.appTable.select(id)[1]
        self.app_name = self.app['name']
        self.log_path = os.path.normpath(cur_dir+'/../workbench/release/log/'+getCurrentTimeStr2()+'-'+self.app_name+'.log')
        self.ant_file_path = os.path.normpath(cur_dir+'/../workbench/release/'+self.app_name+'.xml')
        super(ReleaseTask, self).__init__()

    def prepareTask(self):
        logger.info('prepare release task [%s],[%s]' % (self.app_name,self.app_id))
        self.appTable.update({'id': self.app_id}, {'status': 'Releasing','last_release_status': 'Releasing', 'last_release_time': self.now, 'last_release_log':self.log_path, 'last_release_info': 'prepare to release'})
    def stopTask(self):
        logger.info('stop release task [%s],[%s]' % (self.app_name,self.app_id))

    def runTask(self):
        logger.info('start run release task [%s],[%s]' % (self.app_name,self.app_id))
        app_name = self.app['name']
        app_type = self.app['type']
        repository_type = self.app['repository_type']
        repository_path = self.app['repository_path']
        workspace = os.path.normpath(cur_dir+'/../workbench/release/project')
        app_workspace = os.path.normpath(workspace+'/'+app_name)
        app_war = os.path.normpath(workspace+'/'+app_name+'.war')
        #delete code workspace
        #del_cmd = 'rm -rf %s/%s'%(workspace, app_name)
        #ret = process.run(del_cmd)
        self.appTable.update({'id': self.app_id}, {'last_release_info': 'clearing workspace'})
        if file_util.Exists(app_workspace):
            logger.info('delete old app workspace [%s]'%app_workspace)
            file_util.Delete(app_workspace)
        #delete war
        #del_cmd = 'rm  %s/%s.war'%(workspace, app_name)
        #ret = process.run(del_cmd)
        if file_util.Exists(app_war):
            logger.info('delete old war direction [%s]'%app_war)
            file_util.Delete(app_war)
        #prepare code
        self.appTable.update({'id': self.app_id}, {'last_release_info': 'copying code'})
        if repository_type=='SVN':
            #check out latest code
            svn_cmd = 'svn co %s %s --username=wangming --password=wangming'%(repository_path, app_workspace)
            ret = process.run(svn_cmd)
            if not ret[0] ==0:
                self.appTable.update({'id':self.app_id}, {'last_release_status': 'Failed','last_release_info':'prepare application code from SVN failed'})
                return
        elif repository_type=='Git':
            pass
        elif repository_type=='File':
            file_util.CopyDir(repository_path, app_workspace)
        #compile code
        self.appTable.update({'id': self.app_id}, {'last_release_info': 'compiling code'})
        compile_status = ant_util.build(self.ant_file_path, 'generate.orignal.war', self.log_path)
        if compile_status!=0:
            self.appTable.update({'id': self.app_id}, {'last_release_status': 'Failed','last_release_info':'compile application code failed'})
            return
        #release app
        self.appTable.update({'id': self.app_id}, {'last_release_info': 'everything is ok and is releasing'})
        if app_type =='JavaWeb' or app_type =='JavaWeb-Maven':
            tomcat_path = '/Library/tomcat7/webapps'
            file_util.Copy(app_war, tomcat_path)
        else:
            pass
        ret = isAppAccessed(self.app['access_url'])
        if not ret:
            self.appTable.update({'id': self.app_id}, {'status': 'Down', 'last_release_status': 'Failed','last_release_info': 'access url failed'})
            return
        self.appTable.update({'id': self.app_id}, {'status': 'Running', 'last_release_status': 'Success','last_release_info': 'release the app successfully'})

    def run(self):
        self.prepareTask()
        self.runTask()
        self.stopTask()

def getCurrentTimeStr():
    now = datetime.datetime.now()
    return datetime.datetime.strftime(now, '%Y.%m.%d %H:%M:%S.%f')

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

def isAppAccessed(url):
    retry_times = 5
    interval = 5
    while(retry_times>0):
        if isAccessedUrl(url):
            return True
        time.sleep(interval)
        retry_times-=1
        interval+=5
    return False

def getCurrentTimeStr2():
    now = datetime.datetime.now()
    return datetime.datetime.strftime(now, '%Y%m%d%H%M%S')

if __name__ == '__main__':
    tt = ReleaseTask(12)
    tt.run()
