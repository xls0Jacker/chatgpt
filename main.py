#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-06-11 10:41
from os import listdir, remove

from PySide2.QtCore import QSize, QDate, QTime, Signal
from PySide2.QtWidgets import QApplication, QMessageBox, QListWidgetItem, QFileDialog, QMenu, QAction, QInputDialog, \
    QWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QPixmap, QCursor, QFontDatabase, QFont, Qt
import re
# 成员列表中用户的名称是唯一的

class loginInterface():# 登录界面
    # "100%Jacker""09058572"
    # 账号和密码
    account = "1"
    keywords = "1"
    def __init__(self):
        # 载入 UI
        self.ui = QUiLoader().load('ui/login.ui')
        # 设置界面图标
        app.setWindowIcon(QIcon('Ficons/10.ico'))
        # 禁止拉伸窗口大小
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        # 载入字体
        QFontDatabase.addApplicationFont("Fonts/Mengshen-Handwritten.ttf")

        # 登录按钮被点击
        self.ui.loginButton.clicked.connect(self.loginConformity)
        self.ui.keywords.returnPressed.connect(self.loginConformity)
        # 账号回车
        self.ui.account.returnPressed.connect(self.LineChange)

        # 将光标置于账号上
        self.ui.account.setFocus()

        # 设置登录界面的主图标
        ico = self.ui.label
        ico.setPixmap(QPixmap('Ficons/10.ico'))
        ico.setScaledContents(True) # 自适应图片

    def LineChange(self):# 账号回车换行功能
        self.ui.keywords.setFocus()

    def loginConformity(self):# 账号密码检测
        acct = self.ui.account.text()
        kwords = self.ui.keywords.text()
        if acct == self.account and kwords == self.keywords:
            self.m = mainInterface()
            self.m.ui.setWindowTitle(acct) # 将用户名称设计为主界面标题
            self.m.ui.move(1500, 100)
            self.m.ui.show()
            self.ui.close()
        elif acct == "" and kwords == "":
            QMessageBox.warning(self.ui, "提示", "请输入账号和密码")
        elif acct == "" and kwords != "":
            QMessageBox.warning(self.ui, "提示", "请输入账号")
        elif acct != "" and kwords == "":
            QMessageBox.warning(self.ui, "提示", "请输入密码")
        else:
            QMessageBox.warning(self.ui, "提示", "请检查账号和密码是否正确")
