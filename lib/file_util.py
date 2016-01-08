#!/usr/ali/bin/python

import os, sys, shutil
import string_util as StringUtil
import no_block_process

# operations for local file/dir
def ListFile(dirname):
    dirname = StringUtil.AddLastSlash(dirname)
    _filelist = os.listdir(dirname)
    _filelist.sort()

    filelist = list()
    for filename in _filelist:
        fullname = dirname + filename
        if IsFile(fullname):
            filelist.append(filename)
    return filelist

def ListFileByFullName(dirname):
    dirname = StringUtil.AddLastSlash(dirname)
    _filelist = ListFile(dirname)
    filelist = [dirname + filename for filename in _filelist]
    return filelist

def ListSubDir(dirname):
    dirname = StringUtil.AddLastSlash(dirname)
    _filelist = os.listdir(dirname)
    _filelist.sort()

    filelist = list()
    for filename in _filelist:
        fullname = dirname + filename
        if IsDir(fullname):
            filelist.append(fullname)
    return filelist

def IsDir(dirname):
    return os.path.isdir(dirname)

def IsFile(filename):
    return os.path.isfile(filename)

def MakeDirs(dirpath):
    return os.makedirs(dirpath)
def MakeDirs_f(dirpath):
    try:
        os.makedirs(dirpath)
    except OSError,e:
        if str(e).find('File exists') == -1:
            raise
    finally:
        pass

def Delete(path_or_file):
    rmcmd = "rm -rf %s" % path_or_file
    output, error, code = no_block_process.ExecuteCmd(rmcmd)
    pass

def Exists(path_or_dir):
    return os.path.exists(path_or_dir)

def GetDirpath(filename):
    return os.path.dirname(filename)

def Copy(srcFile, dstFile):
    shutil.copy(srcFile, dstFile)
    pass
def CopyDir(srcDir, dstDir):
    shutil.copytree(srcDir, dstDir)

def Move(srcFile, dstFile):
    shutil.move(srcFile, dstFile)
    pass
