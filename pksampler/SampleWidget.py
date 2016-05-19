""" SampleWidget.py: Graphical interfaces to SampleControl objects. """


import fpformat
import thread
from qt import *
import Globals
from Globals import loadPixmap
import Widgets
import PovWidgets
pkaudio = Globals.getPKAudio()
from MidiDialogForm import MidiDialogForm
from Grouping import Group
from SampleControl import SampleControl


POVRAY_DIR = '/usr/home/ajole/src/pksampler/pksampler/pov'
TRACK_HEIGHT = 360


displayTimer = Globals.DisplayTimer()



class MidiDialog(MidiDialogForm):
    def __init__(self, parent=None, name=None, modal=1, f=0):
        MidiDialogForm.__init__(self, parent, name, 1, f)
        self.lastValue = -1 # used to match up the widget to the hardwarep
        
    def showEvent(self, e):
        Group.addMidiListener(self.midiCallback)
        
    def midiCallback(self, data):
        """ called by the sequencer when the dialog is shown. """
        self.channelLineEdit.setText(str(data[0]))
        self.controllerLineEdit.setText(str(data[1]))
        self.lastValue = data[2]
    
    def accept(self):
        Group.removeMidiListener(self.midiCallback)
        QDialog.accept(self)
    
    def reject(self):
        Group.removeMidiListener(self.midiCallback)
        QDialog.reject(self)


class MainDisplay(QFrame):
    """ Displays information about a sample in real-time. """
    
    class TimeDisplay(PovWidgets.LEDDigitDisplay):
        """ Displays frame-time. """

        def __init__(self, parent=None, name=None, f=0):
            PovWidgets.LEDDigitDisplay.__init__(self, 6, parent, name, f)
            self.setCaption('PKSampler: Time Display')

        def setFrame(self, value):
            """ Set the time in kilo-frames. """
            self.setValue(int(value / 1000))
        Globals.psyco_bind(setFrame)
            
    class PitchDisplay(QWidget):
        """ A xx.xx% display of the pitch of a track. """
        def __init__(self, parent=None, name=None, f=0):
            QWidget.__init__(self, parent, name, f)
            
            self.leftDisplay = PovWidgets.LEDDigitDisplay(3, self)
            self.rightDisplay = PovWidgets.LEDDigitDisplay(3, self)
            
            self.leftDisplay.move(0,0)
            self.rightDisplay.move(self.leftDisplay.width()+4, 0)
            self.rightDisplay.justify('right')
            self.rightDisplay.setDefaultDigit(0)
            self.setFixedSize(self.rightDisplay.x()+self.rightDisplay.width(),
                              self.leftDisplay.height())
                              
        def paintEvent(self, e):
            paint = QPainter(self)
            # the background between
            paint.setPen(QColor('black'))
            paint.setBrush(QColor('black'))
            paint.drawRect(self.rightDisplay.x()-5,self.rightDisplay.y(),20, 25)
            # the decimal
            paint.setPen(QColor('green'))
            paint.drawEllipse(self.rightDisplay.x() - 3, 21,2,2)
            QWidget.paintEvent(self, e)
        Globals.psyco_bind(paintEvent)
            
        def setPitch(self, flt):
            """ set a floating point value to the display. """
            sflt = fpformat.fix(flt, 3)
            di = sflt.find('.')
            if sflt[0] == '-':
                left = sflt[1:di]
                neg = 1
            else:
                left = sflt[:di]
                neg = 0
            right = sflt[di+1:di+4]
            self.leftDisplay.setValue(int(left))
            self.rightDisplay.setValue(int(right))
            if neg:
                self.leftDisplay.setValue('-',2)
        Globals.psyco_bind(setPitch)
    
    def __init__(self, sampleControl, parent=None, name=None, f=0):
        QFrame.__init__(self, parent, name, f)
        self.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
        self.setCaption('PKSampler: Main Display')
        self.setFixedSize(180,130)

        self.sampleControl = sampleControl
        QObject.connect(self.sampleControl, PYSIGNAL('pause'),
                        self.slotPause)
        QObject.connect(self.sampleControl, PYSIGNAL('unpause'),
                        self.slotStart)
        QObject.connect(self.sampleControl, PYSIGNAL('cue'),
                        self.slotCue)
        QObject.connect(self.sampleControl, PYSIGNAL('start'),
                        self.slotStart)
        QObject.connect(self.sampleControl, PYSIGNAL('loaded'),
                        self.slotLoaded)
        QObject.connect(self.sampleControl, PYSIGNAL('unloaded'),
                        self.slotUnload)
        QObject.connect(self.sampleControl, PYSIGNAL('pitchChanged'),
                        self.slotPitch)
        
        # Tempo/Pitch labels
        font = QFont()
        font.setPointSize(7)

        self.tempo = -1
        
        # Loaded LED
        #self.loadedLED = PovWidgets.LED('led', 'red', self)
        #self.loadedLED.move(65, 70)
        #self.loadedLEDTimer = QTimer(self)
        #QObject.connect(self.loadedLEDTimer, SIGNAL("timeout()"),
        #                self.loadedLED.stopFlashing)
        
        # Search Slider
        self.searchSlider = PovWidgets.SearchSlider(self)
        self.searchSlider.move(5,self.height() - 25)
        self.searchSlider.setL33t(1)
        self.searchSlider.setValue(0)
        self.searchSlider.setAnimated(0)
        self.connect(self.searchSlider, SIGNAL("valueChanged(int)"),
                     self.slotSearch)
        QToolTip.add(self.searchSlider,
                     'Indicates the player\'s position in the song.\nCan also be used to search.')
        
        # BUTTONS
        