# ------------------------------------------------------------------------------------- #
class mainInterface():# 主界面
    # 存储姓名和图标映射关系
    map_Icon_Name = dict()

    def __init__(self):
        # 默认 slogan
        self.defaultSlogan = "我是一个可爱的机器人~"

        # 载入 UI
        self.ui = QUiLoader().load('ui/main.ui')
        # 设置界面图标
        app.setWindowIcon(QIcon('Ficons/10.ico'))
        # 设置刷新按钮图标及其大小
        self.ui.refreshButton.setIcon(QIcon('icon/refresh.ico'))
        self.ui.refreshButton.setIconSize(QSize(50, 50))
        # 禁止拉伸窗口大小
        self.ui.setFixedSize(self.ui.width(), self.ui.height())

        # 添加好友
        self.ui.addButton.clicked.connect(self.AddInterface)
        # 刷新好友列表
        self.ui.refreshButton.clicked.connect(self.data_init)
        # 右键好友项生成菜单
        self.ui.list.customContextMenuRequested.connect(self.myListWidgetContext)
        # 双击进入好友界面
        self.ui.list.doubleClicked.connect(self.FriendContext)
        # 进入好感度机制界面
        self.ui.configureButton.clicked.connect(self.ConfigureInterface)

        # 好友列表初始化
        self.data_init()


    def data_init(self):# 生成好友列表
        self.ui.list.clear() # 清空当前列表 防止再调用时残留
        self.map_Icon_Name.clear() # 清空缓存表 防止再调用时残留
        with open("friends.txt", "r", encoding='utf-8') as fp:
            temp = fp.read()
            pattern = re.compile(r'(.+(.png|jpg|jpeg|ico)) (.+) (-?\d+)')
            print(re.findall(pattern, temp)) # 只要元组的第一项和第三项和第四项 分别是图标地址和姓名以及好感度数值
            for i in re.findall(pattern, temp):
                self.map_Icon_Name[i[2]] = i[0] # 以姓名为键
                flag = False # 标志是否存在该名称文件
                for filename in listdir("friends"):# 匹配好友名称 生成好友信息文件
                    if i[2] + '.txt' == filename:
                        flag = True
                if flag == False:
                    # 生成好友信息文件
                    with open('friends/' + i[2] + '.txt', "w", encoding='utf-8') as fw:
                        # 文件第一行存储图片位置 文件第二行存储好友名称 第三行存储好感度 第四行是默认 slogan 自动存储
                        fw.write(i[0]+'\n'+i[2]+'\n'+i[3]+'\n'+self.defaultSlogan+'\n')
                    # 生成好友日志文件
                    with open('friends/' + i[2] + '_dialog.txt', "w", encoding='utf-8') as fw:
                        fw.writable() # 没有操作 创建文件
        # print(self.map_Icon_Name) # 检查
        # 加入列表项
        self.ui.list.setIconSize(QSize(50, 50))
        for n, p in self.map_Icon_Name.items():
            item = QListWidgetItem()
            item.setIcon(QIcon(p))
            item.setText(n)
            self.ui.list.addItem(item)

    def myListWidgetContext(self, position): # 右键生成菜单
        # 弹出菜单
        popMenu = QMenu()
        delAct = QAction("删除好友", self.ui)
        # 查看右键时是否在item上面,如果不在.就不显示删除
        if self.ui.list.itemAt(position):
            popMenu.addAction(delAct)
            delAct.triggered.connect(self.DeleteItem) # 菜单选项点击触发
            popMenu.exec_(self.ui.list.mapToGlobal(position)) # 将菜单出现的位置设置为当前鼠标的位置

    def DeleteItem(self): # 删除好友
        decision = QMessageBox.question(self.ui, "提示", "是否删除该好友？")
        if decision == QMessageBox.Yes:
            name = self.ui.list.currentItem().text() # 获取当前所选对象的文本
            with open("friends.txt", "r", encoding='utf-8') as fp:
                infor = fp.readlines()# 获取每一行用空字符拆分来匹配名称（前提是名称中不能存在空格）
                tempInfor = infor # 用于存储删除一行后的文本信息
                for line in infor:
                    for n in line.split():
                        if n == name:
                            remove("friends/" + name + ".txt") # 删除好友文件夹中的文本文件
                            tempInfor.remove(line)
                            with open("friends.txt", "w", encoding='utf-8') as fw: # 将删除一行后的文本信息写进去
                                fw.writelines(tempInfor)
            self.data_init() # 刷新榜单


    def AddInterface(self):# 调起添加好友的程序窗口
        self.add = addInterface()
        self.add.ui.show()

    def FriendContext(self): # 双击进入好友界面
        self.fri = friendInterface()
        self.fri.ui.show()
        self.fri.name = self.ui.list.currentItem().text() # 获取当前所选项的名称
        self.fri.icon = self.ui.list.currentItem().icon() # 获取当前所选项的图标
        self.fri.data_init() # 加载参数

    def ConfigureInterface(self): # 进入好感度机制界面
        self.cfg = configureInterface()
        self.cfg.ui.show()
