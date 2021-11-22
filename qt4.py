#!/usr/bin/env python
# -*-coding:utf8-*-
# !/bin/bash

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Notice
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <1> Header
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Common
import os, sys
path_NextLib_QT4_cmn_py = os.path.dirname(os.path.abspath(__file__))

path_NextLib = os.path.abspath(path_NextLib_QT4_cmn_py + "/../..")
sys.path.append(path_NextLib)

# NextLib Module
from NextLib.cmn import *

# Qt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *

# Qt4 (Variables)
# ONLY_INT = QIntValidator()
# ONLY_NUM = QRegExpValidator(QRegExp("[-+]?[0-9]*[.][0-9]*[eEdD][-+][0-9]*"))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <2> Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# QT4 Run Class (되는 시스템이 있고 안되는 시스템이 있어서 현재는 사용보류)
# class QT4_CLASS(QApplication):
#     def __init__(self):
#         QApplication.__init__(self, sys.argv)
#         # Common
#         self.path = path_NextLib_QT4_cmn_py
#         self.thisStyle = self.style()  # for loading icon images
#         return
#
#     def QtShow(self):  # 실행 후 종료 이벤트로 종료
#         sys.exit(self.exec_())

# ------------------------------------------------------------------------------
# QStatusBar
# ------------------------------------------------------------------------------
class STATUSBAR_CLASS:
    def __init__(self, wgStatusbar):
        self.widget = wgStatusbar
        return

    def New(self):
        self.Set_Defaults()
        return

    def Set_Defaults(self):
        self.Set_Text("Ready")
        return

    def Set_Text(self, strText='Ready', sec=-1):
        self.widget.showMessage(strText, sec)
        return

    def Set_Notice(self, strText='Ready', sec=60):
        self.widget.showMessage(strText, sec)
        return

    def Clear_Text(self):
        self.widget.clearMessage()
        return

    def Add_Widget(self, widget, stretch=0):
        self.widget.addWidget(widget, stretch)
        return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <4> Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ------------------------------------------------------------------------------
# Bool and Check
# ------------------------------------------------------------------------------
def Get_CheckToBool(state):
    if state == Qt.Unchecked:
        state = False  # 0
    elif state == Qt.PartiallyChecked:
        state = True  # 1
    elif state == Qt.Checked:
        state = True  # 2
    return state

def Get_BoolToCheck(state):
    if state:
        state = Qt.Checked
    elif not state:
        state = Qt.Unchecked
    return state

def Set_Check(widget, bCheck=True):
    widget.setChecked(bCheck)
    return

def Get_Check(widget):
    bCheck = widget.isChecked()
    return bCheck

# ------------------------------------------------------------------------------
# QVariables
# ------------------------------------------------------------------------------
def Get_QRect(rectData):
    data = [rectData.x(), rectData.y(), rectData.width(), rectData.height()]
    return data

def Set_QRect(arrData=[]):
    rectData = QRect(arrData[0], arrData[1], arrData[2], arrData[3])
    return rectData

def Get_QSize(sizeData):
    data = [sizeData.width(), sizeData.height()]
    return data

def Set_QSize(size):
    sizeData = QSize(size[0], size[0])
    return sizeData

# ------------------------------------------------------------------------------
# Common Function (for Widget)
# ------------------------------------------------------------------------------
def Set_Focus(widget):  # qtDesigner 에서 default 항목은 항상 체크 해제된 상태여야함
    widget.setFocus()
    return

def Set_Enable(widget, bMode=True):
    widget.setEnabled(bMode)
    return

def Set_Disable(widget, bMode=True):
    widget.setDisabled(bMode)
    return

def Set_Text(widget, value):
    if not isinstance(value, str):
        widget.setText("-")  # "No Data"
        return
    widget.setText(value)
    return

def Get_Text(widget):
    text = widget.text()
    return str(text)

