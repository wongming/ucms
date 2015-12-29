import os,sys
import json
import web

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../control/')

import DriverControl

web.config.debug = False

urls = (
    "/","Index",
    "/dashboard","Dashboard",
    "/driver","ListDriver",
    "/driver/(.+)","ViewDriver"
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

def _process_bslash(self, in_dict):
    for k in in_dict.keys():
        v=in_dict[k]
        if type(v) == types.StringType or type(v) == types.UnicodeType:
            v = re.sub(r'\\',r'\\\\', v)
            v = re.sub(r'"',r'\\"', v)
            v = re.sub(r"'",r"\\'", v)
        in_dict[k] = v
if __name__ == "__main__":
    app.run()