# ------------------------------------------------------------------------------------- #
class addInterface():# 添加好友

    def __init__(self):
        self.defaultIcon = "icon/normalIcon.ico"  # 默认头像
        self.defaultName = "100%Jacker"  # 默认姓名
        self.defaultLove = "" # 默认好感度
        self.defaultSlogan = "我是一个可爱的机器人~"
        self.newIcon = "icon/normalIcon.ico"
        self.newName = "100%Jacker"
        self.newLove = ""
        self.item = QListWidgetItem()  # 预览对象

        self.ui = QUiLoader().load('ui/additem.ui')
        app.setWindowIcon(QIcon('Ficons/10.ico'))
        self.ui.setFixedSize(self.ui.width(), self.ui.height())  # 禁止拉伸窗口大小

        # 切换浏览可选状态
        self.ui.freeSelection.toggled.connect(self.FreeSelected)
        self.ui.defaultSelection.toggled.connect(self.DefaultSelected)
        # 检测文本变化
        self.ui.nameEdit.textChanged.connect(self.HandleTextChange)
        self.ui.loveEdit.textChanged.connect(self.HandleTextChange_2)
        # 展开文件夹
        self.ui.dialogButton.clicked.connect(self.ShowFolder)
        # 确认添加好友
        self.ui.confirmButton.clicked.connect(self.AddFriend)
        # 取消退出页面
        self.ui.cancelButton.clicked.connect(self.Close)
        # 设置回车光标转移
        self.ui.loveEdit.returnPressed.connect(self.LineChange)
        # 设置回车确认
        self.ui.nameEdit.returnPressed.connect(self.AddFriend)

        # 设置按钮默认状态
        self.ui.dialogButton.setEnabled(False)
        self.ui.defaultSelection.setChecked(True)
        # 设置默认文本
        self.ui.nameEdit.setPlaceholderText("100%Jacker")
        self.ui.loveEdit.setPlaceholderText("0")
        # 丝滑体验
        self.ui.loveEdit.setFocus()


        self.data_init()

    def data_init(self):
        self.ui.list.setIconSize(QSize(50, 50))
        self.item.setIcon(QIcon(self.defaultIcon))
        self.item.setText(self.defaultName)
        self.ui.list.addItem(self.item)

    def AddFriend(self):# 确认添加
        # 检测好感度文本是否为数值 否则设置为默认值
        content = self.ui.loveEdit.text()
        if content.isdigit() == False and content != "":
            QMessageBox.warning(self.ui, "提示", "请输入整型数值")
            content = self.defaultLove
            self.ui.loveEdit.setText(self.defaultLove)
            return
        decision = QMessageBox.question(self.ui, "确认", "确认添加该好友吗？")
        if decision == QMessageBox.Yes:
            if self.newLove == "":
                self.newLove = "0"
            with open("friends.txt", "a", encoding="utf-8") as fw:
                fw.write(self.newIcon + " " + self.newName + " " + self.newLove + "\n")
            # # 重载主界面的列表
            # self.Refresh()
            # 关闭添加好友界面
            self.ui.close()


    def FreeSelected(self):# 自定义头像被选中
        self.ui.dialogButton.setEnabled(True) # 开启使用浏览按钮

    def DefaultSelected(self):# 默认被选中
        self.ui.dialogButton.setEnabled(False) # 禁用浏览按钮

    def HandleTextChange(self):# 姓名文本发生改变
        content = self.ui.nameEdit.text()
        self.item.setText(content)
        self.newName = content # 将当前名字做备份

    def HandleTextChange_2(self):# 好感度文本发生改变
        content = self.ui.loveEdit.text()
        self.newLove = content # 备份

    def ShowFolder(self): # 选取照片作为头像
        filePath, _ = QFileDialog.getOpenFileName(
            self.ui,  # 父窗口对象
            "选择你要上传的图片",  # 标题
            r"C:\Users\27414\Pictures\Saved Pictures",  # 起始目录为系统的图像目录
            "图片类型 (*.png *.jpg *.bmp *.ico)"  # 选择类型过滤项，过滤内容在括号中
        )
        self.item.setIcon(QIcon(filePath))
        self.newIcon = filePath # 将当前图片位置做备份

    def LineChange(self):
        self.ui.nameEdit.setFocus()

    def Close(self):# 取消退出添加好友的窗口
        self.ui.close()