def Get_fValue(widget, trailing=None):
    text = widget.text()
    if trailing is not None:
        fValue = round(float(text), trailing)
    else:
        fValue = float(text)
    return float(fValue)

def Get_iValue(widget):
    text = widget.text()
    return int(text)

def Get_Count(widget):
    return int(widget.count())

def Get_CurIndex(widget):
    index = widget.currentIndex()
    return int(index)

def Get_CurItem(widget):
    item = widget.currentItem()
    return item

def Set_CurIndex(widget, pos):
    widget.setCurrentIndex(-1)
    widget.setCurrentIndex(pos)
    return

def Set_Size(widget, w=120, h=25):
    widget.resize(w, h)
    return

def Get_Page(widget):
    return Get_CurIndex(widget)

def Set_Page(widget, pos=0):
    Set_CurIndex(widget, pos)
    return

def Set_FontSize(widget, size=10):
    fontWidget = widget.font()
    fontWidget.setPointSize(size)
    widget.setFont(fontWidget)
    return widget

def Show(widget):
    widget.show()
    return

def Hide(widget):
    widget.hide()
    return

def Clear_Data(widget):
    widget.clear()
    return

# ------------------------------------------------------------------------------
# Connect
# ------------------------------------------------------------------------------
def Get_Func_Connect(widget, func, *argv):
    if len(argv) == 0:
        funcConnect = func
    else:
        if widget == argv[0]:
            funcConnect = lambda: func(*argv)
        elif argv[0] == -1:
            funcConnect = lambda: func(widget)
        else:
            funcConnect = lambda: func(widget, *argv)
    return funcConnect

# ------------------------------------------------------------------------------
# Icon
# ------------------------------------------------------------------------------
def Make_Icon(path=""):  # jpg, png 가능
    wgIcon = QIcon()
    wgIcon.addPixmap(QPixmap(path))
    return wgIcon

# ------------------------------------------------------------------------------
# QButton
# ------------------------------------------------------------------------------
def Connect_clicked_Button(widget, func, *argv):
    funcConnect = Get_Func_Connect(widget, func, *argv)
    widget.clicked.connect(funcConnect)
    return

# ------------------------------------------------------------------------------
# QCombo
# ------------------------------------------------------------------------------
def Make_Combo(arrData=[], setCurrent=-1):
    wgCombo = QComboBox()
    if len(arrData) > 0:
        wgCombo.addItems(arrData)
        wgCombo.setCurrentIndex(-1)
        wgCombo.setCurrentIndex(setCurrent)  # always be behind addItems
    Set_Policy_ComboEdit(wgCombo, 0)
    Set_FontSize(wgCombo, 10)
    return wgCombo

# Connect
def Connect_Combo(widget, signal, func, *argv):
    funcConnect = Get_Func_Connect(widget, func, *argv)
    if signal == 0 or signal == 'currentIndexChanged':
        widget.currentIndexChanged.connect(funcConnect)
    elif signal == 1 or signal == 'itemSelectionChanged':
        widget.itemSelectionChanged.connect(funcConnect)
    else:
        print('[Error:Combo] Cannot find signal function')
    return

def Connect_currentIndexChanged_Combo(widget, func, *argv):
    funcConnect = Get_Func_Connect(widget, func, *argv)
    widget.currentIndexChanged.connect(funcConnect)
    return

def Connect_currentIndexChanged_Combo2(widget, func):
    funcConnect = Get_Func_Connect(widget, func, widget)
    widget.currentIndexChanged.connect(funcConnect)
    return

def Connect_activated_Combo(widget, func, *argv):
    funcConnect = Get_Func_Connect(widget, func, *argv)
    widget.activated.connect(funcConnect)
    return

def Connect_highlighted_Combo(widget, func, *argv):
    funcConnect = Get_Func_Connect(widget, func, *argv)
    widget.highlighted.connect(funcConnect)
    return

