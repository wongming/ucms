import os,sys
import json
import web

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../control/')

import DriverControl
import CaseControl

web.config.debug = False

urls = (
    "/","Index",
    "/dashboard","Dashboard",
    "/driver","ListDriver",
    "/driver/(.+)","ViewDriver",
    "/case","ListCase",
    "/case/(.+)","ViewCase"
)

app = web.application(urls, globals(), autoreload = False)

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
        return render.dashboard()

class ListDriver(object):
    def POST(self):
        ctl = DriverControl.DriverController()
        submit_data = web.input()
        startIndex = int(submit_data['startIndex'])
        bufferSize = int(submit_data['bufferSize'])
        ret = ctl.getDrivers(startIndex, startIndex+bufferSize)
        totalDataNo = ctl.count()
        result = {"pageData": ret[1], "startIndex": startIndex, "bufferSize": bufferSize, "totalDataNo": totalDataNo}
        return json.dumps(result)

    def GET(self):
        return render.listDriver()

class ViewDriver(object):
    def GET(self, id):
        ctl = DriverControl.DriverController()
        ret = ctl.getDriver(id)
        if not ret:
            return render.notFound()
        return render.driver(ret)

class ListCase(object):
    def POST(self):
        ctl = CaseControl.CaseController()
        submit_data = web.input()
        startIndex = int(submit_data['startIndex'])
        bufferSize = int(submit_data['bufferSize'])
        ret = ctl.getCases(startIndex, startIndex+bufferSize)
        totalDataNo = ctl.count()
        result = {"pageData": ret[1], "startIndex": startIndex, "bufferSize": bufferSize, "totalDataNo": totalDataNo}
        return json.dumps(result)
    def GET(self):
        return render.listCase()

class ViewCase(object):
    def GET(self, id):
        ctl = CaseControl.CaseController()
        ret = ctl.getCase(id)
        if not ret:
            return render.notFound()
        return render.case(ret)

if __name__ == "__main__":
    app.run()
