#!/usr/bin/env python
#-*-coding:utf8-*-
#!/bin/bash

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Notice
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 출력 시 문자열 정렬하는 방법 (% 다음의 '#'은 숫자)
# %#d, %#s : '#'크기만큼 오른쪽 정렬
# %-#d, %-#s : '#'크기만큼 왼쪽 정렬
# %+#d, %+#f : 숫자 앞에 부호 출력
# %0#d, %0#f : 숫자 앞에 빈공간 '0' 출력

# False : 0, "", None
# True  : any number except 0 ( *~ < 0 < ~* )

# args : 여러 개를 가리킬 경우 (ex) *args
# argv : 하나의 값을 가리킬 경우 (ex) argv[0]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <1> Header
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Common
import os
path_NextLib_cmn_py = os.path.dirname(os.path.abspath(__file__))

# System
import sys, pexpect, subprocess, threading
import time
import fnmatch, glob, pickle
import shutil
import copy
from collections import OrderedDict

from datetime import datetime

# Path
homePath    = os.path.expanduser("~")
NEXTPath    = homePath + "/.NEXTfoam"
libPath     = path_NextLib_cmn_py
iconPath    = libPath + "/Resources/Icons"
picPath     = libPath + "/Resources/Pictures"

# Python
pyVer       = sys.version_info

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <2> Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOG_CLASS (v1.0)
class LOG_CLASS:
    def __init__(self, path="./"):  # 시작위치만 지정해주면 하위폴더에 로그파일이 저장됨
        self.path = path
        self.max_write = 256
        self.data = []
        return

    def New(self):
        if len(self.data) == 0:
            self.data = [">>> Start >>>\n"]
        else:
            for ii in range(len(self.data)):
                del self.data[-1]
            self.data = [">>> Start >>>\n"]
        return self.data

    def Add(self, newData=""):
        # Check
        if len(self.data) >= self.max_write:
            self.data[1] = "--- deleted ---\n"
            del self.data[2]

        # Save
        self.data.append(newData)
        return

    def End(self):
        self.data.append('\n<<< End <<<')
        # Save
        os.system("mkdir -p %s/Log" % self.path)
        logFile_Name = ("%s/Log/%s.log" % (self.path, Get_CurTime()))
        try:
            with open(logFile_Name, "w") as logFile:
                logFile.writelines("\n".join(self.data))
        except IOError:
            print("[Error] LOG_CLASS::End() >> Cannot save log file, %s" % self.path)
            return

        return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <3> Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ------------------------------------------------------------------------------
# C-type Function
# ------------------------------------------------------------------------------
# T_ (v1.0)
def T_(text, *argv):    # 한글 출력 가능한지 확인 필요
    if not isinstance(text, str):
        return
    text = text % argv
    return str(text)

# Print (v1.0)
def Print(text, *argv):
    if not isinstance(text, str):
        return
    text = text % argv
    print(text)
    return

# ------------------------------------------------------------------------------
# Show Variable
# ------------------------------------------------------------------------------
def SHOW_VALUE(*data):
    print("# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #")
    if isinstance(data, list):
        for dd in data:
            print(dd)
    else:
        print(data)
    return

# ------------------------------------------------------------------------------
# Check Variable
# ------------------------------------------------------------------------------
# Check_BOOL (v1.0)
def Check_BOOL(data):
    if data:
        print("True")
    else:
        print("False")
    return

# IsBool (v1.0)
def IsBool(data):
    if type(data) == bool:
        return True
    return False

# IsNum (v1.0)
def IsNum(strData):
    if strData.isdigit():
        return True
    return False

# GetNum (v1.0)
def GetNum(strData):
    if IsNum(strData):
        return int(strData)
    return None

# IsEmpty (v1.0)
def IsEmpty(data):
    if not data:    # if data == "":
        return True
    return False


# ------------------------------------------------------------------------------
# Connect Function
# ------------------------------------------------------------------------------
# Get_Func_argv (v1.0)
def Get_Func_argv(func, *args):
    newFunc = func
    if len(args) > 0:
        newFunc = lambda: func(*args)
    return newFunc


# Get_Func_widget_argv (v1.0)
def Get_Func_widget_argv(widget, func, *args):
    newFunc = func
    if len(args) > 0:
        newFunc = lambda: func(widget, *args)
    return newFunc