def Disconnect_Combo(widget, nameFunc=''):
    if nameFunc == 'currentIndexChanged':
        widget.currentIndexChanged.disconnect()
    elif nameFunc == 'activated':
        widget.activated.disconnect()
    elif nameFunc == 'highlighted':
        widget.highlighted.disconnect()
    else:
        print("[Error:Combo] Cannot disconnect")
    return

# Data
def Add_Data_Combo(wgCombo, data, curText=""):
    if not isinstance(curText, str):
        return
    if isinstance(data, list):
        wgCombo.addItems(data)
    else:
        wgCombo.addItem(data)
    #
    if curText:
        Set_Text_Combo(wgCombo, curText)
    return wgCombo

def Set_Data_Combo(wgCombo, data, curText=""):
    if not isinstance(curText, str):
        return
    wgCombo.clear()
    if isinstance(data, list):
        wgCombo.addItems(data)
    else:
        wgCombo.addItem(data)
    #
    if curText:
        Set_Text_Combo(wgCombo, curText)
    return wgCombo

def Add_Separator_Combo(wgCombo, pos=-1):
    if pos == -1: pos = Get_Count(wgCombo)
    wgCombo.insertSeparator(pos)
    return wgCombo

def Del_Index_Combo(wgCombo, pos=-1):
    if pos == -1: pos = Get_Count(wgCombo) - 1
    wgCombo.removeItem(pos)
    return

def Clear_Data_Combo(widget):
    widget.clear()
    return

def Change_Text_Combo(wgCombo, index, strText=""):
    if not isinstance(strText, str):
        return
    wgCombo.setItemText(index, strText)
    return

# Current
def Get_Text_Combo(wgCombo, index=-1):
    strText = ""
    if index == -1:
        strText = wgCombo.currentText()
        return str(strText)
    if 0 <= index < Get_Count(wgCombo):
        strText = wgCombo.itemText(index)
    return str(strText)

def Set_Text_Combo(wgCombo, strText=""):
    if not isinstance(strText, str):
        return
    #
    wgCombo.setCurrentIndex(-1)
    for ii in range(wgCombo.count()):
        if strText == wgCombo.itemText(ii):
            wgCombo.setCurrentIndex(ii)
    return

def Get_CurIndex_Combo(wgCombo):
    index = wgCombo.currentIndex()
    return int(index)

def Set_CurIndex_Combo(wgCombo, pos):
    wgCombo.setCurrentIndex(-1)
    wgCombo.setCurrentIndex(pos)
    return

# Editable
def Set_Editable_Combo(wgCombo, bMode=True):
    wgCombo.setEditable(bMode)
    return

def Set_Text_ComboEdit(wgCombo, strText=''):
    if not isinstance(strText, str):
        return
    wgCombo.setEditText(strText)
    return wgCombo

def Set_Policy_ComboEdit(wgCombo, policy=0):
    # 0 : QComboBox.NoInsert	# 엔터입력 시 새로운 항목이 추가되지 않도록 설정
    wgCombo.setInsertPolicy(policy)
    return

# ------------------------------------------------------------------------------
# QDialog or QMainWindow
# ------------------------------------------------------------------------------
def Get_UI(dlg_win, path=""):
    UI_CLASS = loadUiType(path)[0]
    if not UI_CLASS:
        print("[Error] Get_UI")
        return None
    ui = UI_CLASS()
    ui.setupUi(dlg_win)
    return ui

# ------------------------------------------------------------------------------
# QDialog
# ------------------------------------------------------------------------------
# OpenFileDlg (v1.1)
# (ex) ext: "CAD Files (*.stp *.step);;STL Files (*.stl);;All Files (*.*)"
# path=QDir.homePath()):
def OpenFileDlg(parent=None, title="Open file", ext="All Files (*.*)", path=homePath):
    fileName = QFileDialog.getOpenFileName(parent, title, path, ext)
    if fileName == "":
        return ""
    return str(fileName)