# ------------------------------------------------------------------------------------- #
class friendInterface(): # 好友界面
    icon = QIcon() # 当前好友图标位置（通过主界面传参）
    name = "" # 当前好友名称（通过主界面传参）
    def __init__(self):
        self.defaultDialog = "" # 默认日志文本
        self.defaultLoveChanged = 0 # 默认好感度修改值
        self.newDialog = ""  #  新日志文本
        self.newLoveChanged = 0  # 新好感度修改值
        self.love = int() # 好感度数值

        self.ui = QUiLoader().load('ui/friend.ui')
        app.setWindowIcon(QIcon('Ficons/10.ico'))
        self.ui.setFixedSize(self.ui.width(), self.ui.height())  # 禁止拉伸窗口大小

        # 点击修改
        self.ui.modifyButton.clicked.connect(self.ModifyButtonClicked)
        # 检测文本修改
        self.ui.sloganEdit.textChanged.connect(self.HandleTextChanged)
        self.ui.inforEdit.textChanged.connect(self.HandleTextChanged_2)
        # 点击确认
        self.ui.confirmButton_1.clicked.connect(self.ConfirmButton_1Clicked)
        self.ui.confirmButton_2.clicked.connect(self.ConfirmButton_2Clicked)
        # 回车点击确认
        self.ui.sloganEdit.returnPressed.connect(self.ConfirmButton_1Clicked)
        self.ui.inforEdit.returnPressed.connect(self.ConfirmButton_2Clicked)
        # 列表项双击打开日志
        self.ui.dialog.doubleClicked.connect(self.OpenDialog)
        # 右键菜单
        self.ui.dialog.customContextMenuRequested.connect(self.myListWidgetContext)

        # 设置控件的初始显示状态
        self.ui.sloganEdit.setVisible(False)
        self.ui.confirmButton_1.setVisible(False)
        self.ui.warning.setVisible(False)
        self.ui.confirmButton_2.setVisible(False)
        # 设置 slogan 默认文本
        self.ui.sloganEdit.setPlaceholderText("我是一个可爱的机器人~")
        # 设置日志表单图标的默认大小
        self.ui.dialog.setIconSize(QSize(32, 32))
        # 设置 QSpinBox 的取值范围
        self.ui.changedNumber.setMinimum(-25)
        self.ui.changedNumber.setMaximum(25)

    def data_init(self): # 载入个人信息 && 好感度图片匹配
        self.ui.dialog.clear() # 清空当前列表项

        self.ui.icon.setPixmap(self.icon.pixmap(QSize(150, 150))) # 将图片转为 pixmap 并设计大小
        self.ui.setWindowTitle(self.name)
        self.ui.name.setText(self.name)
        # 调整字体的样式
        self.ui.name.setFont(QFont("Mengshen-Handwritten", 20))
        self.ui.loveNumber.setStyleSheet("color: white")
        self.ui.loveNumber.setFont(QFont("Mengshen-Handwritten", 10))
        self.ui.loveNumber.setAlignment(Qt.AlignCenter) # 文本居中
        # 从文件调取 slogan 信息
        for filename in listdir("friends"):
            if self.name + ".txt" == filename:
                with open("friends/" + filename, "r", encoding='utf-8') as fp:
                    infor = fp.readlines()
                    self.ui.sloganEdit.setText(infor[3])  # 个人信息的第四行是 slogan
                    self.love = int(infor[2]) # 没有换行符捏
                    self.ui.loveNumber.setText(str(self.love)) # 载入好感度数值
        # 匹配好感度图片
        self.ui.love.setScaledContents(True)  # 自适应图片
        if self.love <= -75:
            self.ui.love.setPixmap(QPixmap('Licons/love-8.png'))
        elif -75 < self.love <= -50:
            self.ui.love.setPixmap(QPixmap('Licons/love-7.png'))
        elif -50 < self.love <= -25:
            self.ui.love.setPixmap(QPixmap('Licons/love-6.png'))
        elif -25 < self.love <= 0:
            self.ui.love.setPixmap(QPixmap('Licons/love-5.png'))
        elif 0 < self.love <= 25:
            self.ui.love.setPixmap(QPixmap('Licons/love-1.png'))
        elif 25 < self.love <= 50:
            self.ui.love.setPixmap(QPixmap('Licons/love-2.png'))
        elif 50 < self.love <= 75:
            self.ui.love.setPixmap(QPixmap('Licons/love-3.png'))
        elif 75 < self.love:
            self.ui.love.setPixmap(QPixmap('Licons/love-4.png'))
        # 载入日志文件
        with open("friends/" + self.name + "_dialog.txt", "r", encoding='utf-8') as fp:
            lines = fp.readlines()
            for line in lines:
                if line.strip() == "": # 防止空挡报错
                    continue
                self.item = QListWidgetItem()  # 预览对象
                infor = line.split()
                self.item.setText("好感度波动值：" + infor[4] +  " " + infor[2] + " " + infor[3])
                preLove = int(infor[0])
                if preLove <= -75:
                    self.item.setIcon(QIcon('Licons/love-8.png'))
                elif -75 < preLove <= -50:
                    self.item.setIcon(QIcon('Licons/love-7.png'))
                elif -50 < preLove <= -25:
                    self.item.setIcon(QIcon('Licons/love-6.png'))
                elif -25 < preLove <= 0:
                    self.item.setIcon(QIcon('Licons/love-5.png'))
                elif 0 < preLove <= 25:
                    self.item.setIcon(QIcon('Licons/love-1.png'))
                elif 25 < preLove <= 50:
                    self.item.setIcon(QIcon('Licons/love-2.png'))
                elif 50 < preLove <= 75:
                    self.item.setIcon(QIcon('Licons/love-3.png'))
                elif 75 < preLove:
                    self.item.setIcon(QIcon('Licons/love-4.png'))
                # 加入修改后的列表对象
                self.ui.dialog.addItem(self.item)

    def ModifyButtonClicked(self): # 修改控件的可见状态 && 转移光标位置
        self.ui.slogan.setVisible(False)
        self.ui.modifyButton.setVisible(False)
        self.ui.sloganEdit.setVisible(True)
        self.ui.confirmButton_1.setVisible(True)
        self.ui.warning.setVisible(True)
        self.ui.sloganEdit.setFocus()

    def HandleTextChanged(self): # 同步修改 slogan 文本
        text = self.ui.sloganEdit.text()
        self.ui.slogan.setText(text)

    def HandleTextChanged_2(self): # 不为空时出现确认按钮
        if self.ui.inforEdit.text() != "":
            self.ui.confirmButton_2.setVisible(True)
        else:
            self.ui.confirmButton_2.setVisible(False)

    # def HandleValueChanged(self): # 更新好感度修改值
    #     self.newLoveChanged = self.ui.changedNumber.value()

    def ConfirmButton_1Clicked(self): # 修改控件的可见状态 && 转移光标位置 && 存储信息
        self.ui.sloganEdit.setVisible(False)
        self.ui.confirmButton_1.setVisible(False)
        self.ui.warning.setVisible(False)
        self.ui.slogan.setVisible(True)
        self.ui.modifyButton.setVisible(True)
        self.ui.inforEdit.setFocus()
        for filename in listdir("friends"):
            if self.name + ".txt" == filename:
                with open("friends/" + filename, "r", encoding='utf-8') as fp:
                    infor = fp.readlines()
                    infor[3] = self.ui.sloganEdit.text() # 个人信息的第四行是 slogan
                with open("friends/" + filename, "w", encoding='utf-8') as fw:
                    fw.writelines(infor)

    def ConfirmButton_2Clicked(self): # 生成日志列表对象
        decision = QMessageBox.question(self.ui, "提示", "是否保存此次日志内容？")
        if decision == QMessageBox.Yes:
            date = QDate.currentDate()  # 获取当前日期
            time = QTime.currentTime()  # 获取当前时间
            nowDate = date.toString(Qt.ISODate) # 转化为 -- 形式
            nowTime = time.toString(Qt.DefaultLocaleLongDate) # 转化为 .. 形式
            # 一个日志格式为：编辑时的好感度数值+内容+日期+好感度修改值
            self.newDialog = str(self.love) + " " + self.ui.inforEdit.text() + " " \
                             + nowDate + " " + nowTime + " " + str(self.ui.changedNumber.value()) + '\n'
            # 追加日志
            with open("friends/" + self.name + "_dialog.txt", "a", encoding='utf-8') as fw:
                # print(self.newDialog)
                fw.write(self.newDialog)
            # 更新好友信息中的好感度数值
            self.love = self.love + self.ui.changedNumber.value()
            # print(self.love, self.ui.changedNumber.value())
            with open("friends/" + self.name + ".txt", "r", encoding="utf-8") as fp:
                lines = fp.readlines()
                lines[2] = str(self.love)+'\n'
            with open("friends/" + self.name + ".txt", "w", encoding="utf-8") as fw:
                fw.writelines(lines)
            # 重载好友信息
            self.data_init()

    def OpenDialog(self): # 打开日志
        self.log = dialogInterface()
        self.log.ui.show()
        self.log.name = self.name # 获取当前好友名称 用作文件查询
        self.log.icon = self.ui.dialog.currentItem().icon() # 获取当前所选项的图标
        self.log.id = self.ui.dialog.row(self.ui.dialog.currentItem()) + 1 # 获取当前列表项序号（以 1 开始）
        self.log.data_init() # 加载参数

    def myListWidgetContext(self, position): # 右键生成菜单
        # 弹出菜单
        popMenu = QMenu()
        delAct = QAction("删除该日志", self.ui)
        # 查看右键时是否在item上面,如果不在.就不显示删除
        if self.ui.dialog.itemAt(position):
            popMenu.addAction(delAct)
            delAct.triggered.connect(self.DeleteDialog) # 菜单选项点击触发
            popMenu.exec_(self.ui.dialog.mapToGlobal(position)) # 将菜单出现的位置设置为当前鼠标的位置

    def DeleteDialog(self): # 删除日志项
        decision = QMessageBox.question(self.ui, "提示", "是否删除该条日志？")
        if decision == QMessageBox.Yes:
            text = self.ui.dialog.currentItem().text()  # 获取当前所选对象的文本
            text = text.split() # 将文本拆分为列表 获得主码：时间
            # print(text)
            with open("friends/" + self.name + "_dialog.txt", "r", encoding='utf-8') as fp:
                infor = fp.readlines()  # 获取每一行用空字符拆分来匹配名称（前提是名称中不能存在空格）
                tempInfor = infor  # 用于存储删除一行后的文本信息
                for line in infor:
                    for n in line.split():
                        if n == text[2]: # 将删除一行后的文本信息写进去
                            tempInfor.remove(line)
                            with open("friends/" + self.name + "_dialog.txt", "w", encoding='utf-8') as fw:
                                fw.writelines(tempInfor)
            self.data_init()  # 刷新列表项
