import os

def kill(pid=None, keyword=None):
    if pid:
        return killByPid(pid)
    if keyword:
        return killByKeyword(keyword)

def killByPid(pid):
    ret = os.system('kill %s'%pid)
    if not ret==0:
        return False
    return True

def killByKeyword(keyword):
    ps_info = os.popen('ps |grep %s'% keyword)
    pids = []
    for line in ps_info:
        infos = line.split(' ')
        pids.append(infos[0])
    for pid in pids:
        killByPid(pid)
    return True

def list():
    pass

if __name__ == '__main__':
    pass