# OpenFilesDlg (v1.1)
def OpenFilesDlg(parent=None, title="Open files", ext="All Files (*.*)", path=homePath):
    fileNames = QFileDialog.getOpenFileNames(parent, title, path, ext)
    if fileNames == "":
        return ""
    arrFiles = []
    for dd in fileNames:
        arrFiles.append(str(dd))
    return arrFiles

# SaveFileDlg (v1.1)
def SaveFileDlg(parent=None, title="Save file", ext="All files (*.*)", path=homePath):
    fileName = QFileDialog.getSaveFileName(parent, title, path, ext, None)
    if fileName == "":
        return ""
    return fileName

# OpenFilesDlg (v1.1)
def OpenFolderDlg(parent=None, title="Open folder", path=homePath):
    options = QFileDialog.ShowDirsOnly  # | QFileDialog.DontUseNativeDialog
    pathName = QFileDialog.getExistingDirectory(parent, title, path, options)
    if pathName == "":
        return ""
    return pathName

# SaveFolderDlg (v1.1)
def SaveFolderDlg(parent=None, title="Create new folder", path=homePath):
    dlg = QFileDialog()
    options = QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog
    # dlg.setLabelText(QFileDialog.Accept, "Open")
    # dlg.setLabelText(QFileDialog.Reject, "Cancel")
    pathName = dlg.getSaveFileName(parent, title, path, "Directory", "", options)
    if pathName == "":
        return ""
    os.mkdir(pathName)
    dlg.close()
    return pathName

# ------------------------------------------------------------------------------
# QMainWindow
# ------------------------------------------------------------------------------
# Create_Window (v1.0)
def Create_Window(w=640, h=480, title="Qt4 Window (with NLibrary)"):
    win = QMainWindow()
    win.resize(w, h)
    win.setWindowTitle(title)
    Move_Window_Center(win)
    # if bShow: win.show() # 여기서 쓰면 추가 설정값이 적용되지않고 화면에 나타남
    return win

# Get_Window_UI (v1.0)
def Get_Window_UI(parent=None, path="", title=""):
    win = QMainWindow(parent)
    ui = Get_UI(win, path)
    return win, ui

# Move_Window_Center (v1.0)
def Move_Window_Center(win):
    winSize = win.geometry()
    monitorSize = QApplication.desktop().screenGeometry()
    x = (monitorSize.width() / 2) - (winSize.width() / 2)
    y = (monitorSize.height() / 2) - (winSize.height() / 2)
    win.setGeometry(x, y, winSize.width(), winSize.height())
    return win

# Set_Window_Title (v1.0)
def Set_Window_Title(win, title=""):
    win.setWindowTitle(title)
    return

# Connect_CloseEvent (v1.0)
def Connect_CloseEvent(dlg_win, func):
    dlg_win.closeEvent = func
    return

# Set_Window_Top (v1.0)
def Set_Window_Top(win, bMode=True):
    # flags = Qt.WindowFlags()
    if bMode:   # Always on Top
        flags = win.windowFlags() | Qt.WindowStaysOnTopHint

    else:   # Normal
        flags = win.windowFlags() & ~Qt.WindowStaysOnTopHint

    # Set
    win.setWindowFlags(flags)
    win.showNormal()
    return

# ------------------------------------------------------------------------------
# QMessageBox (v1.0)
# ------------------------------------------------------------------------------
# Msg (v1.0)
def Msg(parent=None, title="", text=""):
    QMessageBox.information(parent, title, text)
    return

# NoticeMsg (v1.0)
def NoticeMsg(parent=None, text=""):
    QMessageBox.information(parent, "Notice", str(text))
    return

# WarningMsg (v1.0)
def WarningMsg(parent=None, text=""):
    result = QMessageBox.warning(parent, "Warning", str(text), QMessageBox.Yes | QMessageBox.Cancel)
    if result == QMessageBox.Yes:
        result = "Yes"  # 1
    else:
        result = "No"  # 0
    return result

