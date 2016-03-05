#!/usr/bin/python
import sys
from arachne import *
import re
STATUS    = 0x1
ERROR     = 0x2
FATAL     = 0x4
DEBUG     = 0x8
NO_FORMAT = 0x10

WEB_ROOT="/var/www/"
def shell_exec(command,In=None,Block=True,**kargs):
    import subprocess as sp
    if not Block:
        p = sp.Popen(command.split(" "))
        return None
    else:
        p = sp.Popen(command.split(" "),stdout=sp.PIPE,stdin=sp.PIPE)
        return p.communicate(In)[0]

def _ident(x,**kargs):
    return x

def FindFiles(currentpath,**kargs):
    import os
    sort_alg=kargs.pop('key') if 'key' in kargs else _ident
    currentpath = os.path.abspath(currentpath)
    DirSep = "/" if 'DirSep' not in kargs else kargs['DirSep']
    currentpath,MatchString=DirSep.join(currentpath.split(DirSep)[:-1]),currentpath.split(DirSep)[-1]
    MatchRgx=re.compile(MatchString)
    MatchList = []
    Recursive = True if 'Recursive' in kargs else False
    def SimpleFind(currentpath,MatchString):
        for File in os.listdir(currentpath):
            if MatchRgx.match(File) is not None:
                MatchList.append(currentpath+DirSep+File)
        return MatchList
        
    def RecurFind(currentpath,previouspath,MatchString):
        for File in os.listdir(currentpath):
            nextpath = currentpath+DirSep+File
            if (os.path.isdir(nextpath)):
                RecurFind(nextpath,currentpath,MatchString)
            elif MatchRgx.match(File) is not None:
                MatchList.append(currentpath+DirSep+File)        

        try:
            os.chdir(previouspath)
        except:
            return MatchList
        
    if (Recursive is False):
        L=SimpleFind(currentpath,MatchString)
        return sorted(L,key=sort_alg)
    else:
        return sorted(RecurFind(currentpath,'',MatchString),key=sort_alg)


def SetContent(parentNode,content,**kargs):
    return([content])

def ImportData(parent,**kargs):
    parent.name = parent.content.split('/').pop() # record the non-normalized filename
    Mode="rb" if "Unicode" not in kargs else "r"
    try:
        with open(parent.content,"rb") as f:
            return [f.read()]
    except:
        Update(ERROR,"could not open %s",parent.content)

def FindRegex(parent,*args,**kargs):
    import re

    regex = args[0] if 'rgx' not in kargs else kargs['rgx']
    rgx = re.compile(bytes(regex,encoding="utf-8"),re.DOTALL|re.MULTILINE) if type(parent.content) is bytes else re.compile(regex,re.DOTALL|re.MULTILINE)
    return rgx.findall(parent.content)


File=Creator(SetContent,Name="File")
Data=Creator(ImportData,Name="Data")

def populate_data(Parent,Target,**kargs):
    """
    Populate Data from Target into Node:
    """
    D=[f.newchildren(Data,**kargs) for f in [Parent.newchildren(File,h) for h in FindFiles(Target,**kargs)]]

    ReturnList=False if 'ReturnList' not in kargs else kargs.pop('ReturnList')
    if 'ReturnList' not in kargs and len(D) == 1:
        return D[0]
    elif len(D) >= 1:
        return NodeList(D)
    elif ReturnList:
        return []
    else:
        return False

