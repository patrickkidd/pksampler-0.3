""" A dialog that detects the tempo if a file. """

from qt import *
from TempoDetectorDialogForm import TempoDetectorDialogForm
import PKAudio
from PKAudio import PK
import threading


class DetectionThread(threading.Thread):

    def __init__(self, parent, media):
        threading.Thread.__init__(self)
        
        self.media = media
        self.parent = parent
        self.start()
        
    def run(self):
        """ Do the detection. """
        tempo = self.parent.detector.Detect(self.media)
        if tempo > 0:
            self.parent.FoundTempo(tempo)


class TempoDetectorDialog(TempoDetectorDialogForm):
    """ Signals: PYSIGNAL("accepted"), ()
                 PYSIGNAL("rejected"), ()
                 PYSIGNAL("done"), ()
    """

    def __init__(self, parent=None):
        TempoDetectorDialogForm.__init__(self, parent, "Tempo Detector", 0, Qt.WStyle_Customize | Qt.WStyle_NormalBorder | Qt.WStyle_Title | Qt.WStyle_SysMenu)
        self.detecting = 0
        self.acceptButton.hide()
        self.rejectButton.hide()
        self.cancelButton = QPushButton(self)
        self.cancelButton.setText("&Cancel")
        self.cancelButton.setGeometry(QRect(6,42,274,25))
        self.connect(self.cancelButton, SIGNAL("clicked()"), self.slotCancel)
        
    def Detect(self, path):
        """ Detects the tempo in another thread. """
        self.detecting = 1
        media = PK.CreateMediaLayer(path)
        if media:
            self.detector = PKAudio.TempoDetector()
            QObject.connect(self.detector, PYSIGNAL("progress"), 
                    self.slotProgress)
            self.thread = DetectionThread(self, media)
        else:
            self.setCaption("Internal file error")
            self.textLabel.setText("Invalid file path")
            self.rejectButton.setEnabled(1)
        self.detecting = 0
    
    def FoundTempo(self, tempo):
        self.cancelButton.hide()
        self.acceptButton.show()
        self.rejectButton.show()
        self.tempo = tempo
        self.textLabel.setText("Detected "+str(tempo)+" bpms.\nDoes this sound right?")
        self.acceptButton.setEnabled(1)
        self.rejectButton.setEnabled(1)
        self.multButton.setEnabled(1)
        self.divButton.setEnabled(1)
        
    def closeEvent(self, e):
        e.accept()
        self.detector.StopDetecting()
        TempoDetectorDialogForm.closeEvent(self, e)
        
    def slotCancel(self):
        self.close()
        
    def slotProgress(self):
        """ Update the progress according to the detector. """
        self.progressBar.setProgress(self.detector.GetProgress())
    
    def slotMult2(self):
        self.tempo *= 2
        self.textLabel.setText(str(self.tempo)+"bpms\nDoes this sound right?")
        
    def slotDiv2(self):
        self.tempo /= 2
        self.textLabel.setText(str(self.tempo)+"bpms\nDoes this sound right?")
        
    def slotAccept(self):
        self.accept()
        self.emit(PYSIGNAL("accepted"), ())
        self.emit(PYSIGNAL("done"), ())
        
    def slotReject(self):
        self.reject()
        self.emit(PYSIGNAL("rejected"), ())
        self.emit(PYSIGNAL("done"), ())
        