# ------------------------------------------------------------------------------
# File
# ------------------------------------------------------------------------------
# IsFile (v1.0)
def IsFile(path=""):
    if not path:
        return False
    if os.path.isfile("%s" % path):
        return True
    # if os.path.exists(path): return True       # 아무 함수를 써도 됨
    return False

# IsLink (v1.0)
def IsLink(fileFullname=''):
    if os.path.islink(fileFullname): return True
    return False

# Check_FileExt (v1.0)
def Check_FileExt(extName, *checkNames):
    for dd in checkNames:
        if dd == extName:
            return True
    return False

# Get_FileList (v1.0)
def Get_FileList(path=''):  # 정규식 사용 가능, 경로가 없으면 [] 반환
    if not IsDir(path):
        return []
    #
    arrName = glob.glob(path)
    return arrName

# Find_Files (v1.1)
def Find_Files(startPath=".", option="*", bPath=True, bView=False, bSort=True):
    arrFoundFiles = []
    startPath = startPath.replace("\"", "")
    for fullPath, subPath, fileNames in os.walk(startPath):
        for ff in fnmatch.filter(fileNames, option):
            if bPath:
                ff = os.path.join(fullPath, ff)
            #
            arrFoundFiles.append(ff)
            # Input
            if bView:
                print(ff)
    # Sort
    if bSort:
        arrFoundFiles.sort()
    return arrFoundFiles

# Find_All (v1.2)
def Find_All(startPath=".", option="*", bPath=True, bView=False, bSort=True):
    arrFoundAll = []
    startPath = startPath.replace("\"", "")
    for fullPath, subPath, fileNames in os.walk(startPath):
        # if Dir
        if fullPath != startPath:
            arrFoundAll.append(fullPath)

        # if File
        for ff in fnmatch.filter(fileNames, option):
            if bPath:
                ff = os.path.join(fullPath, ff)
            #
            arrFoundAll.append(ff)
            # Input
            if bView:
                print(ff)
    # Sort
    if bSort:
        arrFoundAll.sort()
    return arrFoundAll

# ------------------------------------------------------------------------------
# File (Path/Name/Ext)
# ------------------------------------------------------------------------------
def Get_FilePath(path):      # Path/Name.ext    >> Path
    if not os.path.isfile(str(path)):
        print('#Error >> Get_FilePath() : Cannot find path[ %s ]'% path)
        return False
    if isinstance(path, list):
        print('#Error >> Get_FilePath() : The input path is list [%s]' % path)
        return False
    #
    splitData = os.path.split(str(path))
    return splitData[0]

def Get_FileNameExt(path):  # Path/Name.ext    >> Name.ext
    if not os.path.isfile(path):
        print('[Error:Get_FileNameExt] Cannot find file [%s]' % path)
        return False
    if isinstance(path, list):
        print('[Error:Get_FileNameExt] The input path is list [%s]' % path)
        return False
    split_Data = os.path.split(str(path))
    return split_Data[1]

def Get_FileName(path):      # Path/Name.ext    >> Name
    if not os.path.isfile(path):
        #print('Error>> Get_FileName() : cannot open file, %s' % path)
        return False
    if isinstance(path, list):
        #print('#Error >> Get_FileExt() : The input path is list [%s]' % path)
        return False
    #
    split_Data = os.path.split(path)
    Ext = "." + Get_FileExt(str(path))
    #
    if not Get_FileExt(path):
        return split_Data[1]
    else:
        str_FileName = split_Data[1].replace(Ext, '')
        return str_FileName

def Get_FileExt(path):  # Path/Name.ext    >> ext (lower)
    if not os.path.isfile(str(path)) :
        #print('#Error >> Get_FileExt() : Cannot find file[ %s ]'% path)
        return False
    if isinstance(path, list):
        #print('#Error >> Get_FileExt() : The input path is list [%s]' % path)
        return False
    #
    split_Data = os.path.splitext(str(path))
    extName = split_Data[1]
    extName = extName.replace(".", "")
    return extName.lower()

def Get_ParentPathName(path):         # Parent/Path   >> Parent
    path = str(path)
    index = path.rfind("/")
    resultPath = path[:index]
    return resultPath

def Get_PathName(filePathName):  # Parent/Path   >> Path
    path = str(filePathName)
    index = path.rfind("/")
    resultPath = path[index + 1:]
    return resultPath


