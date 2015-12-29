# -*- coding: utf-8 -*-
import sys,os
import inspect, types
import re
import md5
import traceback
reload(sys)
sys.setdefaultencoding('utf8')
cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_dir+'/../db/')
sys.path.append(cur_dir+'/../common/')
sys.path.append(cur_dir+'/../conf/')
import logging, logging.config
import ConfigParser
import collections
import copy
import urllib
import urllib2

class RT(object):
    SUCC = 0
    EMPTY = 1
    DUP = 2
    ERR = 3

class BaseController(object):
    logging.config.fileConfig(cur_dir+'/../conf/log.conf')
    logger = logging.getLogger("control")
    #conf = ConfigParser.ConfigParser()
    #conf.optionxform = str
    #conf.read(cur_dir+'/../conf/common.cfg')
    pass

    def _post_RTS(self, url, param):
        try:
            param = urllib.urlencode(param)
            req = urllib2.Request(url,param)
            rep = urllib2.urlopen(req)
            ret = rep.read()
            #print ret
            ret = (RT.SUCC, ret)
        except Exception,e:
            err = traceback.format_exc()
            print err
            ret = (RT.IERR,'unknow reason')
        return ret
    def _get_RTS(self, url):
        try:
            req = urllib2.Request(url)
            rep = urllib2.urlopen(req)
            ret = rep.read()
            #print ret
            ret = (RT.SUCC, ret)
        except Exception,e:
            err = traceback.format_exc()
            print err
            ret = (RT.IERR,'unknow reason')
        return ret

if __name__ == '__main__':
    pass
