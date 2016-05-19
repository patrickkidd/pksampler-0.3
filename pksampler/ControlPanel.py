#!/bin/env python
""" The PKSampler Control Panel """

import Globals
from qt import *
import Widgets
import SampleControl
import SampleWidget
from ControlPanelForm import ControlPanelForm
pkaudio = Globals.getPKAudio()


displayTimer = Globals.DisplayTimer()
conf = Globals.ConfFile()

class ControlPanel(ControlPanelForm):
    """ SIGNALS:
            PYSIGNAL('pathAdded'), (path,)
            PYSIGNAL('pathRemoved'), (path,)
            PYSIGNAL('useGradients'), (bool,)
            PYSIGNAL('mixersChanged'), ()
    """

    def __init__(self, parent=None):
        global conf
        ControlPanelForm.__init__(self, parent, 'PKSampler: Control Panel', 1)
        self.driver = pkaudio.Driver()
        #if conf.getBufferSize() != PK.bufferSize():
        #    PK.setBufferSize(conf.getBufferSize())
        #if conf.getDriver() != PK.getDriver():
        #    PK.setDriver(conf.getDriver())
        
        # Ladspa effects are loaded upon static init, so they go here.
        #for i in range(PK.LadspaPlugin.numPlugins()):
        #    self.effectsListBox.insertItem(PK.LadspaPlugin.pluginName(i))
            
        # DON'T put this in here! (initial values send signals, too!)
        # self.matchUpValues() 
        
    def setDirty(self, qstring=None):
        """ Called when the user changes something. """
        self.buttonApply.setEnabled(True)
                
    def slotAddPath(self):
        """ Pop a dir dialog and add to the list box. """
        homedir = Globals.get_user_home_dir()
        qstring = QFileDialog.getExistingDirectory(homedir, self)
        if qstring.isNull():
            return
        else:
            path = qstring.ascii()
            if path.endswith('/') or path.endswith('\\'):
                path = path[:len(path)-1]
            self.pathListBox.insertItem(path)
            self.buttonApply.setEnabled(1)
            
    def slotRemovePath(self):
        """ Remove the path in the pathListPath """
        path = self.pathListBox.selectedItem().text().ascii()
        self.pathListBox.takeItem(self.pathListBox.selectedItem())
        self.buttonApply.setEnabled(1)
        
    def slotPathSelectionChanged(self):
        """ Update removePathButton. """
        if self.pathListBox.selectedItem():
            self.removePathButton.setEnabled(1)
        else:
            self.removePathButton.setEnabled(0)
            
    def slotMainOutputSelected(self, item):
        if self.driver.numMixers() > 1:
            if item.text().ascii() == self.cueOutputListBox.currentText().ascii():
                new_item = self.cueOutputListBox.selectedItem()
                if new_item and new_item.next():
                    self.cueOutputListBox.setSelected(new_item.next(), 1)
                else:
                    self.cueOutputListBox.setSelected(self.cueOutputListBox.firstItem(), 1)
        self.setDirty()
        
    def slotCueOutputSelected(self, item):
        if self.driver.numMixers() > 1:
            if item.text().ascii() == self.mainOutputListBox.currentText().ascii():
                new_item = self.mainOutputListBox.selectedItem()
                if new_item and new_item.next():
                    self.mainOutputListBox.setSelected(new_item.next(), 1)
                else:
                    self.mainOutputListBox.setSelected(self.mainOutputListBox.firstItem(), 1)
        self.setDirty()
        
    def matchUpValues(self):
        """ Get the widget to reflect stored values. 
            (Don't write any changes here)
        """
        global conf
        
        # driver name
        driverName = conf.getDriver()
        if driverName == '':
            driverName = 'alsa'
        for i in range(self.driverListBox.count()):
            item = self.driverListBox.item(i)
            if driverName == item.text().ascii():
                self.driverListBox.setCurrentItem(item)
                break
        
        # buffer size
        bufferSize = conf.getBufferSize()
        for i in range(self.bufferSizeListBox.count()):
            item = self.bufferSizeListBox.item(i)
            if bufferSize == int(item.text().ascii()):
                self.bufferSizeListBox.setCurrentItem(item)
                break
                
        # Audio devices
        for i in range(self.driver.numMixers()):
            name = self.driver.getMixer(i).name()
            
            # add originals
            if not self.mainOutputListBox.findItem(name):
                self.mainOutputListBox.insertItem(name)
            if not self.cueOutputListBox.findItem(name):
                self.cueOutputListBox.insertItem(name)
                
            if conf.getMainOutput() == name:
                self.mainOutputListBox.setSelected(i, 1)
            if conf.getCueOutput() == name:
                self.cueOutputListBox.setSelected(i, 1)
        
        # Selector Paths
        for path in conf.getSelectorPaths():
            if path != '' and self.pathListBox.findItem(path) == None:
                self.pathListBox.insertItem(path)
                self.emit(PYSIGNAL('pathAdded'), (path,))
                
        # convert from True/False -> 1/0
        self.gradientsCheckBox.setChecked(conf.getUseGradients())

        # animation granularity
        gran = conf.getAnimationGranularity()
        for i in range(self.animationGranularityComboBox.count()):
            g = int(self.animationGranularityComboBox.text(i).ascii())
            if gran == g:
                self.animationGranularityComboBox.setCurrentItem(i)
        Widgets.ANIMATION_CEOF = gran
        
        # Pitch Range
        pitchRange = conf.getPitchRange()
        for i in range(self.pitchComboBox.count()):
            perc = int(self.pitchComboBox.text(i).ascii().replace('%',''))
            if pitchRange == perc:
                self.pitchComboBox.setCurrentItem(i)
        SampleWidget.pitchRange = pitchRange
        
        # display update interval
        interval = conf.getDisplayUpdateInterval()
        self.updateIntervalSlider.setValue(interval)
        
        # use output window
        if int(self.useOutputCheckBox.isChecked()) != conf.getUseOutputWindow():
            self.useOutputCheckBox.setChecked(bool(conf.getUseOutputWindow()))
                    
    def slotApply(self):
        """ Write the configuration to the conf file and to the app. """
        global conf
        if not self.buttonApply.isEnabled():
            return
        
        # buffer size, driver
        if self.bufferSizeListBox.currentText().ascii() != None:
            bufferSize = int(self.bufferSizeListBox.currentText().ascii())
        else:
            bufferSize = Globals.default_buffersize
        if self.driverListBox.currentText().ascii() != None:
            driverName = self.driverListBox.currentText().ascii().lower()
        else:
            driverName = Globals.default_driver_name
            
        # selector paths
        pathsChanged = 0
        listBox_paths = []
        for i in range(self.pathListBox.count()):
            listBox_paths.append(self.pathListBox.text(i).ascii())
        conf_paths = conf.getSelectorPaths()
        added_paths = []
        for path in listBox_paths:
            if not path in conf_paths:
                added_paths.append(path)                
        removed_paths = []
        for path in conf_paths:
            if not path in listBox_paths:
                removed_paths.append(path)
        for path in removed_paths:
            conf.removeSelectorPath(path)
            self.emit(PYSIGNAL('pathRemoved'), (path,))
        for path in added_paths:
            conf.addSelectorPath(path)
            self.emit(PYSIGNAL('pathAdded'), (path,))
            
        # pitch range
        r = int(self.pitchComboBox.currentText().ascii()[:-1])
        SampleWidget.pitchRange = r
        conf.setPitchRange(r)
        
        # output devices (conf values)
        changed = False
        if self.mainOutputListBox.currentText().ascii() != conf.getMainOutput():
            conf.setMainOutput(self.mainOutputListBox.currentText().ascii())
            # find, set main
            for i in range(self.driver.numMixers()):
                if self.driver.getMixer(i).name() == conf.getMainOutput():
                    SampleControl.mainMixer = self.driver.getMixer(i)
                    changed = True
        if self.cueOutputListBox.currentText().ascii() != conf.getCueOutput():
            conf.setCueOutput(self.cueOutputListBox.currentText().ascii())
            # find, set cue
            for i in range(self.driver.numMixers()):
                if self.driver.getMixer(i).name() == conf.getCueOutput():
                    SampleControl.cueMixer = self.driver.getMixer(i)
                    changed = True
        if changed:
            self.emit(PYSIGNAL('mixersChanged'), ())
                    
        # draw gradients
        if self.gradientsCheckBox.isChecked():
            use_gradients = True
        else:
            use_gradients = False
        if use_gradients != Widgets.use_gradients:
            Widgets.use_gradients = use_gradients
            self.emit(PYSIGNAL('useGradients'), (use_gradients,))
        conf.setUseGradients(Widgets.use_gradients)

        # animation granularity
        gran = int(str(self.animationGranularityComboBox.currentText()))
        Widgets.ANIMATION_COEF = gran
        conf.setAnimationGranularity(gran)
        
        # update interval
        interval = self.updateIntervalSlider.value()
        self.slotUpdateInterval(interval)
            
        # use output interval
        conf.setUseOutputWindow(int(self.useOutputCheckBox.isChecked()))
        
        conf.save()
        self.matchUpValues()
        self.buttonApply.setEnabled(0)
        
    def slotUpdateInterval(self, interval):
        global displayTimer, conf
        if interval != displayTimer.getInterval():
            displayTimer.setInterval(interval)
            conf.setDisplayUpdateInterval(interval)
        
        
        
if __name__ == "__main__":
    from qt import *
    a = QApplication([])
    w = ControlPanel()
    w.matchUpValues()
    w.show()
    a.setMainWidget(w)
    a.exec_loop()
    #w.show()
    #a.setMainWidget(w)
    #a.exec_loop()