##~         self.upCueButton = PovWidgets.PushButton('cue_up_button','green', self)
##~         self.upCueButton.move(5, 34)
##~         self.connect(self.upCueButton, SIGNAL("clicked()"), self.slotCueUp)
##~         QToolTip.add(self.upCueButton, 'Moves to the next cue points.')
##~         
##~         self.downCueButton = PovWidgets.PushButton('cue_down_button', 'green', self)
##~         self.downCueButton.move(5, 67)
##~         self.connect(self.downCueButton, SIGNAL("clicked()"), self.slotCueDown)
##~         QToolTip.add(self.downCueButton, 'Moves to the previous cue setting')
##~
##~         # current cue box
##~         self.currentCueBox = PovWidgets.LEDDigit(self)
##~         self.currentCueBox.move(65,35)
##~         QToolTip.add(self.currentCueBox, 'Displays the current cue setting')

        self.mainZoneButton = PovWidgets.PushButton('main_zone_button',
                                                    'green',
                                                    self)
        self.mainZoneButton.move(5, 34)
        self.mainZoneButton.setToggleButton(1)
        self.connect(self.mainZoneButton, SIGNAL("toggled(bool)"),
                     self.slotMainZoneToggled)
        self.mainZoneButton.setOn(True) # **after the previous line
        QToolTip.add(self.mainZoneButton, 'Enables the main output zone.')
        
        self.cueZoneButton = PovWidgets.PushButton('cue_zone_button',
                                                   'green',
                                                   self)
        self.cueZoneButton.move(5, 67)
        self.cueZoneButton.setToggleButton(1)
        self.connect(self.cueZoneButton, SIGNAL("toggled(bool)"),
                     self.slotCueZoneToggled)
        self.cueZoneButton.setOn(True) # **after the previous line
        QToolTip.add(self.cueZoneButton, 'Enables the cue output zone.')    

        self.collapseButton = PovWidgets.PushButton('collapse_button',
                                                    'blue',
                                                    self)
        self.collapseButton.move(5, 1)
        QToolTip.add(self.collapseButton, 'Collapses this track.')

        
##~         # current cue box
##~         self.currentCueBox = PovWidgets.LEDDigit(self)
##~         self.currentCueBox.move(65,35)
##~         QToolTip.add(self.currentCueBox, 'Displays the current cue setting')        
        # Time display
        self.timeDisplay = MainDisplay.TimeDisplay(self)
        self.timeDisplay.move(60,4)
        QToolTip.add(self.timeDisplay, 'Displays the time in kilo-frames')   
        
        # Pitch Display
        self.pitchDisplay = MainDisplay.PitchDisplay(self)
        self.pitchDisplay.move(60, 35)
        
        # "drag me" label
        self.dragmeLabel = QLabel(self)
        self.dragmeLabel.setPixmap(loadPixmap('dragme.png'))
        self.dragmeLabel.move(68,67)
        
        # Group button
        self.groupButton = PovWidgets.PushButton('group_button', 'blue', self)
        self.groupButton.setToggleButton(1)
        self.groupButton.move(126,67)
