import os,sys
import threading
import time, datetime
import stest
cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../db/')
sys.path.append(cur_dir+'/../control/')
sys.path.append(cur_dir+'/../common/')
from table import PlanTable, PlanResultTable
from BaseControl import RT
import logging, logging.config
logging.config.fileConfig(cur_dir+'/../conf/log.conf')
logger = logging.getLogger('plantask')
class TestPlanTask(threading.Thread):
    def __init__(self, plan_result):
        self.plan_result_id = plan_result['id']
        self.plan_name = plan_result['plan_name']
        self.plan_path = os.path.normpath(cur_dir+'/../workbench/case/'+self.plan_name+'.json')
        self.log_path = os.path.normpath(cur_dir+'/../workbench/case/log/tp_'+self.plan_name+'_id_'+str(self.plan_result_id)+'.log')
        self.report_name = 'tp_'+self.plan_name+'_id_'+str(self.plan_result_id)
        self.report_path = os.path.normpath(cur_dir+'/../workbench/case/log/'+self.report_name+'.html')
        self.planTable = PlanTable()
        self.planResultTable = PlanResultTable()
        super(TestPlanTask, self).__init__()

    def prepareTask(self):
        logger.info('prepare plan task [%s],[%s]' % (self.plan_name,self.plan_result_id))

    def stopTask(self):
        logger.info('stop plan task[%s],[%s]' % (self.plan_name,self.plan_result_id))

    def runTask(self):
        logger.info('start run plan task')
        ret = self.planResultTable.update({'id': self.plan_result_id}, {'status': 'Running', 'start_time':datetime.datetime.now()})
        if not ret[0]==RT.SUCC:
            logger.error('update PlanResultTable [%s] failed' % self.plan_result_id)
            return
        ret = self.planTable.update({'name': self.plan_name}, {'last_status': 'Running'})
        if not ret[0]==RT.SUCC:
            logger.error("update PlanTable's status [%s] failed" % self.plan_name)
            return
        test_result = stest.runPlan(self.plan_path)
        test_status = 'Success' if test_result.wasSuccessful() else 'Failed'
        test_start_time =test_result.startTime
        test_stop_time = test_result.stopTime
        log_file = open(self.log_path,'w')
        log_file.write(test_result.log.getvalue())
        log_file.close()
        #htmlReport
        report_file = open(self.report_path,'w')
        report_file.write(test_result.html_report)
        report_file.close()

        ret = self.planTable.update({'name': self.plan_name}, {'last_status': test_status})
        if not ret[0]==RT.SUCC:
            logger.error("update PlanTable's status [%s] failed" % self.plan_name)
            return
        ret = self.planResultTable.update({'id': self.plan_result_id}, {'status': test_status, 'start_time': test_start_time, 'stop_time': test_stop_time,'log':self.log_path, 'report': self.report_name})
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

def startPlanSchedulerTask():
    planTable = PlanTable()
    rt, plans = planTable.selectAll({'timed': 1})
    if not len(plans) == 0:
        from apscheduler.schedulers.background import BackgroundScheduler
        scheduler = BackgroundScheduler()
        for plan in plans:
            start_time = datetime.datetime.strptime(plan['crontab'], "%Y-%m-%d %H:%M:%S")
            scheduler.add_job(runPlan, 'interval', days=1, next_run_time=start_time, args=[plan])
        scheduler.start()

def runPlan(plan):
    planResultTable = PlanResultTable()
    plan_result = {}
    plan_result['plan_name'] = plan['name']
    plan_result['status'] = 'new'
    plan_result['type'] = '1'
    ret = planResultTable.insert(plan_result)

if __name__ == '__main__':
    startPlanSchedulerTask()
    startPlanTask()
