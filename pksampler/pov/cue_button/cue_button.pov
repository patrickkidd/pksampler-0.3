
#include "cue_button.inc"


PK_Light()
PK_Camera()
   
difference {
   PK_Plane()
   TapButtonIndentShape
}                                 

DrawCueButton(ButtonClockedColor())
