# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/patrick/pksampler-0.3/pksampler/MidiDialogForm.ui'
#
# Created: Wed Jun 29 02:38:59 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class MidiDialogForm(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("MidiDialogForm")

        self.setModal(1)

        MidiDialogFormLayout = QGridLayout(self,1,1,6,6,"MidiDialogFormLayout")

        self.pushButton2 = QPushButton(self,"pushButton2")

        MidiDialogFormLayout.addWidget(self.pushButton2,2,1)

        self.groupBox1 = QGroupBox(self,"groupBox1")
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(6)
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        self.textLabel4 = QLabel(self.groupBox1,"textLabel4")

        groupBox1Layout.addWidget(self.textLabel4,0,0)

        self.textLabel5 = QLabel(self.groupBox1,"textLabel5")

        groupBox1Layout.addWidget(self.textLabel5,1,0)

        self.channelLineEdit = QLineEdit(self.groupBox1,"channelLineEdit")
        self.channelLineEdit.setEnabled(0)

        groupBox1Layout.addWidget(self.channelLineEdit,0,1)

        self.controllerLineEdit = QLineEdit(self.groupBox1,"controllerLineEdit")
        self.controllerLineEdit.setEnabled(0)

        groupBox1Layout.addWidget(self.controllerLineEdit,1,1)

        MidiDialogFormLayout.addMultiCellWidget(self.groupBox1,1,1,0,1)

        self.pushButton1 = QPushButton(self,"pushButton1")
        self.pushButton1.setDefault(1)

        MidiDialogFormLayout.addWidget(self.pushButton1,2,0)

        self.textLabel3 = QLabel(self,"textLabel3")

        MidiDialogFormLayout.addMultiCellWidget(self.textLabel3,0,0,0,1)

        self.languageChange()

        self.resize(QSize(163,151).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pushButton2,SIGNAL("clicked()"),self.reject)
        self.connect(self.pushButton1,SIGNAL("clicked()"),self.accept)


    def languageChange(self):
        self.setCaption(self.__tr("Midi Selector"))
        self.pushButton2.setText(self.__tr("Cancel"))
        self.groupBox1.setTitle(QString.null)
        self.textLabel4.setText(self.__tr("Channel:"))
        self.textLabel5.setText(self.__tr("Controller:"))
        self.channelLineEdit.setText(self.__tr("1"))
        self.controllerLineEdit.setText(self.__tr("1"))
        self.pushButton1.setText(self.__tr("OK"))
        self.textLabel3.setText(self.__tr("Move a midi control..."))


    def __tr(self,s,c = None):
        return qApp.translate("MidiDialogForm",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = MidiDialogForm()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