# ------------------------------------------------------------------------------------- #
class dialogInterface():
    # 界面传参
    name = ""
    icon = QIcon()
    id = int()
    def __init__(self):
        # ui 界面初始化
        self.ui = QUiLoader().load('ui/dialog.ui')
        # 禁止拉伸窗口大小
        self.ui.setFixedSize(self.ui.width(), self.ui.height())

    def data_init(self):
        # 根据列表项位次设定标题
        self.ui.setWindowTitle("日志" + " " + str(self.id) + " ")
        # 调整字体的样式
        self.ui.loveNumber.setStyleSheet("color: white")
        self.ui.loveNumber.setFont(QFont("Mengshen-Handwritten", 10))
        self.ui.loveNumber.setAlignment(Qt.AlignCenter) # 文本居中
        self.ui.changedNumber.setFont(QFont("Mengshen-Handwritten", 15))
        self.ui.name.setFont(QFont("Mengshen-Handwritten", 15))
        self.ui.description.setFont(QFont("Mengshen-Handwritten", 12))
        # 设置好感度图标
        self.ui.love.setPixmap(self.icon.pixmap(QSize(64, 64))) # 将图片转为 pixmap 并设计大小
        # 设置名称
        self.ui.name.setText(self.name)
        # 拆分信息填入相应位置
        with open("friends/" + self.name + "_dialog.txt", "r", encoding='utf-8') as fp:
            lines = fp.readlines()
        infor = lines[self.id - 1].split()
        # print(infor)
        self.ui.loveNumber.setText(infor[0]) # 设置好感度数值
        self.ui.textBrowser.append(infor[1]) # 填入内容
        self.ui.time.setText(infor[2] + " " + infor[3]) # 载入编辑时间
        self.ui.changedNumber.setText(infor[4]) # 载入好感度波动值
