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
        self.plan_name = plan_result['plan']
        self.plan_path = cur_dir+'/../workbench/plan/'+self.plan_name
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
        result = stest.runCase(self.plan_name)
        ret = self.planResultTable.update({'id': self.plan_result_id}, {'status': 'success', 'start_time':datetime.datetime.now()})
        if not ret[0]==RT.SUCC:
            logger.error('update PlanResultTable [%s] failed' % self.plan_result_id)
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
                tp_tasks.append(tp_task)
            for task in tp_tasks:
                task.start()
        else:
            logger.info('none plan task found...')
            #print 'none plan task found...'
        time.sleep(0.5)

if __name__ == '__main__':
    startPlanTask()
