import os,sys
import json
import web

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../control/')
sys.path.append(cur_dir+'/../lib/')

from DriverControl import DriverController
from CaseControl import CaseController
from PlanControl import PlanController
from AppControl import AppController
from BaseControl import BaseController
from BaseControl import RT
import ps_util

web.config.debug = False

urls = (
    "/","Index",
    "/dashboard","Dashboard",
    "/setting","Setting",
    "/driver","ListDriver",
    "/driver/(\d+)","ViewDriver",
    "/driver/(\d+)/mod","ModifyDriver",
    "/driver/(\d+)/del","DeleteDriver",
    "/driver/add","AddDriver",
    "/case","ListCase",
    "/case/(\d+)","ViewCase",
    "/case/(\d+)/mod","ModifyCase",
    "/case/(\d+)/del","DeleteCase",
    "/case/(\d+)/run","RunCase",
    "/case/(.+)/result","ListCaseResult",
    "/case/add","AddCase",
    "/plan","ListPlan",
    "/plan/(\d+)","ViewPlan",
    "/plan/(\d+)/mod","ModifyPlan",
    "/plan/(\d+)/run","RunPlan",
    "/plan/(\d+)/del","DelPlan",
    "/plan/(.+)/result","ListPlanResult",
    "/plan/add","AddPlan",
    "/report/(.+)","ViewReport",
    "/app","ListApp",
    "/app/(\d+)","ViewApp",
    "/app/(\d+)/mod","ModifyApp",
    "/app/(\d+)/del","DeleteApp",
    "/app/add","AddApp",
    "/app/(\d+)/release","ReleaseApp"
)

app = web.application(urls, globals(), autoreload = True)

if web.config.get('_session') is None:
    store = web.session.DiskStore(cur_dir + '/sessionStore')
    session = web.session.Session(app, store)
else:
    session = web.config._session

render = web.template.render(cur_dir + '/template/', base='base', cache = False, globals={'session': session})
no_base_render = web.template.render(cur_dir + '/template/', cache = False, globals={'session': session})

class Index:
    def GET(self):
        web.seeother('/dashboard')

class Dashboard:
    def GET(self):
        driverCtl = DriverController()
        caseCtl = CaseController()
        planCtl = PlanController()
        appCtl = AppController()
        statisticInfo={}
        totalDrivers = driverCtl.count()
        totalCases = caseCtl.count()
        totalPlans = planCtl.count()
        totalApps = appCtl.count()
        statisticInfo['totalDrivers'] = totalDrivers
        statisticInfo['totalCases'] = totalCases
        statisticInfo['totalPlans'] = totalPlans
        statisticInfo['totalApps'] = totalApps
        #plan statistic
        succPlans = planCtl.countPlanResult({'status':'success'})
        errPlans = planCtl.countPlanResult({'status':'failed'})
        rngPlans = planCtl.countPlanResult({'status':'running'})
        statisticInfo['succPlans'] = succPlans
        statisticInfo['errPlans'] = errPlans
        statisticInfo['rngPlans'] = rngPlans
        #case statistic
        succCases = planCtl.countPlanResult({'status':'success'})
        errCases = planCtl.countPlanResult({'status':'failed'})
        rngCases = planCtl.countPlanResult({'status':'running'})
        statisticInfo['succCases'] = succCases
        statisticInfo['errCases'] = errCases
        statisticInfo['rngCases'] = rngCases
        #app info
        apps = appCtl.getAllApps()
        statisticInfo['apps'] = apps
        return render.dashboard(statisticInfo)

class Setting:
    def GET(self):
        return render.setting()

class ListDriver(object):
    def POST(self):
        ctl = DriverController()
        submit_data = web.input()
        startIndex = int(submit_data['startIndex'])
        bufferSize = int(submit_data['bufferSize'])
        ret = ctl.getDrivers(startIndex, startIndex+bufferSize)
        totalDataNo = ctl.count()
        result = {"pageData": ret[1], "startIndex": startIndex, "bufferSize": bufferSize, "totalDataNo": totalDataNo}
        return json.dumps(result)

    def GET(self):
        return render.listDriver()

