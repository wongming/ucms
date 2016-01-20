import os,sys
import threading
import time,datetime
import stest
cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../db/')
sys.path.append(cur_dir+'/../control/')
sys.path.append(cur_dir+'/../common/')
from table import CaseTable,CaseResultTable
from BaseControl import RT
import logging, logging.config
logging.config.fileConfig(cur_dir+'/../conf/log.conf')
logger = logging.getLogger('casetask')
class TestCaseTask(threading.Thread):
    def __init__(self, case_result):
        print case_result
        self.case_result_id = case_result['id']
        self.case_name = case_result['case']
        self.case_path = cur_dir+'/../workbench/case/'+self.case_name
        self.caseTable = CaseTable()
        self.caseResultTable = CaseResultTable()
        super(TestCaseTask, self).__init__()

    def prepareTask(self):
        logger.info('prepare case task [%s],[%s]' % (self.case_name,self.case_result_id))

    def stopTask(self):
        logger.info('stop case task[%s],[%s]' % (self.case_name,self.case_result_id))

    def runTask(self):
        logger.info('start run case task')
        ret = self.caseResultTable.update({'id': self.case_result_id}, {'status': 'running', 'start_time':datetime.datetime.now()})
        if not ret[0]==RT.SUCC:
            logger.error('update CaseResultTable [%s] failed' % self.case_result_id)
            return
        result = stest.runCase(self.case_path)
        ret = self.caseResultTable.update({'id': self.case_result_id}, {'status': 'success', 'start_time':datetime.datetime.now()})
        if not ret[0]==RT.SUCC:
            logger.error('update CaseResultTable [%s] failed' % self.case_result_id)
            return

    def run(self):
        self.prepareTask()
        self.runTask()
        self.stopTask()

#status:new, waiting, running

def startCaseTask():
    caseResultTable = CaseResultTable()
    while True:
        tc_tasks = []
        rt,tc_result_list = caseResultTable.selectAll({'status':'new'})
        if not len(tc_result_list)==0:
            for tc_result in tc_result_list:
                tc_task = TestCaseTask(tc_result)
                tasks.append(tc_tasks)
            for task in tc_tasks:
                task.start()
        else:
            logger.info('none case task found...')
            #print 'none case task found...'
        time.sleep(0.5)

if __name__ == '__main__':
    startCaseTask()
