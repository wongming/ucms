import os,sys
import threading
import time,datetime
import stest
cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../db/')
sys.path.append(cur_dir+'/../control/')
sys.path.append(cur_dir+'/../lib/')

from table import AppTable
from BaseControl import RT
import logging, logging.config
import ant_util
logging.config.fileConfig(cur_dir+'/../conf/log.conf')
logger = logging.getLogger('releasetask')
class ReleaseTask(threading.Thread):
    def __init__(self, id):
        self.app_id = id
        self.now = getCurrentTimeStr()
        self.appTable = AppTable()
        self.app_name = self.appTable.select(id)['name']
        self.log_path = os.path.normpath(cur_dir+'/../workbench/release/log/'+self.now+self.app_name)
        self.ant_file_path = os.path.normpath(cur_dir+'/../workbench/release/'+self.app_name+'.xml')
        super(ReleaseTask, self).__init__()

    def prepareTask(self):
        logger.info('prepare release task [%s],[%s]' % (self.app_name,self.app_id))
        self.appTable.update({'id', self.app_id}, {'status': 'Releasing','last_release_time': now})

    def stopTask(self):
        logger.info('stop release task [%s],[%s]' % (self.app_name,self.app_id))
        self.appTable.update({'id', self.app_id}, {'status': 'Running','last_release_time': now})

    def runTask(self):
        logger.info('start run release task [%s],[%s]' % (self.app_name,self.app_id))
        status = ant_util.build(ant_file_path, 'generate.orignal.war',self.log_path)
        self.appTable.update({'id', self.app_id}, {'status': status==0?'Running':'Down','last_release_time': now, 'last_release_status': status==0?'Success':'Failed','last_release_log':self.log_path})

    def run(self):
        self.prepareTask()
        self.runTask()
        self.stopTask()

def getCurrentTimeStr():
    now = datetime.datetime.now()
    return datetime.datetime.strftime(now, '%Y.%m.%d %H:%M:%S.%f'

if __name__ == '__main__':
    pass