class DeleteDriver(object):
    def POST(self, id):
        ctl = DriverController()
        #ret = ctl.deleteDriver(id)
        return [RT.SUCC,'']

class ViewDriver(object):
    def GET(self, id):
        ctl = DriverController()
        ret = ctl.getDriver(id)
        if not ret:
            return render.notFound()
        return render.driver(ret)

class AddDriver(object):
    def GET(self):
        return render.addDriver()

    def POST(self):
        submit_data = web.input()
        ctl = DriverController()
        ret = ctl.addDriver(submit_data)
        if not ret[0] == RT.SUCC:
            return [RT.ERR, ret[1]]
        driver = ctl.getDriverByName(submit_data['name'])
        if not driver:
            return [RT.ERR, 'insert driver succ, select error']
        return [RT.SUCC, driver['id']]

class ListCase(object):
    def POST(self):
        ctl = CaseController()
        submit_data = web.input()
        startIndex = int(submit_data['startIndex'])
        bufferSize = int(submit_data['bufferSize'])
        ret = ctl.getCases(startIndex, startIndex+bufferSize)
        totalDataNo = ctl.count()
        result = {"pageData": ret[1], "startIndex": startIndex, "bufferSize": bufferSize, "totalDataNo": totalDataNo}
        return json.dumps(result)

    def GET(self):
        return render.listCase()

class DeleteCase(object):
    def POST(self, id):
        ctl = CaseController()
        #ret = ctl.deleteCase(id)
        return [RT.SUCC,'']

class ViewCase(object):
    def GET(self, id):
        ctl = CaseController()
        ret = ctl.getCase(id)
        print ret
        if not ret:
            return render.notFound()
        isExecuted = False if (ctl.countCaseResult({'case_name': ret['name']})==0) else True
        return render.case(ret, isExecuted)

class AddCase(object):
    def GET(self):
        ctl = DriverController()
        driver_list = ctl.getAllDrivers()
        driver_map = ctl.getAllDriversMap()
        return render.addCase(driver_list, json.dumps(driver_map))

    def POST(self):
        submit_data = web.input()
        ctl = CaseController()
        ret = ctl.addCase(submit_data)
        if not ret[0] == RT.SUCC:
            return [RT.ERR, ret[1]]
        case = ctl.getCaseByName(submit_data['name'])
        print case
        if not case:
            return [RT.ERR, 'insert case succ, select error']
        return [RT.SUCC, case['id']]

class RunCase(object):
    def POST(self, case_id):
        ctl = CaseController()
        ret = ctl.runCase(case_id)
        if not ret[0]==RT.SUCC:
            return [RT.ERR, ret[1]]
        return [RT.SUCC, '']

class ListCaseResult(object):
    def POST(self, case_name):
        ctl = CaseController()
        submit_data = web.input()
        startIndex = int(submit_data['startIndex'])
        bufferSize = int(submit_data['bufferSize'])
        ret = ctl.getCaseResults(startIndex, startIndex+bufferSize, {'case_name': case_name},{'id': 'desc'})
        totalDataNo = ctl.countCaseResult({'case_name': case_name})
        result = {"pageData": ret[1], "startIndex": startIndex, "bufferSize": bufferSize, "totalDataNo": totalDataNo}
        return json.dumps(result)

class ListPlan(object):
    def POST(self):
        ctl = PlanController()
        submit_data = web.input()
        startIndex = int(submit_data['startIndex'])
        bufferSize = int(submit_data['bufferSize'])
        ret = ctl.getPlans(startIndex, startIndex+bufferSize)
        totalDataNo = ctl.count()
        result = {"pageData": ret[1], "startIndex": startIndex, "bufferSize": bufferSize, "totalDataNo": totalDataNo}
        return json.dumps(result)

    def GET(self):
        return render.listPlan()

class DeletePlan(object):
    def POST(self, id):
        ctl = PlanController()
        #ret = ctl.deletePlan(id)
        return [RT.SUCC,'']

