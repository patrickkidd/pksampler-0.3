#include "tool_button.inc"

          
PK_Camera()
PK_Light() 


difference {
   PK_Plane()
   ButtonIndentShape
}

                
DrawToolButton(ButtonClockedColor())  

