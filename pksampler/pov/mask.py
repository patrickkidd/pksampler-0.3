#!/usr/local/bin/python

from qt import QPixmap, QApplication, Qt, bitBlt
import sys
import os

# MASK,LAST_FRAME_INDEX 

BUTTON_MASK = [109,86,50,32]

# generics
button = BUTTON_MASK, 8
tap_button = [108,85,52,50], 8
peak = [129, 13, 8, 167], 127
knob = [109, 67, 54, 53], 127
led = [121, 87, 28,28], 3.1
mixerslider = [120, 14, 30, 173], 127

# originals
search_slider = [47, 90, 172, 23], 127
leddigit = [124, 87, 23, 32], 11
exit_button = [108, 78, 51, 45], 8
pitch_wheel = [119, 44, 36, 112], 25
pitch_center_button = [115,86,40,32], 8
number_button = BUTTON_MASK, 10

masks = {  
    'search_slider' : search_slider,
    'leddigit' : leddigit,
    'exit_button' : exit_button,
    'pitch_wheel' : pitch_wheel,
    'pitch_center_button' : pitch_center_button,
    
    'mixerslider' : mixerslider,
    'outer_mixerslider' : mixerslider,
    
    'led' : led,
    'outer_led' : led,
    
    'reverb_knob' : knob,
    'delay_knob' : knob,
    
    'tap_button' : tap_button,
    'start_button' : tap_button,
    'cue_button' : tap_button,
    
    'button' : button,
    'nudge_up_button' : button,
    'nudge_down_button' : button,
    'pitch_down_button' : button,
    'pitch_up_button' : button,
    'pause_button' : button,
    'loop_button' : button,
    'collapse_button' : button,
    'cue_up_button' : button,
    'cue_down_button' : button,
    'config_button' : button,
    'pk_button' : button,
    'eject_button' : button,
    'save_button' : button,
    'group_button' : button,
    'outer_group_button' : button,
    'auto_group_button' : button,
    'main_zone_button' : button,
    'cue_zone_button' : button,
    'tempo_button' : button,
    'tool_button' : button,
    'group_edit_button' : button,
    'output_button' : button,
    'sequencer_button' : button,

    #'number_button' : number_button,
    
    'peak_module' : peak,
    'outer_peak_module' : peak
}

types = ['bmp','png']
outfile = os.path.join('..','embedded_pixmaps.py')

spinner="\|/-\|/-"
spinpos=0

def update_spinner():
    global spinner, spinpos
    sys.stdout.write("\b"+spinner[spinpos])
    spinpos=(spinpos+1)%8
    sys.stdout.flush()
    
    
def main():
    app = QApplication([])
    did_something = 0
    for name in os.listdir('.'):
    
        if name.find('mask.py') != -1:
            continue
        
        if os.path.isdir(name):
            dirname = name
            try:
                namelist = os.listdir(dirname)
            except:
                print "Couldn't read directory:",dirname
                continue
                
            if dirname in masks:
                print '\nSetting mask for pixmaps in',dirname,'... ',
                for filename in namelist:
                    ext = filename[filename.rfind('.')+1:]
                    base = filename[0:filename.rfind('.')]
                    
                    if ext in types:
                        filepath = os.path.join(dirname, filename)
                        old_p = QPixmap(filepath)
                        
                        if not old_p.isNull() and dirname in masks:
                            name_mask, its = masks[dirname]
                            # don't mask already masked files
                            if old_p.width() > name_mask[2]:
                                new_p = QPixmap(name_mask[2], name_mask[3])
                                bitBlt(new_p, 0,0, old_p, 
                                       name_mask[0], name_mask[1], name_mask[2], name_mask[3], 
                                       Qt.CopyROP)
                                old_p = None
                                new_p.save(filepath, ext.upper(), 100)
                                update_spinner()
                                did_something += 1
    print
    
    if did_something:
        print 'Updated',did_something,'files.'
    else:
        print 'No updates made.'
        
    if '-embed' in sys.argv and not os.path.isfile(outfile):
        print 'Embedding pixmap data into %s... ' % outfile,
        sys.stdout.flush()
        os.system('pyuic -embed pixmaps `find . -name \'*.bmp\'` > %s' % outfile)
        print 'done'

    
if __name__ == '__main__':    
    main()
