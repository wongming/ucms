import os,sys
import threading
import time,datetime
import stest
cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../db/')
sys.path.append(cur_dir+'/../control/')
sys.path.append(cur_dir+'/../common/')
from table import PlanTable,PlanResultTable
from BaseControl import RT
import logging, logging.config
logging.config.fileConfig(cur_dir+'/../conf/log.conf')
logger = logging.getLogger('plantask')
class TestPlanTask(threading.Thread):
    def __init__(self, plan_result):
        self.plan_result_id = plan_result['id']
        self.plan_name = plan_result['plan_name']
        self.plan_path = os.path.normpath(cur_dir+'/../workbench/'+self.plan_name+'.json')
        self.log_path = os.path.normpath(cur_dir+'/../workbench/log/tp_'+self.plan_name+'_id_'+str(self.plan_result_id)+'.log')
        self.planTable = PlanTable()
        self.planResultTable = PlanResultTable()
        super(TestPlanTask, self).__init__()

    def prepareTask(self):
        logger.info('prepare plan task [%s],[%s]' % (self.plan_name,self.plan_result_id))

    def stopTask(self):
        logger.info('stop plan task[%s],[%s]' % (self.plan_name,self.plan_result_id))

    def runTask(self):
        logger.info('start run plan task')
        ret = self.planResultTable.update({'id': self.plan_result_id}, {'status': 'running', 'start_time':datetime.datetime.now()})
        if not ret[0]==RT.SUCC:
            logger.error('update PlanResultTable [%s] failed' % self.plan_result_id)
            return
        test_result = stest.runPlan(self.plan_path)
        test_status = 'success' if test_result.wasSuccessful() else 'failed'
        test_start_time =test_result.startTime
        test_stop_time = test_result.stopTime
        log_file = open(self.log_path,'w')
        log_file.write(test_result.log.getvalue())
        log_file.close()
        ret = self.planResultTable.update({'id': self.plan_result_id}, {'status': test_status, 'start_time': test_start_time, 'stop_time': test_stop_time,'log':self.log_path})
        if not ret[0]==RT.SUCC:
            logger.error("update PlanResultTable's result [%s] failed" % self.plan_result_id)
            return

    def run(self):
        self.prepareTask()
        self.runTask()
        self.stopTask()

#status:new, waiting, running

def startPlanTask():
    planResultTable = PlanResultTable()
    while True:
        tp_tasks = []
        rt,tp_result_list = planResultTable.selectAll({'status':'new'})
        if not len(tp_result_list)==0:
            for tp_result in tp_result_list:
                tp_task = TestPlanTask(tp_result)
                tp_task.run()
        else:
            logger.info('none plan task found...')
            #print 'none plan task found...'
        time.sleep(0.5)

if __name__ == '__main__':
    startPlanTask()
