# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/patrick/pksampler-0.3/pksampler/ControlPanelForm.ui'
#
# Created: Wed Jun 29 02:38:59 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *

image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x20\x00\x00\x00\x20" \
    "\x08\x06\x00\x00\x00\x73\x7a\x7a\xf4\x00\x00\x09" \
    "\xd6\x49\x44\x41\x54\x58\x85\x75\x97\x5b\x6f\x1b" \
    "\xd7\xb9\x86\x9f\xb5\xd6\x90\x33\x9c\x19\x0e\x49" \
    "\x91\x12\x25\x8a\x52\x6c\x49\x6e\x63\x45\x89\x0d" \
    "\xcb\x70\x63\x37\x4a\xe3\x16\x28\xda\x8d\x8d\x5d" \
    "\x20\xd8\x17\xfd\x09\x01\xfa\x27\xf2\x5b\x72\x59" \
    "\xa0\x17\xbb\xd9\x45\x73\x51\x04\x6d\x53\xc7\x68" \
    "\x82\x04\xa9\x63\xc1\xb2\x64\xd9\x96\x6d\x3a\x3a" \
    "\x99\x1a\x9e\x86\xc3\x39\xad\x5e\xc8\xa6\xa5\xb8" \
    "\x79\x81\xc1\x80\x33\x58\xf3\x3d\xeb\x3b\x2e\x8a" \
    "\x5f\xfd\xef\xbb\x7a\x76\x69\x1e\xc3\x32\x59\x9e" \
    "\x7a\x8b\xcd\xf5\xfb\x6c\x1f\xee\x50\x3f\x53\x25" \
    "\x67\x09\x72\x07\x82\xf6\xe6\x03\x16\x4a\x25\x84" \
    "\xd6\xec\x04\x01\x59\x14\x31\xe5\x79\x84\x49\x42" \
    "\x36\x3d\xcd\xb3\x76\x9b\x62\xb1\x48\xa3\xd1\xc4" \
    "\xf7\x25\xd5\x6a\x13\xdb\xce\x53\x2c\x66\x98\x66" \
    "\xca\x0f\x69\x65\x65\x45\x88\xf9\xa5\x79\xed\x95" \
    "\x3c\x3c\xcb\x63\xed\x9d\x35\x3c\xcf\xe3\xab\x6f" \
    "\xbe\xa2\xed\xb7\x11\x42\xd0\x9c\x69\x62\x48\x83" \
    "\xbd\x56\x0b\x23\x97\xc3\x71\x5d\x4c\xcb\x22\x49" \
    "\x12\xf2\xf9\x3c\xb9\x7c\x1e\xd3\x34\x99\x9a\x9a" \
    "\xc2\xf7\x3b\x7c\xf9\xc5\x37\x1c\x1e\xf6\x28\x57" \
    "\x2a\xe4\xf3\x0a\xab\x90\xe1\xfb\x3e\x96\x65\xb1" \
    "\xf6\xce\x3b\x38\x8e\x33\x06\x98\x9d\x9d\x45\x5c" \
    "\xbf\x7e\x5d\xd7\x6a\x35\x06\x47\x47\xb4\xf7\xf6" \
    "\x78\xf3\xfc\x79\x12\xa5\xe8\x8c\x46\x08\x21\x50" \
    "\xca\xc4\x34\xab\x08\x21\xc9\x32\x49\x2e\xd7\x47" \
    "\x88\x94\xde\xbd\x7b\xbc\x5e\xa9\x20\x72\x39\xfa" \
    "\xa3\x11\x1b\x7b\x7b\xd4\x85\x60\xb5\xd1\x20\xe7" \
    "\x79\xe4\x6a\x35\x36\x46\x23\xfe\xfc\xb7\xbf\x81" \
    "\x10\x44\xa3\x11\xef\xfe\xec\x67\x84\xc3\x21\x7e" \
    "\xa7\x83\x10\x82\xab\x57\xaf\xa2\x6a\x4a\x7d\xb8" \
    "\x6a\x9a\x5c\x36\x4d\xae\xcd\xcd\x31\x15\xc7\xd4" \
    "\xa3\x88\xf2\xf2\x32\x8d\xf9\x79\xee\xdf\x7f\xcc" \
    "\xe6\x66\x80\x6d\x9f\x27\x49\x1c\xe2\xd8\x63\x6e" \
    "\xae\xc8\xcd\x9b\x9f\xf1\xe8\xf1\x63\x6a\x96\x45" \
    "\x39\x9f\xa7\x59\x2c\xb2\xbd\xb7\xc7\xc6\xee\x2e" \
    "\xeb\xed\x36\x87\xad\x16\xd5\x38\xe6\x6c\xb1\x48" \
    "\x43\x4a\x94\x69\xe2\x4e\x4e\xf2\xf9\xcd\x9b\x3c" \
    "\x7e\xfc\x98\x5e\xaf\x47\x96\x65\xa8\xf7\x9a\xcd" \
    "\x0f\xb3\x38\xe6\xf3\xce\x1e\x77\xdc\x90\x8d\xfc" \
    "\x90\xbb\xce\x10\x5d\x33\x28\x15\x2a\x14\x0b\x36" \
    "\xb7\x6f\xff\x93\x7b\x8f\xfe\x41\xee\x47\x7b\x14" \
    "\xa6\x7c\x86\xb9\x1e\x33\x17\xe7\xb1\x8a\x13\x3c" \
    "\xdc\xf7\xb9\xb3\xb9\xc9\x94\x6d\x73\x6d\x79\x99" \
    "\x4b\x93\x93\x9c\xa9\x54\xb8\xdb\x6e\xf3\xcf\xbb" \
    "\x77\xa9\x5b\x16\x6f\x9e\x3b\xc7\xac\xeb\x12\x75" \
    "\x3a\xec\xf8\x3e\xb9\x5c\x8e\x9c\x61\xd0\x6c\x36" \
    "\x11\xe7\x7f\x3c\xa7\xcb\x6f\x4d\x63\x37\x3c\x0c" \
    "\xcb\xc0\xb6\x6d\x0c\x65\x90\x64\x09\x79\x9d\xe7" \
    "\x82\x75\x01\x91\x09\xfe\xf2\xd7\xbf\x70\x6b\xfb" \
    "\x16\xcb\x3f\x5f\xa6\x36\x59\x23\x8e\x63\x74\xa4" \
    "\x99\x97\xf3\x6c\x7e\x75\x9b\xad\xdb\xb7\x39\x3b" \
    "\x35\x85\xed\x38\xf8\xfd\x3e\x83\x20\x60\xe1\xc2" \
    "\x05\xb6\xef\xdc\x41\x67\x19\x8e\xeb\x62\xbb\x2e" \
    "\x6f\xac\xae\x12\xc5\x31\x59\x96\xb1\xbc\xbc\x8c" \
    "\x91\xfb\x71\x85\xc2\x4c\x91\xc0\x0f\x38\xd8\x3e" \
    "\x60\xd4\x1b\x91\x44\x09\x49\x94\xe0\x58\x0e\xcd" \
    "\xff\x6e\x32\x59\x99\x64\xed\xea\x1a\x41\x10\x70" \
    "\xeb\x4f\xb7\x30\x94\x81\x65\x5a\xd8\xb6\xcd\xc4" \
    "\xea\x04\xbf\xf8\xf5\xaf\x79\x6b\x75\x95\x83\xa7" \
    "\x4f\xb1\x6c\x9b\x73\x8e\x83\xe3\xba\x14\x4b\x25" \
    "\xae\xfc\xf4\xa7\xc4\x71\xcc\x70\x38\x64\x30\x18" \
    "\x8c\xaf\x28\x8a\xf0\x7d\x1f\x71\xe5\x57\x57\xf4" \
    "\xda\xdb\x6b\xfc\xe1\xf7\x7f\x60\xd0\x1f\x60\x99" \
    "\x16\x8e\xe3\x90\x37\xf2\x2c\x34\x17\xb8\x74\xe9" \
    "\x12\xb6\x6d\x93\x24\x09\x5a\x6b\x46\xa3\x11\x86" \
    "\x61\xa0\x94\x42\x08\x71\xea\xc3\xbd\x5e\x6f\xfc" \
    "\x71\x21\x04\x00\x42\x08\x0c\xc3\x20\x49\x12\x0c" \
    "\xc3\xc0\xf3\x3c\x1c\xc7\xa1\x56\xab\x1d\x87\x60" \
    "\xe5\xcd\x15\xfd\x93\x2b\x3f\x61\x6e\x6e\x0e\xc7" \
    "\x71\x48\x92\x84\xe1\x70\xc8\xfd\xfb\xf7\x69\xb5" \
    "\x5a\x6c\x6d\x6d\xb1\xb8\xb8\x48\xbd\x5e\x67\x38" \
    "\x1c\x12\xc7\xf1\xb8\x8c\x84\x10\xe4\x72\x39\x94" \
    "\x52\x48\x29\x71\x5d\x17\xdb\xb6\x31\x4d\x13\x21" \
    "\x04\x5a\x6b\x84\x10\x48\x29\x29\x16\x8b\x58\x96" \
    "\x35\x5e\x9b\x65\x19\xf5\x7a\x1d\xd1\x6c\x36\x75" \
    "\x9a\xa6\xd4\xeb\x75\x2e\x5f\xbe\xcc\xf4\xf4\x34" \
    "\x07\x07\x07\xec\xec\xec\xb0\xbe\xbe\x4e\x96\x65" \
    "\x5c\xba\x74\x89\xc5\xc5\x45\xb4\xd6\x63\xc3\x2f" \
    "\xee\x42\x08\x0a\x85\x02\x8e\xe3\x20\xa5\x3c\x65" \
    "\x20\x0c\x43\xba\xdd\x2e\xbd\x5e\x8f\x6e\xb7\xcb" \
    "\x60\x30\x60\x34\x1a\xa1\xb5\xc6\x30\x0c\x2e\x5c" \
    "\xb8\x80\xa8\x56\xab\xfa\xe2\xc5\x8b\xbc\xff\xfe" \
    "\xfb\x7c\xfc\xf1\xc7\xb4\x5a\x2d\x4a\xa5\x12\x52" \
    "\x4a\xb4\xd6\x4c\x4c\x4c\x70\x78\x78\xc8\xea\xea" \
    "\x2a\x67\xce\x9c\x61\xf4\xbc\x3f\x68\xad\x19\x0e" \
    "\x87\xf4\x7a\xbd\xb1\x81\x6e\xb7\xcb\x70\x38\x44" \
    "\x6b\x8d\x52\x0a\xcb\xb2\xf0\x3c\x0f\xd7\x75\xc7" \
    "\xd0\x52\xca\x31\xe8\xe2\xe2\x22\x62\x6d\x6d\x4d" \
    "\xe7\x72\x39\xae\x5c\xb9\xc2\xc2\xc2\x02\x49\x92" \
    "\xd0\x6e\xb7\x09\xc3\x10\x80\xad\xad\x2d\xa2\x28" \
    "\xe2\xdb\x6f\xbf\x25\x0c\x43\xe6\xe6\xe6\xc6\x3b" \
    "\xb7\x6d\x9b\x62\xb1\x48\xa9\x54\xa2\x50\x28\x90" \
    "\x24\x09\x69\x9a\xa2\x94\x42\x6b\x3d\xde\x84\x52" \
    "\x0a\xcf\xf3\x28\x16\x8b\x18\x86\x71\xaa\x13\x1a" \
    "\x8d\x46\x83\xf5\xf5\x75\x3e\xfa\xe8\x23\x0c\xc3" \
    "\xe0\x83\x0f\x3e\xc0\x34\x4d\x3c\xcf\x63\x7b\x7b" \
    "\x1b\xdb\xb6\xb9\x7b\xf7\x2e\x83\xc1\x00\x80\xf9" \
    "\xf9\x79\x5c\xd7\x3d\x15\x8a\x17\xa1\xa9\xd5\x6a" \
    "\x78\x9e\x37\x36\x90\x24\x92\xd1\x48\x11\x86\x8a" \
    "\x20\x50\xf8\xbe\xa0\x50\x48\x99\x9c\x0c\x51\x4a" \
    "\x33\xe8\xf7\x11\x2b\x2b\x2b\xba\xd3\xe9\x90\x24" \
    "\xc9\x78\xe1\xc2\xc2\x02\xc3\xe1\x10\xc3\x30\xd8" \
    "\xdd\xdd\x25\x49\x12\x94\x52\xd4\x6a\x35\x7e\xf1" \
    "\xde\x7b\x4c\x97\xcb\xe4\x47\x23\x54\x92\x30\x28" \
    "\x97\xc9\x4e\xc4\x1e\x20\x8e\x63\xfe\xf8\xc7\xaf" \
    "\xa9\xd7\xaf\x91\xcf\xbf\x80\x4d\x51\x6a\x84\x61" \
    "\x44\x28\x65\x30\x3d\x6d\xd0\x98\x01\x23\x4d\x53" \
    "\xd2\x34\x1d\x97\x8b\xeb\xba\x58\x96\x45\xa3\xd1" \
    "\xa0\x54\x2a\xf1\xf6\x1b\x6f\x50\x3c\x3a\xa2\x66" \
    "\x18\x94\x0d\x83\x7c\xab\x85\x78\xf4\x08\xad\x35" \
    "\x1a\x70\xca\x65\xf6\x97\x96\x4e\x41\x3c\x7d\xba" \
    "\xcb\xe6\xe6\x97\x3c\x79\x72\x8f\xd7\x5f\xff\x2f" \
    "\xaa\xd5\x06\xa6\x19\x90\x65\x26\x49\x72\x5c\x69" \
    "\xad\x56\x48\xb9\xfc\x1a\xc6\xd9\xb3\x67\xa9\xd5" \
    "\x6a\x14\x0a\x05\xaa\xd5\x2a\xae\xeb\x22\xa5\x44" \
    "\x04\x01\xf2\xc1\x03\xb2\xdd\x5d\x0c\x21\xa8\x3a" \
    "\x0e\x32\xcb\x18\x15\x0a\x84\xae\x8b\x00\x72\x83" \
    "\x01\x96\xef\x33\xb5\xbd\xcd\xde\xd2\x12\x7a\x9c" \
    "\x68\xe0\xba\x16\xfd\xfe\x11\xff\xfa\xd7\xef\x59" \
    "\x5c\x7c\x97\x66\xf3\x32\x96\x15\x52\x28\x0c\x49" \
    "\x53\x93\x38\x2e\x32\x18\x58\xa8\x6b\xd7\xae\x7d" \
    "\xb8\xbc\xbc\x4c\xa5\x52\xc1\x34\x4d\xe4\x68\x84" \
    "\xda\xda\x42\x6f\x6c\x90\x76\xbb\x64\x5a\x93\x6a" \
    "\x8d\x00\x4c\xa5\x30\xd2\x94\xe2\xf4\x34\x59\xa5" \
    "\x42\x2f\x08\x18\xe4\xf3\xc4\x51\x44\x65\x30\x20" \
    "\xa8\x54\x40\x08\x3c\xcf\x63\x62\xc2\x63\x77\x77" \
    "\x8f\x20\x08\x79\xf6\xec\x01\x41\xd0\xa6\x5c\x3e" \
    "\x47\x9a\x7a\x24\x49\x1e\x50\xd4\xeb\x1e\x06\xc0" \
    "\x68\x34\xe2\xf1\xf6\x36\x8b\x5a\x23\xf7\xf7\x8f" \
    "\xbb\xde\xf7\x0e\x0f\xfd\x28\xa2\x90\xcb\x51\x5c" \
    "\x5a\xc2\x9d\x9d\x25\xfa\xec\x33\x6a\xcf\x93\x2f" \
    "\x55\x0a\xd9\x6e\x33\x25\x04\xfb\x67\xcf\x82\x10" \
    "\x2c\x2d\x2d\x61\x59\x16\x9f\x7e\xfa\x19\x4f\x9f" \
    "\xb6\xd9\xdb\xbb\x43\x10\x3c\xe3\x37\xbf\xf9\x1d" \
    "\xab\xab\x17\xf1\x3c\x97\x4a\xc5\x42\x5d\xbc\x78" \
    "\xf1\x43\x21\x04\x1b\x9f\x7e\xca\x82\x94\x64\x59" \
    "\xc6\x7f\x92\x06\xd2\x2c\x23\xdf\xef\x13\x3c\x7c" \
    "\x08\xcf\x73\x40\x0b\x81\x12\x02\xd3\xb2\x98\x2c" \
    "\x16\xb1\x1d\x87\x23\x29\x11\x42\x50\x2a\x95\x98" \
    "\x99\x99\xa2\xdb\xf5\xf1\xfd\x3e\xa3\xd1\x80\xcd" \
    "\xcd\x2f\xe9\xf5\x8e\xf8\xe4\x93\xff\x63\x73\xf3" \
    "\xcb\x63\x0f\x54\xab\x55\xf6\xc3\x90\x24\xcb\x30" \
    "\xbe\x97\xd1\x27\x15\xc4\x31\xbd\xd1\x88\xa2\x6d" \
    "\x63\x3b\x0e\xb5\x7a\x9d\x6a\xa3\x81\xe1\x79\xf4" \
    "\xb2\x8c\x56\xbb\xcd\x93\xed\x6d\xd2\x7a\x1d\x55" \
    "\x28\x00\x50\xaf\xd7\xf9\xe5\x2f\x7f\xce\x8d\x1b" \
    "\x9f\xb3\xbe\xfe\x90\x30\x1c\xf0\xf7\xbf\x7f\x0c" \
    "\x40\xa5\xb2\x7a\x0c\x60\x18\x06\xa1\x52\xf4\xa3" \
    "\x88\xf2\x89\x7e\xfd\x42\x99\xd6\xa4\x59\x46\x94" \
    "\xa6\xf4\x92\x84\xf3\x33\x33\x1c\x66\x19\x5f\xdf" \
    "\xbe\xcd\xd6\x27\x9f\xb0\xeb\xfb\x74\xc2\x90\x20" \
    "\x8e\x89\xb3\x8c\xff\xf9\xed\x6f\x69\x9c\x39\x33" \
    "\x5e\x5f\x2e\x97\xb9\x7e\xfd\x3d\xca\xe5\x6f\xf8" \
    "\xfa\xeb\x75\xc2\x30\xc6\xb6\x2d\x66\x66\x6a\x8c" \
    "\xdb\xd2\x74\xb3\xc9\xd3\x6e\xf7\x14\x80\x7e\x9e" \
    "\x80\x71\x9a\xd2\x8f\x22\xf6\x06\x03\x1e\xfa\x3e" \
    "\xff\xbf\xb1\xc1\x28\x49\x88\xb2\x6c\xdc\x84\x4e" \
    "\xca\xef\x74\x68\x7c\xef\x99\x6d\xdb\x5c\xbd\xfa" \
    "\x36\x2b\x2b\x6f\x10\x45\x11\x8e\xe3\xb0\xb8\xb8" \
    "\xf8\x12\x60\x6e\x6e\x8e\x87\x37\x6e\xf0\x7a\xad" \
    "\x86\x78\xbe\xeb\x38\xcb\x08\xe2\x98\xc3\x20\xe0" \
    "\x81\xef\xd3\xea\x76\x89\xd2\x1f\x3e\xe5\x02\x48" \
    "\xc3\xe0\xf1\xfe\x13\x9a\xc6\x59\x02\x19\x60\x67" \
    "\x36\x5e\x72\xdc\x1d\xa5\x94\x94\x4a\xa5\x97\x9e" \
    "\xcd\xb2\xd3\x00\x37\x3a\x1d\xa2\x34\x45\x00\x61" \
    "\x92\xd0\x0e\x43\x1e\xf9\x3e\x3b\x9d\x0e\xc1\x89" \
    "\x31\x7c\x52\xca\xcc\xe3\x36\x4a\x14\xe7\xca\xb8" \
    "\xcd\x32\xee\xac\x87\xe1\x18\x6c\xe9\x2d\xd0\x20" \
    "\xa4\xa0\x91\x6f\x30\x1d\x4d\xbf\xb2\x76\x30\x18" \
    "\xbc\x04\x98\x98\x98\x60\x28\x25\xbb\xfd\x3e\x4a" \
    "\x08\x5a\xbd\x1e\x0f\x7c\x9f\x6e\x18\x8e\x4b\x52" \
    "\x2a\x45\xce\xb2\x28\x78\x45\xec\x39\x8f\xf2\xf2" \
    "\x04\xc5\x39\x0f\xe4\xf3\x79\xa0\x41\x20\x20\x03" \
    "\x29\x24\x42\x1e\x0f\xad\x7d\xb1\x0f\x79\x5e\x81" \
    "\x70\x1c\xe7\x25\x00\xc0\x54\xa3\xc1\x17\xad\x16" \
    "\x4a\x08\xfc\x38\xc6\xab\x54\xf8\xd1\xb9\x73\x14" \
    "\x2b\x15\x1c\xcf\xc3\xb2\x6d\x28\xc0\x81\x79\xc0" \
    "\x50\x0c\xd1\x02\x92\x38\x41\x19\x6a\x3c\x21\x5f" \
    "\x5c\x27\x01\x84\x10\x3c\x53\xcf\x90\x48\xa6\xa2" \
    "\xa9\xb1\x3d\xc3\x30\x4e\x03\x5c\xbf\x7e\x9d\xfd" \
    "\x56\x8b\xe9\x99\x19\x6a\xf5\x3a\x79\xd3\x1c\xbf" \
    "\x4b\x48\xd8\x89\x76\x78\x12\x3c\x21\x89\x13\x74" \
    "\x76\xec\x97\x51\x7f\x84\x53\x76\x8e\x0d\x0a\x81" \
    "\x90\x2f\x8d\x9f\xbc\xcb\x4c\x72\xa4\x8e\x10\x79" \
    "\xc1\x64\x34\xf9\x12\xe2\x24\x40\xb3\xd9\xa4\xd9" \
    "\x6c\x9e\x72\x93\x46\xb3\x97\xec\x71\x7f\x78\x9f" \
    "\x70\x14\x92\xbd\xc8\xfc\xe7\x71\x89\x86\x11\x66" \
    "\xc1\xc4\xb4\xcd\xe3\x19\x22\x8f\x8f\x60\x52\xc8" \
    "\x53\xbf\x2f\x57\x2e\x33\xec\x0f\x59\x8f\xd7\x91" \
    "\x3d\x49\x35\xaa\xbe\x0a\x30\x36\xaa\x35\x47\x47" \
    "\x47\x74\xb2\x0e\x47\xf6\x11\x7e\xe8\x93\x25\x19" \
    "\x68\x5e\x29\x3b\x9d\x69\x82\x6e\x80\x69\x9b\x98" \
    "\xd2\x44\xfa\x92\xb4\x98\x22\x0b\x12\xa9\x8e\x21" \
    "\x4c\x69\xb2\xd2\x58\xe1\xc6\x77\x37\x28\x0c\x0b" \
    "\xf4\x8c\x1e\xe2\x48\x30\xcb\xec\xab\x00\x77\xee" \
    "\xdc\xe1\xe6\x17\x37\x99\xb8\x30\x41\xe9\xb5\x12" \
    "\xd9\x20\x43\x67\xfa\x3f\xd6\xfb\x0b\xa5\x71\xca" \
    "\xb0\x37\xc4\x9d\x72\x69\xcc\x34\x30\x7a\x06\xe1" \
    "\x41\x48\x47\x77\xc8\x4a\x19\xf3\xf5\x79\x94\x52" \
    "\x1c\x26\x87\xe4\x9f\xff\x97\x0c\x8c\x00\x3f\xef" \
    "\xbf\x0a\xb0\xbb\xbb\x8b\xf6\x34\xee\x8c\x4b\x1a" \
    "\xa7\xa7\xdc\xfd\x43\xd2\xfa\xd8\x0b\x81\x17\xd0" \
    "\xb2\x5b\xa8\x92\xc2\x9d\x74\x99\x51\x33\xa8\x9e" \
    "\xa2\xa9\x9a\x3c\x09\x9e\xa0\x72\x8a\x9c\xcc\x21" \
    "\xa4\xc0\x32\x2d\xb4\xa3\x31\xbe\xfb\xee\xbb\x53" \
    "\xa7\xd9\x28\x8a\x38\x6a\x1d\x51\xb8\x57\x40\xaa" \
    "\x1f\x9e\x0b\xaf\x48\x40\x6f\xb7\x47\xb9\x56\xc6" \
    "\x30\x0c\xa4\x94\x28\xa5\x50\x4a\x71\xab\x75\xeb" \
    "\xd8\x86\xe4\x65\x72\x0a\x81\x7c\x4d\xf2\x6f\xc9" \
    "\xcd\x66\xe0\x2f\x28\xf3\x75\x00\x00\x00\x00\x49" \
    "\x45\x4e\x44\xae\x42\x60\x82"

