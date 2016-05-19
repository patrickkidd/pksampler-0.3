""" Patch.py: a sequencer patch """


class PatchFile:
    """ a collection of samples, a name, and a tempo. """
    
    def __init__(self, patchfile=''):
        self.name = ''
        self.tempo = 137
        self.files = []
        if patchfile:
            self.load(patchfile)
        
    def load(self, patchfile):
        f = open(patchfile, 'r')
        
        tempo = int(f.readline()[6:])
        self.tempo = tempo
        
        patchName = f.readline()[5:].strip()
        if patchName:
            self.name = patchName
        
        for line in f.readlines():
            line = line.replace('\n', '')
            self.addFile(line)
        
    def save(self, patchfile):
    
        if os.path.isfile(patchfile):
            ret = QMessageBox.question(
                        self,
                        "Overwrite file?",
                        "the file \"%s\" exists, do you want to overwrite it?" % self.saveFileName,
                        QMessageBox.Ok,
                        QMessageBox.Cancel)
            if ret == QMessageBox.Cancel:
                return
        
        if not patchfile[-8:] == '.pkpatch':
            patchfile += '.pkpatch'
        
        f = open(patchfile, "w")
        f.write('tempo %i\n' % self.tempo)
        f.write('name %s\n' % self.name)
        for fname in self.files:
            f.write(fname+'\n')
        
        QMessageBox.information(
                self,
                "File saved sucessfully",
                "File saved sucessfully",
                QMessageBox.Ok)
        
    def addFile(self, fname):
        if not fname in self.files:
            self.files.append(fname)
            
    def removeFile(self, fname):
        if fname in self.files:
            self.files.remove(fname)
            
    def getFileNames(self):
        return self.files
        