# ------------------------------------------------------------------------------
# File (Read/Write)
# ------------------------------------------------------------------------------
# Read_File (v2.0)
def Read_File(path):
    readData = ""
    if os.path.isfile(path):
        with open(path, "r") as File:
            readData = File.read()
    return readData

# Read_File (v2.0)
def Read_File_LineData(path):
    # Init
    readData = []

    # Read
    if os.path.isfile(path):
        with open(path, "r") as File:
            readData = File.readlines()
    return readData

# Get_LinesData_inFile (v1.2)
def Get_InfoFile(path, pos_Start=0, pos_End=-1, iOpt=-1, bOpt2=True, bRemove=True):
    resultData = Get_LinesData_inFile(path, pos_Start, pos_End, iOpt, bOpt2, bRemove)
    return resultData

# Get_LinesData_inFile (v1.2)
def Get_LinesData_inFile(path, pos_Start=0, pos_End=-1, iOpt=-1, bOpt2=True, bRemove=False):
    # Read file
    readData = Read_File(path)

    # Remove comment, empty, etc...
    readData = Remove_Comment(readData, 0)
    readData = Remove_Empty(readData, bRemove=bRemove)
    splitData = readData.split("\n")

    # Extract only pure data
    realData = []
    for dd in splitData:
        if dd:
            realData.append(dd)
    #
    resultData = []
    if len(realData) > 0 and pos_Start >= 0:
        if pos_End == -1:
            pos_End = len(realData)
        for ii in range(pos_Start, pos_End):
            if ii < len(realData):
                resultData.append(realData[ii])
    # Additional Option
    if iOpt >= 0:
        totalGroupData = []
        groupData = []
        for dd in resultData:
            if dd.find("-") == 0:
                if len(groupData) > 0:
                    totalGroupData.append(groupData)
                groupData = []
            else:
                groupData.append(dd)
        #
        totalGroupData.append(groupData)
        if iOpt < len(totalGroupData):
            tmpData = totalGroupData[iOpt]
            selectedData = []

            for dd in tmpData:
                dd = dd.split(" ")
                selectedData.append(dd)
            resultData = selectedData
            if bOpt2:   # 앞에 항목만 가지고 옴
                return Extract_First_Data(resultData)
        else:
            return []
    return resultData

def Extract_First_Data(arrData=[]):  # Get_LinesData_inFile의 추가기능 함수
    extractData = []
    for dd in arrData:
        extractData.append(dd[0])
    return extractData

# Write_File (v2.0)
def Write_File(path, data):
    try:
        with open(path, "w") as File:
            File.write(data)
        return True
    except:
        return False

# ------------------------------------------------------------------------------
# Dir
# ------------------------------------------------------------------------------
# IsDir (v1.0)
def IsDir(path=""):
    if not path:
        return False
    if os.path.isdir(path):
        return True
    return False

# IsDirEmpty (v1.0)
def IsDirEmpty(path=""):
    if IsDir(path):
        print("1")
        if Find_Files(path) == 0:
            print("2")
            return True
        print("3")
    print("4")
    return True

# IsMount (v1.0)
def IsMount(path):
    if os.path.ismount(str(path)):
        return True
    return False

# Find Dirs (v1.1)
def Find_Dirs(startPath=".", option="*", bPath=True, bView=False, bSort=True):
    arrFoundDirs = []
    startPath = startPath.replace("\"", "")
    for fullPath, subPath, fileNames in os.walk(startPath):
        for ff in fnmatch.filter(subPath, option):
            if bPath:
                ff = os.path.join(fullPath, ff)
            arrFoundDirs.append(ff)
            # Input
            if bView:
                print(ff)
    # Sort
    if bSort: arrFoundDirs.sort()
    return arrFoundDirs


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Ordered Dictionary
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# NOTICE
# Python3.6 이상에서는 일단 Dict도 순서대로 들어감, 그 이하 버전은 순서대로 들어가지 않음
# Python 3.6 미만에서는 아래와 같이 사용
# OrderedDict([
#   ("one", 1), ("two", 2), ("three", 3), ("four", 4), ("five", 5)
#   ])
# Python 3.6 이상에서는 아래와 같이 아무렇게나 사용가능
# OrderedDict([
#   "one": 1, "two": 2, "three": 3, "four": 4, "five": 5
#   ])
def New_Dict(data, value):
    newDict = OrderedDict({data : value})
    return newDict

