import os

BUILD_SUCCESSFUL = "BUILD SUCCESSFUL"
BUILD_FAILED = "BUILD FAILED"

def build(build_file, ant_target, log_file=None):
    ant_cmd = "ant -f %s %s 2>&1" % (build_file, ant_target)
    status = 1
    ret = os.popen(ant_cmd)
    if log_file:
        log_file_name = log_file
        log_file = open(log_file_name,"w+")
        log_file.write(ret.read())
        log_file.flush()
        log_file.close()
        ret = open(log_file_name,"r").readlines()
    for line in ret:
        print line
        if BUILD_SUCCESSFUL in line:
            status = 0
    return status
    
if __name__ == '__main__':
    print build('/Users/wangming/workspace/atrs/workbench/release/compile_war.xml','generate.orignal.war')