# ErrorMsg (v1.0)
def ErrorMsg(parent=None, text=""):
    QMessageBox.critical(parent, "Error", str(text))
    return

# QuestionMsg (v1.0)
def QuestionMsg(parent=None, text=""):
    result = QMessageBox.question(parent, "Question", str(text), QMessageBox.No | QMessageBox.Yes)
    if result == QMessageBox.No:
        result = "No"  # False
    elif result == QMessageBox.Yes:
        result = "Yes"  # True
    return result

def QuestionMsg2(parent=None, text=""):
    result = QMessageBox.question(parent, "Question", str(text), QMessageBox.Cancel | QMessageBox.No | QMessageBox.Yes)
    if result == QMessageBox.No:
        result = "No"  # False
    elif result == QMessageBox.Yes:
        result = "Yes"  # True
    elif result == QMessageBox.Cancel:
        result = "Cancel"  # True
    return result

# ------------------------------------------------------------------------------
# QTab
# ------------------------------------------------------------------------------
def Connect_Tab_Changed(wgTab, func):   # (ex) def func(index): print(index) return
    wgTab.currentChanged.connect(func)
    return

# ------------------------------------------------------------------------------
# THREAD_CLASS (v1.0)
# ------------------------------------------------------------------------------
# Notice : 클래스를 할당할 경우 무조건 self.를 붙여서 쓰레드 변수가 함수 밖에서도 소멸되지않도록 해야함
# (Ex)
class THREAD_CLASS(QThread):
    def __init__(self):
        QThread.__init__(self)
        # Common
        self.bPause = False  # 쓰레드 일시 정지 변수
        self.bStop = False  # 쓰레드 탈출 변수
        return

    def Start(self, nameFunc, iPriority=3):  # 0~6: Low~Fast, 3: Normal(Default)
        self.bPause = False
        self.bStop = False
        #
        self.run = nameFunc
        self.start(iPriority)
        return

    def Next(self, nameFunc=None):
        self.bPause = False
        self.bStop = False

        ## 참고 ##
        # 이전 쓰레드 작업 종료 후 이어서 다른 쓰레드 작업 추가 시 사용 (무한대로 추가 가능함)
        # 단, 따로 실행시키는 것이 아니라 이전 함수의 마지막 부분에 넣어야함
        if nameFunc is not None:
            self.quit = nameFunc
        self.quit()
        return

    # Command
    def Pause(self):
        self.bPause = True
        return

    def Continue(self):
        self.bPause = False
        return

    def Stop(self, bOpt=False):
        self.bStop = True  # 강제가 아닌 지역 변수로 진행 중인 작업 중단시킴
        return

    def Terminate(self, bOpt=False):
        self.bStop = True  # 강제가 아닌 지역 변수로 진행 중인 작업 중단시킴(강제 종료 전 먼저 확인)
        self.terminate()  # 현재 진행 중인 쓰레드를 강제로 멈춤, 대신 다음 작업은 불가능
        return

    # emit
    ## 주의 ##
    # emit 함수는 쓰레드가 먼저 시작한 순서가 아니라 쓰래드 작업이 먼저 끝난 순서대로 실행됨
    # 그러므로 emit 함수는 왠만하면 한번씩 사용할 것, emit()은 동시에 실행되지 않음
    # 쓰레드 도중 실행되어야 할 UI를 정의하거나 저장된 함수를 실행하는 함수(쓰레드 내에서는 UI 실행이 불가능하므로 emit으로 전달시켜야함)

    # Signal
    signal_uiJob = pyqtSignal()

    def Show_UI(self, nameFunc=None):
        if nameFunc is None:
            self.signal_uiJob.connect(nameFunc)
        self.signal_uiJob.emit()
        return

    # Check
    def IsRunning(self):
        return self.isRunning()

    def IsFinished(self):
        return self.isFinished()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <5> Run
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~