def Find_Dict_Data(dictData={}, value=""):
    for key in dictData.keys():
        if key == value:
            return True
    return False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# List
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def New_List(*data):                        # (ex) New_List(,,,)
    array = []
    for ii, dd in enumerate(data):
        array.append(dd)
    return array

def IsList(arrData):
    if isinstance(arrData, list):
        return True
    return False

def Add_List(arrData, data):                # Add_List([a,b], [c,d]) >> [a,b,[c,d]]
    arrData.append(data)
    return arrData

def Insert_List(arrData, data, pos=0):      # Combine_List([a,b], [c,d]) >> [a,b,c,d]
    if not IsList(data): data = [data]
    arrData.insert(pos, data)
    return arrData

def Combine_List(arrData, data, pos=0):     # (ex) Insert_List([,,], 3, [,,])
    if not IsList(data): data = [data]
    for ii, dd in enumerate(data):
        arrData.insert(pos+ii, dd)  # pos 크기가 배열크키보다 크면 맨 뒤에 추가됨
    return arrData

def Replace_List(arrData, data, i):
    arrData[i] = data
    return

def Del_List_Data(arrData, data=''):
    arrData.remove(data)    # 동일한 항목을 삭제함
    return arrData

def Del_List_Index(arrData, i=-1):
    if i >= 0 :                # 인덱스를 삭제함
        del arrData[i]
    return

def Copy_List(arrData):
    arrNewData = list(arrData)
    return arrNewData

# def Clear_List(arrData):  # 굳이 할 필요가 없음
#     arrData = []
#     del arrData
#     return arrData

def Sort_List(arrData, reverse=True):
    arrData.sort()
    if reverse:
        arrData.reverse()
    return

def Reverse_List(arrData):
    arrData.reverse()
    return

def Merge_List(arrData, spaceData):         # (ex) Merge_List( [,,], ',')
    strData = ''
    count = len(arrData) - 1
    for ii, dd in enumerate(arrData):
        if ii >= count: spaceData = ''
        strData += (str(dd) + str(spaceData))
    return strData

def Check_List(arrData, data):
    if data in arrData:
        return True
    return False

def FindString_List(arrData, data):
    for ii, dd in enumerate(arrData):
        if dd == data:
            return ii
    return -1

def FindString_List_Adv(arrData, data, column=0, bOpt=False):
    # bOpt: False, 리스트 안 실제 갯수가 2개 이상이라면 제일 처음 발견된 하나만 출력
    result = []
    for ii, dd in enumerate(arrData):
        if dd[column] == data:
            if not bOpt: return ii
            else: result.append(ii)
    if len(result) == 0: return -1
    return result


# ------------------------------------------------------------------------------
# Pickle
# ------------------------------------------------------------------------------
# Load_Pickle (v1.2)
def Load_Pickle(fileName, bOpt=True):  # bOpt: T-전체로 읽기, F-개별적으로 읽기
    data = None
    with open(fileName, "rb") as pkFile:
        data = False
        if bOpt:
            data = pickle.load(pkFile)
        else:
            # Header
            version = pickle.load(pkFile)
            num = pickle.load(pkFile)
            # Data
            for ii in range(0, num):
                data.append(pickle.load(pkFile))
    return data

# Save_Pickle (v1.2)
def Save_Pickle(fileName, data, bOpt=True):  # bOpt: T-전체로 저장, F-개별적으로 저장
    if bOpt:
        with open(fileName, "wb") as pkFile:
            pickle.dump(data, pkFile, protocol=0)
    else:
        if isinstance(data, list):
            data = data[0]
        with open(fileName, "wb") as pkFile:
            # Header
            pickle.dump(1.0, pkFile, protocol=0)        # version
            pickle.dump(len(data), pkFile, protocol=0)  # num
            # Data
            for dd in data:
                pickle.dump(dd, pkFile, protocol=0)
    return

# ------------------------------------------------------------------------------
# Internet
# ------------------------------------------------------------------------------
# Open Website (v1.0)
def Open_Website(address):
    import webbrowser
    if address.find('http://', 0) == -1 or address.find('https://', 0) == -1:
        address = 'https://' + address
    webbrowser.open_new(address)
    return

# ------------------------------------------------------------------------------
# Time/Date
# ------------------------------------------------------------------------------
# Delay (v1.0)
def Delay(sec):
    time.sleep(sec)
    return

# Get_CurTime (v1.0)
def Get_CurTime():
    now = datetime.now()
    curTime = "%4d%02d%02d-%02d%02d%02d" \
              % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    return curTime

