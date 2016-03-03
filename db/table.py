#encoding = utf-8
import os,sys
import time
import re
import types
import json
reload(sys)
sys.setdefaultencoding('utf8')
import mysql_wrapper
import logging, logging.config

cur_dir = os.path.split(os.path.realpath(__file__))[0]

class Result(object):
    SUCC = 0
    EMPTY = 1
    DUP = 2
    ERR = 3

RT = Result()

class BaseTable(object):
    logging.config.fileConfig(os.path.join(cur_dir, 'log.conf'))
    logger = logging.getLogger("db")
    def __init__(self):
        self.db = mysql_wrapper.MysqlWrapper()

    def execute(self, line):
        return self.db_wrapper.execute(line)

    def normalize_str(self, in_str):
        out_str = in_str.replace('\\','\\\\')
        out_str = re.sub(r'"','\\"', out_str)
        return out_str

    def clean(self,cond_str):
        if not self.db_wrapper.clear_rows_by_condition(self.TABLE_NAME, cond_str):
            self.logger.error('delete data from table %s, cond_str = %s' % (self.TABLE_NAME, cond_str))
            return(RT.ERR,'')
        return (RT.SUCC,'')

    def _process_bslash(self, in_dict):
        for k in in_dict.keys():
            v=in_dict[k]
            if type(v) == types.StringType or type(v) == types.UnicodeType:
                v = re.sub(r'\\',r'\\\\', v)
                v = re.sub(r'"',r'\\"', v)
                v = re.sub(r"'",r"\\'", v)
            in_dict[k] = v

    def select(self, id):
        ret = self.db.get_row_by_id(self.TABLE_NAME, id)
        if len(ret) == 0:
            self.logger.error('select item from %s failed and ID = [%s]' % (self.TABLE_NAME, id))
            return (RT.ERR, '')
        return [RT.SUCC, ret]

    def selectByName(self, name):
        ret = self.db.get_row(self.TABLE_NAME, 'name', name)
        if len(ret) == 0:
            self.logger.error('select item from %s failed and name = [%s]' % (self.TABLE_NAME, name))
            return (RT.ERR, '')
        return (RT.SUCC, ret)

    def selects(self, start, limit, cond_dict={}, order_dict={}):
        ret = self.db.get_rows_by_dict(self.TABLE_NAME, start, limit, cond_dict, order_dict=order_dict)
        return (RT.SUCC, ret)

    def count(self, cond_dict={}):
        ret = self.db.count(self.TABLE_NAME, cond_dict)
        if ret == -1:
            self.logger.error('count item of %s failed' % self.TABLE_NAME)
            return (RT.ERR, '')
        return (RT.SUCC, ret)

    def insert(self, item_dict):
        self._process_bslash(item_dict)
        cond_dict={}
        cond_dict['name'] = item_dict['name']
        if not self.db.isunique_by_dict(self.TABLE_NAME, cond_dict):
            self.logger.error('duplicate data in %s [%s]' % (self.TABLE_NAME, item_dict['name']))
            return (RT.DUP, 'duplicate item')
        ret = self.db.insert_row(self.TABLE_NAME, item_dict)
        if not ret:
            return (RT.ERR, 'somthing error failed when insert item to %s' % self.TABLE_NAME)
        return (RT.SUCC, '')

    def update(self, cond_dict, value_map):
        ret = self.db.update_value_by_dict(self.TABLE_NAME, cond_dict, value_map)
        if not ret:
            return (RT.ERR, 'somthing error failed when update item to %s' % self.TABLE_NAME)
        return (RT.SUCC, ret)

    def selectAll(self,cond_dict={}, order_dict={}):
        ret = self.db.get_all_rows_by_dict(self.TABLE_NAME, cond_dict, order_dict=order_dict)
        return (RT.SUCC, ret)

def gen_field_str(field_dict):
    return field_dict['name'] + ' ' + field_dict['type']  + ' ' + field_dict['attr']

