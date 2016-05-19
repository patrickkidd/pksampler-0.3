#include "pitch_center_button.inc"
 
          
PK_Camera()
PK_Light()
   

difference {
   PK_Plane()
   ButtonIndentShape
   scale <.75,1,1>
}

DrawPitchCenterButton(ButtonClockedColor())
          
  