# ------------------------------------------------------------------------------
# Process
# ------------------------------------------------------------------------------
# Execute (v1.0)
def Execute(cmd=""):
    os.system(cmd)
    return

# Execute1 (v1.11)
def Execute1(cmd=""):  # cmd는 배열로 여러 개 입력 가능, 실행 완료 할 때 까지 기다리는 함수
    # Check
    if not isinstance(cmd, list) and not isinstance(cmd, tuple):
        cmd = [cmd]
    # Run
    for dd in cmd:
        pexpect.run(dd)  # os.system()과 동일    >> 시간 지나면 종료되는 문제 해결해야함
    return

# Execute2 (v1.0)
def Execute2(cmd=""):   # 명령어를 실행하지만 다른 쉘과 통신할 수 없음
    # Check
    if not isinstance(cmd, list) and not isinstance(cmd, tuple):
        cmd = [cmd]
    # Run
    for dd in cmd:
        output = subprocess.Popen(["/bin/bash", "-c", dd], shell=True)
        # subprocess.run(["/bin/bash", "-c", dd], shell=True)  # Popen의 간소화 함수 (Python 3.5이상)
        output.terminate()  # 죽이지 않으면 좀비프로세서로 계속 남음
    return

# ------------------------------------------------------------------------------
# Find String
# ------------------------------------------------------------------------------
# Find_String (v1.2)
def Find_String(sourceData="", findString="", startPos=0, endPos=-1, endChar=[], bReverse=False):
    # Init
    found_Pos = -1
    search_Pos = -1

    total_Pos = len(sourceData)
    stringSize = len(findString)

    # Run
    while search_Pos < total_Pos and found_Pos < 0:
        # Find
        if not bReverse:
            search_Pos = sourceData.find(findString, startPos, endPos)
        else:
            search_Pos = sourceData.rfind(findString, startPos, endPos)

        # Find Result
        if search_Pos == -1:
            return -1
        # Check
        if len(endChar) == 0:
            bCheckWord = True
            found_Pos = search_Pos
        else:
            checkPos = search_Pos + stringSize
            if checkPos >= total_Pos:
                bCheckWord = True
                found_Pos = search_Pos
            else:
                bCheckWord = False
                for dd in endChar:
                    if dd == sourceData[checkPos]:
                        bCheckWord = True
                        found_Pos = search_Pos
                        break
        # Next
        if not bCheckWord:
            startPos = search_Pos + 1

    # Result
    # print("Find_String: %d" %found_Pos)
    return found_Pos

# Find_Nearby_String (v1.3)
def Find_Nearby_String(sourceData="", findString="", startPos=0, endPos=-1, bReverse=False):
    # Init
    total_Pos = len(sourceData)

    # Check
    startPos = max(0, startPos)
    if endPos < 0:
        endPos = total_Pos
    else:
        if endPos >= total_Pos:
            endPos = total_Pos
    total_Pos = len(sourceData[startPos:endPos])

    # Find
    if not bReverse:
        found_Pos = sourceData[startPos:endPos].find(findString, 0)
    else:
        found_Pos = sourceData[startPos:endPos].rfind(findString, 0)
        if found_Pos == -1:
            found_Pos = False
        elif found_Pos >= 0:
            found_Pos = -(total_Pos - found_Pos)
    #
    #print("found_Pos: %d (%d:%d)[%d]" % (found_Pos, startPos, endPos, total_Pos))
    return found_Pos

# Find_BracesSet (v1.1)
def Find_BracesSet(sourceData="", startPos=0):
    # Init
    firstPos = startPos
    lastPos = startPos
    curPos = startPos

    bCheck = False
    count = 0

    # Check
    if len(sourceData) < 2:
        return -1, -1

    if curPos == -1 or curPos >= len(sourceData):
        return -1, -1

    # Find
    while not bCheck:
        if count == 0 and sourceData[curPos] == ";":
            return -1, -1

        if sourceData[curPos] == "{":
            if count == 0:
                firstPos = curPos
            count += 1

        elif sourceData[curPos] == "}":
            count -= 1
            if count == 0:
                lastPos = curPos + 1
                bCheck = True
        # Next
        curPos += 1

    # Check
    if firstPos >= lastPos:
        lastPos = firstPos

    # End
    return firstPos, lastPos

