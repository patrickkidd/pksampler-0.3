#include "group_edit_button.inc"

          
PK_Camera()
PK_Light()

difference {
   PK_OuterPlane()
   ButtonIndentShape
}
                
DrawGroupEditButton(ButtonClockedColor())                