# ------------------------------------------------------------------------------------- #
class configureInterface():
    def __init__(self):
        # ui 界面初始化
        self.ui = QUiLoader().load('ui/configure.ui')
        # 禁止拉伸窗口大小
        self.ui.setFixedSize(self.ui.width(), self.ui.height())

        # 点击修改文本
        self.ui.modifyButton.clicked.connect(self.ShowModifyEdit)
        # 点击确认修改
        self.ui.confirmButton.clicked.connect(self.Confirmation)

        # 界面初始化
        self.data_init()

        # 设置编辑框的初始状态为可读状态
        self.ui.plainTextEdit_1.setReadOnly(True)
        self.ui.plainTextEdit_2.setReadOnly(True)
        self.ui.plainTextEdit_3.setReadOnly(True)
        self.ui.plainTextEdit_4.setReadOnly(True)
        self.ui.plainTextEdit_5.setReadOnly(True)
        self.ui.plainTextEdit_6.setReadOnly(True)
        self.ui.plainTextEdit_7.setReadOnly(True)
        self.ui.plainTextEdit_8.setReadOnly(True)
        # 设置确认按钮的默认显示状态
        self.ui.confirmButton.setVisible(False)


    def data_init(self):
        # 显示不同等级好感度图标
        self.ui.love_1.setPixmap(QIcon('Licons/love-1.png').pixmap(QSize(64, 64))) # 将图片转为 pixmap 并设计大小
        self.ui.love_2.setPixmap(QIcon('Licons/love-2.png').pixmap(QSize(64, 64)))
        self.ui.love_3.setPixmap(QIcon('Licons/love-3.png').pixmap(QSize(64, 64)))
        self.ui.love_4.setPixmap(QIcon('Licons/love-4.png').pixmap(QSize(64, 64)))
        self.ui.love_5.setPixmap(QIcon('Licons/love-5.png').pixmap(QSize(64, 64)))
        self.ui.love_6.setPixmap(QIcon('Licons/love-6.png').pixmap(QSize(64, 64)))
        self.ui.love_7.setPixmap(QIcon('Licons/love-7.png').pixmap(QSize(64, 64)))
        self.ui.love_8.setPixmap(QIcon('Licons/love-8.png').pixmap(QSize(64, 64)))
        # 载入好感度描述
        L = [] # QplainTextEdit 组成的列表
        L.append(self.ui.plainTextEdit_1)
        L.append(self.ui.plainTextEdit_2)
        L.append(self.ui.plainTextEdit_3)
        L.append(self.ui.plainTextEdit_4)
        L.append(self.ui.plainTextEdit_5)
        L.append(self.ui.plainTextEdit_6)
        L.append(self.ui.plainTextEdit_7)
        L.append(self.ui.plainTextEdit_8)
        for id in range(8):
            with open("configure/" + "description_" + str(id + 1) + ".txt", "r", encoding = 'utf-8') as fp:
                lines = fp.read()
                L[id].setPlainText(lines)

    def ShowModifyEdit(self):# 改变编辑文本框状态 && 改变按钮可见状态
        # 改变文本框状态
        self.ui.plainTextEdit_1.setReadOnly(False)
        self.ui.plainTextEdit_2.setReadOnly(False)
        self.ui.plainTextEdit_3.setReadOnly(False)
        self.ui.plainTextEdit_4.setReadOnly(False)
        self.ui.plainTextEdit_5.setReadOnly(False)
        self.ui.plainTextEdit_6.setReadOnly(False)
        self.ui.plainTextEdit_7.setReadOnly(False)
        self.ui.plainTextEdit_8.setReadOnly(False)
        # 设置可见状态
        self.ui.modifyButton.setVisible(False)
        self.ui.confirmButton.setVisible(True)

    def Confirmation(self): # 确认后载入设置中
        decision = QMessageBox.question(self.ui, "提示", "确认修改好感度机制？")
        if decision == QMessageBox.Yes:
            # 设置可见状态
            self.ui.modifyButton.setVisible(True)
            self.ui.confirmButton.setVisible(False)
            # 写入文件
            L = []  # QplainTextEdit 组成的列表
            L.append(self.ui.plainTextEdit_1)
            L.append(self.ui.plainTextEdit_2)
            L.append(self.ui.plainTextEdit_3)
            L.append(self.ui.plainTextEdit_4)
            L.append(self.ui.plainTextEdit_5)
            L.append(self.ui.plainTextEdit_6)
            L.append(self.ui.plainTextEdit_7)
            L.append(self.ui.plainTextEdit_8)
            for id in range(8):
                with open("configure/" + "description_" + str(id + 1) + ".txt", "w", encoding='utf-8') as fw:
                    fw.write(L[id].toPlainText())
            # 设置编辑框的初始状态为可读状态
            self.ui.plainTextEdit_1.setReadOnly(True)
            self.ui.plainTextEdit_2.setReadOnly(True)
            self.ui.plainTextEdit_3.setReadOnly(True)
            self.ui.plainTextEdit_4.setReadOnly(True)
            self.ui.plainTextEdit_5.setReadOnly(True)
            self.ui.plainTextEdit_6.setReadOnly(True)
            self.ui.plainTextEdit_7.setReadOnly(True)
            self.ui.plainTextEdit_8.setReadOnly(True)
            # 重载好感度描述
            self.data_init()

app = QApplication([])
login = loginInterface()
login.ui.show()
app.exec_()