# Find_Indent (v1.0)
def Find_Indent(sourceData="", curPos=0):
    pos = Find_Nearby_String(sourceData, "\n", 0, curPos, True)
    if not pos:
        pos = curPos
    else:
        pos = -(pos+1)
    return pos

# ------------------------------------------------------------------------------
# Insert String
# ------------------------------------------------------------------------------
# Insert_String_byPos (v2.0)
def Insert_String_byPos(data, startPos=0, insertStr=""):
    # Init
    allData = data
    lastPos = len(allData)

    # Replace string by position
    changeAllData = data[0:startPos]
    for ee in insertStr:
        changeAllData += ee

    # Insert
    changeAllData += data[startPos:lastPos]
    #
    return changeAllData

# ------------------------------------------------------------------------------
# Replace String
# ------------------------------------------------------------------------------
# Replace_String_byPos (v2.1)
def Replace_String_byPos(data, startPos=0, endPos=0, newStr="", bStay=False):  # bType: 위치 유지 여부
    # Check
    if not data:
        return data

    # Init
    allData = data
    lastPos = len(allData)

    # Replace string by position
    changeAllData = data[0:startPos]
    for ee in newStr:
        changeAllData += ee
        startPos += 1
    # Stay
    if bStay:
        for ii in range(startPos, endPos):
            changeAllData += " "
    changeAllData += data[endPos:lastPos]
    #
    return changeAllData

# Replace_String (v1.1)
def Replace_String(data, orgStr="", newStr="", count=0):  # 0:All, 1~: times(1 is once)
    # Check
    if not data:
        return data

    # Init
    allData = data
    lastPos = len(allData)
    lenStr = len(orgStr)

    # Find org string
    pos = 0
    replaceData = ""
    pos_Start = allData.find(orgStr)
    while pos < lastPos:
        if pos == pos_Start:
            # Replace to new string
            for ee in newStr:
                replaceData += ee
            pos += lenStr

            # Check and Next
            count -= 1
            if count == 0:
                pos_Start = -1
            else:
                pos_Start = allData.find(orgStr, pos)
        else:
            replaceData += allData[pos]
            pos += 1
    # End
    return replaceData

# ------------------------------------------------------------------------------
# Remove String
# ------------------------------------------------------------------------------
# Remove_Empty (v1.2)
# 모든 공백(" "), 탭문자("\t")를 한 칸의 공백으로 변경 (추가 옵션: 원하는 문자 추가 가능, bRemove: 한칸의 공백이 아닌 아예 제거)
def Remove_Empty(data, addOpt="", bRemove=False):
    # Check
    if not data:
        return data

    allData = data
    changeData = ""

    pos = 0
    lastPos = len(allData)
    dd_prev = " "
    while pos < lastPos:
        dd = allData[pos]

        # Check
        if dd == " " or dd == "\t" or dd == addOpt:
            if dd_prev != " " and dd_prev != "\t" and dd_prev != addOpt:
                if not bRemove:
                    changeData += " "
        else:
            changeData += dd

        # Next
        dd_prev = dd
        pos += 1

    # End
    return changeData


# Remove_Comment (v1.1)
def Remove_Comment(data, iType=3, bStay=False):  # iType - 0: 모든 주석 제거, bStay- 주석 제거된 위치 유지 여부
    # Check
    if not data:
        return data

    # Init
    allData = data
    lastPos = len(allData)

    # Delete
    if iType == 0 or (iType & 1) == 1:  # (/* ... */) 제거
        pos_Start = allData.find("/*")
        while pos_Start != -1:
            pos_End = allData.find("*/", pos_Start + 1)
            if pos_End == -1:
                pos_End = lastPos
            # Delete
            allData = Replace_String_byPos(allData, pos_Start, pos_End + 2, "", bStay)
            pos_Start = allData.find("/*", pos_Start)

    if iType == 0 or (iType & 2) == 2:  # 주석(//) 제거
        pos_Start = allData.find("//")
        while pos_Start != -1:
            pos_End = allData.find("\n", pos_Start + 1)
            if pos_End == -1:
                pos_End = lastPos
            # Delete
            allData = Replace_String_byPos(allData, pos_Start, pos_End, "", bStay)
            pos_Start = allData.find("//", pos_Start)

    if iType == 0 or (iType & 4) == 4:  # 주석(#) 제거
        pos_Start = allData.find("#")
        while pos_Start != -1:
            pos_End = allData.find("\n", pos_Start + 1)
            if pos_End == -1:
                pos_End = lastPos
            # Delete
            allData = Replace_String_byPos(allData, pos_Start, pos_End, "", bStay)
            pos_Start = allData.find("#", pos_Start)
    # End
    return allData

