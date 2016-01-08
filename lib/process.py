import os
import time
import tempfile

def run(cmd):
    process = Process()
    returnCode, stdout, stderr = process.run(cmd)
    return returnCode, stdout, stderr

class Process(object):
    def run(self, cmd, retryTimes=5):
        for i in range(retryTimes):
            returnCode, stdout, stderr = self.runOnce(cmd)
            if returnCode != 0:
                print '[ERROR]. run cmd [%s] failed! retry %s...' % ( cmd, i + 1)
                time.sleep(1)
            else:
                return returnCode, stdout, stderr
        return returnCode, stdout, stderr

    def runOnce(self, cmd):
        stdoutFile = tempfile.NamedTemporaryFile()
        stderrFile = tempfile.NamedTemporaryFile()
        cmd = '%(cmd)s 1>>%(out)s 2>>%(err)s' %\
            {'cmd': cmd,\
                 'out': stdoutFile.name,\
                 'err': stderrFile.name}
        returnCode = os.system(cmd)
        stdout = stdoutFile.read()
        stderr = stderrFile.read()
        stdoutFile.close()
        stderrFile.close()
        return returnCode, stdout, stderr
