import os
import web

web.config.debug = False

urls = (
    "/","Index",
    "/dashboard","Dashboard",
    "/getData","pageList"
)

cur_dir = os.path.split(os.path.realpath(__file__))[0]

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
        return no_base_render.index()
class Dashboard:
    def GET(self):
        return render.dashboard()

class pageList(object):
    def POST(self):
        data = [
            {
                "task": "Go to US",
                "time": "2010-09-05",
                "location": "1"
            },
            {
                "task": "Come back China",
                "time": "2010-09-15",
                "location": "2"
            },
            {
                "task": "Go to lab",
                "time": "2010-09-20",
                "location": "3"
            },
            {
                "task": "Go to Shopping",
                "time": "2010-09-25",
                "location": "4"
            },
            {
                "task": "Attend conference",
                "time": "2010-09-30",
                "location": "5"
            },
            {
                "task": "View TV",
                "time": "2010-10-01",
                "location": "6"
            },
            {
                "task": "View SAKAI",
                "time": "2010-10-02",
                "location": "7"
            },
            {
                "task": "View Movie",
                "time": "2010-10-01",
                "location": "8"
            },
            {
                "task": "Review papers",
                "time": "2010-10-03",
                "location": "9"
            },
            {
                "task": "1sdfsdf papers",
                "time": "2010-10-03",
                "location": "10"
            },
            {
                "task": "Go to US",
                "time": "2010-09-05",
                "location": "11"
            },
            {
                "task": "Come back China",
                "time": "2010-09-15",
                "location": "12"
            },
            {
                "task": "Go to lab",
                "time": "2010-09-20",
                "location": "13"
            },
            {
                "task": "Go to Shopping",
                "time": "2010-09-25",
                "location": "14"
            },
            {
                "task": "Attend conference",
                "time": "2010-09-30",
                "location": "15"
            },
            {
                "task": "View TV",
                "time": "2010-10-01",
                "location": "16"
            },
            {
                "task": "View SAKAI",
                "time": "2010-10-02",
                "location": "17"
            },
            {
                "task": "View Movie",
                "time": "2010-10-01",
                "location": "18"
            },
            {
                "task": "Review papers",
                "time": "2010-10-03",
                "location": "19"
            },
            {
                "task": "1sdfsdf papers",
                "time": "2010-10-03",
                "location": "20"
            }
        ]
        submit_data = web.input()
        startIndex = int(submit_data['startIndex'])
        bufferSize = int(submit_data['bufferSize'])
        pageData = []
        i = 0
        while i<bufferSize:
            pageData.append(data[startIndex+i])
            i=i+1
        totalDataNo = len(data)
        result = {'pageData': pageData, 'startIndex': startIndex, 'bufferSize':bufferSize}
        print result
        return result       

if __name__ == "__main__":
    app.run()