##~         self.groupLED = PovWidgets.LED('led', 'red', self)
##~         self.groupLED.move(90, 70)
##~         self.groupLED.hide()
        
        QObject.connect(self.groupButton, SIGNAL('toggled(bool)'), 
                        self.sampleControl.setGrouped)
##~         QObject.connect(self.sampleControl, PYSIGNAL('grouped'), self.groupLED.setOn)
        QObject.connect(self.sampleControl, PYSIGNAL('grouped'), 
                        self.groupButton.setOn)
        
    def updateDisplay(self):
        """ Check up on the sample. """
        pos = self.sampleControl.pos()
        l = self.sampleControl.getLength()
        self.timeDisplay.setFrame(pos)
        range = self.searchSlider.maxValue() - self.searchSlider.minValue()
        v = int(((pos * 1.0)/ l) * range)
        self.searchSlider.setPixmap(v)
        if self.sampleControl.atEnd() and not self.sampleControl.looping():
            self.sampleControl.slotPause()
           
    def slotLoaded(self):
        """ Turn on the led, init widgets, set the cue points. """
        self.slotCue()
            
    def slotUnload(self):
        """ Called when the sampleControl emits 'unloaded'. """
        global displayTimer
        displayTimer.deregister(self)
        self.timeDisplay.setValue(-1)
            
    def slotCue(self):
        """ Called when the sample is cued. """
        global displayTimer
        if self.sampleControl.isLoaded():
            p = self.sampleControl.pos()
            self.searchSlider.setValue(p)
            self.timeDisplay.setValue(p)
##~             self.loadedLED.stopFlashing()
##~             self.loadedLED.setColor('red')
##~             self.loadedLED.setOn()
        displayTimer.deregister(self)
        
    def slotStart(self):
        """  """
        global displayTimer
        if self.sampleControl.isLoaded():
##~             self.loadedLED.setColor('green')
##~             self.loadedLED.startFlashing()
            displayTimer.register(self)
    
    def slotPause(self):
        global displayTimer
        if self.sampleControl.isLoaded():
            pass
##~             self.loadedLED.stopFlashing()
##~             self.loadedLED.setColor('green')
##~             self.loadedLED.setOn()
        displayTimer.deregister(self)
        

    def slotPitch(self, pitch):
        self.pitchDisplay.setPitch(pitch)
        
    def slotCueUp(self):
        """ increment the selected cue. """
        if self.sampleControl.isLoaded():
            self.sampleControl.slotCuePoint(self.sampleControl.currentCue + 1)
        
    def slotCueDown(self):
        """ Decrement the selected cue. """
        if self.sampleControl.isLoaded():
            self.sampleControl.slotCuePoint(self.sampleControl.currentCue - 1)
        
    def slotSearch(self, v):
        """ Called when the slider is moved. """
        if self.sampleControl.isLoaded():
            pos = int(self.sampleControl.getLength() * (v / 127.0))
            self.sampleControl.slotSearch(pos)
            
    def slotMainZoneToggled(self, a0):
        """ Called when the mainZoneButton is toggled. """
        self.sampleControl.slotSetZone(0,a0)
        
    def slotCueZoneToggled(self, a0):
        """ Called when the cueZoneButton is toggled. """
        self.sampleControl.slotSetZone(1, a0)


