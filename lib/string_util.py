#!/usr/ali/bin/python

import os, sys

def AddLastSlash(string):
    '''
    ensure the returned dirpath is endswith "/"
    '''
    if not string.endswith('/'):
        string = string + '/'
    return string

def RemoveLastSlash(string):
    if string.endswith('/'):
        string = string[:-1]
    return string

def RemoveLastComma(string):
    if string.endswith(','):
        string = string[:-1]
    return string

def IsEndWithSlash(string):
    if string.endswith('/'):
        return True
    return False

def AddEscapeCharacter(string):
    '''
    add escape character for string, including \, "
    example:
      before call this function: select * from "path1";
      call this function 1 time: select * from \"path1\";
      call this function  twice: select * from \\\"path1\\\";
    '''
    string = string.replace("\\", "\\\\")
    string = string.replace("\"", "\\\"")
    string = string.replace("\'", "\\\'")
    return string

def SplitLines(content, itemsplit, linesplit):
    _linelist = content.split(linesplit)
    linelist = list()
    for line in _linelist:
        if line.isspace() or line == "":
            continue
        items = line.split(itemsplit)
        linelist.append(items)
    return linelist