class ControlPanelForm(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("ControlPanelForm")

        self.setIcon(self.image0)
        self.setSizeGripEnabled(0)
        self.setModal(1)

        ControlPanelFormLayout = QVBoxLayout(self,6,5,"ControlPanelFormLayout")

        self.tabWidget2 = QTabWidget(self,"tabWidget2")

        self.tab = QWidget(self.tabWidget2,"tab")
        tabLayout = QVBoxLayout(self.tab,6,6,"tabLayout")

        self.groupBox2 = QGroupBox(self.tab,"groupBox2")
        self.groupBox2.setLineWidth(2)
        self.groupBox2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2.layout().setSpacing(6)
        self.groupBox2.layout().setMargin(6)
        groupBox2Layout = QGridLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(Qt.AlignTop)
        spacer2 = QSpacerItem(170,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox2Layout.addItem(spacer2,1,0)

        self.pathListBox = QListBox(self.groupBox2,"pathListBox")

        groupBox2Layout.addMultiCellWidget(self.pathListBox,0,0,0,2)

        self.removePathButton = QPushButton(self.groupBox2,"removePathButton")
        self.removePathButton.setEnabled(0)

        groupBox2Layout.addWidget(self.removePathButton,1,1)

        self.addPathButton = QPushButton(self.groupBox2,"addPathButton")

        groupBox2Layout.addWidget(self.addPathButton,1,2)
        tabLayout.addWidget(self.groupBox2)

        layout7 = QHBoxLayout(None,0,6,"layout7")

        layout6 = QHBoxLayout(None,0,6,"layout6")

        self.textLabel1_6 = QLabel(self.tab,"textLabel1_6")
        layout6.addWidget(self.textLabel1_6)

        self.animationGranularityComboBox = QComboBox(0,self.tab,"animationGranularityComboBox")
        layout6.addWidget(self.animationGranularityComboBox)
        layout7.addLayout(layout6)
        spacer3 = QSpacerItem(90,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout7.addItem(spacer3)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.textLabel1_2 = QLabel(self.tab,"textLabel1_2")
        layout2.addWidget(self.textLabel1_2)

        self.pitchComboBox = QComboBox(0,self.tab,"pitchComboBox")
        layout2.addWidget(self.pitchComboBox)
        layout7.addLayout(layout2)
        tabLayout.addLayout(layout7)

        self.groupBox4 = QGroupBox(self.tab,"groupBox4")
        self.groupBox4.setColumnLayout(0,Qt.Vertical)
        self.groupBox4.layout().setSpacing(6)
        self.groupBox4.layout().setMargin(6)
        groupBox4Layout = QVBoxLayout(self.groupBox4.layout())
        groupBox4Layout.setAlignment(Qt.AlignTop)

        layout5 = QHBoxLayout(None,0,6,"layout5")

        self.gradientsCheckBox = QCheckBox(self.groupBox4,"gradientsCheckBox")
        layout5.addWidget(self.gradientsCheckBox)
        spacer7 = QSpacerItem(116,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout5.addItem(spacer7)

        self.useOutputCheckBox = QCheckBox(self.groupBox4,"useOutputCheckBox")
        layout5.addWidget(self.useOutputCheckBox)
        groupBox4Layout.addLayout(layout5)

        layout4 = QVBoxLayout(None,0,6,"layout4")

        self.updateIntervalSlider = QSlider(self.groupBox4,"updateIntervalSlider")
        self.updateIntervalSlider.setMaxValue(500)
        self.updateIntervalSlider.setValue(100)
        self.updateIntervalSlider.setOrientation(QSlider.Horizontal)
        self.updateIntervalSlider.setTickmarks(QSlider.Below)
        self.updateIntervalSlider.setTickInterval(50)
        layout4.addWidget(self.updateIntervalSlider)

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.textLabel2_4 = QLabel(self.groupBox4,"textLabel2_4")
        layout3.addWidget(self.textLabel2_4)
        spacer4 = QSpacerItem(61,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout3.addItem(spacer4)

        self.textLabel1_5 = QLabel(self.groupBox4,"textLabel1_5")
        layout3.addWidget(self.textLabel1_5)
        spacer5 = QSpacerItem(61,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout3.addItem(spacer5)

        self.textLabel3 = QLabel(self.groupBox4,"textLabel3")
        layout3.addWidget(self.textLabel3)
        layout4.addLayout(layout3)
        groupBox4Layout.addLayout(layout4)
        tabLayout.addWidget(self.groupBox4)
        self.tabWidget2.insertTab(self.tab,QString.fromLatin1(""))

        self.tab_2 = QWidget(self.tabWidget2,"tab_2")
        tabLayout_2 = QVBoxLayout(self.tab_2,6,6,"tabLayout_2")

        self.groupBox1 = QGroupBox(self.tab_2,"groupBox1")
        self.groupBox1.setEnabled(0)
        self.groupBox1.setLineWidth(2)
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(6)
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        self.textLabel2 = QLabel(self.groupBox1,"textLabel2")
        self.textLabel2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.textLabel2.sizePolicy().hasHeightForWidth()))

        groupBox1Layout.addWidget(self.textLabel2,0,1)

        self.bufferSizeListBox = QListBox(self.groupBox1,"bufferSizeListBox")
        self.bufferSizeListBox.setEnabled(0)
        self.bufferSizeListBox.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.bufferSizeListBox.sizePolicy().hasHeightForWidth()))
        self.bufferSizeListBox.setFrameShape(QListBox.StyledPanel)

        groupBox1Layout.addWidget(self.bufferSizeListBox,1,1)

        self.textLabel1 = QLabel(self.groupBox1,"textLabel1")
        self.textLabel1.setPaletteForegroundColor(QColor(255,0,0))

        groupBox1Layout.addWidget(self.textLabel1,0,0)

        self.driverListBox = QListBox(self.groupBox1,"driverListBox")

        groupBox1Layout.addWidget(self.driverListBox,1,0)
        tabLayout_2.addWidget(self.groupBox1)

        self.groupBox3 = QGroupBox(self.tab_2,"groupBox3")
        self.groupBox3.setLineWidth(2)
        self.groupBox3.setColumnLayout(0,Qt.Vertical)
        self.groupBox3.layout().setSpacing(6)
        self.groupBox3.layout().setMargin(6)
        groupBox3Layout = QGridLayout(self.groupBox3.layout())
        groupBox3Layout.setAlignment(Qt.AlignTop)

        self.cueOutputListBox = QListBox(self.groupBox3,"cueOutputListBox")

        groupBox3Layout.addWidget(self.cueOutputListBox,2,1)

        self.mainOutputListBox = QListBox(self.groupBox3,"mainOutputListBox")

        groupBox3Layout.addWidget(self.mainOutputListBox,2,0)

        self.textLabel2_2 = QLabel(self.groupBox3,"textLabel2_2")

        groupBox3Layout.addWidget(self.textLabel2_2,1,1)

        self.textLabel1_3 = QLabel(self.groupBox3,"textLabel1_3")

        groupBox3Layout.addWidget(self.textLabel1_3,1,0)

        self.textLabel2_3 = QLabel(self.groupBox3,"textLabel2_3")

        groupBox3Layout.addMultiCellWidget(self.textLabel2_3,0,0,0,1)
        tabLayout_2.addWidget(self.groupBox3)
        self.tabWidget2.insertTab(self.tab_2,QString.fromLatin1(""))

        self.TabPage = QWidget(self.tabWidget2,"TabPage")
        TabPageLayout = QVBoxLayout(self.TabPage,6,6,"TabPageLayout")

        self.textLabel1_4 = QLabel(self.TabPage,"textLabel1_4")
        TabPageLayout.addWidget(self.textLabel1_4)

        self.effectsListBox = QListBox(self.TabPage,"effectsListBox")
        self.effectsListBox.setSelectionMode(QListBox.NoSelection)
        TabPageLayout.addWidget(self.effectsListBox)
        self.tabWidget2.insertTab(self.TabPage,QString.fromLatin1(""))
        ControlPanelFormLayout.addWidget(self.tabWidget2)

        layout4_2 = QHBoxLayout(None,0,6,"layout4_2")
        Horizontal_Spacing2 = QSpacerItem(198,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout4_2.addItem(Horizontal_Spacing2)

        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        layout4_2.addWidget(self.buttonOk)

        self.buttonApply = QPushButton(self,"buttonApply")
        self.buttonApply.setEnabled(0)
        layout4_2.addWidget(self.buttonApply)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        layout4_2.addWidget(self.buttonCancel)
        ControlPanelFormLayout.addLayout(layout4_2)

        self.languageChange()

        self.resize(QSize(441,393).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.buttonApply,SIGNAL("clicked()"),self.slotApply)
        self.connect(self.gradientsCheckBox,SIGNAL("toggled(bool)"),self.setDirty)
        self.connect(self.pitchComboBox,SIGNAL("activated(const QString&)"),self.setDirty)
        self.connect(self.pathListBox,SIGNAL("selectionChanged()"),self.slotPathSelectionChanged)
        self.connect(self.removePathButton,SIGNAL("clicked()"),self.slotRemovePath)
        self.connect(self.addPathButton,SIGNAL("clicked()"),self.slotAddPath)
        self.connect(self.buttonOk,SIGNAL("clicked()"),self.accept)
        self.connect(self.buttonOk,SIGNAL("clicked()"),self.slotApply)
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self.reject)
        self.connect(self.bufferSizeListBox,SIGNAL("highlighted(const QString&)"),self.setDirty)
        self.connect(self.driverListBox,SIGNAL("highlighted(const QString&)"),self.setDirty)
        self.connect(self.mainOutputListBox,SIGNAL("selectionChanged(QListBoxItem*)"),self.slotMainOutputSelected)
        self.connect(self.cueOutputListBox,SIGNAL("selectionChanged(QListBoxItem*)"),self.slotCueOutputSelected)
        self.connect(self.updateIntervalSlider,SIGNAL("sliderMoved(int)"),self.setDirty)
        self.connect(self.useOutputCheckBox,SIGNAL("stateChanged(int)"),self.setDirty)
        self.connect(self.updateIntervalSlider,SIGNAL("valueChanged(int)"),self.slotUpdateInterval)
        self.connect(self.animationGranularityComboBox,SIGNAL("activated(const QString&)"),self.setDirty)


    def languageChange(self):
        self.setCaption(self.__tr("PKSampler: Control Panel"))
        self.groupBox2.setTitle(self.__tr("Selector Paths"))
        self.removePathButton.setText(self.__tr("Remove"))
        self.addPathButton.setText(self.__tr("Add..."))
        self.textLabel1_6.setText(self.__tr("Animation granularity\n"
"(more = faster)"))
        self.animationGranularityComboBox.clear()
        self.animationGranularityComboBox.insertItem(self.__tr("1"))
        self.animationGranularityComboBox.insertItem(self.__tr("2"))
        self.animationGranularityComboBox.insertItem(self.__tr("3"))
        self.animationGranularityComboBox.insertItem(self.__tr("4"))
        self.animationGranularityComboBox.insertItem(self.__tr("6"))
        self.animationGranularityComboBox.insertItem(self.__tr("8"))
        self.textLabel1_2.setText(self.__tr("Pitch Max"))
        self.pitchComboBox.clear()
        self.pitchComboBox.insertItem(self.__tr("8%"))
        self.pitchComboBox.insertItem(self.__tr("12%"))
        self.pitchComboBox.insertItem(self.__tr("24%"))
        self.pitchComboBox.insertItem(self.__tr("100%"))
        self.groupBox4.setTitle(self.__tr("User Interface"))
        self.gradientsCheckBox.setText(self.__tr("Draw Gradients"))
        self.useOutputCheckBox.setText(self.__tr("Use Output Window"))
        QToolTip.add(self.updateIntervalSlider,self.__tr("Adjusts the display interval for all user interface components"))
        self.textLabel2_4.setText(self.__tr("Faster (0ms)"))
        self.textLabel1_5.setText(self.__tr("GUI Update interval"))
        self.textLabel3.setText(self.__tr("Slower (500ms)"))
        self.tabWidget2.changeTab(self.tab,self.__tr("General"))
        self.groupBox1.setTitle(self.__tr("Driver"))
        self.textLabel2.setText(self.__tr("Buffer Size (bytes)"))
        self.bufferSizeListBox.clear()
        self.bufferSizeListBox.insertItem(self.__tr("256"))
        self.bufferSizeListBox.insertItem(self.__tr("512"))
        self.bufferSizeListBox.insertItem(self.__tr("1024"))
        self.bufferSizeListBox.insertItem(self.__tr("2048"))
        self.bufferSizeListBox.insertItem(self.__tr("4096"))
        self.textLabel1.setText(self.__tr("<u>You may need to restart the application for these.</u>"))
        self.driverListBox.clear()
        self.driverListBox.insertItem(self.__tr("alsa"))
        self.driverListBox.insertItem(self.__tr("arts"))
        self.driverListBox.insertItem(self.__tr("devdsp"))
        self.driverListBox.insertItem(self.__tr("null"))
        self.groupBox3.setTitle(self.__tr("Outputs"))
        self.textLabel2_2.setText(self.__tr("Cue"))
        self.textLabel1_3.setText(self.__tr("Main"))
        self.textLabel2_3.setText(self.__tr("Select the audio devices to be used for the main and cue zones."))
        self.tabWidget2.changeTab(self.tab_2,self.__tr("Audio Devices"))
        self.textLabel1_4.setText(self.__tr("Detected LadspaPlugins. These plugins cannot be used yet."))
        self.tabWidget2.changeTab(self.TabPage,self.__tr("Effects"))
        self.buttonOk.setText(self.__tr("&OK"))
        self.buttonOk.setAccel(QString.null)
        self.buttonApply.setText(self.__tr("A&pply"))
        self.buttonApply.setAccel(self.__tr("Alt+P"))
        self.buttonCancel.setText(self.__tr("&Cancel"))
        self.buttonCancel.setAccel(QString.null)


    def slotApply(self):
        print "ControlPanelForm.slotApply(): Not implemented yet"

    def slotAddPath(self):
        print "ControlPanelForm.slotAddPath(): Not implemented yet"

    def slotRemovePath(self):
        print "ControlPanelForm.slotRemovePath(): Not implemented yet"

    def slotPathSelectionChanged(self):
        print "ControlPanelForm.slotPathSelectionChanged(): Not implemented yet"

    def slotPitchRangeChanged(self,a0):
        print "ControlPanelForm.slotPitchRangeChanged(const QString&): Not implemented yet"

    def slotMainOutputSelected(self,a0):
        print "ControlPanelForm.slotMainOutputSelected(QListBoxItem*): Not implemented yet"

    def slotCueOutputSelected(self,a0):
        print "ControlPanelForm.slotCueOutputSelected(QListBoxItem*): Not implemented yet"

    def slotUpdateInterval(self,a0):
        print "ControlPanelForm.slotUpdateInterval(int): Not implemented yet"

    def setDirty(self):
        print "ControlPanelForm.setDirty(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("ControlPanelForm",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = ControlPanelForm()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