class ControlWidget(QFrame):
    """ A 180 x 220 pushbutton play/stop control for a sample. """
    
    def __init__(self, sampleControl, parent=None, name=None, f=0):
        QFrame.__init__(self, parent, name, f)
        self.setCaption('PKSampler: Play Control')
        self.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
        self.setFixedSize(180, 230)
        self.sampleControl = sampleControl
        
        button_defs = (
                # attrname, ctor, pos, color, slotfunc, tooltip
                ('toolButton', PovWidgets.PushButton, (5, 10), 'tool_button', 'red', None, 'Shows/Hides the Tool Widget'),
                ('reverbKnob', PovWidgets.Knob, (69, 0), 'reverb_knob', None, None, 'Reverb'),
                ('delayKnob', PovWidgets.Knob, (124, 0), 'delay_knob', None, None, 'Delay'),
                ('pitchCenterButton', PovWidgets.PushButton, (35, 55), 'pitch_center_button', 'red', self.slotPitchCenter, 'Zeros the pitch'),
                ('nudgeUpButton', PovWidgets.PushButton, (75, 55), 'nudge_up_button', 'red', self.sampleControl.slotNudgeUp, 'Nudges the pitch up'),
                ('nudgeDownButton', PovWidgets.PushButton, (126, 55), 'nudge_down_button', 'red', self.sampleControl.slotNudgeDown, 'Nudges the pitch down'),
                ('pitchUpButton', PovWidgets.PushButton, (75,91), 'pitch_up_button', 'red', None, 'Bends the pitch up'),
                ('pitchDownButton', PovWidgets.PushButton, (126, 91), 'pitch_down_button', 'red', None, 'Bends the pitch down'),
                ('loopButton', PovWidgets.PushButton, (126, 134), 'loop_button', 'green', None, 'Loops the track between cue points'),
                ('pauseButton', PovWidgets.PushButton, (75, 134), 'pause_button', 'blue', self.sampleControl.slotPause, 'Pauses the track'),
                ('cueButton', PovWidgets.TapButton, (75, 177), 'cue_button', 'red', self.sampleControl.slotCue, 'Returns to the cue point and stops'),
                ('startButton', PovWidgets.TapButton, (126, 177), 'start_button', 'green', self.sampleControl.slotStart, 'Starts the track from the current position'),
                )
        for attrname, ctor, pos, pov_dir, color, slotfunc, tooltip in button_defs:
            if color:
                button = ctor(pov_dir, color, self, attrname)
            else:
                button = ctor(pov_dir, self, attrname)
            self.__dict__[attrname] = button
            button.move(*pos)
            if slotfunc:
                self.connect(button, SIGNAL("clicked()"), slotfunc)
            QToolTip.add(button, tooltip)
        
        # volume, pitch
        self.volumeSlider = PovWidgets.MixerSlider('mixerslider', self)
        self.pitchWheel = PovWidgets.VerticalJogWheel('pitch_wheel', self)
        self.volumeSlider.move(5,55)
        self.pitchWheel.move(35,115)
        self.pitchCenterButton.setFixedSize(40,32)
        
        # outs
        QObject.connect(self.pitchUpButton, SIGNAL("pressed()"),
                        self.sampleControl.slotPitchUp)
        QObject.connect(self.pitchUpButton, SIGNAL("released()"),
                        self.sampleControl.slotPitchStop)
        QObject.connect(self.pitchDownButton, SIGNAL("pressed()"),
                        self.sampleControl.slotPitchDown)
        QObject.connect(self.pitchDownButton, SIGNAL("released()"),
                        self.sampleControl.slotPitchStop)
        QObject.connect(self.reverbKnob, SIGNAL('valueChanged(int)'),
                        self.sampleControl.slotReverb)
        QObject.connect(self.delayKnob, SIGNAL('valueChanged(int)'),
                        self.sampleControl.slotDelay)
        self.connect(self.volumeSlider, SIGNAL("valueChanged(int)"),
                     self.sampleControl.slotVolume)
        self.connect(self.volumeSlider, SIGNAL("valueChanged(int)"),
                     self.slotVolume)
        self.connect(self.pitchWheel, PYSIGNAL('moved'),
                     self.slotPitch)
        self.connect(self.loopButton, SIGNAL("toggled(bool)"),
                     self.sampleControl.slotLooping)
        # ins
        QObject.connect(self.sampleControl, PYSIGNAL('loaded'),
                        self.slotLoaded)   

        self.loopButton.setToggleButton(1)
        self.sampleControl.slotLooping(1)
        self.reverbKnob.setValue(64)
        self.delayKnob.setValue(64)

        
    def slotVolume(self, v):
        """ Set the tooltip for the volume value. Called by the slider. """
        QToolTip.remove(self.volumeSlider)
        QToolTip.add(self.volumeSlider, str(127 - v))
        
    def slotPitch(self, delta):
        """ Set the tooltip for the pitch value. Called by the wheel. """
        # convert pixel delta into sensitivity
        pitch = self.sampleControl.getPitch()
        pitch += delta * .05
        self.sampleControl.slotPitch(pitch)
        QToolTip.remove(self.pitchWheel)
        QToolTip.add(self.pitchWheel, str(self.sampleControl.getPitch())+'%')
        
    def slotPitchCenter(self):
        """ Zeros the pitch """
        self.sampleControl.slotPitch(0.0)
        QToolTip.remove(self.pitchWheel)
        QToolTip.add(self.pitchWheel, '0.0%')
        
    def slotLooping(self, a0):
        """ Called when the SampleControl emits 'looping' """
        self.loopButton.setOn(a0)
        
    def slotLoaded(self):
        """ Called when the SampleControl emits 'loaded' """
        if self.sampleControl.looping():
            self.loopButton.setOn(1)
            
        