# ------------------------------------------------------------------------------
# Thread
# ------------------------------------------------------------------------------
# Run_Thread (v1.0)
# Notice : 쓰레드 변수는 self 와 같이 사용하여 로컬 함수 밖에서 소멸되지않도록 해야함
def Run_Thread(func=None, *args):
    if func is None: return
    thread = threading.Thread(target=func, args=args)
    # thread = multiprocessing.Process(target=func, args=args)
    thread.daemon = True
    thread.start()
    # thread.join() # 다른 Thread 함수가 끝날때까지 기다림(멀티쓰레드 제외하고 사용금지)
    return thread


# Get_Thread_Lock (v1.0)
def Get_Thread_Lock():
    return threading.Lock()


# Start_Thread_Lock (v1.0)
def Start_Thread_Lock(lock):
    lock.acquire()
    return


# End_Thread_Lock (v1.0)
def End_Thread_Lock(lock):
    lock.release()
    return

# ------------------------------------------------------------------------------
# Only for GUI
# ------------------------------------------------------------------------------
# Get_TempCasePath (v1.0)
def Get_TempCasePath(path=".", tempName="NoNamed"):
    # Set defaults
    num = 1
    name = tempName
    newTempPath = path + '/' + tempName

    # Check
    while IsDir(newTempPath):
        name = tempName + "%d" % num
        newTempPath = path + '/' + name
        num += 1
    return newTempPath

# Del_TempCasePath (v1.0)
def Del_TempCasePath(path=".", tempName="NoNamed"):
    delPath = "%s" % path
    if delPath.find(tempName) >= 0:
        os.system(T_("rm -rf '%s'", delPath))
    return

# Check_TempCasePath (v1.0)
def Check_TempCasePath(path=".", tempName="NoNamed"):
    checkPath = "%s" % path
    if checkPath.find(tempName) >= 0:
        return True
    return False

# ------------------------------------------------------------------------------
# Convert Value
# ------------------------------------------------------------------------------
def Convert_YesNo_Load(value):
    if value == "yes":
        result = "Yes"
    elif value == "no":
        result = "No"
    else:
        result = "No"
    return str(result)

def Convert_YesNo_Save(value):
    if value == "Yes":
        result = "yes"
    elif value == "No":
        result = "no"
    else:
        result = "no"
    return str(result)

# --------------------------------------------------------------------------
def Convert_OnOff_Load(value):
    if value == "on":
        result = "On"
    elif value == "off":
        result = "Off"
    else:
        result = "Off"
    return str(result)

def Convert_OnOff_Save(value):
    if value == "On":
        result = "on"
    elif value == "Off":
        result = "off"
    else:
        result = "off"
    return str(result)

# --------------------------------------------------------------------------
def Convert_TrueFalse_Load(value):
    if value == "true":
        result = "True"
    elif value == "false":
        result = "False"
    else:
        result = "False"
    return str(result)

def Convert_TrueFalse_Save(value):
    if value == "True":
        result = "true"
    elif value == "False":
        result = "false"
    else:
        result = "false"
    return str(result)

# def Convert_Value(value, opt=""):   # opt: YN, TF, OnOff, 01
#     result = ""
#     if isinstance(value, str):
#         value = value.lower()
#         if value == "false" or value == "no" or value == "off" or value == "0":
#             result = 0
#         elif value == "true" or value == "yes" or value == "on" or value == "1":
#             result = 1
#
#     elif isinstance(value, int):
#         if value == 0:
#             if opt == "YN": result = "no"
#             elif opt == "TF": result = "false"
#             elif opt == "01": result = "0"
#
#         if value == 1:
#             if opt == "YN": result = "yes"
#             elif opt == "TF": result = "true"
#             elif opt == "01": result = "1"
#     #
#     return result

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <5> Run
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Default run
if not IsDir(NEXTPath):
    Execute("mkdir -p %s" % NEXTPath)

# Run Test
if __name__ == '__main__':
    # Test here
    Find_All()
    # Get_LinesData_inFile("/home/test/Work/Project/MOBIS/1.GUI/Install_Moca-v2/MOCAFoam-v2.2/Setting/Info/solidInfo", bOpt=1)
    print("OK")
    # pass
