#!/bin/env python
import os, tempfile, sys
import time
#import paramiko

def ExecuteCmd(cmd, printDetail=True, remoteCmd=False):
    if not remoteCmd:
        process = Process()
    else:
        process = RemoteProcess()
    output, error, code = process.run(cmd, 1)
    if printDetail:
        if len(output):
            print 'output: ', output
        if len(error):
            print 'error: ', error
    return output, error, code

class RemoteProcess(object):
    def __init__(self):
        self.ssh_client = self._get_ssh_client()

    def __del__(self):
        self.ssh_client.close()
    '''
    def _get_ssh_client(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect($ssh_ip,$ssh_port,$ssh_user,$ssh_pwd)
        return ssh_client
    '''
    def run(self, cmd, retryTimes=5):
        for i in range(retryTimes):
            stdout, stderr, returnCode = self.runOnce(cmd)
            if returnCode != 0:
                print '[ERROR]. run cmd [%s] failed! retry %s...' % ( cmd, i + 1)
                time.sleep(1)
            else:
                return stdout, stderr, returnCode
        return stdout, stderr, returnCode

    def runOnce(self, cmd):
        stdin,stdout,stderr = self.ssh_client.exec_command(cmd)
        stdout = stdout.read().strip()
        stderr = stderr.read().strip()
        if stderr:
            return stdout, stderr, 1
        else:
            return stdout, stderr, 0

class Process(object):
    def run(self, cmd, retryTimes=5):
        for i in range(retryTimes):
            stdout, stderr, returnCode = self.runOnce(cmd)
            if returnCode != 0:
                print '[ERROR]. run cmd [%s] failed! retry %s...' % ( cmd, i + 1)
                time.sleep(1)
            else:
                return stdout, stderr, returnCode
        return stdout, stderr, returnCode

    def runOnce(self, cmd):
        stdoutFile = tempfile.NamedTemporaryFile()
        stderrFile = tempfile.NamedTemporaryFile()
        cmd = '%(cmd)s 1>>%(out)s 2>>%(err)s' %\
            {'cmd': cmd,\
                 'out': stdoutFile.name,\
                 'err': stderrFile.name}
        returnCode = os.system(cmd)
        # the returnCode of os.system() is encoded by the wait(),
        # it is a 16-bit number, the higher byte is the exit code of the cmd
        # and the lower byte is the signal number to kill the process
        stdout = stdoutFile.read()
        stderr = stderrFile.read()
        stdoutFile.close()
        stderrFile.close()
        return stdout, stderr, returnCode

    def runInBackground(self, cmd, outFileName, errFildName):
        cmd = '%(cmd)s 1>%(out)s 2>%(err)s &' % {
            'cmd': cmd,
            'out': outFileName,
            'err': errFildName
            }
        returnCode = os.system(cmd)
        return returnCode

    def runinConsole(self, cmd):
        cmd = '%(cmd)s 1>>%(out)s 2>>%(err)s' %\
            {'cmd': cmd,\
                 'out': '/dev/null',\
                 'err': '/dev/null'}
        returnCode = os.system(cmd)

if __name__ == '__main__':
    pass