class CollapsedControlWidget(QWidget):
    """ A Collapsed version of a ControlWidget. """
    def __init__(self, sampleControl, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
        self.setFixedSize(50, 360)
        self.sampleControl = sampleControl
        
        self.collapseButton = PovWidgets.PushButton('collapse_button', 'blue', self)
        self.collapseButton.move(0, 1)
        QToolTip.add(self.collapseButton, 'Expands the track.')
        
        self.volumeSlider = PovWidgets.MixerSlider('mixerslider', self)
        self.volumeSlider.move(11,35)
        self.volumeSlider.setValue(63)
        QObject.connect(self.volumeSlider, SIGNAL("valueChanged(int)"),
                        self.sampleControl.slotVolume)
        #QToolTip.add(self.volumeSlider, 'Controls the volume')
        
        self.leftPeakMeter = PovWidgets.PeakModule('peak_module', 
                self.sampleControl.effectChains[0]['peak'].left, self)
        self.rightPeakMeter = PovWidgets.PeakModule('peak_module', 
                self.sampleControl.effectChains[0]['peak'].right, self)
        self.leftPeakMeter.move(1,34)
        self.rightPeakMeter.move(36,34)
        QObject.connect(self.sampleControl, PYSIGNAL('start'),
                        self.slotStart)
        QObject.connect(self.sampleControl, PYSIGNAL('pause'),
                        self.slotStop)
        QObject.connect(self.sampleControl, PYSIGNAL('unpause'),
                        self.slotStart)
        QObject.connect(self.sampleControl, PYSIGNAL('cue'),
                        self.slotStop)
        
        self.pitchUpButton = PovWidgets.PushButton('pitch_up_button',
                                                   'red',
                                                   self)
        self.pitchUpButton.move(0, 210)
        #QToolTip.add(self.pitchUpButton, 'Bends the pitch up.')
        
        self.pitchDownButton = PovWidgets.PushButton('pitch_down_button',
                                                     'red',
                                                     self)
        self.pitchDownButton.move(0, 243)
        #QToolTip.add(self.pitchDownButton, 'Bends the pitch down.')
        
        QObject.connect(self.pitchUpButton, SIGNAL("pressed()"),
                        self.sampleControl.slotPitchUp)
        QObject.connect(self.pitchUpButton, SIGNAL("released()"),
                        self.sampleControl.slotPitchStop)
        QObject.connect(self.pitchDownButton, SIGNAL("pressed()"),
                        self.sampleControl.slotPitchDown)
        QObject.connect(self.pitchDownButton, SIGNAL("released()"),
                        self.sampleControl.slotPitchStop)
        
        self.pauseButton = PovWidgets.PushButton('pause_button',
                                                 'blue',
                                                 self)
        self.pauseButton.move(0, 276)
        self.connect(self.pauseButton, SIGNAL('clicked()'),
                     self.sampleControl.slotPause)
        #QToolTip.add(self.pauseButton, 'Pauses the sample.')
        
        self.startButton = PovWidgets.TapButton('start_button',
                                                'green',
                                                self)
        self.startButton.move(0, 309)
        #self.connect(self.startButton, SIGNAL('clicked()'),
        #             self.sampleControl.slotStart)
        #QToolTip.add(self.startButton,
        #             'Starts the sample from the beginning.')        
        
    def slotStart(self):
        #self.leftPeakMeter.start()
        #self.rightPeakMeter.start()
        pass
    
    def slotStop(self):
        self.leftPeakMeter.stop()
        self.rightPeakMeter.stop()
        
        
class ToolWidget(QWidget):
    """ Contains utilities like tempo detection and (persistent) sample
        settings.
    """
    
    def __init__(self, sampleControl, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.sampleControl = sampleControl
        self.setFixedSize(180,130)
        self.setPaletteBackgroundColor(Globals.BACKGROUND_COLOR)
        
        self.saveButton = PovWidgets.PushButton('save_button', 'red', self)
        self.saveButton.move(126, 23)
        QObject.connect(self.saveButton, SIGNAL('clicked()'), self.slotSave)
        
        self.tempoButton = PovWidgets.PushButton('tempo_button', 'red', self)
        self.tempoButton.move(5, 95)
        QObject.connect(self.tempoButton, SIGNAL('clicked()'),
                        self.slotDetectTempo)
        
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(60, self.height() - 32, 115, 25)
        self.progressBar.setTotalSteps(100)
        self.progressBar.setEnabled(0)
        
        self.outputLabel = QLabel(self)
        self.outputLabel.resize(80,20)
        self.outputLabel.move(5, 45)
        
        self.pitchUpButton = PovWidgets.PushButton('pitch_up_button',
                                                   'green',
                                                   self)
        self.pitchDownButton = PovWidgets.PushButton('pitch_down_button',
                                                     'green', self)
        self.pitchUpButton.move(75, 59)
        self.pitchDownButton.move(126, 59)
        self.pitchUpButton.setEnabled(0)
        self.pitchDownButton.setEnabled(0)
        QObject.connect(self.pitchUpButton, SIGNAL('clicked()'),
                        self.slotPitchUp)
        QObject.connect(self.pitchDownButton, SIGNAL('clicked()'),
                        self.slotPitchDown)
        
        self.midiButton = PovWidgets.PushButton('pk_button', 'red', self)
        self.midiButton.move(5, 23)
        
        self.unloadButton = PovWidgets.PushButton('eject_button', 'red', self)
        self.unloadButton.move(5, 59)
        
        self.detector = pkaudio.TempoDetector()
        self.detectedTempo = 0.0
        self.detectingTempo = 0
    
    def updateDisplay(self):
        """ Called to check on the tempo detector. """
        progress = self.detector.getProgress()
        if progress < 100:
            self.progressBar.setProgress(progress)
        # done
        else:
            self.killTimers()
            self.detectingTempo = 0
            self.progressBar.setProgress(100)
            self.progressBar.setEnabled(0)
            self.detectedTempo = float(fpformat.fix(self.detectedTempo, 3))
            self.pitchUpButton.setEnabled(1)
            self.pitchDownButton.setEnabled(1)
            self.outputLabel.setText(str(self.detectedTempo)+' bpms')
        
    def slotDetectTempo(self):
        """ Called when the select tempo button is clicked. """
        global displayTimer
        if not self.detectingTempo and self.sampleControl.path:
            self.path = self.sampleControl.path
            self.progressBar.setProgress(0)
            self.progressBar.setEnabled(1)
            self.detectingTempo = 1
            displayTimer.register(self)
            thread.start_new_thread(self.detectionThread, ())
            
        # cancel a detect
        else:
            self.detector.stopDetecting()
            self.progressBar.setEnabled(0)
            self.detectingTempo = 0
            self.pitchUpButton.setEnabled(0)
            self.pitchDownButton.setEnabled(0)
            self.progressBar.setProgress(0)
            self.outputLabel.setText('')
            displayTimer.deregister(self)
            
    def detectionThread(self):
        """ Run in another thread to detect the tempo. """
        self.detectedTempo = self.detector.detect(self.path)
        
    def slotPitchUp(self):
        self.detectedTempo *= 2
        self.outputLabel.setText(str(self.detectedTempo)+' bpms')
        
    def slotPitchDown(self):
        self.detectedTempo /= 2
        self.outputLabel.setText(str(self.detectedTempo)+' bpms')
    
    def slotSave(self):
        conf = Globals.ConfFile()
        conf.writeSampleData(self.sampleControl)
        conf.save()
        
        
class SampleWidget(QWidget):
    """ The main widget for controlling a track.
        SIGNALS:
            PYSIGNAL('collapsed'), ()
            PYSIGNAL('expanded'), ()
            PYSIGNAL('unload'), ()
    """
    
    def __init__(self, parent=None, name=None, f=0):
        QWidget.__init__(self, parent, name, f)
        self.setCaption('PKSampler: Sample')
        
        self.sampleControl = SampleControl()
        QObject.connect(self.sampleControl, PYSIGNAL('unloaded'),
                        self.slotSampleControlUnloaded)

        # Uncollapsed
        self.toolWidget = ToolWidget(self.sampleControl, self)
        self.toolWidget.move(0,0)
        QObject.connect(self.toolWidget.midiButton, SIGNAL('clicked()'), 
                       self.slotMidiDialog)
        
        self.mainDisplay = MainDisplay(self.sampleControl, self)
        self.mainDisplay.show()
        self.mainDisplay.move(0,0)
        QObject.connect(self.mainDisplay.collapseButton, SIGNAL('clicked()'), 
                        self.slotCollapse)
        
        self.controllerWidget = ControlWidget(self.sampleControl, self)
        self.controllerWidget.move(0,self.mainDisplay.height())
        QObject.connect(self.controllerWidget, PYSIGNAL('cue'), 
                        self.mainDisplay.slotCue)
        QObject.connect(self.controllerWidget, PYSIGNAL('playing'), 
                        self.mainDisplay.slotStart)
        QObject.connect(self.controllerWidget, PYSIGNAL('paused'), 
                        self.mainDisplay.slotPause)
        QObject.connect(self.controllerWidget, PYSIGNAL('pitch'), 
                        self.mainDisplay.slotPitch)
       
        # animation timer
        self.animTimer = QTimer(self)
        self.animWidget = self.mainDisplay
        QObject.connect(self.animTimer, SIGNAL('timeout()'), self.slotAnim)
        QObject.connect(self.controllerWidget.toolButton, SIGNAL('clicked()'), 
                        self.slotToolWidget)
        
        # Collapsed
        self.collapsedWidget = CollapsedControlWidget(self.sampleControl, self)
        self.collapsedWidget.hide()
        QObject.connect(self.collapsedWidget.collapseButton,
                        SIGNAL('clicked()'), 
                        self.slotExpand)
        
        # link the volumes
        QObject.connect(self.collapsedWidget.volumeSlider,
                        SIGNAL('valueChanged(int)'), 
                        self.controllerWidget.volumeSlider.setPixmap)
        QObject.connect(self.controllerWidget.volumeSlider,
                        SIGNAL('valueChanged(int)'), 
                        self.collapsedWidget.volumeSlider.setPixmap)
        QObject.connect(self.toolWidget.unloadButton, SIGNAL('clicked()'), 
                        self.slotUnload)
        
        self.slotExpand()
        
    def isLoaded(self):
        return self.sampleControl.isLoaded()
        
    def closeEvent(self, e):
        """ Kill the sample. """
        self.sampleControl.unload()
        QWidget.closeEvent(self, e)

    def slotSampleControlUnloaded(self):
        """ Called when the SampleControl is unloaded. """
        Group.removeAllForTrack(self)

    def slotUnload(self):
        """ Called when the unload button on the toolWidget is clicked, to
            unload the sample.
        """
        if self.sampleControl.isLoaded():
            self.sampleControl.sample.stop()
        self.close() # unloads the sample
        self.emit(PYSIGNAL('unload'), ())
        
    def mouseDoubleClickEvent(self, e):
        self.slotMidiDialog()
        e.accept()
                
    def slotMidiDialog(self):
        """ Pop midi dialog. """
        dialog = MidiDialog(self)
        res = dialog.exec_loop()
        if res == QDialog.Accepted:
            # bind the dialog
            Group.addMidiListener(self.slotMidiVolume,
                                  int(dialog.channelLineEdit.text().ascii()))
            if dialog.lastValue != -1:
                self.slotMidiVolume(dialog.lastValue)
        
    def slotMidiVolume(self, value):
        """ Called when a controller is bound to this volume. """
        anim = self.controllerWidget.volumeSlider.getAnimated()
        self.controllerWidget.volumeSlider.setAnimated(0)
        self.controllerWidget.volumeSlider.setValue(127-value)
        self.controllerWidget.volumeSlider.setAnimated(anim)
        
    def slotCollapse(self):
        self.mainDisplay.hide()
        self.toolWidget.hide()
        self.controllerWidget.hide()
        self.setFixedSize(self.collapsedWidget.size())
        self.collapsedWidget.show()
        self.emit(PYSIGNAL('collapsed'), ())

    def slotExpand(self):
        self.collapsedWidget.hide()
        self.setFixedSize(self.mainDisplay.width(),
                          self.mainDisplay.height()+self.controllerWidget.height())
        self.mainDisplay.show()
        self.toolWidget.show()
        self.controllerWidget.show()
        self.emit(PYSIGNAL('expanded'), ())      
        
    def slotLoad(self, fname=None):
        """ Load a track, just delete the old one. """
        if not fname:
            fname = QFileDialog.getOpenFileName(
                os.environ,
                "Supported Files (*.wav *.ogg)", 
                self,
                "open file dialog", 
                "Select a file")
            if not fname:
                return
        
        fname = QString(fname) # to avoid confusion
        self.sampleControl.load(fname.ascii())
        if self.isLoaded():
            QToolTip.remove(self)
            fi = QFileInfo(fname)
            self.sampleControl.sample.path = fname.ascii()
            QToolTip.add(self, fi.baseName())
            self.controllerWidget.volumeSlider.setValue(64)
            
        else:
            Globals.PrintErr("Filename "+fname.ascii()+" is not valid")

    def slotToolWidget(self):
        """ Called by the tool button. """
        self.animTimer.stop()
        # move tool widget up, down
        if self.animWidget == self.mainDisplay:
            self.animWidget = self.toolWidget
        else:
            self.animWidget = self.mainDisplay
            
        self.animWidget.move(0, self.animWidget.height() * -1)
        self.animWidget.show()
        self.animWidget.raiseW()
        self.animTimer.start(Globals.animInterval)
            
    def slotAnim(self):
        """ Animate the tool/control widget one tick. """
        self.animWidget.move(self.animWidget.x(), self.animWidget.y() + 25)
        # done
        if self.animWidget.y() >= 0:
            self.animWidget.move(0,0)
            self.animTimer.stop()


def main():
    pkaudio = Globals.getPKAudio()
    #pkaudio.start_server()
    pkaudio.connect_to_host(startserver=0)
    a = QApplication([])
    w = SampleWidget()
    w.slotLoad('/home/ajole/wav/track.wav')
    w.show()
    a.setMainWidget(w)
    a.exec_loop()


w2 = None
def test():

    def create():
        global w2
        w2 = SampleWidget()
        w2.slotLoad('/home/ajole/wav/trance.wav')
        w2.sampleControl.slotStart()
        w2.sampleControl.slotSetZone(0, True)
        w2.show()
    
    import pkaudio
    pkaudio.connect_to_host(startserver=1)
    a = QApplication([])

    w1 = SampleWidget(f=Qt.WDestructiveClose)
    w1.slotLoad('/home/ajole/wav/track.wav')
    w1.sampleControl.slotStart()
    w1.sampleControl.slotSetZone(0, True)
    w1.show()

    b = QPushButton('create', None)
    QObject.connect(b,
                    SIGNAL('clicked()'),
                    create)
    b.show()
    a.setMainWidget(b)
    a.exec_loop()
    w1 = None

def test_LoadTest():
    NUM = 5

    from Globals import DisplayTimer
    displayTimer = DisplayTimer()
    displayTimer.setInterval(25)
    a = QApplication([])
    widgets = []
    x = 0
    for i in range(5):
        w = SampleWidget()
        w.slotLoad('/home/ajole/wav/track.wav')
        w.move(x+64, 50)
        w.show()
        widgets.append(w)
        x += w.width()
    a.setMainWidget(widgets[0])
    a.exec_loop()
    
    
if __name__ == "__main__":
    #import profile
    #profile.run('main()')
    #test_LoadTest()
    pass
