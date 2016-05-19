# -*- coding: utf-8 -*-

import os
from qt import *
from newpatchform import PatchForm


class NewPatchDialog(PatchForm):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        PatchForm.__init__(self,parent,name,modal,fl)
        
    def accept(self):
        if not hasattr(self, 'saveFileName'):
            self.slotSaveAs()
    
        if not hasattr(self, 'saveFileName'):
            return
    
        if self.saveFileName:
            self.save(self.saveFileName)
        QDialog.accept(self)
        
    def slotNameChanged(self, qstring):
        self.patchName = str(qstring)
        
    def tooManyFiles(self):
        QMessageBox.information(
                self,
                'Too many Files',
                'You can only add 9 files.',
                QMessageBox.Ok)
        
    def slotAddOne(self):
        if self.filenamesListBox.count() == 9:
            self.tooManyFiles()
            return
            
        fname = QFileDialog.getOpenFileName(
           os.environ['HOME'],
           "Supported Files (*.wav *.ogg)", 
           self,
           "select file dialog", 
           "Select a track")
        if not fname:
            return
       
        if not self.filenamesListBox.findItem(fname):
            self.filenamesListBox.insertItem(fname)
            
    def slotAddMany(self):
        fnames = QFileDialog.getOpenFileNames(
                "Supported Files (*.wav)",
                os.environ['HOME'])
        for fname in fnames:
            if self.filenamesListBox.count() == 9:
                self.tooManyFiles()
                break
            if not self.filenamesListBox.findItem(fname):
                self.filenamesListBox.insertItem(fname)  
              
    def slotRemove(self):
        if not self.filenamesListBox.currentText().isNull():
            index = self.filenamesListBox.currentItem()
        self.filenamesListBox.removeItem(index)
                
    def slotOpen(self):
        fname = QFileDialog.getOpenFileName(
                os.environ['HOME'],
                "Sequencer Patches (*.pkpatch)",
                self,
                "open file dialog",
                "Pick a patch to open")
        if not fname.isNull():
            self.saveFileName = fname.ascii()
            self.load(fname)
            
    def slotSaveAs(self):
        if not self.nameLineEdit.text().isNull():
            fname = self.nameLineEdit.text().ascii() + '.pkpatch'
            initial = os.path.join(os.environ['HOME'], fname)
        else:
            initial = os.environ['HOME']
        fname = QFileDialog.getSaveFileName(
                initial,
                "Sequencer Patches (*.pkpatch)",
                self,
                "save file dialog",
                "Pick a file to save to")
        if not fname.isNull():
            self.saveFileName = fname.ascii()
        
        self.save(self.saveFileName)
        
    def save(self, fname):
        if os.path.isfile(self.saveFileName):
            ret = QMessageBox.question(
                    self,
                    "Overwrite file?",
                    "the file \"%s\" exists, do you want to overwrite it?" % self.saveFileName,
                    QMessageBox.Ok,
                    QMessageBox.Cancel)
            if ret == QMessageBox.Cancel:
                return
        
        if not hasattr(self, 'patchName'):
            self.patchName = ''
        
        self.saveFileName = fname
        if not self.saveFileName[-8:] == '.pkpatch':
            self.saveFileName += '.pkpatch'
        
        f = open(self.saveFileName, "w")
        f.write('tempo %i\n' % self.tempoSpinBox.value())
        f.write('name %s\n' % self.nameLineEdit.text().ascii())
        for i in range(self.filenamesListBox.count()):
            f.write(self.filenamesListBox.text(i).ascii()+'\n')
        
        QMessageBox.information(
                self,
                "File saved sucessfully",
                "File saved sucessfully",
                QMessageBox.Ok)
                
    def load(self, fname):
        fname = str(fname)
        f = open(fname, 'r')
        
        tempo = int(f.readline()[6:])
        self.tempoSpinBox.setValue(tempo)
        
        self.patchName = f.readline()[5:].strip()
        if self.patchName:
            self.nameLineEdit.setText(self.patchName)
        
        self.filenamesListBox.clear()
        for line in f.readlines():
            line = line.replace('\n', '')
            self.filenamesListBox.insertItem(line)
    
    
def main():
    a = QApplication([])
    w = NewPatchDialog()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
        
        
if __name__ == '__main__':
    main()

