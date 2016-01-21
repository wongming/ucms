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
        self.case_name = case_result['case_name']
        self.case_path = cur_dir+'/../workbench/tc_'+self.case_name
        self.log_path = cur_dir+'/../workbench/log/tc_'+self.case_name+'_id_'+str(self.case_result_id)+'.log'
        self.caseTable = CaseTable()
        self.caseResultTable = CaseResultTable()
        super(TestCaseTask, self).__init__()

    def prepareTask(self):
        logger.info('prepare case task [%s],[%s]' % (self.case_name,self.case_result_id))

    def stopTask(self):
        logger.info('stop case task[%s],[%s]' % (self.case_name,self.case_result_id))

    def runTask(self):
        logger.info('start run case task')
        ret = self.caseResultTable.update({'id': self.case_result_id}, {'status': 'running'})
        if not ret[0]==RT.SUCC:
            logger.error('update CaseResultTable to running [%s] failed' % self.case_result_id)
            return
        test_result = stest.runCase(self.case_path)
        test_status = 'success' if test_result.wasSuccessful() else 'failed'
        test_start_time =test_result.startTime
        test_stop_time = test_result.stopTime
        log_file = open(self.log_path,'w')
        log_file.write(test_result.log.getvalue())
        log_file.close()
        ret = self.caseResultTable.update({'id': self.case_result_id}, {'status': test_status, 'start_time': test_start_time, 'stop_time': test_stop_time,'log':self.log_path})
        if not ret[0]==RT.SUCC:
            logger.error("update CaseResultTable's result [%s] failed" % self.case_result_id)
            return

    def run(self):
        self.prepareTask()
        self.runTask()
        self.stopTask()

#status:new, waiting, running

def startCaseTask():
    caseResultTable = CaseResultTable()
    while True:
        rt,tc_result_list = caseResultTable.selectAll({'status':'new'})
        if not len(tc_result_list)==0:
            for tc_result in tc_result_list:
                tc_task = TestCaseTask(tc_result)
                tc_task.start()
        else:
            #logger.info('none case task found...')
            #print 'none case task found...'
            pass
        time.sleep(0.5)

if __name__ == '__main__':
    startCaseTask()