class SystemOptionTable(BaseTable):
    TABLE_NAME = 'T_SYSTEM_OPTION'
    ID= {'name':'id', 'type':'INT(4)', 'attr':'NOT NULL AUTO_INCREMENT'}
    NAME = {'name':'name', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    CODE = {'name':'code', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    STANDARD = {'name':'standard', 'type':'CHAR(40)', 'attr':''}
    DESCRIPTION = {'name':'description', 'type':'CHAR(100)', 'attr':''}

    CRtab_SQL = 'CREATE TABLE ' + TABLE_NAME + '('\
            + gen_field_str(ID) + ','\
            + gen_field_str(NAME) + ','\
            + gen_field_str(CODE) + ','\
            + gen_field_str(STANDARD) + ','\
            + gen_field_str(DESCRIPTION) + ','\
            + 'PRIMARY KEY(id)'\
            + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'

    DROPtab_SQL = 'DROP table ' + TABLE_NAME

class AccountTable(BaseTable):
    TABLE_NAME = 'T_ACCOUNT'
    ID= {'name':'id', 'type':'INT(4)', 'attr':'NOT NULL AUTO_INCREMENT'}
    USERNAME = {'name':'username', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    PASSWORD = {'name':'password', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    NAME = {'name':'name', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    IS_SUPER = {'name':'is_super', 'type':'BOOL', 'attr':'NOT NULL DEFAULT 0'}
    CREATE_DATE = {'name':'create_date', 'type':'DATETIME', 'attr':'NOT NULL'}

    CRtab_SQL = 'CREATE TABLE ' + TABLE_NAME + '('\
            + gen_field_str(ID) + ','\
            + gen_field_str(USERNAME) + ','\
            + gen_field_str(PASSWORD) + ','\
            + gen_field_str(NAME) + ','\
            + gen_field_str(IS_SUPER) + ','\
            + gen_field_str(CREATE_DATE) + ','\
            + 'PRIMARY KEY(id)'\
            + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'

    DROPtab_SQL = 'DROP table ' + TABLE_NAME

class DriverTable(BaseTable):
    TABLE_NAME = 'T_DRIVER'
    ID= {'name':'id', 'type':'INT(4)', 'attr':'NOT NULL AUTO_INCREMENT'}
    NAME = {'name':'name', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    DESCRIPTION = {'name':'description', 'type':'TEXT', 'attr':''}
    PARAM = {'name':'param', 'type':'TEXT', 'attr':'NOT NULL'}
    SETUPPY = {'name':'setuppy', 'type':'TEXT', 'attr':'NOT NULL'}
    TEARDOWNPY = {'name':'teardownpy', 'type':'TEXT', 'attr':'NOT NULL'}
    EXECPY = {'name':'execpy', 'type':'TEXT', 'attr':'NOT NULL'}

    CRtab_SQL = 'CREATE TABLE ' + TABLE_NAME + '('\
            + gen_field_str(ID) + ','\
            + gen_field_str(NAME) + ','\
            + gen_field_str(DESCRIPTION) + ','\
            + gen_field_str(PARAM) + ','\
            + gen_field_str(SETUPPY) + ','\
            + gen_field_str(TEARDOWNPY) + ','\
            + gen_field_str(EXECPY) + ','\
            + 'PRIMARY KEY(id)'\
            + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'

    DROPtab_SQL = 'DROP table ' + TABLE_NAME

class CaseTable(BaseTable):
    TABLE_NAME = 'T_CASE'
    ID= {'name':'id', 'type':'INT(4)', 'attr':'NOT NULL AUTO_INCREMENT'}
    NAME = {'name':'name', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    DESCRIPTION = {'name':'description', 'type':'TEXT', 'attr':'NOT NULL'}
    PARAM = {'name':'param', 'type':'TEXT', 'attr':'NOT NULL'}
    DRIVER = {'name':'driver', 'type':'CHAR(40)', 'attr':'NOT NULL'}

    CRtab_SQL = 'CREATE TABLE ' + TABLE_NAME + '('\
            + gen_field_str(ID) + ','\
            + gen_field_str(NAME) + ','\
            + gen_field_str(DESCRIPTION) + ','\
            + gen_field_str(PARAM) + ','\
            + gen_field_str(DRIVER) + ','\
            + 'PRIMARY KEY(id)'\
            + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'

    DROPtab_SQL = 'DROP table ' + TABLE_NAME

class CaseResultTable(BaseTable):
    TABLE_NAME = 'T_CASE_RESULT'
    ID= {'name':'id', 'type':'INT(4)', 'attr':'NOT NULL AUTO_INCREMENT'}
    CASENAME = {'name':'case_name', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    CREATETIME = {'name':'create_time', 'type':'DATETIME', 'attr':''}
    STATUS = {'name':'description', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    LOG = {'name':'driver', 'type':'TEXT', 'attr':''}
    STARTTIME = {'name':'start_time', 'type':'DATETIME', 'attr':''}
    STOPTIME = {'name':'stop_time', 'type':'DATETIME', 'attr':''}
    USER = {'name':'user', 'type':'CHAR(40)', 'attr':''}
    DESCRIPTION = {'name':'description', 'type':'TEXT', 'attr':''}

    CRtab_SQL = 'CREATE TABLE ' + TABLE_NAME + '('\
            + gen_field_str(ID) + ','\
            + gen_field_str(CASENAME) + ','\
            + gen_field_str(CREATETIME) + ','\
            + gen_field_str(STATUS) + ','\
            + gen_field_str(LOG) + ','\
            + gen_field_str(STARTTIME) + ','\
            + gen_field_str(STOPTIME) + ','\
            + gen_field_str(DESCRIPTION) + ','\
            + 'PRIMARY KEY(id)'\
            + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'

    DROPtab_SQL = 'DROP table ' + TABLE_NAME
    def insert(self, item_dict):
        self._process_bslash(item_dict)
        ret = self.db.insert_row(self.TABLE_NAME, item_dict)
        if not ret:
            return (RT.ERR, 'somthing error failed when insert item to %s' % self.TABLE_NAME)
        return (RT.SUCC, '')

class PlanTable(BaseTable):
    TABLE_NAME = 'T_PLAN'
    ID= {'name':'id', 'type':'INT(4)', 'attr':'NOT NULL AUTO_INCREMENT'}
    NAME = {'name':'name', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    DESCRIPTION = {'name':'description', 'type':'TEXT', 'attr':'NOT NULL'}
    CASE_LIST = {'name':'case_list', 'type':'TEXT', 'attr':'NOT NULL'}
    LASE_STATUS = {'name':'last_status', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    CRONTAB = {'name':'crontab', 'type':'CHAR(100)', 'attr':'NOT NULL'}
    PEOPLE = {'name':'poeple', 'type':'TEXT', 'attr':'NOT NULL'}

    CRtab_SQL = 'CREATE TABLE ' + TABLE_NAME + '('\
            + gen_field_str(ID) + ','\
            + gen_field_str(NAME) + ','\
            + gen_field_str(DESCRIPTION) + ','\
            + gen_field_str(CASE_LIST) + ','\
            + gen_field_str(LASE_STATUS) + ','\
            + gen_field_str(CRONTAB) + ','\
            + gen_field_str(PEOPLE) + ','\
            + 'PRIMARY KEY(id)'\
            + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'

    DROPtab_SQL = 'DROP table ' + TABLE_NAME

class PlanResultTable(BaseTable):
    TABLE_NAME = 'T_PLAN_RESULT'
    ID= {'name':'id', 'type':'INT(4)', 'attr':'NOT NULL AUTO_INCREMENT'}
    PLANNAME = {'name':'plan_name', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    CREATETIME = {'name':'create_time', 'type':'DATETIME', 'attr':''}
    STATUS = {'name':'description', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    LOG = {'name':'driver', 'type':'text', 'attr':'NOT NULL'}
    STARTTIME = {'name':'start_time', 'type':'DATETIME', 'attr':'NOT NULL'}
    STOPTIME = {'name':'stop_time', 'type':'DATETIME', 'attr':'NOT NULL'}
    USER = {'name':'user', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    DESCRIPTION = {'name':'description', 'type':'TEXT', 'attr':''}

    CRtab_SQL = 'CREATE TABLE ' + TABLE_NAME + '('\
            + gen_field_str(ID) + ','\
            + gen_field_str(PLANNAME) + ','\
            + gen_field_str(CREATETIME) + ','\
            + gen_field_str(STATUS) + ','\
            + gen_field_str(LOG) + ','\
            + gen_field_str(STARTTIME) + ','\
            + gen_field_str(STOPTIME) + ','\
            + gen_field_str(DESCRIPTION) + ','\
            + 'PRIMARY KEY(id)'\
            + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'

    DROPtab_SQL = 'DROP table ' + TABLE_NAME
    def insert(self, item_dict):
        self._process_bslash(item_dict)
        ret = self.db.insert_row(self.TABLE_NAME, item_dict)
        if not ret:
            return (RT.ERR, 'somthing error failed when insert item to %s' % self.TABLE_NAME)
        return (RT.SUCC, '')

class AppTable(BaseTable):
    TABLE_NAME = 'T_APP'
    ID= {'name':'id', 'type':'INT(4)', 'attr':'NOT NULL AUTO_INCREMENT'}
    NAME = {'name':'name', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    DESCRIPTION = {'name':'description', 'type':'TEXT', 'attr':''}
    STATUS = {'name':'status', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    TYPE = {'name':'type', 'type':'CHAR(40)', 'attr':'NOT NULL'}
    SCRIPT = {'name':'script', 'type':'TEXT', 'attr':''}
    ACCESSURL = {'name':'access_url', 'type':'CHAR(100)', 'attr':''}
    REPOSITORYTYPE = {'name':'repository_type', 'type':'CHAR(40)', 'attr':''}
    REPOSITORYPATH = {'name':'repository_path', 'type':'CHAR(100)', 'attr':''}
    LASTRELEASETIME = {'name':'last_release_time', 'type':'DATETIME', 'attr':''}
    LASTRELEASESTATUS = {'name':'last_release_status', 'type':'CHAR(40)', 'attr':''}
    LASTRELEASELOG = {'name':'last_release_log', 'type':'CHAR(100)', 'attr':''}
    LASTRELEASEINFO = {'name':'last_release_info', 'type':'CHAR(100)', 'attr':''}

    CRtab_SQL = 'CREATE TABLE ' + TABLE_NAME + '('\
            + gen_field_str(ID) + ','\
            + gen_field_str(NAME) + ','\
            + gen_field_str(DESCRIPTION) + ','\
            + gen_field_str(STATUS) + ','\
            + gen_field_str(TYPE) + ','\
            + gen_field_str(ACCESSURL) + ','\
            + gen_field_str(SCRIPT) + ','\
            + gen_field_str(REPOSITORYPATH) + ','\
            + gen_field_str(REPOSITORYTYPE) + ','\
            + gen_field_str(LASTRELEASETIME) + ','\
            + gen_field_str(LASTRELEASESTATUS) + ','\
            + gen_field_str(LASTRELEASELOG) + ','\
            + gen_field_str(LASTRELEASEINFO) + ','\
            + 'PRIMARY KEY(id)'\
            + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'

    DROPtab_SQL = 'DROP table ' + TABLE_NAME

if __name__ == '__main__':
    #DRIVER TEST

    t = DriverTable()
    param ={"a":2,"b":7,"duedata":14}
    setup ='''print 'setup!'
'''
    teardown ='''print 'teardown!'
'''
    exex='assert (self.a*self.b == self.duedata)'
    description ='mutiply driver'
    item_dict = {'name':'t5','param':json.dumps(param),'setuppy':setup,'teardownpy':teardown,'execpy':exex,'description':description}
    #print item_dict
    print t.insert(item_dict)
    #print t.select(1)
    #print t.selects(0,2)
    #print len(t.selects(1,2))
    print t.count()
