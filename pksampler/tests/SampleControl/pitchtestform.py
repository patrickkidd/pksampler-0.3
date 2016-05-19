# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/patrick/pksampler-0.3/pksampler/tests/SampleControl/pitchtestform.ui'
#
# Created: Wed Jun 29 02:39:00 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class pitchtestform(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("pitchtestform")


        pitchtestformLayout = QHBoxLayout(self,6,6,"pitchtestformLayout")

        self.slider1 = QSlider(self,"slider1")
        self.slider1.setMaxValue(127)
        self.slider1.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider1)

        self.slider2 = QSlider(self,"slider2")
        self.slider2.setMaxValue(127)
        self.slider2.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider2)

        self.slider3 = QSlider(self,"slider3")
        self.slider3.setMaxValue(127)
        self.slider3.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider3)

        self.slider4 = QSlider(self,"slider4")
        self.slider4.setMaxValue(127)
        self.slider4.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider4)

        self.slider5 = QSlider(self,"slider5")
        self.slider5.setMaxValue(127)
        self.slider5.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider5)

        self.slider6 = QSlider(self,"slider6")
        self.slider6.setMaxValue(127)
        self.slider6.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider6)

        self.slider7 = QSlider(self,"slider7")
        self.slider7.setMaxValue(127)
        self.slider7.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider7)

        self.slider8 = QSlider(self,"slider8")
        self.slider8.setMaxValue(127)
        self.slider8.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider8)

        self.slider9 = QSlider(self,"slider9")
        self.slider9.setMaxValue(127)
        self.slider9.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider9)

        self.slider10 = QSlider(self,"slider10")
        self.slider10.setMaxValue(127)
        self.slider10.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider10)

        self.slider11 = QSlider(self,"slider11")
        self.slider11.setMaxValue(127)
        self.slider11.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider11)

        self.slider12 = QSlider(self,"slider12")
        self.slider12.setMaxValue(127)
        self.slider12.setOrientation(QSlider.Vertical)
        pitchtestformLayout.addWidget(self.slider12)

        self.languageChange()

        self.resize(QSize(270,173).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("PitchTest"))


    def __tr(self,s,c = None):
        return qApp.translate("pitchtestform",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = pitchtestform()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
