# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/patrick/pksampler-0.3/pksampler/Small/sampleform.ui'
#
# Created: Wed Jun 29 02:39:00 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class SampleForm(QFrame):
    def __init__(self,parent = None,name = None):
        QFrame.__init__(self,parent,name)

        if not name:
            self.setName("SampleForm")

        self.setMinimumSize(QSize(170,360))
        self.setMaximumSize(QSize(180,360))
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)


        self.cueButton = QPushButton(self,"cueButton")
        self.cueButton.setGeometry(QRect(95,305,75,45))

        self.volumeSlider = QSlider(self,"volumeSlider")
        self.volumeSlider.setGeometry(QRect(5,175,45,175))
        self.volumeSlider.setMaxValue(127)
        self.volumeSlider.setOrientation(QSlider.Vertical)

        self.playButton = QPushButton(self,"playButton")
        self.playButton.setGeometry(QRect(95,255,75,45))

        self.deleteButton = QPushButton(self,"deleteButton")
        self.deleteButton.setGeometry(QRect(5,15,75,45))

        self.textLabel = QLabel(self,"textLabel")
        self.textLabel.setGeometry(QRect(85,30,86,16))
        self.textLabel.setPaletteBackgroundColor(QColor(123,247,185))
        self.textLabel.setFrameShape(QLabel.TabWidgetPanel)

        self.loopingButton = QPushButton(self,"loopingButton")
        self.loopingButton.setGeometry(QRect(95,205,75,45))
        self.loopingButton.setToggleButton(1)

        self.titleLabel = QLabel(self,"titleLabel")
        self.titleLabel.setGeometry(QRect(0,0,170,16))

        self.languageChange()

        self.resize(QSize(176,360).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cueButton,SIGNAL("clicked()"),self.slotCue)
        self.connect(self.playButton,SIGNAL("clicked()"),self.slotPlay)
        self.connect(self.volumeSlider,SIGNAL("valueChanged(int)"),self.slotVolume)
        self.connect(self.deleteButton,SIGNAL("clicked()"),self.slotDelete)
        self.connect(self.loopingButton,SIGNAL("toggled(bool)"),self.slotLooping)


    def languageChange(self):
        self.setCaption(self.__tr("SampleForm"))
        self.cueButton.setText(self.__tr("Cue"))
        self.playButton.setText(self.__tr("Play"))
        self.deleteButton.setText(self.__tr("Delete"))
        self.textLabel.setText(self.__tr("0"))
        self.loopingButton.setText(self.__tr("Looping"))
        self.titleLabel.setText(QString.null)


    def slotPlay(self):
        print "SampleForm.slotPlay(): Not implemented yet"

    def slotCue(self):
        print "SampleForm.slotCue(): Not implemented yet"

    def slotVolume(self,a0):
        print "SampleForm.slotVolume(int): Not implemented yet"

    def slotDelete(self):
        print "SampleForm.slotDelete(): Not implemented yet"

    def slotLooping(self,a0):
        print "SampleForm.slotLooping(bool): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("SampleForm",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = SampleForm()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