class ViewPlan(object):
    def GET(self, id):
        ctl = PlanController()
        ret = ctl.getPlan(id)
        if not ret:
            return render.notFound()
        isExecuted = False if (ctl.countPlanResult({'plan_name': ret['name']})==0) else True
        return render.plan(ret, isExecuted)

class AddPlan(object):
    def GET(self):
        return render.addPlan()

    def POST(self):
        submit_data = web.input()
        ctl = PlanController()
        ret = ctl.addPlan(submit_data)
        if not ret[0] == RT.SUCC:
            return [RT.ERR, ret[1]]
        plan = ctl.getPlanByName(submit_data['name'])
        if not plan:
            return [RT.ERR, 'insert plan succ, select error']
        return [RT.SUCC, plan['id']]

class RunPlan(object):
    def POST(self, plan_id):
        ctl = PlanController()
        ret = ctl.runPlan(plan_id)
        if not ret[0]==RT.SUCC:
            return [RT.ERR, ret[1]]
        return [RT.SUCC, '']

class ListPlanResult(object):
    def POST(self, plan_name):
        ctl = PlanController()
        submit_data = web.input()
        startIndex = int(submit_data['startIndex'])
        bufferSize = int(submit_data['bufferSize'])
        ret = ctl.getPlanResults(startIndex, startIndex+bufferSize,{'plan_name': plan_name}, {'id': 'desc'})
        totalDataNo = ctl.countPlanResult()
        result = {"pageData": ret[1], "startIndex": startIndex, "bufferSize": bufferSize, "totalDataNo": totalDataNo}
        return json.dumps(result)

class ViewReport(object):
    def GET(self,report):
        return web.template.frender(cur_dir + '/../workbench/case/log/'+report+'.html')()

class ListApp(object):
    def POST(self):
        ctl = AppController()
        submit_data = web.input()
        startIndex = int(submit_data['startIndex'])
        bufferSize = int(submit_data['bufferSize'])
        apps = ctl.getAllApps(startIndex, startIndex+bufferSize)
        return json.dumps(apps)

    def GET(self):
        ctl = AppController()
        apps = ctl.getAllApps()
        return render.listApp(apps)

class DeleteApp(object):
    def POST(self, id):
        ctl = AppController()
        #ret = ctl.deleteApp(id)
        return [RT.SUCC,'']

class ViewApp(object):
    def GET(self, id):
        ctl = AppController()
        ret = ctl.getApp(id)
        if not ret:
            return render.notFound()
        return render.app(ret)

class AddApp(object):
    def GET(self):
        return render.addApp()

    def POST(self):
        submit_data = web.input()
        ctl = AppController()
        ret = ctl.addApp(submit_data)
        if not ret[0] == RT.SUCC:
            return [RT.ERR, ret[1]]
        plan = ctl.getAppByName(submit_data['name'])
        if not plan:
            return [RT.ERR, 'insert plan succ, select error']
        #return [RT.SUCC, plan['id']]
        return render.app(plan)

class ReleaseApp(object):
    def POST(self, id):
        ctl = AppController()
        ret = ctl.releaseApp(id)
        if not ret[0]==RT.SUCC:
            return [RT.ERR, ret[1]]
        return [RT.SUCC, ret[1]]

#enable task Thread
def startTestTask():
    ps_util.kill(keyword='TestCaseTask')
    ps_util.kill(keyword='TestPlanTask')
    tc_task_script = cur_dir+'/../control/TestCaseTask.py'
    tc_task_log = cur_dir+'/../log/caseTask.log'
    tp_task_script = cur_dir+'/../control/TestPlanTask.py'
    tp_task_log = cur_dir+'/../log/planTask.log'
    #print os.system('python %s >>%s 2>&1 &' % (tc_task_script,tc_task_log))
    #print os.system('python %s >>%s 2>&1 &' % (tp_task_script,tp_task_log))
    os.system('python %s &' % tc_task_script)
    os.system('python %s &' % tp_task_script)

if __name__ == "__main__":
    startTestTask()
    app.run()
